# Distribution Plan

Everything published is 100% engine-rendered original audio: fully owned, with
no sampled or licensed source material anywhere in the pipeline, so copyright
risk is minimal and monetization is unencumbered. The distribution
platform is deliberately undecided; this plan is written platform-neutral so the
choice (long-form video platform, live stream, podcast feed, direct hosting, or
a mix) can be made late. The differentiator everywhere is honesty: the credible
alternative to "healing frequency" channels. (Practical guidance, not legal
advice.)

## Platform-independent constraints

Two constraints hold on any major platform and shape everything below:

1. **Originality policies.** Major video and streaming platforms now demonetize
   or downrank mass-produced, templated content, including generated audio with
   no evident human input. Consequences for us, regardless of platform:
   - Every published piece must be materially different: distinct recipe, seed,
     cover art, and a written science note per item.
   - Show the human: descriptions explain design decisions and link the evidence
     review; periodic "how this was built" explainers both differentiate and
     document originality.
   - Quality cadence over volume. One or two strong releases per week beats
     daily near-duplicates.
2. **Provenance.** `manifest.csv` records recipe, seed, engine version and git
   commit, plus a SHA-256 checksum and publication status for every artifact.
   Identical inputs regenerate byte-identical audio on the same platform and
   library versions (verified in practice; floating-point rounding can shift
   checksums across hardware), which is both our reproducibility promise and
   our ownership evidence if a dispute ever arises.

## Formats (mapped to engine recipes)

| Series | Recipe | Lengths | Notes |
|---|---|---|---|
| Deep Work - Verbal | `deep-work-verbal` | 1 h, 2 h, 3 h | flagship; "no lyrics by design" |
| Deep Work - Analytical | `deep-work-analytical` | 1 h, 2 h | steady-pulse variant |
| Downshift | `downshift` | 25-30 min | descending arc; "one session" framing |
| Sleep Wind-Down | `sleep-wind-down` | 40 min | explicitly not an 8-hour loop |
| Morning Ramp-Up | `morning-ramp-up` | 20-30 min | ascending arc |

Pipeline per release:

```bash
.venv/bin/python -m cognitionfm render --recipe deep-work-verbal --duration 2h --seed <n> --out renders/dwv-2h-s<n>.wav
.venv/bin/python -m cognitionfm video --audio renders/dwv-2h-s<n>.wav --recipe deep-work-verbal --seed <n>
```

Add each published render to `manifest.csv` and rebuild the site so the public
ledger stays current.

## Honest-claims style guide

Titles and descriptions market on evidence-awareness and never overclaim. The
allowed-claims table is in [01-evidence-review.md §4](01-evidence-review.md);
summary rules:

- Name the *design*, not a guaranteed *outcome*: "built so nothing grabs your
  attention" is fine; "makes you 3x more productive" never ships.
- No "Hz" claims, no brainwave language, no "dopamine," no "scientifically proven."
- Every description carries a short "Why it sounds like this" section with 2-3
  named citations, an honest-limits line ("works for many people, not everyone;
  test it against silence"), and a link to the evidence review.

**Title pattern:** `Deep Work - Verbal | 2 hours of generative focus audio (no lyrics, no surprises)`

**Description skeleton:**

```
Original generative audio by CognitionFM, composed by our own engine and owned end to end.

WHY IT SOUNDS LIKE THIS
- No lyrics or sharp onsets: unpredictable sound reliably disrupts verbal working
  memory (the "irrelevant sound effect": Salame & Baddeley 1982; Jones & Macken).
- Slow chord drift, no melody: background music should stay background
  (Kampfe et al. 2011 meta-analysis).
- Quiet master (-23 LUFS): louder music distracts more on complex tasks
  (Gonzalez & Aiello 2019).

HONEST LIMITS
For complex verbal work, silence can beat any music. This is designed to lose
to silence as rarely as possible. Test both.

Design docs and research review: <site link>
Recipe: deep-work-verbal | Seed: 42 | Engine: v0.1.0
```

## Competitive positioning

Claude FM ([Anthropic's 24/7 licensed lo-fi live stream](https://www.digitalmusicnews.com/2026/06/11/anthropic-claude-fm/),
human-curated, roughly 1,000 concurrent listeners, driven by a hook inside their
own developer tool) and channels like Lofi Girl define the adjacent territory.
Our positioning:

- **Don't compete on cozy.** They own "pleasant vibe" with human curation and
  brand reach. We own **functional specificity** (per-state formats),
  **evidence-based design**, and **reproducibility** (any mix regenerable from
  recipe + seed).
- **Provenance transparency is our counter to licensing opacity.** They credit
  artists without publishing terms; we publish the manifest, the recipes, and
  the seed for every published minute.
- **The stream never loops.** `python -m cognitionfm stream` generates endless,
  never-repeating audio, something a fixed licensed playlist cannot offer.

## Implemented capabilities

- **Cover art:** `python -m cognitionfm art --recipe X --seed N` produces
  seed-linked generative art, one accent color per series, same seed as the audio.
- **Video assembly:** `python -m cognitionfm video --audio ... --recipe X --seed N`
  builds an mp4 with rotating "why it sounds like this" captions (from the
  recipe's `notes:`), baked into cycling frames.
- **Live stream:** `python -m cognitionfm stream --recipe X --url rtmp://<ingest>/<key>`
  renders 30-minute segments with incrementing seeds, crossfades the joins,
  applies calibrated LUFS gain, and pushes h264/AAC with 2-second keyframes.
  Test locally with `--url test.flv --max-duration 60s`.
- **Chapters:** `python -m cognitionfm chapters --recipe X --duration 2h --seed N`
  derives chapter marks from the harmonic walk, snapped to chord changes;
  paste the output into release descriptions.
- **Trust-anchor site:** `site/` (see README for build and deploy). Public pages:
  landing, evidence review, playlist specs, testing protocol, provenance ledger.
  This is the link every release description carries; this strategy doc stays
  internal.

## Remaining roadmap

1. Pick the distribution platform(s); fill the placeholder links on the site
   landing page with real destinations at first release.
2. "Regenerate this exact mix yourself" as the community angle (needs the
   LICENSE decision). Local playback exists: `python -m cognitionfm play`.
3. R2 (or equivalent) hosting for full-length mixes linked from the site.
4. v2, only if releases show traction: in-browser generative player (Web Audio
   port of the engine), the Endel / generative.fm product direction.
