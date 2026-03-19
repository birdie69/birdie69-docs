# ADR-008: Streak Calculation Strategy

**Date:** 2026-03-19  
**Status:** Accepted  
**Deciders:** Instructor, SA Agent  
**Category:** Backend / Domain Model

---

## Context

Sprint 3 introduces streak tracking as the first engagement feature. A streak represents
consecutive days of engagement. The business requirement is: a streak continues for each
day both partners submit their daily answer.

Three calculation strategies are possible: store a counter on the domain model (denormalized),
calculate at query time from the Answer history, or use a hybrid nightly-batch approach.

Crucially, a `Streak` entity was already scaffolded in Sprint 0 as part of the initial
domain model:

```csharp
// Birdie69.Domain.Entities.Streak (already exists)
public sealed class Streak : AuditableEntity
{
    public Guid UserId { get; private set; }
    public int CurrentCount { get; private set; }
    public int LongestCount { get; private set; }
    public DateOnly LastActivityDate { get; private set; }

    public void RecordActivity(DateOnly today) { ... }  // consecutive-day logic already implemented
}
```

`AppDbContext` already has `DbSet<Streak> Streaks`. This means Option A is already
partially implemented at the domain layer.

---

## Decision

**Option A — Stored streak counter on the `Streak` entity, incremented via domain event handler.**

The `Streak` entity is per-user (not per-couple). For MVP, a user's streak increments when
they submit an answer on a consecutive day. The `AnswerSubmittedEvent` (already raised in
`Answer.Submit()`) triggers an `AnswerSubmittedEventHandler` that finds or creates the
user's `Streak` record and calls `streak.RecordActivity(DateOnly.FromDateTime(DateTime.UtcNow))`.

**MVP simplification:** The streak increments when the user submits their own answer
(individual engagement), not gated on partner completion. This mirrors how popular habit
apps (Duolingo, Streaks) define streaks. The "couple both answered" gate is preserved for
the answer reveal UX (ADR-007) but not applied to streak counting for MVP.

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **A — Stored counter on Streak entity (chosen)** | O(1) read; already scaffolded in domain; `RecordActivity()` handles day-continuity correctly; `LongestCount` tracked for free | Requires event handler wiring; breaks on retroactive answer inserts (not a current feature) |
| B — Calculated at query time from Answer table | Always accurate; no denormalized state | O(n) scan per request; needs composite index on `(UserId, SubmittedAt)`; adds latency to streak display |
| C — Hybrid: calculated nightly, cached in Redis | Accurate + fast | Requires scheduled job infrastructure (IHostedService or Azure Function); over-engineered for MVP |

---

## Implementation Plan (Sprint 3)

### Domain layer (already scaffolded — no changes needed)
- `Streak.cs` entity with `RecordActivity(DateOnly)` and `IsActiveToday(DateOnly)`
- `AppDbContext.Streaks` DbSet

### Infrastructure / Application layer (to implement)
1. **`IStreakRepository`** — `GetByUserIdAsync`, `AddAsync`, `UpdateAsync`
2. **`AnswerSubmittedEventHandler`** — handles `AnswerSubmittedEvent`:
   - Load or create `Streak` for the user
   - Call `streak.RecordActivity(today)` only if `!streak.IsActiveToday(today)` (idempotent)
   - Persist via `IStreakRepository`
3. **`GetStreakQuery`** + **`GetStreakQueryHandler`** — returns `StreakDto { CurrentCount, LongestCount, LastActivityDate, IsActiveToday }`
4. **EF Core configuration** — `StreakConfiguration` with index on `UserId` (unique) and `LastActivityDate`
5. **EF Core migration** — `AddStreakTable` (or verify existing migration covers it)

### API layer
- `GET /v1/streaks/me` → `StreakDto` (200) or `{ currentCount: 0 }` if no streak exists yet

### Web UI
- Streak counter display on the home screen (current count + flame icon)
- Milestone overlay for 7-day, 14-day, 30-day streaks (basic celebration, no animation)

---

## Consequences

### Positive
- Zero extra DB reads for displaying the streak (single row lookup by UserId)
- `LongestCount` tracked automatically — free engagement data for future analytics
- Domain logic for day-continuity is already tested via unit test on `Streak` entity
- `IsActiveToday()` allows idempotent handler execution (safe to re-process events)

### Negative
- Streak count is slightly denormalized — if an Answer row is deleted or backdated,
  the `Streak` counter will be stale (acceptable: retroactive edits are not a current feature)
- Requires a domain event handler wired via MediatR notification (`DomainEventNotification<AnswerSubmittedEvent>`)

### Future
- **Couple-level streak:** Once the UX requires "streak broken if partner didn't answer",
  add `CoupleStreak` tracked on the `Couple` entity. The handler checks `BothPartnersAnsweredAsync`
  before calling `RecordActivity`. Warrants a new ADR when scoped.
- **Streak freeze / grace day:** Premium feature — allow one missed day without breaking
  the streak. Add `GraceDaysRemaining` on `Streak` entity.
- **Recalculation endpoint:** Admin-only `POST /v1/admin/streaks/recalculate` that recomputes
  all streaks from Answer history for data-integrity recovery. Implements Option B as a
  batch utility.

---

## References

- `src/Birdie69.Domain/Entities/Streak.cs`
- `src/Birdie69.Infrastructure/Persistence/AppDbContext.cs`
- `src/Birdie69.Domain/Events/AnswerSubmittedEvent.cs`
- ADR-007: Answer Reveal API Contract (AnswerSubmittedEvent source)
