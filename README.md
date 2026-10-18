# SmartPromo-Behaviour-Aware-Email-Campaign-Engine

<img width="1918" height="1169" alt="image" src="https://github.com/user-attachments/assets/28176e29-7c69-435a-85ef-8bb6afb8cca8" />
<img width="1918" height="1169" alt="image" src="https://github.com/user-attachments/assets/53203bf4-f4da-4e4d-b8dc-1d4006fa9ef6" />



A portfolio project demonstrating how customer purchase history, inactivity, and product preferences can drive more relevant email campaigns for a fictional online retail brand.

> **⚠️ This project uses synthetic data only. No real customer data is used and no emails are sent to real recipients.**

## Brand

**Velora** — a fictional UK-based online lifestyle and home goods retailer specialising in curated textiles, tableware, and seasonal collections.

---

## Project Structure

```
SmartPromo/
├── templates/
│   └── promo-email.html    # Production-ready promotional email template
├── tests/
│   └── test_template.py    # Automated template tests
├── preview.py              # Render & preview the email locally
└── README.md               # This file
```

## Quick Start

### Prerequisites

- Python 3.10+ (no external packages required for Step 1)

### Preview the Email

```bash
# Render with sample data and open in your default browser
python3 preview.py

# Or write to a specific file
python3 preview.py --out my_preview.html

# Override personalisation values
python3 preview.py --data FIRST_NAME=Alex COUPON_CODE=SAVE10
```

### Run Tests

```bash
python3 tests/test_template.py
```

---

## Step 1 — Email Foundation

### Design Decisions

| Decision | Rationale |
|---|---|
| **Table-based layout** | `<div>` layouts break in Outlook and many webmail clients. Tables remain the only reliable cross-client approach. |
| **Inline CSS** | Most email clients strip `<style>` blocks. Critical styles are inlined; the `<style>` block provides progressive enhancement for clients that support it (Apple Mail, iOS Mail). |
| **Text-based logo** | Avoids image-blocking issues. Renders reliably even with images disabled. |
| **`role="presentation"`** | Layout tables should not be announced as data tables by screen readers. |
| **VML button for Outlook** | Outlook on Windows does not support CSS `border-radius` on `<a>` tags. VML `<v:roundrect>` provides a rendered button. |
| **Emoji icons** | Used instead of images for category cards — avoids external image dependencies and renders in all modern email clients. |
| **600px max-width** | Industry standard for email width. Works in all major clients and adapts via media queries on mobile. |
| **Georgia + Arial stack** | System fonts ensure consistent rendering without `@font-face` (which most email clients ignore). Georgia adds editorial warmth; Arial is the sans-serif fallback. |
| **Preheader text** | Hidden text that appears in inbox preview alongside the subject line. Critical for open rates. |
| **UTM parameters on CTA** | Enables Google Analytics tracking without any JavaScript dependency. |

### Personalisation Placeholders

| Placeholder | Description | Example |
|---|---|---|
| `{{FIRST_NAME}}` | Customer's first name | Priya |
| `{{COUPON_CODE}}` | Unique or segment-specific discount code | AUTUMN20-VLR |
| `{{CUSTOMER_ID}}` | Customer ID used in unsubscribe/preference links | CUST-10042 |

### Accessibility

- Semantic heading hierarchy (`<h1>` for brand, `<h2>` for hero, `<h3>` for sections)
- `role="presentation"` on all layout tables
- `lang="en"` on the root `<html>` element
- `aria-label` on the CTA button
- Adequate colour contrast (dark text on light backgrounds, light text on dark footer)
- Underlined links for visibility beyond colour alone

### Mobile Responsiveness

The template uses a `@media` query at 620px to:
- Stack two-column layouts vertically
- Add horizontal padding for thumb-friendly tap targets
- Scale heading and coupon-code font sizes
- Make the CTA button full-width

### Email Client Compatibility Notes

A local browser preview validates HTML structure and visual layout but **cannot** guarantee rendering in production email clients. Key differences include:

- **Gmail** strips `<style>` blocks and ignores media queries in many configurations
- **Outlook (Windows)** uses the Word rendering engine, not a browser engine
- **Yahoo Mail** may rewrite class names and inline certain styles
- **Apple Mail / iOS** offers the best CSS support of any email client

For production use, the template should be tested with a service such as Litmus or Email on Acid. This project uses inline CSS as the primary styling strategy to maximise compatibility.

---

## Limitations

- This is a portfolio demonstration, not a production email platform.
- No emails are actually sent. The template is rendered to static HTML for local preview.
- Personalisation uses simple string replacement; a production system would use a templating engine with auto-escaping.
- Image-free design avoids external dependencies but limits visual richness.

---

## Roadmap

- [ ] **Step 2** — Synthetic customer dataset (CSV)
- [ ] **Step 3** — Segmentation engine (Python + SQL)
- [ ] **Step 4** — Personalised email variant generation
- [ ] **Step 5** — QA checklist and A/B testing plan
- [ ] **Step 6** — Documentation and portfolio polish

---

## License

This project is for educational and portfolio purposes. The brand "Velora" is entirely fictional.

