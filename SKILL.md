---
name: sound-human
description: Rewrite generated English so it reads as though a person wrote it. Use when text sounds machine-made, when a draft needs to pass as native, when prose is going in front of readers who will judge it, or when output may carry invisible watermark characters. Triggers: sound human, humanize this, de-AI this, remove AI tells, strip the watermark, make this read native.
version: 1.0.0
license: MIT
---

# Sound Human

Generated English gives itself away twice: in characters a keyboard cannot
type, and in sentences built the same way every time. Erase the first. Rewrite
the second.

## Run the linter before you read

```bash
python3 lint/soundhuman.py --strip draft.md > clean.md   # erase the marks
python3 lint/soundhuman.py --check clean.md              # score what is left
```

The linter owns everything mechanical: invisible characters, typography, worn
words, sentence-length spread. Do not re-litigate its findings by eye, and do
not claim a text is clean without running it. Your judgment is for what it
cannot see, which is most of what matters.

If the linter is not available, apply the rules below by hand and say that you
did, so nobody mistakes an unchecked read for a measured one.

## The rules

**1. Strip the marks first.** Zero-width spaces, word joiners, byte-order
marks, soft hyphens, no-break spaces. Nobody types these. One of them survives
a copy-paste and the text announces its origin no matter how well it reads.
This is the only rule with a mechanical fix, so take it for free.

**2. Type like a keyboard.** Straight quotes. Three dots, not one character.
Hyphens, not dashes. A person writing at speed reaches for a comma or a full
stop, never an em dash.

**3. Vary sentence length or nothing else matters.** This is the rule the other
tools skip. Machine prose settles into a band, twelve to eighteen words, and
stays there for a page. Human prose lurches: four words, then thirty-one, then
nine. Read your draft and look only at the shapes. If every line is the same
length, you have written a clean, correct page that reads as generated, and no
word substitution will fix it. Break one sentence in three. Let one
run long.

**4. Give every verb an owner.** Data does not tell us. Cultures do not shift.
Decisions do not emerge. Someone read the number, changed their behaviour,
decided. Name them. When you cannot, the sentence was probably empty.

**5. Name the specific thing.** "The implications are significant" says
nothing. Which implication? To whom? A sentence that gestures at importance
without holding anything is filler wearing a suit.

**6. Delete the run-up.** "Here's the thing." "It's worth noting that." "Let's
dive in." Every one announces a point instead of making it. Cut the announcement
and start at the point.

<!-- sound-human: off -->
**7. Refuse the reveal-by-negation frame.** "It's not X, it's Y." "Not just X,
but Y." The setup exists to make a plain claim feel earned. State Y.

**8. Cut the adverbs.** Really, simply, actually, genuinely, fundamentally.
They add emphasis to sentences that have not earned it. If the sentence needs
propping up, the problem is the sentence.

**9. Retire the worn words.** Delve, leverage, robust, seamless, comprehensive,
navigate, unlock, foster, tapestry, landscape. Each was ordinary English before
generated text wore it out. Use the plain word underneath.
<!-- sound-human: on -->

**10. Stop when you are done.** No "in conclusion". No "the bottom line is". No
closing restatement of what the reader read. Human writing ends on its
last real sentence.

**11. Two beats three.** Three parallel items reads as a rhythm the writer
chose for its sound rather than its content. Two lands. One lands harder.

**12. Keep the hedges that carry meaning.** "The upload probably failed" and
"the upload failed" are different claims. Removing a hedge to tighten a sentence
changes what the text asserts. Tighten around hedges, never through them.

## Quick checks

Before delivering prose, in this order:

- Ran `--strip`? If not, the text may carry marks that reading cannot find.
- Any em dash, curly quote, or ellipsis character?
- Three sentences in a row within four words of each other in length?
- Any sentence where an abstraction performs a human action?
- Any sentence claiming something is important without naming it?
- Any paragraph whose first clause you could delete with nothing lost?
- Any "not X, it's Y"?
- Any -ly word carrying no information?
- Does the last paragraph restate the piece?
- Three-item list that would land harder with two?

## Score before you ship

| Dimension | Question | Out of |
|---|---|---|
| Marks | Any character a keyboard cannot produce? | pass / fail |
| Rhythm | Do the sentence lengths swing, or hold a band? | 10 |
| Ownership | Does a named someone perform each verb? | 10 |
| Specificity | Named things, or categories standing in for them? | 10 |
| Restraint | Anything here to impress rather than to inform? | 10 |
| Ending | Does it stop, or wind down? | 10 |

Marks is pass or fail, not a score. One invisible character fails the text
regardless of the other five.

Under 40 of 50, rewrite rather than edit. Edited machine prose stays machine
prose with better vocabulary; the shapes survive word-level fixes, and the
shapes are what the reader hears.

## What this does not do

It does not make weak writing true. A paragraph with nothing to say comes out
of this process shorter, cleaner, better punctuated, and still empty. If the
draft has no content, say so instead of polishing it.

It does not defeat detection, and does not try to. It removes the artefacts of
generation so that writing worth reading is read on its own terms. Where
you have to disclose that you used AI, disclose it. This skill changes how
prose sounds, never whether you tell the truth about who wrote it.

It does not apply to code, data, or quoted material. Straight quotes inside a
string literal change the string. Run `--strip` on prose files, not on source.

It is a regex pass plus your reading, not a grammar parser. A zero score means
clean of the things the linter knows about.

## References

- `references/tells.md` - the words and phrases, with the plain version of each
- `references/patterns.md` - the sentence and paragraph shapes
- `references/examples.md` - before and after, with the reason for each change
