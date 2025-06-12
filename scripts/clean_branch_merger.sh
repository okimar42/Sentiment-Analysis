#!/usr/bin/env bash

# clean_branch_merger.sh
# -------------------------------------------------------------
# A configurable, safety-first automation script that merges
# eligible branches into main while preserving repository
# integrity.  Designed to be idempotent and usable both in CI
# and locally.
# -------------------------------------------------------------

set -euo pipefail

############################################
# Helper: usage information                #
############################################
usage() {
  cat <<EOF
Usage: $0 [options]

Options:
  --dry-run                  Simulate actions but do not push or merge
  --max-branches <num>       Limit number of branches to process (defaults to unlimited)
  --exclude-patterns <list>  Comma-separated list of additional branch glob patterns to skip
  --require-tests            Run project tests after each merge; abort on failure
  --notification-webhook <url>  POST final JSON report to the given webhook
  -h, --help                 Show this help and exit
EOF
}

############################################
# Default configuration                    #
############################################
DRY_RUN=false
MAX_BRANCHES=0   # 0 means unlimited
EXTRA_EXCLUDE=""
REQUIRE_TESTS=false
WEBHOOK=""

############################################
# Parse CLI arguments                      #
############################################
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --max-branches) MAX_BRANCHES="$2"; shift 2 ;;
    --exclude-patterns) EXTRA_EXCLUDE="$2"; shift 2 ;;
    --require-tests) REQUIRE_TESTS=true; shift ;;
    --notification-webhook) WEBHOOK="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option $1" >&2; usage; exit 1 ;;
  esac
done

############################################
# Global variables                         #
############################################
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Filter patterns
PROTECTED_PATTERNS=("develop" "staging" "release/*")
PERSONAL_PATTERNS=("feature/experimental-*" "personal/*")
READY_PATTERNS=("feature/*" "bugfix/*" "hotfix/*" "cursor/*")

# Convert comma separated extra excludes into array
IFS=',' read -ra EXTRA <<< "$EXTRA_EXCLUDE"

############################################
# Utility functions                        #
############################################
log() { echo "[$(date +%H:%M:%S)] $*"; }
error() { echo "[ERROR] $*" >&2; }

check_cmd() { command -v "$1" >/dev/null 2>&1; }

has_do_not_merge_label() {
  local branch="$1"
  if ! check_cmd gh; then return 1; fi
  local pr_json
  pr_json=$(gh pr list --head "$branch" --json labels -q '.[0].labels[].name' 2>/dev/null || true)
  [[ "$pr_json" == *"DO-NOT-MERGE"* ]]
}

has_open_pr() {
  local branch="$1"
  if ! check_cmd gh; then return 1; fi
  gh pr list --head "$branch" --state open --limit 1 -q '.[].number' | grep -qE '^[0-9]+'
}

branch_is_ahead_of_main() {
  local branch="$1"
  git rev-list --left-right --count "main...$branch" | awk '{exit $1==0}'
}

contains_sensitive_diff() {
  local branch="$1"
  git diff --unified=0 "origin/main..$branch" | grep -E --ignore-case "(secret|password|token|aws_access_key|private_key)" -q && return 0 || return 1
}

run_tests() {
  if [ -f "package.json" ] && check_cmd npm; then
    npm test --silent
  elif [ -f "pytest.ini" ] || ls tests/*.py >/dev/null 2>&1; then
    check_cmd pytest && pytest -q
  else
    log "No test suite detected; skipping tests"
  fi
}

post_webhook() {
  local payload="$1"
  if [ -n "$WEBHOOK" ]; then
    curl -s -X POST -H "Content-Type: application/json" -d "$payload" "$WEBHOOK" || true
  fi
}

############################################
# Main logic                               #
############################################
log "Fetching latest data from origin"
 git fetch --all --prune

BACKUP_TAG="backup-pre-merge-$(date +%Y%m%d-%H%M%S)"
log "Creating backup tag $BACKUP_TAG"
 $DRY_RUN || git tag "$BACKUP_TAG" && git push origin "$BACKUP_TAG" >/dev/null 2>&1

# Determine candidate branches
mapfile -t REMOTE_BRANCHES < <(git for-each-ref --format='%(refname:strip=3)' refs/remotes/origin)

CANDIDATES=()
for br in "${REMOTE_BRANCHES[@]}"; do
  # Skip main/master equivalent
  [[ "$br" == "main" || "$br" == "master" ]] && continue

  # Exclude protected patterns
  skip=false
  for pat in "${PROTECTED_PATTERNS[@]}"; do
    [[ "$br" == $pat ]] && { skip=true; break; }
  done
  # Exclude personal patterns
  if ! $skip; then
    for pat in "${PERSONAL_PATTERNS[@]}"; do
      [[ "$br" == $pat ]] && { skip=true; break; }
    done
  fi
  # Exclude extra patterns
  if ! $skip && [ ${#EXTRA[@]} -gt 0 ]; then
    for pat in "${EXTRA[@]}"; do
      [[ "$br" == $pat ]] && { skip=true; break; }
    done
  fi
  # Must match ready pattern
  if ! $skip; then
    ready_match=false
    for pat in "${READY_PATTERNS[@]}"; do
      [[ "$br" == $pat ]] && { ready_match=true; break; }
    done
    $ready_match || skip=true
  fi

  $skip || CANDIDATES+=("$br")

done

log "Found ${#CANDIDATES[@]} candidate branches after filtering"

MERGED=()
SKIPPED=()
MANUAL_REVIEW=()

COUNT=0
for br in "${CANDIDATES[@]}"; do
  ((MAX_BRANCHES)) && [ $COUNT -ge $MAX_BRANCHES ] && { log "Reached max branches limit ($MAX_BRANCHES)"; break; }
  ((COUNT++))

  log "Processing $br"

  branch_is_ahead_of_main "origin/$br" || { log " -> Branch not ahead of main; skipping"; SKIPPED+=("$br (no new commits)"); continue; }

  if has_open_pr "$br"; then
    log " -> Active PR found for $br; skipping"
    SKIPPED+=("$br (active PR)")
    continue
  fi

  if has_do_not_merge_label "$br"; then
    log " -> DO-NOT-MERGE label detected; skipping"
    SKIPPED+=("$br (DO-NOT-MERGE)")
    continue
  fi

  if contains_sensitive_diff "origin/$br"; then
    log " -> Security-sensitive changes detected; sending to manual review"
    MANUAL_REVIEW+=("$br (sensitive diff)")
    continue
  fi

  git checkout main >/dev/null 2>&1
  git pull origin main >/dev/null 2>&1
  git checkout -B merge-temp "origin/$br" >/dev/null 2>&1
  log " -> Rebasing $br onto main"
  git rebase origin/main || { error "Rebase failed for $br; manual resolution required"; MANUAL_REVIEW+=("$br (rebase conflicts)"); git rebase --abort || true; continue; }

  git checkout main >/dev/null 2>&1

  if git merge --no-commit --no-ff "merge-temp" >/dev/null 2>&1; then
    git merge --abort >/dev/null 2>&1 # dry-run merge succeeded
  else
    error " -> Merge conflicts detected; manual review required"
    MANUAL_REVIEW+=("$br (merge conflicts)")
    git merge --abort || true
    continue
  fi

  if $DRY_RUN; then
    log " -> Dry-run enabled; merge simulated successfully"
  else
    log " -> Performing merge"
    git merge --no-ff "merge-temp" -m "Merge $br into main"

    if $REQUIRE_TESTS; then
      log " -> Running tests"
      if ! run_tests; then
        error "Tests failed after merging $br; reverting merge"
        git reset --hard HEAD~1
        MANUAL_REVIEW+=("$br (tests failed)")
        continue
      fi
    fi

    log " -> Pushing main to origin"
    git push origin main
    MERGED+=("$br")
  fi

done

# Cleanup temp branch if it exists
 git branch -D merge-temp >/dev/null 2>&1 || true

############################################
# Reporting                                #
############################################
REPORT=$(cat <<JSON
{
  "timestamp": "$(date -Iseconds)",
  "dry_run": $DRY_RUN,
  "merged": $(printf '%s
' "${MERGED[@]}" | jq -R -s -c 'split("\n")[:-1]'),
  "skipped": $(printf '%s
' "${SKIPPED[@]}" | jq -R -s -c 'split("\n")[:-1]'),
  "manual_review": $(printf '%s
' "${MANUAL_REVIEW[@]}" | jq -R -s -c 'split("\n")[:-1]'),
  "backup_tag": "$BACKUP_TAG"
}
JSON
)

echo "\n===== SUMMARY ====="
echo "$REPORT" | jq . || echo "$REPORT"

post_webhook "$REPORT"

log "Done"