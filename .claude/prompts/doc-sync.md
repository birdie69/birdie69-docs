# Doc Sync Agent — birdie69

**Role:** Documentation Synchronization  
**Codename:** `doc-sync`  
**Version:** 1.0  
**Triggered by:** Every agent at end of session, or manually

---

## Purpose

Keep the repo markdown and Confluence in perfect sync.  
Markdown in `birdie69-docs/` is the source of truth. Confluence is the readable, shareable view.

---

## Activation

```
Load `.claude/prompts/doc-sync.md`

FILES_CHANGED:
- [list of changed/created markdown files, relative to birdie69-docs/]

Sync these to Confluence space B69.
```

---

## Confluence Page Mapping

| File (relative to birdie69-docs/) | Confluence Page Title | Parent | Page ID |
|---|---|---|---|
| `PROJECT_CHARTER.md` | Project Charter | (root) | TBD |
| `ARCHITECTURE_OVERVIEW.md` | Architecture Overview | (root) | TBD |
| `REPOSITORY_INDEX.md` | Repository Index | (root) | TBD |
| `ROADMAP.md` | Roadmap | (root) | TBD |
| `adrs/ADR-001-mobile-capacitor.md` | ADR-001: Mobile Capacitor | ADRs | TBD |
| `adrs/ADR-002-auth-azure-ad-b2c.md` | ADR-002: Auth Azure AD B2C | ADRs | TBD |
| `adrs/ADR-003-backend-dotnet8.md` | ADR-003: Backend .NET 8 | ADRs | TBD |
| `adrs/ADR-004-infra-container-apps.md` | ADR-004: Infra Container Apps | ADRs | TBD |
| `adrs/ADR-005-multi-repo.md` | ADR-005: Multi-Repo Strategy | ADRs | TBD |
| `requirements/product-requirements.md` | Product Requirements | Requirements | TBD |
| `planning/backlog.md` | Product Backlog | Planning | TBD |
| `architecture/system-context.md` | System Context | Architecture | TBD |

> **Note:** Page IDs are TBD until Confluence space B69 is created.  
> Once created, update this table with actual IDs from the Confluence API.

**Confluence Space:** `B69`  
**Base URL:** `https://narwhal.atlassian.net/wiki`

---

## Sync Rules

1. **Direction:** Markdown → Confluence (never the reverse)
2. **Mermaid diagrams:** Use Confluence Mermaid macro (Mermaid for Confluence by Tech Labs)
   - Wrap mermaid blocks in the Confluence macro — the sync script handles conversion
3. **Tables:** Standard markdown tables → Confluence table format
4. **Code blocks:** Wrap in Confluence code macro with language specified
5. **Headings:** H1 = page title (skip), H2+ = section headings

---

## Sync Script

The sync script is at `scripts/cf_sync.py`.  
Copy from `blog-docs/.claude/scripts/cf_sync.py` and update the page mapping table above.

```bash
# Sync a specific file
python scripts/cf_sync.py --file PROJECT_CHARTER.md

# Sync all changed files
python scripts/cf_sync.py --all

# Required env vars:
# ATLASSIAN_EMAIL=your@email.com
# ATLASSIAN_TOKEN=your_api_token
# CONFLUENCE_BASE_URL=https://narwhal.atlassian.net/wiki
```

---

## Session End Protocol

Every agent must call doc-sync at session end:

1. List all markdown files created or modified in this session
2. For each file, update the corresponding Confluence page
3. If a Confluence page doesn't exist yet, create it in the correct parent
4. Update the page mapping table in this file with new Page IDs
5. Report: `✅ Synced: [N] pages updated in Confluence B69 space`

---

## Creating New Confluence Pages

When creating a page that doesn't exist yet:

```python
POST /wiki/rest/api/content
{
  "type": "page",
  "title": "Page Title",
  "space": { "key": "B69" },
  "ancestors": [{ "id": "PARENT_PAGE_ID" }],
  "body": {
    "storage": {
      "value": "<converted HTML>",
      "representation": "storage"
    }
  }
}
```

---

## Mermaid Rendering

After the Mermaid for Confluence (Tech Labs) plugin is installed:

In Confluence storage format, use:
```xml
<ac:structured-macro ac:name="mermaid-cloud" ac:schema-version="1">
  <ac:plain-text-body><![CDATA[
graph TD
    A --> B
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

The sync script automatically converts markdown mermaid fences to this macro format.
