#!/usr/bin/env python3
import pathlib, yaml, html
from slugify import slugify

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG_DIR = ROOT / "registry"
DOCS_DIR = ROOT / "docs"

def yaml_loader_without_timestamps():
    class NoTSLoader(yaml.SafeLoader):
        pass
    for ch, resolvers in list(NoTSLoader.yaml_implicit_resolvers.items()):
        NoTSLoader.yaml_implicit_resolvers[ch] = [
            (tag, regexp) for tag, regexp in resolvers if tag != 'tag:yaml.org,2002:timestamp'
        ]
    return NoTSLoader

def write_markdown(p: pathlib.Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def _esc(s):
    return html.escape(str(s), quote=True)

def render_repo_table(entry: dict) -> str:
    rows = []
    for inst in entry.get("repositories", []):
        inst_name = inst.get("name", "")
        for comp in inst.get("code", []) or []:
            rows.append(
                {
                    "repository": inst_name,
                    "type": comp.get("type", ""),
                    "repo": comp.get("repo", ""),
                    "description": comp.get("description", ""),
                    "language": comp.get("language", ""),
                    "license": comp.get("license", ""),
                }
            )
    if not rows:
        return "_No linked code repositories shared._"

    lines = []
    lines.append('<table class="datatable">')
    lines.append("<thead><tr>")
    for col in [
        "Repository",
        "Type",
        "Source code",
        "Description",
        "Language",
        "License",
    ]:
        lines.append(f"<th>{_esc(col)}</th>")
    lines.append("</tr></thead>")
    lines.append("<tbody>")
    for r in rows:
        link = (
            f'<a href="{_esc(r["repo"])}" target="_blank" rel="noopener">{_esc(r["repo"])}</a>'
            if r["repo"]
            else ""
        )

        # helper for tag span
        def tag_html(value, cls="tag"):
            return f'<span class="{cls}">{_esc(value)}</span>' if value else ""

        lines.append("<tr>")
        lines.append(f"<td>{_esc(r['repository'])}</td>")
        lines.append(f"<td>{tag_html(r['type'], 'tag type-tag')}</td>")
        lines.append(f"<td>{link}</td>")
        lines.append(f"<td>{_esc(r['description'])}</td>")
        lines.append(f"<td>{tag_html(r['language'], 'tag lang-tag')}</td>")
        lines.append(f"<td>{tag_html(r['license'], 'tag license-tag')}</td>")
        lines.append("</tr>")
    lines.append("</tbody></table>")
    return "\n".join(lines)


def render_institution_page(entry: dict) -> str:
    lines = []
    lines.append(f"# {entry['institution']} 🇨🇭")
    lines.append("")
    lines.append(f"- **ROR**: `{entry['id']}`")
    lines.append("")
    lines.append("## Repositories")
    for inst in entry.get("repositories", []):
        lines.append(f"### {inst['name']}")
        if inst.get("url"):
            lines.append(f"- URL: [{inst['url']}]({inst['url']})")
        if inst.get("api_rest"):
            lines.append(f"- REST API: [{inst['api_rest']}]({inst['api_rest']})")
        if inst.get("oai_pmh"):
            lines.append(f"- OAI-PMH: [{inst['oai_pmh']}]({inst['oai_pmh']})")
        if inst.get("software"):
            lines.append(f"- Software: `{inst['software']}`")
        if inst.get("dspace_version"):
            lines.append(f"- DSpace version: `{inst['dspace_version']}`")
        lines.append(f"- Status: `{inst['status']}`")
        if inst.get("contact"):
            lines.append(f"- Contact: `{inst['contact']}`")
        if inst.get("last_verified"):
            lines.append(f"- Last verified: `{inst['last_verified']}`")
        lines.append("")
    lines.append("## Linked code repositories")
    lines.append(render_repo_table(entry))
    lines.append("")
    return "\n".join(lines)

def build_catalog(entries: list) -> str:
    lines = []
    lines.append("# Institutions List")
    lines.append("")
    lines.append("| Institution | ROR | Repositories |")
    lines.append("|---|---|---|")
    for e in entries:
        inst_names = ", ".join(i["name"] for i in e.get("repositories", []))
        page = f"institutions/{slugify(e['id'])}.md"
        lines.append(f"| [{e['institution']}]({page}) | `{e['id']}` | {inst_names} |")
    lines.append("")
    return "\n".join(lines)

def main():
    Loader = yaml_loader_without_timestamps()
    entries = []
    for yml in sorted(REG_DIR.glob("*.yaml")):
        data = yaml.load(yml.read_text(encoding="utf-8"), Loader=Loader)
        entries.append(data)
        out = DOCS_DIR / "institutions" / f"{slugify(data['id'])}.md"
        write_markdown(out, render_institution_page(data))

    write_markdown(DOCS_DIR / "institutions.md", build_catalog(entries))

if __name__ == "__main__":
    main()
