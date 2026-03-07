# Repository Index — birdie69

**Organization:** [learn-claude](https://github.com/learn-claude)  
**Last Updated:** 2026-02-14

---

## Active Repositories

| Repository | Purpose | Stack | Status |
|-----------|---------|-------|--------|
| [birdie69-docs](https://github.com/learn-claude/birdie69-docs) | Project documentation, ADRs, .claude/ agent prompts | Markdown | ✅ Active |
| [birdie69-api](https://github.com/learn-claude/birdie69-api) | .NET 8 ASP.NET Core REST API | C# .NET 8 | 🔧 Setup |
| [birdie69-cms](https://github.com/learn-claude/birdie69-cms) | Strapi v5 question bank CMS | Node.js / TypeScript | 🔧 Setup |
| [birdie69-web](https://github.com/learn-claude/birdie69-web) | Next.js 14+ web + Capacitor mobile | TypeScript / React | 🔧 Setup |
| [birdie69-infra](https://github.com/learn-claude/birdie69-infra) | Terraform IaC for Azure | Terraform / HCL | 🔧 Setup |

---

## Archived Repositories (Blog Platform — superseded by birdie69)

| Repository | Reason |
|-----------|--------|
| [blog-docs](https://github.com/learn-claude/blog-docs) | Pivoted to birdie69 |
| [blog-api-strapi](https://github.com/learn-claude/blog-api-strapi) | Pivoted to birdie69 |
| [blog-infra-azure](https://github.com/learn-claude/blog-infra-azure) | Pivoted to birdie69 |
| [blog-mobile-ios-swiftui](https://github.com/learn-claude/blog-mobile-ios-swiftui) | Pivoted to birdie69 |
| [blog-mobile-android-kotlin](https://github.com/learn-claude/blog-mobile-android-kotlin) | Pivoted to birdie69 |
| [blog-web-nextjs](https://github.com/learn-claude/blog-web-nextjs) | Pivoted to birdie69 |

---

## Repository Details

### birdie69-docs

- **Branch protection:** `main` protected, PRs required
- **Key files:**
  - `PROJECT_CHARTER.md` — product vision, goals, stack
  - `ARCHITECTURE_OVERVIEW.md` — system design
  - `ROADMAP.md` — phased delivery plan
  - `adrs/` — Architecture Decision Records
  - `requirements/` — product requirements
  - `planning/` — backlogs and sprint plans
  - `.claude/` — AI agent prompts and rules

### birdie69-api

- **Branch protection:** `main` protected, PRs required
- **Pattern:** Clean Architecture + DDD + CQRS (MediatR)
- **Key tools:** EF Core, FluentValidation, Serilog, OpenTelemetry, xUnit
- **Structure:** `src/{Domain,Application,Infrastructure,Api}/`, `tests/`

### birdie69-cms

- **Branch protection:** `main` protected, PRs required
- **Purpose:** Content management for question bank only
- **API consumer:** birdie69-api (read-only via Strapi REST API)

### birdie69-web

- **Branch protection:** `main` protected, PRs required
- **Web:** Next.js 14+ App Router + Tailwind CSS + shadcn/ui
- **Mobile:** Capacitor wraps Next.js build → iOS + Android native apps
- **Auth:** Azure AD B2C MSAL integration

### birdie69-infra

- **Branch protection:** `main` protected, PRs required
- **Pattern:** Brick → Blueprint → Env
- **Environments:** `dev`, `staging`, `prod`
- **Azure resources:** Container Apps, PostgreSQL Flexible Server, Redis Cache, Key Vault, B2C tenant, Blob Storage, Log Analytics
