"""Compile the reviewed Deck lesson as a source-bound block, with a whole-ROM inverse."""

from types import FunctionType

from scripts import review_rafael_deck_tutorial_followup_20261122 as draft
from scripts import stage_forest_expeditions_20261118 as stage
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter
from scripts import stage_london_guild_assignments_20261118 as paragraphs


base,native = draft.base,draft.native
current = draft.current
PROOF = draft.ROOT / "stored_preflight_v2.json"
TARGET = draft.ROOT / "compiled_SC0_B43_v2.bin"
REVIEW = draft.ROOT / "contextual_review_v2.json"
PHRASES = {7:("show you","aboard ship"),14:("Deck View",),17:("First up is the captain.","That's you, FI.","A ship needs a captain to sail.","It can't set a course on its own."),
           20:("Sail Handler","They angle the sails for the wind.","You'll need one for each mast."),30:("First Mate","at sea"),
           45:("Deck View","from the menu","your crew's assignments")}


def plan_fe(row,painter):
    for _,lines,data in stage.system.candidate_rows(row["english"],row["protected_phrases"]):
        try:
            plane = painter(data[1:])
            stage.system.check_FE_rows(data[1:],plane)
        except AssertionError:
            continue
        assert data[0]==254
        assert all(any(phrase in line for line in lines) for phrase in row["protected_phrases"])
        return data[1:],dict(lines=lines,expected_native_pages=1,encoded_hex=data.hex())
    raise AssertionError(f"No native system layout passed for {row['id']}")


def main():
    assert not any(path.exists() for path in (PROOF,TARGET,REVIEW))
    packet,release = map(base.load,(draft.OUTPUT,current.RELEASE))
    candidate = base.digest(current.ROM)
    assert candidate == packet["previous_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]==packet["previous_registry_sha256"]
    assert base.digest(current.native.CLEAN)==release["clean_input_sha256"]
    source,rom = map(base.NdsImage.open,(current.native.CLEAN,current.ROM))
    before = native.files(rom)
    clean_arm = source.read_file(native.ARM)
    assert native.digest(before[native.ARM])==release["target_ARM9_sha256"]
    ctx = native.RegisteredRuntime(current.RELEASE,release["own_registered_startup"],captain=3)
    painter = current_fe_painter(ctx)
    archive = native.IlnkContainer.parse(before[draft.FILE])
    jarchive = native.IlnkContainer.parse(source.read_file(draft.FILE))
    jblock,eblock = jarchive.blocks[draft.BLOCK],archive.blocks[draft.BLOCK]
    rows = [r | dict(protected_phrases=PHRASES.get(r["source_reference"]["record_index"],()))
            for r in packet["records"]]
    refinements = {
        17: ("First up is the captain. That's you, FI. A ship needs a captain to sail. It can't set a course on its own.",
             "Julio identifies Rafael directly, then repeats why the ship needs a captain. Keep the two reasons and the light joke. The four complete sentences fit all tested given-name widths."),
        20: ("Next is the Sail Handler. They angle the sails for the wind. You'll need one for each mast.",
             "Keep the job name, the angle of the sails relative to the wind and the per-mast staffing rule. Each of Julio's instructions can finish in the same row."),
    }
    for row in rows:
        number = row["source_reference"]["record_index"]
        if number in refinements:
            english,note = refinements[number]
            row.update(english=english,localization_note=note,earlier_native_visual_refinement=True)
        row.pop("draft_auto_layout")
    assert len(rows)==12
    assert all(r["source_reference"]["block_sha256"]==native.digest(jblock) and
               r["current_reference"]["block_sha256"]==native.digest(eblock) for r in rows)
    inventory,_,_ = native.scoped_inventory()
    env = vars(stage) | {"plan_progressive":paragraphs.plan_progressive,"plan_fe":plan_fe}
    env["changed_speech"] = FunctionType(stage.changed_speech.__code__,env)
    rebuild = FunctionType(stage.rebuild.__code__,env)
    target,commands,plans = rebuild(rows,jblock,eblock,inventory,clean_arm,ctx.arm,painter)
    installed = [r for r in rows if r["decision"]=="revision"]
    assert set(plans)=={r["id"] for r in installed} and len(installed)==6
    assert all(plan["expected_native_pages"]==1 for plan in plans.values())
    assert target != eblock
    for cmd in commands:
        source_hex,current_hex,new_hex = (cmd[k] for k in ("source","current","stored"))
        if cmd["record_ids"]:
            assert source_hex[:12]==current_hex[:12]==new_hex[:12]
        else:
            assert cmd["word"] not in stage.RELATIVE and current_hex==new_hex

    archive.blocks[draft.BLOCK] = target
    packed = archive.to_bytes()
    actual = native.IlnkContainer.parse(packed)
    assert len(actual.blocks)==len(archive.blocks)
    assert actual.blocks[draft.BLOCK]==target
    assert all(a==b for i,(a,b) in enumerate(zip(actual.blocks,archive.blocks,strict=True)) if i!=draft.BLOCK)
    archive.blocks[draft.BLOCK] = eblock
    assert archive.to_bytes()==before[draft.FILE]
    match = native.IlnkContainer.parse(before[draft.FILE])
    assert [i for i,(a,b) in enumerate(zip(match.blocks,actual.blocks,strict=True)) if a!=b]==[draft.BLOCK]
    rom.replace_file(draft.FILE,packed)
    after = native.files(rom)
    assert before.keys()==after.keys() and {key for key in before if before[key]!=after[key]}=={draft.FILE}
    digest = native.digest(bytes(rom.rom.save()))
    rom.replace_file(draft.FILE,before[draft.FILE])
    assert bytes(rom.rom.save())==current.ROM.read_bytes()
    TARGET.write_bytes(target)
    base.save(REVIEW,packet | dict(records=rows,prior_contextual_review=str(draft.OUTPUT),
        prior_contextual_review_sha256=base.digest(draft.OUTPUT),earlier_native_preview=str(draft.ROOT/"native_preflight.json"),
        earlier_native_preview_sha256=base.digest(draft.ROOT/"native_preflight.json")))
    base.save(PROOF,dict(predecessor_sha256=candidate,proposed_ROM_sha256=digest,changed_file=draft.FILE,
        changed_block=draft.BLOCK,clean_block_sha256=native.digest(jblock),predecessor_block_sha256=native.digest(eblock),
        compiled_block=str(TARGET),compiled_block_sha256=base.digest(TARGET),
        draft=str(REVIEW),draft_sha256=base.digest(REVIEW),
        compiled_archive_sha256=native.digest(packed),complete_whole_ROM_inverse=True,commands=commands,plans=plans,
        fresh_visual_and_progressive_native_checks_pending=True,actual_gameplay=False,ROM_file_written=False))
    print(f"Compiled six Deck lesson updates with {len(commands)} exact command bindings and a whole-ROM inverse.",flush=True)


if __name__ == "__main__":
    main()

