# Backend Registry/Config Integrity Testing Guidelines

## Overview

This document describes the standardized approach for implementing registry/configuration integrity tests across all backend microservices and Python packages in this project. The goal is to ensure that all critical registries (choices, configs, rate limits, API endpoints, etc.) are validated automatically, preventing drift, duplication, or omissions.

## Why Integrity Testing?
- Prevents silent errors from misconfigured registries or missing config values
- Catches accidental duplication or drift between code and configuration
- Ensures all services meet a baseline of reliability and maintainability

## Step-by-Step Implementation

1. **Copy the Template**
   - Start with `backend/test_integrity_template.py` as your base.
   - Place the file in your new service or package as `test_integrity.py`.

2. **Customize Fixtures and Tests**
   - Replace the `sample_registry` fixture with your service's actual registry/config loading logic.
   - Add or modify test functions to cover all critical registries, configs, and dependencies for your service.

3. **Add Service-Specific Checks**
   - Validate all required environment variables are present.
   - Add database connection and API endpoint health checks.
   - Check for required service dependencies (e.g., Redis, Celery, external APIs).

4. **Integrate with CI**
   - Ensure your CI pipeline runs `pytest test_integrity.py` on every push and pull request.
   - Configure branch protection rules to require passing integrity tests before merging.

5. **Troubleshooting**
   - If a test fails, review the error message and check for missing/duplicate registry entries, config drift, or incomplete exports.
   - Use the inline comments in the template for guidance.

## Code Examples

### Django Service Example
```python
# test_integrity.py
import pytest
from myapp import models

def test_model_choices_unique():
    values = [v for v, _ in models.MyModel.CHOICES]
    assert len(values) == len(set(values)), "Duplicate values in CHOICES"
```

### Standalone Package Example
```python
# test_integrity.py
import pytest
from mypackage.config import REGISTRY

def test_registry_no_duplicates():
    assert len(REGISTRY) == len(set(REGISTRY)), "Duplicate entries in REGISTRY"
```

## Test Naming and Organization
- Name your file `test_integrity.py` for consistency.
- Group related tests by registry/config type.
- Use fixtures for setup and utility functions for common logic.

## CI Integration
- Add a step in your CI workflow to run integrity tests (see `.github/workflows/ci.yml`).
- Ensure CI fails if any integrity test fails.
- Upload test results to the CI summary for visibility.

## Architectural Diagram
```
flowchart TD
    A[Registry/Config] -->|Validated by| B[test_integrity.py]
    B -->|Run in| C[CI Pipeline]
    C -->|Status Check| D[Branch Protection]
```

## Troubleshooting
- **Missing Env Vars:** Ensure all required environment variables are set in your CI and local environment.
- **Test Failures:** Review error messages and check for typos, missing configs, or outdated registry entries.
- **CI Issues:** Confirm that the test file is included in the test discovery path and that dependencies are installed.

## References
- [test_integrity_template.py](../backend/test_integrity_template.py)
- [README.md Testing Standards Section](../README.md)

# use context7 use taskmaster 