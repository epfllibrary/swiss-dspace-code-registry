#!/usr/bin/env python3
import sys, json, pathlib
from jsonschema import Draft202012Validator
import yaml, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "registry.schema.json"
REG_DIR = ROOT / "registry"

def yaml_loader_without_timestamps():
    class NoTSLoader(yaml.SafeLoader):
        pass
    # prevent implicit timestamp resolution: keep dates as strings
    for ch, resolvers in list(NoTSLoader.yaml_implicit_resolvers.items()):
        NoTSLoader.yaml_implicit_resolvers[ch] = [
            (tag, regexp) for tag, regexp in resolvers if tag != 'tag:yaml.org,2002:timestamp'
        ]
    return NoTSLoader

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def iter_registry_files():
    for p in sorted(REG_DIR.glob("*.yaml")):
        yield p

def http_ok(url: str) -> bool:
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        if r.status_code >= 400 or r.status_code == 405:
            r = requests.get(url, allow_redirects=True, timeout=10)
        return 200 <= r.status_code < 400
    except requests.RequestException:
        return False

def main():
    schema = load_schema()
    validator = Draft202012Validator(schema)
    Loader = yaml_loader_without_timestamps()

    errors_found = 0
    for path in iter_registry_files():
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=Loader)
        errs = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errs:
            print(f"[ERROR] {path.name} is invalid:")
            for e in errs:
                loc = "/".join(map(str, e.path)) or "<root>"
                print(f"  - {loc}: {e.message}")
            errors_found += 1
        else:
            print(f"[OK] {path.name} matches the schema")

        # URL checks (optional but helpful)
        if isinstance(data, dict):
            for inst in data.get("repositories", []):
                for key in ("url", "api_rest", "oai_pmh"):
                    if key in inst:
                        ok = http_ok(inst[key])
                        print(f"    {key}: {inst[key]} -> {'OK' if ok else 'FAIL'}")
                        if not ok: errors_found += 1
                for comp in inst.get("code", []) or []:
                    repo = comp.get("repo")
                    if repo:
                        ok = http_ok(repo)
                        print(f"    Repo: {repo} -> {'OK' if ok else 'FAIL'}")
                        if not ok: errors_found += 1

    if errors_found:
        print(f"\nValidation finished with {errors_found} error(s).", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nValidation successful.")
        sys.exit(0)

if __name__ == "__main__":
    main()
