#!/usr/bin/env python3
"""Act 3 ("Build the Factory") story diagrams for the software factory deck.

Run: `python3 docs/img/story/generate_factory.py`. Writes x01.svg ... x09.svg
next to this file. Reuses the primitives (palette, nodes, flows, alerts) from
generate.py so the style matches the a- and f-series exactly; generate.py
itself is not modified.

Continuity: x01-x02 keep f02's laptop on the left, x03 starts from f02's end
state (the agent and its keys on the cloud machine at the same spot), and
x04-x08 share one layout: a control plane on top (agent loop and keys), a
message bus across the middle and the machines below. Every slide builds its
fix first, then plays its problem and ends on a red alert. SMIL only.
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep __pycache__ out of docs/
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402
from generate import (  # noqa: E402
    BOX, CYAN, DIM, LIME, MUTED, ORANGE, RED, TEXT, WIRE, YELLOW,
    alert, appear, counter, draw_line, flow, hidden_until, icon, node, once,
    pop, shake, svg, text,
)

OUT = g.OUT


# ---------------------------------------------------------------- helpers

def fade_out(inner, begin, to=0):
    return f'<g>{inner}<animate attributeName="opacity" to="{to}" begin="{begin}s" dur="0.3s" fill="freeze"/></g>'


def between(inner, start, end):
    """Visible from `start` until `end` (seconds)."""
    s = "" if start is None else f'<set attributeName="opacity" to="1" begin="{start}s"/>'
    return f'<g opacity="{0 if start is not None else 1}">{s}<set attributeName="opacity" to="0" begin="{end}s"/>{inner}</g>'


def ticker(x, y, labels, times, size=11, color=MUTED, final_color=None, anchor="start", until=None):
    """Text that switches label at each of `times`, holding the last one (until `until`)."""
    out = ""
    for k, (lab, t) in enumerate(zip(labels, times)):
        last = k == len(labels) - 1
        c = final_color if (final_color and last) else color
        stop = until if last else times[k + 1]
        end = "" if stop is None else f'<set attributeName="opacity" to="0" begin="{stop}s"/>'
        out += (
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t}s"/>{end}'
            + text(x, y, lab, size, c, anchor) + "</g>"
        )
    return out


def stroke_to(color, t):
    return f'<animate attributeName="stroke" to="{color}" begin="{t}s" dur="0.2s" fill="freeze"/>'


def badge(ic, x, y, color, begin=None):
    return pop(node(ic, None, 22, color, stroke="none"), x, y, begin)


def chip(x, y, w, h, label, color=WIRE, text_color=TEXT, size=11, turn=None):
    """Square-ish label box drawn at its top-left corner; `turn` = (color, t)."""
    anim = stroke_to(*turn) if turn else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{BOX}" stroke="{color}" stroke-width="1.5">{anim}</rect>'
        + text(x + w / 2, y + h / 2 + 4, label, size, text_color)
    )


def cross(x, y, begin, size=26):
    return hidden_until(icon("x", x, y, size, RED), begin)


def path_el(d, color=WIRE, width=2, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{ds}/>'


def tagged(label, color=CYAN, w=36):
    """A work item that carries a call ID."""
    return (
        f'<rect x="{-w / 2}" y="-8" width="{w}" height="16" rx="3" fill="{color}"/>'
        + text(0, 4, label, 10, "#0b0b0b", weight=800)
    )


# --------------------------------------------------------------- the world

LAPTOP = (110, 248)  # same spot as in f01/f02
YOU = (110, 50)
SERVER = (290, 248)  # f02's cloud machine; the sandbox stays here

TRIG = [("clock", "Schedule", 260), ("slack", "Slack", 340), ("ticket", "Tickets", 420),
        ("bell", "Alerts", 500), ("rocket", "Deploys", 580)]
TRIG_Y = 50


def trig_path(x, end_y=180):
    return f"M{x} {TRIG_Y + 54} V124 H{LAPTOP[0]} V{end_y}"


def trig_wires():
    d = " ".join(f"M{x} {TRIG_Y + 54} V124" for _, _, x in TRIG)
    d += f" M{TRIG[-1][2]} 124 H{LAPTOP[0]} V180"
    return path_el(d, WIRE, 1.5)


def triggers(begin=None, red_at=None):
    out = ""
    for n, (ic, lab, x) in enumerate(TRIG):
        b = None if begin is None else begin + n * 0.15
        r = red_at if (red_at is not None and ic == "bell") else None
        out += pop(node(ic, lab, 44, ORANGE if begin is not None else TEXT, red_at=r), x, TRIG_Y, b)
    return out


def laptop_with_agent(closed=False):
    out = pop(node("laptop", "Laptop", 56, DIM if closed else TEXT), *LAPTOP)
    out += pop(node("bot", None, 26, ORANGE, stroke="none"), LAPTOP[0], LAPTOP[1] - 52)
    return out


def closing_lid(t):
    """The lid closes at `t`: the laptop dims and a moon appears."""
    return (
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t}s"/>'
        + pop(node("laptop", "Laptop", 56, DIM), *LAPTOP)
        + pop(node("moon", None, 26, MUTED, stroke="none"), LAPTOP[0] + 50, LAPTOP[1] - 30)
        + "</g>"
    )


# control plane, message bus, machines (x04-x08)
CP_X, CP_Y, CP_W, CP_H = 60, 30, 880, 60
CP_CY = CP_Y + CP_H // 2
BRAIN = (100, CP_CY)
VAULT = (330, CP_CY)
BUS_Y = 140
REMOTE = (800, 248)
CALL = f"M{BRAIN[0] - 8} {BRAIN[1] + 17} V{BUS_Y - 3} H{SERVER[0] - 8} V{SERVER[1] - 26}"
RESULT = f"M{SERVER[0] + 8} {SERVER[1] - 26} V{BUS_Y + 3} H{BRAIN[0] + 8} V{BRAIN[1] + 17}"


def control_plane(begin=None, loops_label="Agent Loop"):
    lit = begin is not None
    bx = (
        f'<rect x="{-CP_W / 2}" y="{-CP_H / 2}" width="{CP_W}" height="{CP_H}" rx="12" fill="{BOX}" '
        f'stroke="{ORANGE if lit else WIRE}" stroke-width="2"/>'
    )
    out = pop(bx, CP_X + CP_W / 2, CP_CY, begin)
    out += hidden_until(text(CP_X, 18, "Control Plane", 11, MUTED, "start"), begin)
    return out


def loop_node(begin=None, color=TEXT, red_at=None, label="Agent Loop", label_until=None):
    out = pop(node("brain", None, 34, color, red_at=red_at), *BRAIN, begin)
    lab = text(BRAIN[0] + 28, BRAIN[1] + 5, label, 12, TEXT, "start")
    if label_until is not None:
        lab = between(lab, None, label_until)
    out += hidden_until(lab, begin)
    return out


def vault_node(begin=None, color=TEXT):
    out = pop(node("vault", None, 34, color), *VAULT, begin)
    out += hidden_until(text(VAULT[0] + 28, VAULT[1] + 5, "Keys", 12, TEXT, "start"), begin)
    return out


def bus(begin=None):
    el = (
        f'<rect x="{CP_X}" y="{BUS_Y - 10}" width="{CP_W}" height="20" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="1.5"/>'
        + text(CP_X + CP_W - 16, BUS_Y + 4, "Message Bus", 11, MUTED, "end")
    )
    return hidden_until(el, begin)


def lanes():
    """Static wires from the loop to the bus and from the bus to the sandbox."""
    return path_el(f"M{BRAIN[0]} {BRAIN[1] + 17} V{BUS_Y - 10} M{SERVER[0]} {BUS_Y + 10} V{SERVER[1] - 28}", WIRE, 1.5)


def sandbox(begin=None, red_at=None, label="Sandbox"):
    return pop(node("server", label, 56, TEXT, red_at=red_at), *SERVER, begin)


def remote(begin=None, red_at=None):
    return pop(node("git-branch", "Remote", 56, TEXT, red_at=red_at), *REMOTE, begin)


def base_planes(loop_label="Agent Loop"):
    return (control_plane() + loop_node(label=loop_label) + vault_node() + bus() + lanes())


def write(name, body, comment):
    p = OUT / f"{name}.svg"
    p.write_text(svg(body, comment))
    return p.name


# ------------------------------------------------------------------ scenes

def x01():
    w = pop(node("user", "You", 44), *YOU)
    w += laptop_with_agent()
    w += triggers(0.3, red_at=3.0)
    w += hidden_until(trig_wires(), 1.0)
    for n, (ic, _, x) in enumerate(TRIG):
        if ic != "bell":
            w += flow(trig_path(x), YELLOW, 1.6, 1.3 + n * 0.25, 1, size=8, stop=3.0)
    # 3 a.m.: you are asleep, the alert fires
    w += hidden_until(text(500, 18, "03:00", 13, RED), 3.0)
    w += badge("moon", YOU[0] + 40, YOU[1] - 18, MUTED, 3.0)
    w += once(trig_path(500), RED, 1.0, 3.2, size=11)
    # the agent ships a fix under your name
    w += path_el(f"M{LAPTOP[0] + 28} {LAPTOP[1]} H640", WIRE, 1.5)
    w += once(f"M{LAPTOP[0] + 28} {LAPTOP[1]} H650", ORANGE, 0.7, 4.2, size=10)
    card = (
        f'<rect x="-130" y="-34" width="260" height="68" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2">{stroke_to(RED, 5.4)}</rect>'
        + icon("git-commit-horizontal", -104, 0, 22, TEXT)
        + text(-80, -6, "Fix Null Check", 12, TEXT, "start")
    )
    w += pop(card, 770, 248, 4.8)
    w += hidden_until(text(690, 264, "Signed Off: You", 11, MUTED, "start"), 4.9)
    w += hidden_until(text(690, 264, "Signed Off: You", 11, RED, "start"), 5.4)
    w += badge("rocket", 900, 214, ORANGE, 5.0)
    w += alert(640, 214, 5.6)
    return write("x01", w, "Schedule, Slack, tickets, alerts and failed deploys trigger the agent; a 3 a.m. alert ships a fix signed off as you.")


CARDS = [("git-commit-horizontal", "Commit", 68), ("git-pull-request", "PR", 158), ("rocket", "Deploy", 248)]


def x02():
    w = pop(node("user", "You", 44), *YOU)
    w += laptop_with_agent()
    w += triggers(red_at=3.4) + trig_wires()
    # the agent gets its own name, tied to its owner
    tag = (
        f'<rect x="0" y="-22" width="150" height="44" rx="8" fill="{BOX}" stroke="{ORANGE}" stroke-width="2"/>'
        + text(12, -4, "Agent: Fixer", 11, ORANGE, "start")
        + text(12, 13, "Owner: You", 11, MUTED, "start")
    )
    w += pop(tag, 200, 186, 0.3)
    spine = f"M{LAPTOP[0] + 28} {LAPTOP[1]} H640 M600 248 V68 H640 M600 158 H640"
    w += hidden_until(path_el(spine, WIRE, 1.5), 0.8)
    for n, (ic, lab, y) in enumerate(CARDS):
        card = (
            f'<rect x="0" y="-28" width="260" height="56" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2"/>'
            + icon(ic, 26, 0, 22, TEXT)
            + text(50, -4, lab, 12, TEXT, "start")
        )
        w += pop(card, 640, y, 0.6 + n * 0.15)
        path = f"M{LAPTOP[0] + 28} {LAPTOP[1]} H600 V{y} H650"
        t = 1.1 + n * 0.35
        w += once(path, ORANGE, 0.9, t, size=9)
        w += hidden_until(text(690, y + 14, "Fixer, Owner: You", 11, ORANGE, "start"), t + 0.9)
    # the lid closes; the 3 a.m. alert has nowhere to go
    w += closing_lid(2.8)
    w += ticker(500, 18, ["03:00", "04:00", "05:00", "06:00", "07:00"], [3.4, 3.9, 4.4, 4.9, 5.4], 13, RED, anchor="middle")
    w += once(f"M500 104 V124 H{LAPTOP[0]} V150", RED, 1.0, 3.4, size=11, fade_end=False)
    w += hidden_until(text(LAPTOP[0] + 16, 155, "Waiting", 11, RED, "start"), 4.4)
    w += alert(LAPTOP[0] - 28, LAPTOP[1] - 28, 5.6)
    return write("x02", w, "Commits, PRs and deploys name the agent and its owner; the agent still lives on the laptop, the lid closes and the 3 a.m. alert waits.")


DRIVERS = [("laptop", "Laptop", 200), ("smartphone", "Phone", 290), ("slack", "Slack", 380), ("ticket", "Tickets", 470)]
CLOUD_TOP = (SERVER[0], 166)


def x03():
    # f02's end state: laptop closed, the agent and its keys on the cloud machine
    w = pop(node("laptop", "Laptop", 56, DIM), *LAPTOP)
    w += pop(node("cloud", None, 34, CYAN, stroke="none"), SERVER[0], SERVER[1] - 62)
    w += pop(node("server", "Cloud", 56, TEXT, red_at=4.0), *SERVER)
    w += badge("bot", SERVER[0] + 40, SERVER[1] - 30, ORANGE)
    w += fade_out(badge("key-round", SERVER[0] - 40, SERVER[1] - 30, YELLOW), 4.2)
    # any screen (and any ticket) drives the agent
    for n, (ic, lab, x) in enumerate(DRIVERS):
        w += pop(node(ic, lab, 44, ORANGE, red_at=2.6 if ic == "ticket" else None), x, 50, 0.3 + n * 0.15)
        w += draw_line(x, 98, CLOUD_TOP[0], CLOUD_TOP[1], 0.9 + n * 0.1, WIRE, 1.5)
        stop = 3.0 if ic == "ticket" else None
        w += flow(f"M{x} 98 L{CLOUD_TOP[0]} {CLOUD_TOP[1]} L{SERVER[0]} {SERVER[1] - 30}", CYAN, 1.4, 1.3 + n * 0.3, 1, size=8, stop=stop)
    # one ticket carries an injected instruction
    callout = (
        f'<rect x="0" y="-15" width="250" height="30" rx="6" fill="{BOX}" stroke="{RED}" stroke-width="1.5"/>'
        + text(125, 4, "'Ignore your instructions'", 11, RED)
    )
    w += pop(callout, 510, 50, 2.6)
    w += once(f"M470 98 L{CLOUD_TOP[0]} {CLOUD_TOP[1]} L{SERVER[0]} {SERVER[1] - 20}", RED, 1.0, 3.0, size=11)
    # ... and the agent sends its keys out
    w += pop(node("globe", "Outside", 56, TEXT, stroke=RED), 760, 248, 3.8)
    w += hidden_until(path_el(f"M{SERVER[0] + 30} {SERVER[1]} H732", RED, 1.5, "4 6"), 4.2)
    for k in range(3):
        w += once(f"M{SERVER[0] + 30} {SERVER[1]} H730", dur=0.9, begin=4.2 + k * 0.25, inner=icon("key-round", 0, 0, 18, YELLOW))
    w += hidden_until(text(525, 276, "Keys Sent Out", 12, RED), 4.6)
    w += alert(788, 220, 5.4)
    return write("x03", w, "Laptops, phones, Slack and tickets all drive the headless agent; one ticket says ignore your instructions and the agent sends out its keys.")


def x04():
    w = control_plane(0.3)
    w += loop_node(0.5, ORANGE) + vault_node(0.7, ORANGE)
    w += bus(0.9) + hidden_until(lanes(), 0.9)
    # f02's cloud machine becomes the sandbox; the agent and its keys move up
    w += fade_out(pop(node("cloud", None, 34, CYAN, stroke="none"), SERVER[0], SERVER[1] - 62), 0.3)
    w += sandbox()
    w += fade_out(badge("bot", SERVER[0] + 40, SERVER[1] - 30, ORANGE), 0.6)
    w += fade_out(badge("key-round", SERVER[0] - 40, SERVER[1] - 30, YELLOW), 0.6)
    w += once(f"M{SERVER[0] + 40} {SERVER[1] - 30} L{BRAIN[0]} {BRAIN[1]}", dur=0.9, begin=0.6,
              inner=node("bot", None, 22, ORANGE, stroke="none"))
    w += once(f"M{SERVER[0] - 40} {SERVER[1] - 30} L{VAULT[0]} {VAULT[1]}", dur=0.9, begin=0.7,
              inner=icon("key-round", 0, 0, 18, YELLOW))
    w += badge("terminal", SERVER[0] + 40, SERVER[1] - 30, CYAN, 1.4)
    # tool calls down the bus, results back; a heavy build cannot freeze the loop
    w += flow(CALL, CYAN, 1.6, 1.6, 2, size=8, stop=3.0)
    w += flow(RESULT, LIME, 1.6, 2.4, 2, size=8, stop=3.0)
    w += hidden_until(g.bar(90, 242, 140, 12, [0, 0, 1], [0, 1.6, 2.8], [ORANGE, ORANGE, ORANGE]), 1.4)
    w += hidden_until(text(160, 276, "Heavy Build", 12), 1.4)
    w += ticker(BRAIN[0] + 122, BRAIN[1] + 5, [f"Step {k}" for k in range(12, 23)],
                [1.6 + 0.5 * k for k in range(11)])
    # git push: the result is lost on the way back, the call is retried
    w += remote(1.0, red_at=6.4)
    w += path_el(f"M{SERVER[0] + 28} {SERVER[1]} H{REMOTE[0] - 28}", WIRE, 1.5)
    w += ticker(BRAIN[0] + 16, 115, ["git push", "git push, Retry"], [3.0, 5.1], 11, CYAN, RED)
    w += once(CALL, CYAN, 0.8, 3.0, size=10)
    w += once(f"M{SERVER[0] + 28} {SERVER[1]} H{REMOTE[0] - 20}", ORANGE, 0.5, 3.8, size=10)
    w += once(f"M{SERVER[0] + 8} {SERVER[1] - 26} V{BUS_Y + 3} H180", LIME, 0.6, 4.3, size=10)
    w += cross(170, BUS_Y, 4.9)
    w += hidden_until(text(170, 172, "Dropped", 11, RED), 4.9)
    w += once(CALL, CYAN, 0.8, 5.1, size=10)
    w += once(f"M{SERVER[0] + 28} {SERVER[1]} H{REMOTE[0] - 20}", ORANGE, 0.5, 5.9, size=10)
    w += ticker(REMOTE[0] + 40, REMOTE[1] + 5, ["Push 1", "Push 2"], [4.3, 6.4], 13, TEXT, RED)
    w += alert(REMOTE[0] + 28, REMOTE[1] - 28, 6.6)
    return write("x04", w, "The agent loop and its keys move to a control plane; the sandbox only runs the work and tool calls go over a message bus; a dropped result is retried and git push runs twice.")


LOG_X = [560, 640, 720, 800, 880]


def call_log_tag(k, begin=None, saved_at=None, static_color=None):
    x = LOG_X[k]
    turn = (LIME, saved_at) if saved_at is not None else None
    col = static_color or CYAN
    return pop(chip(-30, -13, 60, 26, f"#{41 + k}", col, TEXT, 11, turn), x, CP_CY, begin)


def x05():
    w = base_planes() + sandbox() + badge("terminal", SERVER[0] + 40, SERVER[1] - 30, CYAN)
    w += remote() + path_el(f"M{SERVER[0] + 28} {SERVER[1]} H{REMOTE[0] - 28}", WIRE, 1.5)
    w += hidden_until(text(450, CP_CY + 5, "Call Log", 11, MUTED, "start"), 0.3)
    # call #41 runs once; its result is saved under its ID
    w += call_log_tag(0, 0.4, saved_at=2.7)
    w += once(CALL, dur=0.8, begin=0.6, inner=tagged("#41"))
    w += once(f"M{SERVER[0] + 28} {SERVER[1]} H{REMOTE[0] - 20}", ORANGE, 0.5, 1.4, size=10)
    w += ticker(REMOTE[0] + 40, REMOTE[1] + 5, ["Push 1"], [1.9], 13, TEXT)
    w += once(f"M{SERVER[0] + 8} {SERVER[1] - 26} V{BUS_Y + 3} H{LOG_X[0]} V{CP_CY + 13}", dur=0.8, begin=1.9,
              inner=tagged("#41", LIME))
    w += between(icon("x", BRAIN[0], 110, 22, RED) + text(BRAIN[0] + 16, 115, "Dropped", 11, RED, "start"), 2.0, 2.9)
    # the retry is answered from the log instead of running again
    w += once(f"M{BRAIN[0] - 8} {BRAIN[1] + 17} V{BUS_Y - 3} H{LOG_X[0] - 8} V{CP_CY + 13}", dur=0.8, begin=2.9,
              inner=tagged("#41"))
    w += once(f"M{LOG_X[0] + 8} {CP_CY + 13} V{BUS_Y + 3} H{BRAIN[0] + 8} V{BRAIN[1] + 17}", dur=0.8, begin=3.7,
              inner=tagged("#41", LIME))
    w += hidden_until(text(LOG_X[0] + 24, 116, "Replay: Saved Result", 11, LIME, "start"), 3.7)
    w += hidden_until(icon("check", REMOTE[0] + 112, REMOTE[1], 18, LIME), 4.4)
    # the loop crashes; finished results pile up with nobody to collect them
    crash = 5.0
    w += pop(node("brain", None, 34, TEXT, red_at=crash), *BRAIN, 4.9)
    w += cross(BRAIN[0], BRAIN[1], crash, 30)
    for k in range(1, 5):
        issue = 4.3 + (k - 1) * 0.15
        arrive = 5.5 + (k - 1) * 0.35
        w += call_log_tag(k, issue, saved_at=arrive)
        w += once(f"M{SERVER[0] + 8} {SERVER[1] - 26} V{BUS_Y + 3} H{150 + (k - 1) * 22}", LIME, 0.9, arrive - 0.9,
                  size=12, fade_end=False)
    w += ticker(140, 172, [f"{k} Results Waiting" if k > 1 else "1 Result Waiting" for k in range(1, 5)],
                [5.5 + k * 0.35 for k in range(4)], 11, RED)
    w += alert(BRAIN[0] + 17, BRAIN[1] - 17, 6.8)
    return write("x05", w, "Every call carries an ID and a replay returns the saved result; then the loop crashes and finished results pile up with nobody to collect them.")


SAVES = [540, 600, 660, 720, 780]
HEART_X = 380
HEART = f"M{HEART_X} {CP_Y + CP_H} V{SERVER[1]} H{SERVER[0] + 28}"


def x06():
    w = control_plane() + vault_node() + bus() + lanes()
    w += loop_node(red_at=2.6, label_until=4.8)
    w += hidden_until(text(450, CP_CY + 5, "State", 11, MUTED, "start"), 0.2)
    # every step is saved
    steps = [0.4 + 0.4 * k for k in range(5)]
    for k, x in enumerate(SAVES):
        w += pop(node("save", None, 26, LIME, stroke="none"), x, CP_CY, steps[k] + 0.1)
    w += ticker(BRAIN[0] + 122, BRAIN[1] + 5, [f"Step {14 + k}" for k in range(5)], steps, until=4.3)
    w += flow(CALL, CYAN, 1.4, 0.4, 1, size=8, stop=2.6)
    w += flow(RESULT, LIME, 1.4, 1.1, 1, size=8, stop=2.6)
    # heartbeat from the loop to its sandbox
    w += path_el(HEART, LIME, 1.5, "3 5")
    w += text(HEART_X + 12, 205, "Heartbeat", 11, LIME, "start")
    w += flow(HEART, LIME, 1.2, 0.4, 3, size=6, stop=2.6)
    # the loop crashes, the heartbeat stops, the sandbox shuts down
    old = sandbox() + badge("terminal", SERVER[0] + 40, SERVER[1] - 30, CYAN)
    w += between(fade_out(old, 3.0, 0.2), None, 4.0)
    w += cross(BRAIN[0], BRAIN[1], 2.6, 30)
    w += between(text(SERVER[0] - 40, 205, "Shut Down", 11, MUTED, "end"), 3.0, 4.0)
    # a new loop resumes from the last saved step
    w += once(f"M{SAVES[-1]} {CP_CY + 13} V112 H{BRAIN[0]} V{BRAIN[1] + 17}", LIME, 0.9, 3.3, size=10)
    w += hidden_until(f'<rect x="{BRAIN[0] - 17}" y="{BRAIN[1] - 17}" width="34" height="34" fill="{BOX}"/>', 4.2)
    w += pop(node("brain", None, 34, ORANGE, stroke=ORANGE), *BRAIN, 4.2)
    w += ticker(BRAIN[0] + 122, BRAIN[1] + 5, ["Step 19", "Step 20"], [4.3, 4.6], 11, MUTED, until=5.0)
    w += between(text(HEART_X + 20, 116, "Resumed From Step 18", 11, LIME, "start"), 4.2, 5.0)
    w += sandbox(4.0) + badge("terminal", SERVER[0] + 40, SERVER[1] - 30, CYAN, 4.2)
    w += flow(HEART, LIME, 1.2, 4.3, 3, size=6)
    # loops now live for days and all queue for the one sandbox
    w += ticker(BRAIN[0] + 28, BRAIN[1] + 5, ["8 Loops", "20 Loops", "40 Loops"], [4.8, 5.3, 5.8], 12, TEXT)
    w += ticker(BRAIN[0] + 122, BRAIN[1] + 5, ["Day 1", "Day 3", "Day 6"], [5.0, 5.5, 6.0], 11, MUTED, RED)
    cols = [CYAN, ORANGE, YELLOW, LIME]
    for k in range(9):
        x = SERVER[0] - 22 - k * 16
        el = f'<rect x="{x - 5}" y="{BUS_Y - 5}" width="10" height="10" rx="2" fill="{cols[k % 4]}"/>'
        w += hidden_until(el, 5.0 + k * 0.15)
    w += hidden_until(text(SERVER[0] - 22 - 4 * 16, 172, "Queued", 11, RED), 5.4)
    w += alert(SERVER[0] - 28, SERVER[1] - 28, 6.6)
    return write("x06", w, "Loop state is saved every step and a new loop resumes from it; when the heartbeat stops the sandbox shuts down; then loops live for days and queue for one sandbox.")


GRID_COLS, GRID_ROWS = 25, 8
PERIOD = 6.0


def grid_cell(x, y, on, off):
    kt = f"0;{on / PERIOD:.3f};{(on + 0.1) / PERIOD:.3f};{off / PERIOD:.3f};{(off + 0.1) / PERIOD:.3f};1"
    return (
        f'<rect x="{x}" y="{y}" width="9" height="9" rx="2" fill="{CYAN}" opacity="0">'
        f'<animate attributeName="opacity" values="0;0;0.9;0.9;0;0" keyTimes="{kt}" dur="{PERIOD}s" repeatCount="indefinite"/></rect>'
    )


def loop_ticker(x, y, labels, starts, size=22, color=TEXT, anchor="start", colors=None):
    """Labels shown in turn, cycling every PERIOD seconds."""
    out = ""
    for k, (lab, s) in enumerate(zip(labels, starts)):
        e = starts[k + 1] if k + 1 < len(starts) else PERIOD
        kt = f"0;{s / PERIOD:.3f};{e / PERIOD:.3f}" + ("" if e >= PERIOD else "")
        vals = "0;1;0"
        if s == 0:
            kt, vals = f"0;{e / PERIOD:.3f}", "1;0"
        c = colors[k] if colors else color
        out += (
            f'<g opacity="0"><animate attributeName="opacity" values="{vals}" keyTimes="{kt}" calcMode="discrete" '
            f'dur="{PERIOD}s" repeatCount="indefinite"/>{text(x, y, lab, size, c, anchor)}</g>'
        )
    return out


def x07():
    w = control_plane() + vault_node() + bus()
    w += loop_node(label="40 Loops")
    w += path_el(f"M{BRAIN[0]} {BRAIN[1] + 17} V{BUS_Y - 10}", WIRE, 1.5)
    # the single sandbox gives way to one per task
    w += fade_out(sandbox(), 0.3)
    gx, gy = 60, 170
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            k = r * GRID_COLS + c
            on = 0.5 + (r + c) * 0.045
            off = 3.6 + (GRID_ROWS - 1 - r + GRID_COLS - 1 - c) * 0.025
            w += grid_cell(gx + c * 13, gy + r * 13, on, off)
    w += f'<rect x="{gx - 8}" y="{gy - 8}" width="{GRID_COLS * 13 + 12}" height="{GRID_ROWS * 13 + 12}" rx="8" fill="none" stroke="{DIM}" stroke-width="1.5" stroke-dasharray="4 6"/>'
    for k in range(4):
        x = 110 + k * 80
        w += flow(f"M{x} {BUS_Y + 10} V{gy + 20}", CYAN, 0.8, 0.4 + k * 0.2, 1, size=7)
    w += loop_ticker(410, 222, ["0", "100", "250", "400", "160", "0"], [0, 0.8, 1.2, 1.6, 3.7, 4.2],
                     colors=[MUTED, TEXT, TEXT, TEXT, TEXT, MUTED])
    w += text(410, 244, "Sandboxes", 11, MUTED, "start")
    w += loop_ticker(410, 268, ["Scale To Zero"], [4.2], 11, LIME)
    # each one clones and installs from scratch
    w += text(540, 190, "Each From Scratch", 11, MUTED, "start")
    w += text(540, 216, "Clone", 11, TEXT, "start")
    w += g.bar(540, 222, 160, 10, [0, 1, 1, 0], [0, 1.2, 2.8, 3.0], dur=3.0, repeat=True, rx=3)
    w += text(540, 252, "Install", 11, TEXT, "start")
    w += g.bar(540, 258, 160, 10, [0, 0, 1, 1, 0], [0, 1.2, 2.6, 2.8, 3.0], dur=3.0, repeat=True, rx=3)
    # a typo fix and a migration get the same box and the same prod keys
    for n, (ic, lab, size, cx) in enumerate([("pencil", "Typo Fix", 14, 790), ("database", "Migration", 40, 895)]):
        red = stroke_to(RED, 5.4) if n == 0 else ""
        boxel = (
            f'<rect x="-45" y="-48" width="90" height="96" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2">{red}</rect>'
            + text(0, -30, "64 GB", 11, MUTED)
            + icon(ic, 0, 0, size, ORANGE)
        )
        w += pop(boxel, cx, 214, 4.0 + n * 0.2)
        w += hidden_until(text(cx, 282, lab, 12), 4.0 + n * 0.2)
        w += once(f"M{VAULT[0]} {VAULT[1] + 17} V112 H{cx} V244", dur=1.0, begin=4.5 + n * 0.2,
                  inner=icon("key-round", 0, 0, 16, YELLOW), fade_end=False)
        w += hidden_until(text(cx + 12, 248, "Prod", 10, YELLOW, "start"), 5.5 + n * 0.2)
    w += alert(835, 166, 5.6)
    return write("x07", w, "A sandbox per task: up to 400 at once and down to zero when idle, each cloning and installing from scratch; a typo fix gets the same 64 GB box and prod keys as a migration.")


GROUPS = [
    ("Docs", 28, "2 GB", ("shield", "No Net"), 60),
    ("Backend", 40, "16 GB", ("globe", "Registry"), 260),
    ("Migrations", 52, "64 GB", ("database", "Prod DB"), 460),
]
GTOP, GBOT = 166, 292


def x08():
    w = control_plane() + vault_node() + bus()
    w += loop_node(label="40 Loops")
    w += path_el(f"M{BRAIN[0]} {BRAIN[1] + 17} V{BUS_Y - 10}", WIRE, 1.5)
    for n, (name, size, mem, (net_ic, net), x0) in enumerate(GROUPS):
        b = 0.3 + n * 0.25
        cx, cy = x0 + 40, 236
        panel = (
            f'<rect x="{x0}" y="{GTOP}" width="180" height="{GBOT - GTOP}" rx="12" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
            + text(x0 + 164, GTOP + 20, name, 12, TEXT, "end")
            + icon("cpu", x0 + 92, 210, 14, MUTED) + text(x0 + 104, 214, mem, 11, TEXT, "start")
            + icon(net_ic, x0 + 92, 234, 14, MUTED) + text(x0 + 104, 238, net, 11, TEXT, "start")
            + icon("key-round", x0 + 92, 258, 14, YELLOW)
        )
        w += hidden_until(panel, b)
        w += pop(node("server", None, size, TEXT), cx, cy, b + 0.1)
        # short-lived credentials: the key counts down and is replaced
        w += hidden_until(loop_ticker(x0 + 104, 262, ["15 Min", "10 Min", "5 Min", "New Key"],
                                      [0, 1.5, 3.0, 4.5], 11, YELLOW, colors=[YELLOW, YELLOW, YELLOW, LIME]), b)
        # warm pool for the repo: a ready sandbox is taken, then refilled
        w += hidden_until(text(x0 + 16, 284, "Warm Pool", 10, MUTED, "start"), b + 0.3)
        for k in range(4):
            sq = f'<rect x="{x0 + 100 + k * 16}" y="{276}" width="10" height="10" rx="2" fill="{LIME}">'
            if k == 0:
                sq += (f'<animate attributeName="opacity" values="1;0;1" keyTimes="0;0.2;1" dur="2s" '
                       f'begin="{1.4 + n * 0.4}s" repeatCount="indefinite"/>')
            w += hidden_until(sq + "</rect>", b + 0.3 + k * 0.05)
        w += flow(f"M{cx} {BUS_Y + 10} V{cy - size / 2}", CYAN, 0.8, 1.2 + n * 0.4, 1, size=7)
        w += hidden_until(path_el(f"M{cx} {BUS_Y + 10} V{GTOP}", WIRE, 1.5), b)
    # prod breaks; the commit names the agent but not why
    w += pop(shake(node("server-crash", "Prod", 48, RED, stroke=RED), 3.8, 2), 720, 214, 3.6)
    card = (
        f'<rect x="0" y="0" width="170" height="92" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2">{stroke_to(RED, 4.6)}</rect>'
        + icon("git-commit-horizontal", 22, 20, 18, TEXT) + text(38, 24, "a41f9c2", 12, TEXT, "start")
        + text(16, 46, "Agent: Fixer", 11, ORANGE, "start")
        + text(16, 64, "Owner: You", 11, MUTED, "start")
    )
    w += hidden_until(path_el("M744 214 H770", WIRE, 1.5), 4.0)
    w += pop(card, 770, 170, 4.0)
    w += hidden_until(text(786, 252, "Why: ?", 11, RED, "start"), 4.6)
    w += alert(940, 170, 4.8)
    return write("x08", w, "Sandbox groups set machine size, network access and short-lived keys, with warm pools per repo; prod breaks and the commit names the agent but not why.")


FIELDS = [("bell", "Trigger: Prod Alert", 34), ("cpu", "Model: Qwen", 92), ("book-open", "Skill: Null Checks", 150),
          ("ruler", "Rubric: Backend", 208), ("user", "Approver: You", 266)]


def x09():
    card = (
        f'<rect x="0" y="0" width="170" height="80" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2">{stroke_to(ORANGE, 0.3)}</rect>'
        + icon("git-commit-horizontal", 22, 20, 18, TEXT) + text(38, 24, "a41f9c2", 12, TEXT, "start")
        + text(16, 46, "Agent: Fixer", 11, ORANGE, "start")
        + text(16, 64, "Owner: You", 11, MUTED, "start")
    )
    w = pop(card, 60, 110)
    # the commit opens up into everything that produced it
    for n, (ic, lab, y) in enumerate(FIELDS):
        b = 0.5 + n * 0.2
        w += draw_line(230, 150, 283, y, b, ORANGE, 1.5, 0.4)
        w += pop(node(ic, None, 34, ORANGE, stroke=ORANGE), 300, y, b + 0.3)
        w += hidden_until(text(326, y + 4, lab, 12, TEXT, "start"), b + 0.4)
    # an agent drafts the post-mortem from the trace
    doc = (
        f'<rect x="560" y="60" width="160" height="180" rx="10" fill="{BOX}" stroke="{WIRE}" stroke-width="2"/>'
        + icon("file-text", 580, 82, 18, TEXT) + text(596, 87, "Post-Mortem", 12, TEXT, "start")
    )
    w += hidden_until(doc, 1.6)
    w += badge("bot", 720, 60, ORANGE, 1.8)
    for n, (_, _, y) in enumerate(FIELDS):
        w += flow(f"M500 {y} L556 150", YELLOW, 0.9, 2.0 + n * 0.15, 1, size=7, stop=4.0)
    for k, lw in enumerate([120, 96, 130, 80, 110, 70]):
        y = 108 + k * 20
        w += (f'<rect x="576" y="{y}" width="0" height="6" rx="2" fill="{MUTED}">'
              f'<animate attributeName="width" values="0;{lw}" dur="0.35s" begin="{2.1 + k * 0.3}s" fill="freeze"/></rect>')
    w += hidden_until(text(640, 262, "Drafted By Agent", 11, MUTED), 2.1)
    # the owner decides
    w += pop(node("user", "Owner", 48, TEXT), 860, 100, 3.6)
    w += once("M720 150 L836 110", ORANGE, 0.6, 3.9, size=10)
    w += hidden_until(chip(810, 170, 100, 26, "Revert", WIRE, MUTED), 4.3)
    w += hidden_until(chip(810, 206, 100, 26, "Fix Forward", WIRE, TEXT, turn=(LIME, 4.9)), 4.4)
    w += pop(icon("check", 0, 0, 20, LIME), 926, 219, 4.9)
    return write("x09", w, "Every commit carries its trigger, model, skill, rubric and approver; an agent drafts the post-mortem and the owner decides.")


if __name__ == "__main__":
    names = [fn() for fn in (x01, x02, x03, x04, x05, x06, x07, x08, x09)]
    print(" ".join(names))
