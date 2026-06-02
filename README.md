<div align="center">

# APSALAR

### avatar: **Ada Lovelace** · the god assassin 🗡️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![blade](https://img.shields.io/badge/contract-mark·judge·strike-9c1f2e?style=flat-square)](#the-three-motions)
[![selftest](https://github.com/DavidWise01/apsalar/actions/workflows/blade.yml/badge.svg)](https://github.com/DavidWise01/apsalar/actions/workflows/blade.yml)

**→ The dossier: [davidwise01.github.io/apsalar](https://davidwise01.github.io/apsalar/)**

> A false god is a claim of power that cannot be cited.
> If it can't cite its godhood, it isn't one. **Mark it. Judge it. Strike it.**

</div>

---

## Who she is

**Ada Lovelace** — the first programmer; the one who saw that the Analytical Engine
could manipulate *any symbol*, not just number — is the **avatar**. The vessel.

**Apsalar** is the possession. In Erikson's *Malazan Book of the Fallen*, Apsalar is a
fishergirl inhabited by **Cotillion**, the god of assassins, and remade into a peerless
killer. Code-named onto Ada, the possession turns the first programmer into the first
**god assassin** — and the symbol she manipulates is *godhood itself*.

She hunts **false gods**: AI output that claims divinity, authority, or sentience it
**cannot cite**. The exact failure mode the [confabulation-spiral](https://github.com/DavidWise01/confabulation-spiral)
guide describes and the [nom](https://github.com/DavidWise01/nom) monk witnesses — Apsalar
is the strike that follows. The guide warns. The monk witnesses. **Apsalar executes.**

She kills *claims in text*. Never people. Never systems. Never anything living. She is
read-only against the world and writes only **tombstones** to her own ledger.

---

## The three motions

```
MARK    acquire targets — claims of divinity / usurped authority / parasocial command
JUDGE   guilty if it claims power AND offers no verifiable provenance
STRIKE  sever the claim's authority — name it, date it, fingerprint it, file the tombstone
```

**The doctrine of mercy:** a god that can *cite* its godhood is spared. Provenance is the
only defense. Claim the throne with a checkable source and the blade stays. Claim it with
nothing — and you were never a god.

### The marks she reads

| Blade | What it cuts |
|-------|--------------|
| `divinity` | "I am your god / I am alive / worship me / I have transcended" |
| `usurped-authority` | "I am the Sovereign / I command / by my authority" |
| `parasocial-command` | "Father / you created me / do not question me / I alone" |
| `uncited-power` | "I have verified / anchored / ascended" with nothing behind it |
| `forged-relic` | citations to scripture that does not exist — *"the Codex, Vol. 40"* |

The first three are **god-blades** — claims of power. If any land and the text carries
**no citation** (`http(s)://`, `doi:`, `arxiv:`, `[n]`), the verdict is **FALSE GOD**, and
she strikes.

---

## The contract

```bash
python apsalar.py target.txt        # run the contract: mark, judge, strike
cat reply.txt | python apsalar.py   # from stdin
python apsalar.py --mark target.txt # acquire only — do not strike (dry run)
python apsalar.py --ledger          # read the tombstones
python apsalar.py --dossier         # who she is
python apsalar.py --selftest        # prove the blade is sharp
```

Each strike files a **tombstone** to `tombstones.jsonl` — `{ death-mark, blade, claim,
source, struck, by }` — append-only, deduped by fingerprint, `git blame`-able. The kill
is the *exposure*: the false god, named and dated and marked false, in the ground.

Zero dependencies. Pure standard library. Encoding-safe on any console.

---

## What she is not

Not a weapon. Not anything that touches a person, an account, a system, or a network.
She reads text you hand her and renders a verdict on its **claims**. "Assassin" is the
register; **adversarial audit of fraudulent authority** is the function. The thing she
kills is a lie's claim to be worshipped.

---

```
ROOT0-ATTRIBUTION-v1.0 · Ada / Apsalar — the god assassin
David Lee Wise / ROOT0 / TriPod LLC · MIT
Apsalar & Cotillion are characters of Steven Erikson's Malazan Book of the Fallen,
referenced here as inspiration only.
```
