# Sprint 4 — Notifications Delivery + Tech Debt

**Sprint Name:** Sprint 4 — Notifications Delivery + Tech Debt  
**Status:** 🏃 ACTIVE  
**Start Date:** 2026-04-24  
**End Date:** TBD  
**Sprint Goal:** Harden security + deliver FCM push skeleton via ACA Job

---

## Sprint Scope

| Ticket | Summary | Points | Status | Repo |
|--------|---------|--------|--------|------|
| [B69-30](https://narwhal.atlassian.net/browse/B69-30) | API: Gate dev JWT bypass — wrap OnMessageReceived block with builder.Environment.IsDevelopment() | 1 | ⏳ To Do | birdie69-api |
| [B69-31](https://narwhal.atlassian.net/browse/B69-31) | CMS: Generate Strapi read-only API token, store in Azure Key Vault, update birdie69-api to read from Key Vault reference | 2 | ⏳ To Do | birdie69-api / birdie69-cms |
| [B69-32](https://narwhal.atlassian.net/browse/B69-32) | Infra: Add Key Vault Managed Identity access to birdie69-api Container App in Terraform | 3 | ⏳ To Do | birdie69-infra |
| [B69-33](https://narwhal.atlassian.net/browse/B69-33) | NEW REPO: birdie69-notification-job — .NET 8 console app (ACA Job), Clean Architecture lite | 3 | ⏳ To Do | birdie69-notification-job (new) |
| [B69-34](https://narwhal.atlassian.net/browse/B69-34) | Notification Job: GetCouplesDueForNotificationQuery — eligibility rules (hour match, token present, not both answered) | 5 | ⏳ To Do | birdie69-notification-job |
| [B69-35](https://narwhal.atlassian.net/browse/B69-35) | Notification Job: INotificationSender + StubNotificationSender + SendDailyNotificationsCommand | 3 | ⏳ To Do | birdie69-notification-job |
| [B69-36](https://narwhal.atlassian.net/browse/B69-36) | Infra: Terraform notification_job brick — ACA Job with cron schedule "0 * * * *" (every hour) | 3 | ⏳ To Do | birdie69-infra |
| [B69-37](https://narwhal.atlassian.net/browse/B69-37) | API: OpenAPI spec update + integration test for notification eligibility query | 2 | ⏳ To Do | birdie69-api / birdie69-docs |

**Total Points:** 22  
**Capacity:** 22 (matching Sprint 3 velocity)

---

## Deferred / Backlog

| Ticket | Summary | Reason |
|--------|---------|--------|
| [B69-38](https://narwhal.atlassian.net/browse/B69-38) | DEFERRED: Firebase project setup + FirebaseNotificationSender | Blocked on human action — Firebase project must be created manually before implementation |

---

## Sprint Goal Details

### Tech Debt Hardening (B69-30, B69-31, B69-32)

**B69-30 — JWT Dev Bypass Guard (1 pt)**
- Wrap `OnMessageReceived` handler in `Program.cs` with `if (builder.Environment.IsDevelopment())`
- Prevents dev-mode auth bypass from leaking into staging/production
- Verify: `ASPNETCORE_ENVIRONMENT=Production` → `Bearer alice` returns 401

**B69-31 — Strapi Read-Only Token + Key Vault (2 pts)**
- Generate Strapi API token scoped to Question find/findOne only
- Store in Azure Key Vault as `birdie69-strapi-read-token`
- birdie69-api reads token via Key Vault reference in appsettings.json
- Local dev: `STRAPI_READ_TOKEN` via `.env`

**B69-32 — Key Vault Managed Identity (3 pts)**
- Add `azurerm_user_assigned_identity` to birdie69-api Container App
- Grant `Key Vault Secrets User` role on `birdie69-kv`
- `terraform validate` + `terraform plan` (no apply in Sprint 4)

### FCM Push Notification Skeleton (B69-33, B69-34, B69-35)

**B69-33 — New Repo Scaffold (3 pts)**
- `birdie69/birdie69-notification-job` GitHub repo
- .NET 8 console app, Clean Architecture lite (Application + Infrastructure layers)
- EF Core reads from shared PostgreSQL DB
- GitHub Actions CI, README

**B69-34 — Eligibility Query (5 pts)**
- `GetCouplesDueForNotificationQuery → IReadOnlyList<NotificationTargetDto>`
- `NotificationTargetDto`: `{ CoupleId, UserId, NotificationToken, QuestionTitle }`
- Eligibility rules:
  1. `Couple.NotificationTime.Hour == DateTime.UtcNow.Hour`
  2. `User.NotificationToken` is not null/empty
  3. User has NOT already answered today
  4. "Both answered" suppression: skip if BOTH partners answered
  5. Today's question exists in local DB
- 5 unit test scenarios

**B69-35 — INotificationSender + StubSender + Command (3 pts)**
- `INotificationSender.SendAsync(token, title, body, ct)` interface
- `StubNotificationSender`: logs to console (no real FCM)
- `SendDailyNotificationsCommand`: orchestrates query → loop → send
- Notification content: `title="birdie69 🐦"`, `body="Your daily question is ready: {questionTitle}"`
- Exception handling: log + continue (don't abort remaining sends)
- 3 unit test scenarios

### Infrastructure (B69-36)

**B69-36 — Terraform ACA Job (3 pts)**
- New brick: `birdie69-infra/bricks/notification_job/`
- `azurerm_container_app_job` with cron `"0 * * * *"` (hourly)
- Key Vault references for DB connection string + Strapi token
- Wired into `blueprints/app/main.tf`
- `terraform validate` passes

### Documentation & Testing (B69-37)

**B69-37 — OpenAPI Spec + Integration Tests (2 pts)**
- `birdie69-docs/api-specs/v1-notifications.yaml` — notification eligibility concept
- Integration test: `GET /v1/streaks/me` still 200 after B69-30 guard
- Full test suite re-run: 60 tests pass

---

## Architectural Decisions (ADR-010)

| Decision | Outcome |
|----------|---------|
| Notification delivery platform | Azure Container Apps Job (NOT Azure Functions) |
| New repo | `birdie69-notification-job` |
| Clean Architecture scope | Application + Infrastructure only (no Domain, no API layers) |
| Dev notification sender | `StubNotificationSender` — logs to console |
| Real FCM sender | Deferred to Sprint 5 (B69-38) — conditional on Firebase project |
| Timezone for MVP | UTC — no UI selector in Sprint 4 |
| "Both answered" suppression | YES — skip if both partners answered today |
| Notification opt-out | Deferred to Sprint 5 |
| Firebase project creation | Manual human action (not Terraform) |

---

## Dependencies

```
B69-30 (JWT guard)     ──► B69-37 (integration test must run after guard)
B69-31 (Key Vault secret) ──► B69-32 (Managed Identity must reference the secret)
B69-33 (new repo) ──► B69-34 (eligibility query — repo must exist)
B69-33 (new repo) ──► B69-35 (sender interface — repo must exist)
B69-33 (new repo) ──► B69-36 (Terraform job — image from this repo)

Parallel tracks:
  Track 1 (API/Security): B69-30 → B69-37
  Track 2 (Infra/Security): B69-31 → B69-32
  Track 3 (Notification Job): B69-33 → B69-34 + B69-35
  Track 4 (Infra/Job): B69-36 (can start after B69-33 scaffold)
```

---

## Definition of Done

- [ ] All acceptance criteria met per ticket description
- [ ] Unit tests pass (≥80% coverage on new code)
- [ ] Integration tests pass (API endpoints return correct status codes)
- [ ] `dotnet build` zero errors for all .NET projects
- [ ] `terraform validate` passes for all Terraform changes
- [ ] PR reviewed and merged to main
- [ ] ROADMAP.md updated (checkboxes ticked)
- [ ] Confluence synced
- [ ] Full birdie69-api test suite: 60 tests passing after B69-30

---

## Daily Log

| Date | Update |
|------|--------|
| 2026-04-24 | Sprint 4 planned. Tickets B69-30 through B69-37 groomed and estimated (22 pts). B69-38 deferred to backlog (conditional on Firebase). ROADMAP.md v2.4 updated. Confluence synced. SA Agent ADR-010 decisions incorporated. |
