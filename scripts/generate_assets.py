#!/usr/bin/env python3
"""
Generates dual-theme (dark & light) Bento Grid SVG assets for the GitHub Profile README.
Run: python3 scripts/generate_assets.py
"""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"

THEMES = {
    "dark": {
        "canvas": "#0d1117",
        "card": "#161b22",
        "card_alt": "#131922",
        "border": "#30363d",
        "divider": "#21262d",
        "text": "#f0f6fc",
        "subtext": "#8b949e",
        "muted": "#6e7681",
        "pill_bg": "#21262d",
        "pill_border": "#30363d",
        "pill_text": "#c9d1d9",
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
        "cat_fe": "#38bdf8",
        "cat_be": "#fb7185",
        "cat_db": "#34d399",
        "cat_ops": "#a78bfa",
    },
    "light": {
        "canvas": "#ffffff",
        "card": "#f6f8fa",
        "card_alt": "#ffffff",
        "border": "#d0d7de",
        "divider": "#d8dee4",
        "text": "#1f2328",
        "subtext": "#57606a",
        "muted": "#6e7781",
        "pill_bg": "#ffffff",
        "pill_border": "#d0d7de",
        "pill_text": "#24292f",
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
        "cat_fe": "#0284c7",
        "cat_be": "#e11d48",
        "cat_db": "#059669",
        "cat_ops": "#7c3aed",
    },
}


def render_pills(pills: list[str], x_start: int, y: int, t: dict, max_width: int = 390) -> str:
    """Renders compact rounded tech pills on a single row (wrapping cleanly if needed)."""
    out = []
    x = x_start
    row_y = y
    for label in pills:
        w = max(48, len(label) * 7 + 20)
        if x + w > x_start + max_width:
            x = x_start
            row_y += 28
        out.append(
            f'<rect x="{x}" y="{row_y}" width="{w}" height="22" rx="6" '
            f'fill="{t["pill_bg"]}" stroke="{t["pill_border"]}" stroke-width="1" />'
            f'<text x="{x + w / 2:.1f}" y="{row_y + 14.5}" text-anchor="middle" '
            f'fill="{t["pill_text"]}" font-family="{FONT_MONO}" font-size="11">{escape(label)}</text>'
        )
        x += w + 7
    return "\n  ".join(out)


def build_hero_bento(mode: str) -> str:
    t = THEMES[mode]
    # 900x240: Left main hero card (0..568) + 16px gap + Right snapshot card (584..900)
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

  <text x="608" y="76" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11">LOCATION</text>
  <text x="608" y="94" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Cairo, Egypt (UTC+2)</text>

  <text x="608" y="124" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11">SPECIALIZATION</text>
  <text x="608" y="142" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Multi-Tenant SaaS &amp; Commerce</text>

  <text x="608" y="172" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11">CURRENTLY SHIPPING</text>
  <text x="608" y="190" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="13.5" font-weight="500">Web Platforms &amp; VS Code Tooling</text>

  <text x="608" y="218" fill="{t["link"]}" font-family="{FONT_MONO}" font-size="11">taha-hamdy.vercel.app</text>
</svg>
'''


def build_project_card(
    mode: str,
    title: str,
    badge: str,
    line1: str,
    line2: str,
    tags: list[str],
    footer_left: str,
    accent_key: str,
) -> str:
    t = THEMES[mode]
    accent = t[accent_key]
    pills_svg = render_pills(tags, 24, 102, t, max_width=392)
    badge_w = max(72, len(badge) * 6.5 + 18)
    badge_x = 416 - badge_w
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="172" viewBox="0 0 440 172" fill="none">
  <rect x="0.75" y="0.75" width="438.5" height="170.5" rx="13.25" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5" />
  <rect x="24" y="24" width="6" height="20" rx="3" fill="{accent}" />
  <text x="38" y="39" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="16" font-weight="700">{escape(title)}</text>

  <rect x="{badge_x:.1f}" y="22" width="{badge_w:.1f}" height="22" rx="11" fill="{t["pill_bg"]}" stroke="{t["pill_border"]}" stroke-width="1" />
  <text x="{badge_x + badge_w / 2:.1f}" y="36.5" text-anchor="middle" fill="{t["subtext"]}" font-family="{FONT_MONO}" font-size="10">{escape(badge)}</text>

  <text x="24" y="68" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(line1)}</text>
  <text x="24" y="86" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(line2)}</text>

  {pills_svg}

  <line x1="24" y1="138" x2="416" y2="138" stroke="{t["divider"]}" stroke-width="1" />
  <text x="24" y="156" fill="{t["link"]}" font-family="{FONT_MONO}" font-size="11.5" font-weight="600">{escape(footer_left)}</text>
  <text x="416" y="156" text-anchor="end" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11">OPEN -&gt;</text>
</svg>
'''


def render_pill_rows(rows: list[list[str]], x_start: int, y_start: int, t: dict) -> str:
    """Renders explicit balanced rows of compact rounded tech pills."""
    out = []
    for row_idx, row in enumerate(rows):
        x = x_start
        y = y_start + row_idx * 29
        for label in row:
            w = max(54, len(label) * 7 + 22)
            out.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="23" rx="6" '
                f'fill="{t["pill_bg"]}" stroke="{t["pill_border"]}" stroke-width="1" />'
                f'<text x="{x + w / 2:.1f}" y="{y + 15}" text-anchor="middle" '
                f'fill="{t["pill_text"]}" font-family="{FONT_MONO}" font-size="11">{escape(label)}</text>'
            )
            x += w + 8
    return "\n  ".join(out)


def build_stack_bento(mode: str) -> str:
    t = THEMES[mode]
    quads = [
        (0, 0, "FRONTEND & UI", "cat_fe", [["TypeScript", "Next.js", "React"], ["Tailwind CSS", "Shadcn UI", "Material UI"]]),
        (458, 0, "BACKEND & APIS", "cat_be", [["NestJS", "Node.js", "Express", "Fastify"], ["GraphQL", "REST APIs", "Webhooks"]]),
        (0, 132, "DATABASES & ORMS", "cat_db", [["PostgreSQL", "MySQL", "MongoDB", "Redis"], ["Prisma", "Drizzle ORM", "TypeORM"]]),
        (458, 132, "DEVOPS & DELIVERY", "cat_ops", [["Docker", "Nginx", "GitHub Actions"], ["Vercel", "DigitalOcean", "Git"]]),
    ]
    blocks = []
    for x, y, title, color_key, rows in quads:
        pills = render_pill_rows(rows, x + 22, y + 48, t)
        blocks.append(
            f'<rect x="{x + 0.75}" y="{y + 0.75}" width="440.5" height="114.5" rx="13.25" '
            f'fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5" />\n'
            f'  <circle cx="{x + 28}" cy="{y + 27}" r="4.5" fill="{t[color_key]}" />\n'
            f'  <text x="{x + 40}" y="{y + 31}" fill="{t["text"]}" font-family="{FONT_MONO}" '
            f'font-size="11.5" font-weight="700" letter-spacing="0.8">{escape(title)}</text>\n'
            f'  {pills}'
        )
    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="248" viewBox="0 0 900 248" fill="none">
  {inner}
</svg>
'''


def build_principles_bento(mode: str) -> str:
    t = THEMES[mode]
    cards = [
        (0, 0, "01", "cat_fe", "Strict Type Safety & Contracts", "End-to-end TypeScript sharing with Zod and class-validator", "keeps untrusted inputs out of core business logic."),
        (458, 0, "02", "cat_ops", "Performance & Rendering", "Next.js Server Components, SSR streaming, and caching", "keep client bundles lean and Core Web Vitals fast."),
        (0, 114, "03", "cat_db", "Resilient Business Workflows", "Idempotent webhook handlers, atomic DB transactions,", "and safe retry queues protect critical state mutations."),
        (458, 114, "04", "cat_be", "Modular Architecture", "Clear separation between UI, application services, and", "persistence keeps features testable and maintainable."),
    ]
    blocks = []
    for x, y, num, color_key, title, l1, l2 in cards:
        blocks.append(
            f'<rect x="{x + 0.75}" y="{y + 0.75}" width="440.5" height="96.5" rx="13.25" '
            f'fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5" />\n'
            f'  <text x="{x + 24}" y="{y + 32}" fill="{t[color_key]}" font-family="{FONT_MONO}" '
            f'font-size="12" font-weight="700">{num}</text>\n'
            f'  <text x="{x + 50}" y="{y + 32}" fill="{t["text"]}" font-family="{FONT_SANS}" '
            f'font-size="14.5" font-weight="700">{escape(title)}</text>\n'
            f'  <text x="{x + 24}" y="{y + 57}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(l1)}</text>\n'
            f'  <text x="{x + 24}" y="{y + 76}" fill="{t["subtext"]}" font-family="{FONT_SANS}" font-size="12.5">{escape(l2)}</text>'
        )
    inner = "\n  ".join(blocks)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="212" viewBox="0 0 900 212" fill="none">
  {inner}
</svg>
'''


def main() -> None:
    projects = [
        (
            "project-nestjs-forge",
            "NestJS Forge",
            "VS Code Extension",
            "Interactive VS Code scaffolding tool for generating NestJS",
            "modules, controllers, services, and DTOs cleanly.",
            ["TypeScript", "VS Code API", "NestJS"],
            "TahaHamdy-MernDev/nestjs-forge-vs-extension",
            "cat_be",
        ),
        (
            "project-admin-panel",
            "Admin Panel",
            "Live on Vercel",
            "Operations dashboard with structured data tables, role-based",
            "views, and modular component primitives.",
            ["Next.js", "TypeScript", "Tailwind CSS"],
            "TahaHamdy-MernDev/admin-panel",
            "cat_fe",
        ),
        (
            "project-buy-from-egypt",
            "Buy From Egypt",
            "E-Commerce",
            "Full-stack commerce platform built for catalog browsing,",
            "structured checkout flows, and order management.",
            ["TypeScript", "Next.js", "Node.js"],
            "TahaHamdy-MernDev/buy_from_egypt",
            "cat_db",
        ),
        (
            "project-qwafel",
            "Qwafel Platform",
            "Live on Vercel",
            "Modern production web application built with TypeScript,",
            "optimized rendering, and responsive layouts.",
            ["TypeScript", "React", "Vercel"],
            "TahaHamdy-MernDev/qwafel",
            "cat_ops",
        ),
    ]

    for mode in ("dark", "light"):
        (ASSETS / f"bento-hero-{mode}.svg").write_text(build_hero_bento(mode), encoding="utf-8")
        (ASSETS / f"bento-stack-{mode}.svg").write_text(build_stack_bento(mode), encoding="utf-8")
        (ASSETS / f"bento-principles-{mode}.svg").write_text(build_principles_bento(mode), encoding="utf-8")
        for slug, title, badge, l1, l2, tags, footer_left, accent_key in projects:
            svg = build_project_card(mode, title, badge, l1, l2, tags, footer_left, accent_key)
            (ASSETS / f"{slug}-{mode}.svg").write_text(svg, encoding="utf-8")

    # Clean up older hero files if present
    for old in ("hero-dark.svg", "hero-light.svg"):
        p = ASSETS / old
        if p.exists():
            p.unlink()

    print(f"Generated {len(list(ASSETS.glob('*.svg')))} dual-theme SVG Bento assets in {ASSETS}")


if __name__ == "__main__":
    main()
