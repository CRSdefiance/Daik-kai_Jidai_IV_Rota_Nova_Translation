"""Register the source-reviewed Square rumors and exactly reconstructable patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET

from scripts import register_hodram_opening_reply_20261122 as parent
from scripts import stage_square_rumor_followup_20261122 as stage
from scripts import verify_square_rumor_followup_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-square-rumor-followup-v1-20261122"
ROOT = parent.ROOT.with_name("square_rumor_followup_registered_20261122")
ROM = ROOT/"Translation_DS_Square_Rumor_Followup_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_square_rumor_followup_candidate")
VERIFY, PATCH = PACKAGE/"verification", PACKAGE/"translation.xdelta"
REVIEW, RELEASE = VERIFY/"registered_review.json", VERIFY/"registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_square_rumor_followup_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE/"own_startup_verification.json",stage.STARTUP_CAPTURE,EVIDENCE/"qa_passed.xml"
VISUAL = EVIDENCE/"visual_review.json"
live = SimpleNamespace(LIVE=display.LIVE)
CHECKPOINT = "Registered three revised regional Square rumors and eighteen justified retentions."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_source = checked_text(getsource(parent.parent.parent.original),{
    "original_ARM9_and_overlay_preserved=True":
        "original_ARM9_and_overlay_preserved=False, only_COMMON_directory_and_offset_fields_changed=True, original_overlay_preserved=True",
})
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP,STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(startup_source,__file__+"::startup","exec"),startup_scope)


def native_count():
    return len(stage.PROSE)


def observed_count():
    return sum(r.get("native_mask_exact",False) for rows in base.load(live.LIVE)["observed"].values() for r in rows)


def verify(registry,previous,viewed):
    stored,played,visual = map(base.load,(stage.PROOF,live.LIVE,VISUAL))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == played["candidate_sha256"] == base.digest(stage.REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == played["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["allocations"]["complete_COMMON_and_ARM9_table_inverse"]
    assert stored["allocations"]["all_unselected_native_copy_spans_exact"] and stored["allocations"]["all_41_blocks_fit_8KiB"]
    assert viewed == visual["sheets"] == stored["sheets"] | played["sheets"]
    assert visual["reviewed_candidate_sha256"] == candidate
    assert all(base.digest(p) == h for evidence in (viewed,played["evidence"]) for p,h in evidence.items())
    assert played["original_saved_gameplay"] and observed_count() == 2
    assert played["revised_gameplay_records"] == [714,715] and played["revised_offline_only_records"] == [725]
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]

    clean,old,target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    first,final = map(native.files,(old,target))
    assert first.keys() == final.keys() and {p for p in first if first[p]!=final[p]} == {ARM,COMMON}
    directory = stage.town.DIRECTORY_OFFSET
    end = stage.relocate.__globals__["TABLE_END"]
    assert first[ARM][:directory] == final[ARM][:directory] and first[ARM][end:] == final[ARM][end:]
    hashes = {p:native.digest(final[p]) for p in (ARM,COMMON)}
    assert hashes[ARM] == stored["target_ARM9_sha256"] and hashes[COMMON] == stored["target_COMMON_sha256"]
    assert native.digest(first[ARM]) == previous["target_ARM9_sha256"] == stored["before_ARM9_sha256"]
    for path in hashes:
        target.replace_file(path,first[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = bind_registered_story_percent_guard(guard)(native.files(clean),final)
    assert checks == stored["source25"] and checks["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_scope["startup_proof"](previous,candidate,final[ARM])
    observed = {r["message_ID"]:r for holds in played["observed"].values() for r in holds if r.get("native_mask_exact")}
    records = [r | {"observed_changed_page":observed.get(r["message_ID"])} for r in stored["records"]]
    assert len(records)==21 and all(all(r["review"].values()) for r in records)
    assert {r["message_ID"] for r in records if r["decision"]=="revision"} == stage.PROSE.keys()
    result = dict(candidate_sha256=candidate,records=records,checked_story_format_guard=checks,
        ordinary_regional_dialogue=played,visual_review=viewed,prior_records_reviewed=21,
        wording_revisions=3,justified_retentions=18,unchanged_wrap_leads=stored["unchanged_wrap_leads"],
        historical_source_credit=dict(by_census_id={},direct_keys=0),full_editorial_goal_complete=False,hardware=False)
    return stored,result,hashes


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1051 and len(checks) == 386": "len(batches) == 1052 and len(checks) == 387",
    "source_bound_hodram_reply_block={stage.PATH:stored['after_block_sha256']}": "source_bound_square_rumor_storage=stored['allocations']",
    "changed_component_hashes={stage.PATH:archives[stage.PATH]}": "changed_component_hashes=archives",
    "changed_internal_files=[stage.PATH]": "changed_internal_files=sorted(archives)",
    "changed_components=1": "changed_components=2",
    "previous['target_COMMON_sha256']": "archives[COMMON]",
    "previously_localized_records=15, contextual_records_revisited=15":
        "previously_localized_records=21, contextual_records_revisited=21",
    "prior_records_reviewed=15": "prior_records_reviewed=21",
    "prose_revisions=2": "prose_revisions=3",
    "wrap_only_revisions=1": "wrap_only_revisions=0",
    "justified_retentions=12": "justified_retentions=18",
    "text_display_revisions=1": "text_display_revisions=3",
    "ordinary_Hodram_opening=True, all_three_changed_records_observed=True":
        "ordinary_Valencia_and_Syracuse=True, offline_China_rumor=True",
    "observed_Hodram_story_holds": "observed_ordinary_regional_rumors",
    "stage.PROOF, STARTUP, QA, live.LIVE, DISPLAY, args.visual_review":
        "stage.PROOF, STARTUP, QA, live.LIVE, args.visual_review",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Regional Square rumor testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the revised rumors about Valdes, the Centurione Company, and the Chinese shopkeeper's wish. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_opening_reply","square_rumor_followup").replace(
    "verified_story_literal_names_predecessor","verified_hodram_opening_reply_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit,{
    "Preserve the Hodram opening reply candidate, predecessor and staged ROM":
        "Preserve the Square rumor candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Regional Square rumors

The source pass covers all 21 regional faction and person rumors. Three revisions clarify Valdes's command, give the Centurione Company's old Mediterranean boast its own sentence, and restore the Chinese shopkeeper's wish that the unnamed admiral were empress. The other 18 rumors have specific retention reasons. [Japanese and exact installed references](../{REVIEW.as_posix()})

Ordinary continuations from existing Valencia and Syracuse saves showed the two European rumors, their original Shopkeeper labels and the return paths. The China rumor passed offline native layout and visual checks. Two earlier minor wraps in this family remain on the follow-up list. Startup, clean-input reconstruction and 17 focused tests passed. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_opening_reply","square_rumor_followup")
scope = parent.scope | globals()
for program in (build,commit):
    exec(compile(program,__file__+"::register","exec"),scope)


if __name__=="__main__":
    scope["main"]()
