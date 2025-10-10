# Two-Repository Setup Guide

## Quick Reference: sam-sample-python + test-flow

This document explains how to set up and use the two-repository architecture.

## 📦 The Two Repositories

### Repository 1: test-flow
```
URL: https://github.com/ALTIMETRIK/test-flow
Purpose: Centralized workflow library
Owner: Platform/DevOps team
Access: Read access for all developers
```

**Contains:**
- ✅ Reusable deployment actions
- ✅ Validation logic
- ✅ Promotion workflows
- ✅ Documentation
- ❌ NO application code
- ❌ NO application secrets

### Repository 2: sam-sample-python (THIS REPO)
```
URL: https://github.com/ALTIMETRIK/sam-sample-python
Purpose: Flask application
Owner: Application development team
Access: Write access for app developers
```

**Contains:**
- ✅ Flask application code
- ✅ Unit tests
- ✅ Dockerfile
- ✅ Helm charts
- ✅ Workflows that CALL test-flow
- ✅ Application secrets (in GitHub environments)

## 🔧 Setup Instructions

### Step 1: Ensure Both Repos Exist

```bash
# Clone both repositories
git clone https://github.com/ALTIMETRIK/test-flow.git
git clone https://github.com/ALTIMETRIK/sam-sample-python.git

# Verify structure
cd test-flow
ls .github/actions/  # Should see validation actions

cd ../sam-sample-python
ls .github/workflows/  # Should see deploy-to-environments.yml
```

### Step 2: Verify Workflow Configuration

Check that `sam-sample-python` workflows reference `test-flow` correctly:

```yaml
# In sam-sample-python/.github/workflows/deploy-to-environments.yml

- name: Checkout test-flow repository
  uses: actions/checkout@v4
  with:
    repository: ${{ github.repository_owner }}/test-flow  # ← Must match your org
    path: test-flow
```

**Important:** Replace `${{ github.repository_owner }}` with your actual GitHub organization if needed!

### Step 3: Set Up GitHub Environments

In **sam-sample-python** repository (not test-flow!):

1. Go to **Settings** → **Environments**
2. Create these environments:
   - `dev-int` (no protection)
   - `future` (no protection)
   - `active` (optional protection)
   - `promotion-approval-uat` (1 reviewer)
   - `uat` (environment secrets)
   - `promotion-approval-staging` (1 reviewer)
   - `staging` (environment secrets)
   - `promotion-approval-prod` (2+ reviewers)
   - `prod` (strict protection + secrets)

### Step 4: Add Environment Secrets

In **sam-sample-python** → **Settings** → **Environments** → [environment name] → **Secrets**:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
DOCKER_REGISTRY_URL
KUBECONFIG (or K8S_CLUSTER_URL)
DATABASE_URL
API_KEY
```

**Note:** Secrets go in sam-sample-python, NOT in test-flow!

### Step 5: Test the Setup

```bash
cd sam-sample-python

# Test auto-deploy to DEV-INT
git checkout -b test-deploy
echo "# test" >> README.md
git add README.md
git commit -m "test: trigger deploy"
git push origin test-deploy

# Merge to main (triggers auto-deploy)
gh pr create --base main --title "Test deployment"
gh pr merge --squash
```

Check GitHub Actions tab to verify workflow runs and calls test-flow actions!

## 🎯 How Actions Are Called

### Pattern Explanation

```yaml
# Step 1: Checkout test-flow (external repo)
- name: Checkout test-flow repository
  uses: actions/checkout@v4
  with:
    repository: ALTIMETRIK/test-flow    # External repo reference
    path: test-flow                     # Local folder name

# Step 2: Checkout sam-sample-python (current repo)
- name: Checkout sam-sample-python
  uses: actions/checkout@v4
  with:
    path: sam-sample-python             # Local folder name

# Step 3: Use action from test-flow
- name: Run Validation
  uses: ./test-flow/.github/actions/deployment-lifecycle-validation
  #     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  #     Local path to the checked out test-flow repo
```

### Why This Works

1. GitHub Actions checks out test-flow repo into `./test-flow/` directory
2. GitHub Actions checks out sam-sample-python into `./sam-sample-python/`
3. Actions are available locally and can be referenced via path
4. No need to publish actions to GitHub Marketplace!

### Visual Representation

```
GitHub Actions Runner:
├── test-flow/                      ← Checked out from ALTIMETRIK/test-flow
│   └── .github/actions/
│       └── deployment-lifecycle-validation/
│           └── action.yml          ← Used here!
│
└── sam-sample-python/              ← Checked out from ALTIMETRIK/sam-sample-python
    ├── app/
    └── .github/workflows/
        └── deploy-to-environments.yml  ← Calling action
```

## 🔐 Repository Permissions

### test-flow Repository

**Who needs access:**
- ✅ Platform team: **Write** access
- ✅ All developers: **Read** access (to use actions)

**GitHub Settings:**
```
Settings → General → Visibility
- Internal or Public (so apps can access)

Settings → Manage Access
- Platform team: Maintain or Admin
- Developers: Read (automatic if internal)
```

### sam-sample-python Repository

**Who needs access:**
- ✅ App team: **Write** access
- ✅ Platform team: **Read** or **Triage** access

**GitHub Settings:**
```
Settings → General → Visibility
- Private or Internal (contains business logic)

Settings → Manage Access
- App developers: Write or Maintain
- Platform team: Read or Triage
```

## 🐛 Troubleshooting

### Error: "Repository not found"

```yaml
Error: repository 'ALTIMETRIK/test-flow' not found
```

**Solutions:**
1. Verify test-flow repository exists
2. Check repository visibility (must be accessible to sam-sample-python)
3. Verify organization name is correct
4. Ensure GitHub token has access to both repos

### Error: "Action not found"

```yaml
Error: Unable to resolve action ./test-flow/.github/actions/..., 
unable to find version ''
```

**Solutions:**
1. Verify checkout step completed successfully
2. Check path is correct: `./test-flow/.github/actions/...`
3. Verify action.yml exists in test-flow repo
4. Check spelling of action name

### Error: "Permission denied"

```yaml
Error: Resource not accessible by integration
```

**Solutions:**
1. Check repository permissions
2. Verify GITHUB_TOKEN has necessary scopes
3. For cross-organization: may need PAT (Personal Access Token)

### Workflow Doesn't Trigger

**Check:**
1. Workflow file is in correct location: `.github/workflows/`
2. YAML syntax is valid: `yamllint deploy-to-environments.yml`
3. Workflow is enabled: Settings → Actions → Enable workflows
4. Branch protection isn't blocking: Settings → Branches

## 📝 Adding New Applications

To add another app using test-flow:

### 1. Create New App Repository
```bash
gh repo create ALTIMETRIK/new-python-app --private
cd new-python-app
```

### 2. Copy Workflow Template
```bash
# Copy from sam-sample-python
cp ../sam-sample-python/.github/workflows/deploy-to-environments.yml \
   .github/workflows/deploy.yml
```

### 3. Update References
```yaml
# In .github/workflows/deploy.yml
# Update any app-specific references:
# - Image names
# - Application name
# - Specific build steps
```

### 4. Add Application Code
```bash
# Add your application files
mkdir -p app
echo "# New App" > README.md
```

### 5. Test
```bash
git add .
git commit -m "feat: initial setup"
git push origin main
# Watch GitHub Actions run!
```

**That's it!** New app immediately has full deployment workflow with all validation gates.

## 🎓 Best Practices

### DO ✅

1. **Keep test-flow generic** - No app-specific logic
2. **Add app logic in app repos** - sam-sample-python contains app-specific steps
3. **Version test-flow** - Use tags/releases for stability
4. **Document changes** - Update test-flow README when changing actions
5. **Test in dev first** - Validate test-flow changes before production use

### DON'T ❌

1. **Don't put secrets in test-flow** - They belong in app repos
2. **Don't hardcode values** - Use inputs for flexibility
3. **Don't break backward compatibility** - Other apps depend on test-flow
4. **Don't mix concerns** - Keep validation logic in test-flow, app logic in apps
5. **Don't skip testing** - Changes to test-flow affect all apps!

## 📊 Comparison with Alternatives

### vs. Monorepo
```
Two-Repo Approach:
✅ Clear boundaries
✅ Independent versioning
✅ Easier access control
❌ More complex setup

Monorepo:
✅ Simpler initially
❌ Everything together
❌ Harder to control access
❌ Slower CI/CD
```

### vs. Duplicated Workflows
```
Two-Repo (Reusable):
✅ Update once
✅ Consistent across apps
✅ Easy to maintain
✅ Scales well

Duplicated:
❌ Update 20 times
❌ Inconsistencies
❌ Hard to maintain
❌ Doesn't scale
```

### vs. GitHub Marketplace Actions
```
Two-Repo (Private):
✅ Full control
✅ Internal only
✅ Custom to your needs
❌ Self-maintained

Marketplace:
✅ Community maintained
❌ Public only
❌ Generic solutions
❌ Less control
```

## 🔄 Updating test-flow

When you update test-flow actions:

```bash
cd test-flow

# Make changes to actions
vim .github/actions/deployment-lifecycle-validation/action.yml

# Test changes
git checkout -b update-validation
git add .
git commit -m "feat: add new validation check"
git push origin update-validation

# Create PR and merge
gh pr create
gh pr merge

# Tag a release (optional but recommended)
git tag -a v1.1.0 -m "Add new validation check"
git push origin v1.1.0
```

**Result:** All apps using test-flow automatically get the update on next run!

## 📈 Scaling to Multiple Apps

```
test-flow (one repo)
    ↓ used by
    ├─→ sam-sample-python
    ├─→ another-python-app
    ├─→ java-microservice
    ├─→ nodejs-api
    ├─→ go-service
    └─→ ... (unlimited apps)

One update → All apps benefit
```

## Summary

**Two-Repository Architecture:**
- ✅ **test-flow** = Workflow library (reusable actions)
- ✅ **sam-sample-python** = Application code (calls test-flow)
- ✅ Clear separation of concerns
- ✅ Easy to maintain and scale
- ✅ Enterprise-grade approach

The setup is complete and ready to use! 🚀

