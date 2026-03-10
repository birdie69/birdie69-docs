# Roadmap — birdie69

**Version:** 1.6  
**Last Updated:** 2026-03-10  
**Learning Goal:** Build a complete AI-driven development workflow from HLD to shipped product.

---

## Phase 0: Project Foundation (Week 1)

**Goal:** All repos initialized, CI/CD skeletons in place, local dev working.

### Day 1 — Architecture & Setup ✅ COMPLETE (2026-03-07)
- [x] Project pivot decided and documented (ADRs 001–005)
- [x] birdie69-docs: Charter, Architecture Overview, Repository Index, Roadmap, ADRs, Agent Roster
- [x] Original product specs added to `specs/` (development plan, product spec, UI/UX design system)
- [x] 5 GitHub repos created and pushed to `birdie69` org
- [x] All agent prompts updated for birdie69 context (.claude/prompts/)
- [x] Jira project `B69` created — 15 tickets (B69-1 Done, B69-2–15 in backlog)
- [x] Confluence space `B69` created — 17 pages imported
- [x] birdie69-cms: reusable Strapi config files pre-staged (database.ts, develop.js, tsconfig.json, docker-compose.yml)
- [x] GitHub org: all repos transferred from `learn-claude` to `birdie69`
- [x] Local workspace: blog-* repos removed, only birdie69-* remain
- [x] Branch protection enabled on all 5 repos (PR required, no force push) — B69-16 ✅
- [x] Sprint 0 — Foundation created in Jira (B69-2, B69-3, B69-4, B69-5, B69-6, B69-16)

### Day 2 — API Scaffold ✅ COMPLETE (2026-03-09)
- [x] `birdie69-api`: .NET 8 Clean Architecture scaffold (Domain, Application, Infrastructure, Api) — B69-2 ✅
  - Domain entities: User, Couple, Question, Answer, InviteCode
  - CQRS handlers via MediatR, FluentValidation, AutoMapper
  - EF Core + PostgreSQL + Redis stubs
  - Azure AD B2C JWT middleware (stub)
  - Swagger UI at `http://localhost:8080/swagger`
  - 12 unit/application tests + 1 integration test — all passing
- [x] `birdie69-api`: Docker Compose for local PostgreSQL + Redis
- [x] Post-scaffold fixes: Swashbuckle (net8.0), FluentValidation DI, GlobalUsings, Result<T> wrapping
- [x] Dockerfile fix: `Directory.Build.props` + `global.json` before `dotnet restore`, `.dockerignore` added — PR #3, #4 ✅
- [x] Dev agent prompt updated: mandatory iterative 8-step protocol (build/test after each layer)
- [x] Dev auth bypass: `OnMessageReceived` replaces non-JWT Bearer tokens (e.g. "dev") with self-signed dev JWT; all validation disabled in non-prod — PR #5, #6, #7 ✅
- [x] EF Core migrations: `InitialCreate` generated, auto-applied at startup in non-prod — PR #5 ✅
- [x] Swagger fix: `AuthorizeOperationFilter` adds Bearer lock per `[Authorize]` operation so Swagger UI sends the token — PR #8 ✅

### Day 3 — CMS Setup ✅ COMPLETE (2026-03-10)
- [x] `birdie69-cms`: Strapi v5 (5.36.1) initialized with PostgreSQL — B69-3 ✅
  - `Question` content type: title, body, category (enum), scheduledDate, tags, isActive
  - Read-only API token generated for birdie69-api
  - Dockerfile multi-stage (builder + runtime), docker-compose with .tmp + dist volumes
  - GitHub Actions CI: `npm ci` + `npm run build` on PR
  - Node 20 pinned via `.nvmrc`
- [x] `birdie69-api`: Strapi integration — `ICmsService` + `CmsService` (typed HttpClient + Redis cache, TTL=midnight UTC)
  - `QuestionDto` updated: DocumentId, Title, Body, Category, ScheduledDate, Tags
  - `GetTodayQuestionQueryHandler` uses `ICmsService` (replaces local DB lookup)
  - Redis fallback to in-memory cache when Redis unavailable
  - docker-compose: PostgreSQL port 5433 (conflict-free with CMS on 5432)
  - 3 integration tests: 401 / 404 (CMS null) / 200 (CMS has question) — all passing

### Day 4 — Terraform Foundation ✅ COMPLETE (2026-03-10)
- [x] `birdie69-infra`: Brick → Blueprint → Env structure initialized — B69-5 ✅
  - Bricks: container_app, postgres, redis, key_vault, blob_storage, container_registry
  - Blueprint: `blueprints/app/` — composes all bricks + Log Analytics + Container Apps Environment
  - Envs: dev / staging / prod with env-specific sizing (no apply yet)
  - Dev: postgres B_Standard_B1ms, redis Basic C0 | Staging/Prod: GP_Standard_D2s_v3, Standard C1
  - Sensitive values use `REPLACE_WITH_REAL_VALUE` placeholders — no secrets committed
- [x] GitHub Actions CI: `terraform fmt --check` + `terraform validate -backend=false` (matrix: dev/staging/prod)
- [x] Terraform 1.6.0 pinned via `.terraform-version`
- [x] PR workflow followed: `feat/B69-5-terraform-scaffold` → PR #1 → merged ✅

### Day 5 — Web Scaffold ✅ COMPLETE (2026-03-10)
- [x] `birdie69-web`: Next.js 14 App Router initialized — B69-4 ✅
  - TypeScript + Tailwind CSS + ESLint, App Router, `src/` dir, `@/*` alias
  - shadcn/ui: `components.json` + Button + Card components
  - MSAL Azure AD B2C stub: `msalConfig.ts`, `msalInstance.ts`, `AuthProvider.tsx`
  - Pages: home (`page.tsx` — Today's Question placeholder), login (`login/page.tsx`), protected layout (`(auth)/layout.tsx`)
  - Capacitor: `capacitor.config.ts` (`appId: com.birdie69.app`, `webDir: out`), `next.config.ts` `output: "export"`
  - TanStack Query + Zustand installed
  - `.env.local.example` with MSAL + API URL placeholders
  - Node 20 pinned via `.nvmrc`
- [x] Vitest unit tests: `HomePage.test.tsx` (renders heading + sign-in prompt) — 2 tests passing
- [x] GitHub Actions CI: `npm ci` + lint + build + test on PR to main
- [x] PR workflow followed: `feat/B69-4-web-scaffold` → PR #1 → merged ✅

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
| Phase 0: Foundation | ✅ Complete (Sprint 1 next) | Sprint 0 |
| Phase 1: Core Features | ⏳ Planned | Sprint 1 + 2 |
| Phase 2: Engagement | ⏳ Planned | Sprint 3 + 4 |
| Phase 3: Payments | ⏳ Planned | Sprint 5 + 6 |
| Phase 4: Production | ⏳ Planned | Sprint 7 |
| Phase 5: Post-MVP | ⏳ Planned | Sprint 8+ |
