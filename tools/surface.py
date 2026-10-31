"""GitHub's own interface, redrawn at native pixel size so the profile can break it open.

Everything here is drawn in CSS pixels. Scenes scale it to the README column (846 px
on desktop, 308 px on a phone), so a 14 px label here renders as 14 px on the page.
Measurements and colors were taken from the live profile in both themes.
"""

from datetime import date
from html import escape
from json import loads
from pathlib import Path

HERE = Path(__file__).parent
WIDTHS = loads((HERE / "fonts/mona-sans-widths.json").read_text())
MANROPE = loads((HERE / "fonts/manrope-widths.json").read_text())
DATA = loads((HERE / "data/github.json").read_text())

NATIVE = {
    "dark": dict(canvas="#0d1117", fg="#f0f6fc", muted="#9198a1", border="#3d444d", accent="#4493f8",
                 badge="#212830", timeline="#3d444d", timeline_opacity=.7, year="#1f6feb", success="#238636",
                 merged="#ab7df8", open="#3fb950", outline="#ffffff", outline_opacity=.05, button="#212830", folder="#7d8590",
                 levels=["#151b23", "#033a16", "#196c2e", "#2ea043", "#56d364"]),
    "light": dict(canvas="#ffffff", fg="#1f2328", muted="#59636e", border="#d1d9e0", accent="#0969da",
                  badge="#f6f8fa", timeline="#d1d9e0", timeline_opacity=.7, year="#0969da", success="#1f883d",
                  merged="#8250df", open="#1a7f37", outline="#010409", outline_opacity=.06, button="#f6f8fa", folder="#54aeff",
                  levels=["#eff2f5", "#aceebb", "#4ac26b", "#2da44e", "#116329"]),
}

OCTICONS = {
    "repo-push": "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0V1.5h-8a1 1 0 0 0-1 1v6.708A2.493 2.493 0 0 1 4.5 9h2.25a.75.75 0 0 1 0 1.5H4.5a1 1 0 0 0 0 2h4.75a.75.75 0 0 1 0 1.5H4.5A2.5 2.5 0 0 1 2 11.5Zm12.23 7.79h-.001l-1.224-1.224v6.184a.75.75 0 0 1-1.5 0V9.066L10.28 10.29a.75.75 0 0 1-1.06-1.061l2.505-2.504a.75.75 0 0 1 1.06 0L15.29 9.23a.751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018Z",
    "repo": "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z",
    "git-pull-request": "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z",
    "git-merge": "M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z",
    "lock": "M4 4a4 4 0 0 1 8 0v2h.25c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 12.25 15h-8.5A1.75 1.75 0 0 1 2 13.25v-5.5C2 6.784 2.784 6 3.75 6H4Zm8.25 3.5h-8.5a.25.25 0 0 0-.25.25v5.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25ZM10.5 6V4a2.5 2.5 0 1 0-5 0v2Z",
    "directory": "M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1H1.75Z",
    "file": "M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v9.586A1.75 1.75 0 0 1 13.25 16h-9.5A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h9.5a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 9 4.25V1.5Zm6.75.062V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914-.013-.011Z",
    "history": "m.427 1.927 1.215 1.215a8.002 8.002 0 1 1-1.6 5.685.75.75 0 1 1 1.493-.154 6.5 6.5 0 1 0 1.18-4.458l1.358 1.358A.25.25 0 0 1 3.896 6H.25A.25.25 0 0 1 0 5.75V2.104a.25.25 0 0 1 .427-.177ZM7.75 4a.75.75 0 0 1 .75.75v2.992l2.028.812a.75.75 0 0 1-.557 1.392l-2.5-1A.751.751 0 0 1 7 8.25v-3.5A.75.75 0 0 1 7.75 4Z",
}

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
CELL, PITCH = 10, 13
GRID_X, GRID_Y = 45.8, 35


def measure(value, size, weight=400, family=None):
    table = (family or WIDTHS)["semibold" if weight >= (500 if family is MANROPE else 600) else "regular"]
    return sum(table.get(ch, .55) for ch in value) * size


def fit(value, size, room, weight=400):
    """Truncate with an ellipsis the way GitHub's CSS would."""
    if measure(value, size, weight) <= room:
        return value
    while value and measure(value + "…", size, weight) > room:
        value = value[:-1]
    return value.rstrip() + "…"


def t(x, y, value, size=14, fill="#000", weight=400, anchor="start", extra=""):
    return (f'<text class="gh" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}" {extra}>{escape(value)}</text>')


def link(x, y, value, size, color, weight=400):
    # GitHub underlines links inside text in its current default theme.
    width = measure(value, size, weight)
    return (t(x, y, value, size, color, weight) +
            f'<path d="M{x} {y + 2.5:.1f}h{width:.1f}" stroke="{color}" stroke-width="1"/>')


def icon(name, x, y, fill, size=16):
    scale = f" scale({size / 16})" if size != 16 else ""
    return f'<path transform="translate({x} {y}){scale}" d="{OCTICONS[name]}" fill="{fill}"/>'


def rrect(x, y, w, h, r, fill="none", stroke="none", extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'


def short_date(value):
    d = date.fromisoformat(value)
    return f"{MONTHS[d.month - 1]} {d.day}"


CELL_PATH = "h5a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-5a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2"


def cells(n, weeks, rows, extra=""):
    """One rounded-square path per level keeps 371 days small and crisp."""
    paths = {}
    for col, week in enumerate(weeks):
        for day, count, level in week:
            row = (date.fromisoformat(day).weekday() + 1) % 7
            if row in rows:
                x, y = GRID_X + col * PITCH + 2.5, 32 + GRID_Y + row * PITCH + .5
                paths.setdefault(level, []).append(f"M{x:.1f} {y}{CELL_PATH}")
    return "".join(f'<path d="{"".join(d)}" fill="{n["levels"][level]}" stroke="{n["outline"]}" '
                   f'stroke-opacity="{n["outline_opacity"]}" {extra}/>' for level, d in sorted(paths.items()))


def calendar(n, width, weeks=None, years=True):
    """Heading, calendar, legend and year switcher as (top y, svg) pieces, plus the box width.

    The bordered box itself is left to the caller, which may need to cut it.
    """
    weeks = weeks if weeks is not None else DATA["weeks"]
    box_w = width - 100 if years else width
    pieces = [(0, t(0, 18, f"{DATA['total']:,} contributions in the last year", 16, n["fg"]))]
    last_label = -9
    for col, week in enumerate(weeks):
        for day, count, level in week:
            d = date.fromisoformat(day)
            if d.day == 1 and col - last_label > 2 and col < len(weeks) - 1:
                pieces.append((44, t(GRID_X + col * PITCH, 32 + 26, MONTHS[d.month - 1], 12, n["fg"])))
                last_label = col
    for row, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        pieces.append((32 + GRID_Y + row * PITCH, t(15, 32 + GRID_Y + row * PITCH + 9, name, 12, n["fg"])))
    for row in range(7):
        pieces.append((32 + GRID_Y + row * PITCH, cells(n, weeks, {row})))
    foot = 32 + 147
    legend_right = box_w - 41
    legend = t(legend_right, foot, "More", 12, n["muted"], anchor="end")
    x = legend_right - measure("More", 12) - 4 - 5 * PITCH + 3
    for i, color in enumerate(n["levels"]):
        legend += rrect(x + i * PITCH + .5, foot - 9.5, 9, 9, 2, color, n["outline"], f'stroke-opacity="{n["outline_opacity"]}"')
    legend += t(x - 5, foot, "Less", 12, n["muted"], anchor="end")
    if width > 600:
        legend += t(GRID_X, foot, "Learn how we count contributions", 12, n["muted"])
    pieces.append((foot - 12, legend))
    if years:
        for i, year in enumerate([DATA["year"], DATA["year"] - 1, DATA["year"] - 2]):
            y = 32 + i * 42
            button = rrect(box_w + 16, y, 84, 32, 6, n["year"]) if i == 0 else ""
            button += t(box_w + 32, y + 20, str(year), 12, "#ffffff" if i == 0 else n["muted"])
            pieces.append((y + 16, button))
    return pieces, box_w


def badge(n, x, y, name):
    return (f'<circle cx="{x + 16}" cy="{y + 16}" r="17" fill="{n["badge"]}" stroke="{n["canvas"]}" stroke-width="2"/>'
            + icon(name, x + 8, y + 8, n["muted"]))


def feed(n, top, width, compact=False):
    """The Contribution activity timeline for the current month. Returns (svg, bottom)."""
    right = width - (0 if compact else 100)
    out = t(0, top + 18, "Contribution activity", 16, n["fg"])
    y = top + 56
    month = DATA["month"]
    out += t(8, y, month, 12, n["fg"], 600) + t(12 + measure(month, 12, 600), y, str(DATA["year"]), 12, n["muted"])
    out += f'<path d="M{12 + measure(f"{month}{DATA["year"]}", 12, 600) + 16:.1f} {y - 4}H{right}" stroke="{n["border"]}"/>'
    line_top = y + 14
    items = ""
    y += 30

    if DATA["commits"]:
        total = sum(c for _, c in DATA["commits"])
        repos = len(DATA["commits"])
        items += badge(n, 1, y, "repo-push")
        items += t(41, y + 22, f"Created {total} commit{'s' * (total != 1)} in {repos} repositor{'ies' if repos != 1 else 'y'}", 16, n["fg"])
        most = max(c for _, c in DATA["commits"])
        for i, (repo, count) in enumerate(DATA["commits"]):
            yy = y + 52 + i * 25
            items += link(41, yy, repo, 14, n["accent"])
            items += link(41 + measure(repo, 14) + 8, yy, f"{count} commit{'s' * (count != 1)}", 12, n["muted"])
            if not compact:
                items += rrect(right - 176, yy - 8, max(8, 140 * count / most), 8, 4, n["success"])
        y += 52 + len(DATA["commits"]) * 25 + 30

    if DATA["created"] and not compact:
        count = len(DATA["created"])
        items += badge(n, 1, y, "repo")
        items += t(41, y + 22, f"Created {count} repositor{'ies' if count != 1 else 'y'}", 16, n["fg"])
        for i, (repo, language, color, day) in enumerate(DATA["created"]):
            yy = y + 54 + i * 30
            items += icon("repo", 41, yy - 13, n["muted"])
            items += link(65, yy, fit(repo, 14, right - 140 if compact else right - 340), 14, n["accent"])
            if language and not compact:
                items += f'<circle cx="{right - 229}" cy="{yy - 5}" r="6" fill="{color}"/>'
                items += t(right - 218, yy, language, 12, n["muted"])
            items += t(right, yy, short_date(day), 12, n["muted"], anchor="end")
        y += 54 + count * 30 + 26

    for repo, pulls in ([] if compact else DATA["pulls"][:1]):
        count = len(pulls)
        items += badge(n, 1, y, "git-pull-request")
        repos = len(DATA["pulls"])
        items += t(41, y + 22, f"Opened {count} pull request{'s' * (count != 1)} in {repos} repositor{'ies' if repos != 1 else 'y'}", 16, n["fg"])
        items += t(41, y + 52, fit(repo, 14, right - 41), 14, n["muted"])
        for i, (title, merged, state, day) in enumerate(pulls):
            yy = y + 82 + i * 30
            items += icon("git-merge" if merged else "git-pull-request", 41, yy - 13,
                          n["merged"] if merged else n["open"] if state == "OPEN" else n["muted"])
            items += link(61, yy, fit(title, 14, right - 61 - (70 if compact else 120)), 14, n["fg"])
            items += t(right, yy, short_date(day), 12, n["muted"], anchor="end")
        y += 82 + count * 30 + 26

    items += badge(n, 1, y, "lock")
    items += t(41, y + 22, fit(f"{DATA['private']:,} contributions in private repositories", 16, right - 41 - (0 if compact else 110)), 16, n["muted"])
    if not compact:
        items += t(right, y + 21, f"{MONTHS[date.fromisoformat(DATA['generated']).month - 1]} 1 – {short_date(DATA['generated'])}", 12, n["muted"], anchor="end")
    y += 66
    out += f'<path d="M17 {line_top}V{y + 400}" stroke="{n["timeline"]}" stroke-opacity="{n["timeline_opacity"]}" stroke-width="2"/>'
    out += items
    out += rrect(.5, y + .5, right - 1, 31, 6, n["button"], n["border"])
    out += t(right / 2, y + 21, "Show more activity", 14, n["accent"], 600, "middle")
    return out, y + 32


def file_list(n, width, rows):
    """A repository's file table: latest commit header, then folders and files."""
    entries = sorted(DATA["bento"]["entries"], key=lambda e: (e[1] != "tree", e[0].lower()))[:rows]
    out = rrect(.5, .5, width - 1, 49 + len(entries) * 37, 6, n["canvas"], n["border"])
    out += f'<path d="M1 .5h{width - 2}v48H1Z" fill="{n["badge"]}"/>'
    out += rrect(.5, .5, width - 1, 49 + len(entries) * 37, 6, "none", n["border"])
    out += f'<circle cx="28" cy="25" r="10" fill="{n["border"]}"/>'
    out += t(46, 30, "invrnt", 14, n["fg"], 600)
    commits = f"{DATA['bento']['commits']} Commits"
    commits_w = measure(commits, 14, 600)
    room = width - 46 - measure("invrnt ", 14, 600) - 4 - commits_w - 56
    out += t(46 + measure("invrnt ", 14, 600) + 4, 30, fit(DATA["bento"]["message"], 14, room), 14, n["muted"])
    out += icon("history", width - 16 - commits_w - 24, 17, n["muted"])
    out += t(width - 16, 30, commits, 14, n["fg"], 600, "end")
    body = []
    for i, (name, kind) in enumerate(entries):
        y = 49 + i * 37
        row = f'<path d="M1 {y + .5}H{width - 1}" stroke="{n["border"]}"/>'
        row += icon("directory" if kind == "tree" else "file", 16, y + 11, n["folder"] if kind == "tree" else n["muted"])
        row += t(44, y + 24, name, 14, n["fg"])
        body.append(row)
    return out, body
