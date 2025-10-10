# Sample Python App - Visual Flow Diagrams

## How Sample-Python Uses Test-Flow

```mermaid
flowchart TD
    subgraph "Sample Python App Repository"
        A[Push to main] --> B[deploy-to-environments.yml]
        C[Manual Trigger] --> B
        D[Promotion Request] --> E[promote-app.yml]
    end
    
    subgraph "Test-Flow Repository Actions Used"
        F[deployment-lifecycle-validation]
        G[branch-validation]
        H[release-check]
        I[deploy-to-release]
        J[promotion-validation]
        K[pre-promotion-checks]
        L[execute-promotion]
        M[post-promotion-verification]
    end
    
    B --> F
    B --> G
    B --> H
    B --> I
    
    E --> J
    E --> K
    E --> L
    E --> M
    
    style A fill:#90EE90
    style C fill:#FFD700
    style D fill:#87CEEB
```

## Exact Match to Original Diagram

This is how the original diagram maps to the implementation:

```mermaid
flowchart TD
    A["GitHub Actions<br/>(Deployment Trigger)"] --> B{"Deployment<br/>Lifecycle Validation"}
    B -->|Yes| C["Branch Validation"]
    B -->|No| Z["Workflow Stops<br/>(Failure)"]
    C --> D["Future or Active Release"]
    D -->|Yes| E["Deploy to Future Release<br/>Duration - Unlimited"]
    D -->|Check fails| Z
    
    style A fill:#FFD700,stroke:#333,stroke-width:2px
    style B fill:#B0C4DE,stroke:#333,stroke-width:2px
    style C fill:#B0C4DE,stroke:#333,stroke-width:2px
    style D fill:#F5DEB3,stroke:#333,stroke-width:2px
    style E fill:#90EE90,stroke:#333,stroke-width:2px
    style Z fill:#FFB6C6,stroke:#333,stroke-width:2px
```

### Implementation Mapping:

| Diagram Element | Implementation | File Location |
|----------------|----------------|---------------|
| **GitHub Actions (Deployment Trigger)** | `deploy-to-environments.yml` | `sample-python/.github/workflows/` |
| **Deployment Lifecycle Validation** | Job: `deployment-lifecycle-validation` | Uses `test-flow/.github/actions/deployment-lifecycle-validation` |
| **Branch Validation** | Job: `branch-validation` | Uses `test-flow/.github/actions/branch-validation` |
| **Future or Active Release** | Job: `release-check` | Uses `test-flow/.github/actions/release-check` |
| **Deploy to Future Release** | Job: `deploy-to-environment` | Uses `test-flow/.github/actions/deploy-to-release` |
| **Workflow Stops (Failure)** | Automatic on any validation failure | Built-in to each action |

## Complete Deployment Sequence

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant GH as GitHub
    participant SP as sample-python workflow
    participant TF as test-flow actions
    participant ENV as Environment
    
    Dev->>GH: Push to main or trigger workflow
    GH->>SP: Start deploy-to-environments.yml
    
    SP->>SP: Build & Test Python App
    Note over SP: Runs pytest, builds image
    
    SP->>TF: deployment-lifecycle-validation
    TF-->>SP: ✅ Valid
    
    SP->>TF: branch-validation
    TF-->>SP: ✅ Valid
    
    SP->>TF: release-check (if future/active)
    TF-->>SP: ✅ Release available
    
    SP->>TF: deploy-to-release
    TF->>ENV: Deploy application
    ENV-->>TF: ✅ Deployed
    TF-->>SP: ✅ Success
    
    SP-->>Dev: Deployment complete!
```

## Promotion Flow with Approval Gates

```mermaid
stateDiagram-v2
    [*] --> Validate: Trigger Promotion
    Validate --> Approval: Validation Passed
    Validate --> Failed: Validation Failed
    
    Approval --> PreChecks: Approved by Reviewers
    Approval --> Rejected: Rejected
    
    PreChecks --> Execute: All Checks Passed
    PreChecks --> Failed: Checks Failed
    
    Execute --> Verify: Deployment Complete
    Verify --> Success: Verification Passed
    Verify --> Failed: Verification Failed
    
    Success --> [*]
    Failed --> [*]
    Rejected --> [*]
    
    note right of Validate
        Uses promotion-validation
        from test-flow
    end note
    
    note right of Approval
        GitHub Environment
        Protection Rules
    end note
    
    note right of PreChecks
        Uses pre-promotion-checks
        from test-flow
    end note
    
    note right of Execute
        Uses execute-promotion
        from test-flow
    end note
    
    note right of Verify
        Uses post-promotion-verification
        from test-flow
    end note
```

## Environment Promotion Paths

```mermaid
graph LR
    A[DEV-INT<br/>Auto-deploy] --> B[FUTURE<br/>Manual]
    A --> C[ACTIVE<br/>Manual]
    B --> C
    C --> D[UAT<br/>1 approval]
    C --> E[STAGING<br/>1 approval]
    D --> E
    E --> F[PROD<br/>2+ approvals]
    
    style A fill:#90EE90
    style B fill:#FFD700
    style C fill:#87CEEB
    style D fill:#DDA0DD
    style E fill:#F0E68C
    style F fill:#FFB6C6
```

## Workflow Job Dependencies

```mermaid
flowchart TD
    subgraph "deploy-to-environments.yml"
        A[build-and-test] --> B[deployment-lifecycle-validation]
        B --> C[branch-validation]
        C --> D[release-check]
        A --> E[build-docker]
        C --> E
        D --> F[deploy-to-environment]
        E --> F
        F --> G[auto-deploy-notification]
    end
    
    style A fill:#E6F3FF
    style B fill:#FFE6E6
    style C fill:#FFE6E6
    style D fill:#FFE6E6
    style E fill:#E6F3FF
    style F fill:#E6FFE6
    style G fill:#FFF9E6
```

```mermaid
flowchart TD
    subgraph "promote-app.yml"
        A[validate-promotion] --> B[approval-gate]
        B --> C[pre-promotion-checks]
        C --> D[promote-release]
        D --> E[post-promotion-verification]
    end
    
    style A fill:#FFE6E6
    style B fill:#FFE6CC
    style C fill:#FFE6E6
    style D fill:#E6FFE6
    style E fill:#E6F3FF
```

## Real-World Deployment Timeline

```mermaid
gantt
    title Sample Python App Release Timeline
    dateFormat  HH:mm
    axisFormat %H:%M
    
    section Development
    Feature Development     :dev, 00:00, 8h
    PR Review              :review, after dev, 2h
    Merge to main          :merge, after review, 5m
    Auto-deploy DEV-INT    :devint, after merge, 10m
    
    section Testing
    Deploy to FUTURE       :future, after devint, 15m
    QA Testing in FUTURE   :qa1, after future, 4h
    Promote to ACTIVE      :active, after qa1, 10m
    Regression Testing     :qa2, after active, 4h
    
    section UAT
    Request Promotion      :req1, after qa2, 5m
    Wait for Approval      :app1, after req1, 1h
    Promote to UAT         :uat, after app1, 15m
    Partner Testing        :partner, after uat, 8h
    
    section Pre-Prod
    Request Promotion      :req2, after partner, 5m
    Wait for Approval      :app2, after req2, 2h
    Promote to STAGING     :staging, after app2, 15m
    Final Validation       :final, after staging, 2h
    
    section Production
    Request Promotion      :req3, after final, 5m
    Wait for Approvals     :app3, after req3, 4h
    Promote to PROD        :prod, after app3, 20m
    Smoke Tests            :smoke, after prod, 30m
    Monitor Production     :monitor, after smoke, 4h
```

## Architecture Overview

```mermaid
C4Context
    title System Context - Sample Python App Deployment
    
    Person(dev, "Developer", "Writes code and triggers deployments")
    Person(qa, "QA Engineer", "Tests in various environments")
    Person(approver, "Approver", "Reviews and approves promotions")
    
    System(sampleapp, "Sample Python App", "Flask application")
    System(testflow, "Test-Flow", "Reusable deployment workflows")
    
    System_Ext(github, "GitHub Actions", "CI/CD platform")
    System_Ext(k8s, "Kubernetes", "Container orchestration")
    System_Ext(registry, "Docker Registry", "Image storage")
    
    Rel(dev, github, "Triggers workflows")
    Rel(github, sampleapp, "Builds and tests")
    Rel(github, testflow, "Uses validation actions")
    Rel(approver, github, "Approves promotions")
    Rel(github, registry, "Pushes images")
    Rel(github, k8s, "Deploys to")
    Rel(qa, k8s, "Tests in")
```

## Validation Gates Detail

```mermaid
flowchart LR
    subgraph "Gate 1: Lifecycle Validation"
        A1[Check deployment window]
        A2[Verify prerequisites]
        A3[Check blocking issues]
    end
    
    subgraph "Gate 2: Branch Validation"
        B1[Verify branch name]
        B2[Check environment rules]
        B3[Validate CI status]
    end
    
    subgraph "Gate 3: Release Check"
        C1[Query release system]
        C2[Check availability]
        C3[Validate schedule]
    end
    
    START([Start]) --> A1
    A1 --> A2
    A2 --> A3
    A3 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> END([Deploy])
    
    A1 -.-> FAIL([Workflow Stops])
    A2 -.-> FAIL
    A3 -.-> FAIL
    B1 -.-> FAIL
    B2 -.-> FAIL
    B3 -.-> FAIL
    C1 -.-> FAIL
    C2 -.-> FAIL
    C3 -.-> FAIL
    
    style START fill:#90EE90
    style END fill:#90EE90
    style FAIL fill:#FFB6C6
```

## Component Integration

```mermaid
graph TB
    subgraph "sample-python Repository"
        A[Application Code]
        B[Tests]
        C[Dockerfile]
        D[Helm Charts]
        E[Workflows]
    end
    
    subgraph "test-flow Repository"
        F[Validation Actions]
        G[Deployment Actions]
        H[Promotion Actions]
    end
    
    subgraph "Runtime"
        I[Build & Test]
        J[Docker Build]
        K[Validation]
        L[Deployment]
    end
    
    A --> I
    B --> I
    C --> J
    E --> K
    F --> K
    K --> L
    G --> L
    D --> L
    H --> L
    
    style E fill:#FFD700
    style F fill:#87CEEB
    style G fill:#87CEEB
    style H fill:#87CEEB
```

## Summary

### ✅ Yes - The Diagram Matches!

The flow diagram you provided **exactly matches** the `test-flow` repository implementation:

1. **GitHub Actions (Deployment Trigger)** = Entry point workflows
2. **Deployment Lifecycle Validation** = First validation gate
3. **Branch Validation** = Second validation gate
4. **Future or Active Release** = Release availability check
5. **Deploy to Future Release** = Final deployment action
6. **Workflow Stops (Failure)** = Built-in failure handling

### 🚀 Sample Python App Integration

The `sample-python` repository now:
- ✅ **Uses all test-flow actions** via composite action pattern
- ✅ **Follows the exact flow** from your diagram
- ✅ **Adds application-specific steps** (build, test, Docker)
- ✅ **Implements promotion workflows** with approval gates
- ✅ **Auto-deploys to DEV-INT** on main push
- ✅ **Supports manual deployments** to all environments

### 📊 Key Features

- **Reusable validation logic** from test-flow
- **Application-specific build steps** in sample-python
- **Clear separation of concerns**
- **Easy to test and maintain**
- **Matches production best practices**

