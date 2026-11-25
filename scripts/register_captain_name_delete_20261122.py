"""Register the verified captain-name editor correction as a runtime-only candidate."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET

from ndspy.code import MainCodeFile

from scripts import register_ceuta_supply_alerts_20261122 as parent
from scripts import stage_captain_name_delete_20261122 as stage
from scripts import verify_hodram_custom_names_20261122 as played
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow=parent.base,parent.native,parent.workflow
ARM,COMMON=native.ARM,"/COMMON/MESFILE.DK4"
PROFILE="all-routes-captain-name-delete-v1-20261122"
ROOT=parent.ROOT.with_name("captain_name_delete_registered_20261122")
ROM=ROOT/"Translation_DS_Captain_Name_Delete_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_captain_name_delete_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_captain_name_delete_registered_20261122.md")
EVIDENCE,DISPLAY=stage.ROOT,played.DEFECT
STARTUP,STARTUP_CAPTURE,QA=EVIDENCE/"own_startup_verification.json",stage.STARTUP_CAPTURE,EVIDENCE/"qa_passed.xml"
VISUAL=EVIDENCE/"visual_review.json"
live=SimpleNamespace(LIVE=played.LIVE)
CHECKPOINT="Registered the captain-name Delete correction and captured a separate surname-substitution defect in Hodram's opening."
guard_spec=parent.guard_spec
bind_registered_story_percent_guard=parent.bind_registered_story_percent_guard
original=parent.parent.startup
startup_source=checked_text(getsource(original),{
    "original_ARM9_and_overlay_preserved=True":"original_ARM9_and_overlay_preserved=False, "
    "source_bound_captain_name_delete_only=True, original_overlay_preserved=True",
})
startup_scope=original.__globals__|{"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE}
exec(compile(startup_source,__file__+"::name-deletion-startup","exec"),startup_scope)


def native_count():
    return len(base.load(stage.PROOF)["native_character_deletion"]["cases"])


def observed_count():
    return len(base.load(live.LIVE)["editable_results"])+1


def verify(registry,previous,viewed):
    stored,edit,defect,vis=map(base.load,(stage.PROOF,live.LIVE,DISPLAY,VISUAL))
    candidate=base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==edit["candidate_sha256"]==base.digest(stage.REBUILT)
    assert previous["candidate_sha256"]==stored["predecessor_sha256"]==edit["predecessor_sha256"]==defect["candidate_sha256"]==base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["macro_like_name_display_defect_remains_open"]
    assert vis["reviewed_candidate_sha256"]==candidate
    expected={p["sheet"]:p["sheet_sha256"] for p in (edit,defect)}
    assert viewed==vis["sheets"]==expected
    assert all(base.digest(path)==sha for values in (viewed,edit["evidence"],defect["evidence"]) for path,sha in values.items())
    assert edit["ordinary_controls_only"] and edit["over_capacity_input_rejected"]
    assert (edit["deletion_before_characters"],edit["deletion_after_characters"])==(2,1)
    assert len(edit["editable_results"])==8 and len(edit["confirmation"])==2
    assert defect["observed_in_ordinary_opening"] and defect["engine_consumer_fix_pending"]
    assert native_count()>=40 and all(c["byte_exact_to_stock"] for c in stored["native_character_deletion"]["noncaptain_scopes"])
    suite,=ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")]==[17,0,0,0]

    clean,old,target=map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]
    before,after=map(native.files,(old,target))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={ARM}
    assert native.digest(after[ARM])==stored["target_ARM9_sha256"]
    assert native.digest(after[COMMON])==previous["target_COMMON_sha256"]
    original,current=map(lambda value:MainCodeFile(value,stage.BASE),(before[ARM],after[ARM]))
    info=stored["source_bound_helper"]
    tail=bytes.fromhex(info["helper_hex"])
    assert bytes(current.sections[-1].data)==bytes(original.sections[-1].data)+tail
    assert info["exact_ARM9_inverse"] and info["original_code_other_callers_and_cache_plan_preserved"]
    current.sections[-1].data=bytearray(original.sections[-1].data)
    slot=stage.patch.DELETE_CALL
    current.sections[0].data[slot:slot+4]=original.sections[0].data[slot:slot+4]
    assert bytes(current.save())==before[ARM]
    target.replace_file(ARM,before[ARM])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()

    checks=bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(clean),after)
    assert checks["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(checks["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous,candidate,after[ARM])
    result=dict(candidate_sha256=candidate,records=[],checked_story_format_guard=checks,stored_helper=info,
        ordinary_editor_evidence=edit,visual_review=viewed,changed_text_records=0,native_cases=native_count(),
        observed_editor_holds=observed_count(),hardware=False,earlier_credit_carried_forward=True,
        unresolved_original_surname_expansion=dict(path=str(DISPLAY),sha256=base.digest(DISPLAY),
            clean_and_installed_speech_unchanged=True,observed_on_predecessor=True),
        historical_source_credit=dict(by_census_id={},direct_keys=0),full_editorial_goal_complete=False)
    return stored,result,{ARM:native.digest(after[ARM]),COMMON:native.digest(after[COMMON])}


old_readme=parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(parent.build,{
    "len(batches) == 1048 and len(checks) == 383":"len(batches) == 1049 and len(checks) == 384",
    "verified_istanbul_tobacco_predecessor=predecessor":"verified_ceuta_supply_alerts_predecessor=predecessor",
    "original_supply_substitution_order=True, archive_hashes=archives, source_owned_supply_literal_slots=stored['source_bound_sailing_supply_text'],":"original_name_fields_and_limits_preserved=True, changed_component_hashes={stage.native.ARM:archives[stage.native.ARM]}, source_bound_captain_name_delete=stored['source_bound_helper'],",
    "changed_internal_files=sorted(archives)":"changed_internal_files=[stage.native.ARM]",
    "changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]":
        "changed_components=1, target_ARM9_sha256=archives[stage.native.ARM], target_COMMON_sha256=previous['target_COMMON_sha256']",
    "archives[stage.ARM]":"archives[stage.native.ARM]",
    "archives[stage.COMMON]":"previous['target_COMMON_sha256']",
    "previously_localized_records=13, contextual_records_revisited=13":"previously_localized_records=0, contextual_records_revisited=0",
    "prior_records_reviewed=13":"prior_records_reviewed=0",
    "prose_revisions=1":"prose_revisions=0",
    "justified_retentions=12":"justified_retentions=0",
    "text_display_revisions=12":"text_display_revisions=0, editor_control_corrections=1",
    "observed_ordinary_Ceuta_supply_panels":"observed_Hodram_name_editor_holds",
    "ordinary_Hodram_sailing=True, offline_automatic_travel_cases=12":"ordinary_Hodram_name_editor=True, unresolved_surname_expansion=True",
    "native_pages_checked=native_count()":"native_deletion_cases=native_count()",
    "natural_depletion_observed=True, hardware=False":"hardware=False",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Captain name editor testing candidate

The [testing ROM](../../{ROM.as_posix()}) makes Delete remove a single character in the captain's name editor. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("ceuta_supply_alerts","captain_name_delete").replace(
    "verified_captain_name_delete_predecessor","verified_ceuta_supply_alerts_predecessor")
old_doc=parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit=checked_text(parent.commit,{
    "Preserve the Ceuta supply alerts candidate, predecessor and staged ROM":"Preserve the captain-name deletion candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Captain name editor deletion

A normal Hodram New Game accepted a sixteen-letter first name and rejected an extra key. One Delete press originally removed two letters. The registered correction removes one Latin character. The existing wide-character path still removes a complete kana. The paired actual replays confirmed the capacity, one-letter deletion, re-entry and all four accepted name fields. The isolated cursor matrix covered mixed character widths, interior deletion, and ordinary and village providers. [Editor replay and checks](../{VERIFY.as_posix()})

The same original opening exposed a separate name-display defect. Charles's source speech uses the surname once. The first expansion contains the accepted name, but the onscreen line also substitutes the FI, FA and FO sequences inside that name. This added an unwanted page. The exact record, screenshots and source and live names are preserved for the display correction. [Surname finding](../{(VERIFY / DISPLAY.name).as_posix()})

Only the name-editor call and its source-scoped helper change. Startup and 17 tests passed. The clean-input patch reconstructs the candidate exactly. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("ceuta_supply_alerts","captain_name_delete")
scope=parent.scope|globals()
for program in (build,commit):
    exec(compile(program,__file__+"::register","exec"),scope)


if __name__=="__main__":
    scope["main"]()

