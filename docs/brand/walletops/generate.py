#!/usr/bin/env python3
"""
walletops.io brand kit generator.

100 unique logo marks × 4 styles, plus a full favicon pack for every mark
and a drop-in recommended/ folder for each product site.

Run from repo root:
    python3 docs/brand/walletops/generate.py

Deps for PNG/ICO/contact sheets: cairosvg, pillow. SVGs need nothing.
"""
from __future__ import annotations

import io
import json
import math
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VB = 64

# --------------------------------------------------------------------------- #
# Palette
# --------------------------------------------------------------------------- #

LINES = {
    "core": {
        "name": "WalletOps",
        "tagline": "Wallet operations platform",
        "primary": "#4F46E5",
        "secondary": "#7C3AED",
        "accent": "#22D3EE",
        "domain": "walletops.io",
    },
    "analytics": {
        "name": "WalletOps Analytics",
        "tagline": "On-chain wallet analytics",
        "primary": "#0284C7",
        "secondary": "#06B6D4",
        "accent": "#FBBF24",
        "domain": "analytics.walletops.io",
    },
    "shield": {
        "name": "Wallet Shield",
        "tagline": "Wallet security and risk monitoring",
        "primary": "#059669",
        "secondary": "#10B981",
        "accent": "#38BDF8",
        "domain": "shield.walletops.io",
    },
    "intelligence": {
        "name": "Wallet Intelligence",
        "tagline": "Wallet labeling, scoring and insight",
        "primary": "#7C3AED",
        "secondary": "#C026D3",
        "accent": "#F472B6",
        "domain": "intel.walletops.io",
    },
    "specialist": {
        "name": "Wallet Specialist",
        "tagline": "Expert wallet services and support",
        "primary": "#EA580C",
        "secondary": "#F59E0B",
        "accent": "#FDE68A",
        "domain": "specialist.walletops.io",
    },
}

INK = "#0F172A"
PAPER = "#FFFFFF"
MUTED_LIGHT = "#64748B"
MUTED_DARK = "#94A3B8"
FONT = "Inter, 'SF Pro Display', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

STYLES = ["solid", "gradient", "outline", "tile"]
STYLE_DESC = {
    "solid": "Flat primary colour, white counters, transparent background.",
    "gradient": "Primary-to-secondary gradient, white counters, transparent background.",
    "outline": "Stroke-only version for monochrome, print, and watermarks.",
    "tile": "White mark on a rounded gradient tile. Use for app icons and favicons.",
}

HERO = {
    "core": "core-w-monogram",
    "analytics": "analytics-w-bars",
    "shield": "shield-check",
    "intelligence": "intel-neural-w",
    "specialist": "spec-seal",
}

PRODUCT_LABEL = {
    "core": "WALLET OPERATIONS PLATFORM",
    "analytics": "ANALYTICS",
    "shield": "SHIELD",
    "intelligence": "INTELLIGENCE",
    "specialist": "SPECIALIST",
}

PNG_SIZES = [16, 32, 48, 180, 192, 512]
PNG_NAMES = {
    16: "favicon-16x16.png",
    32: "favicon-32x32.png",
    48: "favicon-48x48.png",
    180: "apple-touch-icon.png",
    192: "android-chrome-192x192.png",
    512: "android-chrome-512x512.png",
}

# --------------------------------------------------------------------------- #
# Shape model
# --------------------------------------------------------------------------- #
# fill / stroke tokens: 'p' primary  'a' accent  'c' counter (white, or tile gradient)
# over=True  -> drawn after the mask (sits on top of a hole)
# keep=True  -> stays filled in outline style (dots, badges, small accents)


@dataclass
class Shape:
    tag: str
    attrs: dict
    fill: str | None = None
    stroke: str | None = None
    sw: float = 0
    keep: bool = False
    over: bool = False


def S(tag, fill=None, stroke=None, sw=0, keep=False, over=False, **attrs) -> Shape:
    return Shape(tag, attrs, fill, stroke, sw, keep, over)


def fmt(v):
    if isinstance(v, float):
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return s if s not in ("", "-0") else "0"
    return str(v)


def pts(points):
    return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in points)


def rect(x, y, w, h, rx=0, **kw):
    return S("rect", x=x, y=y, width=w, height=h, rx=rx, **kw)


def circle(cx, cy, r, **kw):
    return S("circle", cx=cx, cy=cy, r=r, **kw)


def path(d, **kw):
    return S("path", d=d, **kw)


def line(x1, y1, x2, y2, sw, **kw):
    kw.setdefault("stroke", "p")
    return S("line", x1=x1, y1=y1, x2=x2, y2=y2, sw=sw, **kw)


def polyline(points, sw, **kw):
    kw.setdefault("stroke", "p")
    return S("polyline", points=pts(points), sw=sw, **kw)


def polygon(points, **kw):
    return S("polygon", points=pts(points), **kw)


def regular_polygon(cx, cy, r, n, rot=-90):
    return [
        (cx + r * math.cos(math.radians(rot + 360 * k / n)),
         cy + r * math.sin(math.radians(rot + 360 * k / n)))
        for k in range(n)
    ]


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    out = []
    for k in range(2 * n):
        r = r_out if k % 2 == 0 else r_in
        a = math.radians(rot + 180 * k / n)
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def gear_points(cx, cy, r_out, r_in, teeth=8):
    out = []
    step = 360 / teeth
    for k in range(teeth):
        a0 = k * step
        for da, r in (
            (0, r_in), (step * 0.22, r_in), (step * 0.32, r_out),
            (step * 0.68, r_out), (step * 0.78, r_in),
        ):
            a = math.radians(a0 + da)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


SHIELD_D = "M32 4 L56 12 V30 C56 46 45 56 32 60 C19 56 8 46 8 30 V12 Z"
SHIELD_R = "M32 4 L56 12 V30 C56 46 45 56 32 60 Z"

W_PTS = [(8, 16), (18, 50), (32, 26), (46, 50), (56, 16)]
BOLT_D = "M30 10 L44 10 L32 30 L42 30 L20 54 L26 34 L16 34 Z"
BELL_D = "M22 28 C22 19 26 14 32 14 C38 14 42 19 42 28 V36 H22 Z"
KEYHOLE_D = "M32 22 A7 7 0 1 1 31.99 22 M29 28 L26 42 H38 L35 28"


def wallet(*, x=8, y=18, w=48, h=36, rx=8, card=True, clasp=True, flap=False):
    """Wallet silhouette: peeking card, rounded body, right-hand clasp slot."""
    s = []
    if card:
        s.append(rect(x + 11, y - 10, w - 22, 16, 3, fill="a", keep=True))
    s.append(rect(x, y, w, h, rx, fill="p"))
    if flap:
        s.append(line(x + 6, y + 9, x + w - 6, y + 9, 3.2, stroke="c"))
    if clasp:
        cy = y + h * 0.56
        s.append(rect(x + w - 17, cy - 8, 20, 16, 5, fill="c"))
        s.append(circle(x + w - 9, cy, 4.2, fill="a", over=True, keep=True))
    return s


def check(x, y, sw=5, scale=1.0, **kw):
    kw.setdefault("stroke", "c")
    return polyline(
        [(x - 8 * scale, y), (x - 1.5 * scale, y + 6 * scale), (x + 9 * scale, y - 6 * scale)],
        sw, **kw,
    )


def corner_badge(r=13, fill="c"):
    """Circular cut in the bottom-right, for a service badge."""
    return circle(50, 50, r, fill=fill)


# --------------------------------------------------------------------------- #
# Mark catalog  —  100 unique concepts
# --------------------------------------------------------------------------- #

MARKS: list[dict] = []


def add(line, slug, title, desc, fn):
    MARKS.append({"line": line, "slug": slug, "title": title, "desc": desc, "fn": fn})


def register_marks():
    MARKS.clear()

    # ===== WalletOps core (20) =============================================
    add("core", "core-wallet-classic", "Classic Wallet",
        "Rounded wallet with a peeking card and clasp. The master product mark.",
        lambda: wallet())
    add("core", "core-wallet-pulse", "Ops Pulse",
        "Live operations heartbeat running through the wallet.",
        lambda: wallet(clasp=False) + [polyline(
            [(14, 38), (22, 38), (26, 28), (32, 46), (38, 32), (43, 38), (52, 38)], 3.6, stroke="c")])
    add("core", "core-w-circle", "W Coin",
        "Coin disc with a cut-out W. Works at 16px as the site favicon.",
        lambda: [circle(32, 32, 28, fill="p"),
                 polyline([(16, 20), (23, 46), (32, 30), (41, 46), (48, 20)], 5, stroke="c")])
    add("core", "core-w-monogram", "W Monogram",
        "Bold W with an accent ops node. Recommended WalletOps wordmark companion.",
        lambda: [polyline(W_PTS, 8, stroke="p"),
                 circle(32, 26, 5.5, fill="a", over=True, keep=True)])
    add("core", "core-wo-orbit", "WO Orbit",
        "W monogram with an orbiting O for walletops.io.",
        lambda: [polyline([(10, 18), (20, 50), (32, 28), (44, 50), (50, 22)], 7, stroke="p"),
                 circle(52, 16, 10, stroke="a", sw=4, keep=True),
                 circle(52, 16, 3.2, fill="a", keep=True)])
    add("core", "core-wallet-gear", "Wallet Gear",
        "Operations gear badged onto the wallet.",
        lambda: wallet(clasp=False) + [
            corner_badge(),
            polygon(gear_points(50, 50, 10, 7.2, 8), fill="a", over=True, keep=True),
            circle(50, 50, 3.2, fill="p", over=True, keep=True)])
    add("core", "core-hex-wallet", "Hex Wallet",
        "Chain-style hex containing a wallet outline.",
        lambda: [polygon(regular_polygon(32, 32, 29, 6), fill="p"),
                 rect(18, 24, 28, 18, 4, stroke="c", sw=3.2),
                 circle(41, 33, 3.2, fill="c")])
    add("core", "core-stack", "Card Stack",
        "Layered cards for multi-wallet operations.",
        lambda: [rect(16, 6, 36, 24, 6, fill="a", keep=True),
                 rect(12, 14, 40, 24, 6, fill="p"),
                 rect(8, 22, 48, 32, 8, fill="p"),
                 rect(36, 32, 22, 14, 5, fill="c"),
                 circle(47, 39, 3.8, fill="a", over=True, keep=True)])
    add("core", "core-terminal", "Ops Terminal",
        "Wallet as a command prompt for the ops desk.",
        lambda: wallet(clasp=False, flap=True) + [
            polyline([(16, 30), (24, 38), (16, 46)], 3.8, stroke="c"),
            rect(28, 43, 16, 3.6, 1.6, fill="c")])
    add("core", "core-wallet-bolt", "Ops Bolt",
        "Speed of execution. Lightning cut through the wallet.",
        lambda: wallet(clasp=False, card=True) + [path(BOLT_D, fill="c")])
    add("core", "core-wallet-flow", "Ops Flow",
        "Circular swap arrows around a wallet core.",
        lambda: [path("M32 8 A24 24 0 0 1 56 32", stroke="p", sw=5),
                 polygon([(56, 32), (50, 24), (62, 26)], fill="p"),
                 path("M32 56 A24 24 0 0 1 8 32", stroke="a", sw=5, keep=True),
                 polygon([(8, 32), (14, 40), (2, 38)], fill="a", keep=True),
                 rect(20, 24, 24, 16, 4, fill="p"),
                 circle(38, 32, 2.4, fill="c")])
    add("core", "core-key-wallet", "Wallet Key",
        "Access and control. Key cut into the wallet body.",
        lambda: wallet(clasp=False) + [
            circle(24, 36, 7, stroke="c", sw=3.4),
            rect(30, 34, 18, 4.2, 1.6, fill="c"),
            rect(42, 34, 3.2, 8, 1, fill="c"),
            rect(47, 34, 3.2, 6, 1, fill="c")])
    add("core", "core-wallet-grid", "Ops Grid",
        "Four-cell dashboard grid inside the wallet.",
        lambda: wallet(clasp=False, flap=True) + [
            rect(16, 30, 13, 10, 2, fill="c"),
            rect(35, 30, 13, 10, 2, fill="c"),
            rect(16, 42, 13, 8, 2, fill="c"),
            rect(35, 42, 13, 8, 2, fill="a", over=True, keep=True)])
    add("core", "core-orbit", "Orbit Wallet",
        "Wallet at the centre of an operations orbit.",
        lambda: [circle(32, 32, 26, stroke="p", sw=3),
                 circle(32, 8, 4.5, fill="a", keep=True),
                 rect(18, 22, 28, 22, 6, fill="p"),
                 circle(40, 33, 3.2, fill="c")])
    add("core", "core-layers", "Ops Layers",
        "Stacked service layers under a wallet lid.",
        lambda: [rect(14, 10, 36, 14, 4, fill="a", keep=True),
                 rect(11, 20, 42, 14, 4, fill="p"),
                 rect(8, 30, 48, 22, 7, fill="p"),
                 circle(44, 41, 4, fill="a", over=True, keep=True)])
    add("core", "core-hex-w", "Hex W",
        "W monogram in a hexagonal chain badge.",
        lambda: [polygon(regular_polygon(32, 32, 29, 6), fill="p"),
                 polyline([(16, 22), (23, 44), (32, 30), (41, 44), (48, 22)], 4.2, stroke="c")])
    add("core", "core-wallet-plus", "Add Wallet",
        "Create and onboard wallets. Plus cut-out.",
        lambda: wallet(clasp=False) + [
            rect(29, 28, 6, 20, 2, fill="c"),
            rect(22, 35, 20, 6, 2, fill="c")])
    add("core", "core-fold", "Folded Card",
        "A single folded payment card. Minimal mark.",
        lambda: [rect(10, 16, 44, 32, 7, fill="p"),
                 polygon([(40, 16), (54, 16), (54, 30)], fill="c"),
                 polygon([(42, 16), (54, 16), (54, 28)], fill="a", over=True, keep=True)])
    add("core", "core-infinity", "Ops Loop",
        "Continuous operations. Infinity loop with an accent node.",
        lambda: [path("M18 32 C18 22 26 22 32 32 C38 42 46 42 46 32 C46 22 38 22 32 32 C26 42 18 42 18 32",
                      stroke="p", sw=6),
                 circle(32, 32, 5, fill="a", keep=True)])
    add("core", "core-dots", "Three Dots",
        "Wallet with an ops overflow menu. Simple at every size.",
        lambda: wallet(clasp=False, flap=True) + [
            circle(20, 38, 4, fill="c"), circle(32, 38, 4, fill="c"),
            circle(44, 38, 4, fill="a", over=True, keep=True)])

    # ===== Analytics (20) ==================================================
    add("analytics", "analytics-bars-wallet", "Bars in Wallet",
        "Rising bars cut into the wallet. Core analytics mark.",
        lambda: wallet(clasp=False, flap=True) + [
            rect(16, 40, 8, 10, 2, fill="c"),
            rect(28, 32, 8, 18, 2, fill="c"),
            rect(40, 24, 8, 26, 2, fill="c")])
    add("analytics", "analytics-trend-wallet", "Trend Line",
        "Up-and-to-the-right cut into the wallet, accent arrow head.",
        lambda: wallet(clasp=False, flap=True) + [
            polyline([(14, 46), (24, 36), (32, 42), (44, 26)], 4, stroke="c"),
            polygon([(52, 18), (40, 22), (48, 32)], fill="a", over=True, keep=True)])
    add("analytics", "analytics-donut-wallet", "Donut Wallet",
        "Allocation donut with an accent share.",
        lambda: wallet(clasp=False, flap=True) + [
            circle(32, 38, 11, stroke="c", sw=6.5),
            path("M32 27 A11 11 0 0 1 42 35", stroke="a", sw=6.5, over=True, keep=True)])
    add("analytics", "analytics-w-bars", "W Bar Chart",
        "Five bars whose tops trace a W. Recommended Analytics favicon.",
        lambda: [rect(6, 14, 9, 42, 2.5, fill="p"),
                 rect(17, 34, 9, 22, 2.5, fill="p"),
                 rect(28, 24, 8, 32, 2.5, fill="a", keep=True),
                 rect(38, 34, 9, 22, 2.5, fill="p"),
                 rect(49, 14, 9, 42, 2.5, fill="p")])
    add("analytics", "analytics-candles", "Candlesticks",
        "Three candlesticks cut into the wallet.",
        lambda: wallet(clasp=False, flap=True) + [
            line(20, 26, 20, 50, 2.4, stroke="c"), rect(16.5, 32, 7, 12, 1.4, fill="c"),
            line(32, 22, 32, 50, 2.4, stroke="c"), rect(28.5, 28, 7, 14, 1.4, fill="c"),
            line(44, 24, 44, 48, 2.4, stroke="c"), rect(40.5, 26, 7, 10, 1.4, fill="a", over=True, keep=True)])
    add("analytics", "analytics-sparkline", "Sparkline Card",
        "Compact card with a sparkline and accent end-point.",
        lambda: [rect(8, 16, 48, 32, 7, fill="p"),
                 polyline([(14, 38), (22, 30), (29, 35), (37, 24), (44, 30), (50, 20)], 3.6, stroke="c"),
                 circle(50, 20, 4.2, fill="a", over=True, keep=True)])
    add("analytics", "analytics-gauge", "Performance Gauge",
        "Half-gauge with an accent needle over a wallet.",
        lambda: [path("M8 40 A24 24 0 0 1 56 40", stroke="p", sw=7),
                 line(32, 40, 46, 24, 4.2, stroke="a", keep=True),
                 circle(32, 40, 4.8, fill="a", keep=True),
                 rect(20, 46, 24, 12, 3, fill="p"),
                 circle(38, 52, 2.4, fill="c")])
    add("analytics", "analytics-pie", "Pie Share",
        "Portfolio share pie with an accent slice.",
        lambda: [circle(32, 32, 26, fill="p"),
                 path("M32 32 L32 6 A26 26 0 0 1 54 22 Z", fill="a", keep=True),
                 circle(32, 32, 8, fill="c")])
    add("analytics", "analytics-area", "Area Chart",
        "Filled area chart inside the wallet.",
        lambda: wallet(clasp=False, flap=True) + [
            path("M12 46 L12 40 L22 32 L32 36 L44 24 L52 28 L52 46 Z", fill="c")])
    add("analytics", "analytics-kpi", "KPI Up",
        "Big up-metric. Bar and arrow for daily PnL.",
        lambda: [rect(10, 28, 12, 24, 3, fill="p"),
                 rect(26, 18, 12, 34, 3, fill="p"),
                 rect(42, 8, 12, 44, 3, fill="a", keep=True),
                 polygon([(38, 14), (48, 4), (58, 14)], fill="a", keep=True)])
    add("analytics", "analytics-histogram", "Histogram",
        "Distribution histogram across the wallet floor.",
        lambda: wallet(clasp=False, flap=True) + [
            rect(14 + i * 6, 48 - h, 4.6, h, 1, fill="c")
            for i, h in enumerate((8, 14, 10, 20, 16, 24, 12))])
    add("analytics", "analytics-funnel", "Funnel",
        "Conversion funnel of three decreasing stages.",
        lambda: [polygon([(10, 10), (54, 10), (46, 24), (18, 24)], fill="p"),
                 polygon([(18, 26), (46, 26), (40, 38), (24, 38)], fill="p"),
                 polygon([(24, 40), (40, 40), (36, 54), (28, 54)], fill="a", keep=True)])
    add("analytics", "analytics-heatmap", "Heatmap",
        "3x3 intensity grid. Wallet clustering view.",
        lambda: [rect(8, 8, 48, 48, 10, fill="p")] + [
            circle(18 + (i % 3) * 14, 18 + (i // 3) * 14, r,
                   fill=("a" if r >= 6 else "c"), keep=r >= 6, over=r >= 6)
            for i, r in enumerate((4.2, 6.5, 3.6, 7.2, 5, 8, 3.8, 6, 4.8))])
    add("analytics", "analytics-scatter", "Scatter",
        "Scatter plot on a card. Correlation at a glance.",
        lambda: [rect(8, 12, 48, 40, 8, fill="p"),
                 line(14, 44, 50, 44, 2.4, stroke="c"), line(14, 44, 14, 18, 2.4, stroke="c"),
                 circle(22, 36, 3.2, fill="c"), circle(30, 28, 3.2, fill="c"),
                 circle(38, 32, 3.2, fill="c"), circle(46, 22, 4, fill="a", over=True, keep=True)])
    add("analytics", "analytics-percent", "Percent Move",
        "Circular percent with an accent delta.",
        lambda: [circle(32, 32, 26, fill="p"),
                 path("M32 10 A22 22 0 1 1 14 44", stroke="c", sw=6),
                 polyline([(28, 30), (32, 36), (40, 24)], 4, stroke="a", over=True, keep=True)])
    add("analytics", "analytics-table", "Table Grid",
        "Tabular wallet data. Rows and columns cut through.",
        lambda: [rect(8, 10, 48, 44, 8, fill="p"),
                 line(8, 22, 56, 22, 3, stroke="c"),
                 line(8, 34, 56, 34, 3, stroke="c"),
                 line(8, 46, 56, 46, 3, stroke="c"),
                 line(28, 10, 28, 54, 3, stroke="c")])
    add("analytics", "analytics-waterfall", "Waterfall",
        "Waterfall of stepped PnL bars.",
        lambda: [rect(8, 36, 10, 20, 2, fill="p"),
                 rect(20, 24, 10, 12, 2, fill="p"),
                 rect(32, 16, 10, 8, 2, fill="a", keep=True),
                 rect(44, 28, 12, 28, 2, fill="p"),
                 line(8, 56, 56, 56, 3, stroke="p")])
    add("analytics", "analytics-calendar", "Calendar Heat",
        "Activity calendar. Header plus intensity dots.",
        lambda: [rect(8, 10, 48, 44, 8, fill="p"),
                 rect(8, 10, 48, 12, 0, fill="a", keep=True)] + [
            circle(18 + (i % 4) * 10, 32 + (i // 4) * 10, 3.2,
                   fill=("c" if i not in (5, 9) else "a"),
                   keep=i in (5, 9), over=i in (5, 9))
            for i in range(12)])
    add("analytics", "analytics-radar-chart", "Radar Chart",
        "Pentagon radar for multi-factor wallet scores.",
        lambda: [circle(32, 32, 28, fill="p"),
                 polygon(regular_polygon(32, 32, 20, 5), stroke="c", sw=2.4),
                 polygon(regular_polygon(32, 32, 12, 5, rot=-50), fill="a", over=True, keep=True)])
    add("analytics", "analytics-dual-axis", "Dual Axis",
        "Two-series chart. Volume under price.",
        lambda: [rect(8, 12, 48, 40, 8, fill="p"),
                 polyline([(14, 40), (22, 28), (30, 32), (38, 20), (50, 24)], 3.4, stroke="c"),
                 polyline([(14, 44), (24, 38), (32, 40), (42, 34), (50, 36)], 3.4, stroke="a",
                          over=True, keep=True)])

    # ===== Shield (20) =====================================================
    add("shield", "shield-wallet", "Shielded Wallet",
        "Shield with a wallet outline cut through it.",
        lambda: [path(SHIELD_D, fill="p"),
                 rect(20, 22, 24, 18, 4, stroke="c", sw=3.2),
                 circle(39, 31, 3, fill="c")])
    add("shield", "shield-coin", "Shield Coin",
        "Shield guarding an accent coin.",
        lambda: [path(SHIELD_D, fill="p"),
                 circle(32, 30, 13, fill="c"),
                 circle(32, 30, 9.5, fill="a", over=True, keep=True),
                 circle(32, 30, 3.6, fill="p", over=True, keep=True)])
    add("shield", "shield-check", "Shield Check",
        "Verified shield. Recommended Wallet Shield favicon.",
        lambda: [path(SHIELD_D, fill="p"), check(33, 32, sw=6, scale=1.2)])
    add("shield", "shield-lock", "Shield Lock",
        "Padlock cut into the shield.",
        lambda: [path(SHIELD_D, fill="p"),
                 path("M24 30 V25 A8 8 0 0 1 40 25 V30", stroke="c", sw=3.6),
                 rect(21, 30, 22, 16, 4, fill="c"),
                 circle(32, 37, 3, fill="p", over=True, keep=True)])
    add("shield", "shield-split-w", "Split Shield W",
        "Two-tone shield carrying the W monogram.",
        lambda: [path(SHIELD_D, fill="p"), path(SHIELD_R, fill="a", keep=True),
                 polyline([(18, 22), (24, 44), (32, 30), (40, 44), (46, 22)], 4.2, stroke="c")])
    add("shield", "shield-badge", "Wallet Shield Badge",
        "Wallet with a verified shield badge.",
        lambda: wallet(clasp=False) + [
            corner_badge(14),
            S("path", d=SHIELD_D, fill="a", over=True, keep=True,
              transform="translate(34 32) scale(0.42)"),
            polyline([(46, 46), (49, 50), (55, 42)], 3.2, stroke="p", over=True, keep=True)])
    add("shield", "shield-hex-eye", "Watchful Hex",
        "Hexagonal shield with a monitoring eye.",
        lambda: [polygon(regular_polygon(32, 32, 29, 6), fill="p"),
                 path("M14 32 Q32 16 50 32 Q32 48 14 32 Z", fill="c"),
                 circle(32, 32, 6, fill="p", over=True, keep=True),
                 circle(34, 30, 2, fill="a", over=True, keep=True)])
    add("shield", "shield-key", "Shield Key",
        "Keyhole cut into the shield. Access control.",
        lambda: [path(SHIELD_D, fill="p"),
                 circle(32, 26, 7, fill="c"),
                 polygon([(29, 32), (26, 46), (38, 46), (35, 32)], fill="c")])
    add("shield", "shield-fingerprint", "Biometric Shield",
        "Fingerprint arcs inside the shield.",
        lambda: [path(SHIELD_D, fill="p"),
                 path("M22 42 C22 22 42 22 42 42", stroke="c", sw=2.8),
                 path("M25 40 C25 26 39 26 39 40", stroke="c", sw=2.8),
                 path("M28 38 C28 30 36 30 36 38", stroke="c", sw=2.8)])
    add("shield", "shield-bell", "Alert Shield",
        "Shield with a notification bell.",
        lambda: [path(SHIELD_D, fill="p"),
                 path(BELL_D, fill="c"),
                 rect(22, 36, 20, 4, 2, fill="c"),
                 circle(32, 42, 3, fill="a", over=True, keep=True)])
    add("shield", "shield-slash", "Block Shield",
        "Denied / blocked. Diagonal slash across the shield.",
        lambda: [path(SHIELD_D, fill="p"),
                 line(18, 18, 46, 48, 6, stroke="c")])
    add("shield", "shield-vault", "Vault Dial",
        "Safe-dial vault. Cold-storage protection.",
        lambda: [circle(32, 32, 28, fill="p"),
                 circle(32, 32, 18, stroke="c", sw=3),
                 circle(32, 32, 6, fill="c")] + [
            line(32, 8, 32, 14, 3, stroke="c"), line(32, 50, 32, 56, 3, stroke="c"),
            line(8, 32, 14, 32, 3, stroke="c"), line(50, 32, 56, 32, 3, stroke="c")])
    add("shield", "shield-layers", "Layered Shield",
        "Defense in depth. Two offset shields.",
        lambda: [S("path", d=SHIELD_D, fill="a", keep=True, transform="translate(6 4) scale(0.92)"),
                 S("path", d=SHIELD_D, fill="p", transform="translate(-2 -2)")])
    add("shield", "shield-eye", "Watch Shield",
        "Always-on monitoring eye inside the shield.",
        lambda: [path(SHIELD_D, fill="p"),
                 path("M14 32 Q32 16 50 32 Q32 48 14 32 Z", fill="c"),
                 circle(32, 32, 6, fill="p", over=True, keep=True),
                 circle(34, 30, 2.2, fill="a", over=True, keep=True)])
    add("shield", "shield-alert", "Risk Triangle",
        "Risk warning sitting on a wallet.",
        lambda: [polygon([(32, 4), (60, 52), (4, 52)], fill="p"),
                 rect(29, 22, 6, 16, 2, fill="c"),
                 circle(32, 44, 3.4, fill="c")])
    add("shield", "shield-lock-wallet", "Locked Wallet",
        "Wallet body with a padlock instead of a clasp.",
        lambda: wallet(clasp=False, flap=True) + [
            path("M38 34 V30 A6 6 0 0 1 50 30 V34", stroke="c", sw=3.2),
            rect(36, 34, 16, 14, 3, fill="c"),
            circle(44, 40, 2.4, fill="a", over=True, keep=True)])
    add("shield", "shield-star", "Trusted Shield",
        "Star of trust cut into the shield.",
        lambda: [path(SHIELD_D, fill="p"),
                 polygon(star_points(32, 32, 14, 6), fill="c")])
    add("shield", "shield-pulse", "Live Protect",
        "Live monitoring pulse inside the shield.",
        lambda: [path(SHIELD_D, fill="p"),
                 polyline([(16, 32), (24, 32), (28, 22), (32, 42), (38, 28), (44, 32), (50, 32)],
                          3.6, stroke="c")])
    add("shield", "shield-cross", "Guard Cross",
        "Protective cross on the shield.",
        lambda: [path(SHIELD_D, fill="p"),
                 rect(28, 18, 8, 28, 2, fill="c"),
                 rect(18, 28, 28, 8, 2, fill="c")])
    add("shield", "shield-scan", "Wallet Scan",
        "Scan brackets around a wallet. Incoming threat check.",
        lambda: [path("M12 22 V14 H20", stroke="p", sw=4), path("M52 22 V14 H44", stroke="p", sw=4),
                 path("M12 42 V50 H20", stroke="p", sw=4), path("M52 42 V50 H44", stroke="p", sw=4),
                 rect(18, 22, 28, 20, 5, fill="p"),
                 circle(40, 32, 3, fill="c")])

    # ===== Intelligence (20) ===============================================
    add("intelligence", "intel-wallet-eye", "Wallet Eye",
        "All-seeing eye cut into the wallet.",
        lambda: wallet(clasp=False, flap=True) + [
            path("M14 38 Q32 22 50 38 Q32 54 14 38 Z", fill="c"),
            circle(32, 38, 5.5, fill="p", over=True, keep=True),
            circle(34, 36, 2, fill="a", over=True, keep=True)])
    add("intelligence", "intel-wallet-nodes", "Wallet Graph",
        "Connected node graph cut through the wallet.",
        lambda: wallet(clasp=False, flap=True) + [
            polyline([(16, 46), (26, 30), (38, 42), (50, 26)], 2.8, stroke="c"),
            circle(16, 46, 4, fill="c"), circle(26, 30, 4, fill="c"),
            circle(38, 42, 4.4, fill="a", over=True, keep=True),
            circle(50, 26, 4, fill="c")])
    add("intelligence", "intel-neural-w", "Neural W",
        "W drawn as a neural graph. Recommended Intelligence favicon.",
        lambda: [polyline(W_PTS, 4.2, stroke="p"),
                 line(8, 16, 32, 26, 2.4, stroke="p"),
                 line(32, 26, 56, 16, 2.4, stroke="p"),
                 line(18, 50, 46, 50, 2.4, stroke="p")] + [
            circle(x, y, 5.6, fill=("a" if i == 2 else "p"), keep=True)
            for i, (x, y) in enumerate(W_PTS)])
    add("intelligence", "intel-magnify", "Wallet Lens",
        "Wallet inspected with a magnifying glass.",
        lambda: wallet(clasp=False) + [
            circle(44, 42, 14, fill="c"),
            circle(42, 40, 8, stroke="a", sw=4.2, over=True, keep=True),
            line(48, 46, 56, 54, 5, stroke="a", over=True, keep=True)])
    add("intelligence", "intel-bulb", "Insight Wallet",
        "Lightbulb cut-out. Insight landing on a wallet.",
        lambda: wallet(clasp=False, flap=True) + [
            circle(32, 34, 9, fill="c"),
            rect(27, 43, 10, 4, 1.6, fill="c"),
            rect(28, 48, 8, 3.2, 1.4, fill="c")])
    add("intelligence", "intel-circuit-w", "Circuit W",
        "W trace with circuit pads at each vertex.",
        lambda: [polyline(W_PTS, 6, stroke="p")] + [
            circle(x, y, 5.2, fill="a", keep=True) for x, y in W_PTS] + [
            circle(x, y, 2.2, fill="c") for x, y in W_PTS])
    add("intelligence", "intel-radar", "Wallet Radar",
        "Radar disc with an accent sweep and target blip.",
        lambda: [circle(32, 32, 28, fill="p"),
                 circle(32, 32, 10, stroke="c", sw=2.2),
                 circle(32, 32, 19, stroke="c", sw=2.2),
                 line(32, 6, 32, 58, 2.2, stroke="c"),
                 line(6, 32, 58, 32, 2.2, stroke="c"),
                 path("M32 32 L60 32 A28 28 0 0 0 52 12 Z", fill="a", over=True, keep=True),
                 circle(46, 20, 3.4, fill="p", over=True, keep=True)])
    add("intelligence", "intel-tag", "Wallet Tag",
        "Entity label / tag. Wallet attribution.",
        lambda: [polygon([(8, 20), (42, 20), (58, 32), (42, 44), (8, 44)], fill="p"),
                 circle(20, 32, 5, fill="c"),
                 rect(28, 28, 12, 8, 2, fill="c")])
    add("intelligence", "intel-score", "Score Ring",
        "Open score ring with an accent needle.",
        lambda: [circle(32, 32, 26, stroke="p", sw=7),
                 path("M32 6 A26 26 0 0 1 54 20", stroke="a", sw=7, keep=True),
                 circle(32, 32, 8, fill="p"),
                 polygon([(32, 18), (36, 32), (32, 30), (28, 32)], fill="a", keep=True)])
    add("intelligence", "intel-brain", "Cluster Brain",
        "Insight cluster. Nodes grouped like a cortex.",
        lambda: [circle(24, 22, 12, fill="p"), circle(40, 22, 12, fill="p"),
                 circle(20, 36, 11, fill="p"), circle(44, 36, 11, fill="p"),
                 circle(32, 42, 12, fill="p"),
                 circle(32, 30, 5, fill="a", keep=True),
                 circle(22, 24, 3, fill="c"), circle(42, 24, 3, fill="c"),
                 circle(24, 40, 3, fill="c"), circle(40, 40, 3, fill="c")])
    add("intelligence", "intel-chip", "AI Chip",
        "On-chain intelligence chip.",
        lambda: [rect(16, 16, 32, 32, 6, fill="p")] + [
            rect(x, 10, 4, 8, 1, fill="p") for x in (20, 30, 40)] + [
            rect(x, 46, 4, 8, 1, fill="p") for x in (20, 30, 40)] + [
            rect(10, y, 8, 4, 1, fill="p") for y in (22, 30, 38)] + [
            rect(46, y, 8, 4, 1, fill="p") for y in (22, 30, 38)] + [
            circle(32, 32, 8, fill="c"), circle(32, 32, 3.4, fill="a", over=True, keep=True)])
    add("intelligence", "intel-target", "Target Wallet",
        "Crosshair on a wallet. Entity targeting.",
        lambda: [circle(32, 32, 26, fill="p"),
                 circle(32, 32, 16, stroke="c", sw=3),
                 circle(32, 32, 6, fill="c"),
                 line(32, 6, 32, 58, 2.6, stroke="c"),
                 line(6, 32, 58, 32, 2.6, stroke="c")])
    add("intelligence", "intel-constellation", "Constellation",
        "Labeled wallet cluster in a star map.",
        lambda: [polygon(star_points(18, 18, 7, 3), fill="p"),
                 polygon(star_points(48, 16, 6, 2.6), fill="p"),
                 polygon(star_points(14, 46, 6, 2.6), fill="p"),
                 polygon(star_points(50, 48, 7, 3), fill="p"),
                 polygon(star_points(32, 32, 10, 4.2), fill="a", keep=True),
                 line(18, 18, 32, 32, 2, stroke="p"),
                 line(48, 16, 32, 32, 2, stroke="p"),
                 line(14, 46, 32, 32, 2, stroke="p"),
                 line(50, 48, 32, 32, 2, stroke="p")])
    add("intelligence", "intel-id", "Identity Card",
        "Wallet identity card with portrait and stripes.",
        lambda: [rect(6, 16, 52, 32, 7, fill="p"),
                 circle(20, 32, 8, fill="c"),
                 rect(32, 24, 20, 4, 2, fill="c"),
                 rect(32, 32, 16, 4, 2, fill="c"),
                 rect(32, 40, 12, 4, 2, fill="a", over=True, keep=True)])
    add("intelligence", "intel-binary", "Data Wallet",
        "Ones and zeros streaming through a wallet.",
        lambda: wallet(clasp=False, flap=True) + [
            rect(16, 30, 6, 14, 1.4, fill="c"), circle(19, 48, 3, fill="c"),
            circle(32, 32, 3, fill="c"), rect(29, 38, 6, 14, 1.4, fill="c"),
            rect(42, 30, 6, 14, 1.4, fill="a", over=True, keep=True),
            circle(45, 48, 3, fill="a", over=True, keep=True)])
    add("intelligence", "intel-cluster", "Overlap Cluster",
        "Three overlapping wallets / sets.",
        lambda: [circle(24, 28, 16, fill="p"),
                 circle(40, 28, 16, fill="p"),
                 circle(32, 42, 16, fill="a", keep=True),
                 circle(32, 32, 5, fill="c")])
    add("intelligence", "intel-timeline", "Intel Timeline",
        "Event timeline of labeled wallet activity.",
        lambda: [line(8, 32, 56, 32, 4, stroke="p"),
                 circle(12, 32, 6, fill="p"),
                 circle(32, 32, 8, fill="a", keep=True),
                 circle(52, 32, 6, fill="p"),
                 rect(28, 8, 8, 14, 2, fill="a", keep=True),
                 rect(8, 42, 8, 10, 2, fill="p"),
                 rect(48, 42, 8, 10, 2, fill="p")])
    add("intelligence", "intel-fingerprint", "Print Scan",
        "Fingerprint as the whole mark. Unique wallet identity.",
        lambda: [path("M18 48 C18 18 46 18 46 48", stroke="p", sw=3.4),
                 path("M22 46 C22 24 42 24 42 46", stroke="p", sw=3.4),
                 path("M26 44 C26 28 38 28 38 44", stroke="p", sw=3.4),
                 path("M30 42 C30 32 34 32 34 42", stroke="a", sw=3.4, keep=True)])
    add("intelligence", "intel-spark", "Insight Spark",
        "Four-point spark of a new finding.",
        lambda: [polygon([(32, 4), (38, 26), (60, 32), (38, 38), (32, 60), (26, 38), (4, 32), (26, 26)],
                         fill="p"),
                 circle(32, 32, 8, fill="a", keep=True)])
    add("intelligence", "intel-funnel", "Attribution Funnel",
        "How labels concentrate. Three insight stages.",
        lambda: [polygon([(8, 8), (56, 8), (48, 22), (16, 22)], fill="p"),
                 polygon([(16, 24), (48, 24), (42, 36), (22, 36)], fill="p"),
                 polygon([(22, 38), (42, 38), (36, 56), (28, 56)], fill="a", keep=True)])

    # ===== Specialist (20) =================================================
    add("specialist", "spec-wrench", "Wallet Wrench",
        "Service wrench badged onto the wallet.",
        lambda: wallet(clasp=False) + [
            corner_badge(),
            circle(50, 50, 11, fill="a", over=True, keep=True),
            S("circle", cx=0, cy=-4.2, r=4, fill="p", over=True, keep=True,
              transform="translate(50 50) rotate(45)"),
            S("rect", x=-1.7, y=-4.2, width=3.4, height=12, rx=1.4, fill="p",
              over=True, keep=True, transform="translate(50 50) rotate(45)")])
    add("specialist", "spec-star", "Star Badge",
        "Wallet with a specialist star rating.",
        lambda: wallet(clasp=False) + [
            corner_badge(),
            circle(50, 50, 11.5, fill="a", over=True, keep=True),
            polygon(star_points(50, 50.4, 7.2, 3.2), fill="p", over=True, keep=True)])
    add("specialist", "spec-seal", "Certified Seal",
        "Rosette seal with check and ribbon. Recommended Specialist favicon.",
        lambda: [polygon([(20, 40), (30, 44), (28, 60), (16, 54)], fill="a", keep=True),
                 polygon([(44, 40), (34, 44), (36, 60), (48, 54)], fill="a", keep=True)]
        + [circle(x, y, 5.4, fill="p") for x, y in regular_polygon(32, 28, 19, 10, rot=0)]
        + [circle(32, 28, 19, fill="p"), check(33, 28, sw=5.2, scale=1.05)])
    add("specialist", "spec-check", "Verified Wallet",
        "Wallet with a specialist check cut-out.",
        lambda: wallet(flap=True) + [check(24, 38, sw=4.6)])
    add("specialist", "spec-headset", "Wallet Support",
        "Support headset framing a wallet card.",
        lambda: [path("M12 40 V28 A20 20 0 0 1 52 28 V40", stroke="p", sw=6),
                 rect(6, 34, 11, 16, 4, fill="a", keep=True),
                 rect(47, 34, 11, 16, 4, fill="a", keep=True),
                 rect(20, 40, 24, 16, 4, fill="p"),
                 circle(38, 48, 2.6, fill="c")])
    add("specialist", "spec-cap", "Wallet Scholar",
        "Wallet wearing a graduation cap. Expert knowledge.",
        lambda: [polygon([(32, 6), (58, 16), (32, 26), (6, 16)], fill="a", keep=True),
                 line(56, 16, 56, 28, 2.6, stroke="a", keep=True),
                 circle(56, 29, 2.4, fill="a", keep=True)] + wallet(x=8, y=28, w=48, h=28, rx=7))
    add("specialist", "spec-toolbox", "Toolbox Wallet",
        "Wallet drawn as a specialist toolbox.",
        lambda: [path("M22 24 V18 A10 10 0 0 1 42 18 V24", stroke="p", sw=5),
                 rect(8, 22, 48, 32, 7, fill="p"),
                 line(8, 34, 56, 34, 3, stroke="c"),
                 rect(26, 30, 12, 9, 2, fill="c")])
    add("specialist", "spec-rings", "Wallet Partner",
        "Two linked rings. Partnership and desk work.",
        lambda: wallet(clasp=False, flap=True) + [
            circle(24, 38, 9, stroke="c", sw=3.6),
            circle(40, 38, 9, stroke="c", sw=3.6),
            circle(32, 38, 3, fill="a", over=True, keep=True)])
    add("specialist", "spec-briefcase", "Briefcase",
        "Advisory briefcase. Desk and enterprise work.",
        lambda: [path("M24 20 V14 A8 8 0 0 1 40 14 V20", stroke="p", sw=5),
                 rect(8, 18, 48, 34, 7, fill="p"),
                 rect(26, 30, 12, 8, 2, fill="c")])
    add("specialist", "spec-medal", "Service Medal",
        "Medal with ribbon. Specialist recognition.",
        lambda: [polygon([(20, 8), (28, 8), (32, 28), (24, 28)], fill="a", keep=True),
                 polygon([(44, 8), (36, 8), (32, 28), (40, 28)], fill="a", keep=True),
                 circle(32, 40, 16, fill="p"),
                 polygon(star_points(32, 40, 9, 4), fill="c")])
    add("specialist", "spec-user", "Named Specialist",
        "Person mark for a dedicated specialist.",
        lambda: [circle(32, 22, 12, fill="p"),
                 path("M12 56 C12 40 20 34 32 34 C44 34 52 40 52 56", fill="p"),
                 circle(32, 22, 5, fill="c")])
    add("specialist", "spec-clipboard", "Runbook",
        "Clipboard of procedures. Specialist runbooks.",
        lambda: [rect(12, 10, 40, 48, 6, fill="p"),
                 rect(22, 6, 20, 10, 3, fill="a", keep=True),
                 line(20, 26, 44, 26, 3, stroke="c"),
                 line(20, 34, 44, 34, 3, stroke="c"),
                 line(20, 42, 36, 42, 3, stroke="c")])
    add("specialist", "spec-chat", "Advisor Chat",
        "Conversation bubble. Specialist desk chat.",
        lambda: [rect(8, 10, 48, 34, 10, fill="p"),
                 polygon([(20, 42), (16, 56), (32, 42)], fill="p"),
                 circle(22, 27, 3.6, fill="c"),
                 circle(32, 27, 3.6, fill="c"),
                 circle(42, 27, 3.6, fill="a", over=True, keep=True)])
    add("specialist", "spec-book", "Playbook",
        "Open book. Specialist knowledge base.",
        lambda: [path("M8 14 V50 C20 46 28 46 32 50 V14 C28 18 20 18 8 14 Z", fill="p"),
                 path("M56 14 V50 C44 46 36 46 32 50 V14 C36 18 44 18 56 14 Z", fill="p"),
                 line(32, 14, 32, 50, 3, stroke="c"),
                 circle(32, 32, 5, fill="a", over=True, keep=True)])
    add("specialist", "spec-lifebuoy", "Rescue",
        "Lifebuoy. Help when a wallet is in trouble.",
        lambda: [circle(32, 32, 26, fill="p"),
                 circle(32, 32, 12, fill="c"),
                 rect(29, 6, 6, 52, 0, fill="c"),
                 rect(6, 29, 52, 6, 0, fill="c"),
                 circle(32, 10, 4, fill="a", over=True, keep=True),
                 circle(32, 54, 4, fill="a", over=True, keep=True)])
    add("specialist", "spec-tools", "Crossed Tools",
        "Wrench and driver crossed. Hands-on service.",
        lambda: [S("rect", x=-2, y=-22, width=4, height=44, rx=2, fill="p",
                   transform="translate(32 32) rotate(-40)"),
                 S("circle", cx=0, cy=-20, r=7, fill="p",
                   transform="translate(32 32) rotate(-40)"),
                 S("rect", x=-2, y=-22, width=4, height=44, rx=2, fill="a", keep=True,
                   transform="translate(32 32) rotate(40)"),
                 S("rect", x=-5, y=14, width=10, height=6, rx=1, fill="a", keep=True,
                   transform="translate(32 32) rotate(40)")])
    add("specialist", "spec-calendar", "Booking",
        "Calendar for specialist sessions.",
        lambda: [rect(8, 12, 48, 44, 8, fill="p"),
                 rect(8, 12, 48, 12, 0, fill="a", keep=True),
                 rect(18, 8, 6, 10, 2, fill="p"),
                 rect(40, 8, 6, 10, 2, fill="p"),
                 circle(22, 36, 4, fill="c"),
                 circle(32, 36, 4, fill="c"),
                 circle(42, 36, 4, fill="a", over=True, keep=True)])
    add("specialist", "spec-people", "Desk Pair",
        "Two specialists. Team / desk plan mark.",
        lambda: [circle(22, 18, 9, fill="p"),
                 circle(42, 18, 9, fill="a", keep=True),
                 path("M6 56 C6 40 12 34 22 34 C32 34 36 40 36 56", fill="p"),
                 path("M28 56 C28 40 34 34 42 34 C52 34 58 40 58 56", fill="a", keep=True)])
    add("specialist", "spec-badge", "ID Badge",
        "Specialist identity badge with lanyard.",
        lambda: [rect(28, 4, 8, 10, 2, fill="a", keep=True),
                 rect(12, 14, 40, 44, 7, fill="p"),
                 circle(32, 32, 8, fill="c"),
                 rect(22, 44, 20, 6, 2, fill="c")])
    add("specialist", "spec-compass", "Guidance",
        "Compass. Specialist-led direction.",
        lambda: [circle(32, 32, 28, fill="p"),
                 polygon([(32, 8), (38, 32), (32, 36), (26, 32)], fill="c"),
                 polygon([(32, 56), (26, 32), (32, 28), (38, 32)], fill="a", over=True, keep=True),
                 circle(32, 32, 4, fill="p", over=True, keep=True)])

    slugs = [m["slug"] for m in MARKS]
    if len(MARKS) < 100:
        raise SystemExit(f"need >= 100 marks, got {len(MARKS)}")
    if len(slugs) != len(set(slugs)):
        dup = [s for s in slugs if slugs.count(s) > 1]
        raise SystemExit(f"duplicate slugs: {sorted(set(dup))}")
    missing = [v for v in HERO.values() if v not in slugs]
    if missing:
        raise SystemExit(f"HERO slug missing: {missing}")


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #

def attrs_to_str(attrs: dict) -> str:
    return " ".join(
        f'{k.replace("_", "-")}="{fmt(v)}"'
        for k, v in attrs.items() if v is not None
    )


def emit(shape: Shape, fill_color: str | None, stroke_color: str | None, sw: float) -> str:
    a = dict(shape.attrs)
    a["fill"] = fill_color or "none"
    if stroke_color and sw > 0:
        a["stroke"] = stroke_color
        a["stroke-width"] = sw
        a["stroke-linecap"] = "round"
        a["stroke-linejoin"] = "round"
    return f"<{shape.tag} {attrs_to_str(a)}/>"


def render_mark(shapes: list[Shape], style: str, line: dict, size=VB, uid="g") -> str:
    """Flaticon-style mark: coloured body, white (or tile-matching) counters, accent overlays."""
    p, sec, acc = line["primary"], line["secondary"], line["accent"]
    grad_id = f"{uid}-grad"
    clip_id = f"{uid}-clip"
    defs = (
        f'<linearGradient id="{grad_id}" x1="0" y1="0" x2="{VB}" y2="{VB}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{p}"/>'
        f'<stop offset="1" stop-color="{sec}"/></linearGradient>'
    )
    if style == "tile":
        defs += f'<clipPath id="{clip_id}"><rect width="{VB}" height="{VB}" rx="14"/></clipPath>'

    if style == "outline":
        parts = []
        for s in shapes:
            color = acc if (s.fill == "a" or s.stroke == "a") else p
            if s.keep and s.fill:
                parts.append(emit(s, acc if s.fill == "a" else p, None, 0))
            elif s.stroke and s.sw:
                parts.append(emit(s, None, color, max(2.4, min(s.sw, 4.2))))
            else:
                parts.append(emit(s, None, color, 3.2))
        body = "".join(parts)
        bg = ""
    else:
        if style == "tile":
            colors = {"p": PAPER, "a": acc, "c": f"url(#{grad_id})"}
            bg = f'<rect width="{VB}" height="{VB}" rx="14" fill="url(#{grad_id})"/>'
        elif style == "gradient":
            colors = {"p": f"url(#{grad_id})", "a": acc, "c": PAPER}
            bg = ""
        else:
            colors = {"p": p, "a": acc, "c": PAPER}
            bg = ""
        under, over = [], []
        for s in shapes:
            fill = colors.get(s.fill) if s.fill else None
            stroke = colors.get(s.stroke) if s.stroke else None
            el = emit(s, fill, stroke, s.sw)
            (over if s.over else under).append(el)
        body = "".join(under) + "".join(over)

    if style == "tile":
        inner = f'<g clip-path="url(#{clip_id})">{bg}{body}</g>'
    else:
        inner = bg + body
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB} {VB}" '
        f'width="{size}" height="{size}"><defs>{defs}</defs>{inner}</svg>'
    )


def render_lockup(line_id: str, theme: str) -> str:
    line = LINES[line_id]
    ink = PAPER if theme == "dark" else INK
    muted = MUTED_DARK if theme == "dark" else MUTED_LIGHT
    bg = INK if theme == "dark" else PAPER
    ops = line["accent"] if theme == "dark" else line["primary"]
    label = PRODUCT_LABEL[line_id]
    hero = MARKS_BY_SLUG[HERO[line_id]]
    mark = render_mark(hero["fn"](), "tile", line, size=64, uid=f"{line_id}-{theme}")
    nested = mark.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg x="16" y="16"', 1)
    W, H = 440, 96
    suffix = ""
    if line_id == "core":
        suffix = (f'<tspan font-weight="500" font-size="24" fill="{muted}" dx="6">.io</tspan>')
    text = (
        f'<text x="96" y="52" font-family="{FONT}" font-size="36" font-weight="800" '
        f'fill="{ink}" letter-spacing="-1.4">wallet'
        f'<tspan font-weight="600" fill="{ops}">ops</tspan>{suffix}</text>'
        f'<text x="98" y="76" font-family="{FONT}" font-size="13" font-weight="600" '
        f'letter-spacing="2.8" fill="{muted}">{label}</text>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
        f'<rect width="{W}" height="{H}" rx="16" fill="{bg}"/>{nested}{text}</svg>'
    )


def html_snippet(line: dict) -> str:
    return (
        f'<!-- {line["name"]} favicon pack -->\n'
        f'<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
        f'<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        f'<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        f'<link rel="manifest" href="/site.webmanifest">\n'
        f'<meta name="theme-color" content="{line["primary"]}">\n'
    )


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #

MARKS_BY_SLUG: dict[str, dict] = {}


def clean(d: Path):
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)


def main():
    register_marks()
    global MARKS_BY_SLUG
    MARKS_BY_SLUG = {m["slug"]: m for m in MARKS}

    try:
        import cairosvg
        from PIL import Image, ImageDraw, ImageFont
        raster = True
    except Exception:
        cairosvg = Image = ImageDraw = ImageFont = None
        raster = False
        print("cairosvg/pillow not available: writing SVG only")

    logos_dir = ROOT / "logos"
    fav_dir = ROOT / "favicons"
    lock_dir = ROOT / "lockups"
    prev_dir = ROOT / "preview"
    rec_dir = ROOT / "recommended"
    for d in (logos_dir, fav_dir, lock_dir, prev_dir, rec_dir):
        clean(d)

    manifest = {
        "brand": "walletops.io",
        "count": len(MARKS),
        "lines": LINES,
        "styles": STYLE_DESC,
        "hero": HERO,
        "marks": [],
        "lockups": [],
    }
    tile_pngs: dict[str, Path] = {}
    all_pngs: dict[tuple[str, str], bytes] = {}

    for m in MARKS:
        line = LINES[m["line"]]
        entry = {"slug": m["slug"], "line": m["line"], "title": m["title"], "desc": m["desc"], "files": {}}
        (logos_dir / m["line"]).mkdir(exist_ok=True)
        for style in STYLES:
            svg = render_mark(m["fn"](), style, line, size=256, uid=m["slug"])
            out = logos_dir / m["line"] / f'{m["slug"]}--{style}.svg'
            out.write_text(svg)
            entry["files"][style] = str(out.relative_to(ROOT))
            if raster:
                all_pngs[(m["slug"], style)] = cairosvg.svg2png(
                    bytestring=svg.encode(), output_width=256, output_height=256)

        fdir = fav_dir / m["slug"]
        fdir.mkdir()
        tile_svg = render_mark(m["fn"](), "tile", line, size=64, uid=m["slug"])
        (fdir / "favicon.svg").write_text(tile_svg)
        fav_files = {"svg": str((fdir / "favicon.svg").relative_to(ROOT))}
        if raster:
            for size in PNG_SIZES:
                p = fdir / PNG_NAMES[size]
                cairosvg.svg2png(bytestring=tile_svg.encode(), write_to=str(p),
                                 output_width=size, output_height=size)
                fav_files[str(size)] = str(p.relative_to(ROOT))
            Image.open(fdir / PNG_NAMES[48]).convert("RGBA").save(
                fdir / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
            fav_files["ico"] = str((fdir / "favicon.ico").relative_to(ROOT))
            tile_pngs[m["slug"]] = fdir / PNG_NAMES[192]
        (fdir / "site.webmanifest").write_text(json.dumps({
            "name": line["name"],
            "short_name": "WalletOps" if m["line"] == "core" else line["name"],
            "icons": [
                {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
            ],
            "theme_color": line["primary"],
            "background_color": "#ffffff",
            "display": "standalone",
        }, indent=2) + "\n")
        (fdir / "embed.html").write_text(html_snippet(line))
        entry["favicons"] = fav_files
        manifest["marks"].append(entry)

    for line_id in LINES:
        for theme in ("light", "dark"):
            svg = render_lockup(line_id, theme)
            out = lock_dir / f"{line_id}--{theme}.svg"
            out.write_text(svg)
            manifest["lockups"].append({"line": line_id, "theme": theme, "file": str(out.relative_to(ROOT))})
            if raster:
                cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out.with_suffix(".png")),
                                 output_width=880, output_height=192)

    # Drop-in packs for the five product sites
    for line_id, slug in HERO.items():
        dest = rec_dir / line_id
        src = fav_dir / slug
        shutil.copytree(src, dest)
        line = LINES[line_id]
        (dest / "README.txt").write_text(
            f"{line['name']}  ·  recommended favicon pack\n"
            f"Mark: {slug}\n"
            f"Copy every file in this folder to your website root, then paste embed.html "
            f"into <head>.\n"
        )

    if raster:
        build_contact_sheets(tile_pngs, all_pngs, prev_dir, Image, ImageDraw, ImageFont)

    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (ROOT / "index.html").write_text(build_gallery(manifest))
    write_readme(manifest)
    n = len(MARKS)
    print(f"{n} marks x {len(STYLES)} styles = {n * len(STYLES)} logo SVGs, "
          f"{n} favicon packs, {len(manifest['lockups'])} lockups")


def font(ImageFont, size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def build_contact_sheets(tile_pngs, all_pngs, prev_dir, Image, ImageDraw, ImageFont):
    fnt = font(ImageFont, 11)
    fnt_sm = font(ImageFont, 9)
    slugs = [m["slug"] for m in MARKS]
    cols, cell = 10, 128
    rows = math.ceil(len(slugs) / cols)
    sheet = Image.new("RGB", (cols * cell + 24, rows * (cell + 18) + 40), "#F8FAFC")
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 8), f"walletops.io  ·  {len(slugs)} unique marks  ·  tile / favicon style",
              fill="#0F172A", font=fnt)
    for i, slug in enumerate(slugs):
        im = Image.open(tile_pngs[slug]).convert("RGBA").resize((96, 96), Image.LANCZOS)
        x, y = 12 + (i % cols) * cell, 32 + (i // cols) * (cell + 18)
        sheet.paste(im, (x + 8, y), im)
        draw.text((x + 4, y + 100), f"{i+1:03d}", fill="#64748B", font=fnt_sm)
    sheet.save(prev_dir / "contact-sheet-tiles.png")

    # Per-line style sheets
    for line_id in LINES:
        line_slugs = [m["slug"] for m in MARKS if m["line"] == line_id]
        cols_s = 4
        rows_s = len(line_slugs)
        cell_s = 88
        sh = Image.new("RGB", (cols_s * cell_s + 200, rows_s * (cell_s + 8) + 48), "#FFFFFF")
        d = ImageDraw.Draw(sh)
        d.text((12, 10), f"{LINES[line_id]['name']}  ·  solid / gradient / outline / tile",
               fill="#0F172A", font=fnt)
        for r, slug in enumerate(line_slugs):
            d.text((12, 40 + r * (cell_s + 8) + 30), slug, fill="#334155", font=fnt_sm)
            for j, style in enumerate(STYLES):
                im = Image.open(io.BytesIO(all_pngs[(slug, style)])).convert("RGBA").resize((72, 72), Image.LANCZOS)
                x = 180 + j * cell_s
                y = 36 + r * (cell_s + 8)
                if style == "outline":
                    bg = Image.new("RGBA", (72, 72), (248, 250, 252, 255))
                    bg.alpha_composite(im)
                    sh.paste(bg, (x, y))
                else:
                    sh.paste(im, (x, y), im)
        sh.save(prev_dir / f"{line_id}-styles.png")

    # Heroes row
    heroes = list(HERO.items())
    hs = Image.new("RGB", (5 * 160 + 40, 200), "#F8FAFC")
    d = ImageDraw.Draw(hs)
    d.text((16, 8), "Recommended favicons for each product site", fill="#0F172A", font=fnt)
    for i, (line_id, slug) in enumerate(heroes):
        im = Image.open(tile_pngs[slug]).convert("RGBA").resize((112, 112), Image.LANCZOS)
        hs.paste(im, (24 + i * 160, 36), im)
        d.text((24 + i * 160, 156), LINES[line_id]["name"].replace("WalletOps ", "").replace("Wallet ", ""),
               fill="#334155", font=fnt_sm)
    hs.save(prev_dir / "recommended-heroes.png")


def build_gallery(manifest) -> str:
    lines = manifest["lines"]
    css = """
    :root{--ink:#0F172A;--muted:#64748B;--bg:#F8FAFC;--card:#fff;--line:#E2E8F0}
    *{box-sizing:border-box}body{margin:0;font-family:Inter,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink)}
    header{padding:40px 32px 16px;max-width:1320px;margin:auto}h1{margin:0 0 6px;font-size:34px;letter-spacing:-1px}
    h2{font-size:20px;margin:40px 0 12px}p.lead{color:var(--muted);margin:0 0 20px;max-width:820px;line-height:1.5}
    main{max-width:1320px;margin:auto;padding:0 32px 80px}
    .filters{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 20px}
    .filters button{border:1px solid var(--line);background:#fff;padding:8px 14px;border-radius:999px;cursor:pointer;font-weight:600;font-size:13px}
    .filters button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
    .swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
    .sw{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
    .sw .bar{height:56px}.sw .meta{padding:10px 12px;font-size:12px;color:var(--muted)}.sw b{color:var(--ink);display:block;font-size:14px}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
    .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px}
    .card .row{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:8px 0 12px}
    .card .row a{display:block;border-radius:10px;padding:8px;background:var(--bg);text-align:center}
    .card .row a.dark{background:var(--ink)}.card .row img{width:100%;aspect-ratio:1;display:block}
    .card h3{margin:0;font-size:15px}.card .line{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}
    .card p{font-size:13px;color:var(--muted);margin:6px 0 0;min-height:36px}
    .card .fav{display:flex;align-items:center;gap:10px;margin-top:10px;font-size:12px;color:var(--muted)}
    .card .fav a{color:#4F46E5;font-weight:600;text-decoration:none}
    .lockups{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:16px}
    .lockups img{width:100%;display:block;border-radius:16px;border:1px solid var(--line)}
    .heroes{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}
    .hero{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;text-align:center}
    .hero img{width:96px;height:96px}.hero b{display:block;margin-top:8px}.hero span{font-size:12px;color:var(--muted)}
    .hidden{display:none}code{background:#EEF2FF;padding:2px 6px;border-radius:6px;font-size:12px}
    pre{background:#0F172A;color:#E2E8F0;padding:16px;border-radius:12px;overflow:auto;font-size:12px}
    """
    js = """
    const btns=[...document.querySelectorAll('.filters button')];
    btns.forEach(b=>b.onclick=()=>{btns.forEach(x=>x.classList.remove('on'));b.classList.add('on');
      const f=b.dataset.f;document.querySelectorAll('.card').forEach(c=>c.classList.toggle('hidden',f!=='all'&&c.dataset.line!==f));});
    """
    sw = "".join(
        f'<div class="sw"><div class="bar" style="background:linear-gradient(135deg,{l["primary"]},{l["secondary"]})"></div>'
        f'<div class="meta"><b>{l["name"]}</b>{l["primary"]} · {l["secondary"]} · {l["accent"]}</div></div>'
        for l in lines.values())
    filters = '<button class="on" data-f="all">All 100</button>' + "".join(
        f'<button data-f="{k}">{v["name"]}</button>' for k, v in lines.items())
    heroes = []
    for line_id, slug in manifest["hero"].items():
        m = next(x for x in manifest["marks"] if x["slug"] == slug)
        heroes.append(
            f'<div class="hero"><img src="{m["files"]["tile"]}" alt="{m["title"]}">'
            f'<b>{lines[line_id]["name"]}</b><span>{m["title"]}<br><code>recommended/{line_id}/</code></span></div>')
    cards = []
    for i, m in enumerate(manifest["marks"], 1):
        f = m["files"]
        fav = m["favicons"]
        cards.append(
            f'<div class="card" data-line="{m["line"]}"><div class="line">#{i:03d} · {lines[m["line"]]["name"]}</div>'
            f'<h3>{m["title"]}</h3><div class="row">'
            f'<a href="{f["solid"]}" title="solid"><img src="{f["solid"]}" alt=""></a>'
            f'<a href="{f["gradient"]}" title="gradient"><img src="{f["gradient"]}" alt=""></a>'
            f'<a href="{f["outline"]}" title="outline"><img src="{f["outline"]}" alt=""></a>'
            f'<a class="dark" href="{f["tile"]}" title="tile"><img src="{f["tile"]}" alt=""></a></div>'
            f'<p>{m["desc"]}</p><div class="fav"><img src="{fav.get("16", fav["svg"])}" width="16" height="16" alt="">'
            f'<img src="{fav.get("32", fav["svg"])}" width="32" height="32" alt="">'
            f'<span>pack: <a href="favicons/{m["slug"]}/">favicons/{m["slug"]}/</a></span></div></div>')
    lockups = "".join(f'<img src="{lk["file"]}" alt="{lk["line"]} {lk["theme"]} lockup">' for lk in manifest["lockups"])
    n = len(manifest["marks"])
    snippet = (html_snippet(lines["core"])
               .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>walletops.io brand kit</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="recommended/core/favicon.svg" type="image/svg+xml">
<style>{css}</style></head><body>
<header><h1>walletops.io brand kit</h1>
<p class="lead">{n} unique logo marks × 4 styles = {n * 4} logo files, a full favicon pack for every mark
(SVG, 16/32/48 PNG, 180 apple-touch, 192/512 Android, favicon.ico, webmanifest), and wordmark lockups
for WalletOps, Analytics, Wallet Shield, Wallet Intelligence, and Wallet Specialist.
Generated by <code>generate.py</code>.</p></header>
<main>
<h2>Use on the website</h2>
<p class="lead">Copy <code>recommended/core/</code> to the site root and paste this into <code>&lt;head&gt;</code>.
Swap the folder for analytics, shield, intelligence, or specialist.</p>
<pre>{snippet}</pre>
<h2>Recommended marks</h2><div class="heroes">{''.join(heroes)}</div>
<h2>Palette</h2><div class="swatches">{sw}</div>
<h2>Wordmark lockups</h2><div class="lockups">{lockups}</div>
<h2>All {n} marks</h2><div class="filters">{filters}</div>
<div class="grid">{''.join(cards)}</div>
</main><script>{js}</script></body></html>
"""


def write_readme(manifest):
    n = len(manifest["marks"])
    heroes = "\n".join(
        f"- **{LINES[k]['name']}** — `{v}` → drop-in pack `recommended/{k}/`"
        for k, v in HERO.items())
    (ROOT / "README.md").write_text(f"""# walletops.io brand kit

Logo marks and favicon packs for **walletops.io** (Unstoppable domain) and the four product lines:

| Product | Colour | Recommended mark | Drop-in folder |
|---|---|---|---|
| WalletOps | indigo `#4F46E5` | W Monogram | `recommended/core/` |
| WalletOps Analytics | cyan `#0284C7` | W Bar Chart | `recommended/analytics/` |
| Wallet Shield | green `#059669` | Shield Check | `recommended/shield/` |
| Wallet Intelligence | violet `#7C3AED` | Neural W | `recommended/intelligence/` |
| Wallet Specialist | orange `#EA580C` | Certified Seal | `recommended/specialist/` |

**{n} unique marks × 4 styles = {n * 4} logo SVGs**, plus a favicon pack for every mark.

## Quick start (website favicon)

1. Copy every file in `recommended/core/` (or the matching product folder) to the website root.
2. Paste this into `<head>`:

```html
{html_snippet(LINES["core"]).rstrip()}
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

{heroes}

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
  logos/<line>/        <slug>--{{solid,gradient,outline,tile}}.svg
  favicons/<slug>/     full favicon pack
  recommended/<line>/  copy-paste pack for each product site
  lockups/             wordmark + mark, light and dark
  preview/             contact sheets
  manifest.json        machine-readable index
```
""")


if __name__ == "__main__":
    main()
