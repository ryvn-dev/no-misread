# no-misread

A linter and a Claude skill for both halves of working with a model: the prompt
you send it, and the prose it sends back. Prompts get checked for ambiguity,
because the model rarely asks what you meant: it guesses and runs. Output gets checked for machine
tells, because readers can hear them.

<img src="assets/demo.svg" alt="Terminal output: a paragraph with no banned words and no em dashes still fails, because every sentence lands within two words of the last" width="760">

[繁體中文](README.zh.md)

## What it checks

**In any text**
- Invisible characters: zero-width spaces, word joiners, BOM, soft hyphens.
  Keyboards cannot type them, they survive copy-paste, and they break `grep`.
  `--strip` erases them without touching a single word.
- Machine typography: em dashes, curly quotes, the one-character ellipsis.
- Worn vocabulary, run-up phrases, closing rituals, "not X, it's Y" frames,
  abstractions doing human verbs, vague importance claims.

**In prose** - sentence rhythm. The demo above shows why this one matters: that
paragraph passes every word list in this category, and its sentence lengths are
12, 14, 14, 13, 12. People write 4, then 31, then 9. [Detection
research](https://www.textsight.ai/blog/sentence-length-variance/) calls the
measurement burstiness; `--check` reports the spread (`stdev_words`) and
how packed the middle is (`band_share`), and flags the text only when both
fail, so terse writing is safe.

**In prompts** - the reverse. Contractions the model can misparse, `may` /
`might` / `could` the reader cannot resolve, sentences over 25 words. Even,
flat sentences are correct here, so the rhythm check turns off.

You never pick a mode. The tool reads the text and reports which rules it
applied and why:

```console
$ python3 lint/nomisread.py --check my-prompt.md
  "direction": "going out to a machine",
  "direction_why": "detected: 12 of 26 sentences open with an imperative"
```

`--type prose` or `--type technical` overrides a wrong call.

**Chinese** gets its own rule set the moment `--check` sees it: half-width punctuation
inside Chinese text (the loudest tell there is), translation-shaped grammar,
the worn words (「賦能」「顆粒度」「值得注意的是」), and rhythm counted in
characters. The first draft of this project's own Chinese README scored 87
problems; the current one scores 0.

## Install

```bash
npx skills add ryvn-dev/no-misread --skill no-misread --agent claude-code
```

or clone it:

```bash
git clone https://github.com/ryvn-dev/no-misread ~/.claude/skills/no-misread
```

Plugin: add this repo as a marketplace, install `no-misread`. System prompt:
paste `prompts/system-prompt.md` (~250 words). Output style:
`output-styles/no-misread.md`. The linter alone is one file, standard library,
no install.

## Use

```bash
SKILL=~/.claude/skills/no-misread

python3 "$SKILL/lint/nomisread.py" --strip draft.md > clean.md
python3 "$SKILL/lint/nomisread.py" --check clean.md
python3 "$SKILL/lint/nomisread.py" --learn my-post.md notes.md   # calibrate
python3 "$SKILL/lint/nomisread.py" --self-test
```

Or ask Claude: "make this sound human", "rewrite this prompt so the model
can't misread it".

`--check` exits 1 on findings, so it works as a CI gate. This repo runs it on
its own prose every push.

## Calibration

`--learn` measures writing you produced without a model: your real sentence
spread, and which of the worn words you use. Later checks compare against you
instead of a generic floor. Say `leverage` six times in four thousand words of
your own writing and it stops getting flagged, with the evidence recorded.

It refuses to learn from model output, including its own rewrites. The profile
lives at `~/.no-misread/voice.json`; a checked-in `./profile/voice.json` wins
for a team house style.

## Results and limits

Benchmarked over two models and six scenarios: mean tells per 100 words fell
from 2.74 to 1.34. All eight prose cells improved. Two technical cells on the
smaller model got worse, and [evals/results/RESULTS.md](evals/results/RESULTS.md)
leads with the caveat that the linter measures compliance with its own rules,
not writing quality.

You can game the rhythm check by planting a three-word sentence in every
paragraph. Nothing stops that. The number reports a symptom, and chasing it
as a target grows a different tic.

A zero score means clean of what a regex can see. It is not proof a person
wrote the text, and this tool does not try to defeat AI detectors. Where you
have to disclose that you used AI, disclose it.

Do not run `--strip` on source code: straightening quotes inside a string
literal changes the string.

## License

[MIT](LICENSE) © 2026 ryvn-dev. Use it however you like and keep the copyright
notice. If it caught something in your writing, star the repo so the next
person finds it.
