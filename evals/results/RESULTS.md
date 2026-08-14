# Benchmark results

**Mean tells per 100 words fell from 2.74 to 1.34 across 12 pairs, a drop of
50.9%.** Two models, six scenarios, one generation per cell, measured 2026-08-15.

Read the caveats before quoting that number. The largest one says the result is
partly circular.

| model | scenario | direction | baseline | skill | change |
|---|---|---|---|---|---|
| haiku | readme-intro | coming back | 1.92 | 0.89 | -54% |
| haiku | incident | coming back | 1.85 | 0.00 | -100% |
| haiku | release-notes | coming back | 1.20 | 0.83 | -31% |
| haiku | essay | coming back | 1.95 | 0.63 | -68% |
| haiku | tool-description | going out | 1.28 | 1.33 | **+4%** |
| haiku | error-message | going out | 2.99 | 5.13 | **+72%** |
| sonnet | readme-intro | coming back | 1.37 | 0.00 | -100% |
| sonnet | incident | coming back | 2.86 | 0.00 | -100% |
| sonnet | release-notes | coming back | 1.77 | 0.00 | -100% |
| sonnet | essay | coming back | 3.40 | 0.00 | -100% |
| sonnet | tool-description | going out | 3.61 | 3.23 | -11% |
| sonnet | error-message | going out | 8.66 | 4.08 | -53% |

## What the shape of it says

**Every prose cell improved, eight out of eight, and half went to zero.** That
is the direction it targets, and it holds on both models.

**The going-out direction is where it struggles**, and on the smaller model it
made things worse twice. The error-message cell on haiku is the clearest
failure in the table: given 250 words of rules and asked for four lines, the
model produced something longer and chattier than the plain request did, and
the technical checks punished it. A short, flat, factual string is exactly the
case where a page of writing advice is the wrong intervention.

That is a real limitation and it belongs in the open. If you only write error
strings and tool descriptions, this skill earns its place on the larger model
and not reliably on the smaller one.

## Caveats

**The measurement is partly circular, and this is the caveat that matters.**
The linter counts the tells the skill tells the model to avoid, so a drop in
linter findings is close to measuring whether the model followed instructions.
It does not measure whether the writing got better. Read the falls as
compliance and the rises as failures of compliance, then read the texts. The
raw generations are in `raw/` so you can.

**One generation per cell.** No variance, no error bars. Re-run the matrix
before treating any single cell as a finding. The runner caches, so delete
`raw/` to start fresh.

**Twelve pairs.** Small. Two models from one family.

**The skill condition carries about 250 extra words of prompt.** Input token
counts are not comparable between conditions by design.

**No judge pass in this run.** The harness supports one, runs both orders, and
counts only consistent wins, but the judge would come from the same family as
the writer. Cross-family judging is the correct fix and this has not done it.

**No tool can certify that a person wrote a text**, including this one.

## An earlier run of this harness was invalid

The first attempt ran with the working directory inside this repository, so the
CLI had file access and answered the writing prompts by reading the project's
own examples and describing them. Both conditions produced commentary about
no-misread rather than the text the prompt asked for, and the summary line
read +42% before anyone opened the generations.

Generation now runs in an empty directory with tools switched off. The number
above comes from that run. I deleted the earlier one rather than keeping it as a
comparison, because it measured nothing.

## Reproduce

```bash
python3 evals/run_bench.py                  # deterministic pass
python3 evals/run_bench.py --judge          # add the judge pass
```
