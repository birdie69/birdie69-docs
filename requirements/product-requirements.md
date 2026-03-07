# Product Requirements — birdie69 MVP

**Version:** 1.0  
**Date:** 2026-02-14  
**Author:** BA Agent  
**Status:** Draft

---

## Functional Requirements

### FR-001: User Authentication

**Priority:** Must Have

| # | Requirement |
|---|------------|
| FR-001.1 | Users can sign in with Apple Sign-In |
| FR-001.2 | Users can sign in with Google Sign-In |
| FR-001.3 | Users can sign in via Email Magic Link (passwordless) |
| FR-001.4 | On first login, a user profile is created automatically |
| FR-001.5 | Users can sign out from the app |
| FR-001.6 | Authentication tokens expire and are refreshed silently |

**Acceptance Criteria (FR-001):**
- Given a new user clicks "Sign in with Apple", when authentication succeeds, then a user account is created with externalId = B2C Object ID
- Given an existing user signs in, when authentication succeeds, then their existing profile is loaded
- Given a token expires, when the app is in foreground, then a new token is fetched silently without requiring re-login

---

### FR-002: Partner Connection

**Priority:** Must Have

| # | Requirement |
|---|------------|
| FR-002.1 | A user can generate a unique invite code to connect with a partner |
| FR-002.2 | An invite code is valid for 48 hours |
| FR-002.3 | A user can join a couple by entering an invite code |
| FR-002.4 | A user cannot join their own couple (self-invite is rejected) |
| FR-002.5 | A user can only be in one active couple at a time |
| FR-002.6 | Couples can see each other's profile display name |

**Acceptance Criteria (FR-002):**
- Given user A generates an invite code, when user B enters the code within 48 hours, then they are connected as a couple
- Given a user is already in a couple, when they try to join another couple, then the request is rejected with an appropriate error
- Given an invite code has expired, when a user tries to use it, then an error is returned

---

### FR-003: Daily Question

**Priority:** Must Have

| # | Requirement |
|---|------------|
| FR-003.1 | One question is available per day, shared across all couples |
| FR-003.2 | The question changes at midnight UTC |
| FR-003.3 | Questions are managed in the Strapi CMS by content editors |
| FR-003.4 | Users can see today's question without having answered it yet |
| FR-003.5 | The API caches the daily question in Redis (TTL until next midnight) |

---

### FR-004: Answer Submission

**Priority:** Must Have

| # | Requirement |
|---|------------|
| FR-004.1 | A user can submit one answer per daily question |
| FR-004.2 | A submitted answer cannot be edited or deleted |
| FR-004.3 | After submission, the user sees a "Waiting for partner" state |
| FR-004.4 | Answers are revealed only when **both** partners have submitted |
| FR-004.5 | Users cannot see their partner's answer before submitting their own |

**Acceptance Criteria (FR-004):**
- Given user A submits an answer, when user B has not yet answered, then user A sees "Waiting for [partner name]"
- Given both partners submit answers, when either partner views the question, then both answers are visible
- Given a user tries to submit a second answer, then the request is rejected

---

### FR-005: Push Notifications

**Priority:** Must Have

| # | Requirement |
|---|------------|
| FR-005.1 | Users receive a daily push notification when a new question is available |
| FR-005.2 | Users receive a push notification when their partner submits their answer |
| FR-005.3 | Notification time is configurable per user (default: 8:00 AM local time) |
| FR-005.4 | Users can disable notifications in the app settings |

---

### FR-006: Answer History

**Priority:** Should Have

| # | Requirement |
|---|------------|
| FR-006.1 | Users can browse past questions and both partners' answers |
| FR-006.2 | History is paginated (20 items per page) |
| FR-006.3 | History only shows questions where both partners answered |

---

### FR-007: Streak Tracking

**Priority:** Should Have

| # | Requirement |
|---|------------|
| FR-007.1 | A user's streak increases by 1 for each day both partners answer |
| FR-007.2 | If either partner misses a day, the streak resets to 0 |
| FR-007.3 | The current streak is visible on the home screen |
| FR-007.4 | The longest streak is recorded and displayed |

---

## Non-Functional Requirements

| # | Requirement | Target |
|---|------------|--------|
| NFR-001 | API response time (p95) | < 200ms |
| NFR-002 | API availability | 99.9% uptime |
| NFR-003 | Mobile app startup time | < 2 seconds (cold start) |
| NFR-004 | Test coverage | ≥ 80% (API) |
| NFR-005 | GDPR compliance | User data deletable on request |
| NFR-006 | Accessibility | WCAG 2.1 AA on web |
| NFR-007 | Offline support | Read-only: last question + answers visible offline |

---

## Out of Scope (MVP)

- Group mode (3+ people)
- Custom question creation by users
- In-app video/voice calls
- AI-generated questions
- Multiple languages (English only in MVP)
- Native iOS / Android apps (Capacitor only in MVP)
- Premium subscription (Phase 3)
