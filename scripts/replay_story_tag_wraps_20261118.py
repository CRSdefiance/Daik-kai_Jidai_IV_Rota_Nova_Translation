"""Replay exact question-tag and name excerpts in initialized Rafael and Lil games."""

from argparse import ArgumentParser
from inspect import getsource
import sys
from types import FunctionType

from scripts import replay_late_trade_exchanges_20261118 as lil_template
from scripts import replay_london_guild_assignments_20261118 as replay
from scripts import stage_story_tag_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
R_ROOT = ROOT / "rafael"
L_ROOT = ROOT / "lil"
ROM = R_ROOT / "Rafael_Question_Tag_Excerpts_RESEARCH_ONLY.nds"
LIL_ROM = L_ROOT / "Lil_Question_Tag_Excerpts_RESEARCH_ONLY.nds"
SETUP, LIL_SETUP = R_ROOT / "rafael_fixture.json", L_ROOT / "lil_fixture.json"
EXCERPTS = ((49, (271, 275, 279)), (70, (218, 223, 227)), (82, (5, 8)), (84, (417,)))
LIL_EXCERPTS = ((26, (175,)), (66, (105,)), (129, (36,)), (215, (15,)))


def prepare_rafael():
    packet = base.load(stage.review.SOURCE)
    proof = base.load(stage.PROOF)
    candidate = base.NdsImage.open(stage.ROM)
    sc0 = native.IlnkContainer.parse(candidate.read_file("/data/SC0.DK4"))
    groups = {g["block"]: g for g in packet["groups"] if g["route"] == 0}
    rows = {}
    for n, indices in EXCERPTS:
        for row in groups[n]["records"]:
            if row["source_record_index"] in indices:
                rows[n, row["source_record_index"]] = row

    source = checked_text(getsource(replay.prepare), {
        '    draft = base.load(stage.review.OUTPUT)\n'
        '    rows = {(r["block"], r["source_reference"]["record_index"]): r for r in draft["records"] if r["route"] == 0}\n': "",
        'row["id"]': 'record_id',
        '            cmd = next(c for c in group["commands"] if c["record_ids"] == [row["id"]])':
            '            record_id = f"DK4_MES_B{n}_R{ident:04}"\n'
            '            cmd = next(c for c in group["commands"] if c["source_offset"] == row["source_command_offset"])\n'
            '            assert cmd["record_ids"] == [record_id] or (not cmd["record_ids"] and cmd["stored"] == cmd["current"])',
        "range(3800, 8101, 250)": "range(3800, 6410, 275)",
    })
    assert proof["predecessor_sha256"] == packet["candidate_sha256"]
    assert all(native.digest(sc0.blocks[n]) == g["after"] for g in proof["groups"]
               if (n := g["block"]) in groups and g["route"] == 0)
    scope = vars(replay) | globals() | {"ROOT": R_ROOT, "rows": rows}
    exec(compile(source, __file__ + "::exact-Rafael-excerpts", "exec"), scope)
    scope["prepare"]()


def prepare_lil():
    clone = FunctionType(lil_template.prepare_excerpts.__code__, vars(lil_template) | {"stage": stage})
    data = clone(2, 22, 56, LIL_EXCERPTS, LIL_ROM)
    earlier_inputs = stage.parent.stage.ROOT / "lil_snapshot_inputs.json"
    actions = base.load(earlier_inputs) + [dict(start=n, duration=5, buttons=["A"]) for n in range(3800, 5350, 275)]
    path = L_ROOT / "inputs.json"
    base.save(path, actions)
    base.save(LIL_SETUP, data | dict(inputs=str(path), inputs_sha256=base.digest(path)))


def capture_lil():
    setup = base.load(LIL_SETUP)
    assert setup["fixture_sha256"] == base.digest(LIL_ROM)
    assert setup["inputs_sha256"] == base.digest(setup["inputs"])
    sys.argv = [sys.argv[0], "--rom", str(LIL_ROM), "--out", str(L_ROOT / "capture"), "--frames", "5501",
                "--inputs-json", setup["inputs"], "--capture-every", "999999",
                "--capture-at", *map(str, range(3650, 5501, 25))]
    lil_template.harness.main()


def verify_one(root, fixture, setup, name, surname, count):
    changes = {
        'b"Rafael"': repr(name.encode("ascii")),
        'b"Castor"': repr(surname.encode("ascii")),
        'initialized_Rafael=True': f"initialized_{name}=True",
        'actual_Castor_and_Rafael_macro_glyphs=True': "exact_native_panel_masks=True",
        'f"live_{first // 8 + 1}.png"': f'f"{name.lower()}_live_{{first // 8 + 1}}.png"',
        "including both captain name substitutions.": f"in the initialized {name} route.",
    }
    source = checked_text(getsource(replay.verify), changes)
    receipt = root / "verified.json"
    scope = vars(replay) | {"ROOT": root, "ROM": fixture, "SETUP": setup, "LIVE": receipt, "stage": stage}
    exec(compile(source, __file__ + "::complete-native-panel-masks", "exec"), scope)
    scope["verify"]()
    report = base.load(receipt)
    assert len(report["holds"]) == count and report["exact_native_panel_masks"]
    return report | {"receipt": str(receipt)}


def verify():
    assert not LIVE.exists()
    r = verify_one(R_ROOT, ROM, SETUP, "Rafael", "Castor", 9)
    l = verify_one(L_ROOT, LIL_ROM, LIL_SETUP, "Lil", "Argot", 4)
    expected = ("Lil Argot?", "Admiral Argot?")
    assert all(any(value.encode("ascii") in bytes.fromhex(hold["body_hex"]) for hold in l["holds"]) for value in expected)
    assert all(a["candidate_sha256"] == base.digest(stage.ROM) for a in (r, l))
    evidence = r["evidence"] | l["evidence"]
    evidence.update({str(p): base.digest(p) for p in (ROM, LIL_ROM, r["receipt"], l["receipt"])})
    base.save(LIVE, dict(candidate_sha256=r["candidate_sha256"], initialized_Rafael_and_Lil=True,
        exact_original_commands=True, actual_given_name_and_surname=True, natural_activation=False, hardware=False,
        holds=r["holds"] + l["holds"], sheets=r["sheets"] + l["sheets"], evidence=evidence))


capture_rafael = FunctionType(replay.capture.__code__, vars(replay) | globals() | {"ROOT": R_ROOT, "LAST": 6701})

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare_rafael", "prepare_lil", "capture_rafael", "capture_lil", "verify"))
    globals()[parser.parse_args().action]()
