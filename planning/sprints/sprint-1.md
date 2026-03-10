# Sprint 1 — Partner Connection

**Sprint Name:** Sprint 1 — Partner Connection  
**Status:** 🏃 Active  
**Start Date:** 2026-03-10  
**End Date:** TBD  
**Sprint Goal:** Implement the full partner connection flow — user profile autoprovision, couple invite/join/leave APIs, and the onboarding + couple management Web UI.

---

## Sprint Scope

| Ticket | Summary | Points | Assignee |
|--------|---------|--------|----------|
| [B69-7](https://narwhal.atlassian.net/browse/B69-7) | User profile API: GET /me (autoprovision), PUT /me (update profile), EF Core migration | 5 | tamas.pinter@narwhal.hu |
| [B69-8](https://narwhal.atlassian.net/browse/B69-8) | Couple invite API: POST /couples (create/regenerate), GET /couples/me | 5 | tamas.pinter@narwhal.hu |
| [B69-9](https://narwhal.atlassian.net/browse/B69-9) | Couple join API: POST /couples/join | 3 | tamas.pinter@narwhal.hu |
| [B69-10](https://narwhal.atlassian.net/browse/B69-10) | Couple leave/cancel API: DELETE /couples/me | 3 | tamas.pinter@narwhal.hu |
| [B69-11](https://narwhal.atlassian.net/browse/B69-11) | Web UI: onboarding, invite/join screens, couple status, leave couple | 8 | tamas.pinter@narwhal.hu |

**Total Points:** 24

---

## Sprint Goal Details

### API Layer (B69-7 to B69-10) — birdie69-api
- User autoprovision on first authenticated request (`sub` + `name` claims from JWT)
- EF Core migrations: `User` table + `Couple` table
- Full couple lifecycle: create invite → join → leave/cancel/disband
- Domain: `Couple.RegenerateCode()`, `Couple.Cancel()`, `CoupleStatus.Cancelled` enum value
- Unit tests for all command handlers; integration test for `GET /me`

### Web UI (B69-11) — birdie69-web
- `/onboarding` page → `PUT /me` → redirect to `/home`
- `/home` adapts to couple state (no couple / pending / active)
- `/invite` page with copyable code + regenerate + cancel
- `/join` page with code input + redirect on success

---

## Dependencies

```
B69-11 (Web UI) depends on B69-7, B69-8, B69-9, B69-10 (API contracts)
B69-8 depends on B69-7 (User table + ICurrentUser)
B69-9 depends on B69-8 (Couple table exists)
B69-10 depends on B69-8 (Couple entity)
```

---

## Definition of Done

- [ ] All acceptance criteria met per ticket description
- [ ] Unit tests pass (≥80% coverage on new code)
- [ ] Integration tests pass (API endpoints return correct status codes)
- [ ] EF Core migration applied cleanly on fresh DB
- [ ] PR reviewed and merged to main
- [ ] ROADMAP.md updated (checkboxes ticked)
- [ ] Confluence synced

---

## Daily Log

| Date | Update |
|------|--------|
| 2026-03-10 | Sprint started. Tickets B69-7 to B69-11 in backlog. |

---

## Sprint Retrospective

*To be filled at sprint close.*
