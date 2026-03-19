# ADR-009: Push Notification Architecture

**Date:** 2026-03-19  
**Status:** Accepted  
**Deciders:** Instructor, SA Agent  
**Category:** Backend / Infrastructure / Mobile

---

## Context

birdie69 sends a daily reminder to both partners at a couple-configured time to answer
the day's question. This requires:

1. **Device token storage** — when a user enables push notifications via the Capacitor
   app, FCM assigns a registration token that must be stored per user.
2. **Notification time preference** — each couple sets a preferred delivery time
   (`Couple.NotificationTime: TimeOnly`, default 08:00).
3. **Scheduled delivery** — at the configured time, the API (or a background service)
   must query which couples are due for a notification and dispatch FCM messages.

The `Couple.NotificationTime` field and `User.NotificationToken` field are already
present in the domain model. This ADR documents the delivery architecture and scoping
across Sprint 3 and Sprint 4.

---

## Decision

**Two-phase delivery across sprints:**

### Sprint 3 — Preference UI + Token Registration (data layer only)

1. **Device token storage:** Keep `User.NotificationToken (string?)` on the `User`
   entity for MVP (single active device per user). Add endpoint `PUT /v1/users/me/notification-token`
   that accepts a token string and calls `user.SetNotificationToken(token)`.

2. **Notification time preference UI:** Add command `SetNotificationTimeCommand` +
   endpoint `PUT /v1/couples/me/notification-time` that calls `couple.SetNotificationTime(time)`.
   Add a settings panel to the web UI for time selection.

3. **No FCM delivery in Sprint 3** — the infrastructure for scheduled delivery is
   deferred to Sprint 4 (see Q2 rationale).

### Sprint 4 — FCM Delivery via Azure Functions Timer Trigger

Implement **Option B** (Azure Functions Timer Trigger):
- A timer-triggered Azure Function runs every 15 minutes
- Queries couples where `NotificationTime` falls in the current 15-minute window
  AND at least one partner has not yet answered today's question
- Dispatches FCM messages via Firebase Admin SDK for each qualifying device token
- Function is deployed independently from the API (separate Container App or Azure
  Functions Consumption plan)

---

## Options Considered

### Q2 — Notification delivery mechanism

| Option | Pros | Cons |
|--------|------|------|
| A — Poll-based IHostedService (every minute) | No external infra; runs in-process | Wastes cycles; not precise at scale; adds memory/CPU load to API container |
| **B — Azure Functions Timer Trigger (chosen for Sprint 4)** | Decoupled from API; scales independently; precise 15-min window; no load on API container | Separate deployment; extra infra in Terraform |
| **C — Defer notifications to Sprint 4 (chosen for Sprint 3)** | Massively simplifies Sprint 3; token + preference data is captured now | Engagement value delayed one sprint |

### Q3 — Device token storage

| Option | Pros | Cons |
|--------|------|------|
| **A — `NotificationToken` on User entity (chosen for MVP)** | Already scaffolded; `SetNotificationToken()` already implemented; zero migration needed | Limited to one active device per user; old tokens linger on logout (mitigated by FCM invalid-token cleanup) |
| B — Separate `DeviceToken` table (one user → many devices) | Supports multi-device; proper token lifecycle management | Extra table + migration; join required; over-engineered for MVP |

---

## Device Token Lifecycle

### Registration flow (Sprint 3)
```
User opens app (Capacitor)
  → @capacitor-community/fcm plugin requests FCM token
  → App calls PUT /v1/users/me/notification-token { token: "fcm-token-xyz" }
  → API calls user.SetNotificationToken(token)
  → Token stored in Users.NotificationToken
```

### Delivery flow (Sprint 4)
```
Azure Function (Timer: every 15 min)
  → SELECT couples WHERE NotificationTime BETWEEN :windowStart AND :windowEnd
  → For each couple: check if either partner hasn't answered today
  → Load User.NotificationToken for non-answering partner(s)
  → POST https://fcm.googleapis.com/v1/projects/{project}/messages:send
  → Log delivery result; handle invalid-token cleanup (remove stale tokens)
```

### FCM invalid-token cleanup
When FCM returns `UNREGISTERED` or `INVALID_ARGUMENT` for a token, the delivery handler
should call `user.SetNotificationToken(null)` to clear the stale value. This prevents
repeated failed sends and keeps the token column clean.

---

## Future Migration Path (Q3 — multi-device)

When the product requires multiple device support (e.g., iPad + iPhone):

1. Create `DeviceTokens` table:
   ```sql
   CREATE TABLE DeviceTokens (
     Id UUID PRIMARY KEY,
     UserId UUID NOT NULL REFERENCES Users(Id),
     Token TEXT NOT NULL,
     Platform VARCHAR(10) NOT NULL,  -- 'ios' | 'android'
     RegisteredAt TIMESTAMPTZ NOT NULL,
     LastSeenAt TIMESTAMPTZ
   );
   CREATE UNIQUE INDEX ix_devicetokens_token ON DeviceTokens(Token);
   ```
2. Add EF migration to populate `DeviceTokens` from `Users.NotificationToken` (backfill).
3. Update `PUT /v1/users/me/notification-token` to upsert into `DeviceTokens` instead.
4. Update the Azure Function delivery query to JOIN `DeviceTokens` instead of `Users.NotificationToken`.
5. Deprecate `Users.NotificationToken` column (nullable, stop writing); remove in a
   follow-up migration.

---

## Notification Content

### Daily reminder message
```
Title: "Time to connect 💬"
Body:  "Today's question is waiting for you and [PartnerName]."
Data:  { "type": "daily_reminder", "questionId": "..." }
```

### Partner answered notification (future — Sprint 5+)
Triggered when `AnswerRevealedEvent` fires (both partners answered).
```
Title: "[PartnerName] answered!"
Body:  "Tap to see what they said."
Data:  { "type": "partner_answered", "questionId": "..." }
```

---

## Consequences

### Positive
- Token and preference data captured in Sprint 3 — Sprint 4 delivery just reads existing columns
- No FCM complexity in Sprint 3 maintains sprint velocity
- Azure Functions Timer Trigger decouples notification scheduling from the API container,
  preventing notification load from impacting API response times
- Per-couple `NotificationTime` allows respectful time-zone-aware delivery (future: store
  couple timezone alongside `NotificationTime`)

### Negative
- Engagement value (actual reminders) delayed to Sprint 4
- Azure Function introduces a second deployment artifact to manage in Terraform/CI
- 15-minute precision window means notifications can be up to 15 min late

### Future
- **Timezone support:** Add `Couple.TimezoneId (string?)` field. Azure Function converts
  `NotificationTime` from couple-local to UTC before querying. Warrants a new ADR.
- **Partner-answered notifications:** Wire into `AnswerRevealedEvent` — dedicated
  INotificationService called from the domain event handler dispatches an immediate FCM push.
- **Notification opt-out:** Add `User.NotificationsEnabled (bool)` flag; check before
  dispatching.

---

## References

- `src/Birdie69.Domain/Entities/User.cs` — `NotificationToken` field + `SetNotificationToken()`
- `src/Birdie69.Domain/Entities/Couple.cs` — `NotificationTime` field + `SetNotificationTime()`
- ADR-001: Mobile Strategy — Capacitor (FCM via `@capacitor-community/fcm` plugin)
- ADR-004: Infrastructure — Container Apps (Azure Functions as separate deployment)
- [Firebase Admin SDK for .NET](https://firebase.google.com/docs/admin/setup)
- [Capacitor FCM Plugin](https://github.com/capacitor-community/fcm)
