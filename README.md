## Technical Store System

An advanced multi-store inventory management system with analytics, mobile integration, vendor management, compliance, and audit trails.

**Version:** 0.0.1  
**Author:** Nadeem  
**Email:** zahid_printers@yahoo.com  
**License:** MIT

### Features

- Multi-store inventory management
- Advanced analytics and reporting
- Mobile integration for on-the-go access
- Comprehensive vendor management
- Compliance and audit trails
- Built on Frappe Framework

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app technical_store_system
```

### Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet and quick patterns
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Complete development workflow and troubleshooting
- **[.cursorrules](.cursorrules)** - AI assistant guidelines and coding standards

### Development Workflow

**Important**: This app follows an incremental development approach - ONE feature at a time.

```bash
# Quick start
cd ~/frappe-bench
bench --site [site] install-app technical_store_system
bench start

# Create feature
git checkout -b feature/your-feature
bench --site [site] new-doctype
bench --site [site] migrate

# Test and commit
bench --site [site] run-tests --app technical_store_system
git commit -m "feat: Add feature description"
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for complete workflow guide.

### Contributing

This app uses `pre-commit` for code formatting and linting:

```bash
cd apps/technical_store_system
pre-commit install
```

**Code Quality Tools:**
- ruff (Python linting and formatting)
- eslint (JavaScript linting)
- prettier (Code formatting)
- pyupgrade (Python syntax upgrades)

### Backup & Safety

**Before major changes:**
```bash
# ZFS snapshot (if using ZFS)
sudo zfs snapshot zstore/frappe-bench@before-work

# Database backup
bench --site [site] backup --with-files
```

### CI/CD

GitHub Actions configured for:
- **CI**: Unit tests on push to `develop`
- **Linters**: [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on PRs


### License

mit
