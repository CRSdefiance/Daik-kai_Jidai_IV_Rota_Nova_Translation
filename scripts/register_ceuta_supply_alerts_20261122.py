"""Register the source-bound supply alert corrections in the cumulative candidate."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_istanbul_tobacco_20261122 as parent
from scripts import replay_ceuta_supply_alerts_20261122 as playback
from scripts import stage_ceuta_supply_alerts_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow = parent.base,parent.native,parent.workflow
PROFILE = "all-routes-ceuta-supply-alerts-v1-20261122"
ROOT = parent.ROOT.with_name("ceuta_supply_alerts_registered_20261122")
ROM = ROOT/"Translation_DS_Ceuta_Supply_Alerts_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_ceuta_supply_alerts_candidate")
VERIFY,PATCH = PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE = VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_ceuta_supply_alerts_registered_20261122.md")
EVIDENCE,DISPLAY = stage.ROOT,stage.NATIVE
STARTUP,STARTUP_CAPTURE,QA = EVIDENCE/"own_startup_verification.json",stage.STARTUP_CAPTURE,EVIDENCE/"qa_passed.xml"
VISUAL = EVIDENCE/"visual_review.json"
live = SimpleNamespace(LIVE=playback.LIVE)
CHECKPOINT = "Registered the supply-alert wording and capitalization corrections and verified both warnings during ordinary sailing from Ceuta."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_source = checked_text(getsource(parent.startup),{
    "original_ARM9_and_overlay_preserved=True": "original_ARM9_and_overlay_preserved=False, "
    "only_owned_supply_argument_data_in_ARM9=True, original_overlay_preserved=True",
})
startup_scope = parent.startup.__globals__ | {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE}
exec(compile(startup_source,__file__+"::supply-data-startup","exec"),startup_scope)


def native_count():
    return len(base.load(DISPLAY)["all_supply_modes_and_voice_cases"])


def observed_count():
    return len(base.load(playback.LIVE)["ordinary_alerts"])


def verify(registry,previous,viewed):
    stored,draft,offline,played = map(base.load,(stage.PROOF,stage.MANUSCRIPT,DISPLAY,playback.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==offline["candidate_sha256"]==played["candidate_sha256"]==base.digest(stage.REBUILT)
    assert previous["candidate_sha256"]==stored["predecessor_sha256"]==played["predecessor_sha256"]==base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and base.digest(stage.PROOF)==offline["stored_proof_sha256"]
    assert base.digest(stage.MANUSCRIPT)==stored["manuscript_sha256"] and base.digest(stage.PRIOR)==draft["previous_registered_review_sha256"]
    visual=base.load(VISUAL)
    assert visual["reviewed_candidate_sha256"]==candidate
    expected={r["path"]:r["sha256"] for r in offline["formatting_sheets"]} | {played["sheet"]:played["sheet_sha256"]}
    assert visual["sheets"]==viewed==expected and visual["native_panels_read"]==native_count()==28
    assert all(base.digest(path)==sha for references in (viewed,played["evidence"]) for path,sha in references.items())
    assert played["normal_sailing_inputs"] and played["no_supplied_encounter_or_resource_conditions"]
    assert not played["hardware"] and observed_count()==2
    assert [r["after"]["text"] for r in played["ordinary_alerts"]]==["No water left!","No food left!"]
    suite,=ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")]==[17,0,0,0]

    clean,source,target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]
    jp,before,after = map(native.files,(clean,source,target))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={stage.ARM,stage.COMMON}
    components = {p:native.digest(after[p]) for p in (stage.ARM,stage.COMMON)}
    assert components==stored["target_components"]
    arm,owner = stage.project(jp,before)
    assert arm==after[stage.ARM] and owner==stored["source_bound_sailing_supply_text"]
    assert list(stage.NEW_POINTERS)==offline["exact_actual_getter_pointers"]
    directory = native.digest(arm[stage.DIRECTORY_OFFSET:stage.TABLE_OFFSET])
    old=stage.owned_entries(before[stage.COMMON],before[stage.ARM],directory)
    new=stage.owned_entries(after[stage.COMMON],arm,directory)
    jp_rows=stage.common_message_entries(jp[stage.COMMON],jp[stage.ARM])
    expected,rebound,slots=stage.owned_deployment(before[stage.COMMON],arm,old,{stage.REVISED:stage.NEW_TEXT.encode("ascii")})
    assert expected==after[stage.COMMON] and rebound==new
    assert {str(n):slot for n,slot in slots.items()}==stored["stored_template_allocations"]
    pending=base.load(stage.PENDING)["records"]
    assert len(pending)==stored["unchanged_alternate_display_records"]==276
    assert all(stage.reference(new[r["message_ID"]])==r["current_reference"]
        and new[r["message_ID"]].text.hex()==r["current_hex"] for r in pending)
    for path in components:
        target.replace_file(path,before[path])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    controls = bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(jp,after)
    assert controls["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous,candidate,arm)
    ram=Path(base.load(STARTUP)["read_only_snapshot"]["path"]).read_bytes()
    for offset,size in ((stage.POINTERS,8),(stage.SLOT,len(stage.AFTER))):
        assert ram[offset:offset+size]==arm[offset:offset+size]

    cases=offline["all_supply_modes_and_voice_cases"]
    assert tuple(row["message_ID"] for row in draft["records"])==stage.IDS
    for row in draft["records"]:
        n=row["message_ID"]
        assert (row["source_hex"],row["current_hex"],row["installed_hex"])==tuple(t[n].text.hex() for t in (jp_rows,old,new))
        formatting=[c for c in cases if c["message_ID"]==n]
        assert len(formatting)==(2 if n<609 else 3 if n>609 else 0)
        if formatting:
            assert all(c["exact_first_and_last"] and c["full_raster_and_bounds"] for c in formatting)
        else:
            row["retained_display_evidence"]=str(stage.PRIOR)
        row["registered_reference"]=stage.reference(new[n])|{"exact_stored_hex":new[n].text.hex(),"candidate_sha256":candidate}
        row["formatting_cases"]=formatting
        row["ordinary_gameplay_holds"]=[r for r in played["ordinary_alerts"] if r["message_ID"]==n]
        row["review"]["formatting"]=True
    draft.update(candidate_sha256=candidate,checked_story_format_guard=controls,direct_visual_review=viewed,
        ordinary_sailing_playback=str(playback.LIVE),native_supply_cases=str(DISPLAY),
        unchanged_pending_records=276,historical_source_credit=dict(by_census_id={},direct_keys=13),
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(draft)
    return stored,draft,components


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(parent.build,{
    "len(batches) == 1047 and len(checks) == 382": "len(batches) == 1048 and len(checks) == 383",
    "verified_osaka_glass_predecessor=predecessor": "verified_istanbul_tobacco_predecessor=predecessor",
    "original_name_substitution_order=True, archive_hashes=archives, command_maps_FE_choice_slots_and_actor_style_aliases_preserved=True,":
        "original_supply_substitution_order=True, archive_hashes=archives, source_owned_supply_literal_slots=stored['source_bound_sailing_supply_text'],",
    "_, draft, archives = verify(": "stored, draft, archives = verify(",
    'target_ARM9_sha256=previous["target_ARM9_sha256"]':"target_ARM9_sha256=archives[stage.ARM]",
    "changed_components=1, repository_tests=17": "changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON], repository_tests=17",
    "previously_localized_records=32, contextual_records_revisited=32": "previously_localized_records=13, contextual_records_revisited=13",
    "prior_records_reviewed=32": "prior_records_reviewed=13",
    "prose_revisions=2":"prose_revisions=1",
    "justified_retentions=30":"justified_retentions=12",
    "text_display_revisions=0":"text_display_revisions=12",
    "observed_Istanbul_panels": "observed_ordinary_Ceuta_supply_panels",
    "initialized_Lil_scene=True, ordinary_Hodram_Square_on_exact_predecessor=True": "ordinary_Hodram_sailing=True, offline_automatic_travel_cases=12",
    "native_revised_pages=native_count(), observed_holds=observed_count(), contextual_nameplate_retentions=observed_names(), reclaimed_page_turns=pages_saved(), actual_menu_samples=0, actual_style_objects=0, natural_activation=False, hardware=False":
        "native_pages_checked=native_count(), observed_holds=observed_count(), natural_depletion_observed=True, hardware=False",
    "native_and_emulator_evidence_sha256={str(p):base.digest(p) for p in (live.LIVE, replay.NORMAL, stage.PROOF)}":
        "native_and_emulator_evidence_sha256={str(p):base.digest(p) for p in (live.LIVE, DISPLAY)}",
    "live.LIVE, replay.NORMAL, stage.MANUSCRIPT, args.visual_review":"live.LIVE, DISPLAY, args.visual_review",
    "registered_release_verification=str(RELEASE),":
        "registered_release_verification=str(RELEASE), ARM9_sha256=archives[stage.ARM], MESFILE_sha256=archives[stage.COMMON],",
    "pagination_fixes=pages_saved()":"pagination_fixes=0",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Ceuta supply alerts testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the corrected sailing supply warnings. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("istanbul_tobacco","ceuta_supply_alerts").replace(
    "verified_ceuta_supply_alerts_predecessor","verified_istanbul_tobacco_predecessor")
old_doc=parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit=checked_text(parent.commit,{
    '    research = [Path(base.load(replay.ROOT / "route2/fixture.json")["rom"]), stage.VOYAGE/"editorial/Istanbul_Tobacco_Lil_STAGED.nds", stage.VOYAGE/"editorial/focused/route2/Istanbul_Lil_FOCUSED_ONLY.nds"]':
        "    research = []",
    "Preserve the Istanbul candidate, predecessor and focused ROMs":"Preserve the Ceuta supply alerts candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Sailing supply alerts from Ceuta

Charles's warnings now read “No water left!” and “No food left!” The original resource selection supplies lowercase common nouns in both dialogue callers. The younger First Mate's warning restores the source stammer. The other twelve template wordings retain individual reasons, including the sailor's separate hunger complaint. [Exact decisions and stored references](../{REVIEW.as_posix()})

An ordinary replay from a copied Ceuta save observed both alerts and the return to sailing. Both changed pages match complete native glyph masks. The same voyage did not trigger the historical sea-foam encounter. All 28 supply and automatic-travel panels passed native checks and visual review. Travel cancellation and the other crew voices were checked offline. Hardware remains unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the ROM exactly. Startup and 17 tests passed. The build carries 114 accepted layers and the registered ASCII right-bound correction. The existing capitalized menu strings remain available through their original references. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("istanbul_tobacco","ceuta_supply_alerts")
scope=parent.scope | globals()
for program in (build,commit):
    exec(compile(program,__file__+"::registered","exec"),scope)


if __name__=="__main__":
    scope["main"]()

