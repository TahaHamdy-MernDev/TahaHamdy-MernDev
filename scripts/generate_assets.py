#!/usr/bin/env python3
"""
Generates dual-theme (dark & light) flat, minimalist Bento Grid SVG assets
for the GitHub Profile README, embedding downloaded SVG brand icons from assets/icons/.
Run: python3 scripts/generate_assets.py
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ICONS_DIR = ASSETS / "icons"
ASSETS.mkdir(parents=True, exist_ok=True)

FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"

THEMES = {
    "dark": {
        "card": "#161b22",
        "border": "#30363d",
        "divider": "#21262d",
        "text": "#e6edf3",
        "subtext": "#8b949e",
        "muted": "#6e7681",
        "pill_bg": "#0d1117",
        "pill_border": "#30363d",
        "pill_text": "#c9d1d9",
        "icon_box_bg": "#21262d",
        "icon_box_border": "#30363d",
        "icon_stroke": "#c9d1d9",
        "mono_icon": "#e6edf3",
        "drizzle_icon": "#c5f74f",
    },
    "light": {
        "card": "#f6f8fa",
        "border": "#d0d7de",
        "divider": "#d8dee4",
        "text": "#1f2328",
        "subtext": "#57606a",
        "muted": "#6e7781",
        "pill_bg": "#ffffff",
        "pill_border": "#d0d7de",
        "pill_text": "#24292f",
        "icon_box_bg": "#ffffff",
        "icon_box_border": "#d0d7de",
        "icon_stroke": "#57606a",
        "mono_icon": "#1f2328",
        "drizzle_icon": "#65a30d",
    },
}

# Clean Lucide-style 24x24 stroke icons
UI_ICONS = {
    "layout": (
        '<rect x="3" y="3" width="18" height="18" rx="2" />'
        '<line x1="3" y1="9" x2="21" y2="9" />'
        '<line x1="9" y1="21" x2="9" y2="9" />'
    ),
    "server": (
        '<rect x="2" y="3" width="20" height="8" rx="2" />'
        '<rect x="2" y="13" width="20" height="8" rx="2" />'
        '<line x1="6" y1="7" x2="6.01" y2="7" />'
        '<line x1="6" y1="17" x2="6.01" y2="17" />'
    ),
    "database": (
        '<ellipse cx="12" cy="5" rx="9" ry="3" />'
        '<path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5" />'
        '<path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3" />'
    ),
    "cloud": (
        '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" />'
    ),
    "webhook": (
        '<path d="M18 16.98h-5.99c-1.1 0-1.95.94-2.48 1.9A4 4 0 0 1 2 17c.01-.7.2-1.4.57-2" />'
        '<path d="m6 17 3.13-5.78c.53-.97.1-2.18-.5-3.1a4 4 0 1 1 6.89-4.06" />'
        '<path d="m12 6 3.13 5.73C15.66 12.7 16.9 13 18 13a4 4 0 0 1 0 8" />'
    ),
    "shield": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />'
        '<path d="m9 12 2 2 4-4" />'
    ),
    "zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />'
    ),
    "refresh": (
        '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />'
        '<path d="M21 3v5h-5" />'
        '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />'
        '<path d="M8 16H3v5" />'
    ),
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2" />'
        '<polyline points="2 12 12 17 22 12" />'
        '<polyline points="2 17 12 22 22 17" />'
    ),
    "terminal": (
        '<polyline points="4 17 10 11 4 5" />'
        '<line x1="12" y1="19" x2="20" y2="19" />'
    ),
    "pin": (
        '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />'
        '<circle cx="12" cy="10" r="3" />'
    ),
    "box": (
        '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z" />'
        '<path d="m3.3 7 8.7 5 8.7-5" />'
        '<path d="M12 22V12" />'
    ),
}

MONOCHROME_ICONS = {"shadcnui", "express", "fastify", "vercel"}


def ui_icon_svg(name: str, x: float, y: float, size: int, color: str, stroke_width: float = 1.8) -> str:
    body = UI_ICONS[name]
    return (
        f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    )


def embed_brand_icon(icon_name: str, x: float, y: float, size: int, mode: str, uid: str) -> str:
    """Inlines a downloaded SVG icon from assets/icons/ as a nested <svg> with scoped IDs."""
    t = THEMES[mode]
    if icon_name == "webhook":
        return ui_icon_svg("webhook", x, y, size, t["icon_stroke"], stroke_width=1.8)

    svg_path = ICONS_DIR / f"{icon_name}.svg"
    raw = svg_path.read_text(encoding="utf-8").strip()

    raw = re.sub(r"<\?xml[^>]*\?>", "", raw)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"<title>.*?</title>", "", raw, flags=re.S)

    vb_match = re.search(r'viewBox="([^"]+)"', raw)
    view_box = vb_match.group(1) if vb_match else "0 0 128 128"
    inner_match = re.search(r"<svg[^>]*>(.*)</svg>", raw, flags=re.S)
    inner = inner_match.group(1).strip() if inner_match else ""

    prefix = f"ic_{uid}_{mode}_"
    ids = set(re.findall(r'\bid="([^"]+)"', inner))
    for old_id in ids:
        new_id = prefix + old_id
        inner = inner.replace(f'id="{old_id}"', f'id="{new_id}"')
        inner = inner.replace(f"url(#{old_id})", f"url(#{new_id})")
        inner = inner.replace(f'href="#{old_id}"', f'href="#{new_id}"')

    fill_attr = ""
    if icon_name in MONOCHROME_ICONS:
        fill_attr = f' fill="{t["mono_icon"]}"'
    elif icon_name == "drizzle":
        fill_attr = f' fill="{t["drizzle_icon"]}"'
    elif icon_name == "prisma":
        fill_attr = f' fill="{t["mono_icon"]}"'
    elif icon_name == "typeorm":
        fill_attr = ' fill="#fe0803"'

    backdrop = ""
    if icon_name == "nextjs" and mode == "dark":
        cx = x + size / 2
        cy = y + size / 2
        backdrop = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size / 2 - 0.5:.1f}" fill="#ffffff" />'

    return (
        f'{backdrop}<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" '
        f'viewBox="{view_box}"{fill_attr}>{inner}</svg>'
    )


def build_hero_bento(mode: str) -> str:
    t = THEMES[mode]
    pin_ic = ui_icon_svg("pin", 612, 66, 14, t["subtext"], 1.7)
    layers_ic = ui_icon_svg("layers", 612, 118, 14, t["subtext"], 1.7)
    box_ic = ui_icon_svg("box", 612, 170, 14, t["subtext"], 1.7)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="224" viewBox="0 0 900 224" fill="none">
  <!-- Left Flat Main Card -->
  <rect x="0.5" y="0.5" width="567" height="223" rx="14" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />

  <text x="36" y="64" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="34" font-weight="700" letter-spacing="-0.7">Taha Hamdy</text>
  <text x="36" y="94" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="15" font-weight="500">Mid-Level Full-Stack Software Engineer</text>

  <text x="36" y="132" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="13.5">Building scalable SaaS platforms, modular NestJS APIs,</text>
  <text x="36" y="153" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="13.5">and responsive Next.js dashboards with end-to-end TypeScript.</text>

  <line x1="36" y1="178" x2="532" y2="178" stroke="{t["divider"]}" stroke-width="1" />
  <text x="36" y="201" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11.5">TypeScript  ·  Next.js  ·  NestJS  ·  PostgreSQL  ·  Prisma  ·  Drizzle</text>

  <!-- Right Flat Snapshot Card -->
  <rect x="586.5" y="0.5" width="313" height="223" rx="14" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />
  <text x="612" y="34" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10.5" font-weight="600" letter-spacing="1.2">SNAPSHOT</text>
  <line x1="612" y1="48" x2="874" y2="48" stroke="{t["divider"]}" stroke-width="1" />

  {pin_ic}
  <text x="634" y="77" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10">LOCATION</text>
  <text x="634" y="96" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Cairo, Egypt (UTC+2)</text>

  {layers_ic}
  <text x="634" y="129" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10">FOCUS</text>
  <text x="634" y="148" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Multi-Tenant SaaS &amp; Commerce</text>

  {box_ic}
  <text x="634" y="181" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10">BUILDING</text>
  <text x="634" y="200" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Web Platforms &amp; Dev Tooling</text>
</svg>
'''


def render_icon_pill_rows(
    rows: list[list[tuple[str, str]]],
    card_x: int,
    y_start: int,
    mode: str,
    quad_idx: int,
) -> str:
    """Renders spacious balanced rows of flat pills with embedded SVG brand icons."""
    t = THEMES[mode]
    out = []
    max_right = card_x + 418
    for row_idx, row in enumerate(rows):
        x = card_x + 24
        y = y_start + row_idx * 42
        for col_idx, (icon_key, label) in enumerate(row):
            w = max(72, int(42 + len(label) * 6.7))
            assert x + w <= max_right, f"Pill '{label}' overflows card ({x + w} > {max_right})"
            uid = f"q{quad_idx}r{row_idx}c{col_idx}"
            icon_svg = embed_brand_icon(icon_key, x + 10, y + 7, 16, mode, uid)
            out.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="8" '
                f'fill="{t["pill_bg"]}" stroke="{t["pill_border"]}" stroke-width="1" />\n'
                f'  {icon_svg}\n'
                f'  <text x="{x + 32}" y="{y + 19}" fill="{t["pill_text"]}" '
                f'font-family="{FONT_SANS}" font-size="11.5" font-weight="500">{escape(label)}</text>'
            )
            x += w + 8
    return "\n  ".join(out)


def build_stack_bento(mode: str) -> str:
    t = THEMES[mode]
    quads = [
        (
            0,
            0,
            "layout",
            "FRONTEND & UI",
            [
                [("typescript", "TypeScript"), ("nextjs", "Next.js"), ("react", "React")],
                [("tailwindcss", "Tailwind"), ("shadcnui", "Shadcn UI"), ("materialui", "Material UI")],
            ],
        ),
        (
            460,
            0,
            "server",
            "BACKEND & APIS",
            [
                [("nestjs", "NestJS"), ("nodejs", "Node.js"), ("express", "Express")],
                [("fastify", "Fastify"), ("graphql", "GraphQL"), ("webhook", "Webhooks")],
            ],
        ),
        (
            0,
            174,
            "database",
            "DATABASES & ORMS",
            [
                [("postgresql", "PostgreSQL"), ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("redis", "Redis")],
                [("prisma", "Prisma"), ("drizzle", "Drizzle ORM"), ("typeorm", "TypeORM")],
            ],
        ),
        (
            460,
            174,
            "cloud",
            "DEVOPS & DELIVERY",
            [
                [("docker", "Docker"), ("nginx", "Nginx"), ("githubactions", "Actions")],
                [("vercel", "Vercel"), ("digitalocean", "DigitalOcean"), ("git", "Git")],
            ],
        ),
    ]

    blocks = []
    for idx, (x, y, cat_icon, title, rows) in enumerate(quads):
        cat_svg = ui_icon_svg(cat_icon, x + 29, y + 25, 14, t["icon_stroke"], 1.8)
        pills = render_icon_pill_rows(rows, x, y + 66, mode, idx)
        blocks.append(
            f'<rect x="{x + 0.5}" y="{y + 0.5}" width="439" height="155" rx="14" '
            f'fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />\n'
            f'  <rect x="{x + 24}" y="{y + 20}" width="24" height="24" rx="6" '
            f'fill="{t["icon_box_bg"]}" stroke="{t["icon_box_border"]}" stroke-width="1" />\n'
            f'  {cat_svg}\n'
            f'  <text x="{x + 58}" y="{y + 36}" fill="{t["text"]}" font-family="{FONT_MONO}" '
            f'font-size="11" font-weight="600" letter-spacing="0.9">{escape(title)}</text>\n'
            f'  <line x1="{x + 24}" y1="{y + 53}" x2="{x + 416}" y2="{y + 53}" stroke="{t["divider"]}" stroke-width="1" />\n'
            f'  {pills}'
        )
    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="330" viewBox="0 0 900 330" fill="none">
  {inner}
</svg>
'''


def build_principles_bento(mode: str) -> str:
    t = THEMES[mode]
    cards = [
        (
            0,
            0,
            "shield",
            "Strict Type Safety & Contracts",
            "End-to-end TypeScript sharing with Zod and class-validator",
            "enforces runtime validation and clean API contracts.",
        ),
        (
            460,
            0,
            "zap",
            "Performance & Rendering",
            "Next.js Server Components, streaming SSR, and smart caching",
            "keep client bundles lean and Core Web Vitals fast.",
        ),
        (
            0,
            132,
            "refresh",
            "Resilient Business Workflows",
            "Idempotent webhook handlers, atomic DB transactions, and",
            "background retry queues protect critical state mutations.",
        ),
        (
            460,
            132,
            "layers",
            "Modular Clean Architecture",
            "Clear boundaries between UI, services, and persistence keep",
            "domain logic decoupled, readable, testable, and extensible.",
        ),
        (
            0,
            264,
            "database",
            "Database & Query Efficiency",
            "Normalized schemas, strategic indexing, safe Prisma/Drizzle",
            "migrations, and query profiling prevent N+1 bottlenecks.",
        ),
        (
            460,
            264,
            "terminal",
            "Observability & Automated Delivery",
            "Structured logging, predictable error contracts, Dockerized",
            "builds, and GitHub Actions CI/CD ensure confident releases.",
        ),
    ]

    blocks = []
    for x, y, icon_name, title, l1, l2 in cards:
        ic = ui_icon_svg(icon_name, x + 30, y + 26, 16, t["icon_stroke"], 1.8)
        blocks.append(
            f'<rect x="{x + 0.5}" y="{y + 0.5}" width="439" height="113" rx="14" '
            f'fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />\n'
            f'  <rect x="{x + 24}" y="{y + 20}" width="28" height="28" rx="8" '
            f'fill="{t["icon_box_bg"]}" stroke="{t["icon_box_border"]}" stroke-width="1" />\n'
            f'  {ic}\n'
            f'  <text x="{x + 64}" y="{y + 39}" fill="{t["text"]}" font-family="{FONT_SANS}" '
            f'font-size="14.5" font-weight="600">{escape(title)}</text>\n'
            f'  <text x="{x + 24}" y="{y + 70}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(l1)}</text>\n'
            f'  <text x="{x + 24}" y="{y + 90}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(l2)}</text>'
        )
    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="378" viewBox="0 0 900 378" fill="none">
  {inner}
</svg>
'''


def main() -> None:
    for mode in ("dark", "light"):
        (ASSETS / f"bento-hero-{mode}.svg").write_text(build_hero_bento(mode), encoding="utf-8")
        (ASSETS / f"bento-stack-{mode}.svg").write_text(build_stack_bento(mode), encoding="utf-8")
        (ASSETS / f"bento-principles-{mode}.svg").write_text(build_principles_bento(mode), encoding="utf-8")

    print(f"Generated {len(list(ASSETS.glob('bento-*.svg')))} flat minimalist Bento SVGs.")


if __name__ == "__main__":
    main()
