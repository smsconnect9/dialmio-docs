# Dialmio Help Center

Static help documentation for the Dialmio dialer & call-management CRM. Clean folder URLs (`/getting-started/`, `/whatsapp/`, …), built-in search, mobile friendly. No framework needed.

## Edit content
1. Change the text in `tools/build.py` (each `page(...)` block is one article).
2. Run `python3 tools/build.py` — it regenerates every `docs/*/index.html`, the home page and `assets/search-index.js`.
3. Commit and push.

Page videos live in `docs/assets/video/` (mp4 + jpg poster) and are listed in `VIDEOS` in `tools/build.py`.

## Publish (GitHub Pages)
Settings → Pages → Source: **Deploy from a branch** → `main` / `/docs`. The site lives in the `docs/` folder.
For a custom domain such as `help.dialmio.com`, add it under Settings → Pages → Custom domain and create a DNS `CNAME` record `help` → `smsconnect9.github.io`.
