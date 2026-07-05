# Publishing Plan — CognitionFM on YouTube

Everything uploaded is 100% engine-rendered original audio: fully owned, no
Content ID exposure, monetizable. The channel's differentiator is honesty — the
credible alternative to "528 Hz DNA repair" channels. (Practical guidance, not
legal advice.)

## The critical constraint: YouTube's inauthentic-content policy

As of **July 15, 2025**, YouTube's monetization policy treats **mass-produced or
templated content as "inauthentic"** and ineligible — explicitly including
AI/generated content without evident human originality
([policy](https://support.google.com/youtube/answer/1311392), [coverage](https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/)).
A channel of near-identical dark-screen drone videos is exactly what this targets.
Non-negotiable consequences for us:

1. **Every video must be materially different.** Different recipe, seed, key, or
   duration alone is not "materially different" to a reviewer. Vary the *package*:
   distinct cover art per video, a written science note in each description, and
   periodic explainer content.
2. **Show the human.** Descriptions explain the design decisions and link the
   evidence review (public repo or blog mirror). An occasional "how this was
   built" video (code + research walkthrough) both differentiates and inoculates.
3. **Don't spam uploads.** One or two high-quality mixes per week beats daily
   near-duplicates — for the algorithm and for policy review.

## Formats (mapped to engine recipes)

| Series | Recipe | Lengths | Notes |
|---|---|---|---|
| Deep Work — Verbal | `deep-work-verbal` | 1 h, 2 h, 3 h | flagship; "no lyrics by design" |
| Deep Work — Analytical | `deep-work-analytical` | 1 h, 2 h | steady-pulse variant |
| Downshift | `downshift` | 25–30 min | descending arc; "one session" framing |
| Sleep Wind-Down | `sleep-wind-down` | 40 min | explicitly *not* an 8-hour loop |

Pipeline per video:

```bash
.venv/bin/python -m cognitionfm render --recipe deep-work-verbal --duration 2h --seed <n> --out renders/dwv-2h-s<n>.wav
.venv/bin/python -m cognitionfm video --audio renders/dwv-2h-s<n>.wav --image art/dwv-<n>.png
```

Keep a `renders/manifest.csv` (video → recipe, seed, engine version) so any
published mix is exactly reproducible — that reproducibility is also your
provenance evidence if ownership is ever questioned.

## Honest-claims style guide

Titles/descriptions market on evidence-awareness and never overclaim. The full
allowed-claims table is in [01-evidence-review.md §4](01-evidence-review.md);
summary rules:

- Name the *design*, not a guaranteed *outcome*: "built so nothing grabs your
  attention" ✅ — "makes you 3x more productive" ❌.
- No "Hz" claims, no brainwave language, no "dopamine," no "scientifically proven."
- Every description carries a short "Why it sounds like this" section with 2–3
  citations, an honest-limits line ("works for many people, not everyone — test
  it against silence"), and a link to the evidence review.

**Title pattern:** `Deep Work — Verbal | 2 hours of generative focus audio (no lyrics, no surprises)`

**Description skeleton:**

```
Original generative audio by CognitionFM — composed by our own engine, owned end to end.

WHY IT SOUNDS LIKE THIS
· No lyrics or sharp onsets: unpredictable sound reliably disrupts verbal working
  memory (the "irrelevant sound effect", Salamé & Baddeley 1982; Jones & Macken).
· Slow chord drift, no melody: background music should stay background
  (Kämpfe et al. 2011 meta-analysis).
· Quiet master (-23 LUFS): louder music distracts more on complex tasks
  (Gonzalez & Aiello 2019).

HONEST LIMITS
For complex verbal work, silence can beat any music. This is designed to lose
to silence as rarely as possible. Test both.

Design docs & research review: <repo link>
Recipe: deep-work-verbal · Seed: 42 · Engine: v0.1.0
```

## Channel mechanics

- **Chapters:** timestamps every 15–20 min ("phase shifts" where the harmonic
  center moves) — improves retention UX on long videos.
- **Cover art:** one visual system, one accent color per series; generate
  variations per video (art can be a later engine module).
- **Monetization path:** YPP needs 1,000 subs + 4,000 watch-hours (long-form
  listening content accumulates watch-hours well). Original audio = no Content ID
  claims against you; consider registering finished tracks with a distributor
  later if you want Content ID protection *for* your work.
- **Cadence:** 1–2 uploads/week; one explainer per month. Never announce results
  the testing protocol hasn't shown.

## Competitive positioning (vs. Claude FM and lo-fi brand channels)

[Claude FM](https://musically.com/2026/06/11/anthropics-claude-fm-is-a-24-7-music-stream-on-youtube/)
(Anthropic's 24/7 stream, human-made licensed lo-fi, ~1,000 concurrent listeners,
distributed via `/radio` inside Claude Code) defines the adjacent territory. Our
positioning against it and channels like Lofi Girl:

- **Don't compete on cozy.** They own "pleasant vibe" with human curation and
  brand reach. We own **functional specificity** (per-state formats), **evidence-based
  design**, and **reproducibility** (any mix regenerable from recipe + seed).
- **Provenance transparency is our counter to their licensing opacity.** They
  credit artists but don't publish licensing terms; we publish the manifest, the
  code, and the seed for every published minute.
- **The stream never loops.** `python -m cognitionfm stream` generates endless,
  never-repeating audio — structurally impossible for a licensed-playlist channel.

### Video/visual system (implemented)

- `python -m cognitionfm art --recipe X --seed N` — seed-linked generative cover
  art, one accent color per series; same seed as the audio (provenance made visible).
- `python -m cognitionfm video --audio ... --recipe X --seed N` — assembles the
  mix with rotating "why it sounds like this" captions (from the recipe's `notes:`)
  baked into cycling frames: the ClaudeFM now-playing overlay idea, carrying design
  evidence instead of track credits.

### Live stream (implemented, needs a stream key)

`python -m cognitionfm stream --recipe deep-work-verbal --url rtmp://a.rtmp.youtube.com/live2/<KEY>`
renders 30-min segments with incrementing seeds, crossfades the joins, applies
calibrated LUFS gain, and pushes h264/AAC with 2-second keyframes. Test locally
first with `--url test.flv --max-duration 60s`.

### Trust-anchor site (implemented)

`site/` — static, self-contained (`python site/build.py` rebuilds from the docs +
`manifest.csv`). Public pages: landing, evidence review, playlist specs, testing
protocol, provenance ledger. This is the link every video description carries;
the publishing strategy in this doc stays internal. Keep the manifest current —
it is the public ownership record.

Hosting: **Cloudflare Pages** (`npx wrangler pages deploy site/`) — deployable
without git, repo can stay private, unlimited bandwidth, and Workers on the same
platform is the growth path for the v2 in-browser player. GitHub Pages works too
but requires a public repo on the free tier.

### Remaining roadmap

1. First uploads; put the real channel + repo links on the site landing page
   (currently marked "in preparation").
2. Distribution hooks: a `play` command / tiny web player; "regenerate this exact
   mix yourself" as the community angle.
3. Chapter/timestamp generation from the harmonic walk (engine knows where the
   phase shifts are).
4. v2 (only if the channel shows traction): in-browser generative player
   (Web Audio port of the engine) — the Endel/generative.fm product direction.
