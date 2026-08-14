# Head-to-head: four skills, one baseline, two instruments

Five conditions wrote the same six tasks on sonnet. Every output got scored by
two instruments with opposite loyalties: our linter, which counts what our
skill teaches, and SimpleEnglish's `ste_lint.py`, which counts what the STE
school teaches. Winning only on your own scorer proves compliance with
yourself, so the cross cells are the ones worth reading.

Run of 2026-08-15, after our system prompt gained its machine-bound section.
The earlier run, before that fix, sits in git history with our technical cells
at 3.66 and 7.30.

| condition | ours/100w | theirs/100w | prose stdev | metronomic cells |
|---|---|---|---|---|
| baseline | 3.61 | 4.08 | 7.6 | 0 |
| **no-misread** | 1.22 | 1.28 | 5.8 | 0 |
| stop-slop | 3.27 | 2.58 | 6.8 | 0 |
| simple-english | 0.00 | 0.00 | 4.3 | 1 |
| asd-ste100 | 1.13 | 0.98 | 3.5 | 0 |

Split by direction:

| condition | prose ours | prose theirs | tech ours | tech theirs |
|---|---|---|---|---|
| baseline | 2.35 | 3.15 | 6.13 | 5.93 |
| **no-misread** | 1.57 | 0.84 | 0.54 | 2.15 |
| stop-slop | 1.91 | 1.47 | 5.99 | 4.80 |
| simple-english | 0.00 | 0.00 | 0.00 | 0.00 |
| asd-ste100 | 1.70 | 0.64 | 0.00 | 1.67 |

## Reading it straight

**SimpleEnglish sweeps both counters, and its prose is the flattest on the
table.** Zero violations on both instruments, essay stdev 3.1, one cell
formally metronomic. The six-book human baseline in the arena runs stdev 12 to
22. A counter built from word lists cannot see this, which is why both
counters said perfect while the rhythm said machine. The STE style is correct
for its own goal, which is text a machine parses; applied to an essay it
produces exactly the uniformity that detection research flags.

**Our first technical result was a real loss, and the fix showed up in the numbers.** The
system prompt only carried prose rules, so on tool descriptions and error
messages we scored worse than baseline: 3.66 on our instrument, 7.30 on
theirs. After adding the machine-bound section, 0.54 and 2.15. That is the
test-then-fix loop doing its job.

**On the cross cells we now hold the best non-STE position.** 1.28 on their
instrument against stop-slop's 2.58 and baseline's 4.08, while keeping a prose
spread of 5.8 against their 4.3 and 3.5.

## Caveats

One generation per cell, and it matters: our prose cells moved from 0.00 to
1.57 on our own instrument between two runs whose prompt differed by one
paragraph. Treat single-cell differences as noise and directional means as
signal. Both instruments are word-and-pattern counters; neither measures
whether the writing is good. The rhythm column is our own metric, stated as
such. Raw generations sit in `raw/h2h__*` for reading.
