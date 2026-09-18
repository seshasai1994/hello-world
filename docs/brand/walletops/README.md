# walletops.io brand kit

Logo marks and favicon packs for **walletops.io** (Unstoppable domain) and the four product lines:

| Product | Colour | Recommended mark | Drop-in folder |
|---|---|---|---|
| WalletOps | indigo `#4F46E5` | W Monogram | `recommended/core/` |
| WalletOps Analytics | cyan `#0284C7` | W Bar Chart | `recommended/analytics/` |
| Wallet Shield | green `#059669` | Shield Check | `recommended/shield/` |
| Wallet Intelligence | violet `#7C3AED` | Neural W | `recommended/intelligence/` |
| Wallet Specialist | orange `#EA580C` | Certified Seal | `recommended/specialist/` |

**100 unique marks × 4 styles = 400 logo SVGs**, plus a favicon pack for every mark.

## Quick start (website favicon)

1. Copy every file in `recommended/core/` (or the matching product folder) to the website root.
2. Paste this into `<head>`:

```html
<!-- WalletOps favicon pack -->
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#4F46E5">
```

Change `theme-color` to the product primary when you switch folders.

## What's in a favicon pack

Each `favicons/<slug>/` folder contains:

- `favicon.svg` — sharp at any size
- `favicon.ico` — 16 / 32 / 48 (legacy browsers)
- `favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`
- `apple-touch-icon.png` — 180×180
- `android-chrome-192x192.png`, `android-chrome-512x512.png`
- `site.webmanifest`
- `embed.html` — the snippet above

## Four styles per mark

- **solid** — flat primary, white counters, transparent background
- **gradient** — primary → secondary
- **outline** — stroke-only, for print and watermarks
- **tile** — white glyph on a rounded gradient app-icon (this is what the favicon pack uses)

Browse them all in `index.html`.

## Recommended heroes

- **WalletOps** — `core-w-monogram` → drop-in pack `recommended/core/`
- **WalletOps Analytics** — `analytics-w-bars` → drop-in pack `recommended/analytics/`
- **Wallet Shield** — `shield-check` → drop-in pack `recommended/shield/`
- **Wallet Intelligence** — `intel-neural-w` → drop-in pack `recommended/intelligence/`
- **Wallet Specialist** — `spec-seal` → drop-in pack `recommended/specialist/`

## Regenerate

```bash
python3 docs/brand/walletops/generate.py
```

Requires `cairosvg` and `pillow` only if you want PNG/ICO/contact sheets. SVG output needs nothing.

## Layout

```
docs/brand/walletops/
  generate.py          source of truth — edit marks here
  index.html           visual gallery
  README.md            this file
  logos/<line>/        <slug>--{solid,gradient,outline,tile}.svg
  favicons/<slug>/     full favicon pack
  recommended/<line>/  copy-paste pack for each product site
  lockups/             wordmark + mark, light and dark
  preview/             contact sheets
  manifest.json        machine-readable index
```
