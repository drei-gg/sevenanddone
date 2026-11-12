# $7&D — Seven and Done

Simple apps, paid for once.

Somewhere right now, someone is paying $7.99 a week to delete duplicate photos from their own phone. We think that's absurd. So here's the deal:

- **7 apps** to start, each replacing something that charges you rent.
- **7 engineering days** each, give or take. A measure of effort, not a stopwatch.
- **7-day trial** from the moment you install. No sign-up, no card, no charge you didn't choose.
- **$7, once.** €7 or £7 where that's worth more; less where $7 is a lot of money.
- **7 months**: every app gets at least one update every seven months. Critical fixes ship when they're found.

The full manifesto, fine print included: **[sevenanddone.app](https://sevenanddone.app)**

## This repo

The site: a home page, the manifesto and one stylesheet, with no build step and no cookies. The one script, `theme.js`, remembers the Auto/Light/Dark pick in the browser's local storage so it carries from page to page; nothing leaves the device. The brand faces (Barlow Condensed Black, Noto Sans, Noto Sans Mono, all OFL) are served from this site's own `brand/fonts`, so your browser never calls anyone else. A brand that promises no tracking shouldn't make your browser call anyone on its first page.

`brand/` is the visual identity: the outlined marks, the type and colour tokens, and a specimen page at `/brand/`.

```sh
python3 -m http.server 8777   # then open http://localhost:8777
```

It's served from DigitalOcean App Platform as a static site; every push to `main` deploys.

## App pages

Each app gets `/apps/<slug>/` (landing, Before you buy, free vs $7, support), plus `privacy/` and `terms/` for the store listings. They're stamped once from `apps/_template` and hand-edited from then on:

```sh
python3 apps/new.py qr --name "QR" --store "7&D QR Code Kit" --what "Read and make QR codes. Warns you about scams, for free."
python3 apps/new.py --check   # lists the [bracketed] copy still to write
```

The icon comes from `brand/apps/<slug>/icon.svg`.

## License

Copyright © 2026 Drei Guintu. The code is free software under the [GNU GPL v3](LICENSE): if you can build it, it's yours. We sell the app built, signed and kept up to date.

The GPL covers the code, not the name or the icons. "Seven and Done", "$7&D" and the 7 icon are ours.

A [drei.gg](https://drei.gg) project. Thought of on 9 November 2026.
