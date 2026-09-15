"""
Terminal-chrome SVG of scrolling Python. GitHub runs SMIL inside <img>.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "code-scroll.svg")

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
CYAN = "#67e8f9"

ART_X = PAD
ART_Y = TITLEBAR_H + 8
ART_W = CANVAS_W - PAD * 2
ART_H = CANVAS_H - TITLEBAR_H - STATUS_H - 16

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
    fs = 17
    lh = 22
    gutter = 52
    x = ART_X + gutter
    y0 = ART_Y + 24
    block_h = len(CODE_LINES) * lh
    texts = []
    for copy in (0, 1):
        for i, line in enumerate(CODE_LINES):
            y = y0 + copy * block_h + i * lh
            n = (i % max(len(CODE_LINES), 1)) + 1
            texts.append(
                f'<text x="{ART_X + 18}" y="{y:.1f}" font-size="13" fill="#484f58" '
                f'text-anchor="end">{n:02d}</text>'
            )
            inner = colorize(line) or " "
            texts.append(
                f'<text xml:space="preserve" x="{x}" y="{y:.1f}" font-size="{fs}" '
                f'fill="#c9d1d9">{inner}</text>'
            )
    return (
        f'<g clip-path="url(#codeclip)">'
        f'<g>'
        f'{"".join(texts)}'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 0" to="0 -{block_h}" dur="22s" repeatCount="indefinite"/>'
        f"</g></g>"
    )


def main():
    whoami = f"{USER_HANDLE}@github:~$ whoami"
    title = f"{USER_HANDLE}@github: ~$ python3 nve.py"
    cursor_x = PAD + int((len(whoami) + 1 + len(FULL_NAME)) * 7.35)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="gbg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG2}"/>
    <stop offset="1" stop-color="{BG}"/>
  </linearGradient>
  <clipPath id="codeclip">
    <rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" rx="8"/>
  </clipPath>
</defs>
<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#gbg)"/>
<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}"/>
<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>
<circle cx="{PAD}" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56"/>
<circle cx="{PAD + 16}" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e"/>
<circle cx="{PAD + 32}" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f"/>
<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">{title}</text>

<rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" rx="8" fill="{BG}"/>
{code_scroll()}
<rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="2" fill="{CYAN}" opacity="0">
  <animate attributeName="y" values="{ART_Y};{ART_Y + ART_H - 2}" dur="6.5s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0.22;0" dur="6.5s" repeatCount="indefinite"/>
</rect>
<rect x="{ART_X}" y="{ART_Y}" width="{ART_W}" height="{ART_H}" rx="8" fill="none" stroke="{FRAME}"/>

<line x1="0" y1="{CANVAS_H - STATUS_H}" x2="{CANVAS_W}" y2="{CANVAS_H - STATUS_H}" stroke="{FRAME}"/>
<text x="{PAD}" y="{CANVAS_H - 11}" fill="{TITLE_TEXT}" font-size="13">{whoami} <tspan fill="{CYAN}">{FULL_NAME}</tspan></text>
<rect x="{cursor_x}" y="{CANVAS_H - 24}" width="8" height="14" fill="{CYAN}">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>
'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}  {os.path.getsize(OUT)/1024:.1f} KB")


if __name__ == "__main__":
    main()
