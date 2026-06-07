#!/usr/bin/env python3
"""Generate an interactive 3D graph viewer as a self-contained HTML file.

Usage:
    python3 generate_viewer.py --graph GRAPH_JSON --catalog CATALOG_JSON --output OUTPUT_HTML

Inputs:
    --graph:   Output of skill-graph/scripts/scan_skills.py --json
    --catalog: Output of skill-catalog/scripts/extract_catalog.py
    --output:  Path for the generated HTML file (default: ~/workshop/outputs/skill-catalog/)
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "viewer-template-3d.html"
_OUTPUTS_ROOT = os.path.expanduser(
    os.environ.get("CLAUDE_OUTPUTS_DIR", "~/workshop/outputs")
)
DEFAULT_OUTPUT = os.path.join(
    _OUTPUTS_ROOT,
    "skill-catalog",
    f"{date.today().isoformat()}-skill-graph-viewer.html",
)


def main():
    parser = argparse.ArgumentParser(
        description="Generate interactive skill graph viewer"
    )
    parser.add_argument(
        "--graph", required=True, help="Graph JSON file (from scan_skills.py)"
    )
    parser.add_argument(
        "--catalog", required=True, help="Catalog JSON file (from extract_catalog.py)"
    )
    parser.add_argument(
        "--output", "-o", default=DEFAULT_OUTPUT, help="Output HTML path"
    )
    args = parser.parse_args()

    graph_data = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    catalog_data = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Merge catalog data into graph nodes
    catalog_map = {c["name"]: c for c in catalog_data}
    for node in graph_data.get("nodes", []):
        cat = catalog_map.get(node["id"], {})
        node["strengths"] = cat.get("strengths", [])
        node["pain_point"] = cat.get("pain_point", "")
        node["triggers"] = cat.get("triggers", [])
        node["domain"] = cat.get("domain", "general")
        node["tags"] = cat.get("tags", [])
        node["guide"] = cat.get("guide", "")

    # Inject data into template (replace placeholder + its default fallback value)
    html = template.replace(
        "/*__GRAPH_DATA__*/{nodes:[],edges:[],compositions:[],stats:{}}",
        json.dumps(graph_data, ensure_ascii=False),
    )
    html = html.replace(
        "/*__CATALOG_DATA__*/[]",
        json.dumps(catalog_data, ensure_ascii=False),
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Viewer generated: {output_path}", file=sys.stderr)
    print(f"  Nodes: {len(graph_data.get('nodes', []))}", file=sys.stderr)
    print(f"  Edges: {len(graph_data.get('edges', []))}", file=sys.stderr)


if __name__ == "__main__":
    main()
