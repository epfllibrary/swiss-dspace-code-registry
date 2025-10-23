# 🇨🇭 Swiss DSpace Code Registry (Scenario 2)

A lightweight, structured, and community-contributed **registry of code repositories** related to Swiss DSpace / DSpace-CRIS repositories
(customizations, middleware, modules, scripts, notebooks, frontends/backends). Data is stored as **YAML** files validated by a **JSON Schema**,
and a **static MkDocs site** is generated automatically.

## Swiss focus
This registry is intended for **institutions in Switzerland** (HEIs, research institutes, libraries) maintaining DSpace / DSpace-CRIS repositories.

## Overview
- `registry/*.yaml` — one file per institution (ROR required) listing repositories and linked repositories.
- `schema/registry.schema.json` — validation schema.
- `scripts/validate.py` — validates YAML against the schema, checks URLs.
- `scripts/generate_site.py` — generates Markdown pages from `registry/`.
- `mkdocs.yml` — site configuration (Material theme, red palette, Swiss flag logo).
- `.github/workflows/validate_and_build.yml` — CI: validation + generation + GitHub Pages deployment.

## Contributing (template with red placeholders)
Copy this template into `registry/<your-institution>.yaml` and replace every
<b><span style="color:red">RED</span></b> placeholder.

```yaml
id: <span style="color:red">ror:XXXXXXXXX</span>
institution: <span style="color:red">Your Institution</span>
repositories:
  - name: <span style="color:red">Repository Name</span>
    url: <span style="color:red">https://repo.example.ch</span>
    api_rest: <span style="color:red">https://repo.example.ch/server/api</span>
    oai_pmh: <span style="color:red">https://repo.example.ch/server/oai/</span>
    software: <span style="color:red">dspace</span>   # dspace | dspace-cris
    dspace_version: <span style="color:red">"7.6"</span>
    status: <span style="color:red">production</span>   # production | pilot | archived
    contact: <span style="color:red">contact@example.ch</span>
    last_verified: <span style="color:red">"2025-10-23"</span>
    code:
      - type: <span style="color:red">dspace-frontend</span>   # customization | module | middleware | simple-script | notebook | dspace-frontend | dspace-backend
        repo: <span style="color:red">https://github.com/org/repo</span>
        description: <span style="color:red">Short sentence describing the repository.</span>
        language: <span style="color:red">TypeScript</span>
        license: <span style="color:red">MIT</span>
```

### Run locally
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python scripts/validate.py
python scripts/generate_site.py
mkdocs serve
```

## License
MIT
