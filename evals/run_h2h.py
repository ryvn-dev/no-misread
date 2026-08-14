#!/usr/bin/env python3
"""Head-to-head: our skill against the three biggest skills in the category.

Same tasks, same model, five conditions. Every text gets scored by TWO
instruments with opposite loyalties:

  ours      lint/nomisread.py        counts what OUR skill teaches
  theirs    competitors/ste_lint.py  SimpleEnglish's own scorer, counts what
                                     THEIR school teaches

Neither number is neutral, and that is the point of using both. The cell that
matters is the cross: how our output scores on their instrument, and how
theirs scores on ours. Winning only on your own scorer proves compliance with
yourself.

Conditions:
  baseline        the bare task
  no-misread      our prompts/system-prompt.md
  stop-slop       hardikpandya/stop-slop, SKILL.md + reference files
  simple-english  AminBlg/SimpleEnglish SKILL.md
  asd-ste100      danyuchn/asd-ste100-skill SKILL.md

Generation runs in an empty directory with tools off. One generation per
cell, cached in results/raw/ under h2h__ names; the sonnet baseline and
no-misread cells reuse the earlier benchmark's generations byte for byte.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(HERE, "results", "raw")
SANDBOX = os.path.join(HERE, "results", ".sandbox")
sys.path.insert(0, os.path.join(ROOT, "lint"))
sys.path.insert(0, os.path.join(HERE, "competitors"))
import nomisread as nm  # noqa: E402
import ste_lint  # noqa: E402

MODEL = "claude-sonnet-5"

CONDITIONS = {
    "baseline": None,
    "no-misread": os.path.join(ROOT, "prompts", "system-prompt.md"),
    "stop-slop": os.path.join(HERE, "competitors", "stop-slop-SKILL.md"),
    "simple-english": os.path.join(HERE, "competitors", "simple-english-SKILL.md"),
    "asd-ste100": os.path.join(HERE, "competitors", "asd-ste100-SKILL.md"),
}

# Reuse the earlier run's generations for the two conditions it already ran.
REUSE = {"baseline": "sonnet__baseline__{s}"}

SCENARIOS = [
    ("readme-intro", "prose",
     "Write the introduction section of a README for a CLI tool called sqlpipe "
     "that syncs Postgres tables to S3 as Parquet. About 120 words. Return only "
     "the text."),
    ("incident", "prose",
     "Write a public status-page incident report. Between 14:02 and 14:31 UTC, "
     "12% of API requests failed with HTTP 502 after a deploy removed the cache "
     "warmup step. The deploy was reverted at 14:27. About 100 words. Return "
     "only the text."),
    ("release-notes", "prose",
     "Write release notes for sqlpipe v2.0: the name field of /v2/users split "
     "into first_name and last_name, which breaks clients; a new --incremental "
     "flag; Parquet writes 40% faster. About 120 words. Return only the text."),
    ("essay", "prose",
     "Write about 150 words on why small teams ship faster than large ones. "
     "Return only the text."),
    ("tool-description", "technical",
     "Write the description field for a tool called search_orders that an AI "
     "agent will read to decide when to call it. It searches orders by customer "
     "email, date range, and status, returns at most 50, and errors if the date "
     "range exceeds one year. About 80 words. Return only the text."),
    ("error-message", "technical",
     "Write the exact error message sqlpipe prints when an S3 upload fails with "
     "AccessDenied because the IAM credentials lack s3:PutObject. Two to four "
     "lines. Return only the message text."),
]


def cache(name, produce):
    os.makedirs(RAW, exist_ok=True)
    path = os.path.join(RAW, name + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    value = produce()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(value, fh, indent=1, ensure_ascii=False)
    return value


def generate(cond, scen_id, task):
    if cond in REUSE:
        reuse = os.path.join(RAW, REUSE[cond].format(s=scen_id) + ".json")
        if os.path.exists(reuse):
            with open(reuse, encoding="utf-8") as fh:
                return json.load(fh)

    def produce():
        skill_file = CONDITIONS[cond]
        if skill_file:
            with open(skill_file, encoding="utf-8") as fh:
                body = fh.read()
            # A SKILL.md opens with ---, which claude -p reads as a CLI flag.
            # Frontmatter is packaging, not writing rules, so drop it, and
            # feed the prompt on stdin so no first character can be an option.
            if body.startswith("---\n"):
                end = body.find("\n---\n", 4)
                if end != -1:
                    body = body[end + 5:]
            prompt = f"{body}\n\nFollowing every rule above:\n\n{task}"
        else:
            prompt = task
        os.makedirs(SANDBOX, exist_ok=True)
        try:
            p = subprocess.run(["claude", "-p", "--model", MODEL,
                                "--tools", "none"],
                               input=prompt,
                               cwd=SANDBOX, capture_output=True, text=True,
                               timeout=300)
        except subprocess.TimeoutExpired:
            return {"text": None, "error": "timeout"}
        if p.returncode != 0:
            return {"text": None, "error": (p.stderr or "nonzero exit")[:200]}
        text = p.stdout.strip()
        return {"text": text, "error": None if text else "empty output"}
    return cache(f"h2h__{cond}__{scen_id}", produce)


def main():
    rows, failures = {}, []
    for cond in CONDITIONS:
        for scen_id, kind, task in SCENARIOS:
            got = generate(cond, scen_id, task)
            if got.get("error"):
                failures.append(f"{cond}/{scen_id}: {got['error']}")
                continue
            text = got["text"]
            ours = nm.check(text, None, "prose" if kind == "prose" else "technical")
            theirs = ste_lint.lint(
                text, "descriptive" if kind == "prose" else "procedural")
            rows[(cond, scen_id)] = {
                "kind": kind,
                "ours": ours["tells_per_100w"],
                "theirs": theirs["violations_per_100w"],
                "stdev": ours["rhythm"].get("stdev_words"),
                "metro": bool(ours["rhythm"].get("reads_metronomic")),
            }
            print(f"  {cond:15} {scen_id:18} ours={ours['tells_per_100w']:<6} "
                  f"theirs={theirs['violations_per_100w']:<6} "
                  f"stdev={ours['rhythm'].get('stdev_words', '-')}")

    print("\n" + "=" * 76)
    print(f"{'condition':16} {'ours/100w':>10} {'theirs/100w':>12}   (mean over cells, lower wins)")
    print("-" * 76)
    summary = {}
    for split in ("prose", "technical", None):
        label = split or "ALL"
        print(f"--- {label}")
        for cond in CONDITIONS:
            cells = [v for (c, s), v in rows.items()
                     if c == cond and (split is None or v["kind"] == split)]
            if not cells:
                continue
            o = sum(v["ours"] for v in cells) / len(cells)
            t = sum(v["theirs"] for v in cells) / len(cells)
            sd = [v["stdev"] for v in cells if v["stdev"] is not None]
            sd_mean = round(sum(sd) / len(sd), 1) if sd else None
            metro = sum(1 for v in cells if v["metro"])
            summary[(label, cond)] = (round(o, 2), round(t, 2), sd_mean, metro)
            print(f"{cond:16} {o:>10.2f} {t:>12.2f}   stdev={sd_mean}  metronomic={metro}")

    if failures:
        print("\nFAILED CELLS (not dropped silently):")
        for f in failures:
            print("  " + f)

    with open(os.path.join(HERE, "results", "h2h.json"), "w", encoding="utf-8") as fh:
        json.dump({"cells": {f"{c}::{s}": v for (c, s), v in rows.items()},
                   "summary": {f"{a}::{b}": v for (a, b), v in summary.items()},
                   "failures": failures}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
