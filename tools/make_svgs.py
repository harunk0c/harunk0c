"""Draws the terminal-style section images in ../assets.

GitHub strips colours from README text, so each section is drawn as an SVG
"terminal window" instead. Edit the data below and run:

    python3 tools/make_svgs.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# colours (GitHub dark palette)
C = {
    "fg": "#e6edf3", "dim": "#8b949e", "faint": "#6e7681", "green": "#3fb950",
    "blue": "#79c0ff", "link": "#4493f8", "str": "#a5d6ff", "kw": "#ff7b72",
    "num": "#ffa657", "purple": "#d2a8ff", "yellow": "#e3b341",
}
FONT = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
CHAR = 8.4  # approx. width of one character at 14px


def seg(text, colour="fg", bold=False):
    return (text, colour, bold)


def line(x, y, segments, size=14):
    bold = ' font-weight="700"'
    spans = "".join(
        f'<tspan fill="{C[c]}"{bold if b else ""}>{escape(t)}</tspan>'
        for t, c, b in segments
    )
    return f'<text x="{x}" y="{y}" font-size="{size}">{spans}</text>'


def window(w, h, title, body, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" xml:space="preserve">
  <style>text {{ font-family: {FONT}; white-space: pre; }}</style>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="#0b0f14" stroke="#30363d"/>
  <path d="M10.5 0.5h{w-21}a10 10 0 0 1 10 10v21.5h-{w-1}v-21.5a10 10 0 0 1 10-10z" fill="#161b22"/>
  <line x1="0.5" y1="32" x2="{w-0.5}" y2="32" stroke="#30363d"/>
  <circle cx="20" cy="16.5" r="5.5" fill="#ff5f57"/><circle cx="38" cy="16.5" r="5.5" fill="#febc2e"/><circle cx="56" cy="16.5" r="5.5" fill="#28c840"/>
  <text x="78" y="21" font-size="12" fill="{C["dim"]}">{escape(title)}</text>
  {body}
</svg>
'''


def write(name, svg):
    (ASSETS / name).write_text(svg, encoding="utf-8")
    print("wrote", name)


# ---------- const harun ----------
def about():
    k = lambda key, pad: seg(f"  {key}:" + " " * pad, "blue")
    rows = [
        [seg("const ", "kw"), seg("harun", "blue"), seg(" = {")],
        [k("role", 8), seg('"EEE student @ Karadeniz Technical University"', "str"), seg(",")],
        [k("year", 8), seg("3", "num"), seg(",")],
        [k("focus", 7), seg("["), seg('"robotics"', "str"), seg(", "), seg('"embedded"', "str"), seg(", "),
         seg('"digital design"', "str"), seg(", "), seg('"automation"', "str"), seg("],")],
        [k("drawnTo", 5), seg('"exploration & automation problems"', "str"), seg(",")],
        [seg("};")],
    ]
    body = "\n  ".join(line(24, 62 + i * 24, r) for i, r in enumerate(rows))
    h = 62 + len(rows) * 24
    write("about.svg", window(820, h, "harun.js", body,
          "harun: EEE student at Karadeniz Technical University, 3rd year; focus: robotics, embedded, digital design, automation"))


# ---------- stack ----------
STACK = [
    ("automation", [("Python", "#3572a5"), ("Telegram API", "#26a5e4"), ("Web scraping", "#8b949e")]),
    ("robotics", [("ROS 2", "#6b8dd6"), ("Lidar SLAM", "#a371f7"), ("Simulation", "#3fb950")]),
    ("embedded", [("Arduino", "#00979d"), ("ESP32", "#e7352c"), ("Sensors", "#e3b341")]),
    ("digital design", [("Verilog", "#b2b7f8"), ("CPU architecture", "#ffa657")]),
]


def stack():
    parts, y = [], 52
    for label, chips in STACK:
        parts.append(line(24, y + 19, [seg(label, "dim")], 13))
        x = 190
        for name, dot in chips:
            w = len(name) * 7.8 + 34
            parts.append(
                f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="6" fill="#161b22" stroke="#30363d"/>'
                f'<circle cx="{x+14}" cy="{y+14}" r="4.5" fill="{dot}"/>'
                f'<text x="{x+26}" y="{y+19}" font-size="13" fill="{C["fg"]}">{escape(name)}</text>'
            )
            x += w + 8
        y += 40
    label = "; ".join(f"{l}: " + ", ".join(n for n, _ in c) for l, c in STACK)
    write("stack.svg", window(820, y + 10, "cat stack.txt", "\n  ".join(parts), "Stack — " + label))


# ---------- project cards ----------
PROJECTS = [
    ("project-altair-observer.svg", "Altair-Observer", "VKWHM/", "ROS 2 · PX4 · Python · team", False,
     ["Autonomous indoor drone: lidar SLAM, frontier", "exploration and obstacle avoidance, no GPS"]),
    ("project-altair-silent.svg", "Altair-Silent", "VKWHM/", "ROS 2 · Nav2 · Python · team", False,
     ["Finds a window, flies through it and comes back,", "driven by behavior trees in GPS-denied spaces"]),
    ("project-price-tracker-bot.svg", "price-tracker-bot", None, "Python · Telegram · Shopify", False,
     ["Tracks Shopify prices & stock, pings you on", "Telegram on drops, restocks and target prices"]),
]


def projects():
    for fname, name, target, tags, wip, desc in PROJECTS:
        first = [seg("lrwxr-xr-x  " if target else "drwxr-xr-x  ", "faint"), seg(name, "link", True)]
        first += [seg(" -> " + target, "dim")] if target else [seg("/", "link", True)]
        tag_segs = [seg(tags, "dim")] + ([seg(" · ", "dim"), seg("WIP", "yellow", True)] if wip else [])
        tag_len = len(tags) + (6 if wip else 0)
        body = [
            line(24, 62, first),
            line(int(796 - tag_len * CHAR), 62, tag_segs, 14),
            line(24 + 12 * CHAR, 88, [seg("└─ ", "faint"), seg(desc[0])]),
        ]
        if len(desc) > 1:
            body.append(line(24 + 15 * CHAR, 112, [seg(desc[1])]))
        h = 128 if len(desc) > 1 else 104
        title = f"~/projects/{name}" + ("  (team repo)" if target else "")
        write(fname, window(820, h, title, "\n  ".join(body), f"{name} — {' '.join(desc)} ({tags})"))


# ---------- git log ----------
LOG = [
    ("a1f3c9e", True, "feat:", "price-tracker-bot, Shopify price & stock alerts"),
    ("7d20b14", False, "feat:", "Altair-Silent, drone flies through a window on its own"),
    ("5b91e03", False, "feat:", "Altair-Observer, drone maps & explores indoors without GPS"),
    ("0000001", False, "init:", "B.Sc. Electrical & Electronics Eng. @ KTU"),
]


def gitlog():
    rows = []
    for i, (h, head, kind, msg) in enumerate(LOG):
        segs = [seg(h, "yellow"), seg(" (HEAD) " if head else "        ", "green"), seg(kind + " ", "purple"), seg(msg)]
        rows.append(line(24, 62 + i * 26, segs))
    write("gitlog.svg", window(820, 62 + len(LOG) * 26, "git log --oneline", "\n  ".join(rows),
          "Timeline: " + "; ".join(m for *_, m in LOG)))


# ---------- contact ----------
def contact():
    for fname, title, icon, text in [
        ("contact-email.svg", "mail", "@", "harunyahyakoc2005@gmail.com"),
        ("contact-linkedin.svg", "linkedin", "in", "linkedin.com/in/harunyahyakoc"),
    ]:
        body = line(24, 70, [seg("$ ", "green"), seg("open ", "dim"), seg(text, "link")])
        write(fname, window(404, 94, title, body, f"{title}: {text}"))


# ---------- footer ----------
def footer():
    body = "\n  ".join([
        line(24, 62, [seg("harun@github", "green"), seg(":"), seg("~", "blue"), seg("$ exit")]),
        line(24, 86, [seg("logout", "dim"), seg("  ·  ", "faint"), seg("thanks for stopping by", "dim"),
                      seg("  ·  ", "faint"), seg("[process completed with exit code ", "faint"),
                      seg("0", "green", True), seg("]", "faint")], 13),
    ])
    write("footer.svg", window(820, 104, "harun@github: ~", body, "exit: thanks for stopping by"))


if __name__ == "__main__":
    about(); stack(); projects(); gitlog(); contact(); footer()
