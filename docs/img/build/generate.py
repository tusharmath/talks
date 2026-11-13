#!/usr/bin/env python3
"""Generates the diagrams for the "How to Build a Software Factory" deck.

Run from anywhere: `python3 docs/img/build/generate.py`. Writes triggers.svg,
gates.svg and rollout.svg next to this file. SMIL only, so they animate
inside a plain <img>.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent

ORANGE = "#f97316"
CYAN = "#22d3ee"
RED = "#ef4444"
LIME = "#a3e635"
TEXT = "#d8d8d8"
MUTED = "#8a8a8a"
WIRE = "rgba(255,255,255,0.35)"
BOX = "#141414"
FONT = 'font-family="Space Mono, ui-monospace, Menlo, monospace"'

# Lucide icons (24x24 viewBox), inlined as path markup.
ICONS = {
    "message-square": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "bug": '<path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/><path d="M12 20v-9"/><path d="M6.53 9C4.6 8.8 3 7.1 3 5"/><path d="M6 13H2"/><path d="M3 21c0-2.1 1.7-3.9 3.8-4"/><path d="M20.97 5c0 2.1-1.6 3.8-3.5 4"/><path d="M22 13h-4"/><path d="M17.2 17c2.1.1 3.8 1.9 3.8 4"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "list-filter": '<path d="M3 6h18"/><path d="M7 12h10"/><path d="M10 18h4"/>',
    "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>',
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    "flask-conical": '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/>',
    "eye": '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
}


def icon(name, cx, cy, size=28, color=TEXT):
    """Lucide icon centred on (cx, cy)."""
    s = size / 24
    return (
        f'<g transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({s:.3f})" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{ICONS[name]}</g>'
    )


def text(x, y, s, size=16, color=TEXT, anchor="start", weight=700):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" letter-spacing="1" fill="{color}">{s}</text>'
    )


def f(v):
    return f"{max(0.0, min(1.0, v)):.4f}"


def poly_len(pts):
    return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def dist_to(pts, pred):
    """Distance along an orthogonal polyline until x first satisfies pred."""
    d = 0
    for a, b in zip(pts, pts[1:]):
        if a[1] == b[1] and pred(b[0]):
            # scan along horizontal segment
            step = 1 if b[0] > a[0] else -1
            x = a[0]
            while not pred(x):
                x += step
                d += 1
            return d
        d += abs(b[0] - a[0]) + abs(b[1] - a[1])
    return d


def path_d(pts):
    return "M" + " L".join(f"{x} {y}" for x, y in pts)


def svg(viewbox, comment, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" {FONT}>\n'
        f"  <!-- {comment} -->\n  " + "\n  ".join(body) + "\n</svg>\n"
    )


def item(pts, dur, start, speed, colors, size=20):
    """A work item riding an orthogonal path once per loop.

    colors: list of (distance, color); the item takes each colour once it has
    travelled that far.
    """
    length = poly_len(pts)
    travel = length / speed
    s, e = start / dur, (start + travel) / dur
    assert e < 1, (start, travel, dur)
    h = size / 2
    fills = ";".join(c for _, c in colors)
    fkeys = ";".join(["0"] + [f((start + d / speed) / dur) for d, _ in colors[1:]])
    return (
        f'<rect x="{-h}" y="{-h}" width="{size}" height="{size}" rx="3" fill="{colors[0][1]}" opacity="0">'
        f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{f(s)};{f(s + 0.001)};{f(e - 0.001)};{f(e)};1" dur="{dur}s" begin="-{dur / 2}s" repeatCount="indefinite"/>'
        f'<animate attributeName="fill" values="{fills}" keyTimes="{fkeys}" dur="{dur}s" begin="-{dur / 2}s" calcMode="discrete" repeatCount="indefinite"/>'
        f'<animateMotion path="{path_d(pts)}" keyPoints="0;0;1;1" keyTimes="0;{f(s)};{f(e)};1" calcMode="linear" dur="{dur}s" begin="-{dur / 2}s" repeatCount="indefinite"/>'
        f"</rect>"
    )


def flash(attr, base, hot, times, dur, width=0.04):
    """Discrete flash of `attr` to `hot` at each time in `times` (seconds)."""
    vals, keys = [base], ["0"]
    for t in sorted(times):
        a, b = t / dur, min(t / dur + width, 0.999)
        vals += [hot, base]
        keys += [f(a), f(b)]
    return (
        f'<animate attributeName="{attr}" values="{";".join(vals)}" keyTimes="{";".join(keys)}" '
        f'dur="{dur}s" begin="-{dur / 2}s" calcMode="discrete" repeatCount="indefinite"/>'
    )


# ---------------------------------------------------------------------------
# 1. Triggers: every source of work lands in one queue, triage turns it into
#    a spec, and only specs enter the factory.
# ---------------------------------------------------------------------------
def triggers():
    dur, speed = 8.0, 240
    sources = [("Issues", "message-square", 80), ("Bugs", "bug", 160),
               ("Alerts", "bell", 240), ("Goals", "target", 320)]
    ty, tx0, tx1 = 200, 500, 680  # triage box centre y, left, right
    fx0, fx1 = 800, 940
    body = []
    routes = []
    for label, ic, y in sources:
        pts = [(220, y), (380, y), (380, ty), (fx0 + 70, ty)]
        routes.append(pts)
        body.append(f'<path d="{path_d(pts[:3] + [(tx0, ty)])}" fill="none" stroke="{WIRE}" stroke-width="1.5" stroke-dasharray="4 5"/>')
    body.append(f'<path d="M{tx1} {ty} H{fx0}" fill="none" stroke="{CYAN}" stroke-opacity="0.6" stroke-width="1.5" stroke-dasharray="4 5"/>')
    body.append(f'<path d="M{fx0 - 10} {ty - 6} L{fx0} {ty} L{fx0 - 10} {ty + 6}" fill="none" stroke="{CYAN}" stroke-width="1.5"/>')
    body.append(f'<path d="M{tx0 - 10} {ty - 6} L{tx0} {ty} L{tx0 - 10} {ty + 6}" fill="none" stroke="{WIRE}" stroke-width="1.5"/>')

    # Items: 8 per loop, one source after another, spaced evenly.
    arrivals = []
    order = [0, 2, 1, 3, 2, 0, 3, 1]
    for k, src in enumerate(order):
        pts = routes[src]
        start = k * 0.5
        d_triage = dist_to(pts, lambda x: x >= (tx0 + tx1) / 2)
        r = item(pts, dur, start, speed, [(0, ORANGE), (d_triage, CYAN)])
        body.append(r)
        arrivals.append(start + dist_to(pts, lambda x: x >= tx0) / speed)

    for label, ic, y in sources:
        body.append(icon(ic, 60, y, 28, TEXT))
        body.append(text(92, y + 6, label, 17))

    # Triage box (drawn over items so they pass behind it).
    body.append(
        f'<rect x="{tx0}" y="{ty - 50}" width="{tx1 - tx0}" height="100" fill="{BOX}" stroke="{ORANGE}" stroke-width="2">'
        + flash("stroke-width", "2", "4", arrivals, dur, 0.03) + "</rect>"
    )
    body.append(icon("list-filter", tx0 + 46, ty, 30, ORANGE))
    body.append(text(tx0 + 72, ty + 6, "Triage", 18, "#f2f2f2"))
    body.append(text((tx0 + tx1) / 2, ty + 80, "One Queue", 14, MUTED, "middle"))
    body.append(text((tx1 + fx0) / 2, ty - 14, "Spec", 14, CYAN, "middle"))

    body.append(f'<rect x="{fx0}" y="{ty - 60}" width="{fx1 - fx0}" height="120" fill="{BOX}" stroke="{CYAN}" stroke-width="2"/>')
    body.append(icon("factory", (fx0 + fx1) / 2, ty - 14, 36, CYAN))
    body.append(text((fx0 + fx1) / 2, ty + 34, "Factory", 16, "#f2f2f2", "middle"))

    return svg(
        "0 0 1000 400",
        "Triggers: issues, bugs, alerts and goals (orange items) all land in one triage queue; "
        "triage turns each into a spec (cyan) and only specs enter the factory. Triage pulses on every arrival. SMIL only, 8s loop",
        body,
    )


# ---------------------------------------------------------------------------
# 2. Quality gates: agents push work through Tests, Review and Guardrails.
#    Anything that fails a gate turns red and loops back as rework; only
#    work that clears every gate ships.
# ---------------------------------------------------------------------------
def gates():
    dur, speed = 12.0, 230
    y = 230
    ax0, ax1 = 40, 180
    sx0, sx1 = 830, 960
    gx = [(330, "Tests", "flask-conical"), (510, "Review", "eye"), (690, "Guardrails", "shield-check")]
    gw = 84
    top = 90
    body = []

    # Rework loop over the top.
    body.append(f'<path d="M{gx[-1][0]} {y - 45} V{top} H{(ax0 + ax1) / 2} V{y - 40}" fill="none" stroke="{RED}" stroke-opacity="0.45" stroke-width="1.5" stroke-dasharray="4 5"/>')
    for g, _, _ in gx[:-1]:
        body.append(f'<path d="M{g} {y - 45} V{top}" fill="none" stroke="{RED}" stroke-opacity="0.45" stroke-width="1.5" stroke-dasharray="4 5"/>')
    mx = (ax0 + ax1) / 2
    body.append(f'<path d="M{mx - 6} {y - 50} L{mx} {y - 40} L{mx + 6} {y - 50}" fill="none" stroke="{RED}" stroke-opacity="0.8" stroke-width="1.5"/>')
    body.append(text((ax1 + gx[0][0]) / 2, top - 22, "Rework", 15, RED, "middle"))

    # Main line.
    body.append(f'<path d="M{ax1} {y} H{sx0}" fill="none" stroke="{WIRE}" stroke-width="1.5" stroke-dasharray="4 5"/>')
    body.append(f'<path d="M{sx0 - 10} {y - 6} L{sx0} {y} L{sx0 - 10} {y + 6}" fill="none" stroke="{CYAN}" stroke-width="1.5"/>')

    # Schedule: which gate (index) rejects each item, None = ships.
    # (start seconds, gate that rejects it or None when it ships). Long
    # rework trips start early so every trip ends inside the loop.
    plan = [(0.0, 2), (1.2, None), (2.4, 0), (3.6, None), (4.8, 1), (6.0, None), (7.2, None), (8.4, None)]
    rejects = {0: [], 1: [], 2: []}
    passes = {0: [], 1: [], 2: []}
    for start, fail in plan:
        if fail is None:
            pts = [(ax1 - 30, y), (sx0 + 60, y)]
            colors = [(0, ORANGE), (dist_to(pts, lambda x: x >= gx[-1][0]), CYAN)]
            gates_hit = range(3)
        else:
            g = gx[fail][0]
            pts = [(ax1 - 30, y), (g, y), (g, top), (mx, top), (mx, y - 50)]
            colors = [(0, ORANGE), (dist_to(pts, lambda x: x >= g), RED)]
            gates_hit = range(fail)
            rejects[fail].append(start + (g - (ax1 - 30) - gw / 2) / speed)
        for i in gates_hit:
            passes[i].append(start + (gx[i][0] - (ax1 - 30) - gw / 2) / speed)
        r = item(pts, dur, start, speed, colors)
        body.append(r)

    # Agents box.
    body.append(f'<rect x="{ax0}" y="{y - 40}" width="{ax1 - ax0}" height="80" fill="{BOX}" stroke="{ORANGE}" stroke-width="2"/>')
    body.append(icon("bot", ax0 + 36, y, 30, ORANGE))
    body.append(text(ax0 + 60, y + 6, "Agents", 17, "#f2f2f2"))

    # Gates.
    for i, (g, label, ic) in enumerate(gx):
        # Combined flashes: red on reject, lime on pass.
        events = sorted([(t, RED) for t in rejects[i]] + [(t, LIME) for t in passes[i]])
        vals, keys = [TEXT], ["0"]
        for t, c in events:
            vals += [c, TEXT]
            keys += [f(t / dur), f(t / dur + 0.035)]
        stroke = (
            f'<animate attributeName="stroke" values="{";".join(vals)}" keyTimes="{";".join(keys)}" '
            f'dur="{dur}s" begin="-{dur / 2}s" calcMode="discrete" repeatCount="indefinite"/>'
        )
        body.append(f'<rect x="{g - gw / 2}" y="{y - 45}" width="{gw}" height="90" fill="{BOX}" stroke="{TEXT}" stroke-width="2">{stroke}</rect>')
        body.append(icon(ic, g, y, 34, TEXT))
        body.append(text(g, y + 80, label, 16, TEXT, "middle"))

    # Ship box.
    body.append(f'<rect x="{sx0}" y="{y - 40}" width="{sx1 - sx0}" height="80" fill="{BOX}" stroke="{CYAN}" stroke-width="2"/>')
    body.append(icon("rocket", sx0 + 34, y, 28, CYAN))
    body.append(text(sx0 + 56, y + 6, "Ship", 17, "#f2f2f2"))

    return svg(
        "0 0 1000 340",
        "Quality gates: agents push work items (orange) through Tests, Review and Guardrails. A gate flashes lime as an item passes "
        "and red when it rejects one; rejected items turn red and loop back over the top to the agents as rework. Only items that clear "
        "every gate turn cyan and ship. SMIL only, 12s loop",
        body,
    )


# ---------------------------------------------------------------------------
# 3. Rollout: hand roles over one at a time; each bar fills to the share of
#    the role the factory takes on.
# ---------------------------------------------------------------------------
def rollout():
    dur = 10.0
    rows = [("QA", 100), ("Frontend", 100), ("Backend", 80), ("Platform", 40)]
    x0, w, h = 250, 560, 30
    body = []
    for i, (label, pct) in enumerate(rows):
        y = 50 + i * 80
        t0 = 0.4 + i * 1.3
        t1 = t0 + 1.1 * pct / 100
        fw = w * pct / 100
        body.append(text(x0 - 30, y + h / 2 + 7, label, 20, "#f2f2f2", "end"))
        body.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{h}" fill="rgba(255,255,255,0.08)"/>')
        body.append(
            f'<rect x="{x0}" y="{y}" width="0" height="{h}" fill="{ORANGE}">'
            f'<animate attributeName="width" values="0;0;{fw};{fw};0" keyTimes="0;{f(t0 / dur)};{f(t1 / dur)};0.94;1" dur="{dur}s" repeatCount="indefinite"/>'
            f"</rect>"
        )
        body.append(
            f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(t1 / dur)};{f(t1 / dur + 0.03)};0.94;1" dur="{dur}s" repeatCount="indefinite"/>'
            + icon("bot", x0 + fw - 22, y + h / 2, 20, BOX)
            + text(x0 + w + 24, y + h / 2 + 7, f"{pct}%", 20, ORANGE)
            + "</g>"
        )
    return svg(
        "0 0 1000 360",
        "Rollout: roles are handed to the factory one at a time. Each bar fills to the share the factory takes on "
        "(QA 100%, Frontend 100%, Backend 80%, Platform 40%) and its percentage appears when it lands. SMIL only, 10s loop",
        body,
    )


if __name__ == "__main__":
    for name, fn in [("triggers", triggers), ("gates", gates), ("rollout", rollout)]:
        (OUT / f"{name}.svg").write_text(fn())
        print("wrote", OUT / f"{name}.svg")
