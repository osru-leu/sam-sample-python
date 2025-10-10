# Sample Python Application

A Flask-based Python application demonstrating enterprise deployment workflows using the `test-flow` repository for deployment validation and orchestration.

## 📋 Quick Links

- **[Deployment Guide](DEPLOYMENT.md)** - Complete deployment instructions and scenarios
- **[Flow Diagrams](FLOW-DIAGRAM.md)** - Visual flow diagrams matching the original design
- **[Test-Flow Repository](../test-flow/)** - Reusable deployment workflows and actions

## 🎯 What Makes This Special

This application demonstrates:
- ✅ **Reusable deployment workflows** from test-flow repository
- ✅ **Multi-stage validation gates** before deployment (matches the flow diagram)
- ✅ **Approval-based promotions** between environments
- ✅ **Automated testing** and quality checks
- ✅ **Environment-specific configurations**

## 🚀 Quick Start

### Run Locally
```bash
python run.py
# App runs on http://localhost:5000
```

### Auto-Deploy to DEV-INT
```bash
git push origin main
# ✅ Automatically deploys to DEV-INT environment
```

### Manual Deploy to FUTURE
```bash
gh workflow run deploy-to-environments.yml \
  -f environment=future \
  -f release_type=future
```

### Promote to Production
```bash
gh workflow run promote-app.yml \
  -f release_id=staging-20250110-120000 \
  -f source_environment=staging \
  -f target_environment=prod
```

## 🏗️ Application Structure

```
sample-python/
├── app/                    # Application code
│   ├── __init__.py        # Flask app factory
│   ├── routes.py          # API endpoints
│   ├── task_manager.py    # Business logic
│   └── utils.py           # Utilities
├── test/                  # Unit tests
│   └── test_routes.py
├── .github/workflows/     # Deployment workflows
│   ├── deploy-to-environments.yml  # Uses test-flow actions
│   └── promote-app.yml             # Promotion with approvals
├── deploy/helm/           # Kubernetes Helm charts
├── dockerfile             # Docker image definition
└── requirements.txt       # Python dependencies
```

## 🔄 Deployment Flow

This implementation **exactly matches** the original flow diagram:

```
GitHub Actions → Lifecycle Validation → Branch Validation → Release Check → Deploy ✅
                        ↓ Fail              ↓ Fail           ↓ Fail
                    Stop ❌             Stop ❌          Stop ❌
```

See [FLOW-DIAGRAM.md](FLOW-DIAGRAM.md) for detailed visual diagrams.

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Full deployment guide with examples
- **[FLOW-DIAGRAM.md](FLOW-DIAGRAM.md)** - Visual diagrams and architecture
- **[Test-Flow Actions](../test-flow/.github/actions/)** - Reusable validation actions

## 🧪 Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
pytest test/ -v --cov=app
```

### Build Docker Image
```bash
docker build -t sample-python:latest -f dockerfile .
```

### Run with Docker
```bash
docker run -p 5000:5000 sample-python:latest
```

## 🌍 Environments

| Environment | Trigger | Approvals | Purpose |
|------------|---------|-----------|---------|
| **DEV-INT** | Auto (main push) | None | Integration testing |
| **FUTURE** | Manual | None | Next version preview |
| **ACTIVE** | Manual | None | Current stable release |
| **UAT** | Promotion | 1 | Partner testing |
| **STAGING** | Promotion | 1 | Pre-production |
| **PROD** | Promotion | 2+ | Live production |

## ✨ Features

- 🎯 RESTful API with Flask
- 🧪 Unit tests with pytest
- 🐳 Docker containerization
- ☸️ Kubernetes Helm charts
- 🔄 Automated CI/CD workflows
- 🔒 Multi-stage approval gates
- 📊 Environment-specific configs
