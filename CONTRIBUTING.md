# Contribution Guide

Please add a file `registry/<your-institution>.yaml` validated by the schema.

- **Required**: `id` (ROR), `institution`,  `repositories[].name`, `repositories[].status`.
- **Recommended**: `repositories[].url`, `api_rest`, `oai_pmh`, `software`, `dspace_version`, `contact`, `last_verified`, `code[]` with `description`.

### Local validation
```
pip install -r requirements.txt
python scripts/validate.py
```

### Site generation
```
python scripts/generate_site.py
mkdocs build
mkdocs serve
```
