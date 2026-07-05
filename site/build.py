"""Build the static trust-anchor site from the docs and the provenance manifest.

Usage: .venv/bin/python site/build.py
Output: site/*.html, self-contained, deployable to any static host.

The public site deliberately excludes docs/04 (distribution strategy is
internal); what ships is exactly what a reader needs to verify our claims:
the evidence review, the playlist designs, the testing method, and the
provenance ledger.
"""

import csv
import html
import os
import re
import sys

import markdown

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(REPO, "site")
DOCS = os.path.join(REPO, "docs")

sys.path.insert(0, REPO)
from cognitionfm import __version__  # noqa: E402

PAGES = {  # doc filename -> (slug, nav title)
    "01-evidence-review.md": ("evidence", "Evidence"),
    "02-playlists.md": ("playlists", "Playlists"),
    "03-testing-protocol.md": ("protocol", "Testing"),
}
NAV = [("index", "CognitionFM"), ("evidence", "Evidence"), ("playlists", "Playlists"),
       ("protocol", "Testing"), ("provenance", "Provenance")]

SERIES_CARDS = [
    ("verbal", "Deep Work - Verbal", "Writing, reading, hard debugging. No lyrics, no surprises."),
    ("analytical", "Deep Work - Analytical", "Routine coding and flow work. One steady, soft pulse."),
    ("downshift", "Downshift", "25 minutes of descending energy for stress downregulation."),
    ("sleep", "Sleep Wind-Down", "Pre-bed routine audio that fades to near-silence."),
    ("rampup", "Morning Ramp-Up", "A gentle arousal ramp into the day."),
]

KEY_SOURCES = [
    ("Kämpfe, Sedlmeier & Renkewitz (2011), meta-analysis, Psychology of Music",
     "https://journals.sagepub.com/doi/10.1177/0305735610376261",
     "background music has small, task-dependent effects; it hurts reading and memory, helps mood and sport"),
    ("de Witte et al. (2020), two meta-analyses, Health Psychology Review",
     "https://pubmed.ncbi.nlm.nih.gov/31167611/",
     "music interventions reliably reduce physiological and psychological stress"),
    ("Jespersen et al. (2022), Cochrane systematic review",
     "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD010459.pub3/full",
     "listening to music improves subjective sleep quality in insomnia (moderate certainty)"),
    ("Terry, Karageorghis et al. (2020), meta-analysis of 139 studies, Psychological Bulletin",
     "https://www.semanticscholar.org/paper/Effects-of-music-in-exercise-and-sport%3A-A-review.-Terry-Karageorghis/99f14f1a71027bf338568c65216235c51ba000e5",
     "music measurably improves exercise performance and reduces perceived exertion"),
    ("Salamé & Baddeley (1982) and the changing-state literature",
     "https://www.sciencedirect.com/science/article/abs/pii/S0022537182905210",
     "unpredictable sound, including lyrics, disrupts verbal short-term memory even when ignored"),
]


def page(slug: str, title: str, body: str) -> str:
    nav = "".join(
        f'<a href="{s}.html" class="{"brand" if s == "index" else ""}'
        f'{" active" if s == slug else ""}">{t}</a>'
        for s, t in NAV
    )
    page_title = ("CognitionFM: functional music, honestly designed"
                  if slug == "index" else f"{html.escape(title)} · CognitionFM")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Original generative audio for focus, stress downshift, and sleep. Every design decision cited to peer-reviewed research; weak evidence flagged as weak.">
<title>{page_title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<nav>{nav}</nav>
<main>
{body}
</main>
<footer>Original generative audio, owned end to end. Every mix, image, and claim is
reproducible from the <a href="provenance.html">provenance ledger</a> and the engine
(v{__version__}).</footer>
</body>
</html>
"""


def convert_doc(md_name: str) -> str:
    text = open(os.path.join(DOCS, md_name)).read()
    for name, (slug, _) in PAGES.items():  # inter-doc links -> site slugs
        text = text.replace(f"({name})", f"({slug}.html)")
    text = re.sub(r"\(0\d-[\w-]+\.md\)", "(#)", text)  # non-public docs: defang
    # insert a table of contents after the H1 for scannability
    lines = text.split("\n")
    lines.insert(1, "\n[TOC]\n")
    return markdown.markdown(
        "\n".join(lines),
        extensions=["tables", "fenced_code", "toc"],
        extension_configs={"toc": {"toc_depth": "2-2", "title": "On this page"}},
    )


def build_index() -> str:
    cards = "".join(
        f'<div class="card" style="border-top-color: var(--{var})">'
        f"<h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>"
        for var, t, d in SERIES_CARDS
    )
    sources = "".join(
        f'<li><a href="{href}">{html.escape(name)}</a>: {html.escape(claim)}.</li>'
        for name, href, claim in KEY_SOURCES
    )
    return f"""
<h1>Functional music, honestly designed.</h1>
<p class="lead">CognitionFM renders original, long-form audio for focus, stress
downshift, and sleep. Every design decision traces to published research, and
every mix is reproducible from a seed.</p>

<p class="cta">
<a class="btn" href="evidence.html">Read the evidence</a>
<a class="btn secondary" href="playlists.html">See the playlist designs</a>
</p>

<div class="notice">No 432&nbsp;Hz. No solfeggio. No binaural-beat promises. No
"dopamine hacks." Where the evidence is weak or mixed, <a href="evidence.html">we
say so directly</a>. For complex verbal work, silence might beat any music,
including ours: <a href="protocol.html">test it</a>.</div>

<h2>The formats</h2>
<div class="cards">{cards}</div>

<h2>What the design rests on</h2>
<p>Major claims are cited to peer-reviewed research, prioritizing systematic
reviews and meta-analyses. The five sources doing the most work:</p>
<ul class="sources">{sources}</ul>
<p>The full claim-by-claim review, including what we consider weak (binaural
beats, creativity effects, intimacy) and debunked ("healing frequencies", the
Mozart effect as popularly claimed), is on the
<a href="evidence.html">evidence page</a>.</p>

<h2>Why trust this</h2>
<ul>
<li><strong>Evidence, tiered.</strong> Every claim in the <a href="evidence.html">review</a>
is labeled well-supported, moderate/mixed, weak, or debunked, with sources you can click.</li>
<li><strong>Ownership, provable.</strong> All audio is synthesized by our engine.
The <a href="provenance.html">ledger</a> lists recipe, seed, and engine version for
every published minute; identical inputs regenerate the identical mix.</li>
<li><strong>Tested, not asserted.</strong> Formats ship only after beating or tying a
commercial reference playlist in our own <a href="protocol.html">n-of-1 protocol</a>.</li>
</ul>

<h2>Status</h2>
<p>The engine, recipes, and documentation are complete and current. First public
releases are in preparation; this page will link to them when they exist, and
not before.</p>
"""


def build_provenance() -> str:
    rows = list(csv.DictReader(open(os.path.join(REPO, "manifest.csv"))))
    header = "".join(f"<th>{html.escape(h)}</th>" for h in rows[0].keys())
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(v)}</td>" for v in r.values()) + "</tr>"
        for r in rows
    )
    return f"""
<h1>Provenance</h1>
<p class="lead">Every CognitionFM artifact is listed here with everything needed
to regenerate and verify it: recipe, seed, duration, engine version and commit,
and the SHA-256 checksum of the exact file.</p>
<p>Renders are deterministic. <code>python -m cognitionfm render --recipe
&lt;recipe&gt; --duration &lt;duration&gt; --seed &lt;seed&gt;</code> at the listed
engine commit reproduces the byte-identical audio (compare with
<code>shasum -a 256</code>), and cover art derives from the same seed. This ledger
is the ownership record: nothing published samples, remixes, or launders anyone
else's work. Status is <code>local-test</code> until an artifact is actually
published, at which point its public URL is added.</p>
<table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>
"""


def main():
    out = {"index": ("CognitionFM", build_index()),
           "provenance": ("Provenance", build_provenance())}
    for md_name, (slug, title) in PAGES.items():
        out[slug] = (title, convert_doc(md_name))
    for slug, (title, body) in out.items():
        path = os.path.join(SITE, f"{slug}.html")
        with open(path, "w") as f:
            f.write(page(slug, title, body))
        print(f"wrote {os.path.relpath(path, REPO)}")


if __name__ == "__main__":
    main()
