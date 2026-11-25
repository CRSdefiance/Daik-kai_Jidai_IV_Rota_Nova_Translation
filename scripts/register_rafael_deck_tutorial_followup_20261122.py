"""Register the Rafael Deck lesson after the ordinary post-Trade replay."""

from types import FunctionType
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_rafael_deck_tutorial_followup_20261122 as live
from scripts import register_maria_tutorial_followup_20261122 as template
from scripts import register_ship_room_names_20261122 as parent
from scripts import stage_rafael_deck_tutorial_followup_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow = parent.base,parent.native,parent.workflow
PROFILE = "all-routes-rafael-deck-tutorial-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_deck_tutorial_registered_20261122")
ROM = ROOT/"Translation_DS_Rafael_Deck_Tutorial_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_deck_tutorial_candidate")
VERIFY,PATCH = PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE = VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_deck_tutorial_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP,QA,STARTUP_CAPTURE = EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml",stage.STARTUP_CAPTURE
VISUAL = stage.compiled.draft.ROOT/"visual_review_v2.json"
DISPLAY = stage.render.PROOF
CHECKPOINT = "Registered six refinements to Julio's Deck lesson and verified all twelve pages in the original post-Trade event."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard


startup_reference = parent.startup_template
startup = FunctionType(startup_reference.startup_proof.__code__,startup_reference.startup_proof.__globals__|
    {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE,"checked_report":startup_reference.check_startup_report})


def native_count():
    return base.load(DISPLAY)["offline_pages"]


def observed_count():
    return len(base.load(live.PROOF)["twelve_complete_panels"])


def observed_names():
    return 1


def pages_saved():
    return 0


def verify(registry,previous,viewed):
    stored,draft,rendered,visual,played = map(base.load,(stage.PROOF,stage.compiled.REVIEW,DISPLAY,VISUAL,live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==visual["compiled_candidate_SHA256"]==played["candidate_sha256"]
    assert candidate==rendered["proposed_ROM_sha256"]==base.digest(stage.REBUILT)
    assert previous["candidate_sha256"]==stored["predecessor_sha256"]==draft["previous_sha256"]==base.digest(parent.ROM)
    assert base.digest(stage.compiled.REVIEW)==stored["draft_sha256"]
    assert base.digest(stage.compiled.PROOF)==stored["stage_input_sha256"] and stored["complete_whole_ROM_inverse"]
    assert base.digest(DISPLAY)==stored["native_proof_sha256"]==visual["native_proof_sha256"]
    assert base.digest(VISUAL)==stored["direct_visual_sha256"] and visual["reviewed_all_pages"]==10
    assert viewed=={rendered["sheet"]:rendered["sheet_sha256"],played["sheet"]:played["sheet_sha256"]}
    assert all(base.digest(path)==sha for p in (viewed,played["evidence"]) for path,sha in p.items())
    assert played["ordinary_gameplay_existing_Lisbon_save"] and played["native_lesson_event_after_Trade"]
    assert played["speakerless_system_page_exact"] and played["full_default_capital_F_and_runtime_name"]
    assert played["ordinary_return_to_Lisbon"] and not played["hardware"]
    assert len(played["twelve_complete_panels"])==12 and played["original_command_count"]==16
    assert len(rendered["full_progressive_and_FE_cases"])==6 and rendered["offline_pages"]==10
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")]==[17,0,0,0]

    clean, before, target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]
    old_file,new_file = map(native.files,(before,target))
    assert old_file.keys()==new_file.keys()
    assert {path for path in old_file if old_file[path]!=new_file[path]}=={stage.ARCHIVE}
    new_archive = new_file[stage.ARCHIVE]
    bank = native.IlnkContainer.parse(new_archive)
    predecessor = native.IlnkContainer.parse(old_file[stage.ARCHIVE])
    assert [i for i,(a,b) in enumerate(zip(predecessor.blocks,bank.blocks,strict=True)) if a!=b]==[43]
    block = bank.blocks[43]
    assert block==stage.compiled.TARGET.read_bytes()
    assert native.digest(new_archive)==stored["compiled_archive_sha256"]
    assert native.digest(old_file[native.ARM])==previous["target_ARM9_sha256"]
    assert native.digest(old_file[parent.stage.COMMON])==previous["target_COMMON_sha256"]
    bank.blocks[43]=predecessor.blocks[43]
    assert bank.to_bytes()==old_file[stage.ARCHIVE]
    target.replace_file(stage.ARCHIVE,old_file[stage.ARCHIVE])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    controls=bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(clean),new_file)
    assert controls["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup(previous,candidate,new_file[native.ARM])

    commands = {c["record_ids"][0]:c for c in stored["commands"] if c["record_ids"]}
    observations = {r["id"]:r for r in played["twelve_complete_panels"]}
    fresh = {r["id"] for r in rendered["full_progressive_and_FE_cases"]}
    assert set(commands)==set(observations)=={r["id"] for r in draft["records"]}
    assert fresh=={r["id"] for r in draft["records"] if r["decision"]=="revision"}
    for row in draft["records"]:
        ident=row["id"]
        command,hold=commands[ident],observations[ident]["hold"]
        raw=bytes.fromhex(command["stored"])
        offset=command["stored_offset"]
        assert raw==block[offset:offset+len(raw)] and raw[:6]==bytes.fromhex(command["source"])[:6]
        row["registered_reference"]=dict(candidate_sha256=candidate,file_path=stage.ARCHIVE,block=43,
            command_offset=offset,offset=offset+5,exact_stored_hex=raw[5:raw.index(0,6)].hex(),
            complete_preamble_hex=raw[:6].hex(),complete_command_hex=raw.hex())
        row["gameplay_hold"]=hold
        row["review"]["formatting"]=True
    draft.update(candidate_sha256=candidate,checked_story_format_guard=controls,direct_visual_review=viewed,
        ordinary_Post_Trade_gameplay=str(live.PROOF),native_proof=str(DISPLAY),unchanged_pending_records=276,
        historical_source_credit=dict(by_census_id={},direct_keys=12),full_editorial_goal_complete=False,
        formatting_and_registration_pending=False)
    validate_natural_dialogue_batch(draft)
    return stored,draft,{stage.ARCHIVE:native.digest(new_archive)}


old_readme = template.build[template.build.index('    (PACKAGE / "README.md").write_text'):template.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(template.build,{
    "len(batches) == 1042 and len(checks) == 377":"len(batches) == 1044 and len(checks) == 379",
    "verified_maria_B51_B70_predecessor=predecessor":"verified_ship_room_names_predecessor=predecessor",
    "live.LIVE, display.PROOF, args.visual_review":"live.PROOF, DISPLAY, VISUAL, args.visual_review",
    'source.parent.name + "_" + source.name if source==live.LIVE else source.name':'source.name',
    "native_and_emulator_evidence_sha256=base.digest(live.LIVE),":
        "native_and_emulator_evidence_sha256={str(p):base.digest(p) for p in (live.PROOF, DISPLAY, VISUAL)},",
    "prior_records_reviewed=12, contextual_decisions_reused=3827, observed_Maria_panels=observed_count()":
        "prior_records_reviewed=12, contextual_decisions_reused=0, observed_Rafael_Deck_panels=observed_count()",
    "contextual_records_revisited=12, contextual_decisions_reused=3827":"contextual_records_revisited=12, contextual_decisions_reused=0",
    "initialized_Maria_tutorial_followup=True":"ordinary_Rafael_Deck_after_Trade=True",
    "actual_menu_samples=0, actual_style_objects=0, natural_activation=False, hardware=False":
        "actual_menu_samples=0, actual_style_objects=0, natural_activation=True, hardware=False",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's Deck lesson testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes Julio's reviewed lessons about deck assignments. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("maria_tutorial_followup","rafael_deck_tutorial")
old_doc = template.commit[template.commit.index("    DOC.write_text"):template.commit.index("    prefix =")]
commit = checked_text(template.commit,{
    "    research = [live.ROM]":"    research = []",
    "Preserve the Maria tutorial candidate, predecessor, staged ROM and focused fixture":"Preserve the Rafael Deck lesson candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Rafael's Deck lesson

Julio's captain explanation now uses four complete lines, including the original first-name substitution and the full thought about setting a course. The Sail Handler instructions and the speakerless X-menu instruction keep related words together. Six other turns retain their wording for individual reasons. [Exact clean Japanese, prior English, and final decisions](../{REVIEW.as_posix()})

The original post-Trade event displayed all twelve complete pages in ordinary emulator play from the established Lisbon save. All eleven Julio nameplates, Rafael's substituted first name, the separate system panel and the return to Lisbon passed. Native testing also covered the maximum-length first name. Hardware was outside this pass. [Gameplay and native review](../{VERIFY.as_posix()})

The clean-input patch reconstructs the candidate exactly. Only Rafael's B43 changes. Startup, 17 regressions and the original story speaker-control guard passed, with all 114 accepted layers and the registered ASCII right-bound correction carried forward. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_tutorial_followup","rafael_deck_tutorial")
scope = template.scope | globals()
for source in (build,commit):
    exec(compile(source,__file__+"::registered","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

