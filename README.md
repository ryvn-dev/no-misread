# no-misread

Two people are talking through a keyhole, and neither can ask the other what
they meant.

You write a prompt, and the model reads something you did not say. The model
writes an answer, and you skim four dense paragraphs without taking in the one
sentence that mattered. Both failures are the same failure, running in opposite
directions, and almost nobody treats them as one problem.

This is a skill plus a linter for both directions. **You never pick a mode.**
The text says which way it is going, and the tool reads that.

```console
$ python3 lint/nomisread.py --check my-prompt.md
  "direction": "going out to a machine",
  "direction_why": "detected: 12 of 26 sentences open with an imperative"

$ python3 lint/nomisread.py --check the-answer.md
  "direction": "coming back to a person",
  "direction_why": "detected: only 2 of 65 sentences give an order"
```

**Going out.** Instructions, prompts, tool descriptions, error messages,
anything a model or a non-native reader parses with nobody to ask. Ambiguity is
the enemy, so even, flat, literal sentences are correct here.

**Coming back.** The answer, the draft, the README, the post going out under
your name. Machine cadence is the enemy, so the sentences have to move like a
person wrote them.

## The three that flip

| | Going out to a machine | Coming back to a person |
|---|---|---|
| Sentence length | Even, under 25 words | Varied, or it reads generated |
| Contractions | Avoid: a model misreads `won't` | Keep: people use them |
| `may` / `might` / `could` | Avoid: the reader cannot ask which | Keep: confidence is content |

Everything else holds in both directions. Invisible characters, active voice, a
named actor for every verb, specific over vague, no run-up phrases, no closing
rituals, no worn vocabulary, no reveal-by-negation.

So this is not a balance between two philosophies. One text has one job, and
the tool works out which. `--type technical` or `--type prose` overrides the
call when it gets one wrong, which is the only time you have to think about it.

## What reading cannot find

**Invisible characters.** Zero-width spaces, word joiners, byte-order marks,
soft hyphens, no-break spaces. No keyboard makes them. They survive copy-paste
and they break `grep` and `diff` on the way. `--strip` erases them.

**Rhythm.** Here is a paragraph with no banned words, no em dashes, no `delve`.
Every word list in this category passes it.

```
The parser reads each row and converts it into an internal record format.
Each record is validated against the schema before it moves down the pipeline.
Invalid records are written to a separate file for later manual review by us.
The valid records continue to the writer, which batches them before upload.
The writer retries a failed batch three times before it gives up completely.
```

```console
$ python3 lint/nomisread.py --check draft.md
  "rhythm": {"mean_words": 13, "stdev_words": 0.6, "band_share": 1.0,
             "shortest": 12, "longest": 14, "reads_metronomic": true},
  "verdict": "sentence lengths sit too close together"
```

Twelve, fourteen, fourteen, thirteen, twelve. People do not write like that. We
write four words, then thirty-one, then nine, because a thought ends when it
ends.

Detection research calls this burstiness. Published comparisons put roughly 85%
of GPT-4o's sentences inside a 15-28 word band, against human writing that runs
from four words to past fifty with no centre. Score low on burstiness and
perplexity together and detectors flag the text over 90% of the time. Raise
burstiness alone and that drops to around 40%.

`--check` reports the spread and `band_share`, the fraction of sentences within
25% of the mean. A text has to fail both before this calls it metronomic, so a
deliberately terse passage does not get flagged for being short.

## It calibrates to you

The generic floor is a guess about writers in general, and you are not writers
in general.

```bash
python3 "$SKILL/lint/nomisread.py" --learn old-post.md notes.md email.md
```

Point it at prose **you wrote without a model**. It measures your real spread
and records which worn words you use, then checks later drafts against you.

```console
$ python3 lint/nomisread.py --check draft.md      # before
  "profile": "none (generic thresholds)",  "tells": {"worn_word": 3}

$ python3 lint/nomisread.py --learn my-essays/*.md
  your spread: stdev 9.9 words (mean 12.4, 3 to 38)
  words kept as yours: leverage

$ python3 lint/nomisread.py --check draft.md      # after
  "profile": "applied",  "tells": {},  "yours_not_flagged": ["leverage"]
```

The worn-word list was never a list of words that are wrong. Say `leverage` six
times across four thousand words of your own writing and it is your word.
Evidence is frequency in prose you wrote, so the list cannot grow from a
preference you asserted once.

It refuses to learn from model output, including its own. That loop drifts the
profile toward the model's habits while claiming to describe you.

The profile lands in `~/.no-misread/voice.json`, so it follows you between
projects. A repository that wants a checked-in house voice puts one at
`./profile/voice.json` and that wins. `$NOMISREAD_PROFILE` overrides both.

## Install

```bash
npx skills add ryvn-dev/no-misread --skill no-misread --agent claude-code
```

or clone it:

```bash
git clone https://github.com/ryvn-dev/no-misread ~/.claude/skills/no-misread
```

**Plugin** - add this repository as a marketplace, then install `no-misread`.
**Projects and custom instructions** - paste `prompts/system-prompt.md`, about
250 words. **Output style** - copy `output-styles/no-misread.md`. **Linter
alone** - `lint/nomisread.py` is one file, standard library, no install.

## Use

```bash
SKILL=~/.claude/skills/no-misread     # wherever you installed it

python3 "$SKILL/lint/nomisread.py" --strip draft.md > clean.md
python3 "$SKILL/lint/nomisread.py" --check clean.md   # direction detected for you
python3 "$SKILL/lint/nomisread.py" --self-test
```

A bare `python3 lint/nomisread.py` only works from inside a clone. Installed as
a skill, build the path from where you installed it.

Or ask: *"make this sound human"*, *"rewrite this prompt so the model can't
misread it"*, *"strip the watermark"*.

`--check` exits 1 when it finds something, so it drops into CI as a gate. This
repository runs it over its own prose on every push.

## What it does not do

It does not make weak writing true. A paragraph with nothing to say comes out
cleaner and still empty.

It does not defeat detection, and does not try to. It removes the artefacts of
generation so that writing worth reading gets read on its own terms. Where you
have to disclose that you used AI, disclose it.

It does not parse grammar. The linter is regex plus your reading. A zero means
clean of what the linter knows about, not proof that a person wrote it.

Do not run `--strip` on source code. Straight-quoting a string literal changes
the string.

## Attribution

MIT. Use it, fork it, sell what you build with it.

If you ship this skill or a derivative, keep the copyright notice and credit
`ryvn-dev/no-misread`. That is the whole ask, and the licence requires it.

**If it caught something in your writing, star the repo.** That is how the next
person finds it.

## Licence

[MIT](LICENSE) © 2026 ryvn-dev
