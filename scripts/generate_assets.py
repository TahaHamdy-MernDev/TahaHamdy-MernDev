#!/usr/bin/env python3
"""
Generates dual-theme (dark & light) Bento Grid SVG assets for the GitHub Profile README,
embedding real downloaded SVG brand icons from assets/icons/ and crisp UI vector icons.
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
        "canvas": "#0d1117",
        "card": "#161b22",
        "border": "#30363d",
        "divider": "#21262d",
        "text": "#f0f6fc",
        "subtext": "#8b949e",
        "muted": "#6e7681",
        "pill_bg": "#1c2128",
        "pill_border": "#30363d",
        "pill_text": "#e6edf3",
        "accent": "#818cf8",
        "status_bg": "#064e3b",
        "status_bg_op": "0.4",
        "status_border": "#10b981",
        "status_dot": "#34d399",
        "status_text": "#6ee7b7",
        "grid_stroke": "#30363d",
        "grid_op": "0.35",
        "glow": "#6366f1",
        "glow_op": "0.18",
        "link": "#58a6ff",
        "mono_icon": "#f0f6fc",
        "drizzle_icon": "#c5f74f",
        "cat_fe": "#38bdf8",
        "cat_be": "#fb7185",
        "cat_db": "#34d399",
        "cat_ops": "#a78bfa",
        "cat_perf": "#f59e0b",
        "cat_obs": "#22d3ee",
    },
    "light": {
        "canvas": "#ffffff",
        "card": "#f6f8fa",
        "border": "#d0d7de",
        "divider": "#d8dee4",
        "text": "#1f2328",
        "subtext": "#57606a",
        "muted": "#6e7781",
        "pill_bg": "#ffffff",
        "pill_border": "#d0d7de",
        "pill_text": "#1f2328",
        "accent": "#4f46e5",
        "status_bg": "#ecfdf5",
        "status_bg_op": "1",
        "status_border": "#10b981",
        "status_dot": "#10b981",
        "status_text": "#047857",
        "grid_stroke": "#d0d7de",
        "grid_op": "0.55",
        "glow": "#6366f1",
        "glow_op": "0.10",
        "link": "#0969da",
        "mono_icon": "#1f2328",
        "drizzle_icon": "#65a30d",
        "cat_fe": "#0284c7",
        "cat_be": "#e11d48",
        "cat_db": "#059669",
        "cat_ops": "#7c3aed",
        "cat_perf": "#d97706",
        "cat_obs": "#0891b2",
    },
}

# Clean Lucide-style 24x24 stroke icons for categories, snapshot, and principles
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
    "code": (
        '<polyline points="16 18 22 12 16 6" />'
        '<polyline points="8 6 2 12 8 18" />'
    ),
    "box": (
        '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z" />'
        '<path d="m3.3 7 8.7 5 8.7-5" />'
        '<path d="M12 22V12" />'
    ),
}

MONOCHROME_ICONS = {"shadcnui", "express", "fastify", "vercel"}


def ui_icon_svg(name: str, x: float, y: float, size: int, color: str, stroke_width: float = 2.0) -> str:
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
        return ui_icon_svg("webhook", x, y, size, t["cat_be"], stroke_width=2.0)

    svg_path = ICONS_DIR / f"{icon_name}.svg"
    raw = svg_path.read_text(encoding="utf-8").strip()

    # Strip XML declaration / comments / title tags
    raw = re.sub(r"<\?xml[^>]*\?>", "", raw)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"<title>.*?</title>", "", raw, flags=re.S)

    # Extract viewBox and inner markup
    vb_match = re.search(r'viewBox="([^"]+)"', raw)
    view_box = vb_match.group(1) if vb_match else "0 0 128 128"
    inner_match = re.search(r"<svg[^>]*>(.*)</svg>", raw, flags=re.S)
    inner = inner_match.group(1).strip() if inner_match else ""

    # Scope internal IDs so multiple icons in one SVG never collide
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
        fill_attr = ' fill="#5a67d8"'
    elif icon_name == "typeorm":
        fill_attr = ' fill="#fe0803"'

    # Add a subtle white disc behind Next.js icon in dark mode so its black ring stays crisp
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
    pin_ic = ui_icon_svg("pin", 608, 72, 14, t["cat_fe"], 1.8)
    layers_ic = ui_icon_svg("layers", 608, 120, 14, t["cat_be"], 1.8)
    box_ic = ui_icon_svg("box", 608, 168, 14, t["cat_db"], 1.8)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="240" viewBox="0 0 900 240" fill="none">
  <defs>
    <radialGradient id="glow-{mode}" cx="90%" cy="10%" r="75%">
      <stop offset="0%" stop-color="{t["glow"]}" stop-opacity="{t["glow_op"]}" />
      <stop offset="100%" stop-color="{t["glow"]}" stop-opacity="0" />
    </radialGradient>
    <pattern id="grid-{mode}" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{t["grid_stroke"]}" stroke-width="0.6" stroke-opacity="{t["grid_op"]}" />
    </pattern>
    <clipPath id="clip-left-{mode}">
      <rect x="0" y="0" width="568" height="240" rx="14" />
    </clipPath>
  </defs>

  <!-- Left Main Hero Bento Card -->
  <g clip-path="url(#clip-left-{mode})">
    <rect x="0" y="0" width="568" height="240" rx="14" fill="{t["card"]}" />
    <rect x="0" y="0" width="568" height="240" fill="url(#grid-{mode})" />
    <rect x="0" y="0" width="568" height="240" fill="url(#glow-{mode})" />
  </g>
  <rect x="0.75" y="0.75" width="566.5" height="238.5" rx="13.25" stroke="{t["border"]}" stroke-width="1.5" />

  <!-- Status Pill -->
  <rect x="30" y="28" width="258" height="26" rx="13" fill="{t["status_bg"]}" fill-opacity="{t["status_bg_op"]}" stroke="{t["status_border"]}" stroke-opacity="0.45" stroke-width="1" />
  <circle cx="46" cy="41" r="4" fill="{t["status_dot"]}" />
  <text x="58" y="45" fill="{t["status_text"]}" font-family="{FONT_SANS}" font-size="11" font-weight="600" letter-spacing="0.4">OPEN TO MID-LEVEL FULL-STACK ROLES</text>

  <!-- Name & Role -->
  <text x="30" y="102" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="36" font-weight="700" letter-spacing="-0.8">Taha Hamdy</text>
  <text x="30" y="132" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="15.5" font-weight="500">Mid-Level Full-Stack Software Engineer</text>
  <text x="30" y="160" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="13">Building scalable SaaS platforms, modular NestJS APIs, and</text>
  <text x="30" y="179" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="13">responsive Next.js dashboards with strict end-to-end TypeScript.</text>

  <!-- Bottom Tech Strip -->
  <text x="30" y="212" fill="{t["accent"]}" font-family="{FONT_MONO}" font-size="11.5" font-weight="600">TypeScript  ·  Next.js  ·  NestJS  ·  PostgreSQL  ·  Prisma  ·  Drizzle  ·  Docker</text>

  <!-- Right Snapshot Bento Card -->
  <rect x="584" y="0.75" width="315.25" height="238.5" rx="13.25" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5" />
  <text x="608" y="34" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11" font-weight="600" letter-spacing="1.2">PROFILE SNAPSHOT</text>
  <line x1="608" y1="48" x2="875" y2="48" stroke="{t["divider"]}" stroke-width="1" />

  {pin_ic}
  <text x="628" y="83" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10.5">LOCATION</text>
  <text x="628" y="101" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Cairo, Egypt (UTC+2)</text>

  {layers_ic}
  <text x="628" y="131" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10.5">SPECIALIZATION</text>
  <text x="628" y="149" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Multi-Tenant SaaS &amp; Commerce</text>

  {box_ic}
  <text x="628" y="179" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10.5">CURRENTLY SHIPPING</text>
  <text x="628" y="197" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Web Platforms &amp; VS Code Tooling</text>

  <text x="608" y="222" fill="{t["link"]}" font-family="{FONT_MONO}" font-size="11">taha-hamdy.vercel.app</text>
</svg>
'''


def render_icon_pill_rows(
    rows: list[list[tuple[str, str]]],
    card_x: int,
    y_start: int,
    mode: str,
    quad_idx: int,
) -> str:
    """Renders balanced rows of pills with real embedded SVG logos + labels."""
    t = THEMES[mode]
    out = []
    max_right = card_x + 422
    for row_idx, row in enumerate(rows):
        x = card_x + 20
        y = y_start + row_idx * 38
        for col_idx, (icon_key, label) in enumerate(row):
            # Width: left pad (9) + icon (16) + gap (7) + text + right pad (10)
            w = max(72, int(42 + len(label) * 6.8))
            assert x + w <= max_right, f"Pill '{label}' overflows card ({x + w} > {max_right})"
            uid = f"q{quad_idx}r{row_idx}c{col_idx}"
            icon_svg = embed_brand_icon(icon_key, x + 9, y + 6, 16, mode, uid)
            out.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="8" '
                f'fill="{t["pill_bg"]}" stroke="{t["pill_border"]}" stroke-width="1" />\n'
                f'  {icon_svg}\n'
                f'  <text x="{x + 31}" y="{y + 18}" fill="{t["pill_text"]}" '
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
            "cat_fe",
            [
                [("typescript", "TypeScript"), ("nextjs", "Next.js"), ("react", "React")],
                [("tailwindcss", "Tailwind"), ("shadcnui", "Shadcn UI"), ("materialui", "Material UI")],
            ],
        ),
        (
            458,
            0,
            "server",
            "BACKEND & APIS",
            "cat_be",
            [
                [("nestjs", "NestJS"), ("nodejs", "Node.js"), ("express", "Express")],
                [("fastify", "Fastify"), ("graphql", "GraphQL"), ("webhook", "Webhooks")],
            ],
        ),
        (
            0,
            154,
            "database",
            "DATABASES & ORMS",
            "cat_db",
            [
                [("postgresql", "PostgreSQL"), ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("redis", "Redis")],
                [("prisma", "Prisma"), ("drizzle", "Drizzle ORM"), ("typeorm", "TypeORM")],
            ],
        ),
        (
            458,
            154,
            "cloud",
            "DEVOPS & DELIVERY",
            "cat_ops",
            [
                [("docker", "Docker"), ("nginx", "Nginx"), ("githubactions", "Actions")],
                [("vercel", "Vercel"), ("digitalocean", "DigitalOcean"), ("git", "Git")],
            ],
        ),
    ]

    blocks = []
    for idx, (x, y, cat_icon, title, color_key, rows) in enumerate(quads):
        c = t[color_key]
        cat_svg = ui_icon_svg(cat_icon, x + 25, y + 21, 14, c, 2.0)
        pills = render_icon_pill_rows(rows, x, y + 58, mode, idx)
        blocks.append(
            f'<rect x="{x + 0.75}" y="{y + 0.75}" width="440.5" height="138.5" rx="13.25" '
            f'fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5" />\n'
            f'  <rect x="{x + 20}" y="{y + 16}" width="24" height="24" rx="6" fill="{c}" fill-opacity="0.14" stroke="{c}" stroke-opacity="0.35" stroke-width="1" />\n'
            f'  {cat_svg}\n'
            f'  <text x="{x + 54}" y="{y + 32}" fill="{t["text"]}" font-family="{FONT_MONO}" '
            f'font-size="11.5" font-weight="700" letter-spacing="0.8">{escape(title)}</text>\n'
            f'  <line x1="{x + 20}" y1="{y + 47}" x2="{x + 420}" y2="{y + 47}" stroke="{t["divider"]}" stroke-width="1" />\n'
            f'  {pills}'
        )
    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="294" viewBox="0 0 900 294" fill="none">
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
            "cat_fe",
            "Strict Type Safety & Contracts",
            "End-to-end TypeScript sharing with Zod and class-validator",
            "enforces runtime validation and clean API contracts.",
        ),
        (
            458,
            0,
            "zap",
            "cat_ops",
            "Performance & Rendering",
            "Next.js Server Components, streaming SSR, and smart caching",
            "keep client bundles lean and Core Web Vitals fast.",
        ),
        (
            0,
            116,
            "refresh",
            "cat_db",
            "Resilient Business Workflows",
            "Idempotent webhook handlers, atomic DB transactions, and",
            "background retry queues protect critical state mutations.",
        ),
        (
            458,
            116,
            "layers",
            "cat_be",
            "Modular Clean Architecture",
            "Clear boundaries between UI, services, and persistence keep",
            "domain logic decoupled, readable, testable, and extensible.",
        ),
        (
            0,
            232,
            "database",
            "cat_perf",
            "Database & Query Efficiency",
            "Normalized schemas, strategic indexing, safe Prisma/Drizzle",
            "migrations, and query profiling prevent N+1 bottlenecks.",
        ),
        (
            458,
            232,
            "terminal",
            "cat_obs",
            "Observability & Automated Delivery",
            "Structured logging, predictable error contracts, Dockerized",
            "builds, and GitHub Actions CI/CD ensure confident releases.",
        ),
    ]

    blocks = []
    for x, y, icon_name, color_key, title, l1, l2 in cards:
        c = t[color_key]
        ic = ui_icon_svg(icon_name, x + 26, y + 22, 16, c, 2.0)
        blocks.append(
            f'<rect x="{x + 0.75}" y="{y + 0.75}" width="440.5" height="100.5" rx="13.25" '
            f'fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5" />\n'
            f'  <rect x="{x + 20}" y="{y + 16}" width="28" height="28" rx="8" fill="{c}" fill-opacity="0.14" stroke="{c}" stroke-opacity="0.35" stroke-width="1" />\n'
            f'  {ic}\n'
            f'  <text x="{x + 58}" y="{y + 35}" fill="{t["text"]}" font-family="{FONT_SANS}" '
            f'font-size="14.5" font-weight="700">{escape(title)}</text>\n'
            f'  <text x="{x + 20}" y="{y + 62}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(l1)}</text>\n'
            f'  <text x="{x + 20}" y="{y + 81}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(l2)}</text>'
        )
    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="334" viewBox="0 0 900 334" fill="none">
  {inner}
</svg>
'''


def main() -> None:
    for mode in ("dark", "light"):
        (ASSETS / f"bento-hero-{mode}.svg").write_text(build_hero_bento(mode), encoding="utf-8")
        (ASSETS / f"bento-stack-{mode}.svg").write_text(build_stack_bento(mode), encoding="utf-8")
        (ASSETS / f"bento-principles-{mode}.svg").write_text(build_principles_bento(mode), encoding="utf-8")

    # Remove unused Featured Projects SVGs
    for old_proj in ASSETS.glob("project-*.svg"):
        old_proj.unlink()

    print(f"Generated {len(list(ASSETS.glob('bento-*.svg')))} Bento SVGs using {len(list(ICONS_DIR.glob('*.svg')))} downloaded brand icons.")


if __name__ == "__main__":
    main()
