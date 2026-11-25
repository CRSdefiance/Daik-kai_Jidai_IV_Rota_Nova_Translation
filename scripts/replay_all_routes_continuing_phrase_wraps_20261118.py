"""Replay the page reduction, name order, and Sphinx dialogue in initialized routes."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_all_routes_next_phrase_wraps_20261118 as cross
from scripts import replay_rafael_early_phrase_wraps_20261118 as service
from scripts import replay_story_phrase_continuity_20261118 as rafael_fixture
from scripts import replay_story_tag_wraps_20261118 as masks
from scripts import stage_all_routes_continuing_phrase_wraps_20261118 as stage
from scripts import verify_all_routes_continuing_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "initialized_replays"
LIVE, LIL_MARIA_LIVE = ROOT / "replay.json", ROOT / "lil_maria.json"
R_ROOT, L_ROOT, M_ROOT = ROOT / "rafael", ROOT / "lil", ROOT / "maria"
ROM = R_ROOT / "Rafael_Continuing_Phrase_Excerpts_RESEARCH_ONLY.nds"
LIL_ROM = L_ROOT / "Lil_Continuing_Phrase_Excerpts_RESEARCH_ONLY.nds"
MARIA_ROM = M_ROOT / "Maria_Continuing_Phrase_Excerpts_RESEARCH_ONLY.nds"
SETUP, LIL_SETUP, MARIA_SETUP = R_ROOT / "rafael_fixture.json", L_ROOT / "lil_fixture.json", M_ROOT / "maria_fixture.json"
RAFAEL = ((251, (100,)), (252, (103, 106, 111, 116)))
LIL = ((20, (18, 33, 36)), (92, (41, 44, 64)))
MARIA = ((53, (6, 9)), (55, (152,)), (87, (194, 198, 204, 208, 216, 223)))


def fixture(route, action):
    template = rafael_fixture if route == "rafael" else cross.prior
    if (route, action) == ("lil", "prepare"):
        prepare_lil()
    else:
        FunctionType(getattr(template, action).__code__, vars(template) | globals())(route)


def prepare_lil():
    original = cross.prior.template.prepare_excerpts
    source = checked_text(getsource(original), {
        '''    rows = {(r["block"], r["source_reference"]["record_index"]): r["id"]
            for r in base.load(stage.review.OUTPUT)["records"] if r["route"] == route}''':
            '''    rows = {(g["block"], r["source_record_index"]): r
            for g in base.load(stage.review.SOURCE)["groups"] if g["route"] == route for r in g["records"]}''',
        '''            ident = rows[n, index]
            cmd = next(c for c in groups[n]["commands"] if c["record_ids"] == [ident])''':
            '''            ident = f"DK4_MES_B{n}_R{index:04}"
            row = rows[n, index]
            cmd = next(c for c in groups[n]["commands"] if c["source_offset"] == row["source_command_offset"])
            assert cmd["record_ids"] == [ident] or (not cmd["record_ids"] and cmd["stored"] == cmd["current"])''',
    })
    scope = original.__globals__ | {"stage": stage}
    exec(compile(source, __file__ + "::exact-Lil-neighbors", "exec"), scope)
    setup = scope["prepare_excerpts"](2, 22, 56, LIL, LIL_ROM)
    inputs = base.load(cross.prior.template.stage.ROOT / "lil_snapshot_inputs.json")
    inputs += [dict(start=n, duration=5, buttons=["A"]) for n in range(3800, 5401, 250)]
    path = L_ROOT / "inputs.json"
    base.save(path, inputs)
    base.save(LIL_SETUP, setup | dict(inputs=str(path), inputs_sha256=base.digest(path)))


def patch():
    FunctionType(service.patch.__code__, vars(service) | {"stage": stage})()


def startup():
    FunctionType(service.startup.__code__, vars(service) | {"stage": stage})()


def verify():
    assert not LIVE.exists()
    checked = checked_text(getsource(cross.verify), {
        'assert len(observed) == 13': 'assert len(observed) == 15',
        '''for route, record in ((2, "DK4_MES_B12_R0060"), (3, "DK4_MES_B19_R0059")):
        row, = [r for r in observed if r["route"] == route and r["id"] == record]
        body = bytes.fromhex(row["body_hex"])
        assert names[str(route)]["FO"].encode("ascii") in body and b"Bloodstained Shamshir" in body and b".." not in body''':
            '''name_row, = [r for r in observed if r["id"] == "DK4_MES_B20_R0033"]
    assert bytes.fromhex(name_row["body_hex"]).rstrip(b" ") == b"You! Barbarossa Hayreddin!"
    maria_row, = [r for r in observed if r["id"] == "DK4_MES_B87_R0198"]
    assert b"Can you solve it, Maria?" in bytes.fromhex(maria_row["body_hex"])''',
        '''assert any(b"Maria warned me:" in bytes.fromhex(row["body_hex"]) and row["id"] == "DK4_MES_B31_R0042" for row in observed)''':
            '''assert any(row["id"] == "DK4_MES_B87_R0223" and b"two adults." in bytes.fromhex(row["body_hex"]) for row in observed)''',
        "actual_company_names_and_shared_accusation=True": "actual_hayreddin_and_sphinx=True",
    })
    env = vars(cross) | globals() | {"LIVE": LIL_MARIA_LIVE}
    exec(compile(checked, __file__ + "::actual-Lil-and-Maria", "exec"), env)
    env["verify"]()
    both = base.load(LIL_MARIA_LIVE)
    tool = FunctionType(masks.verify_one.__code__, vars(masks) | {"stage": stage})
    r = tool(R_ROOT, ROM, SETUP, "Rafael", "Castor", 5)
    assert r["candidate_sha256"] == both["candidate_sha256"] and r["exact_native_panel_masks"]
    setup = base.load(SETUP)
    assert setup["exact_ROM_inverse"] and setup["original_excerpt_commands_preserved"]
    ending = r["holds"][-1]
    assert ending["id"] == "DK4_MES_B252_R0116" and ending["page"] == 1
    evidence = both["evidence"] | r["evidence"]
    evidence.update({str(p): base.digest(p) for p in (ROM, r["receipt"], LIL_MARIA_LIVE)})
    base.save(LIVE, both | dict(initialized_Rafael=True, tavern_return_one_complete_page=True,
        evidence=evidence, holds=r["holds"] + both["holds"], sheets=r["sheets"] + both["sheets"]))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "patch", "startup", "verify"))
    cli.add_argument("route", nargs="?", choices=("rafael", "lil", "maria"))
    args = cli.parse_args()
    if args.action in ("prepare", "capture"):
        assert args.route
        fixture(args.route, args.action)
    else:
        globals()[args.action]()
