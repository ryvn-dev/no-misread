# Patterns: sentence and paragraph shapes

Words are the easy layer. A draft can pass every list in `tells.md` and still
read as machine-written, because the shapes survive vocabulary edits. This file
is the layer that matters.

## Rhythm

Read a page and look only at the lengths. Ignore the words.

Generated prose holds a band. Most sentences land between twelve and eighteen
words, because each one is drawn toward the most likely next length, and the
most likely length is the average. Page after page, the same shape.

Human prose lurches. Four words. Then a sentence that runs thirty-one words
because the thought did not finish and the writer kept going rather than break
it in half. Then nine.

The linter reports this as `stdev_words`. Under 5.0, the text reads metronomic
no matter how good the vocabulary is.

**Fix:** break one sentence in three, and let one run long. Do not
redistribute evenly. Even distribution is the disease.

| Shape | Reads as |
|---|---|
| 14, 16, 13, 15, 17 words | machine |
| 4, 22, 9, 31, 7 words | person |
| 5, 5, 5, 5 words | person trying too hard |

That last row matters. Stacked short sentences are their own tell. Fragments
for drama read as manufactured intensity: *"Speed. Quality. Cost. Pick two.
That's it."* Write the sentence.

<!-- no-misread: off -->
## Reveal by negation

The most recognisable machine sentence in English. Set up a wrong answer,
knock it down, deliver the right one.

- "It's not X. It's Y."
- "Not just X, but Y."
- "The problem isn't X. It's Y."
- "X isn't about Y. It's about Z."
- "It stops being X and starts being Y."

The frame makes an ordinary claim feel earned, because the reader gets a small
reversal for free. Once you see it you cannot unsee it, and neither can your
reader.

**Fix:** state Y. Delete the negation entirely. If Y is not interesting without
the run-up, Y was not the point.

## Negative listing

The same move stretched over several sentences. "Not a tool. Not a framework.
A way of thinking." A striptease where the reader waits through two false
answers for one real one.

**Fix:** give the real one first.

## Abstractions with human verbs

Generated text avoids naming an actor, and reaches for abstraction as the
subject instead.

| Written | What happened |
|---|---|
| the data tells us | someone read it and drew a conclusion |
| the culture shifted | people changed what they did |
| the decision emerged | someone decided |
| the conversation moved toward | someone changed the subject |
| the market rewards | buyers paid for it |
| the complaint became a fix | an engineer fixed it that Thursday |
| adoption accelerated | more people signed up |

**Fix:** name the human. When no specific person fits, use *you* and put the
reader in the seat. When neither works, the sentence was empty and should go.

## Narration from a distance

"Nobody designed this." "People tend to underestimate." "This is why teams
struggle." A voice hovering above the scene, describing a category of person
from outside it.

**Fix:** put the reader in the room. "You do not sit down one morning and
decide to build this" beats "nobody designed this."

## Vague declaratives

Sentences that announce significance without carrying anything.

- The implications are significant.
- The reasons are structural.
- The stakes could not be higher.
- This changes everything.
- The consequences are real.

Every one can be deleted with zero loss, which is the test.

**Fix:** name the implication, the reason, the stake. If you cannot, you did
not have one.

## Passive voice with the actor hidden

"Mistakes were made." "The feature was deprecated." "It is believed that."

Passive is not always wrong. It is right when the actor is genuinely unknown,
or when the object is the subject of the paragraph. It is wrong when it is
hiding someone.

**Fix:** ask who did it. If you know, say. If the answer is "we", say we.

## The tricolon

Three parallel items, in rhythm: *fast, reliable, and scalable*. One is
rhetoric. A page of them is a tic, and generated prose produces them at a rate
no human writer sustains, because three is where a list sounds complete.

**Fix:** two items land. One lands harder. Use three when there are exactly
three things, not when the sentence wants a beat.

## Paragraph shape

| Pattern | Problem |
|---|---|
| Every paragraph ends on a short punchy line | The rhythm becomes audible, then tiring |
| Every paragraph opens with a transition word | So, But, And, Now, Yet as scaffolding |
| Every bullet is `**Bold lead**: explanation` | The format is doing the thinking |
| Paragraphs all four to five sentences long | Same disease as sentence rhythm, one level up |
| Section closes by restating the section | Nothing added, length doubled |

**Fix:** vary where the weight sits. Some paragraphs end quietly. Some run two
sentences, some run eight.

## Structural scaffolding

Text that announces its own architecture.

- "In this section, we'll look at..."
- "The rest of this piece explains..."
- "As we'll see below..."
- "Let me walk you through..."
- "First, some background."

**Fix:** delete. Let the piece move. Readers can see the headings.

## Emoji as section markers

🚀 ✨ 🎯 at the head of sections, or leading every bullet. Almost nobody does
this by hand in prose. It arrives from templates and from generated markdown.

**Fix:** remove. Keep emoji where a person would use one, which is roughly
never in a document and sometimes in a message.

## What to keep

Not every regularity is a tell. Parallel structure in a genuine list, a
repeated opening for deliberate effect, a short sentence after a long one for
weight: these are craft. The tell is not the device. The tell is the device
appearing at a rate that no writer chose.
<!-- no-misread: on -->
