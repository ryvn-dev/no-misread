#!/usr/bin/env python3
"""Mine a model's favourite phrases from its own generations.

A phrase earns a place on a tell list by frequency in real output, not by
anyone's taste. This reads a folder of cached generations, counts word
n-grams, and keeps the ones that recur across many samples AND across
different writing tasks. The task filter is the important half: with six
scenarios about the same CLI tool, "postgres tables to s3" repeats because
the prompts repeat, and only phrases that surface no matter what the model
was asked to write are habits of the model.

Usage:
  python3 tools/mine_patterns.py evals/results/raw/'*baseline*.json'
  python3 tools/mine_patterns.py --min-docs 4 --min-scen 3 <glob...>

Output: one phrase per line with its counts, ready to curate by hand into
lint/patterns/. Curate, do not paste: the miner cannot tell a habit from a
domain word, and a pattern file full of scenario nouns would flag every
text about that domain.
"""

import glob
import json
import os
import re
import sys
from collections import defaultdict


def words(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]+`", " ", text)
    return re.findall(r"[a-z][a-z'-]*", text.lower())


def scenario_of(path):
    # cache names look like  model__condition__scenario.json
    base = os.path.basename(path).rsplit(".", 1)[0]
    return base.split("__")[-1]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    def opt(name, default):
        return int(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default
    min_docs = opt("--min-docs", 4)
    min_scen = opt("--min-scen", 3)

    files = []
    for pattern in args:
        files.extend(glob.glob(pattern))
    if not files:
        raise SystemExit("no files matched")

    in_docs = defaultdict(set)     # ngram -> set of file paths
    in_scens = defaultdict(set)    # ngram -> set of scenarios
    for path in sorted(set(files)):
        try:
            data = json.load(open(path, encoding="utf-8"))
            text = data.get("text") or ""
        except (ValueError, OSError):
            text = open(path, encoding="utf-8").read()
        if not text:
            continue
        ws = words(text)
        seen = set()
        for n in (3, 4, 5):
            for i in range(len(ws) - n + 1):
                seen.add(" ".join(ws[i:i + n]))
        for g in seen:
            in_docs[g].add(path)
            in_scens[g].add(scenario_of(path))

    rows = [(len(in_docs[g]), len(in_scens[g]), g)
            for g in in_docs
            if len(in_docs[g]) >= min_docs and len(in_scens[g]) >= min_scen]
    # Longer phrases first at equal support, so "the most common cause is"
    # outranks its own fragments.
    rows.sort(key=lambda r: (-r[0], -len(r[2])))

    kept = []
    for docs, scens, g in rows:
        if any(g in longer for longer in kept):
            continue
        kept.append(g)
        print(f"{docs:>3} docs  {scens} tasks   {g}")
    print(f"\n{len(kept)} candidate phrases from {len(set(files))} files. "
          "Curate before shipping: domain nouns are not habits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
