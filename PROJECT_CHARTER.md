# Project Charter — birdie69

**Version:** 1.0  
**Date:** 2026-02-14  
**Status:** Active  
**Learning Goal:** Build and orchestrate a solo AI-driven development team using Claude, from HLD to shipped product.

---

## Product Vision

**birdie69** is a daily-question relationship app designed for couples.  
Every day, both partners receive the same anonymous question. They answer independently, then compare their responses — sparking honest conversations, deeper understanding, and playful connection.

> "A daily mirror for two."

---

## Problem Statement

Couples often fall into routines and stop asking each other meaningful questions.  
Existing apps focus on tracking, tasks, or communication tools — not on discovery and connection.  
birdie69 creates a daily ritual that makes emotional connection a habit.

---

## Core Features (MVP)

| # | Feature | Description |
|---|---------|-------------|
| 1 | Daily Question | One curated question per day, same for both partners |
| 2 | Anonymous Answer | Both answer independently before seeing each other's reply |
| 3 | Partner Connection | Invite code to link two accounts as a couple |
| 4 | Answer Reveal | Reveal only when both partners have answered |
| 5 | History | Browse past questions and answers |
| 6 | Gamification | Streaks, badges for consistency |
| 7 | Push Notifications | Daily question reminder via FCM |
| 8 | Authentication | Passwordless: Apple Sign-In, Google Sign-In, Magic Link |

---

## Target Users

- Couples aged 22–45
- Both casual and intentional relationships
- Mobile-first (iOS and Android)
- Available globally (English, later Hungarian)

---

## Technology Stack

| Layer | Technology | Decision |
|-------|-----------|----------|
| Mobile / Web | Next.js 14+ + Capacitor | ADR-001 |
| API | .NET 8 ASP.NET Core | ADR-003 |
| CMS (Question Bank) | Strapi v5 | — |
| Database | PostgreSQL 15+ | — |
| Cache | Redis | — |
| Authentication | Azure AD B2C | ADR-002 |
| Infrastructure | Azure Container Apps | ADR-004 |
| IaC | Terraform (Brick→Blueprint→Env) | — |
| CI/CD | GitHub Actions | — |
| Payments | Stripe | — |
| Push Notifications | Firebase Cloud Messaging | — |
| Email | SendGrid / Azure Communication Services | — |
| Analytics | Mixpanel | — |
| Storage | Azure Blob Storage | — |
| CDN | Cloudflare | — |

---

## Repository Structure

| Repo | Purpose |
|------|---------|
| `birdie69-docs` | Documentation, ADRs, agent prompts |
| `birdie69-api` | .NET 8 ASP.NET Core API |
| `birdie69-cms` | Strapi v5 (question bank management) |
| `birdie69-web` | Next.js 14+ web app + Capacitor mobile |
| `birdie69-infra` | Terraform infrastructure (Azure) |

See `REPOSITORY_INDEX.md` for details.

---

## Agent Roster

| Agent | Role | Prompt File |
|-------|------|-------------|
| Instructor | Orchestrator — coordinates all agents | (this chat) |
| BA | Business Analyst — requirements, user stories | `.claude/prompts/agent-ba.md` |
| SA | Solution Architect — HLD, ADRs, tech decisions | `.claude/prompts/agent-sa.md` |
| Dev | Developer — implementation, code review | `.claude/prompts/agent-dev.md` |
| PM | Product Manager — backlog, sprints, Jira | `.claude/prompts/agent-pm.md` |
| DevOps | Infrastructure, CI/CD, Terraform | `.claude/prompts/agent-devops.md` |

---

## Architecture Principles

1. **Clean Architecture** — strict layer separation (Domain → Application → Infrastructure → Presentation)
2. **DDD (Domain-Driven Design)** — domain model drives the design
3. **API-First** — OpenAPI contracts before implementation
4. **Security by Design** — zero-trust, Azure AD B2C externalized identity
5. **Testability** — 80%+ coverage, TDD encouraged
6. **Observability** — structured logging (Serilog), distributed tracing (OpenTelemetry), Prometheus metrics
7. **Documentation as Code** — ADRs, OpenAPI, all in repo; synced to Confluence
8. **IaC Everything** — no manual Azure resource creation; Terraform manages all infra

---

## Non-Goals (MVP)

- Native iOS (SwiftUI) — planned post-MVP (see ADR-001)
- Native Android (Kotlin) — planned post-MVP (see ADR-001)
- Group or multi-person mode
- In-app video or voice calls
- Custom AI-generated questions (rule-based only in MVP)

---

## Success Metrics (MVP)

| Metric | Target |
|--------|--------|
| Daily Active Couples | 1,000 within 3 months |
| D7 Retention | > 40% |
| Answer Submission Rate | > 70% of pushed questions answered |
| Streak Average | > 5 days |
| App Store Rating | ≥ 4.2 |

---

## Jira Project

- **Key:** `B69`
- **Type:** Scrum
- **Space:** `narwhal.atlassian.net` → Project: birdie69

## Confluence Space

- **Key:** `B69`  
- **Name:** birdie69  
- **URL:** `https://narwhal.atlassian.net/wiki/spaces/B69`

---

## Learning Objectives

This project is a structured learning exercise. Primary goals:

1. Master AI-driven multi-agent development workflows
2. Practice Clean Architecture + DDD in .NET 8
3. Learn Capacitor-based cross-platform mobile development
4. Configure and use Terraform (Brick→Blueprint→Env) for Azure
5. Set up a production-grade CI/CD pipeline with GitHub Actions
6. Integrate Azure AD B2C for externalized identity management
7. Document every architectural decision as an ADR
8. Maintain dual-homed documentation (repo + Confluence)
