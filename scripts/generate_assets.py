#!/usr/bin/env python3
"""
Generates dual-theme (dark & light) flat, minimalist, subtly animated SVG sections
for the GitHub Profile README:
- profile-hero-v2-{dark,light}.svg       : Flat 2-card hero + snapshot with smooth staggered fade-in
- profile-stack-v2-{dark,light}.svg      : Clean 4-row horizontal spec sheet with real animated brand icons
- profile-principles-v2-{dark,light}.svg : 3-column x 2-row flat editorial principles grid with animated icons
- btn-*-{dark,light}.svg                 : Rounded flat monochrome button pills
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
        "icon_box_bg": "#ffffff",
        "icon_box_border": "#d0d7de",
        "icon_stroke": "#57606a",
        "mono_icon": "#1f2328",
        "drizzle_icon": "#65a30d",
    },
}

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
    "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" />',
    "webhook": (
        '<path d="M18 16.98h-5.99c-1.1 0-1.95.94-2.48 1.9A4 4 0 0 1 2 17c.01-.7.2-1.4.57-2" />'
        '<path d="m6 17 3.13-5.78c.53-.97.1-2.18-.5-3.1a4 4 0 1 1 6.89-4.06" />'
        '<path d="m12 6 3.13 5.73C15.66 12.7 16.9 13 18 13a4 4 0 0 1 0 8" />'
    ),
    "shield": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />'
        '<path d="m9 12 2 2 4-4" />'
    ),
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />',
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
    "globe": (
        '<circle cx="12" cy="12" r="10" />'
        '<line x1="2" y1="12" x2="22" y2="12" />'
        '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />'
    ),
    "linkedin": (
        '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />'
        '<rect x="2" y="9" width="4" height="12" />'
        '<circle cx="4" cy="4" r="2" />'
    ),
    "mail": (
        '<rect x="2" y="4" width="20" height="16" rx="2" />'
        '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />'
    ),
    "folder": (
        '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z" />'
    ),
}

# Single-path monochrome icons that adapt cleanly to dark & light modes
MONOCHROME_ICONS = {"nextjs", "shadcnui", "express", "fastify", "vercel", "prisma"}


def ui_icon_svg(name: str, x: float, y: float, size: int, color: str, stroke_width: float = 1.75) -> str:
    body = UI_ICONS[name]
    return (
        f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" viewBox="0 0 24 24" '
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
    view_box = vb_match.group(1) if vb_match else "0 0 24 24"
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
    elif icon_name == "typeorm":
        fill_attr = ' fill="#fe0803"'

    return (
        f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" '
        f'viewBox="{view_box}"{fill_attr}>{inner}</svg>'
    )


def build_hero(mode: str) -> str:
    t = THEMES[mode]
    pin_ic = ui_icon_svg("pin", 612, 62, 14, t["subtext"], 1.7)
    layers_ic = ui_icon_svg("layers", 612, 114, 14, t["subtext"], 1.7)
    box_ic = ui_icon_svg("box", 612, 166, 14, t["subtext"], 1.7)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="216" viewBox="0 0 900 216" fill="none">
  <style>
    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .a1 {{ opacity: 0; animation: fadeUp 0.55s ease-out 0.05s forwards; }}
    .a2 {{ opacity: 0; animation: fadeUp 0.55s ease-out 0.16s forwards; }}
    .a3 {{ opacity: 0; animation: fadeUp 0.55s ease-out 0.28s forwards; }}
    .a4 {{ opacity: 0; animation: fadeUp 0.55s ease-out 0.38s forwards; }}
    @media (prefers-reduced-motion: reduce) {{
      .a1, .a2, .a3, .a4 {{ opacity: 1; animation: none; }}
    }}
  </style>

  <!-- Left Flat Identity Card -->
  <rect x="0.5" y="0.5" width="565" height="215" rx="14" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />

  <g class="a1">
    <text x="36" y="60" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="34" font-weight="700" letter-spacing="-0.7">Taha Hamdy</text>
    <text x="36" y="90" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="15" font-weight="500">Full-Stack Software Engineer</text>
  </g>

  <g class="a2">
    <text x="36" y="128" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="13.5">Designing and shipping production SaaS platforms, modular</text>
    <text x="36" y="149" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="13.5">NestJS APIs, and fast Next.js interfaces with TypeScript.</text>
  </g>

  <g class="a3">
    <line x1="36" y1="172" x2="530" y2="172" stroke="{t["divider"]}" stroke-width="1" />
    <text x="36" y="195" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11.5">TypeScript  ·  Next.js  ·  NestJS  ·  PostgreSQL  ·  Prisma  ·  Drizzle</text>
  </g>

  <!-- Right Flat Snapshot Card -->
  <rect x="585.5" y="0.5" width="314" height="215" rx="14" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />
  <text x="612" y="34" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10.5" font-weight="600" letter-spacing="1.2">SNAPSHOT</text>
  <line x1="612" y1="48" x2="874" y2="48" stroke="{t["divider"]}" stroke-width="1" />

  <g class="a2">
    {pin_ic}
    <text x="634" y="73" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10">LOCATION</text>
    <text x="634" y="92" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Cairo, Egypt (UTC+2)</text>
  </g>

  <g class="a3">
    {layers_ic}
    <text x="634" y="125" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10">FOCUS</text>
    <text x="634" y="144" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Multi-Tenant SaaS &amp; Commerce</text>
  </g>

  <g class="a4">
    {box_ic}
    <text x="634" y="177" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="10">BUILDING</text>
    <text x="634" y="196" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Web Platforms &amp; Dev Tooling</text>
  </g>
</svg>
'''


def build_stack(mode: str) -> str:
    """Clean 4-row horizontal spec sheet with real embedded animated brand icons."""
    t = THEMES[mode]
    rows = [
        (
            "layout",
            "Frontend",
            [
                ("typescript", "TypeScript"),
                ("nextjs", "Next.js"),
                ("react", "React"),
                ("tailwindcss", "Tailwind"),
                ("shadcnui", "Shadcn UI"),
                ("materialui", "MUI"),
            ],
        ),
        (
            "server",
            "Backend",
            [
                ("nestjs", "NestJS"),
                ("nodejs", "Node.js"),
                ("express", "Express"),
                ("fastify", "Fastify"),
                ("graphql", "GraphQL"),
                ("webhook", "Webhooks"),
            ],
        ),
        (
            "database",
            "Databases",
            [
                ("postgresql", "PostgreSQL"),
                ("mysql", "MySQL"),
                ("mongodb", "MongoDB"),
                ("redis", "Redis"),
                ("prisma", "Prisma"),
                ("drizzle", "Drizzle"),
                ("typeorm", "TypeORM"),
            ],
        ),
        (
            "cloud",
            "DevOps",
            [
                ("docker", "Docker"),
                ("nginx", "Nginx"),
                ("githubactions", "Actions"),
                ("vercel", "Vercel"),
                ("digitalocean", "DigitalOcean"),
                ("git", "Git"),
            ],
        ),
    ]

    row_h = 74
    total_h = row_h * len(rows)
    blocks = [
        '''<style>
    @keyframes floatWave {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-2.2px); }
    }
    @keyframes rowIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .row { opacity: 0; animation: rowIn 0.5s ease-out forwards; }
    .ic { animation: floatWave 3.8s ease-in-out infinite; }
    @media (prefers-reduced-motion: reduce) {
      .row { opacity: 1; animation: none; }
      .ic { animation: none; }
    }
  </style>''',
        f'<rect x="0.5" y="0.5" width="899" height="{total_h - 1}" rx="14" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />',
        f'<line x1="176" y1="16" x2="176" y2="{total_h - 16}" stroke="{t["divider"]}" stroke-width="1" />',
    ]

    for r_idx, (cat_icon, cat_label, items) in enumerate(rows):
        y_top = r_idx * row_h
        y_mid = y_top + row_h / 2
        row_delay = 0.08 * r_idx

        if r_idx > 0:
            blocks.append(f'<line x1="20" y1="{y_top}" x2="880" y2="{y_top}" stroke="{t["divider"]}" stroke-width="1" />')

        row_parts = [
            f'<rect x="24" y="{y_mid - 14:.1f}" width="28" height="28" rx="7" fill="{t["icon_box_bg"]}" stroke="{t["icon_box_border"]}" stroke-width="1" />',
            ui_icon_svg(cat_icon, 31, y_mid - 7, 14, t["icon_stroke"], 1.8),
            f'<text x="64" y="{y_mid + 4.5:.1f}" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13" font-weight="600">{escape(cat_label)}</text>',
        ]

        x = 200.0
        for c_idx, (icon_key, label) in enumerate(items):
            uid = f"st_r{r_idx}c{c_idx}"
            wave_delay = (r_idx * 0.45 + c_idx * 0.25) % 3.8
            icon_el = embed_brand_icon(icon_key, x, y_mid - 9, 18, mode, uid)
            row_parts.append(f'<g class="ic" style="animation-delay:{wave_delay:.2f}s">{icon_el}</g>')
            row_parts.append(
                f'<text x="{x + 25:.1f}" y="{y_mid + 4.5:.1f}" fill="{t["text"]}" '
                f'font-family="{FONT_SANS}" font-size="12.5" font-weight="500">{escape(label)}</text>'
            )
            step = max(78.0, 26.0 + len(label) * 7.0 + 18.0)
            x += step
        assert x - 18.0 <= 886.0, f"Row '{cat_label}' overflowed ({x - 18.0} > 886)"

        blocks.append(f'<g class="row" style="animation-delay:{row_delay:.2f}s">\n    ' + "\n    ".join(row_parts) + "\n  </g>")

    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{total_h}" viewBox="0 0 900 {total_h}" fill="none">
  {inner}
</svg>
'''


def build_principles(mode: str) -> str:
    """3-column x 2-row flat editorial principles grid with staggered entrance & subtle icon pulse."""
    t = THEMES[mode]
    cards = [
        (
            "shield",
            "Type Safety & Contracts",
            "End-to-end TypeScript with Zod",
            "and class-validator enforces strict",
            "runtime validation at every boundary.",
        ),
        (
            "zap",
            "Rendering Performance",
            "Next.js Server Components, SSR",
            "streaming, and caching keep client",
            "bundles lean and Web Vitals fast.",
        ),
        (
            "refresh",
            "Resilient Workflows",
            "Idempotent webhook handlers,",
            "atomic DB transactions, and retry",
            "queues protect critical state.",
        ),
        (
            "layers",
            "Modular Architecture",
            "Clean boundaries between UI,",
            "services, and persistence keep",
            "domains decoupled and testable.",
        ),
        (
            "database",
            "Query Efficiency",
            "Normalized schemas, strategic",
            "indexes, Prisma/Drizzle migrations,",
            "and profiling prevent N+1 issues.",
        ),
        (
            "terminal",
            "Automated Delivery",
            "Structured logs, predictable error",
            "contracts, Docker builds, and CI/CD",
            "enable confident, repeatable releases.",
        ),
    ]

    card_w = 288
    card_h = 152
    gap_x = 18
    gap_y = 18
    total_h = card_h * 2 + gap_y

    blocks = [
        '''<style>
    @keyframes cardIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseSoft {
      0%, 100% { opacity: 0.78; }
      50% { opacity: 1; }
    }
    .pcard { opacity: 0; animation: cardIn 0.55s ease-out forwards; }
    .pic { animation: pulseSoft 4.2s ease-in-out infinite; }
    @media (prefers-reduced-motion: reduce) {
      .pcard { opacity: 1; animation: none; }
      .pic { animation: none; }
    }
  </style>'''
    ]

    for idx, (icon_name, title, l1, l2, l3) in enumerate(cards):
        col = idx % 3
        row = idx // 3
        x = col * (card_w + gap_x)
        y = row * (card_h + gap_y)
        ic = ui_icon_svg(icon_name, x + 28, y + 26, 16, t["icon_stroke"], 1.8)
        delay = 0.08 * idx
        p_delay = 0.65 * idx
        blocks.append(
            f'<g class="pcard" style="animation-delay:{delay:.2f}s">\n'
            f'    <rect x="{x + 0.5}" y="{y + 0.5}" width="{card_w - 1}" height="{card_h - 1}" rx="14" '
            f'fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />\n'
            f'    <g class="pic" style="animation-delay:{p_delay:.2f}s">\n'
            f'      <rect x="{x + 22}" y="{y + 20}" width="28" height="28" rx="8" '
            f'fill="{t["icon_box_bg"]}" stroke="{t["icon_box_border"]}" stroke-width="1" />\n'
            f'      {ic}\n'
            f'    </g>\n'
            f'    <text x="{x + 22}" y="{y + 72}" fill="{t["text"]}" font-family="{FONT_SANS}" '
            f'font-size="14" font-weight="600">{escape(title)}</text>\n'
            f'    <text x="{x + 22}" y="{y + 96}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12">{escape(l1)}</text>\n'
            f'    <text x="{x + 22}" y="{y + 114}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12">{escape(l2)}</text>\n'
            f'    <text x="{x + 22}" y="{y + 132}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12">{escape(l3)}</text>\n'
            f'  </g>'
        )

    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{total_h}" viewBox="0 0 900 {total_h}" fill="none">
  {inner}
</svg>
'''


def build_button(mode: str, icon_name: str, label: str, width: int) -> str:
    t = THEMES[mode]
    h = 36
    ic = ui_icon_svg(icon_name, 16, 10.5, 15, t["icon_stroke"], 1.8)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" fill="none">
  <rect x="0.5" y="0.5" width="{width - 1}" height="{h - 1}" rx="10" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1" />
  {ic}
  <text x="39" y="22.5" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="12.5" font-weight="500">{escape(label)}</text>
</svg>
'''


def main() -> None:
    # Remove v1 profile SVGs so GitHub camo CDN serves the fresh v2 animated assets immediately
    for old in ASSETS.glob("profile-*.svg"):
        old.unlink()

    buttons = [
        ("portfolio", "globe", "Portfolio", 112),
        ("linkedin", "linkedin", "LinkedIn", 114),
        ("email", "mail", "Email", 94),
        ("repos", "folder", "Repositories", 134),
    ]

    for mode in ("dark", "light"):
        (ASSETS / f"profile-hero-v3-{mode}.svg").write_text(build_hero(mode), encoding="utf-8")
        (ASSETS / f"profile-stack-v2-{mode}.svg").write_text(build_stack(mode), encoding="utf-8")
        (ASSETS / f"profile-principles-v2-{mode}.svg").write_text(build_principles(mode), encoding="utf-8")
        for slug, icon_name, label, width in buttons:
            (ASSETS / f"btn-{slug}-{mode}.svg").write_text(build_button(mode, icon_name, label, width), encoding="utf-8")

    print("Generated 6 animated v2 section SVGs + 8 button SVGs.")


if __name__ == "__main__":
    main()
