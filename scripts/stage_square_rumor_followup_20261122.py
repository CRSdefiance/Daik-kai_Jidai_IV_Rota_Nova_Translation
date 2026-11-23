"""Review the Square regional rumor family and compile the three source corrections."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import checkpoint_regional_town_dialogue_20261115 as regional
from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_hodram_opening_reply_20261122 as parent
from scripts import stage_square_rumors_20261115 as earlier
from scripts import stage_rafael_deck_tutorial_followup_20261122 as release_tools
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town = parent.base, parent.native, earlier.template
ARM, COMMON, CLEAN = town.ARM, town.COMMON, town.CLEAN
ROOT = Path("work/analysis/square_rumor_followup_20261122")
ROM, PROOF = ROOT/"Square_Rumor_Followup_STAGED.nds", ROOT/"stored_proof.json"
PATCH, REBUILT = ROOT/"translation.xdelta", ROOT/"clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT/"startup/capture/capture_report.json"
PROSE = {
    714: "Admiral Valdes leads Spain's navy. The fleet is so imposing they call it the Invincible Armada.",
    715: "The Centurione Company once traded far and wide. Their ships crisscrossed the Mediterranean as if it were theirs.",
    725: "They say an empress would ruin China. I don't buy it. I wish the admiral who routs Japanese pirates were our empress...",
}
NOTES = earlier.NOTES | {
    710: "Keep the shopkeeper's surprise that even young women now sail to trade. The exclamation gives the reaction its own beat. The live wrapper splits Times from the rest of that sentence.",
    713: "The hearsay, ancestor's reputation, past command and Indian Ocean all come through naturally. The native wrapper starts its last row at Indian Ocean.",
    714: "Valdes leads the Spanish navy. The strength of the fleet itself earns the epithet. Two direct sentences sound like a shopkeeper passing along local knowledge.",
    715: "Separate the company's wide trade from its former habit of sailing everywhere in the Mediterranean as if it owned the sea. The shopkeeper's comparison stays figurative.",
    725: "Connect the speaker's rebuttal to the wish that the unnamed admiral who drives off Japanese pirates were their empress. Her identity and her possible rule are both left implicit elsewhere.",
}
HOLDS = {
    "valencia": ((7950, 714), (8350, None), (8750, None)),
    "syracuse": ((6750, 715), (7150, None), (7550, None), (10350, 51)),
}
WITNESSES = ROOT/"selected_rumor"


def stage():
    assert not ROOT.exists()
    previous = base.load(parent.RELEASE)
    assert previous["candidate_sha256"] == base.digest(parent.ROM)
    assert previous["registry_sha256"] == base.digest(base.REGISTRY)
    assert previous["manifest_sha256"] == base.digest(parent.MANIFEST)
    ctx = town.RegisteredRuntime(parent.RELEASE, previous["own_registered_startup"],captain=3)
    arm, common = ctx.arm, ctx.common
    assert base.digest(CLEAN) == previous["clean_input_sha256"]
    clean = base.NdsImage.open(CLEAN)
    source_arm = clean.read_file(ARM)
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(common) == previous["target_COMMON_sha256"]
    assert all(arm[a:b] == source_arm[a:b] for a,b in earlier.SOURCE_RANGES)
    directory = native.digest(arm[town.DIRECTORY_OFFSET:town.TABLE_OFFSET])
    sources = town.common_message_entries(clean.read_file(COMMON),source_arm)
    before = town.owned_entries(common,arm,directory)
    prior = base.load(earlier.MANUSCRIPT)
    old = {r["message_ID"]:r for r in prior["records"]}
    rows, storage = {}, {}
    for n in earlier.NUMBERS:
        source,current = sources[n],before[n]
        assert old[n]["source_hex"] == source.text.hex() and old[n]["staged_hex"] == current.text.hex()
        assert b"%" not in source.text and b"%" not in current.text
        logical = " ".join(current.text.decode("ascii").split())
        authored = PROSE.get(n,logical)
        rows[n] = dict(id=f"COMMON_MESSAGE_{n}",message_ID=n,file_path=COMMON,speaker="Shopkeeper",
            source_reference=town.reference(source),current_reference=town.reference(current),
            clean_Japanese=source.text.decode("cp932"),source_hex=source.text.hex(),current_hex=current.text.hex(),
            previous_English=logical,english=authored,source_meaning=earlier.MEANING[n],
            localization_note=NOTES[n],decision="revision" if n in PROSE else "retention",
            review=dict.fromkeys(town.GATES,True),preserved_runtime_arguments=[])
        if n in PROSE:
            storage[n] = town.compile_paragraph(authored)

    allocate = FunctionType(relocate.__code__,relocate.__globals__ | {"DIRECTORY": directory})
    revised,target_arm,installed,allocation = allocate(common,arm,rows,storage)
    assert allocation["changed_visible_templates"] == list(PROSE)
    assert allocation["all_unselected_native_copy_spans_exact"] and allocation["complete_COMMON_and_ARM9_table_inverse"]
    assert target_arm[:town.DIRECTORY_OFFSET] == arm[:town.DIRECTORY_OFFSET]
    assert target_arm[relocate.__globals__["TABLE_END"]:] == arm[relocate.__globals__["TABLE_END"]:]
    deployed = town.with_components(ctx,target_arm,revised)
    cpu,get,provider = deployed.machine(target_arm,revised,deployed.raw,deployed.plan)
    render,_,_ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    prev_cpu,_,_ = ctx.machine(arm,common,ctx.raw,ctx.plan)
    pictures = []
    for n,row in rows.items():
        actual = installed[n].text
        p = get(0x5528C,n)
        assert bytes(cpu.mem_read(p,len(actual)+1)) == actual+b"\0"
        formatted,lines = town.native_layout(cpu,actual,n,())
        assert 1 <= len(lines) <= 4 and all(lines) and " ".join(lines) == row["english"]
        old_body,old_lines = town.native_layout(prev_cpu,before[n].text,n,())
        row.update(native_pages=1,before_lines=old_lines,visible_lines=lines,installed_hex=actual.hex(),
            registered_reference=town.reference(installed[n]),native_format_pointer=p)
        if n in PROSE:
            assert before[n].text != actual and lines != old_lines and all(len(v)>9 for v in lines)
            for title,code,body in (("Before",arm,old_body),("Revised",target_arm,formatted)):
                pixels,glyphs = town.render_portrait(render,code,kanji,body)
                assert [g["code"] for g in glyphs] == town.glyph_codes(body)
                pictures.append((f"{n} {title}",pixels))
                if title=="Revised":
                    row["native_plane_hex"] = bytes(pixels).hex()
        else:
            assert formatted == old_body and actual == before[n].text
    assert provider.reads and bytes(cpu.mem_read(deployed.actor_root,0x1A04)) == deployed.actor_bytes
    image = base.NdsImage.open(parent.ROM)
    original = native.files(image)
    for path,data in ((ARM,target_arm),(COMMON,revised)):
        image.replace_file(path,data)
    final = native.files(image)
    assert original.keys() == final.keys() and {p for p in original if final[p]!=original[p]} <= {ARM,COMMON}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean),final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    result = bytes(image.rom.save())
    for path in (ARM,COMMON):
        image.replace_file(path,original[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    candidate = base.digest(ROM)
    for row in rows.values():
        row["registered_reference"].update(candidate_sha256=candidate,file_path=COMMON,
            archive_sha256=native.digest(revised),exact_stored_hex=row["installed_hex"])
    sheets = town.portrait_sheets(ROOT,pictures)
    base.save(PROOF,dict(candidate_sha256=candidate,predecessor_sha256=previous["candidate_sha256"],
        translation_policy="natural-dialogue-v2",target_locale="en-US", clean_sha256=previous["clean_input_sha256"],
        source_exact_ranges=earlier.SOURCE_RANGES, records=list(rows.values()), allocations=allocation,
        before_ARM9_sha256=native.digest(arm),target_ARM9_sha256=native.digest(target_arm),
        target_COMMON_sha256=native.digest(revised),whole_parent_inverse=True,
        source25=guard,sheets={r["path"]:r["sha256"] for r in sheets},offline_native_only=True,
        scene_context="With no company market share, a Square shopkeeper may give the regional faction rumor. "
        "The original selector uses the current town's region to choose one independent response.",
        unchanged_wrap_leads=[710,713]))
    print(f"Staged {candidate}. Reviewed 21 rumors and checked all three revised pages with the native formatter.",flush=True)


def replay(city):
    receipt = base.load(PROOF)
    assert base.digest(ROM) == receipt["candidate_sha256"]
    def schedule(case):
        events,_,end,history,donor = regional.capture.schedule(case)
        return events, [frame for frame,_ in HOLDS[case]], end, history, donor
    source = checked_text(getsource(playback.main),{
        "    rom = parent.ROM\n    release = base.load(parent.RELEASE)": "    rom = ROM\n    release = receipt",
    })
    scope = vars(playback) | globals() | dict(receipt=receipt,ROOT=WITNESSES,
        observer=regional.capture.scoped_observer,get_schedule=schedule,FOCUS=set(range(3668)))
    exec(compile(source,__file__+"::ordinary-regional-replay","exec"),scope)
    scope["main"](city)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("stage","patch","startup",*HOLDS))
    action = cli.parse_args().action
    if action=="stage":
        stage()
    elif action in HOLDS:
        replay(action)
    else:
        inherited = getattr(release_tools,action)
        FunctionType(inherited.__code__,inherited.__globals__ | globals())()
