# ADR-007: Answer Reveal API Contract

**Date:** 2026-03-14
**Status:** Accepted
**Deciders:** Instructor, SA Agent
**Category:** Backend / API Design

---

## Context

The core UX rule of birdie69 is: **a user cannot see their partner's answer until both
partners have submitted their own answer.** This "both-answered gate" is already
implemented in `GetAnswersQueryHandler` via `IAnswerRepository.BothPartnersAnsweredAsync`.

The open question is how the API communicates the "waiting" state to the client. The
client needs to distinguish three states:

1. **Neither answered** — user has not yet submitted
2. **Waiting** — user has submitted, partner has not yet
3. **Revealed** — both have submitted, answers are visible

The current handler returns `Result.Failure(Error.Conflict("Answer.NotBothAnswered", ...))`,
which would map to a 409 response. This is technically correct but has two problems:
- State 1 and State 2 are indistinguishable from the HTTP status alone
- The client cannot show the user's own (already submitted) answer text while waiting

---

## Decision

**Option B — HTTP 200 with `isRevealed: false` and `partnerAnswer: null`.**

`GET /v1/answers/{questionId}` always returns HTTP 200 (when the question exists and the
user is authenticated in an active couple). The response carries enough information for
the client to render all three states without any additional calls:

```json
{
  "questionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "isRevealed": false,
  "myAnswer": {
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "text": "My answer text",
    "submittedAt": "2026-03-14T09:15:00Z"
  },
  "partnerAnswer": null
}
```

When both partners have answered, `isRevealed` is `true` and `partnerAnswer` is populated.

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| A — HTTP 423/409 on waiting state | Simple handler; current code close to this | States 1 & 2 indistinguishable; client loses own answer text; 423 is non-standard; 409 semantically imprecise |
| **B — HTTP 200 with `isRevealed: false` (chosen)** | Single status code; client gets own answer while waiting; clean state machine in one response; no polling confusion | Requires handler return-type change from `Result<IReadOnlyList<AnswerDto>>` to `Result<AnswerRevealDto>` |
| C — HTTP 200 only when both answered, 404 otherwise | Simple | Client cannot distinguish "not answered" from "question not found"; loses own answer text |

---

## Response Shape

### `AnswerRevealDto`

```csharp
public sealed record AnswerRevealDto(
    Guid QuestionId,
    bool IsRevealed,
    AnswerDto? MyAnswer,
    AnswerDto? PartnerAnswer);

public sealed record AnswerDto(
    Guid Id,
    string Text,
    DateTime SubmittedAt);
```

### State Mapping

| `myAnswer` | `partnerAnswer` | `isRevealed` | Client UI |
|-----------|----------------|-------------|-----------|
| `null` | `null` | `false` | "Answer today's question" CTA |
| populated | `null` | `false` | "Waiting for your partner..." |
| populated | populated | `true` | Reveal both answers |

### HTTP Error Cases (unchanged)

| Condition | Status | Error code |
|-----------|--------|------------|
| User not authenticated | 401 | — |
| User not in a couple | 409 | `Answer.NoCouple` |
| Question not found | 404 | `Question.NotFound` |

---

## Required Handler Changes (Dev tasks)

1. Change `GetAnswersQuery` return type from `Result<IReadOnlyList<AnswerDto>>` to
   `Result<AnswerRevealDto>`.
2. Change `GetAnswersQueryHandler` to:
   - Always fetch the requesting user's own answer (may be null if not submitted yet).
   - Call `BothPartnersAnsweredAsync` to set `IsRevealed`.
   - Only populate `PartnerAnswer` when `IsRevealed` is true.
   - Return `Result.Success(new AnswerRevealDto(...))` in all non-error cases.
3. Add `GetByUserAndQuestionAsync` usage for "my answer" lookup (already on `IAnswerRepository`).
4. Update the API controller mapping from `Result.Failure` → error responses as before
   (no change for 401/409/404 paths).

---

## scheduledDate Ownership (Q2)

For completeness, the scheduledDate strategy for MVP is:

**Option B — Seed script assigns dates sequentially.** A one-time seed script
(or Strapi admin bulk-import) creates 20–30 questions with `scheduledDate` = today,
today+1, today+2, etc. `CmsService` continues to query Strapi by `scheduledDate = today`.

This is the simplest approach for an MVP demo and requires no changes to the existing
`CmsService` or `IQuestionRepository`.

**Future evolution path:** Once the product requires per-couple personalization, introduce
an `ordinal` field on the Strapi question content type and change `CmsService` to query
by `ordinal = (today - couple.createdDate).Days + 1`. This warrants a new ADR at that time.

---

## Consequences

### Positive
- Client always knows the user's own submission state without a separate call.
- Clean state machine: client renders purely based on `isRevealed` and null-checks.
- `IsRevealed` flag could later be extended to a `revealedAt` timestamp for analytics.

### Negative
- `GetAnswersQuery` / `GetAnswersQueryHandler` require non-trivial refactoring.
- AutoMapper configuration must be updated for the new `AnswerRevealDto`.
- Integration tests for the handler must be rewritten.

### Future
- `isRevealed` could be combined with an `AnswerReveal` domain event to trigger push
  notifications when the partner answers (notify the first-submitter).

---

## References

- `src/Birdie69.Application/Features/Answers/Queries/GetAnswers/GetAnswersQuery.cs`
- `src/Birdie69.Application/Features/Answers/Queries/GetAnswers/GetAnswersQueryHandler.cs`
- `src/Birdie69.Domain/Entities/Answer.cs`
- `src/Birdie69.Domain/Interfaces/IAnswerRepository.cs`
- ADR-006: Question Entity Persistence Strategy
