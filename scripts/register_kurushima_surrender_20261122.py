"""Register the source-checked Kurushima surrender in the cumulative testing build."""

from types import FunctionType
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_kurushima_surrender_20261122 as live
from scripts import register_rafael_deck_tutorial_followup_20261122 as parent
from scripts import stage_kurushima_surrender_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow=parent.base,parent.native,parent.workflow
PROFILE="all-routes-maria-kurushima-surrender-v1-20261122"
ROOT=parent.ROOT.with_name("maria_kurushima_surrender_registered_20261122")
ROM=ROOT/"Translation_DS_Maria_Kurushima_Surrender_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_maria_kurushima_surrender_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_maria_kurushima_surrender_registered_20261122.md")
EVIDENCE=stage.ROOT
STARTUP,STARTUP_CAPTURE,QA=stage.ROOT/"own_startup_verification.json",stage.STARTUP_CAPTURE,stage.ROOT/"qa_passed.xml"
VISUAL=stage.ROOT/"visual_review.json"
DISPLAY=live.NATIVE
CHECKPOINT="Corrected Kurushima's offer of surrender in Maria's encounter and verified all eight panels in ordinary play from Nagasaki."
guard_spec=parent.guard_spec
bind_registered_story_percent_guard=parent.bind_registered_story_percent_guard
startup=FunctionType(parent.startup.__code__,parent.startup.__globals__|{"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE})


def native_count():
    return len(base.load(live.NATIVE)["native"]["layouts"])


def observed_count():
    return len(base.load(live.LIVE)["complete_panels"])


def observed_names():
    return len({r["after"]["name"] for r in base.load(live.LIVE)["complete_panels"]})


def pages_saved():
    return 0


def verify(registry,previous,viewed):
    stored,draft,raster,played=map(base.load,(stage.PROOF,stage.MANUSCRIPT,DISPLAY,live.LIVE))
    candidate=base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==raster["candidate_sha256"]==played["candidate_sha256"]
    assert candidate==base.digest(stage.REBUILT)
    assert previous["candidate_sha256"]==stored["predecessor_sha256"]==draft["previous_sha256"]==base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and base.digest(stage.MANUSCRIPT)==stored["manuscript_sha256"]
    assert base.digest(stage.PROOF)==raster["stored_proof_sha256"]
    visual=base.load(VISUAL)
    assert visual["reviewed_candidate_sha256"]==candidate
    assert viewed==visual["sheets"]=={r["sheet"]:r["sheet_sha256"] for r in (raster,played)}
    assert all(base.digest(path)==sha for refs in (viewed,played["evidence"]) for path,sha in refs.items())
    assert raster["all_four_name_width_pages"] and raster["native"]["id"]==stage.ID
    assert played["ordinary_Nagasaki_voyage"] and played["observed_postdialogue_sea_transition"]
    assert len(played["complete_panels"])==8 and played["retained_exact_panels"]==7 and not played["hardware"]
    suite,=ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")]==[17,0,0,0]

    clean,source,target=map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]
    before,after=map(native.files,(source,target))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={stage.ARCHIVE}
    prior,new=[native.IlnkContainer.parse(data) for data in (before[stage.ARCHIVE],after[stage.ARCHIVE])]
    assert [i for i,(a,b) in enumerate(zip(prior.blocks,new.blocks,strict=True)) if a!=b]==[stage.BLOCK]
    original=native.IlnkContainer.parse(clean.read_file(stage.ARCHIVE)).blocks[stage.BLOCK]
    current=new.blocks[stage.BLOCK]
    assert native.digest(original)==stored["source_block_sha256"]
    assert native.digest(current)==stored["compiled_block_sha256"]
    assert native.digest(after[stage.ARCHIVE])==stored["compiled_archive_sha256"]
    assert native.digest(after[native.ARM])==previous["target_ARM9_sha256"]
    assert native.digest(after["/COMMON/MESFILE.DK4"])==previous["target_COMMON_sha256"]
    target.replace_file(stage.ARCHIVE,before[stage.ARCHIVE])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    controls=bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(clean),after)
    assert controls["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup(previous,candidate,after[native.ARM])

    compiled={r["record_ids"][0]:r for r in stored["commands"] if r["record_ids"]}
    shots={r["id"]:r["after"] for r in played["complete_panels"]}
    assert set(compiled)==set(shots)=={r["id"] for r in draft["records"]}
    for row in draft["records"]:
        ident=row["id"]
        c=compiled[ident]
        raw=bytes.fromhex(c["stored"])
        at=c["stored_offset"]
        assert raw==current[at:at+len(raw)] and bytes.fromhex(c["source"])[:6]==raw[:6]
        row["registered_reference"]=dict(candidate_sha256=candidate,file_path=stage.ARCHIVE,block=stage.BLOCK,
            command_offset=at,offset=at+5,exact_stored_hex=raw[5:raw.index(0,6)].hex(),complete_command_hex=raw.hex())
        row["gameplay_hold"]=shots[ident]
        row["review"]["formatting"]=True
    draft.update(candidate_sha256=candidate,checked_story_format_guard=controls,direct_visual_review=viewed,
        ordinary_Nagasaki_replay=str(live.LIVE),native_proof=str(DISPLAY),unchanged_pending_records=276,
        historical_source_credit=dict(by_census_id={},direct_keys=8),full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(draft)
    return stored,draft,{stage.ARCHIVE:native.digest(after[stage.ARCHIVE])}


old_readme=parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(parent.build,{
    "len(batches) == 1044 and len(checks) == 379":"len(batches) == 1045 and len(checks) == 380",
    "verified_ship_room_names_predecessor=predecessor":"verified_rafael_deck_tutorial_predecessor=predecessor",
    "live.PROOF, DISPLAY, VISUAL, args.visual_review":"live.LIVE, DISPLAY, args.visual_review",
    "(live.PROOF, DISPLAY, VISUAL)":"(live.LIVE, DISPLAY)",
    "previously_localized_records=12, contextual_records_revisited=12":"previously_localized_records=8, contextual_records_revisited=8",
    "prior_records_reviewed=12":"prior_records_reviewed=8",
    "observed_Rafael_Deck_panels":"observed_Kurushima_panels",
    "ordinary_Rafael_Deck_after_Trade=True":"ordinary_Maria_Kurushima_encounter=True",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Maria's Kurushima encounter testing candidate

The [testing ROM](../../{ROM.as_posix()}) restores who is being asked to surrender in Maria's confrontation with Kurushima. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_deck_tutorial","maria_kurushima_surrender").replace(
    "verified_maria_kurushima_surrender_predecessor","verified_rafael_deck_tutorial_predecessor").replace(
    "prose_revisions=6","prose_revisions=1").replace("justified_retentions=6","justified_retentions=7")
old_doc=parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit=checked_text(parent.commit,{
    "Preserve the Rafael Deck lesson candidate, predecessor and staged ROM":"Preserve the Maria Kurushima candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Maria's encounter with Kurushima

Kurushima offers to let Maria surrender without a fight if she agrees to be his. He threatens to spare only her. The previous wording made Kurushima sound as though he might surrender. The corrected line preserves his coercive tone, her given-name substitution, and her response. Seven nearby turns retain their wording with individual reasons. [Exact Japanese, previous text and revised dialogue](../{REVIEW.as_posix()})

The original encounter opened during an ordinary departure from a saved game at Nagasaki. The replay verified all eight dialogue panels and their nameplates, including the full corrected text and the transition back to Sea View. Offline native checks covered four name-width cases. Hardware remains unvisited. [Native and emulator verification](../{VERIFY.as_posix()})

Only Maria's encounter block changes. Startup and 17 focused tests passed with all 114 accepted layers and the ASCII right-bound correction. The clean-input patch rebuilds the candidate exactly. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_deck_tutorial","maria_kurushima_surrender")
scope=parent.scope|globals()
for program in (build,commit):
    exec(compile(program,__file__+"::register","exec"),scope)


if __name__=="__main__":
    scope["main"]()

