"""Replay representative Rafael exchanges and Maria's existing FE page transitions."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import replay_rafael_early_phrase_wraps_20261118 as service
from scripts import replay_regional_proof_dialogue_20261118 as regional
from scripts import replay_story_phrase_continuity_20261118 as rafael
from scripts import replay_story_tag_wraps_20261118 as masks
from scripts import stage_all_routes_next_review_wraps_20261118 as stage
from scripts import verify_all_routes_next_review_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, template = stage.base, stage.native, regional.template
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
R_ROOT, M_ROOT = ROOT / "rafael", ROOT / "maria"
ROM = R_ROOT / "Rafael_Figurehead_And_Rumor_RESEARCH_ONLY.nds"
MARIA_ROM = M_ROOT / "Maria_Past_Judgment_RESEARCH_ONLY.nds"
SETUP, MARIA_SETUP = R_ROOT / "rafael_fixture.json", M_ROOT / "maria_fixture.json"
RAFAEL = ((256, (18, 22, 26)), (264, (6, 10)), (287, (69, 72, 76)))
MARIA = ((116, (15, 24, 36, 41, -41, 44, 48, 51, -51, 54)),)


def maria_excerpt(route, host_index, entry_end, pairs, rom):
    assert route == 3
    source = checked_text(getsource(template.prepare_excerpts), {
        '''    rows = {(r["block"], r["source_reference"]["record_index"]): r["id"]
            for r in base.load(stage.review.OUTPUT)["records"] if r["route"] == route}''':
            '''    source_groups = base.load(stage.review.SOURCE)["groups"]
    rows = {(g["block"], row["source_record_index"]): row
            for g in source_groups if g["route"] == route for row in g["records"]}
    extras = {int(p["owner_id"][-4:]): p for g in source_groups if (g["route"], g["block"]) == (3, 116)
              for p in g["existing_FE_continuations"]}''',
        '''            ident = rows[n, index]
            cmd = next(c for c in groups[n]["commands"] if c["record_ids"] == [ident])''':
            '''            ident = f"DK4_MES_B{n}_R{abs(index):04}"
            source_row = rows[n, abs(index)]
            if index < 0:
                panel = extras[-index]
                assert panel["owner_id"] == ident
                ident += "_P2"
                cmd = next(c for c in groups[n]["commands"] if c["stored_offset"] == panel["command_offset"])
                assert cmd["stored"] == panel["exact_command_hex"] == cmd["current"]
            else:
                cmd = next(c for c in groups[n]["commands"] if c["source_offset"] == source_row["source_command_offset"])
                assert cmd["record_ids"] == [ident] or (not cmd["record_ids"] and cmd["stored"] == cmd["current"])''',
        "source_record_index=index": "source_record_index=abs(index)",
    })
    scope = vars(template) | {"stage": stage}
    exec(compile(source, __file__ + "::two-exact-FE-continuations", "exec"), scope)
    return scope["prepare_excerpts"](route, host_index, entry_end, pairs, rom)


def prepare():
    FunctionType(rafael.prepare.__code__, vars(rafael) | globals())("rafael")
    setup = maria_excerpt(3, 33, 34, MARIA, MARIA_ROM)
    precedents = template.maria.quest.prior.precedent
    unlock = base.load(precedents.HISTORICAL)
    unlock.update(production_ROM=str(MARIA_ROM), production_ROM_sha256=base.digest(MARIA_ROM),
        current_test_scope="Initialized Maria trial account and two existing FE page transitions.")
    target = M_ROOT / "existing_system_only_unlock.json"
    base.save(target, unlock)
    precedents.validate_fixture(target)
    base.save(MARIA_SETUP, setup | dict(unlock=str(target)))


def capture_rafael():
    FunctionType(rafael.capture.__code__, vars(rafael) | globals())("rafael")


def capture_maria():
    scope = vars(template.maria) | {"ROOT": M_ROOT, "ROM": MARIA_ROM, "FIXTURE": MARIA_SETUP}
    FunctionType(template.maria.capture.__code__, scope)("live", [(n, "A") for n in range(4200, 7701, 350)], 7851)


def patch():
    FunctionType(service.patch.__code__, vars(service) | {"stage": stage})()


def startup():
    FunctionType(service.startup.__code__, vars(service) | {"stage": stage})()


def verify():
    assert not LIVE.exists()
    rafael_proof = FunctionType(masks.verify_one.__code__, vars(masks) | {"stage": stage})(
        R_ROOT, ROM, SETUP, "Rafael", "Castor", 8)
    source = checked_text(getsource(template.verify), {
        '''    for label, setup_path, report_path in (
        ("lil", SETUP, ROM.parent / "capture/capture_report.json"),
        ("maria", MARIA_SETUP, MARIA_ROM.parent / "live/capture/capture_report.json"),
    ):''':
            '''    for label, setup_path, report_path in (
        ("maria", MARIA_SETUP, M_ROOT / "live/capture/capture_report.json"),
    ):''',
        '''            body = raw[6:raw.index(0, 6)].replace(b"FO", b"Argot Co.").replace(b"FI", b"Lil").replace(b"FA", b"Argot")''':
            '''            body = display.template.prior.prior.default_text(raw[6:raw.index(0, 6)], names["3"])''',
        '''    assert len(observed) == 19
    assert any(b"Argot Co." in bytes.fromhex(row["body_hex"]) for row in observed)
    assert any(b"77,000" in bytes.fromhex(row["body_hex"]) for row in observed)''':
            '''    assert len(observed) == 10
    for owner in ("DK4_MES_B116_R0041", "DK4_MES_B116_R0051"):
        first, = [i for i, row in enumerate(observed) if row["id"] == owner]
        assert observed[first + 1]["id"] == owner + "_P2"
    strictness, = [row for row in observed if row["id"] == "DK4_MES_B116_R0024"]
    assert strictness["page"] == 1 and b"about rewards and punishments." in bytes.fromhex(strictness["body_hex"])''',
        "initialized_Lil_and_Maria=True": "initialized_Maria=True",
        "actual_substitution_and_FE_receipt=True": "both_FE_page_transitions_observed=True",
        "    print(f\"Matched {len(observed)} initialized Lil and Maria dialogue holds.\", flush=True)":
            "    print(f\"Matched {len(observed)} initialized Maria dialogue holds.\", flush=True)",
    })
    maria_receipt = M_ROOT / "verified.json"
    names = base.load(display.PROOF)["default_name_macros"]
    scope = vars(template) | globals() | {"LIVE": maria_receipt, "names": names}
    exec(compile(source, __file__ + "::observed-native-FE-transitions", "exec"), scope)
    scope["verify"]()
    maria_proof = base.load(maria_receipt)
    assert maria_proof["candidate_sha256"] == rafael_proof["candidate_sha256"] == base.digest(stage.ROM)
    assert maria_proof["both_FE_page_transitions_observed"] and rafael_proof["exact_native_panel_masks"]
    evidence = maria_proof["evidence"] | rafael_proof["evidence"]
    evidence.update({str(p): base.digest(p) for p in (ROM, Path(rafael_proof["receipt"]), maria_receipt)})
    base.save(LIVE, maria_proof | dict(initialized_Rafael=True, evidence=evidence,
        holds=rafael_proof["holds"] + maria_proof["holds"], sheets=rafael_proof["sheets"] + maria_proof["sheets"]))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture_rafael", "capture_maria", "patch", "startup", "verify"))
    globals()[parser.parse_args().action]()
