# Product Backlog — birdie69

**Last Updated:** 2026-02-14  
**Jira Project:** B69  
**Status:** Phase 0 — Foundation

---

## Epics

| Epic | Description | Phase |
|------|-------------|-------|
| EPIC-1: Foundation | Repo scaffolds, CI/CD, local dev | Phase 0 |
| EPIC-2: Partner Connection | Couple invite + join flow | Phase 1 / Sprint 1 |
| EPIC-3: Daily Question | Question fetch + display | Phase 1 / Sprint 1 |
| EPIC-4: Answer Flow | Submit + reveal answers | Phase 1 / Sprint 1 |
| EPIC-5: Engagement | Push notifications, streaks, history | Phase 2 |
| EPIC-6: Payments | Stripe subscription, premium features | Phase 3 |
| EPIC-7: Production | Azure deployment, CD pipeline | Phase 4 |

---

## Phase 0 — Foundation (Pre-Sprint)

| B69 # | Type | Title | Points | Status |
|--------|------|-------|--------|--------|
| B69-1 | Task | Initialize birdie69-docs: Charter + ADRs + agent prompts | 3 | ✅ Done |
| B69-2 | Task | Initialize birdie69-api: .NET 8 Clean Architecture scaffold | 3 | ⏳ To Do |
| B69-3 | Task | Initialize birdie69-cms: Strapi v5 + Question content type | 3 | ⏳ To Do |
| B69-4 | Task | Initialize birdie69-web: Next.js 14+ + Capacitor + MSAL stub | 3 | ⏳ To Do |
| B69-5 | Task | Initialize birdie69-infra: Terraform Brick→Blueprint→Env | 3 | ⏳ To Do |
| B69-6 | Task | Set up GitHub Actions CI for all repos | 2 | ⏳ To Do |
| B69-7 | Task | Create Jira project B69 + initial tickets | 1 | ⏳ To Do |
| B69-8 | Task | Create Confluence space B69 + import initial docs | 2 | ⏳ To Do |

---

## Sprint 1 — Core: Partner + Question + Answer

**Goal:** A couple can connect, answer a daily question, and reveal each other's answers.  
**Capacity:** TBD (after Phase 0 complete)

| B69 # | Type | Title | Points | Status |
|--------|------|-------|--------|--------|
| B69-9 | Story | As a user, I can generate a partner invite code | 3 | ⏳ Backlog |
| B69-10 | Story | As a user, I can join a couple via invite code | 3 | ⏳ Backlog |
| B69-11 | Story | As a user, I can see today's daily question | 2 | ⏳ Backlog |
| B69-12 | Story | As a user, I can submit my answer to today's question | 3 | ⏳ Backlog |
| B69-13 | Story | As a user, I can see both answers after my partner submits | 3 | ⏳ Backlog |

---

## Sprint 2 — Engagement

| B69 # | Type | Title | Points | Status |
|--------|------|-------|--------|--------|
| B69-14 | Story | As a user, I receive a push notification for today's question | 5 | ⏳ Backlog |
| B69-15 | Story | As a user, I receive a push notification when my partner answers | 3 | ⏳ Backlog |
| B69-16 | Story | As a user, I can see my current answer streak | 3 | ⏳ Backlog |
| B69-17 | Story | As a user, I can browse my answer history | 3 | ⏳ Backlog |

---

## Backlog (Future Sprints)

| B69 # | Type | Title | Phase |
|--------|------|-------|-------|
| B69-18 | Story | Stripe subscription checkout | Phase 3 |
| B69-19 | Story | Premium: unlimited history access | Phase 3 |
| B69-20 | Task | Terraform dev environment apply | Phase 4 |
| B69-21 | Task | Full CD pipeline (image build + Container Apps deploy) | Phase 4 |
| B69-22 | Task | Azure AD B2C tenant configuration (Apple, Google, Magic Link) | Phase 4 |
| B69-23 | Story | Native iOS app (SwiftUI) — post-MVP | Phase 5 |
| B69-24 | Story | Native Android app (Kotlin) — post-MVP | Phase 5 |
