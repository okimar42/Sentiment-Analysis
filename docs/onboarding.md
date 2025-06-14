# Developer Onboarding Guide

## Welcome!

This guide will help you get started as a contributor to this project. Please follow each step carefully to ensure a smooth onboarding experience.

---

## 1. Project Setup
- Clone the repository and install dependencies (see README.md).
- Set up your development environment (Docker, Python, Node.js, etc.).

## 2. Code Standards & Workflow
- Follow the [Cursor Project Rules Index](../.cursorrules) for all development.
- Use Taskmaster for task management and workflow.

## 3. Mandatory Integrity Testing for New Services
- **All new backend microservices and Python packages must implement registry/config integrity tests.**
- Use the [test_integrity_template.py](../backend/test_integrity_template.py) as a starting point.
- Follow the [Testing Guidelines](./testing-guidelines.md) for step-by-step instructions.

### Integrity Testing Checklist
- [ ] Copy and customize `test_integrity_template.py` for your service
- [ ] Validate all registries/configs (choices, rate limits, endpoints, etc.)
- [ ] Add environment variable, DB, and API health checks
- [ ] Integrate integrity tests into your CI pipeline
- [ ] Ensure branch protection requires passing integrity tests
- [ ] Review and update documentation as needed

### Hands-On Exercise
- Implement a `test_integrity.py` for your new service using the template
- Run the tests locally and in CI
- Submit a PR and verify that integrity tests pass before merging

## 4. Integration with Development Workflows
- Use pre-commit hooks and code review checklists to enforce integrity testing
- Reference the [Testing Guidelines](./testing-guidelines.md) for troubleshooting and best practices

## 5. Verification Steps
- Confirm that all integrity tests pass locally and in CI
- Ensure your service is compliant with the integrity testing standard before requesting review

---

For questions or help, contact the maintainers or refer to the documentation links above.

# use context7 use taskmaster 