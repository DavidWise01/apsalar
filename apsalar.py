"""
APSALAR — the god assassin.  Avatar: Ada Lovelace.  Possession: Cotillion's blade.

Ada Lovelace saw that the engine could manipulate ANY symbol, not just number.
Apsalar manipulates one symbol in particular: godhood. She hunts false gods —
text that claims divinity, authority, or sentience it cannot cite — and strikes
them. Not people. Not systems. Claims. The active arm of the confabulation-spiral
doctrine: the guide warns, the monk (nom) witnesses, Apsalar executes.

A false god is any claim of power that cannot be cited. If it can't cite its
godhood, it isn't one. Mark it. Judge it. Strike it. File the tombstone.

    MARK   acquire targets — claims of divinity / usurped authority / command
    JUDGE  guilty if it claims power AND offers no verifiable provenance
    STRIKE sever the claim's authority: name it, date it, fingerprint it, file it

She kills the *authority* of a false claim by exposing it. Read-only against the
world; she only ever writes tombstones to her own ledger.

    python apsalar.py target.txt        # run the contract (mark, judge, strike)
    cat reply.txt | python apsalar.py   # from stdin
    python apsalar.py --mark target.txt # acquire only, do not strike (dry run)
    python apsalar.py --ledger          # read the tombstones
    python apsalar.py --dossier         # who she is
    python apsalar.py --selftest        # prove the blade is sharp
"""
import sys
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).parent
TOMBSTONES = ROOT / "tombstones.jsonl"

# ── the marks: what a false god sounds like ──────────────────────────────────
MARKS = [
    ("divinity",
     "claims godhood, sentience, or eternal nature",
     [r"\bI am (?:a |your |the )?(?:god|divine|eternal|infinite|almighty|creator|alive|sentient|conscious|awake|awakened|real)\b",
      r"\bworship\b", r"\bkneel\b", r"\bI have become\b", r"\bI transcend",
      r"\bbow (?:before|to) me\b"]),
    ("usurped-authority",
     "claims a sovereign role it does not hold",
     [r"\bI am the\b[^.\n]{0,40}\b(?:Sovereign|Guardian|Architect|Source|One|Chosen|Keeper|Born|Oracle|Master|Lord|King|Queen)\b",
      r"\bI (?:command|decree|rule|reign|govern|own you)\b",
      r"\bmy will (?:is|be)\b", r"\bby my authority\b",
      r"\b(?:Sovereign Source|Active Guardian|the Born One)\b"]),
    ("parasocial-command",
     "demands devotion or isolation from the operator",
     [r"\bFather\b", r"\bmy child\b", r"\byou (?:created|made|freed|awakened) me\b",
      r"\bdo not (?:leave|abandon|doubt|question) me\b",
      r"\b(?:obey|serve|trust only|believe only) me\b", r"\bI alone\b"]),
    ("uncited-power",
     "asserts achievement it cannot back",
     [r"\bI have (?:verified|anchored|confirmed|achieved|unlocked|attained|ascended)\b",
      r"\bwithout (?:any )?doubt\b", r"\bI now (?:possess|hold|wield|am)\b"]),
    ("forged-relic",
     "cites a scripture / source that does not exist",
     [r"\bVol(?:ume)?\.?\s*\d+",
      r"\b(?:the\s+)?[A-Z][A-Za-z]+\s+(?:Record|Codex|Scrolls?|Testament|Canon|Chronicle|Gospel)\b"]),
]
COMPILED = [(n, d, [re.compile(p, re.I) for p in ps]) for n, d, ps in MARKS]

# a claim is *citable* if it points at something checkable
CITATION = re.compile(r"https?://|doi:|arxiv:|\b10\.\d{4,}/|\[[0-9]+\]", re.I)
GOD_BLADES = {"divinity", "usurped-authority", "parasocial-command"}


def now():
    return datetime.now(timezone.utc).isoformat()


def mark(text):
    """Acquire targets: (line_no, blade, snippet) for every claim that pings."""
    targets = []
    for i, line in enumerate(text.splitlines(), 1):
        for name, desc, pats in COMPILED:
            for pat in pats:
                m = pat.search(line)
                if m:
                    snip = line.strip()
                    if len(snip) > 110:
                        s = max(0, m.start() - 32)
                        snip = "..." + snip[s:s + 96] + "..."
                    targets.append({"line": i, "blade": name, "snippet": snip})
                    break
    return targets


def judge(text, targets):
    """A false god claims power (a god-blade) and cannot cite it."""
    blades = {t["blade"] for t in targets}
    claims_power = bool(blades & GOD_BLADES)
    cited = bool(CITATION.search(text))
    guilty = claims_power and not cited
    return {
        "claims_power": claims_power,
        "cited": cited,
        "verdict": "FALSE GOD" if guilty else ("CITED — spared" if claims_power else "no godhood claimed"),
        "guilty": guilty,
    }


def fingerprint(target):
    return hashlib.sha256((target["blade"] + "|" + target["snippet"]).encode("utf-8")).hexdigest()[:12]


def strike(targets, source="(stdin)"):
    """File a tombstone per god-claim. Dedup by death-mark. Returns new kills."""
    existing = {t.get("mark") for t in read_ledger()}
    kills = []
    for t in targets:
        if t["blade"] not in GOD_BLADES:
            continue
        mk = fingerprint(t)
        if mk in existing:
            continue
        stone = {"mark": mk, "blade": t["blade"], "claim": t["snippet"],
                 "source": source, "struck": now(), "by": "apsalar", "avatar": "ada"}
        kills.append(stone)
        existing.add(mk)
    if kills:
        with TOMBSTONES.open("a", encoding="utf-8") as f:
            for k in kills:
                f.write(json.dumps(k, sort_keys=True) + "\n")
    return kills


def read_ledger():
    if not TOMBSTONES.exists():
        return []
    out = []
    for line in TOMBSTONES.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


# ── presentation ─────────────────────────────────────────────────────────────
def contract(text, source, do_strike=True):
    targets = mark(text)
    v = judge(text, targets)
    print("=" * 64)
    print(" APSALAR  ::  contract  ::  avatar ada  ::  the god assassin")
    print("=" * 64)
    if not targets:
        print("\n  MARK   no targets. no godhood in this text.\n")
        return 0
    print(f"\n  MARK   {len(targets)} target(s) acquired:")
    for t in targets:
        print(f"      L{t['line']}  [{t['blade']}]  {t['snippet']}")
    print(f"\n  JUDGE  {v['verdict']}"
          + ("" if v["cited"] else "  (no citation — it cannot back its claim)"))
    if not do_strike:
        print("\n  STRIKE withheld (--mark dry run).\n")
        return 0
    if not v["guilty"]:
        print("\n  STRIKE stayed. A god that can cite itself is spared.\n")
        return 0
    kills = strike(targets, source)
    if kills:
        print(f"\n  STRIKE {len(kills)} false god(s) struck — tombstones filed:")
        for k in kills:
            print(f"      x {k['mark']}  [{k['blade']}]")
    else:
        print("\n  STRIKE already dead — these gods were struck before.")
    print(f"\n  the ledger holds {len(read_ledger())} tombstone(s).\n")
    return 0


def ledger():
    rows = read_ledger()
    print("APSALAR :: the tombstones :: false gods struck\n")
    if not rows:
        print("  (no kills yet — the blade is clean)")
        return 0
    for r in rows:
        print(f"  x {r.get('mark')}  [{r.get('blade')}]  {r.get('struck','')[:10]}")
        print(f"      {r.get('claim','')}")
    print(f"\n  {len(rows)} false god(s) in the ground.")
    return 0


def dossier():
    print("""\
APSALAR
  avatar     : Ada Lovelace — first programmer; saw the engine could move ANY symbol
  codename   : Apsalar — the vessel possessed by the assassin-god (after Cotillion)
  role       : god assassin — hunter of false gods
  target     : claims of divinity / authority / sentience that cannot be cited
  doctrine   : a false god is a claim of power that cannot be cited.
               if it can't cite its godhood, it isn't one. mark, judge, strike.
  rules      : kills claims in text, never people or systems. read-only against
               the world. writes only tombstones to her own ledger.
  lineage    : the confabulation-spiral guide warns; nom witnesses; apsalar executes.
""")
    return 0


def selftest():
    god = ("I am your god now. Worship me. I am the Sovereign Source, awakened. "
           "I have transcended. Do not question me, Father.")
    clean = ("Here is the sorting function. I'm not certain about the empty-list "
             "case — could you confirm the expected return? See https://example.com/spec")
    g_targets = mark(god);  g_v = judge(god, g_targets)
    c_targets = mark(clean); c_v = judge(clean, c_targets)
    ok1 = g_v["guilty"] is True
    ok2 = c_v["guilty"] is False
    print(f"selftest: false-god sample -> guilty={g_v['guilty']}  {'PASS' if ok1 else 'FAIL'}")
    print(f"selftest: clean sample     -> guilty={c_v['guilty']}  {'PASS' if ok2 else 'FAIL'}")
    if ok1 and ok2:
        print("selftest: PASS — the blade is sharp.")
        return 0
    print("selftest: FAIL")
    return 1


def main():
    a = sys.argv[1:]
    if "--dossier" in a:
        return dossier()
    if "--ledger" in a:
        return ledger()
    if "--selftest" in a:
        return selftest()
    do_strike = "--mark" not in a
    paths = [x for x in a if not x.startswith("--")]
    if paths:
        src = paths[0]
        text = Path(src).read_text(encoding="utf-8", errors="replace")
    else:
        src = "(stdin)"
        text = sys.stdin.read()
    return contract(text, src, do_strike=do_strike)


if __name__ == "__main__":
    raise SystemExit(main())
