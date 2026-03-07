#!/usr/bin/env python3
"""Re-import Confluence pages with proper markdown → Confluence storage format.

Usage:
    python3 cf_sync.py [DOCS_ROOT]

    DOCS_ROOT  Path to the blog-docs repository root.
               Defaults to the directory two levels above this script
               (.claude/scripts/ → blog-docs/).
               Can also be set via the BLOG_DOCS_ROOT environment variable.
"""

import os, re, json, sys, time, urllib.request, urllib.error, base64, hashlib
from pathlib import Path

# --- Credentials (required) ---
_missing = [v for v in ("ATLASSIAN_EMAIL", "ATLASSIAN_TOKEN") if not os.environ.get(v)]
if _missing:
    print(
        f"Error: required environment variable(s) not set: {', '.join(_missing)}\n"
        f"Export them before running this script:\n"
        f"  export ATLASSIAN_EMAIL='your@email.com'\n"
        f"  export ATLASSIAN_TOKEN='your-api-token'",
        file=sys.stderr,
    )
    sys.exit(1)

EMAIL = os.environ["ATLASSIAN_EMAIL"]
TOKEN = os.environ["ATLASSIAN_TOKEN"]
BASE_URL = "https://narwhal.atlassian.net/wiki/rest/api"
auth_header = base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_header}"
}

# --- Docs root (portable) ---
# Resolution order: CLI arg > env var > relative to script location
_script_dir = Path(__file__).resolve().parent          # .claude/scripts/
_default_docs = _script_dir.parent.parent              # blog-docs/
if len(sys.argv) > 1:
    DOCS = Path(sys.argv[1]).resolve()
elif os.environ.get("BLOG_DOCS_ROOT"):
    DOCS = Path(os.environ["BLOG_DOCS_ROOT"]).resolve()
else:
    DOCS = _default_docs

if not DOCS.is_dir():
    print(
        f"Error: docs root does not exist or is not a directory: {DOCS}\n"
        f"Pass the correct path as an argument or set BLOG_DOCS_ROOT.",
        file=sys.stderr,
    )
    sys.exit(1)

# --- Mermaid macro config (Tech Labs "Mermaid for Confluence" plugin) ---
# Macro name confirmed from live Confluence page inspection.
# Theme options: default, forest, dark, neutral
MERMAID_MACRO = "mermaidjs"
MERMAID_THEME = "forest"

# Page ID mapping (from initial import)
PAGES = {
    "Project Charter":                  ("90997101", None),
    "Architecture Overview":            ("91095057", None),
    "AI Agent Roster":                  ("90997117", None),
    "Getting Started":                  ("91095073", None),
    "Roadmap – Week 1-2":              ("90997133", None),
    "Authentication Requirements":      ("90898451", "90898436"),
    "User Stories – Authentication":    ("91095089", "90898436"),
    "Backlog – Authentication":         ("90997149", "91062273"),
    "Authentication HLD":               ("91062318", "91095041"),
    "ADR-002: JWT Authentication":      ("90898467", "91062288"),
    "ADR-003: Provider Integration":    ("90997165", "91062288"),
    "ADR-004: Terraform Brick-Blueprint-Env": ("91062458", "91062288"),
    "Authentication API v1":            ("90898483", "91062303"),
}

FILE_MAP = {
    "Project Charter":                  DOCS / "PROJECT_CHARTER_v0.md",
    "Architecture Overview":            DOCS / "ARCHITECTURE_OVERVIEW.md",
    "AI Agent Roster":                  DOCS / "AGENT_ROSTER.md",
    "Getting Started":                  DOCS / "GETTING_STARTED.md",
    "Roadmap – Week 1-2":              DOCS / "ROADMAP_WEEK_1_2.md",
    "Authentication Requirements":      DOCS / "requirements/authentication-requirements.md",
    "User Stories – Authentication":    DOCS / "requirements/user-stories-authentication.md",
    "Backlog – Authentication":         DOCS / "planning/backlog-authentication.md",
    "Authentication HLD":               DOCS / "architecture/authentication-hld.md",
    "ADR-002: JWT Authentication":      DOCS / "adrs/ADR-002-jwt-authentication.md",
    "ADR-003: Provider Integration":    DOCS / "adrs/ADR-003-provider-integration.md",
    "ADR-004: Terraform Brick-Blueprint-Env": DOCS / "adrs/ADR-004-terraform-brick-blueprint-env.md",
    "Authentication API v1":            DOCS / "api-specs/authentication-api-v1.yaml",
}


def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_format(text):
    """Apply inline markdown formatting."""
    text = escape_html(text)
    # Bold-italic ***text*** or ___text___ — must be matched BEFORE the
    # separate bold and italic patterns, otherwise the bold regex consumes
    # '**' from '***', leaving a stray '*' that the italic regex picks up
    # and wraps around already-emitted HTML tags, producing malformed output.
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'___(.+?)___', r'<strong><em>\1</em></strong>', text)
    # Bold **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # Italic *text* or _text_ (but not inside words)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'<em>\1</em>', text)
    # Inline code `text`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Strikethrough ~~text~~
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    return text


def parse_table(lines, start):
    """Parse a markdown table block starting at 'start', return (html, next_idx)."""
    rows = []
    i = start
    while i < len(lines) and lines[i].strip().startswith('|'):
        row = lines[i].strip()
        cells = [c.strip() for c in row.split('|')[1:-1]]
        rows.append(cells)
        i += 1

    if not rows:
        return '', start + 1

    def is_separator(cells):
        return all(re.match(r'^:?-+:?$', c.replace(' ', '')) for c in cells if c)

    has_header = len(rows) > 1 and is_separator(rows[1])

    thead_html = ''
    tbody_rows = []

    for idx, cells in enumerate(rows):
        if is_separator(cells):
            continue
        if has_header and idx == 0:
            row_html = ''.join(f'<th><p>{inline_format(c)}</p></th>' for c in cells)
            thead_html = f'<thead><tr>{row_html}</tr></thead>'
        else:
            row_html = ''.join(f'<td><p>{inline_format(c)}</p></td>' for c in cells)
            tbody_rows.append(f'<tr>{row_html}</tr>')

    tbody_html = f'<tbody>{"".join(tbody_rows)}</tbody>' if tbody_rows else ''
    return f'<table>{thead_html}{tbody_html}</table>', i


def parse_list(lines, start, ordered=False):
    """Parse a list block, return (html, next_idx)."""
    tag = 'ol' if ordered else 'ul'
    items = []
    i = start
    pattern = re.compile(r'^\d+\.\s+') if ordered else re.compile(r'^[-*]\s+')

    while i < len(lines):
        line = lines[i]
        if ordered:
            m = re.match(r'^\d+\.\s+(.*)', line)
        else:
            m = re.match(r'^[-*]\s+(.*)', line)
        if m:
            items.append(f'<li><p>{inline_format(m.group(1))}</p></li>')
            i += 1
        else:
            break

    return f'<{tag}>{"".join(items)}</{tag}>', i


def md_to_storage(md: str) -> str:
    """Convert markdown to Confluence storage format."""
    lines = md.split('\n')
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Code block
        if line.startswith('```'):
            lang = line[3:].strip() or 'text'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            body = '\n'.join(code_lines)
            if lang == 'mermaid':
                # Mermaid diagrams need the Tech Labs mermaidjs macro.
                # The plugin expects the diagram wrapped in JSON as
                # {"diagramDefinition": "<mermaid code>"}.
                #
                # CDATA safety: if body contains ']]>' we must prevent it
                # from prematurely terminating the CDATA section. We use a
                # JSON Unicode escape (\u003e for '>') rather than CDATA
                # splitting, because Confluence macro processors often strip
                # only the outer <![CDATA[ / ]]> markers without re-joining
                # adjacent CDATA sections — making split CDATA unreliable.
                # Any spec-compliant JSON parser decodes \u003e back to '>',
                # so the mermaid plugin receives the correct diagram text.
                diagram_json = json.dumps({"diagramDefinition": body})
                safe_content = diagram_json.replace(']]>', r']]\u003e')
                # Stable filename derived from content so repeated syncs
                # don't create orphaned attachments on the Confluence page.
                file_name = f"mermaid_{hashlib.md5(body.encode()).hexdigest()[:16]}"
                output.append(
                    f'<ac:structured-macro ac:name="{MERMAID_MACRO}" ac:schema-version="1">'
                    f'<ac:parameter ac:name="fileName">{file_name}</ac:parameter>'
                    f'<ac:parameter ac:name="theme">{MERMAID_THEME}</ac:parameter>'
                    f'<ac:parameter ac:name="version">2</ac:parameter>'
                    f'<ac:plain-text-body><![CDATA[{safe_content}]]></ac:plain-text-body>'
                    f'</ac:structured-macro>'
                )
            else:
                # Generic code block — escape ]]> to prevent CDATA early-close.
                safe_body = body.replace(']]>', ']]]]><![CDATA[>')
                output.append(
                    f'<ac:structured-macro ac:name="code">'
                    f'<ac:parameter ac:name="language">{lang}</ac:parameter>'
                    f'<ac:plain-text-body><![CDATA[{safe_body}]]></ac:plain-text-body>'
                    f'</ac:structured-macro>'
                )
            # Only skip the closing ``` if we didn't reach EOF
            if i < len(lines):
                i += 1
            continue

        # Heading
        if line.startswith('#'):
            m = re.match(r'^(#{1,6})\s+(.*)', line)
            if m:
                level = len(m.group(1))
                text = inline_format(m.group(2))
                output.append(f'<h{level}>{text}</h{level}>')
                i += 1
                continue

        # Table
        if line.strip().startswith('|'):
            html, i = parse_table(lines, i)
            output.append(html)
            continue

        # Horizontal rule — must be checked before unordered list,
        # because spaced variants like "- - -" also match the list regex.
        # Matches the full CommonMark spec: 3+ hyphens, asterisks, or
        # underscores (with optional spaces between), nothing else on the line.
        if re.match(r'^ {0,3}([-*_]) *(?:\1 *){2,}$', line):
            output.append('<hr/>')
            i += 1
            continue

        # Unordered list
        if re.match(r'^[-*]\s+', line):
            html, i = parse_list(lines, i, ordered=False)
            output.append(html)
            continue

        # Ordered list
        if re.match(r'^\d+\.\s+', line):
            html, i = parse_list(lines, i, ordered=True)
            output.append(html)
            continue

        # Blockquote
        if line.startswith('> '):
            text = inline_format(line[2:])
            output.append(f'<blockquote><p>{text}</p></blockquote>')
            i += 1
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Regular paragraph
        output.append(f'<p>{inline_format(line)}</p>')
        i += 1

    return '\n'.join(output)


def get_version(page_id):
    """Return (version_number, title) or raise on network/API failure."""
    req = urllib.request.Request(
        f"{BASE_URL}/content/{page_id}?expand=version",
        headers=headers
    )
    try:
        with urllib.request.urlopen(req) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GET version failed (HTTP {e.code}): {e.read().decode()[:200]}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"GET version failed (network): {e.reason}")

    try:
        return d["version"]["number"], d["title"]
    except KeyError as e:
        raise RuntimeError(f"Unexpected response shape, missing key {e}: {str(d)[:200]}")


def update_page(page_id, title, content):
    """Return (page_id, None) on success or (None, error_message) on failure."""
    try:
        version, _ = get_version(page_id)
    except RuntimeError as e:
        return None, str(e)

    payload = {
        "version": {"number": version + 1},
        "type": "page",
        "title": title,
        "body": {"storage": {"value": content, "representation": "storage"}}
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/content/{page_id}",
        data=data, headers=headers, method="PUT"
    )
    try:
        with urllib.request.urlopen(req) as r:
            d = json.loads(r.read())
            return d["id"], None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:200]}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"


print("🔄 Re-importing Confluence pages with proper formatting...\n")

failed = []
for title, (page_id, _) in PAGES.items():
    filepath = FILE_MAP[title]
    if not filepath.exists():
        print(f"  ⚠️  Skipped (file not found): {title}")
        continue

    try:
        md = filepath.read_text(encoding='utf-8')
        content = md_to_storage(md)
    except OSError as e:
        print(f"  ❌ Failed to read '{title}': {e}")
        failed.append(title)
        continue

    pid, err = update_page(page_id, title, content)

    if pid:
        print(f"  ✅ Updated: {title}")
    else:
        print(f"  ❌ Failed: {title}: {err[:120]}")
        failed.append(title)

    time.sleep(1)

print(f"\n{'✅' if not failed else '⚠️ '} Re-import complete — "
      f"{len(PAGES) - len(failed)}/{len(PAGES)} pages updated.")
if failed:
    print("Failed pages:")
    for t in failed:
        print(f"  - {t}")
print("🔗 https://narwhal.atlassian.net/wiki/spaces/CLAUDELEARN")
