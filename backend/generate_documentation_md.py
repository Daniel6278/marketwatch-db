import requests
import json
from typing import Any, Dict

OPENAPI_URL = "https://specific-brande-data-group-585a3e34.koyeb.app/openapi.json"
OUTPUT_FILE = "API_ENDPOINTS_DOCUMENTATION.md"

def fetch_openapi_json(url: str) -> Dict[str,Any]:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def render_markdown(spec: Dict[str,Any]) -> str:
    md = []
    info = spec.get("info", {})
    title = info.get("title", "API Documentation")
    version = info.get("version", "")
    description = info.get("description", "")
    md.append(f"# {title}  \n")
    if version:
        md.append(f"**Version:** {version}  \n")
    if description:
        md.append(f"{description}  \n\n")

    paths = spec.get("paths", {})
    for path, methods in paths.items():
        md.append(f"## `{path}`\n")
        for method, op in methods.items():
            md.append(f"### {method.upper()}\n")
            summary = op.get("summary", "")
            if summary:
                md.append(f"*{summary}*  \n")
            description = op.get("description", "")
            if description:
                md.append(f"{description}  \n")
            # parameters
            params = op.get("parameters", [])
            if params:
                md.append("**Parameters:**  \n")
                for p in params:
                    name = p.get("name")
                    ptype = p.get("schema", {}).get("type", "")
                    md.append(f"- `{name}` ({ptype}) — {p.get('description', '')}  \n")
            # responses
            responses = op.get("responses", {})
            if responses:
                md.append("**Responses:**  \n")
                for code, resp in responses.items():
                    desc = resp.get("description", "")
                    md.append(f"- `{code}` — {desc}  \n")
            md.append("\n")
    return "".join(md)

def main():
    spec = fetch_openapi_json(OPENAPI_URL)
    markdown = render_markdown(spec)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"README generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
