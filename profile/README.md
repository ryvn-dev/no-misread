# Your profile

Everything in this folder describes one author. It starts empty, and the skill
runs on generic thresholds until you calibrate.

```bash
python3 lint/soundhuman.py --learn essay.md notes.md old-post.md
```

Point it at writing **you produced without a model**. Old blog posts, long
emails, commit messages, anything with your fingerprints on it. Aim for 2,000
words or more. Below twenty sentences it refuses, because a profile built on
noise then gets applied to everything you write afterwards.

## What it measures

**Your spread.** The generic rule flags a draft whose sentence lengths sit
within a standard deviation of 5. That number is a guess about writers in
general. Once calibrated it compares against you: someone whose own prose runs
at a spread of 14 has a problem at 8, and the fixed floor never sees it.

**Your words.** The worn-word list is a list of words generated text overuses.
It was never a list of words that are wrong. If you say `leverage` six times
across 4,000 words of your own writing, it is your word, and `--check` stops
flagging it. The evidence is frequency in prose you wrote, so the list cannot
grow from a preference you asserted once.

## Two files, both required

`voice.json` is machine-readable and read on every `--check`, so the next run
uses it without anyone remembering to. `learnings.md` is the reason, dated, in
your own words.

Nobody can argue with a number that has no reason attached, and a reason with
no number never fires. Keep both.

## Updating

Run `--learn` again with newer samples. Entries append rather than overwrite,
and `history` keeps every calibration, so you can see your own writing move.
Roughly every couple of months is enough unless your register changes.

To drop an entry, delete it from `voice.json` by hand and say why in
`learnings.md`. The file is yours.

## What it will not do

It will not learn from text a model wrote, including text this skill rewrote.
That closes a loop where the profile drifts toward the model's habits while
claiming to describe yours. Feed it your own writing, or nothing.

It will not imitate another author. Calibration describes you.

This repository ignores `voice.json`. Your writing profile is yours, and it
does not belong in a public fork.
