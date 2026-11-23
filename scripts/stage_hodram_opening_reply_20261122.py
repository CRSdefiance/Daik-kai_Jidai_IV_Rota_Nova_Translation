"""Compile the source-paired Hodram reply, reward, and Hanseatic report."""

from argparse import ArgumentParser
from inspect import getsource
from json import dumps
from pathlib import Path
from types import FunctionType, SimpleNamespace
import sys

from scripts import stage_hodram_opening_20261122 as opening
from scripts import pair_hodram_opening_20261122 as paired
from scripts import register_story_literal_names_20261122 as parent
from scripts import replay_story_literal_names_20261122 as baseline
from scripts import stage_rafael_deck_tutorial_followup_20261122 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
PATH, BLOCK = paired.ARCHIVE, 42
ROOT = Path("work/analysis/hodram_opening_reply_20261122")
ROM, PROOF = ROOT/"Hodram_Opening_Reply_STAGED.nds", ROOT/"stored_proof.json"
PATCH, REBUILT = ROOT/"translation.xdelta", ROOT/"clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT/"startup/capture/capture_report.json"
REPORT = ROOT/"ordinary/capture/capture_report.json"
DRAFT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/hodram_opening_reply_wraps_20261122_v1.json")
CHANGED = {f"DK4_MES_B42_R{i:04d}" for i in (116,120,135)}
PIVOT = "DK4_MES_B42_R0116"
FRAMES = (24320,24670,25020,25370,25720,26070,26420,26770,27120)


def plan_progressive(row, selector, current, original):
    if row["id"] != PIVOT:
        body, plan = opening.plan_progressive(row,selector,current,original)
        assert dumps(row["initial_layout_plan"],sort_keys=True) == dumps(plan,sort_keys=True)
        return body, plan
    # In this one reply, "Anyway..." closes the page as a deliberate change of subject.
    original_planner = opening.layout.prior.layout
    planner_source = checked_text(getsource(original_planner.plan), {
        "profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30":
            "profile.macro_ascii_lengths['FA']==9 and profile.macro_widths['FA']==54",
        "tiny=int(final and start>0 and (stop-start==1 or length<=8))":
            'tiny=int(final and start>0 and (stop-start==1 or length<=8) and text!="Anyway...")',
    })
    settings = SimpleNamespace(**(vars(original_planner) | {"get_dialogue_profile": opening.route_profile}))
    bound = opening.layout.bind_planner
    planner = FunctionType(bound.__code__,bound.__globals__ | {
        "getsource": lambda _:planner_source, "prior": SimpleNamespace(layout=settings)})()
    compile_body = opening.plan_progressive
    plan = FunctionType(compile_body.__code__,compile_body.__globals__ | {"PLANNER": planner})
    requested = row["proposed_visual_lines"]
    encoded, result = plan(row | {"protected_phrases": requested},selector,current,original)
    assert result["lines"] == requested and row["english"] == row["previous_English"]
    return encoded,result


def stage():
    assert not ROOT.exists()
    draft, previous = map(base.load,(DRAFT,parent.RELEASE))
    assert previous["candidate_sha256"] == draft["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(parent.MANIFEST) == previous["manifest_sha256"]
    packet = paired.source_and_current(parent,(BLOCK,))
    source_group, = packet["groups"]
    refs = {row["id"]:row for row in source_group["records"]}
    records = draft["records"]
    assert len(records) == 15 and {r["id"] for r in records if r["decision"] == "revision"} == CHANGED
    for row in records:
        assert all(row[k] == v for k,v in refs[row["id"]].items())
        assert row["native_command_word"] == 0x4000
        assert row["review"]["formatting"] == (row["decision"] == "retention")
        assert all(v for k,v in row["review"].items() if k != "formatting")
        prefix = f'{row["selector"]:02x}'
        row.update(kind="progressive",route=1,source_selector=row["selector"],
            source_hex=prefix+row["source_reference"]["exact_body_hex"],
            current_hex=prefix+row["current_reference"]["exact_body_hex"])

    clean, target = map(base.NdsImage.open,(native.CLEAN,parent.ROM))
    original_files = native.files(target)
    arm = original_files[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    original_archive = original_files[PATH]
    source = native.IlnkContainer.parse(clean.read_file(PATH)).blocks[BLOCK]
    bank = native.IlnkContainer.parse(original_archive)
    current = bank.blocks[BLOCK]
    compiler = opening.compiler
    scope = compiler.env | {"plan_progressive": plan_progressive}
    source_rebuilder = checked_text(getsource(compiler.rebuild_function),{
        '"plan_progressive": workflow.plan_progressive': '"plan_progressive": plan_progressive',
    })
    exec(compile(source_rebuilder,__file__+"::story-compiler","exec"),scope)
    inventory, _, _ = native.scoped_inventory()
    revised,commands,plans = scope["rebuild_function"]()(records,source,current,inventory,clean.read_file(native.ARM),arm,None)
    assert revised != current and plans.keys() == CHANGED
    assert native.digest(source) == source_group["source_block_sha256"]
    assert native.digest(current) == source_group["current_block_sha256"]
    bank.blocks[BLOCK] = revised
    target.replace_file(PATH,bank.to_bytes())
    bank.blocks[BLOCK] = current
    assert bank.to_bytes() == original_archive
    final = native.files(target)
    assert original_files.keys() == final.keys()
    assert {path for path,data in original_files.items() if data != final[path]} == {PATH}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean),final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    result = bytes(target.rom.save())
    target.replace_file(PATH,original_archive)
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM),predecessor_sha256=previous["candidate_sha256"],
        manuscript_sha256=base.digest(DRAFT), clean_sha256=base.digest(native.CLEAN),records=records,
        path=PATH,block=BLOCK,clean_block_sha256=native.digest(source),before_block_sha256=native.digest(current),
        after_block_sha256=native.digest(revised),archive_sha256=native.digest(final[PATH]),
        unchanged_ARM9_sha256=native.digest(arm),commands=commands,plans=plans,source25=guard,
        whole_parent_inverse=True, changed_blocks={PATH:[BLOCK]}))
    print(f"Staged {base.digest(ROM)}. Rebuilt three original dialogue commands and their exact branch targets.",flush=True)


def replay():
    proof, previous, controls = map(base.load,(PROOF,parent.RELEASE,baseline.stage.parent.stage.BASELINE))
    assert proof["predecessor_sha256"] == previous["candidate_sha256"]
    assert base.digest(ROM) == proof["candidate_sha256"]
    assert controls["cold_boot"] and not controls["savestate_loaded"] and not controls.get("battery_save_preloaded")
    assert not controls["callback_errors"] and not any(v for k,v in controls.items() if k.startswith("synthetic_"))
    root = REPORT.parent.parent
    root.mkdir()
    inputs = root/"inputs.json"
    end = FRAMES[-1]+1
    base.save(inputs,[e for e in controls["scripted_input_schedule"] if e["start"]<end])
    harness = baseline.original.harness
    argv = sys.argv
    try:
        sys.argv = [harness.__file__,"--rom",str(ROM),"--out",str(REPORT.parent),"--frames",str(end),
            "--inputs-json",str(inputs),"--press-start","-1","--touchscreen","--capture-every","999999",
            "--capture-at",*map(str,FRAMES)]
        harness.main()
    finally:
        sys.argv = argv


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("stage","patch","startup","replay"))
    action = cli.parse_args().action
    if action in ("stage","replay"):
        globals()[action]()
    else:
        inherited = getattr(precedent,action)
        FunctionType(inherited.__code__,inherited.__globals__ | globals())()
