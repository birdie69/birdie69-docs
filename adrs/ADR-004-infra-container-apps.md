# ADR-004: Infrastructure — Azure Container Apps

**Date:** 2026-02-14  
**Status:** Accepted  
**Deciders:** Instructor, SA Agent  
**Category:** Infrastructure

---

## Context

birdie69 runs multiple services (.NET API, Strapi CMS, possibly background workers).  
We need a hosting platform that:
- Runs containerized workloads
- Scales to zero when idle (cost-efficient for early stage)
- Supports future migration to Kubernetes if needed
- Integrates well with Azure services (B2C, Key Vault, Blob Storage, PostgreSQL)

---

## Decision

Use **Azure Container Apps** for all containerized services.  
Infrastructure managed by **Terraform** (Brick → Blueprint → Env pattern).

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Azure Container Apps (chosen)** | Serverless containers, scale-to-zero, Kubernetes-compatible, Dapr support | Less control than full AKS |
| Azure App Service | Simple, well-known | Container support limited, no scale-to-zero |
| Azure Kubernetes Service (AKS) | Full Kubernetes control | Complex, expensive for early stage |
| Azure Functions | Scale-to-zero, event-driven | Not ideal for long-running API |

---

## Terraform Structure

Follows **Brick → Blueprint → Env** pattern:

```
birdie69-infra/
├── bricks/
│   ├── container_app/        # Reusable container app module
│   ├── postgres/             # PostgreSQL Flexible Server module
│   ├── redis/                # Azure Cache for Redis module
│   ├── key_vault/            # Azure Key Vault module
│   ├── b2c/                  # Azure AD B2C tenant module
│   ├── blob_storage/         # Azure Blob Storage module
│   └── container_registry/   # Azure Container Registry module
├── blueprints/
│   └── app/
│       └── main.tf           # Composition: all bricks for birdie69
└── envs/
    ├── dev/
    │   └── terraform.tfvars  # Dev-specific config (small SKUs, single replica)
    ├── staging/
    │   └── terraform.tfvars  # Staging (prod-like, minimal scale)
    └── prod/
        └── terraform.tfvars  # Production (autoscale, high availability)
```

---

## Kubernetes Migration Path

Azure Container Apps is built on Kubernetes internally.  
If traffic grows and we need full Kubernetes control:
1. Export Container Apps environment → AKS (scripts available)
2. Container images stay the same (no code changes needed)
3. Terraform bricks can be swapped (container_app → aks_deployment)

---

## Consequences

### Positive
- Scale-to-zero: dev/staging costs near zero when not in use
- Managed certificates, ingress, service discovery
- Built-in secret management via Key Vault references
- Dapr sidecar support for future event-driven patterns
- Easy horizontal scaling via revision replicas
- Fully containerized: identical environment locally and in cloud

### Negative
- Less control than AKS (cannot install arbitrary Kubernetes operators)
- Not all Kubernetes features available
- Container Apps-specific CLI/API for some operations

### Local Development
- All services run via **Docker Compose** locally
- Same container images used in development and production
- Docker Compose file maintained in each service repo

---

## References

- [Azure Container Apps documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Terraform AzureRM provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
- `ARCHITECTURE_OVERVIEW.md` — Infrastructure Architecture section
- `birdie69-infra` repository — Brick → Blueprint → Env implementation
