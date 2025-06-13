# Troubleshooting

Having issues running the processor?  Check the sections below before opening
an issue.

---

## Common runtime errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: praw` | Dependencies missing | `pip install -r backend/requirements.txt` |
| `openai.error.AuthenticationError` | `OPENAI_API_KEY` not exported / wrong | Verify key spelling & environment; `echo $OPENAI_API_KEY` |
| `TooManyRequestsError` (OpenAI) | GPT-4 rate-limit | Reduce `--max-posts`, move to VADER-only, upgrade plan |
| Script exits silently / zero posts | Query typo or subreddits private | Double-check `-q` value & Reddit credentials |
| SQLite file empty | Script crashed before commit | Re-run or inspect logs for upstream error |

---

## Verbose logging

Set env var `LOG_LEVEL=DEBUG` (supported by the root logger in `sentiment_processor.py`) to print extra information including API payload sizes and retry attempts.

---

## Network & Proxy settings

* All HTTP traffic is outbound only.
* Respect `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY` env vars if set.
* For corporate proxies ensure they allow `api.openai.com`, `api.twitter.com`, and `oauth.reddit.com`.

---

## Data privacy

No secrets are written to disk.  However output files may contain user-generated
content from Reddit/Twitter – treat them according to your data handling
policies.

---

## Still stuck?

Run with `--dry-run` to validate configuration without hitting external APIs.
If the problem persists gather logs with `LOG_LEVEL=DEBUG` and share them when
requesting help.