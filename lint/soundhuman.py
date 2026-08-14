#!/usr/bin/env python3
"""sound-human: find and remove the marks that make English read as machine-written.

Two jobs, two modes.

  --strip   Rewrite the text with the machine marks taken out: invisible
            characters, and the typography no one types by hand. Safe to run
            on anything. It changes characters, never words.

  --check   Score the text. Reports the tells it can count, plus a rhythm
            measurement that no vocabulary list can catch: human sentence
            length swings, machine sentence length does not.

Ceiling, stated up front: this is a regex pass, not a parser. It cannot see
part of speech, so "that lead" and "to lead" look alike to it. It flags
passive voice only in its common forms. A zero score means the text is clean
of the things this file knows about, not that a person wrote it. Read the
prose yourself before you believe any number here.

Usage:
  python3 soundhuman.py --check  draft.md
  python3 soundhuman.py --strip  draft.md > clean.md
  cat draft.md | python3 soundhuman.py --check -
  python3 soundhuman.py --self-test

Exit codes for --check: 0 clean, 1 tells found.
"""

import json
import re
import statistics
import sys
import unicodedata

# ── Layer 1: characters a keyboard does not produce ────────────────────────
# A person typing in any normal editor emits none of these. Their presence is
# the single most reliable machine signal in a text, and the easiest to erase.

INVISIBLE = {
    "​": "zero-width space",
    "‌": "zero-width non-joiner",
    "‍": "zero-width joiner",
    "⁠": "word joiner",
    "﻿": "zero-width no-break space (BOM)",
    "­": "soft hyphen",
    "‎": "left-to-right mark",
    "‏": "right-to-left mark",
    "⁡": "function application",
    "⁢": "invisible times",
    "⁣": "invisible separator",
    "⁤": "invisible plus",
}

# Spaces that are not the space bar. Legitimate in typesetting, never in a
# draft someone typed, and a favourite carrier for encoded marks.
ODD_SPACE = {
    " ": "no-break space",
    " ": "narrow no-break space",
    " ": "figure space",
    " ": "thin space",
    " ": "hair space",
    " ": "punctuation space",
    " ": "medium mathematical space",
    "　": "ideographic space",
}

# ── Layer 2: typography that arrives with generated text ───────────────────
TYPOGRAPHY = {
    "—": ("em dash", " - "),
    "–": ("en dash", "-"),
    "‘": ("curly open single quote", "'"),
    "’": ("curly close single quote", "'"),
    "“": ("curly open double quote", '"'),
    "”": ("curly close double quote", '"'),
    "…": ("ellipsis character", "..."),
    "→": ("right arrow", "->"),
    "≥": ("greater-or-equal sign", ">="),
    "≤": ("less-or-equal sign", "<="),
}

# ── Layer 3: vocabulary ────────────────────────────────────────────────────
# Words that were ordinary English until generated text wore them out. The
# test for this list is frequency, not taste: each one appears in machine
# prose at many times its rate in human prose.

WORN_WORDS = re.compile(
    r"\b("
    r"delve|tapestry|testament|realm|landscape|intricate|meticulous|"
    r"nuanced|multifaceted|holistic|myriad|plethora|paramount|pivotal|"
    r"crucial|vital|robust|seamless|seamlessly|comprehensive|innovative|"
    r"cutting-edge|state-of-the-art|game-chang\w+|transformative|"
    r"leverag\w+|utiliz\w+|harness\w*|unlock\w*|elevat\w+|empower\w*|"
    r"foster\w*|underscor\w+|showcas\w+|navigat\w+|streamlin\w+|"
    r"facilitat\w+|optimiz\w+|bolster\w*|spearhead\w*|"
    r"boasts|nestled|bustling|vibrant|breathtaking|stunning|"
    r"ever-evolving|fast-paced|rapidly-changing|"
    r"resonat\w+|embark\w*|journey|beacon|treasure trove|"
    r"deep dive|dive into|double down|circle back|lean into|unpack"
    r")\b",
    re.I,
)

# Adverbs doing no work. Generated prose reaches for these to sound certain.
EMPTY_ADVERB = re.compile(
    r"\b("
    # "rather than" is a conjunction, not an intensifier, so it is excluded.
    r"really|very|just|quite|rather(?!\s+than)|simply|actually|basically|literally|"
    r"genuinely|honestly|truly|deeply|fundamentally|inherently|inevitably|"
    r"undoubtedly|certainly|clearly|obviously|notably|importantly|"
    r"crucially|significantly|effectively|essentially|ultimately|"
    r"arguably|remarkably|incredibly|extremely|highly|particularly"
    r")\b",
    re.I,
)

# ── Layer 4: sentence shapes ───────────────────────────────────────────────

# The reveal-by-negation frame. The most recognisable machine sentence there
# is: set up a wrong answer, knock it down, deliver the right one.
CONTRAST_FRAME = re.compile(
    r"\b("
    r"(?:it|this|that|the \w+)(?:'s| is| was)\s+not\s+(?:just\s+)?[^.!?]{2,60}?[,;:—–-]\s*(?:it|this|that)(?:'s| is| was)\b"
    r"|not\s+just\s+[^.!?]{2,60}?\bbut\s+(?:also\s+)?"
    r"|not\s+only\s+[^.!?]{2,60}?\bbut\s+(?:also\s+)?"
    r"|isn't\s+(?:just\s+)?(?:about\s+)?[^.!?]{2,60}?[,;:—–-]\s*it's\b"
    r"|the\s+(?:question|answer|problem|point|issue)\s+is(?:n't| not)\b"
    r"|stops?\s+being\s+[^.;!?]{2,40}?\band\s+starts?\s+being\b"
    r")",
    re.I,
)

# Announcing that a point is coming, instead of making it.
THROAT_CLEARING = re.compile(
    r"(?:^|[.!?]\s+|\n)\s*("
    r"here's (?:the thing|what|why|how|the (?:problem|catch|kicker|truth))"
    r"|let's (?:be clear|dive|talk|explore|unpack|break)"
    r"|it's (?:worth noting|important to note|no secret|no accident)"
    r"|it (?:turns out|is important to note)"
    r"|the (?:truth|reality|fact) is"
    r"|make no mistake"
    r"|at the end of the day"
    r"|in today's [\w\s-]{3,30}(?:world|landscape|era|market|environment)"
    r"|in (?:an|the) (?:ever-evolving|increasingly|rapidly)"
    r"|when it comes to"
    r"|in a world where"
    r"|think about it"
    r"|what if (?:i told you|we|you)"
    r")",
    re.I,
)

# Closing rituals. Human writing usually just stops.
WRAP_UP = re.compile(
    r"(?:^|[.!?]\s+|\n)\s*("
    r"in conclusion|to sum up|to summarize|in summary|all in all|"
    r"overall,|ultimately,|in essence,|at its core,|"
    r"the (?:bottom line|takeaway) is|"
    r"remember(?:,| that)|hope this helps|let me know if"
    r")",
    re.I,
)

# Emphasis that adds nothing after the sentence already made the point.
FALSE_EMPHASIS = re.compile(
    r"\b(let that sink in|full stop\.|period\.|and that's okay|"
    r"that's it\. that's|full circle|no more, no less)\b",
    re.I,
)

# Abstractions given human verbs, which hides who acted. A complaint does not
# become a fix. Someone fixed it.
FALSE_AGENCY = re.compile(
    r"\b("
    r"(?:the\s+)?(?:data|research|evidence|numbers?|results?)\s+(?:tells?|suggests?|reveals?|shows? us)\b"
    r"|(?:the\s+)?(?:culture|conversation|narrative|market|industry|landscape)\s+"
    r"(?:shifts?|moves?|evolves?|rewards?|demands?|shapes?)\b"
    r"|(?:the\s+)?(?:decision|consensus|pattern|truth|answer)\s+(?:emerges?|reveals? itself|becomes clear)\b"
    r"|\w+\s+becomes?\s+(?:a|an|the)\s+\w+\s+(?:overnight|instantly|immediately)\b"
    r")",
    re.I,
)

PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(\w+ed|made|done|given|taken|seen|"
    r"known|held|built|written|shown|found|left|kept|sent|told)\b(?!\s+by\s+\w)",
    re.I,
)

HEDGE_STACK = re.compile(
    r"\b(may|might|could|can)\s+(?:potentially|possibly|perhaps|sometimes|often|likely)\b"
    r"|\b(?:it is|it's)\s+(?:possible|likely)\s+that\s+\w+\s+(?:may|might|could)\b"
    r"|\bhelps?\s+to\s+(?:potentially|better)\b",
    re.I,
)

EMOJI_MARKER = re.compile(
    r"^\s*#{1,6}\s*[\U0001F300-\U0001FAFF☀-➿]"
    r"|^\s*[-*]\s*[\U0001F300-\U0001FAFF☀-➿]\s",
    re.M,
)

# Three parallel items. One tricolon is rhetoric; a page of them is a machine.
TRICOLON = re.compile(
    r"\b(\w+),\s+(\w+),\s+and\s+(\w+)\b(?!\s*[,:])",
    re.I,
)

BOLD_LEAD_BULLET = re.compile(r"^\s*[-*]\s+\*\*[^*]{2,40}\*\*\s*[:—-]", re.M)


# ── Text handling ──────────────────────────────────────────────────────────

def strip_code(text):
    """Remove the spans this file has no business judging.

    Four kinds, and each one is a real class of false positive rather than a
    convenience:

      code           machine typography is correct inside it
      block quotes   someone else's words, which you did not write
      off regions    `<!-- sound-human: off -->` ... `<!-- sound-human: on -->`,
                     for the passage where you quote a tell in order to name it
      links          a URL is not prose

    A document *about* these patterns necessarily contains them. Without the
    off marker this linter scores its own reference files as the worst prose
    it has ever seen, which is true only in the most literal sense.
    """
    text = re.sub(
        r"<!--\s*sound-human:\s*off\s*-->.*?<!--\s*sound-human:\s*on\s*-->",
        " ", text, flags=re.S | re.I)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " CODE ", text)
    text = re.sub(r"^\s*>.*$", " ", text, flags=re.M)
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"^\s{4,}\S.*$", " ", text, flags=re.M)
    return text


def sentences(text):
    body = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", text, flags=re.M)
    body = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.M)
    parts = re.split(r"(?<=[.!?])[\s\"')\]]+", body)
    return [p.strip() for p in parts if len(p.strip().split()) >= 3]


def find_chars(raw, table):
    hits = {}
    for ch, name in table.items():
        n = raw.count(ch)
        if n:
            hits[name] = n
    return hits


# Detection research calls this burstiness. Measured heads-up, generated prose
# packs most of its sentences into one narrow band while human prose spreads
# from a few words to fifty and past it, with no centre. Two numbers describe
# that, and the second one matters more:
#
#   stdev_words   the spread. One long outlier can carry it, so it is not
#                 sufficient on its own.
#   band_share    the share of sentences sitting within 25% of the mean. This
#                 is the shape the research actually describes, and a single
#                 outlier cannot hide a packed middle from it.
#
# A text is called metronomic when the spread is small AND the middle is
# packed. Requiring both keeps a deliberately terse passage from being
# reported as machine-written for the crime of being short.
BAND = 0.25
STDEV_FLOOR = 5.0
BAND_CEILING = 0.70


def rhythm(sents):
    lengths = [len(s.split()) for s in sents]
    if len(lengths) < 5:
        return {"sentences": len(lengths), "measurable": False}
    mean = statistics.mean(lengths)
    sd = statistics.pstdev(lengths)
    lo, hi = mean * (1 - BAND), mean * (1 + BAND)
    inside = sum(1 for n in lengths if lo <= n <= hi)
    share = inside / len(lengths)
    return {
        "sentences": len(lengths),
        "measurable": True,
        "mean_words": round(mean, 1),
        "stdev_words": round(sd, 1),
        "band_share": round(share, 2),
        "shortest": min(lengths),
        "longest": max(lengths),
        "reads_metronomic": sd < STDEV_FLOOR and share > BAND_CEILING,
    }


def check(raw):
    body = strip_code(raw)
    sents = sentences(body)
    words = max(1, len(body.split()))

    marks = {}
    marks.update(find_chars(raw, INVISIBLE))
    marks.update(find_chars(raw, ODD_SPACE))
    typo = {}
    for ch, (name, _) in TYPOGRAPHY.items():
        n = strip_code(raw).count(ch)
        if n:
            typo[name] = n

    counts = {
        "worn_word": len(WORN_WORDS.findall(body)),
        "empty_adverb": len(EMPTY_ADVERB.findall(body)),
        "contrast_frame": len(CONTRAST_FRAME.findall(body)),
        "throat_clearing": len(THROAT_CLEARING.findall(body)),
        "wrap_up": len(WRAP_UP.findall(body)),
        "false_emphasis": len(FALSE_EMPHASIS.findall(body)),
        "false_agency": len(FALSE_AGENCY.findall(body)),
        "passive": len(PASSIVE.findall(body)),
        "hedge_stack": len(HEDGE_STACK.findall(body)),
        "tricolon": len(TRICOLON.findall(body)),
        "emoji_marker": len(EMOJI_MARKER.findall(body)),
        "bold_lead_bullet": len(BOLD_LEAD_BULLET.findall(body)),
    }
    counts = {k: v for k, v in counts.items() if v}

    r = rhythm(sents)
    total = sum(counts.values()) + sum(marks.values()) + sum(typo.values())

    return {
        "words": words,
        "invisible_marks": marks,
        "machine_typography": typo,
        "tells": counts,
        "rhythm": r,
        "tells_total": total,
        "tells_per_100w": round(100.0 * total / words, 2),
        "verdict": verdict(total, marks, r),
    }


def verdict(total, marks, r):
    if marks:
        return "carries invisible characters: run --strip first"
    if r.get("reads_metronomic"):
        return "sentence lengths sit too close together: vary them before anything else"
    if total == 0:
        return "clean of everything this file can see"
    if total <= 3:
        return "close: fix the listed tells"
    return "reads as machine-written"


def strip(raw):
    """Erase the machine marks. Characters change, words do not."""
    out = raw
    for ch in INVISIBLE:
        out = out.replace(ch, "")
    for ch in ODD_SPACE:
        out = out.replace(ch, " ")
    for ch, (_, repl) in TYPOGRAPHY.items():
        out = out.replace(ch, repl)
    out = unicodedata.normalize("NFC", out)
    out = re.sub(r"[ \t]{2,}", " ", out)
    out = re.sub(r" +([,.;:!?])", r"\1", out)
    out = re.sub(r"[ \t]+$", "", out, flags=re.M)
    return out


# ── Self-test ──────────────────────────────────────────────────────────────

DIRTY = (
    "Here's the thing: in today's fast-paced landscape, teams must leverage "
    "robust, comprehensive, and innovative tooling to unlock value.​ It's "
    "not just about speed, it's about culture. The data tells us that adoption "
    "is significantly delayed. Results were seen across the board. This may "
    "potentially help teams navigate the journey — and that's okay. "
    "In conclusion, let that sink in."
)

CLEAN = (
    "We shipped the parser on Tuesday.\n\n"
    "It broke twice that week. Both times the input had a byte-order mark at "
    "the front of the file, which our reader treated as part of the first "
    "field name, so every lookup missed by one character and returned nothing "
    "at all. Ravi found it. He added four lines to the reader and a test that "
    "feeds it a marked file.\n\n"
    "Nobody has reported it since."
)


def self_test():
    d = check(DIRTY)
    assert d["invisible_marks"], d
    assert d["machine_typography"], d
    assert d["tells"]["worn_word"] >= 4, d["tells"]
    assert d["tells"]["throat_clearing"] >= 1, d["tells"]
    assert d["tells"]["contrast_frame"] >= 1, d["tells"]
    assert d["tells"]["false_agency"] >= 1, d["tells"]
    assert d["tells"]["hedge_stack"] >= 1, d["tells"]
    assert d["tells"]["tricolon"] >= 1, d["tells"]
    assert d["tells"]["wrap_up"] >= 1, d["tells"]
    assert d["tells"]["false_emphasis"] >= 1, d["tells"]
    assert d["tells"]["passive"] >= 1, d["tells"]

    stripped = strip(DIRTY)
    assert not check(stripped)["invisible_marks"], "strip left invisible characters"
    assert not check(stripped)["machine_typography"], "strip left machine typography"

    c = check(CLEAN)
    assert not c["invisible_marks"], c
    assert c["tells_total"] == 0, c["tells"]
    assert not c["rhythm"]["reads_metronomic"], c["rhythm"]

    print("self-test OK")
    print("  dirty:", d["tells_total"], "tells,", d["tells_per_100w"], "per 100w")
    print("  clean:", c["tells_total"], "tells, rhythm stdev", c["rhythm"]["stdev_words"])


def main():
    args = sys.argv[1:]
    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return 0
    if "--self-test" in args:
        self_test()
        return 0

    mode = "--strip" if "--strip" in args else "--check"
    src = args[-1]
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()

    if mode == "--strip":
        sys.stdout.write(strip(raw))
        return 0

    report = check(raw)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["tells_total"] else 0


if __name__ == "__main__":
    sys.exit(main())
