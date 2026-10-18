#!/usr/bin/env python3
"""
test_template.py — Automated tests for the SmartPromo email template.

Tests cover:
  1. Template file exists and is valid HTML structure.
  2. All expected placeholders are present in the raw template.
  3. Rendering replaces placeholders correctly.
  4. HTML escaping prevents injection.
  5. Missing data produces safe fallback output.
  6. Rendered HTML contains required structural elements.
"""

import re
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from preview import render_template

TEMPLATE_PATH = PROJECT_ROOT / "templates" / "promo-email.html"


def load_template() -> str:
    """Load the raw email template."""
    assert TEMPLATE_PATH.exists(), f"Template not found: {TEMPLATE_PATH}"
    return TEMPLATE_PATH.read_text(encoding="utf-8")


# ── Test: Template file exists ──────────────────────────────────────────────

def test_template_exists():
    assert TEMPLATE_PATH.exists(), "promo-email.html must exist in templates/"
    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert len(content) > 500, "Template seems too short to be a real email"


# ── Test: Required placeholders present ─────────────────────────────────────

def test_placeholders_present():
    raw = load_template()
    required_placeholders = ["{{FIRST_NAME}}", "{{COUPON_CODE}}", "{{CUSTOMER_ID}}"]
    for ph in required_placeholders:
        assert ph in raw, f"Missing placeholder: {ph}"


# ── Test: Rendering replaces placeholders ───────────────────────────────────

def test_rendering_replaces_placeholders():
    raw = load_template()
    data = {
        "FIRST_NAME": "Anika",
        "COUPON_CODE": "TEST20-XYZ",
        "CUSTOMER_ID": "CUST-99999",
    }
    rendered = render_template(raw, data)

    for key, value in data.items():
        assert value in rendered, f"Value '{value}' for {key} not found in rendered output"
        assert "{{" + key + "}}" not in rendered, f"Placeholder {{{{{key}}}}} was not replaced"


# ── Test: HTML escaping ─────────────────────────────────────────────────────

def test_html_escaping():
    raw = load_template()
    # Attempt XSS via first name
    malicious_name = '<script>alert("xss")</script>'
    data = {
        "FIRST_NAME": malicious_name,
        "COUPON_CODE": "SAFE20",
        "CUSTOMER_ID": "CUST-00001",
    }
    rendered = render_template(raw, data)
    assert malicious_name not in rendered, "Raw script tag should not appear in rendered output"
    assert "&lt;script&gt;" in rendered, "Script tag should be HTML-escaped"


# ── Test: Missing data fallback ─────────────────────────────────────────────

def test_missing_data_fallback():
    raw = load_template()
    # Only provide FIRST_NAME, omit others
    data = {"FIRST_NAME": "Test"}
    rendered = render_template(raw, data)

    # Remaining placeholders should be replaced with safe fallback like [COUPON_CODE]
    assert "{{COUPON_CODE}}" not in rendered, "Raw placeholder should not remain"
    assert "[COUPON_CODE]" in rendered, "Missing placeholder should show safe fallback"


# ── Test: Structural elements in rendered HTML ──────────────────────────────

def test_structural_elements():
    raw = load_template()
    data = {
        "FIRST_NAME": "Ravi",
        "COUPON_CODE": "AUTUMN20-VLR",
        "CUSTOMER_ID": "CUST-10042",
    }
    rendered = render_template(raw, data)

    # DOCTYPE
    assert "<!DOCTYPE html>" in rendered, "Missing DOCTYPE"

    # lang attribute for accessibility
    assert 'lang="en"' in rendered, "Missing lang attribute"

    # role="presentation" on layout tables
    assert 'role="presentation"' in rendered, "Layout tables should have role=presentation"

    # Preheader text
    assert "display: none" in rendered or "display:none" in rendered, "Should have hidden preheader"

    # Unsubscribe link
    assert "unsubscribe" in rendered.lower(), "Must include unsubscribe link"

    # CTA link
    assert "utm_campaign" in rendered, "CTA should have UTM tracking parameters"

    # Footer company info
    assert "Velora Ltd" in rendered, "Footer should contain company name"

    # Offer expiry date
    assert "31 October 2026" in rendered, "Should include explicit offer expiry date"


# ── Test: Mobile responsiveness ─────────────────────────────────────────────

def test_mobile_responsive_styles():
    raw = load_template()

    # Check for responsive media query
    assert "@media" in raw, "Should contain responsive media queries"
    assert "max-width" in raw, "Should use max-width media query for mobile"

    # Check for mobile-specific classes
    assert "mobile-padding" in raw, "Should have mobile padding class"
    assert "stack-column" in raw, "Should have stacking column class for mobile"


# ── Test: Outlook-specific VML button ───────────────────────────────────────

def test_outlook_vml_button():
    raw = load_template()
    assert "v:roundrect" in raw, "Should include VML roundrect for Outlook"
    assert "[if mso]" in raw, "Should have MSO conditional comment"


# ── Run all tests ───────────────────────────────────────────────────────────

def run_tests():
    """Simple test runner — no pytest dependency required."""
    test_functions = [
        test_template_exists,
        test_placeholders_present,
        test_rendering_replaces_placeholders,
        test_html_escaping,
        test_missing_data_fallback,
        test_structural_elements,
        test_mobile_responsive_styles,
        test_outlook_vml_button,
    ]

    passed = 0
    failed = 0
    errors = []

    for test_fn in test_functions:
        name = test_fn.__name__
        try:
            test_fn()
            passed += 1
            print(f"  ✓ {name}")
        except AssertionError as e:
            failed += 1
            errors.append((name, str(e)))
            print(f"  ✗ {name}: {e}")
        except Exception as e:
            failed += 1
            errors.append((name, f"Unexpected error: {e}"))
            print(f"  ✗ {name}: Unexpected error: {e}")

    print(f"\n{'─' * 50}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")

    if errors:
        print("\nFailures:")
        for name, msg in errors:
            print(f"  • {name}: {msg}")
        sys.exit(1)
    else:
        print("\nAll tests passed! ✓")
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
