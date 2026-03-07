# Roadmap — birdie69

**Version:** 1.0  
**Last Updated:** 2026-02-14  
**Learning Goal:** Build a complete AI-driven development workflow from HLD to shipped product.

---

## Phase 0: Project Foundation (Week 1)

**Goal:** All repos initialized, CI/CD skeletons in place, local dev working.

### Day 1 — Architecture & Setup ✅
- [x] Project pivot decided and documented (ADRs 001–005)
- [x] birdie69-docs repo initialized with Charter, Architecture, Roadmap, ADRs
- [x] 5 GitHub repos created in learn-claude org
- [x] Agent prompts updated for birdie69
- [ ] Jira project `B69` created
- [ ] Confluence space `B69` created and initial pages imported

### Day 2 — API Scaffold
- [ ] `birdie69-api`: .NET 8 solution with Clean Architecture project structure
  - Domain, Application, Infrastructure, Api projects
  - EF Core + PostgreSQL (local Docker)
  - Azure AD B2C JWT validation (middleware only, no flows yet)
  - OpenAPI/Swagger UI configured
  - xUnit test projects scaffolded
- [ ] `birdie69-api`: Docker Compose for local PostgreSQL + Redis
- [ ] `birdie69-api`: GitHub Actions CI (build + test)
- [ ] ADR updated if any decisions made

### Day 3 — CMS Setup
- [ ] `birdie69-cms`: Strapi v5 initialized with PostgreSQL
  - `Question` content type (title, body, category, scheduledDate, tags)
  - Read-only API token for birdie69-api consumption
  - Docker Compose for local development
- [ ] `birdie69-api`: Strapi integration (GET /questions/today endpoint)
- [ ] GitHub Actions CI for birdie69-cms

### Day 4 — Terraform Foundation
- [ ] `birdie69-infra`: Brick → Blueprint → Env structure initialized
  - Bricks: container_app, postgres, redis, key_vault, blob_storage
  - Blueprint: `app/` (full birdie69 stack)
  - Envs: dev, staging, prod (variables only, no apply yet)
- [ ] GitHub Actions: terraform fmt + validate on PR

### Day 5 — Web Scaffold
- [ ] `birdie69-web`: Next.js 14+ App Router initialized
  - Tailwind CSS + shadcn/ui configured
  - Capacitor initialized (iOS + Android targets)
  - MSAL (Azure AD B2C) auth integration stub
  - Basic layout: home page, login page
- [ ] GitHub Actions CI (build + lint)

---

## Phase 1: Core Features — MVP Sprint 1 (Week 2–3)

**Goal:** Partner connection + daily question + answer submission working end-to-end.

### Sprint 1 — Partner Connection
- [ ] `B69-xx`: POST /couple/invite — generate invite code
- [ ] `B69-xx`: POST /couple/join — join via invite code
- [ ] `B69-xx`: Couple status in user profile
- [ ] `B69-xx`: Web UI — Invite / Join couple screens
- [ ] `B69-xx`: Database: User, Couple entities + migrations
- [ ] `B69-xx`: Unit tests: CoupleService (invite, join, conflict cases)

### Sprint 2 — Daily Question Flow
- [ ] `B69-xx`: Strapi: question bank seeded (20 questions minimum)
- [ ] `B69-xx`: GET /questions/today — fetch from Strapi, cache in Redis
- [ ] `B69-xx`: POST /answers — submit answer (hidden until both answered)
- [ ] `B69-xx`: GET /answers/{questionId} — reveal only when both submitted
- [ ] `B69-xx`: Web UI — Today's question screen + answer form
- [ ] `B69-xx`: Web UI — Answer reveal screen

---

## Phase 2: Engagement Features (Week 4–5)

**Goal:** Push notifications, streaks, history, gamification.

- [ ] FCM push notification integration (.NET API → FCM)
- [ ] Daily question notification at configurable time per couple
- [ ] Streak tracking (daily answer = streak continues)
- [ ] Answer history (paginated list of past Q&A)
- [ ] Gamification: streak badges, milestone celebrations
- [ ] Mobile: Capacitor build → iOS/Android app submitted to TestFlight/Internal Testing

---

## Phase 3: Payments & Premium (Week 6–7)

**Goal:** Stripe subscription, premium features gate.

- [ ] Stripe integration (subscription checkout)
- [ ] Premium tier: unlimited history, custom question categories
- [ ] Stripe webhooks for subscription lifecycle
- [ ] Billing portal integration

---

## Phase 4: Production Deployment (Week 8)

**Goal:** Full Azure deployment via Terraform + GitHub Actions.

- [ ] Terraform: dev environment applied (Container Apps + DB + Redis)
- [ ] GitHub Actions: full CD pipeline (build → push image → deploy to Container Apps)
- [ ] Staging environment deployment
- [ ] Azure AD B2C tenant configured (Apple, Google, Magic Link flows)
- [ ] Cloudflare: DNS + WAF configured
- [ ] Observability: Serilog → Azure Monitor, OpenTelemetry traces

---

## Phase 5: Post-MVP (Future)

- [ ] Native iOS app (SwiftUI) — ADR-001
- [ ] Native Android app (Kotlin) — ADR-001
- [ ] AI-suggested questions (OpenAI integration)
- [ ] Multiple language support (i18n)
- [ ] Couples analytics dashboard
- [ ] AKS migration if scale requires it (ADR-004)

---

## Progress Tracking

| Phase | Status | Jira Sprint |
|-------|--------|------------|
| Phase 0: Foundation | 🔄 In Progress | Pre-Sprint |
| Phase 1: Core Features | ⏳ Planned | Sprint 1 + 2 |
| Phase 2: Engagement | ⏳ Planned | Sprint 3 + 4 |
| Phase 3: Payments | ⏳ Planned | Sprint 5 + 6 |
| Phase 4: Production | ⏳ Planned | Sprint 7 |
| Phase 5: Post-MVP | ⏳ Planned | Sprint 8+ |
