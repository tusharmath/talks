#!/usr/bin/env python3
"""Act 2 ("Build an AI SDLC") story diagrams for the software factory deck.

Run: `python3 docs/img/story/generate_sdlc.py`. Writes s01.svg ... s09.svg next
to this file. Reuses the primitives (palette, nodes, flows, alerts) from
generate.py so the style matches the a- and f-series exactly; generate.py
itself is not modified.

Act 2 happens before any infrastructure exists, so there are no cloud machines,
control planes or sandboxes here. One world, two regions:

- s01-s02: teams, their repos and agents on the left, the product knowledge in
  the middle, requests turning into PRs on the right.
- s03-s07: a project board (Triage to Review) that gains, slide by slide, a
  board agent, verification agents, owners, a rubric grader and skills.
- s08-s09: the camera pans right to the reports, then goals and a tuner.

Every slide redraws what was built before (static) and animates only what is
new: the fix first, then its problem, ending on a red alert. SMIL only, so the
files animate inside a plain <img>.
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep __pycache__ out of docs/
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402
from generate import (  # noqa: E402
    BOX, CYAN, DIM, EASE, LIME, MUTED, ORANGE, RED, TEXT, WIRE, YELLOW,
    alert, camera, counter, draw_line, flow, hidden_until, icon, line, node,
    once, pop, shake, svg, text,
)

OUT = g.OUT

# Lucide icons not in icons.json (added in memory only; icons.json is untouched).
g.ICONS.update({
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" />',
    "sparkles": (
        '<path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966'
        'l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594'
        'l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z" /><path d="M20 2v4" />'
        '<path d="M22 4h-4" /><circle cx="4" cy="20" r="2" />'
    ),
    "folder-git-2": (
        '<path d="M18 19a5 5 0 0 1-5-5v8" /><path d="M9 20H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9'
        'l.81 1.2a2 2 0 0 0 1.67.9H20a2 2 0 0 1 2 2v5" /><circle cx="13" cy="12" r="2" /><circle cx="20" cy="19" r="2" />'
    ),
    "circle-check": '<circle cx="12" cy="12" r="10" /><path d="m9 12 2 2 4-4" />',
    "user-check": '<path d="m16 11 2 2 4-4" /><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" />',
    "scroll-text": (
        '<path d="M15 12h-5" /><path d="M15 8h-5" /><path d="M19 17V5a2 2 0 0 0-2-2H4" />'
        '<path d="M8 21h12a2 2 0 0 0 2-2v-1a1 1 0 0 0-1-1H11a1 1 0 0 0-1 1v1a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v2'
        'a1 1 0 0 0 1 1h3" />'
    ),
    "siren": (
        '<path d="M7 18v-6a5 5 0 1 1 10 0v6" /><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7'
        'a2 2 0 0 0-2 2z" /><path d="M21 12h1" /><path d="M18.5 4.5 18 5" /><path d="M2 12h1" /><path d="M12 2v1" />'
        '<path d="m4.929 4.929.707.707" /><path d="M12 12v6" />'
    ),
})


# ---------------------------------------------------------------- helpers

def fade_out(inner, begin, to=0):
    return f'<g>{inner}<animate attributeName="opacity" to="{to}" begin="{begin}s" dur="0.3s" fill="freeze"/></g>'


def between(inner, start, end):
    """Visible from `start` (None: from the first frame) until `end`."""
    s = "" if start is None else f'<set attributeName="opacity" to="1" begin="{start}s"/>'
    return f'<g opacity="{0 if start is not None else 1}">{s}<set attributeName="opacity" to="0" begin="{end}s"/>{inner}</g>'


def stroke_to(color, t):
    return f'<animate attributeName="stroke" to="{color}" begin="{t}s" dur="0.2s" fill="freeze"/>'


def badge(ic, x, y, color, begin=None):
    return pop(node(ic, None, 22, color, stroke="none"), x, y, begin)


def chip(x, y, w, h, label, color=WIRE, text_color=TEXT, size=11, turn=None, ic=None, ic_color=None):
    """Label box drawn at its top-left corner; `turn` = (color, t) recolours its border."""
    anim = stroke_to(*turn) if turn else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{BOX}" stroke="{color}" stroke-width="1.5">{anim}</rect>'
    if ic:
        out += icon(ic, x + 16, y + h / 2, 14, ic_color or text_color)
        out += text(x + 30, y + h / 2 + 4, label, size, text_color, "start")
    else:
        out += text(x + w / 2, y + h / 2 + 4, label, size, text_color)
    return out


def path_el(d, color=WIRE, width=2, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{ds}/>'


def move(inner, dx, dy, begin, dur=0.8):
    """Slide `inner` by (dx, dy) at `begin`."""
    return (
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy}" '
        f'dur="{dur}s" begin="{begin}s" fill="freeze" {EASE}/>{inner}</g>'
    )


def write(name, body, comment):
    p = OUT / f"{name}.svg"
    p.write_text(svg(body, comment))
    return p.name


# ------------------------------------------------- s01-s02: teams and knowledge

TEAMS = [("Payments", 55, ORANGE), ("Search", 150, CYAN), ("Mobile", 245, YELLOW)]
REPO_X, AGENT_X = 90, 240
KB = (560, 150)
PRODUCT = [("file-text", "Specs", 470), ("scroll-text", "Decisions", 560), ("siren", "Incidents", 650)]
PRODUCT_Y = 50


def repos(begin=None):
    return "".join(
        pop(node("folder-git-2", name, 44, TEXT), REPO_X, y, None if begin is None else begin + n * 0.15)
        for n, (name, y, _) in enumerate(TEAMS)
    )


def repo_wires(begin=None):
    return "".join(line(REPO_X + 22, y, AGENT_X - 22, y, WIRE, 2, None, begin) for _, y, _ in TEAMS)


def team_agents():
    return "".join(pop(node("bot", None, 44, c, stroke=c), AGENT_X, y) for _, y, c in TEAMS)


def code_flows(begin):
    return "".join(
        flow(f"M{REPO_X + 22} {y} L{AGENT_X - 22} {y}", CYAN, 1.2, begin + n * 0.2, 2, size=7)
        for n, (_, y, _) in enumerate(TEAMS)
    )


def product(dashed=False, red_at=None, begin=None):
    out = ""
    for n, (ic, lab, x) in enumerate(PRODUCT):
        b = None if begin is None else begin + n * 0.15
        el = node(ic, lab, 36, DIM if dashed else TEXT, stroke=WIRE, dashed=dashed, red_at=red_at)
        out += pop(el, x, PRODUCT_Y, b)
    return out


def agent_to_kb(y):
    return f"M{AGENT_X + 22} {y} L{KB[0] - 34} {KB[1] + (y - 150) * 0.25:.0f}"


def kb_to_agent(y):
    return f"M{KB[0] - 34} {KB[1] + (y - 150) * 0.25:.0f} L{AGENT_X + 22} {y}"


def s01():
    w = repos(0.2) + repo_wires(0.6)
    # one agent, then the same agent copied out to every team
    w += pop(node("bot", None, 44, CYAN, stroke=CYAN), AGENT_X, 150, 0.4)
    for n, (_, y, c) in enumerate(TEAMS):
        if y == 150:
            continue
        w += once(f"M{AGENT_X} 150 L{AGENT_X} {y}", dur=0.6, begin=0.9, fade_end=False,
                  inner=node("bot", None, 44, c, stroke=c))
    w += hidden_until(text(AGENT_X, 14, "Same Agent, Every Team", 11, MUTED), 1.0)
    w += code_flows(1.4)
    for n, (_, y, _) in enumerate(TEAMS):
        w += hidden_until(text(AGENT_X + 30, y + 26, "Knows The Code", 10, LIME, "start"), 1.8 + n * 0.15)
    # the product lives somewhere else: nothing connects to it
    w += product(dashed=True, red_at=3.6, begin=2.2)
    slot = (
        f'<rect x="-32" y="-32" width="64" height="64" rx="12" fill="none" stroke="{DIM}" stroke-width="2" stroke-dasharray="5 5"/>'
        + icon("circle-help", 0, 0, 30, YELLOW)
    )
    w += pop(slot, *KB, 2.6)
    w += hidden_until(text(KB[0], KB[1] + 52, "The Product", 12, MUTED), 2.6)
    for n, (_, y, _) in enumerate(TEAMS):
        w += flow(agent_to_kb(y), YELLOW, 1.2, 2.9 + n * 0.2, 1, size=7, stop=4.6)
        w += badge("circle-help", AGENT_X + 24, y - 22, YELLOW, 3.4 + n * 0.1)
    w += alert(KB[0] + 32, KB[1] - 32, 4.0)
    return write("s01", w, "The same agent is copied to every team; each one learns its repo but none can reach the specs, decisions or incidents.")


def s02():
    w = repos() + repo_wires() + team_agents()
    w += code_flows(0.0)
    # the product's knowledge moves into one shared knowledge base
    w += product()
    for ic, _, x in PRODUCT:
        w += draw_line(x, PRODUCT_Y + 44, KB[0] + (x - KB[0]) * 0.3, KB[1] - 34, 0.6, WIRE, 1.5, 0.4)
        w += flow(f"M{x} {PRODUCT_Y + 44} L{KB[0] + (x - KB[0]) * 0.3:.0f} {KB[1] - 34}", MUTED, 1.0, 0.9, 1, size=6)
    w += pop(node("library", "Knowledge Base", 64, ORANGE, stroke=ORANGE), *KB, 0.3)
    for n, (_, y, c) in enumerate(TEAMS):
        x2, y2 = KB[0] - 34, KB[1] + (y - 150) * 0.25
        w += draw_line(AGENT_X + 22, y, x2, y2, 0.8 + n * 0.1, WIRE, 2)
        w += flow(kb_to_agent(y), CYAN, 1.4, 1.2 + n * 0.25, 1, size=7)   # agents read
        w += flow(agent_to_kb(y), LIME, 1.4, 1.9 + n * 0.25, 1, size=7)   # and keep it in sync
    # now every request turns into a PR, even a question
    w += hidden_until(text(770, 32, "Request", 11, MUTED) + text(925, 32, "Result", 11, MUTED), 2.0)
    reqs = [("Fix Login Bug", "pencil", TEXT, 80), ("Add CSV Export", "pencil", TEXT, 150),
            ("Why Is It Slow?", "message-square", YELLOW, 220)]
    for n, (lab, ic, col, y) in enumerate(reqs):
        t = 2.2 + n * 0.7
        q = n == 2
        w += hidden_until(chip(690, y - 15, 160, 30, lab, YELLOW if q else WIRE, col, 11, ic=ic, ic_color=col), t)
        w += draw_line(852, y, 900, y, t + 0.2, WIRE, 1.5, 0.3)
        w += once(f"M852 {y} L900 {y}", YELLOW if q else CYAN, 0.4, t + 0.3, size=8)
        w += pop(node("git-pull-request", None, 40, RED if q else TEXT, red_at=t + 0.8 if q else None), 925, y, t + 0.6)
    w += alert(945, 200, 4.2)
    return write("s02", w, "Specs, decisions and incidents move into a knowledge base every agent reads and keeps in sync; then every request, even a question, comes back as a PR.")


# ------------------------------------------------------ s03-s07: the board

BX, BY, COLW, BH = 120, 50, 112, 150
COLS = ["Triage", "Spec", "Dev", "QA", "Review"]
ROWS = [104, 128, 152]
LANE_Y = 250            # agents and people under the board
SHIP = (750, 125)       # where finished cards go
INBOX_X = 55
ANSWERED = (55, 252)
CARD_COLORS = [CYAN, ORANGE, YELLOW, LIME, CYAN]


def colx(c):
    return BX + c * COLW + COLW / 2


def board(begin=None):
    out = f'<rect x="{BX}" y="{BY}" width="{COLW * 5}" height="{BH}" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2"/>'
    for c, name in enumerate(COLS):
        x = BX + c * COLW
        if c:
            out += f'<path d="M{x} {BY + 8} V{BY + BH - 8}" stroke="rgba(255,255,255,0.1)"/>'
        out += text(x + COLW / 2, BY + 24, name, 12)
    out += text(BX + COLW * 2.5, BY - 14, "Project Board", 12, TEXT)
    return hidden_until(out, begin)


def card_glyph(color, owner=False, risky=False):
    out = f'<rect x="-25" y="-7" width="50" height="14" rx="3" fill="{color}"/>'
    if risky:
        out = f'<rect x="-28" y="-10" width="56" height="20" rx="5" fill="none" stroke="{RED}" stroke-width="1.5"/>' + out
    if owner:
        out += f'<circle cx="-17" cy="0" r="4.5" fill="#0b0b0b" stroke="{TEXT}" stroke-width="1.2"/>'
    return out


def inbox(n, begin=None, step=0.35):
    out = ""
    for k in range(n):
        el = f'<rect x="{INBOX_X - 22}" y="{186 - k * 11}" width="44" height="8" rx="2" fill="{YELLOW}"/>'
        out += el if begin is None else hidden_until(el, begin + k * step)
    lab = text(INBOX_X, 212, "Inbox", 11)
    return out + (lab if begin is None else hidden_until(lab, begin))


def answered(begin=None):
    return pop(node("circle-check", "No PR", 40, LIME, stroke=LIME), *ANSWERED, begin)


def ship_node(begin=None):
    out = line(BX + COLW * 5, SHIP[1], SHIP[0] - 24, SHIP[1], WIRE, 2, None, begin)
    return out + pop(node("rocket", "Shipped", 48, TEXT), *SHIP, begin)


def mover(begin, period, row, color, owner=False, hand=False, ship=True):
    """A card hopping Triage to Review (and out to Shipped), looping forever.
    With `hand`, a hand below the board drags it."""
    x0 = colx(0)
    pts = [(colx(c) - x0, 0) for c in range(5)]
    seq = [p for p in pts for _ in (0, 1)]
    if ship:
        seq.append((SHIP[0] - x0 - 10, SHIP[1] - row))
    n = len(seq)
    kt = ";".join(f"{k / (n - 1):.3f}" for k in range(n))
    vals = ";".join(f"{x:.0f} {y:.0f}" for x, y in seq)
    splines = ";".join(["0.4 0 0.2 1"] * (n - 1))
    fade = ""
    if ship:
        fade = (f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{(n - 2) / (n - 1):.3f};0.99;1" '
                f'dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>')
    body = card_glyph(color, owner)
    if hand:
        body += f'<g transform="translate(0 {LANE_Y - row})">{node("hand", "You", 40, YELLOW, stroke=YELLOW)}</g>'
    return (
        f'<g transform="translate({x0} {row})"><g opacity="0"><set attributeName="opacity" to="1" begin="{begin}s"/>'
        f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}" '
        f'dur="{period}s" begin="{begin}s" repeatCount="indefinite" calcMode="spline" keySplines="{splines}"/>'
        f'<g>{fade}{body}</g></g></g>'
    )


def auto_cards(begin, owner=False, n=4, period=4.8):
    return "".join(
        mover(begin + k * period / n, period, ROWS[k % 3], CARD_COLORS[k % 5], owner) for k in range(n)
    )


def lane_node(ic, label, x, color, begin=None, red_at=None):
    out = line(x, LANE_Y - 22, x, BY + BH, color if begin is not None else WIRE, 1.5, "3 4", begin)
    return out + pop(node(ic, label, 44, color, stroke=color if begin is not None else WIRE, red_at=red_at), x, LANE_Y, begin)


ARTIFACTS = ["video", "file-text", "chart-column"]


def artifacts(begin=None):
    out = ""
    for n, ic in enumerate(ARTIFACTS):
        x = colx(3) - 30 + n * 30
        b = None if begin is None else begin + n * 0.25
        out += badge(ic, x, 182, CYAN, b)
    return out


def board_base(level):
    """Everything on the board built before slide `level` (3..7), drawn static."""
    out = board() + answered() + ship_node()
    out += inbox(3)
    if level >= 5:
        out += lane_node("bot", "Board Agent", colx(1), TEXT)
        out += lane_node("flask-conical", "Verify", colx(3), TEXT) + artifacts()
    return out


RUBRIC_X, RUBRIC_Y, RUBRIC_W, RUBRIC_H = 795, 28, 178, 172
RISKY_Y = 180
RUBRIC_ITEMS = ["Tests Pass", "Migration Test", "No Secrets", "Docs Updated"]
OWNER_GATE = colx(4)
OWNER_SIDE = 750
FAIL_ROW = 1  # rubric item index that keeps failing (Migration Test)


def item_y(k):
    return RUBRIC_Y + 56 + k * 30


def rubric_panel(begin=None, checks=None):
    out = (
        f'<rect x="{RUBRIC_X}" y="{RUBRIC_Y}" width="{RUBRIC_W}" height="{RUBRIC_H}" rx="10" fill="{BOX}" stroke="{ORANGE if begin is not None else WIRE}" stroke-width="2"/>'
        + icon("list-checks", RUBRIC_X + 22, RUBRIC_Y + 24, 18, ORANGE if begin is not None else TEXT)
        + text(RUBRIC_X + 40, RUBRIC_Y + 29, "Rubric", 12, TEXT, "start")
    )
    for k, lab in enumerate(RUBRIC_ITEMS):
        y = item_y(k)
        out += f'<rect x="{RUBRIC_X + 14}" y="{y - 8}" width="16" height="16" rx="3" fill="none" stroke="{WIRE}" stroke-width="1.5"/>'
        out += text(RUBRIC_X + 40, y + 4, lab, 11, TEXT, "start")
        if checks:
            out += checks(k, RUBRIC_X + 22, y)
    return hidden_until(out, begin)


def fail_marks(n, begin=None, step=0.75):
    out = ""
    for k in range(n):
        el = f'<rect x="-6" y="-6" width="12" height="12" rx="2" fill="{RED}"/>'
        out += pop(el, 818 + k * 18, LANE_Y, None if begin is None else begin + k * step)
    return out


def s03():
    w = board(0.3)
    # a few cards waiting in their columns
    for c, r, col in [(1, 0, ORANGE), (2, 1, YELLOW), (3, 0, LIME)]:
        w += pop(card_glyph(col), colx(c), ROWS[r], 0.6 + c * 0.1)
    w += ship_node(0.5)
    # a question needs no PR: it closes in Triage
    w += fade_out(pop(card_glyph(YELLOW), colx(0), ROWS[0], 0.8), 1.9, 0)
    w += between(icon("message-square", colx(0) + 36, ROWS[0], 14, YELLOW), 0.9, 1.9)
    w += answered(1.6)
    w += once(f"M{colx(0)} {ROWS[0]} L{BX + 14} {ROWS[0]} L{BX + 14} {ANSWERED[1]} L{ANSWERED[0] + 24} {ANSWERED[1]}",
              dur=1.0, begin=1.9, inner=card_glyph(YELLOW), fade_end=True)
    # every other card is dragged column to column by hand
    w += mover(1.2, 6.0, ROWS[2], CYAN, hand=True)
    # while new requests pile up in the inbox
    w += inbox(12, 1.4, 0.3)
    w += alert(INBOX_X, 38, 5.0)
    return write("s03", w, "Work lands on a project board, Triage to Review; a question closes without a PR, every other card is dragged by hand while the inbox piles up.")


def s04():
    w = board() + answered() + ship_node() + inbox(3)
    # an agent runs the board: cards move themselves
    w += lane_node("bot", "Board Agent", colx(1), ORANGE, 0.3)
    w += auto_cards(0.9)
    # verification agents run QA and attach artifacts
    w += lane_node("flask-conical", "Verify", colx(3), LIME, 0.6)
    for n, ic in enumerate(ARTIFACTS):
        x = colx(3) - 30 + n * 30
        w += once(f"M{colx(3)} {LANE_Y - 22} L{x} 182", LIME, 0.6, 1.3 + n * 0.25, size=7)
    w += artifacts(1.8)
    # a card ships; the sign-off line is empty
    w += pop(node("rocket", "Shipped", 48, ORANGE, stroke=ORANGE), *SHIP, 3.0)
    sign = chip(812, 110, 160, 30, "Signed Off: ?", WIRE, MUTED, 11, turn=(RED, 3.8), ic="user", ic_color=MUTED)
    w += hidden_until(sign, 3.3)
    w += hidden_until(text(892, 165, "Nobody", 11, RED), 3.8)
    w += alert(972, 110, 4.0)
    return write("s04", w, "A board agent moves every card and verification agents attach screen captures, logs and reports; a card ships with nobody on the sign-off.")


def s05():
    w = board_base(5)
    # every card carries its owner
    w += auto_cards(0.3, owner=True)
    w += lane_node("user-check", "Owner", OWNER_GATE, ORANGE, 0.5)
    # a risky card waits in Review for its owner's sign-off
    ry = RISKY_Y
    w += fade_out(pop(card_glyph(ORANGE, owner=True, risky=True), colx(4), ry, 0.8), 2.2)
    w += fade_out(hidden_until(icon("shield", colx(4) + 40, ry, 16, RED), 0.9), 2.2)
    w += once(f"M{OWNER_GATE} {LANE_Y - 22} L{OWNER_GATE} {ry + 12}", LIME, 0.6, 1.3, size=8)
    w += fade_out(pop(icon("check", 0, 0, 16, LIME), colx(4) + 40, ry, 1.8), 2.2)
    w += once(f"M{colx(4)} {ry} L{SHIP[0] - 10} {SHIP[1]}", dur=0.6, begin=2.2,
              inner=card_glyph(ORANGE, owner=True))
    w += hidden_until(chip(806, 110, 172, 30, "Signed Off: Owner", LIME, TEXT, 11, ic="user-check", ic_color=LIME), 2.6)
    # then the owner rejects the same mistake, week after week
    for k in range(3):
        t = 3.0 + k * 0.6
        y = 172 + k * 26
        w += once(f"M{OWNER_GATE + 22} {LANE_Y} L800 {y}", RED, 0.5, t, size=8)
        w += hidden_until(icon("x", 822, y, 16, RED) + text(836, y + 4, f"Week {k + 1}: No Test", 11, RED, "start"), t + 0.5)
    w += alert(OWNER_GATE + 22, LANE_Y - 22, 5.0)
    return write("s05", w, "Every card gets an owner and risky changes wait for their sign-off; the owner rejects the same mistake every week.")


def s06():
    w = board_base(6) + auto_cards(0.0, owner=True)
    # the owner steps aside; an agent grades every card against a rubric
    w += move(pop(node("user-check", "Owner", 44, TEXT), OWNER_GATE, LANE_Y), OWNER_SIDE - OWNER_GATE, 0, 0.3)
    w += lane_node("bot", "Grader", OWNER_GATE, ORANGE, 1.0)
    w += badge("list-checks", OWNER_GATE + 22, LANE_Y - 22, ORANGE, 1.2)

    def checks(k, x, y):
        if k == FAIL_ROW:
            # fills red each time the same failure is caught
            return (f'<rect x="{x - 6}" y="{y - 6}" width="12" height="12" rx="2" fill="{RED}" opacity="0">'
                    f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.6;1" dur="0.75s" begin="2.2s" repeatCount="6"/></rect>')
        return (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{1.6 + k * 0.2}s"/>'
                f'{icon("check", x, y, 14, LIME)}</g>')
    w += rubric_panel(0.6, checks)
    # grades: most cards pass, the exceptions go to the owner
    w += flow(f"M{OWNER_GATE} {BY + BH} L{OWNER_GATE} {LANE_Y - 22}", LIME, 0.9, 1.4, 2, size=7)
    w += flow(f"M{OWNER_GATE + 22} {LANE_Y} L{OWNER_SIDE - 22} {LANE_Y}", YELLOW, 1.5, 1.8, 1, size=8)
    # the same failure, caught again every week
    w += fail_marks(6, 2.2)
    w += hidden_until(text(812, 284, "Same Failure", 11, RED, "start"), 2.4)
    w += alert(RUBRIC_X + RUBRIC_W - 4, item_y(FAIL_ROW), 4.4)
    return write("s06", w, "Owners write down what they check; an agent grades every card against the rubric and sends the exceptions to a human; the same failure is caught every week.")


def s06_static():
    """s06's additions, drawn static for later slides."""
    def checks(k, x, y):
        if k == FAIL_ROW:
            return f'<rect x="{x - 6}" y="{y - 6}" width="12" height="12" rx="2" fill="{RED}"/>'
        return icon("check", x, y, 14, LIME)
    out = pop(node("user-check", "Owner", 44, TEXT), OWNER_SIDE, LANE_Y)
    out += lane_node("bot", "Grader", OWNER_GATE, TEXT) + badge("list-checks", OWNER_GATE + 22, LANE_Y - 22, TEXT)
    out += rubric_panel(None, checks)
    return out


SKILL = (950, LANE_Y)
DEV = colx(2)
SKILL_LANE = 214


def s07():
    w = board_base(7) + auto_cards(0.0, owner=True) + s06_static()
    # the repeated fix condenses into a skill
    for k in range(6):
        el = f'<rect x="{812 + k * 18}" y="{LANE_Y - 6}" width="12" height="12" rx="2" fill="{RED}"/>'
        w += (f'<g>{el}<animateTransform attributeName="transform" type="translate" values="0 0;{SKILL[0] - 818 - k * 18} 0" '
              f'dur="0.7s" begin="{0.4 + k * 0.08}s" fill="freeze" {EASE}/>'
              f'<animate attributeName="opacity" to="0" begin="{1.0 + k * 0.08}s" dur="0.2s" fill="freeze"/></g>')
    w += pop(node("book-open", "Skill", 40, LIME, stroke=LIME), *SKILL, 1.4)
    w += pop(icon("sparkles", 0, 0, 16, LIME), SKILL[0] - 28, SKILL[1] - 26, 1.6)
    # the next agent loads it
    w += lane_node("bot", "Dev Agent", DEV, ORANGE, 0.5)
    route = f"M{SKILL[0]} {SKILL[1] - 20} V{SKILL_LANE} H{DEV + 22} V{LANE_Y - 22}"
    w += hidden_until(path_el(route, WIRE, 1.5, "3 4"), 1.8)
    w += once(route, dur=1.4, begin=2.0, inner=icon("sparkles", 0, 0, 18, LIME))
    w += badge("book-open", DEV + 22, LANE_Y - 22, LIME, 3.4)
    # the failing rubric line goes green for now
    w += hidden_until(f'<rect x="{RUBRIC_X + 16}" y="{item_y(FAIL_ROW) - 6}" width="12" height="12" fill="{BOX}"/>'
                      + icon("check", RUBRIC_X + 22, item_y(FAIL_ROW), 14, LIME), 3.6)
    # but did the skill help, or did the work just get easier?
    w += pop(node("circle-help", None, 30, YELLOW, stroke=YELLOW), SKILL[0] - 70, SKILL[1], 4.0)
    w += hidden_until(text(SKILL[0] - 70, SKILL[1] + 34, "Helped?", 11, YELLOW), 4.1)
    w += alert(SKILL[0] + 20, SKILL[1] - 20, 4.4)
    return write("s07", w, "The fix that keeps failing condenses into a skill and the next agent loads it; nobody can tell whether it helped.")


def board_world_all():
    """The whole board region as it stands after s07, static."""
    out = board_base(8) + s06_static()
    out += pop(node("book-open", "Skill", 40, TEXT), *SKILL)
    out += lane_node("bot", "Dev Agent", DEV, TEXT) + badge("book-open", DEV + 22, LANE_Y - 22, LIME)
    return out


# ------------------------------------------------- s08-s09: reports and goals

R0 = 1000  # world x of the reports region
TASK = (R0 + 40, 80, 300, 186)       # x, y, w, h of the per-task panel
SKILLP = (R0 + 365, 80, 330, 186)    # per-skill panel
METRICS = [("Cost", 0.62), ("Cycle Time", 0.78), ("Rework", 0.55)]
GOAL_LEVELS = [0.38, 0.42, 0.3]
SKILLS = [("Migration Test", 0.25, 0.7), ("Auth Checks", 0.55, 0.6), ("API Docs", 0.5, 0.45)]
YOU = (R0 + 800, 150)
GOALS = (R0 + 170, 36)
TUNER = (R0 + 780, 150)
DIALS = [("Rubrics", 82), ("Skills", 152), ("Workflows", 222)]


def metric_y(k):
    return TASK[1] + 58 + k * 44


def panel(x, y, w, h, title, ic):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2"/>'
        + icon(ic, x + 22, y + 24, 18, TEXT) + text(x + 40, y + 29, title, 12, TEXT, "start")
    )


def task_panel(levels, begin=None, colors=None, times=None):
    x, y, w, h = TASK
    out = panel(x, y, w, h, "Per Task", "chart-column")
    bw = 150
    for k, (lab, lvl) in enumerate(METRICS):
        my = metric_y(k)
        out += text(x + 16, my + 4, lab, 11, TEXT, "start")
        col = (colors or [CYAN] * 3)[k]
        if times:
            out += g.bar(x + 130, my - 6, bw, 12, levels[k], times, [col] * len(levels[k]), rx=2)
        else:
            out += g.static_bar(x + 130, my - 6, bw, 12, levels[k], col)
    return hidden_until(out, begin)


def skill_panel(begin=None, grow=None):
    x, y, w, h = SKILLP
    out = panel(x, y, w, h, "Rework Per Skill", "book-open")
    out += f'<rect x="{x + 16}" y="{y + 46}" width="10" height="10" rx="2" fill="{LIME}"/>' + text(x + 32, y + 55, "With", 10, MUTED, "start")
    out += f'<rect x="{x + 84}" y="{y + 46}" width="10" height="10" rx="2" fill="{DIM}"/>' + text(x + 100, y + 55, "Without", 10, MUTED, "start")
    bw = 130
    for k, (lab, with_, without) in enumerate(SKILLS):
        sy = y + 88 + k * 34
        out += text(x + 16, sy + 4, lab, 11, TEXT, "start")
        bx = x + 182
        for j, (lvl, col) in enumerate([(without, DIM), (with_, LIME)]):
            by = sy - 8 + j * 9
            if grow is not None:
                t = grow + k * 0.3 + j * 0.15
                out += (f'<rect x="{bx}" y="{by}" width="0" height="7" rx="2" fill="{col}">'
                        f'<animate attributeName="width" values="0;{lvl * bw:.0f}" dur="0.8s" begin="{t}s" fill="freeze" {EASE}/></rect>')
            else:
                out += f'<rect x="{bx}" y="{by}" width="{lvl * bw:.0f}" height="7" rx="2" fill="{col}"/>'
    return hidden_until(out, begin)


def s08():
    world = board_world_all()
    world += task_panel([[0, l, l * 1.08, l] for _, l in METRICS], 0.9, times=[1.2, 2.0, 2.8, 3.6])
    world += skill_panel(1.2, grow=1.6)
    # results stream in from the board
    for k in range(3):
        world += flow(f"M{R0 - 60} {metric_y(k)} L{TASK[0] + 4} {metric_y(k)}", CYAN, 1.4, 1.0 + k * 0.3, 1, size=7)
    # reports pile up; someone has to read them and decide
    world += pop(node("user", "You", 52, TEXT), *YOU, 2.4)
    world += line(SKILLP[0] + SKILLP[2], YOU[1], YOU[0] - 26, YOU[1], WIRE, 2, None, 2.4)
    world += flow(f"M{SKILLP[0] + SKILLP[2]} {YOU[1]} L{YOU[0] - 26} {YOU[1]}", MUTED, 0.6, 2.6, 4, size=6)
    for k in range(9):
        el = f'<rect x="{YOU[0] + 60}" y="{186 - k * 11}" width="40" height="8" rx="2" fill="{MUTED}"/>'
        world += hidden_until(el, 2.8 + k * 0.25)
    world += hidden_until(text(YOU[0] + 80, 212, "Unread", 11, MUTED), 2.8)
    world += pop(node("circle-help", None, 28, YELLOW, stroke=YELLOW), YOU[0], YOU[1] - 56, 3.6)
    world += alert(YOU[0] + 80, 66, 5.0)
    body = camera(world, 0, R0)
    return write("s08", body, "Reports track cost, cycle time and rework per task, and rework with and without each skill; they pile up until someone reads them.")


def s09():
    world = board_world_all()
    # goals above the reports: a target line on every metric
    world += pop(node("target", None, 44, ORANGE, stroke=ORANGE, glow=True), *GOALS, 0.3)
    world += hidden_until(text(GOALS[0] + 34, GOALS[1] + 5, "Goals", 13, TEXT, "start"), 0.4)
    x, y, w, h = TASK
    bx, bw = x + 130, 150
    out = panel(x, y, w, h, "Per Task", "chart-column")
    for k, (lab, lvl) in enumerate(METRICS):
        my = metric_y(k)
        out += text(x + 16, my + 4, lab, 11, TEXT, "start")
        goal = GOAL_LEVELS[k]
        t0 = 2.4 + k * 0.4
        out += g.bar(bx, my - 6, bw, 12, [lvl, lvl, goal], [0, t0, t0 + 1.6], [CYAN, CYAN, LIME], rx=2)
        gx = bx + goal * bw
        out += hidden_until(f'<path d="M{gx:.0f} {my - 12} V{my + 12}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="3 3"/>', 0.8 + k * 0.15)
    world += out
    # Rework is measured, never tuned: locked
    world += pop(icon("lock", 0, 0, 14, ORANGE), x + 104, metric_y(2), 1.6)
    world += hidden_until(text(x + 16, metric_y(2) + 22, "Locked: Cannot Tune", 10, ORANGE, "start"), 1.7)
    world += skill_panel()
    # the tuner turns the dials for rubrics, skills and workflows
    world += pop(node("bot", "Tuner", 52, ORANGE, stroke=ORANGE), *TUNER, 1.0)
    goal_wire = f"M{GOALS[0] + 90} {GOALS[1]} H{TUNER[0]} V{TUNER[1] - 26}"
    world += hidden_until(path_el(goal_wire, ORANGE, 1.5, "4 5"), 1.0)
    world += flow(goal_wire, ORANGE, 1.4, 1.2, 2, size=7)
    for n, (lab, dy) in enumerate(DIALS):
        tx = R0 + 850
        world += hidden_until(text(tx, dy - 12, lab, 12, TEXT, "start"), 1.4 + n * 0.15)
        world += hidden_until(f'<path d="M{tx} {dy + 4} H{tx + 110}" stroke="{WIRE}" stroke-width="3" stroke-linecap="round"/>', 1.4 + n * 0.15)
        world += hidden_until(path_el(f"M{TUNER[0] + 26} {TUNER[1]} L{tx - 8} {dy + 4}", WIRE, 1.5), 1.4 + n * 0.15)
        a, b, c = [(20, 80, 60), (90, 30, 70), (40, 95, 55)][n]
        knob = (f'<rect x="-6" y="-8" width="12" height="16" rx="2" fill="{ORANGE}" transform="translate({a} 0)">'
                f'<animateTransform attributeName="transform" type="translate" values="{a} 0;{b} 0;{c} 0" keyTimes="0;0.55;1" '
                f'dur="2.4s" begin="{2.0 + n * 0.3}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/></rect>')
        world += hidden_until(f'<g transform="translate({tx} {dy + 4})">{knob}</g>', 1.4 + n * 0.15)
        world += flow(f"M{TUNER[0] + 26} {TUNER[1]} L{tx - 8} {dy + 4}", ORANGE, 1.0, 2.0 + n * 0.3, 1, size=6)
    body = camera(world, R0, R0)
    return write("s09", body, "Goals sit above the reports; a tuner agent turns the dials for rubrics, skills and workflows until the metrics reach them, and rework stays locked.")


if __name__ == "__main__":
    names = [fn() for fn in (s01, s02, s03, s04, s05, s06, s07, s08, s09)]
    print(" ".join(names))
