# Sprint 3 — Engagement Features

**Sprint Name:** Sprint 3 — Engagement Features  
**Status:** 🏃 Active  
**Start Date:** 2026-03-20  
**End Date:** TBD  
**Sprint Goal:** Add engagement layer — streak tracking, answer history, notification preferences, FCM token capture, streak badges, and Capacitor mobile init

---

## Sprint Scope

| Ticket | Summary | Points | Assignee |
|--------|---------|--------|----------|
| [B69-29](https://narwhal.atlassian.net/browse/B69-29) | API: wire streak tracking — AnswerSubmittedEvent handler + GET /v1/streaks/me | 5 | tamas.pinter@narwhal.hu |
| [B69-24](https://narwhal.atlassian.net/browse/B69-24) | API: paginated GET /v1/answers/history — past Q&A pairs for the couple | 5 | tamas.pinter@narwhal.hu |
| [B69-25](https://narwhal.atlassian.net/browse/B69-25) | API + Web: notification time preference — PUT /v1/couples/me/notification-time + settings page | 3 | tamas.pinter@narwhal.hu |
| [B69-26](https://narwhal.atlassian.net/browse/B69-26) | API + Web: FCM device token registration — PUT /v1/users/me/notification-token + Capacitor push plugin | 3 | tamas.pinter@narwhal.hu |
| [B69-27](https://narwhal.atlassian.net/browse/B69-27) | Web: streak milestone badges — 7/14/30-day overlay on question page | 3 | tamas.pinter@narwhal.hu |
| [B69-28](https://narwhal.atlassian.net/browse/B69-28) | Mobile: Capacitor iOS + Android project init, verify build in iOS Simulator | 3 | tamas.pinter@narwhal.hu |

**Total Points:** 22

---

## Sprint Goal Details

### Streak Tracking (B69-29) — birdie69-api
- Domain event: `AnswerSubmittedDomainEvent` raised in `SubmitAnswerCommandHandler` after saving
- `StreakUpdatedEventHandler`: loads or creates Streak for user, calls `RecordActivity()`, saves
- `RecordActivity()` logic: today → no-op; yesterday → increment + update LongestCount; else → reset to 1
- EF Core migration for Streaks table (check AppDbContext — already scaffolded)
- `GET /v1/streaks/me` → `{ currentStreak, longestStreak, lastActivityDate }`
- "Your streak" copy (per-user, not couple)

### Answer History (B69-24) — birdie69-api
- `GET /v1/answers/history?page=1&pageSize=20`
- Requires active couple; 403 if not in couple
- `AnswerHistoryItemDto`: questionId, questionTitle, questionBody, scheduledDate, myAnswer?, partnerAnswer?, isRevealed
- Ordered by scheduledDate descending; only questions with ≥1 answer shown
- `IAnswerRepository.GetHistoryByCouple(coupleId, page, pageSize)` new method

### Notification Time Preference (B69-25) — birdie69-api + birdie69-web
- `PUT /v1/couples/me/notification-time` body: `{ notificationTime: "HH:mm" }` (24h)
- Calls `Couple.SetNotificationTime(TimeOnly)` — already implemented; per-couple (shared setting)
- `/settings` page in web: time picker, save button, success/error feedback
- Link from home page (gear icon or Settings button in active couple state)

### FCM Token Registration (B69-26) — birdie69-api + birdie69-web
- `PUT /v1/users/me/notification-token` body: `{ token: string }`
- Calls `User.SetNotificationToken(token)` — already implemented
- Web: `@capacitor/push-notifications` plugin; only runs when `Capacitor.isNativePlatform()` is true
- Data capture only — no actual delivery until Sprint 4

### Streak Milestone Badges (B69-27) — birdie69-web
- After `submitAnswer` succeeds: call `GET /v1/streaks/me`
- If `currentStreak` exactly 7, 14, or 30: show full-screen overlay
  - Text: "🔥 {N}-day streak! Keep it going!" + "Thanks!" dismiss button
- Shown once per milestone per session (component state only, not persisted)

### Capacitor Mobile Init (B69-28) — birdie69-web
- `npx cap add ios` → ios/ directory committed
- `npx cap add android` → optional stretch
- `npm run build && npx cap sync` → no errors
- Verify app opens in iOS Simulator (home page visible)
- `.gitignore` updated; README updated with mobile build instructions

---

## Dependencies

```
B69-29 (streak backend) must complete before B69-27 (streak badges) — badges consume GET /v1/streaks/me
B69-25 (notification time) can run parallel to B69-29 / B69-24
B69-26 (FCM token) can run parallel to all API tickets
B69-28 (Capacitor init) is independent of all API tickets
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
- [ ] GET /v1/streaks/me returns correct count after answer submission

---

## Daily Log

| Date | Update |
|------|--------|
| 2026-03-20 | Sprint started. Tickets B69-29, B69-24, B69-25, B69-26, B69-27, B69-28 created. Architectural decisions (ADR-008/009) confirmed by SA Agent. Streak: per-user stored counter (Option A). Notifications: Sprint 3 stores token/preference only; delivery deferred to Sprint 4 (ADR-009). Capacitor: iOS Simulator verification only (Option B). |

---

## Sprint Retrospective

*To be filled at sprint close.*
