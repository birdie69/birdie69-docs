# AI Agent Roster — birdie69

**Version:** 1.0  
**Last Updated:** 2026-02-14  
**Project:** birdie69

---

## Overview

birdie69 is built by a solo developer orchestrating a team of specialized AI agents.  
Each agent has a defined role, scope, and prompt template.  
The **Instructor** (this chat) coordinates all agents.

---

## Agent Roster

| Agent | Codename | Role | Prompt |
|-------|----------|------|--------|
| Instructor | — | Orchestrator — coordinates all agents, makes final calls | (main chat, orchestration mode) |
| Business Analyst | `agent-ba` | Requirements, user stories, acceptance criteria | `.claude/prompts/agent-ba.md` |
| Solution Architect | `agent-sa` | HLD, ADRs, API contracts, domain model | `.claude/prompts/agent-sa.md` |
| Developer | `agent-dev` | Implementation (.NET 8, Next.js, Strapi, Capacitor) | `.claude/prompts/agent-dev.md` |
| Product Manager | `agent-pm` | Backlog, sprint planning, Jira management | `.claude/prompts/agent-pm.md` |
| DevOps | `agent-devops` | Terraform, GitHub Actions, Docker, Azure deployment | `.claude/prompts/agent-devops.md` |

---

## Agent Responsibilities Matrix

| Task | BA | SA | Dev | PM | DevOps | Instructor |
|------|----|----|-----|----|--------|------------|
| Define requirements | ✅ | — | — | — | — | — |
| Write user stories | ✅ | — | — | — | — | — |
| Design architecture | — | ✅ | — | — | — | — |
| Write ADRs | — | ✅ | — | — | — | — |
| Define API contract | — | ✅ | — | — | — | — |
| Implement features | — | — | ✅ | — | — | — |
| Write tests | — | — | ✅ | — | — | — |
| Docker / CI/CD | — | — | — | — | ✅ | — |
| Terraform | — | — | — | — | ✅ | — |
| Manage backlog | — | — | — | ✅ | — | — |
| Plan sprints | — | — | — | ✅ | — | — |
| Start/close sprints | — | — | — | — | — | ✅ signals → Human |
| Update Jira | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Sync to Confluence | ✅ | ✅ | ✅ | ✅ | ✅ | — |

---

## How to Activate an Agent

Open a new Cursor chat in **Agent mode**, then paste:

```
Load `.claude/rules/global.md` and `.claude/prompts/agent-[ROLE].md`.

CONTEXT:
- Repository: [birdie69-docs / birdie69-api / birdie69-web / etc.]
- Phase: [Phase 0 / Sprint 1 / etc.]
- Jira ticket: B69-NN

TASK:
[describe the task]
```

---

## Agent Communication Flow

```
Human (you)
    ↕
Instructor (main chat — orchestration)
    ↕ signals work items
BA Agent → SA Agent → Dev Agent
                          ↕
                     DevOps Agent
    ↕ sprint management
PM Agent
```

1. **Human** signals to Instructor what phase/feature to work on
2. **Instructor** activates BA agent to write user stories
3. **Instructor** activates SA agent to design architecture / ADRs
4. **Instructor** activates Dev agent to implement
5. **Instructor** activates DevOps agent for infra / CI/CD
6. **Instructor** signals PM agent to groom backlog (on explicit request)
7. **Human** clicks "Start Sprint" in Jira (on Instructor signal)

---

## Rules All Agents Must Follow

See `.claude/rules/global.md` — mandatory reading before every task.

Key rules:
- Language: code/docs in **English**, chat in **Hungarian**
- Every task ends with: Jira update + Confluence sync + ROADMAP update
- No direct push to `main` — always via PR
- No secrets in code — Azure Key Vault for all secrets
- Jira key: `B69`
- Confluence space: `B69` (`https://narwhal.atlassian.net/wiki/spaces/B69`)
