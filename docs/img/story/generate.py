#!/usr/bin/env python3
"""Story diagrams for the "So you want to build a software factory?" deck.

Run: `python3 docs/img/story/generate.py`. Writes a01.svg ... a18.svg (agent
half) and f01.svg ... f13.svg (factory half) next to this file.

Design language follows the anatomy deck: dark boxes, Lucide icons, Space Mono
labels, coloured work items on a belt, orange for the thing you just built,
red for the problem it causes. SMIL only, so they animate inside a plain <img>.

Continuity: every slide redraws everything built so far (static) and animates
only what is new. Each half is one big world; a camera pans from the previous
slide's region to this one's, so consecutive slides read as one continuous shot.
In the agent half the user, the agent core and its context bar are pinned on
the left while the workbench on the right pans.
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ICONS = json.loads((OUT / "icons.json").read_text())

W, H = 1000, 300
ORANGE = "#f97316"
CYAN = "#22d3ee"
RED = "#ef4444"
LIME = "#a3e635"
YELLOW = "#eab308"
TEXT = "#d8d8d8"
MUTED = "#8a8a8a"
DIM = "#4a4a4a"
WIRE = "rgba(255,255,255,0.28)"
BOX = "#141414"
FONT = 'font-family="Space Mono, ui-monospace, Menlo, monospace"'
EASE = 'calcMode="spline" keySplines="0.4 0 0.2 1"'
SPL4 = ";".join(["0.4 0 0.2 1"] * 4)


# ---------------------------------------------------------------- primitives

def icon(name, cx=0, cy=0, size=24, color=TEXT):
    s = size / 24
    return (
        f'<g transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({s:.3f})" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{ICONS[name]}</g>'
    )


def text(x, y, s, size=13, color=MUTED, anchor="middle", weight=700, extra=""):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-weight="{weight}" letter-spacing="1" fill="{color}"{extra}>{s}</text>'
    )


def appear(begin, dur=0.25):
    """Child animation: hidden until `begin`, then fades in."""
    return (
        f'<animate attributeName="opacity" values="0;1" dur="{dur}s" begin="{begin}s" fill="freeze"/>'
    )


def hidden_until(inner, begin):
    if begin is None:
        return inner
    return f'<g opacity="0">{appear(begin)}{inner}</g>'


def pop(inner, x, y, begin=None, scale=1.0):
    """Place `inner` (drawn around 0,0) at x,y. With `begin`, it springs in."""
    if begin is None:
        return f'<g transform="translate({x} {y}) scale({scale})">{inner}</g>'
    return (
        f'<g transform="translate({x} {y}) scale({scale})"><g transform="scale(0)">'
        f'<animateTransform attributeName="transform" type="scale" values="0;1.22;0.92;1" '
        f'keyTimes="0;0.5;0.78;1" dur="0.65s" begin="{begin}s" fill="freeze" '
        f'calcMode="spline" keySplines="0.3 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1"/>'
        f'{inner}</g></g>'
    )


def shake(inner, begin, repeat=1):
    return (
        f'<g>{inner}<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;-5 1;5 -1;-4 2;4 0;-2 -1;0 0" dur="0.45s" begin="{begin}s" '
        f'repeatCount="{repeat}" additive="sum"/></g>'
    )


def node(name, label=None, size=56, color=TEXT, stroke=WIRE, red_at=None, glow=False, dashed=False):
    h = size / 2
    red = ""
    if red_at is not None:
        red = (
            f'<animate attributeName="stroke" to="{RED}" dur="0.2s" begin="{red_at}s" fill="freeze"/>'
        )
    halo = ""
    if glow:
        halo = (
            f'<rect x="{-h - 6}" y="{-h - 6}" width="{size + 12}" height="{size + 12}" rx="14" '
            f'fill="none" stroke="{ORANGE}" stroke-width="2" opacity="0.5">'
            f'<animate attributeName="opacity" values="0.6;0.1;0.6" dur="2s" repeatCount="indefinite"/></rect>'
        )
    dash = ' stroke-dasharray="5 5"' if dashed else ""
    out = (
        f'{halo}<rect x="{-h}" y="{-h}" width="{size}" height="{size}" rx="{size * 0.18:.0f}" '
        f'fill="{BOX}" stroke="{stroke}" stroke-width="2"{dash}>{red}</rect>'
        + icon(name, 0, 0, size * 0.5, color)
    )
    if label:
        out += text(0, h + 17, label, 12 if size < 50 else 13)
    return out


def alert(x, y, begin):
    """Red `!` badge that springs in and keeps pulsing."""
    inner = (
        f'<circle r="11" fill="none" stroke="{RED}" stroke-width="2">'
        f'<animate attributeName="r" values="11;24" dur="1.4s" begin="{begin + 0.4}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.9;0" dur="1.4s" begin="{begin + 0.4}s" repeatCount="indefinite"/></circle>'
        f'<circle r="11" fill="{RED}"/>'
        + text(0, 5, "!", 15, "#0b0b0b", weight=800)
    )
    return pop(inner, x, y, begin)


def flow(path, color=CYAN, dur=1.6, begin=0.0, n=3, size=9, stop=None, rotate=False):
    """`n` work items looping along `path`, staggered. Optional `stop` hides them."""
    out = []
    for k in range(n):
        b = begin + k * dur / n
        end = ""
        if stop is not None:
            end = f'<set attributeName="visibility" to="hidden" begin="{stop}s"/>'
        out.append(
            f'<rect x="{-size / 2}" y="{-size / 2}" width="{size}" height="{size}" rx="2" '
            f'fill="{color}" opacity="0"><set attributeName="opacity" to="0.95" begin="{b}s"/>'
            f'<animateMotion path="{path}" dur="{dur}s" begin="{b}s" repeatCount="indefinite"/>{end}</rect>'
        )
    return "".join(out)


def once(path, color=CYAN, dur=1.0, begin=0.0, size=10, fade_end=True, inner=None):
    """One item travelling `path` once."""
    body = inner or (
        f'<rect x="{-size / 2}" y="{-size / 2}" width="{size}" height="{size}" rx="2" fill="{color}"/>'
    )
    fade = ""
    if fade_end:
        fade = f'<animate attributeName="opacity" values="1;0" dur="0.3s" begin="{begin + dur}s" fill="freeze"/>'
    return (
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{begin}s"/>{fade}'
        f'<animateMotion path="{path}" dur="{dur}s" begin="{begin}s" fill="freeze" {EASE}/>{body}</g>'
    )


def counter(x, y, labels, begin, step, size=22, color=TEXT, final_color=None, anchor="middle"):
    """Text that ticks through `labels`, then holds the last one."""
    out = []
    n = len(labels)
    for i, lab in enumerate(labels):
        b = begin + i * step
        c = final_color if (final_color and i == n - 1) else color
        hide = "" if i == n - 1 else f'<set attributeName="opacity" to="0" begin="{b + step}s"/>'
        out.append(
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="{b}s"/>{hide}'
            + text(x, y, lab, size, c, anchor)
            + "</g>"
        )
    return "".join(out)


def bar(x, y, w, h, levels, times, colors=None, dur=None, repeat=False, label=None, rx=4):
    """Horizontal fill bar. `levels` are 0..1 at `times` (seconds)."""
    total = dur or times[-1] or 1
    kt = ";".join(f"{t / total:.4f}" for t in times)
    if times[0] != 0:
        times = [0] + times
        levels = [levels[0]] + levels
        kt = ";".join(f"{t / total:.4f}" for t in times)
        if colors:
            colors = [colors[0]] + colors
    if times[-1] < total:
        times = times + [total]
        levels = levels + [levels[-1]]
        kt = ";".join(f"{t / total:.4f}" for t in times)
        if colors:
            colors = colors + [colors[-1]]
    ws = ";".join(f"{max(0.0, l) * w:.1f}" for l in levels)
    rep = 'repeatCount="indefinite"' if repeat else 'fill="freeze"'
    col = ""
    if colors:
        col = (
            f'<animate attributeName="fill" values="{";".join(colors)}" keyTimes="{kt}" '
            f'dur="{total}s" calcMode="discrete" {rep}/>'
        )
    first = colors[0] if colors else ORANGE
    out = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#1e1e1e" stroke="{WIRE}" stroke-width="1.5"/>'
        f'<rect x="{x}" y="{y}" width="{levels[0] * w:.1f}" height="{h}" rx="{rx}" fill="{first}">'
        f'<animate attributeName="width" values="{ws}" keyTimes="{kt}" dur="{total}s" {rep}/>{col}</rect>'
    )
    if label:
        out += text(x + w / 2, y + h + 17, label, 12)
    return out


def static_bar(x, y, w, h, level, color, label=None):
    return bar(x, y, w, h, [level, level], [0, 1], [color, color], label=label)


def line(x1, y1, x2, y2, color=WIRE, width=2, dash=None, begin=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    el = f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>'
    return hidden_until(el, begin)


def draw_line(x1, y1, x2, y2, begin, color=WIRE, width=2, dur=0.5):
    """A wire that draws itself from (x1,y1) to (x2,y2)."""
    import math
    L = math.hypot(x2 - x1, y2 - y1)
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
        f'stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}">'
        f'<animate attributeName="stroke-dashoffset" values="{L:.0f};0" dur="{dur}s" begin="{begin}s" fill="freeze" {EASE}/></path>'
    )


def svg(body, comment):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" {FONT}>\n'
        f"  <!-- {comment} SMIL only. -->\n{body}\n</svg>\n"
    )


def camera(inner, x_from, x_to, offset=0, y_from=0, y_to=0):
    """World group panned so world x `x_to` sits at screen x `offset`."""
    a, b = offset - x_from, offset - x_to
    if (a, y_from) == (b, y_to):
        return f'<g transform="translate({b} {-y_to})">{inner}</g>'
    return (
        f'<g transform="translate({a} {-y_from})">'
        f'<animateTransform attributeName="transform" type="translate" values="{a} {-y_from};{b} {-y_to}" '
        f'dur="1s" begin="0s" fill="freeze" {EASE}/>{inner}</g>'
    )


# ------------------------------------------------------------- agent world

STAGE_X = 380  # screen x where the panning workbench starts
CORE = (220, 140)
USER = (62, 140)
R = {0: 0, 1: 640, 2: 1280, 3: 1920, 4: 2560}  # region -> world x

TOOLS = {  # world coords in region 0
    "write": ("file-pen", "write", 50, 60),
    "edit": ("pencil", "edit", 130, 60),
    "shell": ("terminal", "shell", 210, 60),
    "read": ("file-text", "read", 50, 165),
    "search": ("search", "search", 120, 165),
    "rag": ("database", "RAG", 190, 165),
    "fetch": ("globe", "fetch", 260, 165),
    "git": ("git-branch", "git", 330, 165),
    "browser": ("app-window", "browser", 400, 165),
}
REGISTRY = (330, 60)
TOOLSEARCH = (410, 60)
PLUG = (500, 55)


def screen(wx, wy, cam):
    return STAGE_X + wx - cam, wy


def mcp_cluster(begin=None, dim=False, lit=()):
    out = []
    for i in range(10):
        for j in range(10):
            x, y = 470 + j * 13, 100 + i * 13
            k = i * 10 + j
            on = (not dim) or k in lit
            col = CYAN if k in lit and dim else (MUTED if not dim else DIM)
            op = 1 if on else 0.35
            el = f'<rect x="{x}" y="{y}" width="9" height="9" rx="2" fill="{col}" opacity="{op}"/>'
            if begin is not None:
                b = begin + (i + j) * 0.04
                el = f'<g opacity="0">{appear(b, 0.15)}{el}</g>'
            out.append(el)
    return "".join(out)


def agent_core(i, begin=None, red_at=None, glow=False):
    if i == 0:
        inner = node("brain", "LLM", 72, ORANGE if begin is not None else TEXT, red_at=red_at)
    else:
        inner = node("bot", "agent", 72, TEXT, red_at=red_at, glow=glow)
    return pop(inner, *CORE, begin)


def ctx(levels, times, colors=None, repeat=False, dur=None):
    return bar(160, 222, 120, 12, levels, times, colors, dur=dur, repeat=repeat, label="context")


def agent_frame(i, cam_from, cam_to, world, pinned, ctx_svg, comment):
    """Compose one agent slide."""
    clip = (
        f'<defs><clipPath id="stage"><rect x="{STAGE_X - 24}" y="0" width="{W - STAGE_X + 24}" height="{H}"/></clipPath>'
        f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#0b0b0b" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#0b0b0b" stop-opacity="0"/></linearGradient></defs>'
    )
    body = clip
    body += f'<g clip-path="url(#stage)">{camera(world, cam_from, cam_to, STAGE_X)}</g>'
    body += line(258, CORE[1], STAGE_X - 30, CORE[1], WIRE, 2, "4 6") if i > 0 else ""
    body += pinned + ctx_svg
    return svg(body, comment)


def build_agent():
    persist = []  # (from_slide, fn(i) -> world svg) static once built
    files = []

    def world_static(i):
        return "".join(fn(i) for s, fn in persist if s < i)

    def tool(key, begin=None, red_at=None, dim=False):
        ic, lab, x, y = TOOLS[key]
        return pop(node(ic, lab, 44, DIM if dim else TEXT, red_at=red_at), x, y, begin)

    def core_to(wx, wy, cam):
        sx, sy = screen(wx, wy, cam)
        return f"M{CORE[0] + 36} {CORE[1]} L{STAGE_X - 30} {CORE[1]} L{sx} {sy}"

    def back_from(wx, wy, cam):
        sx, sy = screen(wx, wy, cam)
        return f"M{sx} {sy} L{STAGE_X - 30} {CORE[1]} L{CORE[0] + 36} {CORE[1]}"

    def user_static():
        return pop(node("user", "you", 52), *USER)

    scenes = []

    # 1 You call an LLM
    def s1():
        i, cam = 0, 0
        pinned = pop(node("user", "you", 52), *USER, 0.2) + agent_core(0, 0.5)
        code = (
            f'<rect x="-30" y="-16" width="60" height="32" rx="6" fill="{BOX}" stroke="{ORANGE}" stroke-width="2"/>'
            + text(0, 6, "&lt;/&gt;", 16, ORANGE)
        )
        pinned += once(f"M{USER[0] + 26} {USER[1]} L{CORE[0] - 36} {CORE[1]}", CYAN, 0.7, 1.2)
        # code drifts out to the empty workbench, then falls through the floor
        pinned += (
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="2.0s"/>'
            f'<animateMotion path="M{CORE[0] + 40} {CORE[1]} L620 140 L640 330" keyPoints="0;0.6;1" keyTimes="0;0.6;1" '
            f'dur="2.4s" begin="2.0s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1;0.6 0 1 1"/>'
            f'<animateTransform attributeName="transform" type="rotate" values="0;0;35" keyTimes="0;0.6;1" dur="2.4s" begin="2.0s" fill="freeze" additive="sum"/>'
            f"{code}</g>"
        )
        pinned += alert(640, 110, 3.6)
        world = f'<rect x="60" y="40" width="460" height="200" rx="14" fill="none" stroke="{DIM}" stroke-width="2" stroke-dasharray="6 8"/>' + text(290, 145, "no files", 14, DIM)
        persist.append((0, lambda i: f'<rect x="20" y="20" width="0" height="0"/>'))
        return agent_frame(i, cam, cam, world, pinned, ctx([0, 0.15], [0, 1.6], [ORANGE, ORANGE]),
                           "You call an LLM: prompt in, code out as text, nowhere to put it.")
    scenes.append(s1)

    def pinned_base(i, red_at=None, glow=False):
        return user_static() + agent_core(i, red_at=red_at, glow=glow)

    # 2 write tool
    def s2():
        i, cam = 1, 0
        world = world_static(i) + tool("write", 0.6, red_at=3.0)
        pinned = pinned_base(i)
        pinned += f'<g>{flow(core_to(50, 60, cam), CYAN, 1.2, 1.2, 2, stop=3.0)}</g>'
        pinned += once(core_to(50, 60, cam), RED, 0.9, 3.0)
        brk = text(0, 4, '{"path": "a.ts", "con', 12, RED)
        pinned += pop(f'<rect x="-92" y="-14" width="184" height="26" rx="5" fill="{BOX}" stroke="{RED}" stroke-width="1.5"/>{brk}', 520, 250, 3.3)
        pinned += alert(STAGE_X + 50 + 24, 36, 3.4)
        persist.append((1, lambda i: tool("write")))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.15, 0.25], [0, 2]),
                           "Agent gets a write tool; one tool call arrives as broken JSON.")
    scenes.append(s2)

    # file block used by repair / edit
    def file_block(x, y, begin, mode):
        out = f'<rect x="{x}" y="{y}" width="130" height="92" rx="6" fill="{BOX}" stroke="{WIRE}" stroke-width="1.5"/>'
        for k in range(7):
            ly = y + 12 + k * 11
            w = [90, 70, 100, 60, 96, 80, 50][k]
            if mode == "rewrite":
                out += (
                    f'<rect x="{x + 10}" y="{ly}" width="{w}" height="5" rx="2" fill="{DIM}">'
                    f'<animate attributeName="fill" values="{DIM};{ORANGE};{DIM}" dur="0.6s" begin="{begin + k * 0.12}s" repeatCount="indefinite"/></rect>'
                )
            else:
                col = LIME if k == 3 else DIM
                out += f'<rect x="{x + 10}" y="{ly}" width="{w}" height="5" rx="2" fill="{col}"/>'
        return hidden_until(out, begin)

    # 3 repair the JSON
    def s3():
        i, cam = 2, 0
        world = world_static(i)
        pinned = pinned_base(i)
        pinned += pop(node("wrench", "repair", 34, ORANGE), 318, 92, 0.4)
        pinned += line(318, 109, 318, CORE[1], WIRE, 1.5, "3 4", 0.4)
        # packets go in red, come out cyan at the repair step
        pinned += flow(f"M{CORE[0] + 36} {CORE[1]} L318 {CORE[1]}", RED, 0.8, 1.0, 2)
        pinned += flow(f"M318 {CORE[1]} L{STAGE_X - 30} {CORE[1]} L{STAGE_X + 50} 60", CYAN, 0.9, 1.4, 2)
        world += file_block(110, 120, 2.6, "rewrite") + text(175, 230, "2,000 lines rewritten", 12, MUTED)
        world += hidden_until(text(175, 230, "", 1), 2.6)
        pinned += alert(STAGE_X + 245, 120, 3.2)
        persist.append((2, lambda i: ""))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.25, 0.45], [0, 3]),
                           "A repair step fixes the JSON; every edit rewrites the whole file.")
    scenes.append(s3)

    # 4 edit tool
    def s4():
        i, cam = 3, 0
        world = world_static(i) + tool("edit", 0.5)
        world += file_block(110, 120, 1.2, "diff") + hidden_until(text(175, 230, "1 line changed", 12, LIME), 1.2)
        pinned = pinned_base(i) + flow(core_to(130, 60, cam), CYAN, 1.2, 1.1, 2)
        play = node("play", "run", 44, DIM, dashed=True)
        world += pop(play, 330, 160, 2.6) + alert(STAGE_X + 330 + 22, 136, 3.0)
        persist.append((3, lambda i: tool("edit")))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.45, 0.3], [0, 2]),
                           "An edit tool sends a one-line diff; nothing can run the code.")
    scenes.append(s4)

    # 5 shell
    def s5():
        i, cam = 4, 0
        world = world_static(i) + tool("shell", 0.5, red_at=2.8)
        pinned = pinned_base(i) + flow(core_to(210, 60, cam), CYAN, 1.1, 1.1, 2, stop=2.3)
        pinned += flow(back_from(210, 60, cam), ORANGE, 0.7, 2.3, 9, size=7)
        world += hidden_until(text(330, 120, "$ cat big.ts", 13, ORANGE, "start"), 2.1)
        world += counter(330, 142, ["1 line", "2,000 lines", "6,000 lines", "10,000 lines"], 2.4, 0.35, 13, MUTED, RED, "start")
        pinned += alert(STAGE_X + 210 + 24, 36, 3.0)
        persist.append((4, lambda i: tool("shell")))
        return agent_frame(i, cam, cam, world, pinned,
                           ctx([0.3, 0.3, 0.9], [0, 2.3, 3.6], [ORANGE, ORANGE, RED]),
                           "A shell does everything; one cat floods the context.")
    scenes.append(s5)

    # 6 more tools
    def s6():
        i, cam = 5, 0
        keys = ["read", "search", "rag", "fetch", "git", "browser"]
        world = world_static(i) + "".join(tool(k, 0.4 + n * 0.15) for n, k in enumerate(keys))
        pinned = pinned_base(i)
        for n, k in enumerate(keys[:3]):
            _, _, x, y = TOOLS[k]
            pinned += flow(core_to(x, y, cam), CYAN, 1.4, 1.5 + n * 0.3, 1)
        for n, lab in enumerate(["slack", "jira", "sentry"]):
            g = node("circle-help", lab, 40, DIM, stroke=RED, dashed=True)
            world += pop(g, 490 + n * 50, 250 - 12, 2.8 + n * 0.2)
        world += alert(STAGE_X + 590, 210, 3.6)
        persist.append((5, lambda i: "".join(tool(k) for k in keys)))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.3, 0.5], [0, 2.5]),
                           "Read, search, RAG, fetch, git, browser; every other service wants a tool too.")
    scenes.append(s6)

    # 7 MCP
    def s7():
        i, cam = 6, 0
        world = world_static(i) + pop(node("plug", "MCP", 44, ORANGE), *PLUG, 0.4)
        world += mcp_cluster(1.0)
        pinned = pinned_base(i, red_at=3.4)
        pinned += flow(back_from(535, 170, cam), MUTED, 0.9, 1.6, 8, size=6)
        pinned += alert(CORE[0] + 36, CORE[1] - 36, 3.6)
        persist.append((6, lambda i: pop(node("plug", "MCP", 44), *PLUG)
                        + mcp_cluster(dim=i >= 7, lit=(12, 47, 83))))
        return agent_frame(i, cam, cam, world, pinned,
                           ctx([0.5, 1.0], [1.4, 3.4], [ORANGE, RED]),
                           "MCP plugs in another 100 tools; their schemas fill the context.")
    scenes.append(s7)

    # 8 load tools dynamically
    def s8():
        i, cam = 7, 0
        world = world_static(i) + pop(node("library", "registry", 44, ORANGE), *REGISTRY, 0.4)
        pinned = pinned_base(i)
        q = node("circle-help", None, 30, YELLOW, stroke=YELLOW)
        pinned += pop(q, CORE[0], CORE[1] - 62, 2.6) + alert(CORE[0] + 36, CORE[1] - 36, 3.0)
        persist.append((7, lambda i: pop(node("library", "registry", 44), *REGISTRY)))
        return agent_frame(i, cam, cam, world, pinned,
                           ctx([1.0, 0.25], [0.8, 1.8], [RED, ORANGE]),
                           "Only the tools for this task load; the agent no longer knows what exists.")
    scenes.append(s8)

    # 9 tool search
    def s9():
        i, cam = 8, 0
        world = world_static(i) + pop(node("search", "find tool", 44, ORANGE), *TOOLSEARCH, 0.4)
        beam = (
            f'<rect x="462" y="94" width="26" height="140" rx="4" fill="{ORANGE}" opacity="0.18">'
            f'<animate attributeName="x" values="462;584;462" dur="2s" begin="1s" repeatCount="2"/></rect>'
        )
        world += hidden_until(beam, 1.0)
        pinned = pinned_base(i, red_at=4.2)
        pinned += flow(back_from(190, 165, cam), YELLOW, 0.5, 3.2, 12, size=6)
        world += hidden_until(text(190, 228, "50,000 lines", 13, RED), 3.2)
        pinned += alert(CORE[0] + 36, CORE[1] - 36, 4.2)
        persist.append((8, lambda i: pop(node("search", "find tool", 44), *TOOLSEARCH)))
        return agent_frame(i, cam, cam, world, pinned,
                           ctx([0.25, 0.3, 1.0], [0, 3.2, 4.2], [ORANGE, ORANGE, RED]),
                           "The agent searches for the tool it needs; one tool returns 50,000 lines.")
    scenes.append(s9)

    # 10 cap tool output
    def s10():
        i, cam = 9, 0
        world = world_static(i)
        pinned = pinned_base(i, red_at=5.6)
        pinned += pop(node("scissors", "cap", 34, ORANGE), 318, 92, 0.4)
        pinned += line(318, 109, 318, CORE[1], WIRE, 1.5, "3 4", 0.4)
        pinned += flow(f"M{STAGE_X + 50} 165 L{STAGE_X - 30} {CORE[1]} L330 {CORE[1]}", YELLOW, 0.6, 1.0, 6, size=6)
        pinned += flow(f"M310 {CORE[1]} L{CORE[0] + 36} {CORE[1]}", CYAN, 1.2, 1.3, 1, size=8)
        pinned += counter(CORE[0], 40, ["turn 1", "turn 20", "turn 60", "turn 140", "1 hour"], 1.4, 0.9, 13, MUTED, TEXT)
        pinned += alert(CORE[0] + 36, CORE[1] - 36, 5.6)
        persist.append((9, lambda i: ""))
        return agent_frame(i, cam, cam, world, pinned,
                           ctx([1.0, 0.1, 0.3, 0.55, 0.8, 1.0], [0, 0.8, 2.0, 3.2, 4.4, 5.6],
                               [RED, ORANGE, ORANGE, ORANGE, ORANGE, RED]),
                           "Tool output is cut short; turns pile up until the context is full again.")
    scenes.append(s10)

    # 11 compact (pans to the provider)
    def s11():
        i, cam_from, cam = 10, R[0], R[1]
        provider = pop(node("server", "provider", 56, TEXT, red_at=4.0), R[1] + 120, 140)
        world = world_static(i) + provider
        pinned = pinned_base(i)
        pinned += pop(node("fold-vertical", "compact", 30, ORANGE), 120, 228, 0.6)
        pinned += flow(core_to(R[1] + 120, 140, cam), CYAN, 1.0, 1.4, 3, stop=4.0)
        x1, y1 = screen(R[1] + 120, 140, cam)
        pinned += f'<g opacity="0"><set attributeName="opacity" to="1" begin="4.0s"/>{icon("x", x1 - 70, 140, 26, RED)}</g>'
        world += counter(R[1] + 120, 220, ["Tue 10:42", "Tue 10:43", "503"], 3.0, 0.5, 13, MUTED, RED)
        pinned += alert(x1 + 28, 112, 4.2)
        persist.append((10, lambda i: pop(node("server", "provider", 56), R[1] + 120, 140)
                        + pop(node("fold-vertical", "compact", 30), 0, -999)))
        return agent_frame(i, cam_from, cam, world, pinned,
                           ctx([1.0, 0.3, 0.75, 0.3, 0.75, 0.3], [0, 1.0, 2.0, 2.6, 3.4, 4.0],
                               [RED, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE]),
                           "Old turns are squeezed into summaries and the run goes on; the provider fails.")
    scenes.append(s11)

    def compact_pin():
        return pop(node("fold-vertical", "compact", 30), 120, 228)

    # 12 retries, limits and resume
    def s12():
        i, cam = 11, R[1]
        x0 = R[1]
        world = world_static(i)
        world += pop(node("refresh-cw", "retry", 44, ORANGE), x0 + 270, 55, 0.4)
        world += pop(node("gauge", "limits", 44, ORANGE), x0 + 270, 140, 0.6)
        world += pop(node("save", "resume", 44, ORANGE), x0 + 270, 225, 0.8)
        bill = f'<rect x="-80" y="-34" width="160" height="68" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2"><animate attributeName="stroke" to="{RED}" begin="5.2s" dur="0.2s" fill="freeze"/></rect>'
        world += pop(bill, x0 + 470, 140, 1.0)
        world += counter(x0 + 470, 135, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], 1.4, 0.55, 13, MUTED)
        world += counter(x0 + 470, 160, ["$12", "$80", "$190", "$340", "$560", "$790", "$1,000"], 1.4, 0.55, 20, TEXT, RED)
        pinned = pinned_base(i) + compact_pin()
        pinned += flow(core_to(x0 + 120, 140, cam), CYAN, 1.0, 1.0, 3)
        pinned += alert(screen(x0 + 550, 106, cam)[0], 106, 5.3)
        persist.append((11, lambda i: pop(node("refresh-cw", "retry", 44), x0 + 270, 55)
                        + pop(node("gauge", "limits", 44), x0 + 270, 140)
                        + pop(node("save", "resume", 44), x0 + 270, 225)))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.3, 0.75, 0.3], [0, 1.5, 3], repeat=True),
                           "Retries, limits and resume keep it running all week; the bill arrives.")
    scenes.append(s12)

    MODELS = [("DeepSeek", 60), ("Qwen", 140), ("Llama", 220)]

    def models(begin=None, sliders=False, sb=None):
        out = ""
        for n, (name, y) in enumerate(MODELS):
            b = None if begin is None else begin + n * 0.2
            out += pop(node("cpu", name, 44, TEXT), R[2] + 70, y, b)
            if sliders:
                out += pop(node("sliders-horizontal", None, 30, ORANGE if sb is not None else TEXT),
                           R[2] + 150, y, None if sb is None else sb + n * 0.2)
        return out

    # 13 open-weight models
    def s13():
        i, cam_from, cam = 12, R[1], R[2]
        x0 = R[2]
        world = world_static(i) + models(1.0)
        for n, (_, y) in enumerate(MODELS):
            world += pop(node("wrench", None, 30, DIM), x0 + 230, y - 18, 1.4)
            world += pop(node("wrench", None, 30, DIM), x0 + 230, y + 18, 1.4)
            path = f"M{x0 + 92} {y} L{x0 + 214} {y + 18}"
            world += flow(path, RED if n != 1 else YELLOW, 1.1, 2.2 + n * 0.25, 1)
            world += hidden_until(text(x0 + 330, y + 5, ['{"pth": 4}', '{"file": null}', '{"x": "?"}'][n], 13, RED, "start"), 3.0 + n * 0.2)
        world += alert(x0 + 470, 30, 3.6)
        pinned = pinned_base(i) + compact_pin()
        persist.append((12, lambda i: models(sliders=i >= 14)))
        return agent_frame(i, cam_from, cam, world, pinned, ctx([0.3, 0.3], [0, 1]),
                           "Open-weight models plug in cheaply; they call the wrong tool with made-up arguments.")
    scenes.append(s13)

    COLS = ["tool", "args", "tests"]

    def board(cell_colors, begin=None, flips=None):
        x0 = R[2]
        out = ""
        for c, lab in enumerate(COLS):
            out += text(x0 + 300 + c * 80, 22, lab, 12)
        for r, (_, y) in enumerate(MODELS):
            for c in range(3):
                col = cell_colors[r][c]
                anim = ""
                if flips and (r, c) in flips:
                    vals = flips[(r, c)]
                    anim = f'<animate attributeName="fill" values="{vals}" dur="3s" begin="1.6s" calcMode="discrete" repeatCount="indefinite"/>'
                el = f'<rect x="{x0 + 272 + c * 80}" y="{y - 16}" width="56" height="32" rx="6" fill="{col}" opacity="0.9">{anim}</rect>'
                if begin is not None:
                    el = hidden_until(el, begin + 0.15 * (r * 3 + c))
                out += el
        return out

    FAILS = [[RED, LIME, LIME], [LIME, RED, LIME], [LIME, LIME, RED]]

    # 14 evals
    def s14():
        i, cam = 13, R[2]
        world = world_static(i) + board([[DIM] * 3] * 3) + board(FAILS, 1.0)
        world += alert(R[2] + 560, 30, 3.0)
        pinned = pinned_base(i) + compact_pin()
        persist.append((13, lambda i: board(FAILS if i < 15 else [[LIME] * 3] * 3) if i != 14 else ""))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.3, 0.3], [0, 1]),
                           "Evals from real tasks score every model; each fails in a different column.")
    scenes.append(s14)

    # 15 tune per model
    def s15():
        i, cam = 14, R[2]
        world = world_static(i) + models(sliders=True, sb=0.4)
        flips = {(0, 0): f"{LIME};{RED}", (1, 1): f"{RED};{LIME}", (2, 2): f"{LIME};{RED}", (1, 0): f"{LIME};{RED}"}
        world += board(FAILS, None, flips)
        world += alert(R[2] + 560, 30, 2.0)
        pinned = pinned_base(i) + compact_pin()
        persist.append((14, lambda i: ""))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.3, 0.3], [0, 1]),
                           "Each model gets its own prompts and tool descriptions; fixing one breaks another.")
    scenes.append(s15)

    def gate(begin=None):
        return pop(node("shield-check", "evals", 48, LIME if begin is not None else TEXT), R[3] + 90, 110, begin)

    # 16 run the evals on every change
    def s16():
        i, cam_from, cam = 15, R[2], R[3]
        x0 = R[3]
        world = world_static(i) + gate(1.0)
        for n in range(3):
            world += flow(f"M{x0 - 120} 110 L{x0 + 66} 110", ORANGE, 1.2, 1.4 + n * 0.4, 1)
            world += flow(f"M{x0 + 114} 110 L{x0 + 260} 110", LIME, 1.2, 2.0 + n * 0.4, 1)
        world += hidden_until(text(x0 + 300, 115, "all green", 14, LIME, "start"), 2.4)
        world += pop(node("hourglass", None, 32, YELLOW, stroke=YELLOW), x0 + 60, 235, 2.6)
        world += bar(x0 + 100, 228, 460, 14, [0, 0.12, 0.2], [2.8, 6, 12]) + hidden_until(text(x0 + 330, 266, "big task: step 3 of 400", 12), 2.8)
        world += alert(x0 + 590, 222, 4.0)
        pinned = pinned_base(i) + compact_pin()
        persist.append((15, lambda i: gate()))
        return agent_frame(i, cam_from, cam, world, pinned, ctx([0.3, 0.3], [0, 1]),
                           "Every prompt, tool description and model change runs the evals; a big task still crawls.")
    scenes.append(s16)

    def swarm(begin=None, done=False):
        out = ""
        x0 = R[3]
        for r in range(8):
            for c in range(25):
                x, y = x0 + 220 + c * 14, 30 + r * 16
                col = CYAN if done else ORANGE
                el = f'<rect x="{x}" y="{y}" width="9" height="9" rx="2" fill="{col}" opacity="0.85"/>'
                if begin is not None:
                    el = f'<g opacity="0">{appear(begin + (r + c) * 0.025, 0.12)}{el}</g>'
                out += el
        return out

    # 17 sub-agents
    def s17():
        i, cam = 16, R[3]
        x0 = R[3]
        world = world_static(i) + swarm(0.8)
        world += pop(node("hourglass", None, 32, YELLOW, stroke=YELLOW), x0 + 60, 235)
        world += bar(x0 + 100, 228, 460, 14, [0.2, 0.2, 1.0], [0, 1.4, 2.6], [ORANGE, ORANGE, LIME]) + text(x0 + 330, 266, "400 sub-agents, in the background", 12)
        pinned = pinned_base(i, red_at=3.6)
        pinned += flow(f"M{USER[0] + 26} {USER[1]} L{CORE[0] - 36} {CORE[1]}", CYAN, 1.0, 1.0, 2)
        teams = [(CORE[0] - 80, 40, ORANGE), (CORE[0], 28, CYAN), (CORE[0] + 80, 40, YELLOW)]
        for n, (x, y, c) in enumerate(teams):
            pinned += pop(node("users", None, 32, c, stroke=c), x, y, 3.0 + n * 0.15)
            pinned += draw_line(x, y + 16, CORE[0], CORE[1] - 36, 3.1 + n * 0.15, c, 2)
        pinned = shake(pinned, 3.6, 3)
        pinned += alert(CORE[0] + 36, CORE[1] - 36, 3.8)
        persist.append((16, lambda i: swarm(done=True)))
        return agent_frame(i, cam, cam, world, pinned, ctx([0.3, 0.3], [0, 1]),
                           "400 sub-agents run in the background while you keep talking; every team pulls a different way.")
    scenes.append(s17)

    # 18 hooks, permissions, AGENTS.md, skills
    def s18():
        i, cam_from, cam = 17, R[3], R[4]
        x0 = R[4]
        ext = [("webhook", "hooks"), ("shield", "permissions"), ("file-text", "AGENTS.md"), ("book-open", "skills")]
        cols = [ORANGE, CYAN, YELLOW, LIME]
        world = world_static(i)
        for n, (ic, lab) in enumerate(ext):
            x = x0 + 80 + n * 140
            world += draw_line(x0 - 60, 140, x, 140, 1.0 + n * 0.2, WIRE, 2)
            world += pop(node(ic, lab, 56, cols[n], stroke=cols[n]), x, 140, 1.2 + n * 0.2)
            world += pop(node("users", None, 28, cols[n]), x, 60, 2.2 + n * 0.15)
            world += draw_line(x, 74, x, 112, 2.3 + n * 0.15, cols[n], 1.5)
        pinned = user_static() + agent_core(i, glow=True) + compact_pin()
        return agent_frame(i, cam_from, cam, world, pinned, ctx([0.3, 0.3], [0, 1]),
                           "Hooks, permissions, AGENTS.md and skills: each team plugs in its own rules.")
    scenes.append(s18)

    for n, fn in enumerate(scenes, 1):
        p = OUT / f"a{n:02d}.svg"
        p.write_text(fn())
        files.append(p.name)
    return files


# ------------------------------------------------------------ factory world

LANES = [("control", 50), ("management", 150), ("machines", 248)]
F = {0: 0, 1: 1000, 2: 2000, 3: 3000}


def lanes(width=4200):
    out = ""
    for name, y in LANES:
        out += f'<path d="M0 {y + 42} H{width}" stroke="rgba(255,255,255,0.08)" stroke-width="1.5"/>' if y < 240 else ""
    return out


def lane_labels():
    return "".join(
        f'<g transform="translate(14 {y + 4}) rotate(-90)">{text(0, 0, n, 10, DIM)}</g>' for n, y in LANES
    )


def card(color=CYAN, w=14):
    return f'<rect x="{-w / 2}" y="{-w / 2}" width="{w}" height="{w}" rx="3" fill="{color}"/>'


def build_factory():
    persist = []
    files = []

    def static(i):
        return "".join(fn(i) for s, fn in persist if s < i)

    def frame(i, cam_from, cam_to, world, comment, overlay=""):
        body = camera(lanes() + world, cam_from, cam_to) + lane_labels() + overlay
        return svg(body, comment)

    scenes = []

    LAPTOP = (110, 248)
    CLOCK = (110, 150)
    SERVER = (290, 248)
    YOU = (110, 50)
    CP = (290, 50)
    TRIG = [("slack", "slack", 470), ("ticket", "tickets", 550), ("bell", "alerts", 630), ("rocket", "deploys", 710)]
    PRS = (840, 248)
    FLASK = (840, 150)

    def laptop(closed=False):
        return node("laptop", "laptop", 56, DIM if closed else TEXT)

    # 1 schedule agents
    def f1():
        i = 0
        world = pop(laptop(), *LAPTOP, 0.2)
        world += pop(node("bot", None, 26, ORANGE, stroke="none"), LAPTOP[0], LAPTOP[1] - 52, 0.5)
        world += pop(node("clock", "schedule", 52, ORANGE), *CLOCK, 0.8)
        # lid closes: laptop dims
        world += f'<g opacity="0"><set attributeName="opacity" to="1" begin="2.4s"/>{pop(laptop(True), *LAPTOP)}{pop(node("moon", None, 26, MUTED, stroke="none"), LAPTOP[0] + 50, LAPTOP[1] - 30)}</g>'
        world += flow(f"M{CLOCK[0]} {CLOCK[1] + 26} L{LAPTOP[0]} {LAPTOP[1] - 28}", CYAN, 0.9, 1.2, 1, stop=2.4)
        world += once(f"M{CLOCK[0]} {CLOCK[1] + 26} L{LAPTOP[0]} {LAPTOP[1] - 34}", RED, 0.8, 3.0)
        world += hidden_until(text(LAPTOP[0] + 70, LAPTOP[1] + 5, "02:00 skipped", 13, RED, "start"), 3.8)
        world += alert(LAPTOP[0] + 28, LAPTOP[1] - 28, 3.8)
        persist.append((0, lambda i: pop(laptop(True), *LAPTOP) + pop(node("clock", "schedule", 52), *CLOCK)))
        return frame(i, 0, 0, world, "Agents scheduled on your laptop; the lid closes and the nightly run never happens.")
    scenes.append(f1)

    def server(label="cloud"):
        return node("server", label, 56, TEXT)

    # 2 cloud
    def f2():
        i = 1
        world = static(i)
        world += pop(node("cloud", None, 34, CYAN, stroke="none"), SERVER[0], SERVER[1] - 62, 0.3)
        world += pop(server(), *SERVER, 0.5)
        world += once(f"M{LAPTOP[0]} {LAPTOP[1] - 30} Q200 140 {SERVER[0]} {SERVER[1] - 6}",
                      inner=node("bot", None, 24, ORANGE, stroke=ORANGE), dur=1.2, begin=0.9)
        world += pop(node("bot", None, 22, ORANGE, stroke="none"), SERVER[0] + 40, SERVER[1] - 30, 2.1)
        world += flow(f"M{CLOCK[0] + 26} {CLOCK[1]} L{SERVER[0]} {SERVER[1] - 28}", LIME, 1.1, 2.2, 2)
        world += pop(node("user", "you", 44), *YOU, 2.8)
        world += draw_line(YOU[0] + 6, YOU[1] + 24, SERVER[0] - 20, SERVER[1] - 30, 3.0, MUTED, 1.5)
        world += hidden_until(text(205, 120, "ssh", 12, MUTED), 3.4)
        world += alert(YOU[0] + 22, YOU[1] - 22, 3.8)
        persist.append((1, lambda i: pop(server(), *SERVER) + pop(node("bot", None, 22, ORANGE, stroke="none"), SERVER[0] + 40, SERVER[1] - 30)))
        return frame(i, 0, 0, world, "The agent moves to an always-on cloud machine; you can only reach it over SSH.")
    scenes.append(f2)

    CLIENTS = [("monitor", 420), ("smartphone", 490), ("laptop", 560)]

    def cp(begin=None):
        bx = f'<rect x="-70" y="-22" width="140" height="44" rx="10" fill="{BOX}" stroke="{ORANGE if begin is not None else WIRE}" stroke-width="2"/>' + text(0, 5, "control plane", 12, TEXT)
        out = pop(bx, *CP, begin)
        out += pop(node("user", "you", 44), *YOU)
        for n, (ic, x) in enumerate(CLIENTS):
            b = None if begin is None else begin + 0.4 + n * 0.15
            out += pop(node(ic, None, 36, TEXT), x, CP[1], b)
        return out

    # 3 control plane
    def f3():
        i = 2
        world = static(i) + cp(0.5)
        world += draw_line(CP[0], CP[1] + 22, SERVER[0], SERVER[1] - 28, 1.0, WIRE, 2)
        for n, (_, x) in enumerate(CLIENTS):
            world += flow(f"M{x} {CP[1] + 18} L{x} {CP[1] + 30} L{CP[0] + 70} {CP[1] + 30} L{CP[0] + 70} {CP[1]}", CYAN, 1.4, 1.6 + n * 0.3, 1, size=7)
        world += flow(f"M{CP[0]} {CP[1] + 22} L{SERVER[0]} {SERVER[1] - 28}", CYAN, 1.0, 2.0, 2, stop=3.4)
        world += pop(node("moon", None, 26, MUTED, stroke="none"), SERVER[0] - 50, SERVER[1] - 30, 3.4)
        world += hidden_until(text(SERVER[0] + 50, SERVER[1] + 30, "waiting for input", 12, MUTED, "start"), 3.5)
        world += alert(SERVER[0] + 28, SERVER[1] - 28, 3.8)
        persist.append((2, lambda i: cp() + line(CP[0], CP[1] + 22, SERVER[0], SERVER[1] - 28)))
        return frame(i, 0, 0, world, "A control plane lets any screen drive the agent, even your phone; it only moves when someone types.")
    scenes.append(f3)

    def triggers(begin=None):
        out = ""
        for n, (ic, lab, x) in enumerate(TRIG):
            b = None if begin is None else begin + n * 0.15
            out += pop(node(ic, lab, 44, TEXT if begin is None else ORANGE), x, 150, b)
        return out

    # 4 triggers
    def f4():
        i = 3
        world = static(i) + triggers(0.4)
        for n, (_, _, x) in enumerate(TRIG):
            world += flow(f"M{x} 172 L{x} 200 L{SERVER[0] + 28} 200 L{SERVER[0] + 28} {SERVER[1] - 20}", YELLOW, 1.3, 1.2 + n * 0.25, 2, size=8)
        world += flow(f"M{SERVER[0] + 28} {SERVER[1]} L{PRS[0] - 30} {PRS[1]}", ORANGE, 0.7, 1.8, 4, size=8)
        world += pop(node("git-pull-request", None, 56, TEXT, red_at=4.2), *PRS, 1.6)
        world += counter(PRS[0] + 40, PRS[1] + 6, ["3", "18", "41", "67", "100"], 1.9, 0.55, 18, TEXT, RED, "start")
        world += hidden_until(text(PRS[0] + 40, PRS[1] + 26, "untested PRs", 12, MUTED, "start"), 1.9)
        world += alert(PRS[0] + 28, PRS[1] - 28, 4.4)
        persist.append((3, lambda i: triggers() + pop(node("git-pull-request", "PRs", 56), *PRS)))
        return frame(i, 0, 0, world, "Slack, tickets, alerts and failed deploys trigger the agent; 100 untested PRs by morning.")
    scenes.append(f4)

    # 5 verification agents
    def f5():
        i = 4
        world = static(i)
        world += pop(node("flask-conical", "verify", 48, LIME, stroke=LIME), *FLASK, 0.4)
        world += draw_line(FLASK[0], FLASK[1] + 24, PRS[0], PRS[1] - 28, 0.7, LIME, 2)
        world += pop(node("video", None, 30, CYAN), FLASK[0] + 60, FLASK[1] - 22, 1.4)
        world += pop(node("files", None, 30, CYAN), FLASK[0] + 60, FLASK[1] + 18, 1.6)
        world += hidden_until(text(FLASK[0] + 82, FLASK[1] + 52, "artifacts", 11, MUTED, "start"), 1.6)
        world += flow(f"M{PRS[0]} {PRS[1] - 28} L{FLASK[0]} {FLASK[1] + 24}", LIME, 1.0, 1.0, 2)
        # a plain question turned into a PR
        q = node("message-square", None, 32, YELLOW, stroke=YELLOW)
        world += once(f"M470 172 L470 200 L{SERVER[0] + 28} 200 L{SERVER[0] + 28} {SERVER[1] - 20} L{PRS[0] - 30} {PRS[1]}",
                      dur=2.0, begin=2.4, inner=q, fade_end=False)
        world += hidden_until(text(PRS[0] - 40, PRS[1] - 40, "a question", 12, YELLOW, "end"), 4.4)
        world += alert(PRS[0] - 30, PRS[1] - 22, 4.6)
        persist.append((4, lambda i: pop(node("flask-conical", "verify", 48), *FLASK) + line(FLASK[0], FLASK[1] + 24, PRS[0], PRS[1] - 28)))
        return frame(i, 0, 0, world, "Verification agents run tests and attach artifacts; a plain question still becomes a PR.")
    scenes.append(f5)

    BOARD_X, BOARD_Y = 1090, 100
    COLW = 120
    COLNAMES = ["triage", "spec", "dev", "QA", "review"]

    def board(begin=None, owner=None):
        out = f'<rect x="{BOARD_X}" y="{BOARD_Y}" width="{COLW * 5}" height="110" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2"/>'
        for c, name in enumerate(COLNAMES):
            x = BOARD_X + c * COLW
            if c:
                out += f'<path d="M{x} {BOARD_Y + 8} V{BOARD_Y + 102}" stroke="rgba(255,255,255,0.1)"/>'
            out += text(x + COLW / 2, BOARD_Y + 22, name, 12)
        out += text(BOARD_X + COLW * 2.5, BOARD_Y - 12, "project board", 12, TEXT)
        return hidden_until(out, begin)

    def col_x(c):
        return BOARD_X + c * COLW + COLW / 2

    def moving_cards(begin, by_hand=False, crash_at=None, n=5, period=5.0):
        """Cards hopping column to column."""
        out = ""
        cols = [CYAN, ORANGE, YELLOW, LIME, CYAN]
        for k in range(n):
            b = begin + k * period / n
            pts = ";".join(f"{col_x(c) - col_x(0):.0f} 0" for c in range(5))
            vals = ";".join(f"{col_x(c) - col_x(0):.0f} 0" for c in [0, 0, 1, 1, 2, 2, 3, 3, 4, 4])
            kt = "0;0.15;0.25;0.35;0.45;0.55;0.65;0.75;0.85;1"
            stop = ""
            if crash_at is not None and k == 1:
                stop = (f'<animate attributeName="fill" to="{DIM}" begin="{crash_at}s" dur="0.1s" fill="freeze"/>')
            out += (
                f'<g transform="translate({col_x(0)} {BOARD_Y + 50 + (k % 3) * 18})"><g opacity="0">'
                f'<set attributeName="opacity" to="1" begin="{b}s"/>'
                f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}" '
                f'dur="{period * (2 if by_hand else 1)}s" begin="{b}s" repeatCount="indefinite" calcMode="spline" '
                f'keySplines="{";".join(["0.4 0 0.2 1"] * 9)}"/>'
                f'<rect x="-22" y="-7" width="44" height="14" rx="3" fill="{cols[k % 5]}">{stop}</rect></g></g>'
            )
        return out

    # 6 project board (pan)
    def f6():
        i = 5
        world = static(i) + board(1.0)
        world += moving_cards(1.6, by_hand=True, n=2)
        # inbox piling up
        for k in range(8):
            world += hidden_until(f'<rect x="{BOARD_X - 70}" y="{BOARD_Y + 96 - k * 12}" width="44" height="9" rx="2" fill="{YELLOW}"/>', 1.6 + k * 0.4)
        world += hidden_until(text(BOARD_X - 48, BOARD_Y + 128, "inbox", 11), 1.6)
        hand = node("hand", "you", 40, YELLOW, stroke=YELLOW)
        world += (
            f'<g transform="translate({col_x(0)} {BOARD_Y + 160})"><g opacity="0"><set attributeName="opacity" to="1" begin="1.6s"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{COLW} 0;{COLW * 2} 0;{COLW} 0;0 0" dur="5s" begin="1.6s" repeatCount="indefinite" calcMode="spline" keySplines="{SPL4}"/>'
            f"{hand}</g></g>"
        )
        world += alert(BOARD_X - 48, BOARD_Y - 6, 4.5)
        persist.append((5, lambda i: board()))
        return frame(i, F[0], F[1] - 60, world, "Work lands on a project board, Triage to Review; you drag every card by hand.")
    scenes.append(f6)

    BOT = (1800, 150)

    # 7 agent runs the board
    def f7():
        i = 6
        world = static(i)
        world += pop(node("bot", "board agent", 52, ORANGE, stroke=ORANGE, red_at=3.6), *BOT, 0.4)
        world += draw_line(BOT[0] - 26, BOT[1], BOARD_X + COLW * 5, BOT[1], 0.8, ORANGE, 2)
        world += moving_cards(1.0, crash_at=3.6, n=5, period=3.0)
        world += hidden_until(f'<g>{icon("x", BOT[0], BOT[1] - 50, 26, RED)}</g>', 3.6)
        world += alert(BOT[0] + 26, BOT[1] - 26, 3.8)
        persist.append((6, lambda i: pop(node("bot", "board agent", 52), *BOT)))
        return frame(i, F[1] - 60, F[1] - 60, world, "An agent moves the cards itself; it crashes mid-run and the task is lost.")
    scenes.append(f7)

    MACHINE = (1800, 248)

    # 8 durable
    def f8():
        i = 7
        world = static(i) + moving_cards(0.2, n=4, period=3.0)
        for c in range(5):
            world += pop(node("save", None, 24, LIME, stroke="none"), col_x(c), BOARD_Y + 128, 0.6 + c * 0.15)
        world += hidden_until(text(BOARD_X + COLW * 2.5, BOARD_Y + 158, "every step checkpointed", 11, LIME), 1.4)
        old = pop(server("machine"), *MACHINE, 0.3)
        world += f'<g>{old}<animate attributeName="opacity" to="0.15" begin="3.0s" dur="0.4s" fill="freeze"/></g>'
        world += draw_line(MACHINE[0], MACHINE[1] - 28, BOT[0], BOT[1] + 26, 0.6, WIRE, 2)
        world += pop(server("new machine"), MACHINE[0] + 110, MACHINE[1], 3.4)
        for n, ic in enumerate(["clock", "webhook"]):
            world += f'<g>{pop(node(ic, None, 24, MUTED, stroke="none"), MACHINE[0] - 50 - n * 30, MACHINE[1])}<animate attributeName="opacity" to="0" begin="3.0s" dur="0.4s" fill="freeze"/></g>'
        world += alert(MACHINE[0] + 138, MACHINE[1] - 28, 3.9)
        persist.append((7, lambda i: "".join(pop(node("save", None, 24, MUTED, stroke="none"), col_x(c), BOARD_Y + 128) for c in range(5))
                        + pop(server("machine"), MACHINE[0] + 110, MACHINE[1])))
        return frame(i, F[1] - 60, F[1] - 60, world, "Every step is checkpointed so tasks resume; the machine is replaced and its schedules die with it.")
    scenes.append(f8)

    MP = (2050, 150)

    def mplane(begin=None):
        bx = f'<rect x="0" y="-30" width="560" height="60" rx="12" fill="{BOX}" stroke="{ORANGE if begin is not None else WIRE}" stroke-width="2"/>' + text(80, 5, "management plane", 12, TEXT)
        out = pop(bx, *MP, begin)
        for n, (ic, lab) in enumerate([("clock", "schedules"), ("webhook", "triggers"), ("vault", "vault")]):
            b = None if begin is None else begin + 0.4 + n * 0.2
            out += pop(node(ic, None, 34, ORANGE if ic == "vault" and begin is not None else TEXT), MP[0] + 230 + n * 110, MP[1], b)
        return out

    # 9 management plane (pan)
    def f9():
        i = 8
        world = static(i) + mplane(1.0)
        boxes = []
        for n in range(4):
            x = MP[0] + 60 + n * 130
            world += pop(node("server", "sandbox", 44, TEXT), x, 248, 1.6 + n * 0.15)
            world += once(f"M{MP[0] + 450} {MP[1] + 30} L{x} 220", dur=0.8, begin=2.2 + n * 0.2,
                          inner=icon("key-round", 0, 0, 18, YELLOW))
        # silos: three people, each walled in with their own machines
        for n, c in enumerate([ORANGE, CYAN, YELLOW]):
            x = MP[0] + 690 + n * 100
            wall = f'<rect x="{x - 42}" y="20" width="84" height="270" rx="10" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 6"/>'
            world += hidden_until(wall, 3.6 + n * 0.1)
            world += pop(node("user", None, 34, c, stroke=c), x, 50, 3.2 + n * 0.15)
            world += pop(node("server", None, 30, c), x - 18, 248, 3.3 + n * 0.15)
            world += pop(node("server", None, 30, c), x + 18, 248, 3.4 + n * 0.15)
        world += alert(MP[0] + 940, 26, 4.2)
        persist.append((8, lambda i: mplane() + "".join(pop(node("server", "sandbox", 44), MP[0] + 60 + n * 130, 248) for n in range(4))
                        + "".join(pop(node("user", None, 34, c, stroke=c), MP[0] + 690 + n * 100, 50) for n, c in enumerate([ORANGE, CYAN, YELLOW]))))
        return frame(i, F[1] - 60, F[2], world, "Schedules, triggers and a vault move to a management plane, sandboxes get short-lived keys; everyone works in a silo.")
    scenes.append(f9)

    KB = (2790, 150)

    # 10 knowledge base
    def f10():
        i = 9
        world = static(i)
        world += pop(node("library", "knowledge", 60, ORANGE, stroke=ORANGE), *KB, 0.4)
        for n, c in enumerate([ORANGE, CYAN, YELLOW]):
            x = MP[0] + 690 + n * 100
            world += draw_line(x, 68, KB[0] + (n - 1) * 20, KB[1] - 30, 0.8 + n * 0.1, c, 1.5)
            world += flow(f"M{x} 68 L{KB[0] + (n - 1) * 20} {KB[1] - 30}", c, 1.2, 1.2 + n * 0.2, 1, size=7)
        world += flow(f"M{BOT[0] + 26} {BOT[1]} L{MP[0]} {MP[1]} L{KB[0] - 30} {KB[1]}", LIME, 2.0, 1.4, 2, size=7)
        # review column overflowing
        rx = KB[0] + 150
        world += hidden_until(text(rx, 290, "review", 12), 2.0)
        for k in range(14):
            world += hidden_until(f'<rect x="{rx - 22}" y="{270 - k * 14}" width="44" height="10" rx="2" fill="{CYAN if k < 7 else RED}"/>', 2.0 + k * 0.18)
        world += alert(rx + 30, 70, 4.6)
        persist.append((9, lambda i: pop(node("library", "knowledge", 60), *KB)))
        return frame(i, F[2], F[2], world, "Everyone, human and agent, shares one knowledge base kept in sync by agents; work outruns review.")
    scenes.append(f10)

    RUB = (3150, 150)
    HIST = (3060, 248)

    def history(begin=None):
        out = ""
        for k in range(24):
            el = f'<rect x="{HIST[0] - 60 + (k % 12) * 11}" y="{HIST[1] - 6 + (k // 12) * 12}" width="8" height="8" rx="2" fill="{MUTED}"/>'
            out += el if begin is None else hidden_until(el, begin + k * 0.03)
        return out + (text(HIST[0], HIST[1] + 34, "history", 11) if begin is None else hidden_until(text(HIST[0], HIST[1] + 34, "history", 11), begin))

    # 11 rubrics (pan)
    def f11():
        i = 10
        world = static(i)
        world += pop(node("ruler", "rubric", 56, ORANGE, stroke=ORANGE), *RUB, 1.0)
        world += flow(f"M{F[3] - 100} {RUB[1]} L{RUB[0] - 28} {RUB[1]}", CYAN, 1.0, 1.4, 3)
        world += flow(f"M{RUB[0] + 28} {RUB[1]} L{RUB[0] + 200} {RUB[1]}", LIME, 1.0, 1.9, 3)
        world += hidden_until(icon("check", RUB[0] + 220, RUB[1], 22, LIME), 1.9)
        world += flow(f"M{RUB[0]} {RUB[1] - 28} L{RUB[0]} 74", YELLOW, 1.2, 2.2, 1)
        world += pop(node("user-cog", "exceptions", 40, YELLOW, stroke=YELLOW), RUB[0], 50, 2.0)
        world += history(2.8)
        world += flow(f"M{HIST[0]} {HIST[1] - 12} L{RUB[0]} {RUB[1] + 28}", MUTED, 0.6, 3.4, 10, size=6)
        world += counter(RUB[0] + 60, 232, ["re-scoring 1 / 48,210", "re-scoring 9,400 / 48,210", "re-scoring 31,050 / 48,210"], 3.6, 0.9, 12, MUTED, RED, "start")
        world += alert(RUB[0] + 28, RUB[1] - 28, 4.6)
        persist.append((10, lambda i: pop(node("ruler", "rubric", 56, DIM if i >= 12 else TEXT), *RUB)
                        + pop(node("user-cog", "exceptions", 40), RUB[0], 50) + history()))
        return frame(i, F[2], F[3] - 40, world, "Agents review against a rubric and humans take the exceptions; every tweak re-scores all the history.")
    scenes.append(f11)

    REP = (3420, 150)

    def report(begin=None, heights=(30, 42, 36, 55, 48, 64)):
        out = f'<rect x="-70" y="-50" width="140" height="100" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2"/>'
        for k, h in enumerate(heights):
            out += f'<rect x="{-56 + k * 20}" y="{40 - h}" width="12" height="{h}" rx="2" fill="{CYAN}"/>'
        return pop(out, *REP, begin) + (text(REP[0], REP[1] + 72, "reports", 12) if begin is None else hidden_until(text(REP[0], REP[1] + 72, "reports", 12), begin))

    # 12 reports
    def f12():
        i = 11
        world = static(i) + report(0.4)
        world += draw_line(HIST[0] + 70, HIST[1], REP[0] - 70, REP[1] + 30, 0.8, WIRE, 2)
        world += flow(f"M{HIST[0] + 70} {HIST[1]} L{REP[0] - 70} {REP[1] + 30}", MUTED, 1.0, 1.0, 3, size=6)
        for k, lab in enumerate(["cost / task", "cycle time", "rework"]):
            world += hidden_until(text(REP[0] + 90, REP[1] - 30 + k * 26, lab, 12, TEXT, "start"), 1.4 + k * 0.2)
        world += f'<g opacity="0"><set attributeName="opacity" to="1" begin="2.6s"/>{pop(node("ruler", "rubric", 56, DIM, stroke=RED), *RUB)}</g>'
        world += hidden_until(text(RUB[0], RUB[1] - 44, "unchanged since March", 11, RED), 3.0)
        world += alert(RUB[0] + 28, RUB[1] - 28, 3.2)
        persist.append((11, lambda i: report()))
        return frame(i, F[3] - 40, F[3] - 40, world, "Reports keep the history: cost per task, cycle time, rework; the rubrics go stale.")
    scenes.append(f12)

    GOAL = (3700, 150)

    # 13 goals: the self-improving loop
    def f13():
        i = 12
        world = static(i)
        world += pop(node("target", "goals", 60, ORANGE, stroke=ORANGE, glow=True), *GOAL, 0.4)
        # target line over the report, bars climbing to it
        world += hidden_until(f'<path d="M{REP[0] - 66} {REP[1] - 40} H{REP[0] + 66}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 4"/>', 0.8)
        for k in range(6):
            x = REP[0] - 56 + k * 20
            world += f'<rect x="{x}" y="{REP[1] + 40}" width="12" height="0" rx="2" fill="{LIME}"><animate attributeName="height" values="0;{60 + k * 4}" dur="1.2s" begin="{2.2 + k * 0.1}s" fill="freeze" {EASE}/><animate attributeName="y" values="{REP[1] + 40};{REP[1] - 20 - k * 4}" dur="1.2s" begin="{2.2 + k * 0.1}s" fill="freeze" {EASE}/></rect>'
        # the loop: goals -> agent -> rubric -> reports -> goals
        loop = f"M{GOAL[0]} {GOAL[1] + 34} C{GOAL[0]} 290 {RUB[0]} 290 {RUB[0]} {RUB[1] + 30} M{RUB[0]} {RUB[1] - 30} C{RUB[0]} 0 {GOAL[0]} 0 {GOAL[0]} {GOAL[1] - 34}"
        world += hidden_until(f'<path d="{loop}" fill="none" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="4 6" opacity="0.6"/>', 1.0)
        world += pop(node("bot", "tuner", 40, ORANGE, stroke=ORANGE), (GOAL[0] + RUB[0]) / 2, 262, 1.2)
        world += flow(f"M{GOAL[0]} {GOAL[1] + 34} C{GOAL[0]} 290 {RUB[0]} 290 {RUB[0]} {RUB[1] + 30}", ORANGE, 2.0, 1.6, 3, size=8)
        world += flow(f"M{RUB[0]} {RUB[1] - 30} C{RUB[0]} 0 {GOAL[0]} 0 {GOAL[0]} {GOAL[1] - 34}", LIME, 2.0, 2.6, 3, size=8)
        world += f'<g opacity="0"><set attributeName="opacity" to="1" begin="1.8s"/>{pop(node("ruler", "rubric", 56, LIME, stroke=LIME), *RUB)}</g>'
        return frame(i, F[3] - 40, F[3] - 40, world, "Goals sit over the reports; an agent tunes rubrics and workflows until the numbers reach them.")
    scenes.append(f13)

    for n, fn in enumerate(scenes, 1):
        p = OUT / f"f{n:02d}.svg"
        p.write_text(fn())
        files.append(p.name)
    return files


if __name__ == "__main__":
    a = build_agent()
    f = build_factory()
    print(len(a), "agent,", len(f), "factory")
