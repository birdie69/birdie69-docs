# ADR-006: Question Entity Persistence Strategy

**Date:** 2026-03-14
**Status:** Accepted
**Deciders:** Instructor, SA Agent
**Category:** Backend / Domain Model

---

## Context

Sprint 2 introduces the Daily Question Flow. Questions are authored in Strapi CMS and
identified there by a string `documentId`. The .NET 8 API must:

1. Serve `GET /v1/questions/today` to clients
2. Accept `POST /v1/answers` where the client references a specific question

The existing `SubmitAnswerCommandHandler` already references a `Guid QuestionId` and calls
`IQuestionRepository.GetByIdAsync(Guid)`. The existing `Answer` entity has a `Guid QuestionId`
foreign key. The `Question` domain entity, EF configuration, and `IQuestionRepository`
interface are all already in place with a `ExternalId` (string, unique index) field that maps
to Strapi's `documentId`.

The open question is: should the API persist questions locally at all, or treat the Strapi
`documentId` as the only reference?

---

## Decision

**Option A — Local Question entity with idempotent upsert on `GET /questions/today`.**

The local `Question` table is the reference for all answer FK relationships. When a client
calls `GET /v1/questions/today`, the handler:

1. Calls `ICmsService.GetTodayQuestionAsync()` (Strapi → Redis-cached until midnight UTC).
2. Calls `IQuestionRepository.GetByScheduledDateAsync(today)` to check the local DB.
3. If the local row does not exist, creates it via `Question.Create(...)` and persists with
   `IUnitOfWork.SaveChangesAsync()`.
4. Returns a `QuestionDto` enriched with the local `Id` (Guid) alongside `documentId`.

The response `id` (Guid) is what clients store and send in `POST /v1/answers`.

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **A — Local entity, upsert on GET (chosen)** | Referential integrity on Answer FK; consistent Guid-based API; aligns with all existing stubs; single source of truth for query joins | Extra upsert logic in the query handler; local DB must stay in sync with Strapi content |
| B — No local entity, string documentId in Answer | Simpler — no DB sync needed | No FK integrity; breaks all existing handler stubs; inconsistent with rest of API (all IDs are Guids); harder to query answer history by question |

---

## Upsert Strategy Details

### Idempotency

- `Questions` table has a `UNIQUE` index on both `ExternalId` and `ScheduledDate`
  (already configured in `QuestionConfiguration.cs`).
- The check-then-insert in the handler is safe in practice: concurrent requests on the
  same day will both hit the Redis cache after the first call. The upsert path is only
  exercised on the first request after midnight (cache miss).
- If two simultaneous requests race past the Redis cache, EF Core will throw a
  `DbUpdateException` on the second insert. The handler should catch this and re-query
  the now-existing row. The Dev agent must implement this retry in `GetTodayQuestionQueryHandler`.

### Single DB Round-Trip on Cache Hit

```
Redis HIT  → return cached QuestionDto (no DB access at all)
Redis MISS → Strapi fetch → DB check → optional insert → cache → return DTO
```

### Required Handler Changes (Dev tasks)

1. Inject `IQuestionRepository` and `IUnitOfWork` into `GetTodayQuestionQueryHandler`.
2. After Strapi fetch, call `questionRepository.GetByScheduledDateAsync(today)`.
3. If null: `Question.Create(Guid.NewGuid(), item.DocumentId, ...)` → `AddAsync` → `SaveChanges`.
4. Map the local `Question.Id` into the response `QuestionDto`.

### Domain Entity Alignment

The current `Question` entity has a single `Text` field, but `QuestionDto` has separate
`Title` and `Body` fields (from Strapi). The Dev agent must:

- Add `Title`, `Body`, and `Category` fields to the `Question` entity and update
  `QuestionConfiguration`.
- Update `Question.Create(...)` factory signature accordingly.
- Create a new EF migration.

---

## Consequences

### Positive
- Answer FK referential integrity is guaranteed by the relational DB.
- All endpoints use a consistent Guid-based ID scheme.
- No changes required to `SubmitAnswerCommand`, `SubmitAnswerCommandHandler`, or
  `IAnswerRepository` signatures.
- Historical question data is available for analytics and history views without
  calling Strapi.

### Negative
- `GetTodayQuestionQueryHandler` gains a dependency on `IQuestionRepository` and
  `IUnitOfWork` — it is no longer a pure CMS passthrough.
- A new EF migration is required to add `Title`/`Body`/`Category` columns to `Questions`.

### Future
- When the product evolves to per-couple personalized questions (ordinal-based, ADR-007
  candidate), the local `Question` table can be extended without changing the API contract,
  since clients already reference Guids.

---

## References

- `src/Birdie69.Domain/Entities/Question.cs`
- `src/Birdie69.Infrastructure/Persistence/Configurations/QuestionConfiguration.cs`
- `src/Birdie69.Domain/Interfaces/IQuestionRepository.cs`
- `src/Birdie69.Application/Features/Questions/Queries/GetTodayQuestion/GetTodayQuestionQueryHandler.cs`
- `src/Birdie69.Infrastructure/Cms/CmsService.cs`
- ADR-003: Backend .NET 8
