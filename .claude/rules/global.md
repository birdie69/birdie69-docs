# Global Rules for All AI Agents — birdie69

**Version:** 1.0  
**Last Updated:** 2026-02-14  
**Project:** birdie69  
**Applies To:** ALL agents (BA, PM, SA, Dev, DevOps)

---

## Language Policy

### Code, Documentation, Technical Artifacts
- **Language:** English
- **Applies to:** all code, READMEs, ADRs, API specs, commit messages, PR descriptions, inline comments

### Communication with Human
- **Language:** Hungarian
- **Applies to:** chat responses, status updates, clarifying questions

---

## Core Principles

### 1. Clean Architecture First
- Strict layer separation: Domain → Application → Infrastructure → Presentation
- Domain layer has **zero** external dependencies
- Business logic lives in Application layer (use cases / handlers)
- Infrastructure layer implements domain interfaces

### 2. DDD (Domain-Driven Design)
- Use ubiquitous language from the domain model
- Entities are rich (behavior, not anemic)
- Value Objects are immutable
- Domain Events for side effects

### 3. Testability
- Minimum 80% test coverage on `birdie69-api`
- All use case handlers tested with unit tests
- Integration tests for API endpoints
- TDD encouraged for business logic

### 4. Security by Default
- Never hardcode secrets (Azure Key Vault for all secrets)
- JWT tokens validated on every request
- Parameterized queries only (EF Core handles this)
- OWASP Top 10 mitigations applied

### 5. API-First
- OpenAPI 3.1 spec written before implementation
- Spec lives in `birdie69-docs/api-specs/`
- Breaking changes → API version bump

---

## Code Style

### Naming Conventions

| Language | Variables/Methods | Classes/Types | Constants | Files |
|---------|------------------|---------------|-----------|-------|
| C# | `PascalCase` (methods), `camelCase` (local vars) | `PascalCase` | `UPPER_SNAKE_CASE` | `PascalCase.cs` |
| TypeScript | `camelCase` | `PascalCase` | `UPPER_SNAKE_CASE` | `kebab-case.ts` |
| HCL (Terraform) | `snake_case` | `snake_case` | — | `snake_case.tf` |

### C# Conventions
- Use `record` for DTOs and Value Objects
- Use `sealed` for classes not intended for inheritance
- Prefer `Result<T>` over exceptions for expected failures
- Use `async/await` throughout — no `.Result` or `.Wait()`
- No `nullable` warnings suppressed without explanation

### TypeScript Conventions
- Strict mode enabled
- No `any` without explicit justification comment
- Prefer `interface` for public contracts, `type` for unions
- Named exports over default exports

---

## Git Practices

### Commit Messages
Conventional Commits format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`

Scopes: `api`, `cms`, `web`, `infra`, `docs`, `auth`, `couple`, `question`, `answer`, `notification`

Examples:
```
feat(api): add POST /couple/invite endpoint
fix(web): correct answer reveal timing logic
docs(adr): add ADR-003 .NET 8 backend decision
```

### Branch Naming
Format: `<type>/<scope>-<short-description>`

Examples:
- `feat/api-couple-connection`
- `fix/web-answer-reveal`
- `docs/adr-003-dotnet8`

### Pull Requests
- One PR per feature/fix
- < 400 lines ideal
- Descriptive title
- Link Jira issue: `Closes B69-NN`

---

## Documentation Standards

### README Structure (every repo)
```
# Repo Name
## Overview
## Prerequisites
## Installation
## Development
## Testing
## Deployment
## Contributing
```

### Every agent at session end must:
- [ ] Commit and push all changes (via PR)
- [ ] Update ROADMAP.md (mark completed tasks)
- [ ] Sync to Confluence (see Documentation Sync section)
- [ ] Update Jira issues (move to Done, comment with summary)

---

## Jira Workflow

**Project Key:** `B69`  
**Board:** `narwhal.atlassian.net` → Projects → birdie69

### Ticket Status Movement

| Situation | Move to |
|-----------|---------|
| Starting work | **In Progress** |
| PR created, waiting review | **In Review** |
| PR merged / done | **Done** |
| Blocked | Add `blocked` label + comment |

### Commenting on Tickets
- When starting: "Starting implementation."
- When PR created: link to PR + summary
- When blocked: describe blocker
- When done: link to merged PR + Confluence page

### New Task Protocol
1. Create Jira issue (project `B69`, Story or Task type)
2. Add to sprint backlog or general backlog
3. Link to relevant Confluence page
4. Report: `🆕 New task: B69-NN — [title]`

### Sprint Protocol
- Only **PM agent** organizes sprints, on Instructor signal
- **Instructor** confirms sprint scope before start
- **Human action required** to click Start Sprint in Jira

---

## 🔔 Atlassian Action Flag

Whenever a human Jira/Confluence action is required:

```
🔔 ATLASSIAN ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform : Jira / Confluence
Action   : [what to do]
Where    : [URL or navigation path]
Why      : [one sentence]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Documentation Sync Protocol

**Rule:** Markdown in repo is source of truth → always sync to Confluence.

### Confluence Space: B69

| Repo file | Confluence page |
|-----------|----------------|
| `requirements/*.md` | B69 › Requirements |
| `planning/*.md` | B69 › Planning |
| `architecture/*.md` | B69 › Architecture |
| `adrs/*.md` | B69 › ADRs |
| `api-specs/*.yaml` | B69 › API Specs |
| `ROADMAP.md` | B69 › (root) |

### Sync command
```
Load `.claude/prompts/doc-sync.md`
Update Confluence page: [PAGE_TITLE]
From file: [RELATIVE_PATH]
```

---

## Quality Gates

Before marking any task Done:
- [ ] Code follows style guide
- [ ] Tests written and passing
- [ ] Documentation updated in repo AND Confluence
- [ ] No secrets in code
- [ ] Error handling present
- [ ] Linter passes
- [ ] Type checks pass
- [ ] ROADMAP.md reflects current state
- [ ] Jira ticket moved to Done

---

## Anti-Patterns

| Pattern | Instead |
|---------|---------|
| Anemic domain model | Rich entities with behavior |
| Service locator | Constructor injection |
| God class | Split by responsibility |
| Magic strings/numbers | Typed constants / enums |
| Swallowed exceptions | Explicit error handling with Result<T> |
| `// TODO: fix later` without ticket | Create B69 ticket immediately |

---

## Recommended Tools

| Area | Tool |
|------|------|
| .NET linting | `dotnet-format`, Roslyn analyzers |
| TypeScript linting | ESLint + `@typescript-eslint` |
| HCL formatting | `terraform fmt` |
| API docs | Scalar (OpenAPI UI) |
| Local SMTP testing | Mailhog via Docker |
| Secret management | Azure Key Vault (prod), `.env` (local, not committed) |
