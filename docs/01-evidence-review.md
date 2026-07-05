# Evidence Review - What Music Actually Does (and Doesn't Do)

This document is the scientific foundation for every playlist spec and every engine
recipe in CognitionFM. Each claim gets one of four verdicts:

| Tier | Meaning |
|---|---|
| **WELL-SUPPORTED** | Multiple RCTs or meta-analyses, consistent direction, plausible mechanism |
| **MODERATE / MIXED** | Real signal but inconsistent, small, or heavily moderated by person/task |
| **WEAK / SPECULATIVE** | A few small studies, methodological problems, or effect likely non-specific |
| **DEBUNKED / MARKETING** | No credible evidence, or evidence directly contradicts the claim |

Every citation below was verified against the source in July 2026. Where marketing
language circulates ("neuroscience-backed," "healing frequency"), the gap between the
actual finding and the claim is stated explicitly.

---

## 1. The mechanisms that actually matter

Four mechanisms explain most reliable music effects. Everything else in this document
is a special case of these.

### 1.1 Arousal and mood, not "smart music" - WELL-SUPPORTED

The famous "Mozart effect" dissolved under scrutiny. [Thompson, Schellenberg & Husain
(2001)](https://journals.sagepub.com/doi/10.1111/1467-9280.00345) showed the spatial-task
benefit appears after *any* pleasant, energetic music and disappears when arousal and
mood are controlled - a slow, sad Albinoni adagio produced no benefit. [Pietschnig,
Voracek & Formann's meta-analysis (2010, *Intelligence*)](https://www.sciencedirect.com/science/article/abs/pii/S0160289610000267)
of ~40 studies / 3,000+ subjects found publication bias, inflated effects from a single
lab, and "little evidence for a specific, performance-enhancing Mozart effect."

**Design consequence:** music helps performance by putting you at the right arousal
level for the task - not by transferring information into your brain. Choose music by
target arousal, not by composer prestige.

### 1.2 Attention capture: the irrelevant sound effect - WELL-SUPPORTED

Sounds that change unpredictably ("changing-state" sounds: speech, lyrics, staccato
melodies, novel timbres) disrupt serial recall and verbal short-term memory even when
you ignore them ([Salamé & Baddeley 1982](https://www.sciencedirect.com/science/article/abs/pii/S0022537182905210);
Jones & Macken's changing-state work - [overview](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00346/full),
[recent evidence](https://www.tandfonline.com/doi/full/10.1080/25742442.2022.2127988)).
Two robust details:

- Non-speech sounds disrupt about as much as speech **when they contain the same
  acoustic variability**. It's the variability, not the words per se.
- Steady-state, repetitive, predictable sound disrupts far less.

**Design consequence:** for any task holding words or ordered items in working memory
(writing, reading, debugging a specific line), background audio must minimize
*acoustic change*: no lyrics, no sharp transients, no dramatic melodic contour, high
self-similarity. This is the single most load-bearing finding in this system.

### 1.3 Task complexity × music salience - WELL-SUPPORTED

[Kämpfe, Sedlmeier & Renkewitz's meta-analysis (2011, *Psychology of Music*)](https://journals.sagepub.com/doi/10.1177/0305735610376261)
found a **global null**: averaged across everything, background music does nothing.
Disaggregated, it *hurts reading and memory* and *helps emotion and sports*.
[Gonzalez & Aiello (2019, *JEP: Applied*)](https://www.researchgate.net/publication/330693127_More_Than_Meets_the_Ear_Investigating_How_Music_Affects_Cognitive_Task_Performance)
sharpened this: salient music (louder, more layers) improved simple vigilance tasks and
impaired complex ones - and boredom-prone people who most *want* music while working
were the most distracted by it. A [2022 systematic review (Cheah et al., *Music &
Science*)](https://journals.sagepub.com/doi/full/10.1177/20592043221134392) confirms the
same task/music/person interaction structure.

**Design consequence:** there is no one "focus playlist." Simple/boring work tolerates
(and benefits from) stimulating music; complex work needs minimal or no music. The
system therefore splits work playlists by cognitive load.

### 1.4 Preference, familiarity, and personality moderate everything - WELL-SUPPORTED

[Furnham & Bradley (1997)](https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1099-0720(199710)11:5%3C445::AID-ACP472%3E3.0.CO;2-R)
found introverts suffer more from background music than extraverts on recall and
reading. Preference cuts both ways: liked music improves mood and persistence, but
[Perham & Currie (2014)](https://onlinelibrary.wiley.com/doi/abs/10.1002/acp.2994) showed
*preferred* lyrical music impaired reading comprehension as much as disliked lyrical
music - liking a song does not protect you from its lyrics.

**Design consequence:** the system calibrates to the individual (see
[03-testing-protocol.md](03-testing-protocol.md)) and never assumes a universal
prescription. But preference is not a free pass for lyrics during verbal work.

---

## 2. Verdicts by use case

### 2.1 Deep work: writing, reading, language-heavy tasks

**Verdict: music with lyrics or high variability - WELL-SUPPORTED as harmful.
Quiet, steady instrumental music - MODERATE (roughly neutral; helps mood/persistence,
may slightly cost accuracy vs. silence).**

Silence is the performance ceiling for complex verbal work in most lab studies
(Kämpfe 2011; Perham & Currie 2014). Steady instrumental sound earns its place not by
boosting cognition but by masking worse noise (office chatter is a changing-state
sound), stabilizing mood, and making long sessions tolerable. That is a real,
defensible benefit - just not "music makes you smarter."

### 2.2 Deep work: coding and analytical tasks

**Verdict: MODERATE.** Coding is heterogeneous: reading unfamiliar code is
language-heavy (rules above apply); routine implementation in a familiar codebase is
lower verbal load and tolerates a steady pulse. No strong coding-specific literature
exists; this is extrapolation from the task-complexity findings (Gonzalez & Aiello
2019), flagged as such. Steady, predictable, instrumental pulse music is a reasonable
default; drop to ambient or silence when reading/debugging hard code.

### 2.3 Boring/admin work

**Verdict: WELL-SUPPORTED.** The clearest *positive* case for stimulating music:
simple, repetitive tasks benefit from added arousal (Gonzalez & Aiello 2019; the
arousal-mood mechanism). Lyrics and favorites are fine here - the task doesn't compete
for verbal working memory.

### 2.4 Creative thinking

**Verdict: MIXED.** Some studies find positive-mood music broadens ideation; others
(e.g., [Threadgold et al. 2019](https://onlinelibrary.wiley.com/doi/10.1002/acp.3532))
found background music *impaired* verbal insight problem-solving. The honest summary:
moderate arousal and good mood help divergent thinking; verbal creative work is still
verbal work. Treat creative-session music as mood scaffolding before/between thinking,
not during verbal ideation.

### 2.5 Stress reduction and recovery

**Verdict: WELL-SUPPORTED - one of the strongest literatures.**
[de Witte et al. (2020, *Health Psychology Review*)](https://pubmed.ncbi.nlm.nih.gov/31167611/)
ran two meta-analyses over 100+ studies: music interventions produced significant
small-to-medium reductions in both physiological (heart rate, blood pressure, cortisol)
and psychological stress outcomes. A companion meta-analysis on therapist-delivered
music therapy ([de Witte et al. 2022](https://www.tandfonline.com/doi/full/10.1080/17437199.2020.1846580))
found a medium-to-large effect (d ≈ 0.72). Slow tempo (~60-80 BPM), low dynamic range,
and predictability recur as the effective ingredients. Note the effect does **not**
depend on any special frequency or genre - preferred calm music works.

### 2.6 Emotional processing

**Verdict: MODERATE - real but person-dependent, with a known failure mode.**
[Taruffi & Koelsch (2014, *PLOS ONE*)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110490)
(n=772) found sad music reliably provides emotion regulation, consolation, and
imaginative reward - nostalgia, not raw sadness, is the most common evoked emotion.
Benefits are larger for high-empathy listeners. The failure mode: for ruminators,
sad music can entrench low mood rather than process it (mood-regulation styles
literature, Saarikallio and others). Use deliberately, time-boxed, not as all-day
background.

### 2.7 Walking and light exercise

**Verdict: WELL-SUPPORTED - the strongest positive case in the whole literature.**
[Terry, Karageorghis et al.'s meta-analysis (2020, *Psychological Bulletin*, 139
studies)](https://www.semanticscholar.org/paper/Effects-of-music-in-exercise-and-sport%3A-A-review.-Terry-Karageorghis/99f14f1a71027bf338568c65216235c51ba000e5)
found music improves affective valence (g = 0.48), physical performance (g = 0.31),
reduces perceived exertion (g = 0.22), and even improves oxygen-use efficiency
(g = 0.15). Fast tempo beats slow; personally motivational, familiar music beats
generic. This is where your favorite energetic vocal music belongs.

### 2.8 Sleep

**Verdict: WELL-SUPPORTED for subjective sleep quality; mechanism is mundane.**
The [Cochrane review (Jespersen et al. 2022, 13 RCTs, n=1,007)](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD010459.pub3/full)
found moderate-certainty evidence that music listening improves subjective sleep
quality in insomnia, with low-certainty evidence for faster sleep onset and better
efficiency. The plausible mechanism is relaxation + pre-sleep routine/conditioning -
**not** "delta-wave entrainment." Sedative-music criteria across trials: slow
(~60-80 BPM), smooth onsets, narrow dynamics, no lyrics, low volume, used consistently
at the same point in the wind-down.

### 2.9 Deliberate mood lift

**Verdict: WELL-SUPPORTED for short-term mood, MODERATE for lasting effect.**
Music is one of the most reliable laboratory mood-induction tools, and
[Ferguson & Sheldon (2013)](https://www.researchgate.net/publication/265086573_Trying_to_be_happier_really_can_work_Two_experimental_studies)
found the combination that matters: *upbeat music + the intention to feel better*
improved mood, while passive listening alone did not (and over-monitoring your own
mood undermines it). Two studies, so the durability claim is moderate - but the
short-term effect rests on a much older mood-induction literature.

### 2.10 Anger processing - matching beats soothing

**Verdict: MODERATE (small studies, consistent with music-therapy practice).**
[Sharman & Dingle (2015)](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2015.00272/full)
anger-induced 39 extreme-metal listeners: their own aggressive music did *not*
make them angrier - hostility fell as much as in silence, while positive
activation rose. This supports the music-therapy "iso principle": match the
current arousal first, then shift - don't force calm music onto a furious brain.
Caveats: small n, fans only; matching works with music *you* identify with.

### 2.11 Intimacy and sexual arousal

**Verdict: WEAK-to-MODERATE - plausible mechanisms, thin direct literature,
preference and context dominate.**
The only well-identified mechanism is **excitation transfer**: arousal from one
source (music) is misattributed to another. [Marin et al. (2017, *PLOS ONE*)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0183531)
showed arousing music increased sexual-attractiveness ratings of faces (in women,
in a lab). Beyond that: conditioning (music tied to shared history carries the
association), self-consciousness masking (background sound reduces inhibition the
same way it masks office noise), and the folk consensus on slow, bass-heavy,
smooth-timbred grooves - which is genre convention, not a tested prescription.
No study validates any specific "aphrodisiac" genre, tempo, or (obviously)
frequency. Honest design guidance: personal/shared associations first, general
arousal + low awkwardness second, everything else is taste.

---

## 3. Skeptic's corner

### 3.1 Binaural beats - MIXED, and wildly oversold

The honest reading is messier than either camp admits.
[Garcia-Argibay et al.'s meta-analysis (2019, *Psychological Research*)](https://pubmed.ncbi.nlm.nih.gov/30073406/)
reported a medium pooled effect (g = 0.45) across cognition, anxiety, and pain. But
[Basu & Banerjee's 2022 meta-analysis](https://link.springer.com/article/10.1007/s00426-022-01706-7)
found mixed results for memory and attention with major methodological variability,
and recent well-powered work (e.g., a [2025 parametric study in *Scientific
Reports*](https://www.nature.com/articles/s41598-025-88517-z)) found no convincing
sustained-attention enhancement. Underlying studies are small, blinding is nearly
impossible, and the "brainwave entrainment" mechanism is far weaker at the cortex than
marketing implies. **Verdict: possibly a small real effect, mechanism unclear, nowhere
near the "40 Hz unlocks genius mode" claims. CognitionFM does not use binaural beats
and does not need to.**

### 3.2 432 Hz / 528 Hz / solfeggio frequencies - DEBUNKED / MARKETING

No credible evidence that any specific tuning frequency has healing or cognitive
properties. The "ancient solfeggio scale" is a 1990s numerological construction;
ancient cultures could not measure Hertz. The handful of small studies (e.g., on
432 Hz tuning) are underpowered, poorly controlled, and unreplicated. When a slow
528 Hz drone relaxes someone, it's because slow, predictable, low-variability sound
relaxes people (§1.2, §2.5) - the number is irrelevant. **CognitionFM tunes to
A=440 like everyone else and says so publicly.**

### 3.3 "Dopamine music" - MARKETING (a real finding, misread)

Salimpoor et al. (2011, *Nature Neuroscience*) did show striatal dopamine release
during musical chills - for music the listener already loved, at peak emotional
moments. That is a finding about musical pleasure, not a productivity lever. "Boost
dopamine to focus" playlists misappropriate it; intensely pleasurable music is, if
anything, *more* attention-capturing during complex work (§1.2).

### 3.4 Lo-fi hip-hop - the properties are fine, the mythology is not

No special "lo-fi mechanism" exists. Lo-fi works for many people because it is
incidentally well-designed for the changing-state findings: no lyrics, narrow dynamic
range, repetitive structure, moderate tempo, familiar harmonic language. Any music
with those properties does the same job. (That property list is, not coincidentally,
close to CognitionFM's deep-work recipe.)

### 3.5 White/pink noise and "brown noise for ADHD" - MODERATE for noise-masking, WEAK for enhancement

Steady broadband noise is the theoretical ideal steady-state sound: maximum masking,
zero changing-state content. Evidence supports it for masking disruptive environments;
evidence for cognitive *enhancement* (including the stochastic-resonance/ADHD line) is
small and inconsistent. It's a legitimate, boring alternative to music for verbal deep
work - worth including in personal A/B tests.

---

## 4. Claims we may publicly make (and their honest phrasing)

This table feeds every public title and description, wherever the mixes are
published. Nothing stronger than the right column ever ships.

| Underlying finding | ✅ Honest public phrasing | ❌ Never say |
|---|---|---|
| Changing-state / lyrics disrupt verbal work | "Designed around research on why lyrics and sudden changes break focus" | "Scientifically proven to boost focus" |
| Arousal-mood hypothesis | "Built to hold a calm, steady level of alertness" | "Activates your brain's focus network" |
| de Witte stress meta-analyses | "Slow, predictable music measurably reduces stress in controlled studies" | "Melts cortisol away" |
| Jespersen Cochrane sleep review | "Music as part of a wind-down routine improves sleep quality in clinical trials" | "Delta waves put you into deep sleep" |
| No frequency magic | "Tuned to standard A=440 - no healing-frequency claims here, because the evidence isn't" | anything with "432 Hz," "528 Hz," "solfeggio," "Hz healing" |
| Preference/person moderators | "Test it against silence - this works for many people, not everyone" | "Works for everyone" |

---

## 5. Reference list

- Basu & Banerjee (2022). Potential of binaural beats intervention for improving memory and attention. *Psychological Research*. [link](https://link.springer.com/article/10.1007/s00426-022-01706-7)
- Cheah et al. (2022). Background music and cognitive task performance: systematic review. *Music & Science*. [link](https://journals.sagepub.com/doi/full/10.1177/20592043221134392)
- de Witte et al. (2020). Effects of music interventions on stress-related outcomes: systematic review and two meta-analyses. *Health Psychology Review*. [link](https://pubmed.ncbi.nlm.nih.gov/31167611/)
- de Witte et al. (2022). Music therapy for stress reduction: systematic review and meta-analysis. *Health Psychology Review*. [link](https://www.tandfonline.com/doi/full/10.1080/17437199.2020.1846580)
- Ferguson & Sheldon (2013). Trying to be happier really can work. *Journal of Positive Psychology*. [link](https://www.researchgate.net/publication/265086573_Trying_to_be_happier_really_can_work_Two_experimental_studies)
- Furnham & Bradley (1997). Music while you work. *Applied Cognitive Psychology*. [link](https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1099-0720(199710)11:5%3C445::AID-ACP472%3E3.0.CO;2-R)
- Garcia-Argibay, Santed & Reales (2019). Efficacy of binaural auditory beats: meta-analysis. *Psychological Research*. [link](https://pubmed.ncbi.nlm.nih.gov/30073406/)
- Gonzalez & Aiello (2019). More than meets the ear. *JEP: Applied*. [link](https://www.researchgate.net/publication/330693127_More_Than_Meets_the_Ear_Investigating_How_Music_Affects_Cognitive_Task_Performance)
- Jespersen et al. (2022). Listening to music for insomnia in adults. *Cochrane Database of Systematic Reviews*. [link](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD010459.pub3/full)
- Kämpfe, Sedlmeier & Renkewitz (2011). The impact of background music on adult listeners: meta-analysis. *Psychology of Music*. [link](https://journals.sagepub.com/doi/10.1177/0305735610376261)
- Marin, Schober, Gingras & Leder (2017). Misattribution of musical arousal increases sexual attraction. *PLOS ONE*. [link](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0183531)
- Perham & Currie (2014). Does listening to preferred music improve reading comprehension? *Applied Cognitive Psychology*. [link](https://onlinelibrary.wiley.com/doi/abs/10.1002/acp.2994)
- Pietschnig, Voracek & Formann (2010). Mozart effect-Shmozart effect: meta-analysis. *Intelligence*. [link](https://www.sciencedirect.com/science/article/abs/pii/S0160289610000267)
- Salamé & Baddeley (1982). Disruption of short-term memory by unattended speech. *JVLVB*. [link](https://www.sciencedirect.com/science/article/abs/pii/S0022537182905210)
- Sharman & Dingle (2015). Extreme metal music and anger processing. *Frontiers in Human Neuroscience*. [link](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2015.00272/full)
- Taruffi & Koelsch (2014). The paradox of music-evoked sadness. *PLOS ONE*. [link](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110490)
- Terry, Karageorghis et al. (2020). Effects of music in exercise and sport: meta-analytic review. *Psychological Bulletin*. [link](https://www.semanticscholar.org/paper/Effects-of-music-in-exercise-and-sport%3A-A-review.-Terry-Karageorghis/99f14f1a71027bf338568c65216235c51ba000e5)
- Thompson, Schellenberg & Husain (2001). Arousal, mood, and the Mozart effect. *Psychological Science*. [link](https://journals.sagepub.com/doi/10.1111/1467-9280.00345)
- Threadgold et al. (2019). Background music stints creativity. *Applied Cognitive Psychology*. [link](https://onlinelibrary.wiley.com/doi/10.1002/acp.3532)
- Changing-state effect overviews: [Frontiers 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00346/full), [Auditory Perception & Cognition 2022](https://www.tandfonline.com/doi/full/10.1080/25742442.2022.2127988)
