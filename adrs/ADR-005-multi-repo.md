# ADR-005: Repository Structure — Multi-Repo

**Date:** 2026-02-14  
**Status:** Accepted  
**Deciders:** Instructor, SA Agent  
**Category:** Repository Organization

---

## Context

birdie69 consists of 5 distinct service types:
- Documentation and agent prompts
- .NET 8 API
- Strapi CMS
- Next.js + Capacitor web/mobile
- Terraform infrastructure

These services differ in language, runtime, build system, deployment pipeline, and team ownership (even if the team is an AI agent squad).

---

## Decision

Use a **multi-repo** structure: one GitHub repository per service.

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Multi-repo (chosen)** | Clean separation, independent CI/CD, clear ownership, simpler tooling | Cross-service changes need multiple PRs |
| Monorepo (Turborepo / Nx) | Atomic cross-service changes, shared tooling | Complex setup, tooling overhead, mixed language challenge |

---

## Repository Layout

| Repo | Primary Language | CI/CD Pipeline |
|------|----------------|----------------|
| `birdie69-docs` | Markdown | Lint + Confluence sync |
| `birdie69-api` | C# (.NET 8) | dotnet build → test → docker build → push → deploy |
| `birdie69-cms` | TypeScript (Node.js) | npm ci → strapi build → docker build → push → deploy |
| `birdie69-web` | TypeScript (React) | npm ci → next build → Capacitor build → deploy |
| `birdie69-infra` | HCL (Terraform) | terraform fmt → validate → plan → apply |

---

## Cross-Service Coordination

When a feature requires changes in multiple repos:
1. Create linked Jira issues (parent → child or linked issues)
2. Open PRs in each repo with reference to the same Jira issue
3. Merge in dependency order (infra → api → web)
4. Document coordination in Confluence

---

## Consequences

### Positive
- Each repo has its own independent release cycle
- DevOps tooling is language-specific (no polyglot build tools)
- Branch protection, PR rules, and CI/CD are per-service
- Smaller, focused repos are easier for AI agents to operate in
- Simpler `git clone` (no need to clone entire monorepo)

### Negative
- Cross-repo changes require synchronized PRs
- No atomic commits spanning multiple services
- Shared types/contracts (e.g., API response shapes) must be documented (OpenAPI spec in birdie69-docs)

### Mitigation
- OpenAPI spec in `birdie69-docs/api-specs/` is the contract between frontend and backend
- Versioned API endpoints prevent breaking changes
- Jira parent issues link cross-repo work

---

## References

- `REPOSITORY_INDEX.md` — all repo URLs and descriptions
- `birdie69-docs/api-specs/` — OpenAPI contracts
