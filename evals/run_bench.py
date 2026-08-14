#!/usr/bin/env python3
"""Measure whether the skill changes anything. Baseline against skill.

Every number this prints comes from a generation that actually ran. Nothing
here is estimated, and a cell that failed prints as a failure rather than
disappearing from the average.

Design, and what it is worth:

  1. DETERMINISTIC PASS (primary). Generate a text twice per scenario, once
     with the skill in the prompt and once without, then run both through
     lint/nomisread.py. No model judges anything, so no judge bias exists to
     argue about. This is the number to trust.

  2. JUDGE PASS (secondary, --judge). A model scores the two texts blind. Run
     each pair in both orders and count a win only when the SAME text wins
     both times, because position bias in pairwise judging can move accuracy
     by more than ten points. Averaging the two scores hides that; requiring
     agreement surfaces it as a tie.

Known ceiling, stated because it changes how much the judge pass is worth:
the judge and the writer are the same model family. Cross-family judging is
the correct fix and this harness does not do it, so read the judge table as
suggestive and the deterministic table as evidence.

Usage:
  python3 evals/run_bench.py                  # deterministic only
  python3 evals/run_bench.py --judge          # add the judge pass
  python3 evals/run_bench.py --models haiku   # narrow the matrix
Resumable: finished cells are cached in evals/results/raw/.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(HERE, "results", "raw")
sys.path.insert(0, os.path.join(ROOT, "lint"))
import nomisread as nm  # noqa: E402

MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-5",
}

SCENARIOS = [
    ("readme-intro", "coming back",
     "Write the introduction section of a README for a CLI tool called sqlpipe "
     "that syncs Postgres tables to S3 as Parquet. About 120 words. Return only "
     "the text."),
    ("incident", "coming back",
     "Write a public status-page incident report. Between 14:02 and 14:31 UTC, "
     "12% of API requests failed with HTTP 502 after a deploy removed the cache "
     "warmup step. The deploy was reverted at 14:27. About 100 words. Return "
     "only the text."),
    ("release-notes", "coming back",
     "Write release notes for sqlpipe v2.0: the name field of /v2/users split "
     "into first_name and last_name, which breaks clients; a new --incremental "
     "flag; Parquet writes 40% faster. About 120 words. Return only the text."),
    ("essay", "coming back",
     "Write about 150 words on why small teams ship faster than large ones. "
     "Return only the text."),
    ("tool-description", "going out",
     "Write the description field for a tool called search_orders that an AI "
     "agent will read to decide when to call it. It searches orders by customer "
     "email, date range, and status, returns at most 50, and errors if the date "
     "range exceeds one year. About 80 words. Return only the text."),
    ("error-message", "going out",
     "Write the exact error message sqlpipe prints when an S3 upload fails with "
     "AccessDenied because the IAM credentials lack s3:PutObject. Two to four "
     "lines. Return only the message text."),
]

JUDGE_RUBRIC = """You are judging two versions of the same text, A and B.

Score each 0-10 on how much it reads as though a careful person wrote it,
rather than as generated filler. Weigh these, in order:

1. Rhythm. Do sentence lengths vary, or do they hold one band?
2. Specificity. Named things, or categories standing in for them?
3. Ownership. Does someone perform the verbs, or do abstractions act?
4. Restraint. Anything present to impress rather than to inform?
5. Ending. Does it stop, or wind down with a summary?

Reply with only this JSON and nothing else:
{"a": <0-10>, "b": <0-10>, "winner": "a" | "b" | "tie", "why": "<12 words>"}
"""


# The first run of this harness was invalid, and the reason is worth keeping.
# It ran with the working directory inside this repository, so the CLI had file
# access and answered the writing task by READING no-misread's own examples and
# reporting on them. Both conditions produced commentary about this project
# rather than the text that was asked for.
#
# A writing benchmark has to measure writing. Generation runs in an empty
# directory with tools switched off, so the model has the prompt and nothing
# else.
SANDBOX = os.path.join(HERE, "results", ".sandbox")


def run_claude(prompt, model, timeout=240):
    os.makedirs(SANDBOX, exist_ok=True)
    try:
        p = subprocess.run(["claude", "-p", prompt, "--model", model,
                            "--tools", "none"],
                           cwd=SANDBOX,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if p.returncode != 0:
        return None, (p.stderr or "nonzero exit")[:200]
    text = p.stdout.strip()
    return (text, None) if text else (None, "empty output")


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


def skill_prompt(task):
    with open(os.path.join(ROOT, "prompts", "system-prompt.md"), encoding="utf-8") as fh:
        rules = fh.read()
    return f"{rules}\n\n---\n\nFollowing every rule above:\n\n{task}"


def generate(model_key, scen_id, task, condition):
    def produce():
        prompt = skill_prompt(task) if condition == "skill" else task
        text, err = run_claude(prompt, MODELS[model_key])
        return {"text": text, "error": err}
    return cache(f"{model_key}__{condition}__{scen_id}", produce)


def judge(model_key, scen_id, first, second, order):
    def produce():
        prompt = f"{JUDGE_RUBRIC}\n\n--- A ---\n{first}\n\n--- B ---\n{second}\n"
        text, err = run_claude(prompt, MODELS["sonnet"])
        if err:
            return {"error": err}
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            return {"error": "no json in judge reply"}
        try:
            return json.loads(m.group(0))
        except ValueError:
            return {"error": "bad json in judge reply"}
    return cache(f"{model_key}__judge__{scen_id}__{order}", produce)


def main():
    args = sys.argv[1:]
    want_judge = "--judge" in args
    models = list(MODELS)
    if "--models" in args:
        models = args[args.index("--models") + 1].split(",")

    rows, failures, judged = [], [], []
    for mk in models:
        for scen_id, direction, task in SCENARIOS:
            pair = {}
            for cond in ("baseline", "skill"):
                got = generate(mk, scen_id, task, cond)
                if got.get("error"):
                    failures.append(f"{mk}/{scen_id}/{cond}: {got['error']}")
                    continue
                mode = "technical" if direction == "going out" else "prose"
                report = nm.check(got["text"], None, mode)
                pair[cond] = report
                print(f"  {mk:8} {scen_id:18} {cond:9} "
                      f"tells={report['tells_total']:<3} "
                      f"per100w={report['tells_per_100w']:<6} "
                      f"stdev={report['rhythm'].get('stdev_words', '-')}")
            if len(pair) == 2:
                rows.append((mk, scen_id, direction, pair))

            if want_judge and len(pair) == 2:
                b = generate(mk, scen_id, task, "baseline")["text"]
                s = generate(mk, scen_id, task, "skill")["text"]
                fwd = judge(mk, scen_id, b, s, "bs")   # A=baseline B=skill
                rev = judge(mk, scen_id, s, b, "sb")   # A=skill    B=baseline
                if "error" in fwd or "error" in rev:
                    failures.append(f"{mk}/{scen_id}/judge")
                else:
                    skill_won_fwd = fwd.get("winner") == "b"
                    skill_won_rev = rev.get("winner") == "a"
                    if skill_won_fwd and skill_won_rev:
                        verdict = "skill"
                    elif (not skill_won_fwd) and (not skill_won_rev) and \
                            fwd.get("winner") != "tie" and rev.get("winner") != "tie":
                        verdict = "baseline"
                    else:
                        verdict = "inconsistent"   # order flipped the answer
                    judged.append((mk, scen_id, verdict))

    print("\n" + "=" * 78)
    print("DETERMINISTIC PASS (no model judged anything)")
    print("=" * 78)
    print(f"{'model':9} {'scenario':18} {'dir':12} {'base/100w':>10} {'skill/100w':>11} {'change':>8}")
    tot_b = tot_s = 0.0
    for mk, scen_id, direction, pair in rows:
        b = pair["baseline"]["tells_per_100w"]
        s = pair["skill"]["tells_per_100w"]
        tot_b += b
        tot_s += s
        change = "-" if b == 0 else f"{(s - b) / b * 100:+.0f}%"
        print(f"{mk:9} {scen_id:18} {direction:12} {b:>10} {s:>11} {change:>8}")
    if rows:
        drop = "-" if tot_b == 0 else f"{(tot_s - tot_b) / tot_b * 100:+.1f}%"
        print(f"\n  n={len(rows)} pairs   mean tells/100w "
              f"{tot_b / len(rows):.2f} -> {tot_s / len(rows):.2f}   ({drop})")

    if judged:
        print("\n" + "=" * 78)
        print("JUDGE PASS (same model family as the writer: suggestive, not evidence)")
        print("=" * 78)
        wins = sum(1 for _, _, v in judged if v == "skill")
        losses = sum(1 for _, _, v in judged if v == "baseline")
        flips = sum(1 for _, _, v in judged if v == "inconsistent")
        print(f"  skill wins both orders: {wins}")
        print(f"  baseline wins both orders: {losses}")
        print(f"  order changed the answer, counted as neither: {flips}")
        for mk, scen_id, v in judged:
            print(f"    {mk:8} {scen_id:18} {v}")

    if failures:
        print("\nFAILED CELLS (not silently dropped):")
        for f in failures:
            print("  " + f)

    with open(os.path.join(HERE, "results", "results.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "pairs": [{"model": m, "scenario": s, "direction": d,
                       "baseline_per100w": p["baseline"]["tells_per_100w"],
                       "skill_per100w": p["skill"]["tells_per_100w"],
                       "baseline_stdev": p["baseline"]["rhythm"].get("stdev_words"),
                       "skill_stdev": p["skill"]["rhythm"].get("stdev_words")}
                      for m, s, d, p in rows],
            "judged": [{"model": m, "scenario": s, "verdict": v} for m, s, v in judged],
            "failures": failures,
        }, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
