# Model phrase lists

One `.txt` per model family, one phrase per line, `#` for comments. `--check`
counts every occurrence in prose as `model_phrase`.

Entry requirements, in order:

1. `tools/mine_patterns.py` found it recurring across unrelated tasks in that
   model's own generations.
2. A person read the candidates and kept only habits, not domain nouns.

The first mining run over 12 cached generations found zero cross-task phrase
repeats, so this folder ships with no lists. That is a finding, not an
omission: 12 short samples are too few, and a list typed from memory would be
taste wearing a measurement's clothes.
