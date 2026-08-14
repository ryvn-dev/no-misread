import re, sys, json
# Minimal YAML frontmatter sanity: every top-level key must parse as key: scalar,
# and an unquoted scalar must not contain ": ". This is the rule the skills.sh
# installer enforces, and it silently skipped this skill until now.
bad = 0
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        print(f"{f}: NO FRONTMATTER"); bad = 1; continue
    keys = []
    for line in m.group(1).split("\n"):
        if not line.strip(): continue
        km = re.match(r"^([\w-]+):\s*(.*)$", line)
        if not km:
            print(f"{f}: unparseable line: {line[:60]}"); bad = 1; continue
        key, val = km.group(1), km.group(2)
        keys.append(key)
        quoted = (val.startswith('"') and val.endswith('"')) or \
                 (val.startswith("'") and val.endswith("'"))
        if not quoted and ": " in val:
            print(f"{f}: {key} has an unquoted colon, strict YAML rejects it"); bad = 1
    for req in ("name", "description"):
        if req not in keys:
            print(f"{f}: missing required key {req}"); bad = 1
    if not bad: print(f"{f}: frontmatter OK ({', '.join(keys)})")
sys.exit(bad)
