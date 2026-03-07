# .claude/ — AI Agent Workspace — birdie69

This directory contains all AI agent prompts, rules, and automation scripts for the **birdie69** project.

---

## Structure

```
.claude/
├── README.md              ← This file
├── rules/
│   └── global.md          ← Project-wide rules (ALL agents must read this first)
├── prompts/
│   ├── agent-ba.md        ← Business Analyst agent
│   ├── agent-sa.md        ← Solution Architect agent
│   ├── agent-dev.md       ← Developer agent
│   ├── agent-pm.md        ← Product Manager agent
│   ├── agent-devops.md    ← DevOps / Infrastructure agent
│   └── doc-sync.md        ← Documentation sync (Confluence)
└── scripts/
    └── cf_sync.py         ← Python script for Confluence sync
```

---

## How to Activate an Agent

Open a new Cursor chat in **Agent mode**, then paste:

```
Load `.claude/rules/global.md` and `.claude/prompts/agent-[ROLE].md`.

CONTEXT:
- Repository: birdie69-docs
- Phase: [current phase]

TASK:
[describe the task]
```

Replace `[ROLE]` with: `ba`, `sa`, `dev`, `pm`, or `devops`.

---

## Agent Roles Quick Reference

| Agent | When to use |
|-------|------------|
| `agent-ba` | Writing user stories, acceptance criteria, business rules |
| `agent-sa` | Architecture decisions, ADRs, API design, Mermaid diagrams |
| `agent-dev` | Implementation, code review, Docker, CI/CD config |
| `agent-pm` | Backlog grooming, sprint planning, Jira management |
| `agent-devops` | Terraform, GitHub Actions, Azure configuration |

---

## Doc Sync

To sync documentation to Confluence after making changes:

```
Load `.claude/prompts/doc-sync.md`

FILES_CHANGED:
- ROADMAP.md
- requirements/product-requirements.md

Sync to Confluence space B69.
```

---

## Jira Project

**Key:** `B69`  
**URL:** `https://narwhal.atlassian.net/projects/B69`

## Confluence Space

**Key:** `B69`  
**URL:** `https://narwhal.atlassian.net/wiki/spaces/B69`
