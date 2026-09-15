"""
Wrap the Gojo-inspired portrait in a terminal-chrome SVG that GitHub can
animate (SMIL + CSS). Infinity rings, cursed-energy particles, and a soft
pulse sit over the painting. The PNG is embedded so the SVG is self-contained.
"""
import base64
import html
import io
import os
import random
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "assets", "gojo-portrait.png")
OUT = os.path.join(HERE, "..", "gojo-portrait.svg")
OUT_ALIAS = os.path.join(HERE, "..", "harshit-ascii.svg")

USER_HANDLE = os.environ.get("GH_PROFILE_USER", "EthanSharma-Wadeson")
FULL_NAME = os.environ.get("PROFILE_FULL_NAME", "Ethan Sharma-Wadeson")

CANVAS_W, CANVAS_H = 840, 875
TITLEBAR_H = 30
STATUS_H = 32
PAD = 14
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#0a1220"
TITLE_TEXT = "#7d8590"
INK = "#e6edf3"
CYAN = "#67e8f9"
CYAN_DEEP = "#22d3ee"
BLUE = "#38bdf8"

ART_X = PAD
ART_Y = TITLEBAR_H + 8
ART_W = CANVAS_W - PAD * 2
ART_H = CANVAS_H - TITLEBAR_H - STATUS_H - 16
CX = ART_X + ART_W / 2
CY = ART_Y + ART_H / 2


def embed_portrait():
    im = Image.open(SRC).convert("RGB")
    sw, sh = im.size
    # nearly-square art panel: keep the hair, crop extra jacket
    side = sw
    top = max(0, int(sh * 0.03))
    if top + side > sh:
        top = sh - side
    im = im.crop((0, top, sw, top + side))
    im = im.resize((720, 720), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=80, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def particles(rng):
    bits = []
    for i in range(22):
        x = rng.randint(int(ART_X + 40), int(ART_X + ART_W - 40))
        y0 = rng.randint(int(ART_Y + 40), int(ART_Y + ART_H - 80))
        r = rng.choice([1.2, 1.6, 2.0, 2.4])
        dur = rng.uniform(3.8, 7.5)
        delay = rng.uniform(0, 4)
        drift = rng.randint(70, 140)
        col = rng.choice([CYAN, CYAN_DEEP, BLUE, "#a5f3fc"])
        bits.append(
            f'<circle cx="{x}" cy="{y0}" r="{r}" fill="{col}" opacity="0">'
            f'<animate attributeName="cy" from="{y0}" to="{y0 - drift}" dur="{dur:.2f}s" '
            f'begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0.5;0" dur="{dur:.2f}s" '
            f'begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    return "".join(bits)


def rings():
    specs = [
        (300, 318, 18, 14, CYAN, 0.55, 18),
        (250, 268, -12, 22, BLUE, 0.4, 26),
        (340, 300, 8, 28, "#818cf8", 0.32, 34),
    ]
    out = []
    for i, (rx, ry, rot, dur, col, op, dash) in enumerate(specs):
        out.append(
            f'<ellipse cx="{CX:.1f}" cy="{CY:.1f}" rx="{rx}" ry="{ry}" fill="none" '
            f'stroke="{col}" stroke-width="1.6" stroke-dasharray="{dash} {dash // 2}" '
            f'opacity="{op}" transform="rotate({rot} {CX:.1f} {CY:.1f})">'
            f'<animateTransform attributeName="transform" type="rotate" '
            f'from="{rot} {CX:.1f} {CY:.1f}" to="{rot + 360} {CX:.1f} {CY:.1f}" '
            f'dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op * 0.45};{op};{op * 0.45}" '
            f'dur="{6 + i}s" repeatCount="indefinite"/>'
            f"</ellipse>"
        )
    return "".join(out)


KW = {
    "and", "as", "assert", "break", "class", "continue", "def", "elif", "else",
    "for", "from", "if", "import", "in", "lambda", "none", "not", "or", "pass",
    "return", "self", "true", "false", "while", "with", "yield",
}
TOKEN = re.compile(r"(#.*$)|(\".*?\"|'.*?')|\b([A-Za-z_][A-Za-z0-9_]*)\b|(\S+)|(\s+)")

CODE_LINES = [
    "from nve import NarrativeEngine",
    "from physics import Simulation",
    "import numpy as np",
    "",
    "engine = NarrativeEngine()",
    "drift = engine.semantic_shift(market)",
    "",
    "def train(model, world):",
    "    for x, y in world:",
    "        pred = model.forward(x)",
    "        model.backward(pred, y)",
    "    return model",
    "",
    "class Agent:",
    "    def __init__(self, policy):",
    "        self.policy = policy",
    "",
    "    def act(self, state):",
    "        return self.policy.sample(state)",
    "",
    "    def learn(self, reward):",
    "        self.policy.update(reward)",
    "",
    "def step(sim, dt=0.01):",
    "    acc = sim.forces() / sim.mass",
    "    sim.vel += acc * dt",
    "    sim.pos += sim.vel * dt",
    "    return sim.pos",
    "",
    "tokens = tokenize(headline)",
    "emb = embed(tokens)",
    "score = nlp.instability(emb)",
    "",
    "if score > threshold:",
    "    print(\"narrative break\")",
    "",
    "def dfs(u, graph, seen):",
    "    seen.add(u)",
    "    for v in graph[u]:",
    "        if v not in seen:",
    "            dfs(v, graph, seen)",
    "",
    "x = np.linspace(0, 2 * np.pi, 256)",
    "y = np.sin(x) * np.exp(-x / 8)",
    "pred = model.predict(y)",
    "",
    "# agents that learn from the world",
    "while not env.done():",
    "    action = agent.act(env.state)",
    "    env.step(action)",
]


def colorize(line):
    if not line:
        return ""
    parts = []
    for comment, string, ident, other, space in TOKEN.findall(line):
        if space:
            parts.append(html.escape(space))
        elif comment:
            parts.append(f'<tspan fill="#7d8590">{html.escape(comment)}</tspan>')
        elif string:
            parts.append(f'<tspan fill="#a5f3fc">{html.escape(string)}</tspan>')
        elif ident and ident.lower() in KW:
            parts.append(f'<tspan fill="{CYAN}" font-weight="700">{html.escape(ident)}</tspan>')
        elif ident:
            parts.append(f'<tspan fill="#e6edf3">{html.escape(ident)}</tspan>')
        else:
            parts.append(f'<tspan fill="#79c0ff">{html.escape(other)}</tspan>')
    return "".join(parts)


def code_scroll():
    """Seamless vertical loop of Python — the overlay that replaced LIMITLESS."""
    fs = 15
    lh = 19
    x = ART_X + 18
    y0 = ART_Y + 22
    block_h = len(CODE_LINES) * lh
    texts = []
    for copy in (0, 1):
        for i, line in enumerate(CODE_LINES):
            y = y0 + copy * block_h + i * lh
            inner = colorize(line) or " "
            texts.append(
                f'<text xml:space="preserve" x="{x}" y="{y:.1f}" font-size="{fs}" '
                f'fill="#c9d1d9">{inner}</text>'
            )
    return (
        f'<rect x="{ART_X}" y="{ART_Y}" width="{ART_W * 0.58:.1f}" height="{ART_H}" fill="#0d1117" opacity="0.18"/>'
        f'<g clip-path="url(#codeclip)" opacity="0.78">'
        f'<g>'
        f'{"".join(texts)}'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 0" to="0 -{block_h}" dur="22s" repeatCount="indefinite"/>'
        f"</g></g>"
    )


def main():
    b64 = embed_portrait()
    rng = random.Random(7)
    whoami = f"{USER_HANDLE}@github:~$ whoami"
    title = f"{USER_HANDLE}@github: ~$ python3 nve.py"
    cursor_x = PAD + int((len(whoami) + 1 + len(FULL_NAME)) * 7.35)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="gbg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG2}"/>
    <stop offset="1" stop-color="{BG}"/>
  </linearGradient>
  <radialGradient id="aura" cx="42%" cy="38%" r="62%">
    <stop offset="0" stop-color="#67e8f9" stop-opacity="0.28"/>
    <stop offset="0.45" stop-color="#0ea5e9" stop-opacity="0.12"/>
    <stop offset="1" stop-color="#0d1117" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="art">
    <rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" rx="8"/>
  </clipPath>
  <clipPath id="codeclip">
    <rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}"/>
  </clipPath>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#gbg)"/>
<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}"/>
<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>
<circle cx="{PAD + 0}" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56"/>
<circle cx="{PAD + 16}" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e"/>
<circle cx="{PAD + 32}" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f"/>
<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">{title}</text>

<g clip-path="url(#art)">
  <rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" fill="{BG}"/>
  <image x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" preserveAspectRatio="xMidYMin slice" href="data:image/jpeg;base64,{b64}" xlink:href="data:image/jpeg;base64,{b64}"/>
  <rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" fill="url(#aura)">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="4.5s" repeatCount="indefinite"/>
  </rect>
  <g filter="url(#glow)">{rings()}{particles(rng)}</g>
  {code_scroll()}
  <rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="3" fill="{CYAN}" opacity="0">
    <animate attributeName="y" values="{ART_Y};{ART_Y + ART_H - 3}" dur="6.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.28;0" dur="6.5s" repeatCount="indefinite"/>
  </rect>
</g>
<rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" rx="8" fill="none" stroke="{CYAN}" stroke-opacity="0.22"/>

<line x1="0" y1="{CANVAS_H - STATUS_H}" x2="{CANVAS_W}" y2="{CANVAS_H - STATUS_H}" stroke="{FRAME}"/>
<text x="{PAD}" y="{CANVAS_H - 11}" fill="{TITLE_TEXT}" font-size="13">{whoami} <tspan fill="{CYAN}">{FULL_NAME}</tspan></text>
<rect x="{cursor_x}" y="{CANVAS_H - 24}" width="8" height="14" fill="{CYAN}">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>
'''
    for path in (OUT, OUT_ALIAS):
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {path}  {os.path.getsize(path)/1024:.1f} KB")


if __name__ == "__main__":
    main()
