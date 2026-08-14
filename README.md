# sound-human

Make generated English read as though a person wrote it.

A skill plus a linter. The skill teaches the model what to stop doing. The
linter catches what reading cannot: characters no keyboard produces, and the
sentence rhythm that gives a text away no matter how good its vocabulary is.

## The part other tools miss

Here is a paragraph with no banned words, no em dashes, no `delve`, no `here's
the thing`. Every word list in this category passes it.

```
The parser reads each row and converts it into an internal record format.
Each record is validated against the schema before it moves down the pipeline.
Invalid records are written to a separate file for later manual review by us.
The valid records continue to the writer, which batches them before upload.
The writer retries a failed batch three times before it gives up completely.
```

```console
$ python3 lint/soundhuman.py --check draft.md
  "rhythm": {
    "sentences": 5,
    "mean_words": 13,
    "stdev_words": 0.6,
    "shortest": 12,
    "longest": 14,
    "reads_metronomic": true
  },
  "verdict": "sentence lengths sit too close together: vary them before anything else"
```

Twelve, fourteen, fourteen, thirteen, twelve. Every sentence within two words
of the last. People do not write like that. We write four words, then
thirty-one, then nine, because a thought ends when it ends.

Sentence-length spread survives every vocabulary edit, which is why swapping
`leverage` for `use` never fixes a text. Nothing else in this category measures
it.

## Three layers

**Characters.** Zero-width spaces, word joiners, byte-order marks, soft
hyphens, no-break spaces. Invisible, they survive copy-paste, and they break
`grep` and `diff` on the way through. `--strip` erases them.

**Typography.** Em dashes, curly quotes, the single-character ellipsis. Nobody
types these at speed.

**Sentences.** Run-up phrases, reveal-by-negation, abstractions performing human
verbs, vague declaratives, closing rituals, worn vocabulary, and rhythm.

## Install

**Claude Code skill**

```bash
git clone https://github.com/ryvn-dev/sound-human ~/.claude/skills/sound-human
```

**Claude Code plugin** - add this repository as a marketplace, then install
`sound-human`.

**Projects / custom instructions** - paste `prompts/system-prompt.md`, which is
about 250 words.

**Output style** - copy `output-styles/sound-human.md` into your output styles.

**Linter alone** - `lint/soundhuman.py` is one file, standard library only, no
install and no dependencies.

## Use

```bash
python3 lint/soundhuman.py --strip draft.md > clean.md   # erase the marks
python3 lint/soundhuman.py --check clean.md              # score what is left
python3 lint/soundhuman.py --self-test                   # prove the linter works
```

Or ask for it: *"make this sound human"*, *"strip the watermark"*, *"de-AI this
draft"*.

`--check` exits 1 when it finds something, so it drops into CI as a gate.

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

If you ship this skill, or a derivative of it, keep the copyright notice and
credit `ryvn-dev/sound-human`. That is the whole ask, and the licence requires
it.

## Licence

[MIT](LICENSE) © 2026 ryvn-dev
