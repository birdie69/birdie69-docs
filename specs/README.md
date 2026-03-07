# specs/ — Original Product Specification Documents

This directory contains the original business specification documents created before development started.  
They serve as the **authoritative source of product intent** and contain more detail than the derived documentation.

| File | Description |
|------|-------------|
| `product-specification.md` | Product vision, problem statement, core features, user flows, monetization, success metrics |
| `complete-development-plan.md` | Technology stack, architecture, repository structure, week-by-week plan, DB schema, API endpoints, DevOps, cost |
| `uiux-design-system-wireframes.md` | Design principles, color system, typography, components, screen wireframes, animations, accessibility |

## Relationship to other docs

These specs are the **input** to the AI agent workflow.  
The derived documents (PROJECT_CHARTER, ARCHITECTURE_OVERVIEW, ADRs, requirements) are outputs of analyzing these specs.

Where these specs and derived docs differ, the derived docs (which went through architectural review) take precedence.  
Contradictions should be flagged and resolved as new ADRs.
