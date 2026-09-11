# gov-ai-navigator

Static single-page React (Babel-in-browser) app for [govai.averoadvisors.com](https://govai.averoadvisors.com/).

The September 2026 report is **email-only**. After the HubSpot form (portal `24211389`, form `172f7965-64e6-448f-b7c9-090efd3722e6`), the site thanks the visitor and does **not** link to a PDF. Do not put a `.pdf` in this repo: DigitalOcean publishes the tree as the site root, so a tracked file at `public/…pdf` is a public download.

## Rebuild the PDF for HubSpot (not for the site)

```bash
python3 scripts/build_navigator_pdf.py
```

Writes `artifacts/Avero_Start-at-Zero_Government-AI-Navigator_Sep2026.pdf` (gitignored). Upload that file in HubSpot Files; the site never serves it.
