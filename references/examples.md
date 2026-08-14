# Before and after

Every change below names the rule it applies. Where a rewrite would have cost
meaning, the longer version stays and the note says why.

<!-- no-misread: off -->
---

## 1. Run-up, worn words, tricolon

**Before**

> Here's the thing: in today's fast-paced landscape, engineering teams need to
> leverage robust, comprehensive, and innovative tooling in order to unlock
> their full potential.

**After**

> Engineering teams need better tools.

Cut the run-up ("here's the thing"), the setting ("in today's fast-paced
landscape"), the worn verbs ("leverage", "unlock"), and the three-adjective
run. What survived is the claim. It is thin, which the original was hiding.

---

## 2. Reveal by negation

**Before**

> The problem isn't that the tests are slow. It's that nobody trusts them.

**After**

> Nobody trusts the tests.

The negation exists to give the real claim a small reversal to arrive on. State
the claim.

---

## 3. Abstraction performing a human action

**Before**

> The data tells us that adoption stalled in Q3, and the culture shifted toward
> caution.

**After**

> Adoption stalled in Q3. After the outage, three team leads stopped approving
> new rollouts.

"The data tells us" hides the reader of the data. "The culture shifted" hides
the people who changed what they did. Naming them turned one empty sentence
into a specific one, and made the piece longer. That is the correct trade.

---

## 4. Rhythm, with no vocabulary changes at all

**Before** (17, 16, 15, 16 words)

> The parser reads each row and converts it into an internal record format.
> Each record is then validated against the schema before it moves onward.
> Invalid records are written to a separate file for later manual review.
> The valid records continue to the writer, which batches them for upload.

**After** (6, 27, 4, 19 words)

> The parser reads a row.
> It converts the row to an internal record, checks that record against the
> schema, and sends it onward, unless the record fails, in which case it goes
> to a rejects file.
> Nobody reads that file.
> The rest reach the writer, which batches them and uploads the batch.

Same facts, same words, same order. The only change is where the sentences
break. The first version reads as generated because the lengths sit within two
words of each other for four lines. The last line is also a joke, which the
first version had no room for.

---

## 5. Vague declarative

**Before**

> The security implications of this change are significant, and the stakes for
> the team could not be higher.

**After**

> Anyone with a read-only token can now list every user's email address.

The original could be deleted with no loss. That is the test for a vague
declarative.

---

## 6. Passive voice hiding the actor

**Before**

> Mistakes were made during the migration, and the rollback was delayed.

**After**

> I ran the migration against production instead of staging. I noticed forty
> minutes later, which is why the rollback was late.

Passive was doing exactly one job here.

---

## 7. Closing ritual

**Before**

> In conclusion, choosing the right database depends on your access patterns,
> your scale, and your team's experience. Ultimately, the bottom line is that
> there is no one-size-fits-all answer. Hope this helps!

**After**

> Pick the database your team has already run in production. The access
> patterns matter less than the experience does.

Three closing rituals stacked, and none of them said anything. The rewrite
takes a position, which is what the reader wanted from the section.

---

## 8. A hedge that must survive

**Before**

> The upload may have failed because the credentials lack `s3:PutObject`.

**After**

> The upload may have failed. The credentials lack `s3:PutObject`, which is the
> most common cause.

Two sentences instead of one, and the hedge stayed. "The upload failed because
the credentials lack `s3:PutObject`" is shorter, reads better, and asserts a
cause the original did not know. That is not a rewrite. It is a different
claim, and in an error message it sends the reader to fix the wrong thing.

**Kept as-is:** "may have failed" - the original did not know.

---

## 9. Invisible marks

**Before** (as rendered)

> The service returns a 200 on success.

**Before** (as stored)

> `The service returns a 200<U+200B> on success.`

**After**

> The service returns a 200 on success.

No visible difference and no wording change. The zero-width space sat between
the number and the space, survived three copy-pastes, and broke a `grep` for
`200 on`. Reading cannot find this. Run `--strip`.

---

## 10. Text that should not be rewritten

**Before**

> Warning: do not open the enclosure while the capacitor is charged. Wait five
> minutes after disconnecting power.

**After**

> Warning: do not open the enclosure while the capacitor is charged. Wait five
> minutes after disconnecting power.

No change. Two flat, plain, imperative sentences of similar length, in the
passive-adjacent register of safety text. The rhythm rule would have you break
one up. Do not. Uniformity is correct here, because the reader is scanning
under pressure and a stylistic flourish costs them time.

The rules describe prose written to be read. They are not a compliance gate to
run over every string in a repository.
<!-- no-misread: on -->
