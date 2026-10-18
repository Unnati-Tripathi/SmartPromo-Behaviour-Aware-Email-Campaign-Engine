#!/usr/bin/env python3
"""
preview.py — Render the SmartPromo email template with sample data and open
it in the default browser for local inspection.

Usage:
    python3 preview.py                   # opens in browser
    python3 preview.py --out preview.html # writes to file only

This script performs simple {{PLACEHOLDER}} replacement using Python's
str.replace(). It intentionally avoids Jinja2 or other template engines
at this stage to keep dependencies at zero.

Personalization values are safely HTML-escaped before insertion.
"""

import argparse
import html
import os
import sys
import tempfile
import webbrowser
from pathlib import Path

# ---------------------------------------------------------------------------
# Sample data — will be replaced by CSV-driven data in later stages
# ---------------------------------------------------------------------------
SAMPLE_DATA = {
    "FIRST_NAME": "Priya",
    "COUPON_CODE": "AUTUMN20-VLR",
    "CUSTOMER_ID": "CUST-10042",
}

TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "promo-email.html"


def render_template(template_text: str, data: dict[str, str]) -> str:
    """Replace {{KEY}} placeholders with HTML-escaped values.

    If a key is missing from *data*, the placeholder is replaced with a
    safe fallback so the rendered HTML is never broken.
    """
    rendered = template_text
    for key, value in data.items():
        safe_value = html.escape(str(value))
        rendered = rendered.replace("{{" + key + "}}", safe_value)

    # Replace any remaining unreplaced placeholders with a visible fallback
    import re
    remaining = re.findall(r"\{\{(\w+)\}\}", rendered)
    for placeholder in remaining:
        rendered = rendered.replace(
            "{{" + placeholder + "}}",
            html.escape(f"[{placeholder}]"),
        )

    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview SmartPromo email template")
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Write rendered HTML to this path instead of opening a browser",
    )
    parser.add_argument(
        "--data",
        nargs="*",
        metavar="KEY=VALUE",
        help="Override sample data, e.g. --data FIRST_NAME=Alex COUPON_CODE=SAVE10",
    )
    args = parser.parse_args()

    # Load template
    if not TEMPLATE_PATH.exists():
        print(f"Error: template not found at {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Merge overrides
    data = dict(SAMPLE_DATA)
    if args.data:
        for pair in args.data:
            if "=" not in pair:
                print(f"Warning: ignoring invalid override '{pair}' (expected KEY=VALUE)")
                continue
            key, value = pair.split("=", 1)
            data[key.strip()] = value.strip()

    # Render
    rendered_html = render_template(template_text, data)

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(rendered_html, encoding="utf-8")
        print(f"✓ Rendered email written to {out_path.resolve()}")
    else:
        # Write to temp file and open in browser
        out_path = Path(__file__).resolve().parent / "preview_output.html"
        out_path.write_text(rendered_html, encoding="utf-8")
        print(f"✓ Rendered email written to {out_path}")
        webbrowser.open(out_path.as_uri())
        print("✓ Opened in default browser")


if __name__ == "__main__":
    main()
