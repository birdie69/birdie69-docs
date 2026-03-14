# Sprint 2 — Daily Question Flow

**Sprint Name:** Sprint 2 — Daily Question Flow  
**Status:** 🏃 Active  
**Start Date:** 2026-03-14  
**End Date:** TBD  
**Sprint Goal:** Implement the full daily question flow — question delivery from Strapi with local caching, answer submission, partner reveal, and the question/answer web UI.

---

## Sprint Scope

| Ticket | Summary | Points | Assignee |
|--------|---------|--------|----------|
| [B69-17](https://narwhal.atlassian.net/browse/B69-17) | Strapi: seed question bank with 20+ scheduled questions | 3 | tamas.pinter@narwhal.hu |
| [B69-18](https://narwhal.atlassian.net/browse/B69-18) | API: Question entity, EF Core migration, GET /v1/questions/today with Strapi upsert | 5 | tamas.pinter@narwhal.hu |
| [B69-19](https://narwhal.atlassian.net/browse/B69-19) | API: Answer entity, EF Core migration, submit answer, reveal endpoint | 8 | tamas.pinter@narwhal.hu |
| [B69-20](https://narwhal.atlassian.net/browse/B69-20) | Web UI: today's question, answer form, partner reveal screen | 8 | tamas.pinter@narwhal.hu |

**Total Points:** 24

---

## Sprint Goal Details

### CMS (B69-17) — birdie69-cms
- One-time seed script: 20–30 questions, 4 categories (GettingStarted/Communication/Intimacy/DeepEmotions)
- ≥5 questions per category, unique scheduledDate per question (today through today+29)
- Idempotent script, documented in birdie69-cms/README.md

### API Layer (B69-18, B69-19) — birdie69-api
- **B69-18:** Question entity (Id Guid, ExternalDocumentId unique, Title, Body, Category enum, ScheduledDate, Tags, CreatedAt)
  - EF Core migration: Questions table with ExternalDocumentId unique index
  - GetTodayQuestionQueryHandler: Redis HIT → return cached; MISS → Strapi fetch → upsert → cache
  - Race condition guard: catch DbUpdateException → GetByExternalIdAsync fallback
  - IQuestionRepository: GetByScheduledDateAsync, GetByExternalIdAsync (new), AddAsync
- **B69-19:** Answer entity (Id, UserId FK, QuestionId FK, CoupleId FK, Text max 1000, SubmittedAt)
  - EF Core migration: Answers table with (UserId, QuestionId) unique index
  - GetAnswersQueryHandler refactored → Result<AnswerRevealDto>
  - AnswerRevealDto: { IsRevealed: bool, MyAnswer: AnswerDto?, PartnerAnswer: AnswerDto? }
  - All existing answer-related tests updated for new return type

### Web UI (B69-20) — birdie69-web
- API clients: `getTodayQuestion`, `submitAnswer`, `getAnswers`
- Types: QuestionDto, AnswerDto, AnswerRevealDto in `src/lib/api/types.ts`
- Question page: 4 states (no couple / unanswered / waiting / revealed)
- Loading + error states for all API calls

---

## Dependencies

```
B69-18 depends on B69-17 (seeded Strapi question bank)
B69-19 depends on B69-18 (Question entity + local Guid)
B69-20 depends on B69-18 + B69-19 (API contracts for question + answer endpoints)
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
- [ ] AnswerRevealDto reveal logic verified in integration test

---

## Daily Log

| Date | Update |
|------|--------|
| 2026-03-14 | Sprint started. Tickets B69-17 to B69-20 created. Architectural decisions (ADR-006/007) confirmed by SA Agent. |

---

## Sprint Retrospective

*To be filled at sprint close.*
