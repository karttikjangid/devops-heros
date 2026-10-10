# Security checks

Bandit scans the application source, pip-audit checks Python dependencies, Gitleaks scans the demo directory and Trivy scans the built container. Findings stop the workflow before publishing or deployment. Credentials use GitHub Actions secrets and are not committed.
