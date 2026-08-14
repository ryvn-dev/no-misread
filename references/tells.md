# Tells: words and phrases

No word on this list is wrong. Every one of them is ordinary English, and most
were doing useful work until generated text picked them up and used them at ten
times the rate a person would, which is the only reason they now read as a
signature rather than as vocabulary. Frequency put them on this list, not taste.

Replacements are plainer, never fancier. When nothing fits, delete.

<!-- no-misread: off -->
## Characters no keyboard produces

Check these first, because reading cannot find them.

| Character | Name | Why it is there |
|---|---|---|
| `U+200B` | zero-width space | Invisible. Survives copy-paste. Breaks search and diff. |
| `U+200C` `U+200D` | zero-width non-joiner / joiner | Legitimate in Persian, Hindi, Arabic. Not in English prose. |
| `U+2060` | word joiner | Invisible, no rendering effect at all. |
| `U+FEFF` | byte-order mark | Belongs at the head of a file, never mid-sentence. |
| `U+00AD` | soft hyphen | Invisible until the line wraps, then a hyphen appears from nowhere. |
| `U+00A0` `U+202F` | no-break space, narrow no-break space | Look like spaces. Are not spaces. |
| `U+2007` `U+2009` `U+200A` | figure, thin, hair space | Typesetting widths nobody types by hand. |

`--strip` removes all of them. Run it before you judge a text by reading it.

## Typography

| Avoid | Use | Note |
|---|---|---|
| `—` em dash | comma, full stop, or restructure | The single loudest visual tell in generated prose. |
| `–` en dash | hyphen | Correct in ranges, rare in typed drafts. |
| `“ ” ‘ ’` curly quotes | `" '` | Word processors produce them. Keyboards do not. |
| `…` ellipsis character | `...` | Same reason. |
| `→ ≥ ≤` | `-> >= <=` | Fine in maths. A tell in prose. |

## Words worn out by generation

| Worn | Plain |
|---|---|
| delve into | study, examine, read |
| leverage | use |
| utilize | use |
| harness | use |
| facilitate | help, allow, run |
| optimize | improve, tune |
| streamline | simplify, shorten |
| navigate (a problem) | handle, deal with, get through |
| unpack (an idea) | explain |
| unlock (value, potential) | name what it actually produces |
| foster | build, encourage, cause |
| underscore | show, prove |
| showcase | show |
| elevate | improve, raise |
| empower | let, allow, enable |
| bolster | strengthen, support |
| embark on | start, begin |
| deep dive | study, review |
| double down | commit, spend more |
| circle back | return to |
| lean into | accept, do more of |

## Adjectives that claim instead of show

| Claim | What to do |
|---|---|
| robust, powerful, comprehensive | Give the number or the range that earns it. |
| seamless, effortless, frictionless | Say how many steps it takes. |
| innovative, cutting-edge, state-of-the-art | Say what it does that the previous thing did not. |
| crucial, vital, pivotal, paramount | Say what breaks without it. |
| intricate, nuanced, multifaceted | Name the parts. |
| game-changing, transformative | Name what changed. |
| myriad, plethora | Give the count. |
| vibrant, bustling, nestled, breathtaking | Travel-brochure register. Cut. |

## Adverbs

Delete on sight. Each one props up a sentence that has not earned emphasis.

really · very · just · quite · simply · actually · basically · literally ·
genuinely · honestly · truly · deeply · fundamentally · inherently ·
inevitably · undoubtedly · certainly · clearly · obviously · notably ·
importantly · crucially · significantly · essentially · ultimately ·
arguably · remarkably · incredibly · extremely · highly · particularly

Keep an adverb that carries information: *quietly*, *twice*, *badly*,
*yesterday*. The test is whether deleting it changes the meaning. If nothing
changes, it was decoration.

## Run-up phrases

The point comes after these. Start there instead.

- Here's the thing / here's what / here's why / here's the problem
- Let's dive in / let's talk about / let's unpack / let's be clear
- It's worth noting that / it's important to note that
- It turns out that
- The truth is / the reality is / the fact is
- Make no mistake
- When it comes to
- At the end of the day
- In today's fast-paced world / in an ever-evolving landscape
- In a world where
- What if I told you
- Think about it

## Closing rituals

Human writing stops on its last real sentence. Machine writing winds down.

- In conclusion / to sum up / in summary / all in all
- Overall, / ultimately, / in essence, / at its core,
- The bottom line is / the key takeaway is
- Remember that
- Hope this helps / let me know if you have any questions

## Emphasis that adds nothing

- Let that sink in.
- Full stop. / Period.
- And that's okay.
- That's it. That's the whole thing.
- I promise.
- No more, no less.

These arrive after a sentence has already made its point, to insist it landed.
If it landed, the insistence is redundant. If it did not, the insistence does
not help.

## Hedges: keep these

The lists above are things to cut. This one is not.

*may*, *might*, *probably*, *usually*, *in most cases*, *we think* — these
carry the writer's confidence, and confidence is content. "The upload probably
failed" and "the upload failed" are different claims, and a length cap is
exactly the pressure that tempts you to collapse the first into the second.

Cut around a hedge. Never through it.

What to cut is hedges stacked on hedges: *may potentially*, *might possibly*,
*could perhaps sometimes*, *it is possible that this may*. One hedge states
uncertainty. Three state nothing.
<!-- no-misread: on -->
