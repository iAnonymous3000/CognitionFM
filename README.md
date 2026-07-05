# CognitionFM

An evidence-aware functional music system with a generative engine. Two things
live here:

1. **A personal listening system** — research-grounded playlist specs for focus,
   stress, sleep, walking, and emotional processing, with a self-testing protocol.
2. **A generative music engine** — renders original, fully-owned long-form audio
   (ambient focus, downshift, sleep) from evidence-derived recipes, packaged into
   YouTube-ready videos for the CognitionFM channel.

No healing frequencies, no binaural-beat claims, no "dopamine music." Where the
evidence is weak, the docs say so.

## Quickstart

```bash
python3 -m venv .venv
.venv/bin/pip install numpy scipy soundfile pyyaml pillow pytest

# list recipes
.venv/bin/python -m cognitionfm recipes

# render 10 minutes of deep-work ambient (deterministic per seed)
.venv/bin/python -m cognitionfm render --recipe deep-work-verbal --duration 10m --seed 42

# YouTube-ready mp4 with seed-linked cover art + rotating evidence captions
.venv/bin/python -m cognitionfm video --audio renders/deep-work-verbal-10m-seed42.wav --recipe deep-work-verbal --seed 42

# seed-linked cover art on its own
.venv/bin/python -m cognitionfm art --recipe downshift --seed 7

# endless generative live stream (RTMP; use a local .flv + --max-duration to test)
.venv/bin/python -m cognitionfm stream --recipe deep-work-verbal --url rtmp://a.rtmp.youtube.com/live2/<KEY>

# run tests
.venv/bin/python -m pytest tests/
```

Requires Python 3.11+ and ffmpeg (`brew install ffmpeg`).

## Read in this order

| Doc | What it is |
|---|---|
| [docs/01-evidence-review.md](docs/01-evidence-review.md) | What the research supports, tiered verdicts, skeptic's corner, allowed public claims |
| [docs/02-playlists.md](docs/02-playlists.md) | 8 playlist specs — engine-rendered or personal streaming — with selection principles |
| [docs/03-testing-protocol.md](docs/03-testing-protocol.md) | 2-week n-of-1 method to verify each playlist on yourself |
| [docs/04-publishing-plan.md](docs/04-publishing-plan.md) | YouTube channel plan: formats, honest-claims style guide, policy constraints |

## Public site

`site/` holds the static trust-anchor site: the evidence review, playlist specs,
testing protocol, and the provenance ledger ([manifest.csv](manifest.csv)) rendered
with the channel's visual identity. It's what video descriptions link to — the
place where every public claim is checkable.

```bash
.venv/bin/python site/build.py          # rebuild after editing docs or manifest
.venv/bin/python -m http.server 8137 --directory site   # preview locally
```

Deploy (Cloudflare Pages, recommended — no git required, unlimited bandwidth,
repo can stay private):

```bash
npx wrangler login                                  # once
npx wrangler pages deploy site/ --project-name cognitionfm
```

GitHub Pages also works (push repo → Settings → Pages → serve `site/`), but the
free tier requires a public repo. Any static host is fine — the output is
self-contained. Add every published render to `manifest.csv` and rebuild; the
ledger page is the ownership record.

## How the engine works

`recipes/*.yaml` hold only parameters justified by the evidence review (tempo,
attack floors, dynamic ceilings, energy arcs). A generator turns a recipe into an
event list (drone / voice-led pads / shimmer, or pulse / bass / pad); events are
synthesized as detuned partial stacks, mixed through a streaming convolution
reverb, metered to BS.1770 LUFS, true-peak-limited, and written as 24-bit WAV.
Renders stream in constant memory (3-hour mixes are fine) and are bit-identical
per seed — every published mix is reproducible from `(recipe, seed, version)`.

```
cognitionfm/
  dsp/       oscillators, envelopes, filters, slow modulation
  fx/        convolution reverb (synthetic IR), stereo tools
  compose/   scales, chord graph, voice-leading, event voices
  recipes/   generators: ambient_layers, pulse_layers
  master/    BS.1770 loudness, true peak, normalize/finalize
  render.py  chunked streaming pipeline
  video.py   ffmpeg assembly (audio + cover -> mp4)
recipes/     evidence-derived YAML parameter files
docs/        the four documents above
tests/       DSP correctness, loudness reference tones, streaming equivalence
```

## Status

- [x] Phase 1 — engine core + deep-work-verbal proof of concept
- [x] Phase 2 — downshift, sleep, analytical recipes; mastering; tests
- [x] Phase 3 — video assembly, publishing plan
- [x] Morning ramp-up recipe (ascending arc)
- [x] Seed-linked cover art + rotating evidence captions in videos
- [x] Endless generative stream mode (needs a YouTube stream key to go live)
- [ ] Listening iteration on sound design (ongoing — ears beat metrics)
- [ ] Personal playlist A/B tests (docs/03) and first uploads
- [ ] Distribution hooks: play command / web player; public provenance page
