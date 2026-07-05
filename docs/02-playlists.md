# Playlist Specifications

Ten playlists, one clear job each. Every design rule traces to a verdict in
[01-evidence-review.md](01-evidence-review.md) (cited as §-references).

Two kinds of spec:

- **[ENGINE]** — rendered by the CognitionFM generative engine (`recipes/*.yaml`
  implements the parameter block). These are also the YouTube channel formats.
- **[PERSONAL]** — built from commercial streaming music for personal use. The engine
  can't fake vocals or your personal history with a song, and shouldn't try.

Global rules (all playlists):
- **Volume:** background music means background — just above audibility for work
  playlists. Salience scales distraction (§1.3).
- **Familiarity:** work playlists should be *familiar* (novelty captures attention,
  §1.2); emotional and creative playlists can afford novelty.
- **Don't mix jobs.** The moment a focus playlist becomes emotionally interesting,
  it has failed at its job.

---

## 1. Deep Work — Verbal [ENGINE] — writing, reading, hard debugging

The strictest spec. Verbal working memory must be protected (§1.2, §2.1).

- No lyrics, no vocal samples, ever
- High self-similarity: slow harmonic drift, no dramatic melodic contour
- Attack times ≥ 150 ms (no percussive transients)
- Narrow dynamic range; no section that makes you look up
- Honest alternative: silence or broadband noise may beat it for you — test (§3.5)

```yaml
# recipe parameters
tempo_bpm: null            # unpulsed; motion from slow LFO drift only
mode: ionian_or_lydian     # consonant, low-tension
attack_floor_ms: 150
dynamic_range_max_db: 6
melodic_salience: minimal  # no foreground melody
texture: 2-3 sustained layers (pad, sub drone, sparse shimmer)
lufs_target: -23
```

**[PERSONAL] equivalents / search terms:** "ambient drone," "textural ambient," Stars
of the Lid, Eluvium, Brian Eno's ambient series, Max Richter's quieter work, "deep
focus instrumental." Avoid "epic study music" — cinematic dynamics violate the spec.

## 2. Deep Work — Analytical [ENGINE] — routine coding, math, spreadsheets

Lower verbal load tolerates a steady pulse; the pulse aids time-on-task feel
(§2.2 — extrapolated, flagged as such).

- Steady 95–115 BPM pulse, soft-attack percussion only
- Instrumental, repetitive 8/16-bar cycles, gradual filter evolution
- Switch to Playlist 1 (or silence) when reading unfamiliar code

```yaml
tempo_bpm: 95-115
mode: dorian_or_aeolian
attack_floor_ms: 30       # soft ticks allowed, no sharp snares
dynamic_range_max_db: 8
texture: pulse + bass + pad, one slowly-evolving voice
section_change_every_bars: 32   # slow, predictable evolution
lufs_target: -20
```

**[PERSONAL] equivalents:** minimal techno (Kompakt label), dub techno, Tycho,
Bonobo instrumentals, "minimal techno focus," "dub techno mix."

## 3. Admin / Shallow Work [PERSONAL] — email, chores, expense reports

The one work context where stimulating music with lyrics is evidence-aligned (§2.3).

- Upbeat, familiar favorites; lyrics welcome
- Choose energy just above the task's boredom level
- Search terms: your existing favorites; "feel good," decade playlists you know cold.

## 4. Creative / Diffuse Thinking [PERSONAL, ENGINE-assisted]

Mood scaffolding around ideation, not during verbal drafting (§2.4 — mixed evidence,
honest framing).

- Moderately novel instrumental music between thinking bouts; anything goes on breaks
- During actual verbal ideation: drop to Playlist 1 rules or silence
- Search terms: "modern classical," "fourth world," "jazz ambient," Jon Hassell,
  Alice Coltrane, Floating Points.

## 5. Downshift — Stress Reduction [ENGINE]

The strongest clinical literature (§2.5): slow, predictable, low-dynamic music.

- ~60–80 BPM felt motion, descending energy arc across 20–30 min
- Warm consonance, no surprises, generous reverb tails

```yaml
tempo_bpm: 60-80          # felt as slow swells, not a beat
mode: ionian
attack_floor_ms: 300
dynamic_range_max_db: 5
arc: descending           # spectral centroid + density fall over the render
duration_default_min: 25
lufs_target: -24
```

**[PERSONAL] equivalents:** "slow ambient," Hammock, Ólafur Arnalds' quiet pieces,
Hiroshi Yoshimura, "60 bpm relaxation instrumental."

## 6. Emotional Processing [PERSONAL]

Deliberate, time-boxed listening — never background (§2.6).

- Your music, your lyrics, your history; nostalgia does most of the work
- 20–40 minute sessions with a defined end; if you tend to ruminate, pair with
  journaling or a walk, and stop if mood sinks instead of settles
- No search terms needed — you already know these songs.
- **Anger variant (§2.10):** when furious, *match* the arousal — your own
  aggressive/high-energy music — rather than forcing calm; shift toward
  Downshift only after the edge drops (the music-therapy "iso principle").

## 7. Walk / Recover [PERSONAL]

The best-supported positive effect in the whole literature (§2.7).

- Fast (115–140 BPM), personally motivational, familiar vocal music
- Save absolute favorites for the hardest part of the walk/workout
- Search terms: "running 120-140 bpm," your high-energy favorites.

## 8. Sleep Wind-Down [ENGINE]

Routine + relaxation, honestly framed (§2.8): part of a consistent pre-bed sequence,
not an all-night stream.

- 30–45 min, played at the same point in the wind-down every night, low volume
- Slowest attack times in the system; energy arc falls to near-silence
- No claims about sleep stages — the Cochrane-supported outcome is subjective
  sleep quality

```yaml
tempo_bpm: 50-65          # barely-felt motion
mode: ionian_low_register
attack_floor_ms: 500
dynamic_range_max_db: 4
arc: descending_to_silence
duration_default_min: 40
lufs_target: -28          # markedly quiet; player volume low too
```

**[PERSONAL] equivalents:** "sleep ambient no melody," Green-House, Grouper's quieter
side, "drone sleep music" (skip anything labeled with Hz claims — see §3.2).

## 9. Mood Lift [PERSONAL]

Deliberate short-term mood raising (§2.9) — the evidence needs *both* halves:
upbeat music **and** the intention to feel better; passive play doesn't move mood.

- 15–25 min of genuinely upbeat music you love; use it on purpose ("I'm putting
  this on to shift gears"), then get on with the day — don't keep polling your mood
- Major-key, energetic, familiar; lyrics fine; great before social things or
  after a slump
- Search terms: your own feel-good history first; "good mood classics,"
  upbeat playlists in genres you already love.

## 10. Intimacy [PERSONAL]

Requested use case; honest evidence status: thin (§2.11 — one lab mechanism,
excitation transfer, plus conditioning and self-consciousness masking; no
validated genre/tempo prescription and absolutely no "aphrodisiac frequency").

- **Shared history beats acoustics**: music tied to your relationship outperforms
  any generic "sensual" playlist on the conditioning mechanism
- Otherwise: moderate arousal without attention capture — smooth timbres, warm
  bass, steady slow-to-mid grooves, no jarring transitions, no comedy shuffles;
  vocals fine, skip anything lyrically distracting or associated with other contexts
- Long enough not to think about it (60+ min), volume low; gapless > shuffle
- Search terms: "slow jams," "bedroom R&B," trip-hop, "late night soul" — as
  *starting points for taste*, not prescriptions
- Stays personal-use and **off-channel**: publishing this under CognitionFM would
  dilute the focus/recovery brand, and generative synthesis is weakest exactly
  where this playlist lives (vocals, groove, familiarity).

---

## Quick-reference

| State | Playlist | Vocals | Pulse | The one rule |
|---|---|---|---|---|
| Writing/reading | 1 Verbal | never | none | protect verbal memory |
| Routine coding | 2 Analytical | never | steady | predictability |
| Email/chores | 3 Admin | yes | any | raise arousal |
| Ideation | 4 Creative | breaks only | loose | mood, not soundtrack |
| Stressed | 5 Downshift | no | slow swells | descend |
| Heavy day | 6 Processing | yes | any | time-boxed, on purpose |
| Walking | 7 Walk | yes | fast | motivation is legal here |
| Pre-bed | 8 Sleep | never | minimal | same time, every night |
| Slumped | 9 Mood Lift | yes | upbeat | intention + music, then move on |
| Intimate | 10 Intimacy | yes | slow groove | shared history beats acoustics |
