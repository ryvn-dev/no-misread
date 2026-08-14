# Changelog

## 1.0.0 - 2026-08-15

First release.

**Skill**
- `SKILL.md`: twelve rules, a pre-delivery checklist, and a six-dimension score
  where invisible characters are pass/fail rather than scored.
- `references/tells.md`: words, phrases, run-ups, closing rituals, and the
  hedges that must survive an edit.
- `references/patterns.md`: sentence and paragraph shapes, including the rhythm
  measurement.
- `references/examples.md`: ten before/after pairs, one of which changes no
  words at all and only moves the sentence breaks.

**Linter** (`lint/nomisread.py`, standard library only, no install)
- `--strip` erases twelve invisible characters, eight non-keyboard spaces, and
  ten pieces of machine typography. Characters change, words do not.
- `--check` counts twelve classes of tell and reports sentence-length spread.
- `--self-test` proves both directions: a dirty fixture must score, a clean
  fixture must score zero.

**Other surfaces**
- `output-styles/no-misread.md` for Claude Code output styles.
- `prompts/system-prompt.md`, about 250 words, for a system prompt or a custom
  instruction box.
- `.claude-plugin/` manifests for plugin and marketplace installation.
