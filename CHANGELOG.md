# Changelog

## 2.0.0 - 2026-08-15

Renamed from sound-human. That name covered half the problem. The other half
runs the other way: a person writes a prompt and the model reads something they
did not say. One failure, two directions.

**Both directions**
- Text going out to a model gets the rules that stop a misparse: no
  contractions, no vague modals, nothing over 25 words, and the rhythm rule
  switched off, because a reader scanning a procedure wants one shape.
- Text coming back to a person keeps the previous behaviour.
- Most rules hold in both. Three flip.

**No mode switch**
- `--check` reads the text and decides. Frontmatter with a description field is
  a spec somebody loads. A quarter of sentences opening with an imperative
  means somebody executes this.
- Every report carries `direction` and `direction_why`, so you can argue with
  the call. `--type` overrides it.

**Calibration**
- `--learn` measures writing the author produced without a model and records
  their real sentence spread and the worn words they use. Later drafts get
  compared against them rather than against a generic floor.
- The profile resolves `$NOMISREAD_PROFILE`, then `./profile/voice.json` for a
  checked-in house voice, then `~/.no-misread/voice.json`.
- It refuses to learn from model output, including its own.

**Measurement**
- `band_share` joins `stdev_words`: the share of sentences within 25% of the
  mean. A text has to fail both to count as metronomic, so a terse passage no
  longer trips it.
- `evals/run_bench.py` runs baseline against skill and measures with the linter
  rather than a judge. The judge pass is optional, runs both orders, and counts
  only consistent wins.

**Fixes**
- Docs told installed users to run `python3 lint/nomisread.py`, which resolves
  against their project and fails. Both files now build the path from the
  skill's own directory.
- Markdown tables and tight lists have no sentence-ending punctuation between
  rows, so the splitter glued whole tables into one 68-word sentence. That
  inflated the length check and skewed the rhythm number.
- Three semicolons, several empty adverbs, and every em dash in the repo's own
  prose, all caught by running the linter over itself.

**Honesty**
- The README now names the obvious way to game the rhythm check.

## 1.0.0 - 2026-08-15

First release, as sound-human. Skill, reference files, and a standard-library
linter with `--strip`, `--check`, and a two-directional self-test.
