# Testing Protocol - Does It Actually Work For You?

The evidence review is about averages; you are not an average. Preference,
personality, and task mix moderate every effect (evidence review §1.4), so each
playlist earns its place through this protocol or gets changed. The same protocol
A/Bs engine renders against commercial equivalents before anything is published.

## The method: 2-week alternating blocks (n-of-1)

For each playlist you want to validate:

1. **Pick one context.** e.g., "morning writing sessions" for Deep Work - Verbal.
   Don't mix contexts within a test.
2. **Pick a control.** Silence is the honest default for work playlists; your
   current habitual music also works. For sleep, control = your current wind-down.
3. **Alternate by day** (A = playlist, B = control) in an ABBA / BAAB pattern to
   cancel weekday effects. Two weeks ≈ 5+ sessions per condition.
4. **Rate immediately after each session** - 10 seconds, three 1-5 items plus one
   objective-ish anchor:

   | Item | 1 | 5 |
   |---|---|---|
   | Focus: how often did you drift? | constantly | almost never |
   | State: calm/energized as intended? | wrong direction | exactly right |
   | Friction: did you want to switch it off? | yes, actively | forgot it was on |
   | Anchor (pick one per playlist) | - | - |

   Anchors: deep work → # of self-caught distractions or pomodoros completed;
   downshift → resting feel after 20 min (or HR if you wear a watch);
   sleep → minutes-to-sleep estimate next morning; walk → route time.

5. **Log one line per session** in `logs/listening-log.csv`:
   `date,playlist,condition,focus,state,friction,anchor,notes`

   One command does it (validates ranges, fills the date):

   ```bash
   .venv/bin/python -m cognitionfm log --playlist deep-work-verbal \
       --condition A --focus 4 --state 4 --friction 5 --anchor 2
   ```

   And `python -m cognitionfm play --recipe deep-work-verbal --duration 25m`
   renders (once) and plays a session-length mix locally.

## Decision rules (after ~2 weeks)

- Playlist beats control on 2+ items → **keep**.
- Ties control → **keep whichever you prefer** (zero-cost tie).
- Loses to control on focus or friction → **modify one variable** (volume first,
  then density/brightness - for engine recipes that's `lufs_target`, `layers.*.amp`,
  `lp_cutoff_hz.base`) and re-run one week. Two failed modifications → **drop it;
  use the control**. Silence winning is a finding, not a failure.

## Honest limits

- **No blinding.** You know what you're hearing, and expectation inflates effects.
  Acceptable: in real life expectation is part of the effect you'll actually get.
  The comparison against control still catches playlists that are net-negative.
- **Small n.** This detects "works clearly," not subtle effects. Good enough -
  a playlist needing statistics to justify itself isn't worth maintaining.
- **Don't test two changes at once** (new playlist + new schedule = no conclusion).

## Engine A/B before publishing

Before a recipe format ships publicly, it must at minimum **tie** a commercial
reference playlist of the same category (the [playlist specs](02-playlists.md)
list equivalents) in your own two-week block. Publishing something that loses to a random Spotify
ambient playlist would violate the channel's honesty premise.
