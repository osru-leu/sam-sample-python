# Sam Sample Python Application

A Flask-based Python application demonstrating **multi-repository architecture** where application code lives in one repo and deployment workflows are centralized in another.

## 🏢 Two-Repo Architecture

This setup uses **TWO SEPARATE REPOSITORIES**:

### 1. **test-flow** (Workflow Library)
- 📦 Location: `github.com/ALTIMETRIK/test-flow`
- 🎯 Purpose: Centralized deployment workflows and validation actions
- 📝 Contents: Reusable composite actions, deployment logic, validation rules

### 2. **sam-sample-python** (Application Code - THIS REPO)
- 📦 Location: `github.com/ALTIMETRIK/sam-sample-python`
- 🎯 Purpose: Flask application code
- 📝 Contents: Python app, tests, Dockerfile, workflows that **CALL** test-flow

```
┌─────────────────────────────────────────────────────────┐
│  sam-sample-python (Application Repo)                  │
│  ├── app/                  ← Your application code     │
│  ├── test/                 ← Your tests                │
│  └── .github/workflows/    ← Calls test-flow actions  │
│         ↓ uses actions from ↓                          │
└─────────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│  test-flow (Workflow Library - SEPARATE REPO)          │
│  └── .github/actions/      ← Reusable actions          │
│      ├── deployment-lifecycle-validation/              │
│      ├── branch-validation/                            │
│      ├── release-check/                                │
│      ├── deploy-to-release/                            │
│      └── promotion actions...                          │
└─────────────────────────────────────────────────────────┘
```

## 🔗 How It Works

```yaml
# In sam-sample-python/.github/workflows/deploy-to-environments.yml

steps:
  # 1. Get test-flow repository (EXTERNAL REPO)
  - name: Checkout test-flow
    uses: actions/checkout@v4
    with:
      repository: ALTIMETRIK/test-flow  # ← Different repo!
      path: test-flow

  # 2. Get sam-sample-python (THIS REPO)
  - uses: actions/checkout@v4
    with:
      path: sam-sample-python

  # 3. Use test-flow validation action
  - uses: ./test-flow/.github/actions/deployment-lifecycle-validation
    with:
      environment: dev-int
      branch: main
```

**Key Point:** sam-sample-python **calls** test-flow actions, they are **separate repositories**!

## 📋 Quick Links

- **[Architecture Guide](ARCHITECTURE.md)** - Two-repo architecture explained
- **[Deployment Guide](DEPLOYMENT.md)** - Complete deployment instructions
- **[Flow Diagrams](FLOW-DIAGRAM.md)** - Visual architecture diagrams
- **[Integration Summary](INTEGRATION-SUMMARY.md)** - How the two repos connect
- **[test-flow Repository](https://github.com/ALTIMETRIK/test-flow)** - Workflow library (separate repo)

## 🎯 What Makes This Special

This application demonstrates **enterprise-grade deployment architecture**:
- ✅ **Separation of Concerns**: App code separate from deployment logic
- ✅ **Reusable Workflows**: test-flow actions used by multiple apps
- ✅ **Multi-stage Validation**: Deployment lifecycle → Branch → Release checks
- ✅ **Approval Gates**: Human oversight for critical promotions
- ✅ **Centralized Governance**: One place to update deployment rules

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
