# New Service Checklist & Validation Process

## Mandatory Requirements
- [ ] **Integrity Tests:** Implement `test_integrity.py` using the template and guidelines
- [ ] **Config Validation:** Ensure all critical registries/configs are validated (choices, rate limits, endpoints, etc.)
- [ ] **CI Integration:** Add integrity tests to the CI pipeline and require passing status for merges
- [ ] **Branch Protection:** Ensure branch protection rules require passing integrity tests
- [ ] **Documentation:** Update onboarding and service docs with integrity testing details
- [ ] **Code Review:** Include integrity test coverage in code review checklist

## Automated Validation Script (Outline)
- Scan new service repos for `test_integrity.py`
- Check for required test patterns (registry, config, env var, DB/API checks)
- Validate CI config includes integrity test step
- Generate compliance report (pass/fail, missing items)
- Integrate with pre-commit hooks and CI for automated enforcement

## Integration with Development Workflow
- Add checklist to PR template for new services
- Run validation script as part of CI and pre-commit
- Require code review sign-off for integrity test compliance

---

For more details, see [Testing Guidelines](./testing-guidelines.md) and [Onboarding Guide](./onboarding.md).

# use context7 use taskmaster 