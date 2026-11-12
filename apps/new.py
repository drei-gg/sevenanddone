#!/usr/bin/env python3
"""Stamp out an app's pages from apps/_template: the landing page, privacy and terms.

    python3 apps/new.py qr --name "QR" --store "7&D QR Code Kit" \
        --what "Read and make QR codes. Warns you about scams, for free."

This fills the mechanical bits ({{SLUG}}, {{STORE_NAME}} and so on). The per-app copy is
left as visible [bracketed] placeholders with class="todo"; write those by hand.
`python3 apps/new.py --check` lists every placeholder still left in a stamped app.
Run once per app. It never overwrites: the stamped pages are hand-edited from then on.
"""
import argparse, datetime, html, pathlib, re, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "apps" / "_template"
PAGES = ["index.html", "privacy/index.html", "terms/index.html"]


def check():
    left = 0
    for app in sorted(p for p in (ROOT / "apps").iterdir() if p.is_dir() and p.name != "_template"):
        for page in PAGES:
            f = app / page
            if not f.exists():
                print(f"{app.name}/{page}: missing"); left += 1; continue
            for n, line in enumerate(f.read_text().splitlines(), 1):
                if 'class="todo' in line or "{{" in line:
                    print(f"{app.name}/{page}:{n}: {line.strip()[:100]}"); left += 1
    print("no placeholders left" if not left else f"{left} placeholder line(s) left")
    return 1 if left else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?", help="permanent lowercase slug, e.g. qr (matches brand/apps/<slug>/icon.svg)")
    ap.add_argument("--check", action="store_true", help="list placeholders left in stamped apps")
    ap.add_argument("--name", help='short name shown big, e.g. "QR"')
    ap.add_argument("--store", help='App Store name, e.g. "7&D QR Code Kit"')
    ap.add_argument("--what", help="one sentence: what it does")
    ap.add_argument("--status", default="Building", help="Vetting, Building, Testing or Out now")
    ap.add_argument("--email", default="support@sevenanddone.app")
    ap.add_argument("--platform", default="iPhone · iOS 17 or later · Android later")
    ap.add_argument("--updated", default=datetime.date.today().strftime("%-d %B %Y"))
    a = ap.parse_args()

    if a.check:
        sys.exit(check())
    missing = [k for k in ("slug", "name", "store", "what") if not getattr(a, k)]
    if missing:
        ap.error("needs " + ", ".join("--" + m if m != "slug" else "slug" for m in missing))
    if not re.fullmatch(r"[a-z][a-z0-9-]*", a.slug):
        ap.error("slug must be lowercase letters, digits and dashes")

    dest = ROOT / "apps" / a.slug
    if dest.exists():
        sys.exit(f"apps/{a.slug} already exists; edit it by hand")
    icon = ROOT / "brand" / "apps" / a.slug / "icon.svg"
    if not icon.exists():
        print(f"warning: no icon at {icon.relative_to(ROOT)} yet; the pages point there", file=sys.stderr)

    e = lambda s: html.escape(s, quote=True)
    tokens = {
        "SLUG": a.slug, "NAME": e(a.name), "STORE_NAME": e(a.store), "PLATFORM": e(a.platform),
        "WHAT": e(a.what), "STATUS": e(a.status), "EMAIL": e(a.email),
        "SUBJECT": urllib.parse.quote(f"{a.store} support"),
        "UPDATED": e(a.updated),
    }
    for page in PAGES:
        text = (TEMPLATE / page).read_text()
        text = "".join(l for l in text.splitlines(True) if "<!--@TEMPLATE-ONLY-->" not in l)
        text = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: tokens[m.group(1)], text)
        out = dest / page
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(out.relative_to(ROOT))
    print(f"now write the [bracketed] copy; `python3 apps/new.py --check` lists what's left")


if __name__ == "__main__":
    main()
