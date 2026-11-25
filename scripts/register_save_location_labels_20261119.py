"""Register the verified Save and Load labels and clean-input patch."""

from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_save_dialogue_followup_20261119 as parent
from scripts import stage_save_location_labels_20261119 as stage
from scripts import verify_save_location_labels_20261119 as verified
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text

base, native = parent.base, parent.native
PROFILE = "all-routes-save-location-labels-v1-20261119"
ROOT = Path("out/save_location_labels_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Save_Location_Labels_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_save_location_labels_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_save_location_labels_20261119.md")
STARTUP, QA = verified.STARTUP, stage.ROOT / "supported_qa.xml"
CHECKPOINT = "Save and Load separate the sea area from At Sea, and the Load heading uses natural wording."


def verify(registry, previous, viewed):
    stored, game, boot = map(base.load,(stage.PROOF,verified.GAME,STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == game["candidate_sha256"] == boot["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["parent_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_input_sha256"]
    assert stored["entire_parent_inverse"] and base.digest(stored["lead"]["path"]) == stored["lead"]["sha256"]
    assert viewed == {str(p):base.digest(p) for p in (verified.SHEET,verified.OFFLINE)}
    assert all(base.digest(p)==sha for proof in (game,boot) for p,sha in proof["evidence"].items())
    assert all(game["evidence"][str(p)] == viewed[str(p)] for p in (verified.SHEET,verified.OFFLINE))
    assert game["ordinary_emulator_controls"] and not game["hardware"]
    assert [r["menu"] for r in game["both_menus_observed"]] == ["Save","Load"]
    assert game["other_paired_complete_frames"] == [5400,5800,6600,7000]
    assert game["exact_stock_and_fallback_painter_inputs"] == len(stored["stock_and_fallback_painter_arguments"]) == 18
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k,0)) for k in ("tests","failures","errors","skipped")] == [23,0,0,0]
    assert (stage.ROOT/"clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    old,new,clean = map(base.NdsImage.open,(parent.ROM,stage.ROM,stage.CLEAN))
    before,after = map(native.files,(old,new))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]} == {stage.ARM}
    earlier,arm,original = before[stage.ARM],after[stage.ARM],clean.read_file(stage.ARM)
    assert stage.digest(earlier)==previous["target_ARM9_sha256"] and stage.digest(arm)==stored["target_ARM9_sha256"]
    assert stage.digest(after[stage.COMMON])==previous["target_COMMON_sha256"]==stored["target_COMMON_sha256"]
    verify_runtime(arm,previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean),after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7 and not any(controls["source_bound_new_command_counts"].values())
    inverse = bytearray(arm)
    installation = {}
    assert len(stored["records"])==7
    for row in stored["records"]:
        source, ref = row["source_reference"],row["current_reference"]
        loc,span = ref["offset"],ref["allocation"]
        start = source["offset"]
        assert source["ARM9_sha256"]==stage.digest(original)
        assert original[start:start+source["allocation"]].hex()==row["source_hex"]
        assert earlier[loc:loc+span].hex()==row["current_hex"] and arm[loc:loc+span].hex()==row["staged_hex"]
        if row["decision"]!="retention":
            assert row["current_hex"]!=row["staged_hex"]
            inverse[loc:loc+span]=earlier[loc:loc+span]
            installation[str(loc)]=span
        else:
            assert row["current_hex"]==row["staged_hex"]
        row["registered_reference"]=ref | dict(candidate_sha256=candidate,ARM9_sha256=stage.digest(arm),
            exact_stored_hex=row["staged_hex"])
        row["review"]["formatting"]=True
    assert installation==stored["slots_changed"] and bytes(inverse)==earlier
    snap=boot["read_only_snapshot"]
    assert base.digest(snap["path"])==snap["sha256"]
    live=Path(snap["path"]).read_bytes()
    for loc,span in installation.items():
        start=int(loc)
        assert live[start:start+span]==arm[start:start+span]
    new.replace_file(stage.ARM,earlier)
    assert bytes(new.rom.save())==parent.ROM.read_bytes()
    review = {k:stored[k] for k in ("candidate_sha256","parent_sha256","translation_policy","target_locale",
        "encoder","review_gates","records","stock_and_fallback_painter_arguments")}
    review.update(new_contextual_credit=0,observed_gameplay=game,checked_story_format_guard=controls)
    validate_natural_dialogue_batch(review)
    return stored,review,{stage.ARM:stage.digest(arm)}


publish=parent.main
doc=publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme=publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main=checked_text(publish,{
    'len(manifest["batches"]) == 889 and len(manifest["checks"]) == 224':
        'len(manifest["batches"]) == 890 and len(manifest["checks"]) == 225',
    "stage.PROOF, STARTUP, QA, verified.GAME, verified.SHEET, stage.SHEET, args.visual_review":
        "stage.PROOF, STARTUP, QA, verified.GAME, verified.SHEET, verified.OFFLINE, args.visual_review",
    "release_stack_before_save_dialogue.json":"release_stack_before_save_location_labels.json",
    "release_stack_with_save_dialogue.json":"release_stack_with_save_location_labels.json",
    "verified_mutiny_dialogue_predecessor":"verified_save_dialogue_predecessor",
    "save_dialogue_followup_release":"save_location_labels_release",
    "registered_save_dialogue_followup_and_complete_parent_inverse":
        "registered_save_location_labels_and_complete_parent_inverse",
    "save_dialogue_followup_pipeline":"save_location_labels_pipeline",
    'row["decision"] == "revision"':'row["decision"] != "retention"',
    "repository_tests=25":"repository_tests=23",
    "occupied_save_and_focused_write_failure=True":"ordinary_save_and_load_slot_lists=True",
    "prose_revisions=4, wrap_only_revisions=0, justified_retentions=0":
        "prose_revisions=1, spacing_revisions=3, wrap_only_revisions=0, justified_retentions=3",
    "previously_localized_templates=4":"previously_localized_labels=7",
    "save_dialogue_followup_20261119":"save_location_labels_20261119",
    "Preserve save dialogue ROM or clean reconstruction":"Preserve save location label ROM or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Save and Load location labels test candidate

The [local ROM](../../{ROM.as_posix()}) includes the corrected At Sea separator and the revised Load heading.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Hardware remains unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Save and Load location labels

Both menus now display **N. Sea At Sea** with a separator before the status. The status follows the same rule as **Docked**. The Southeast Asia name loses its trailing padding so it receives exactly one separator, like the six other sea areas. The Load heading reads **Select a save to load.** The existing Save heading and both Docked labels were retained with individual reasons. [Exact review](../{REVIEW.as_posix()})

Two ordinary emulator runs with identical controls on copies of the Syracuse save verified both lists against the prior candidate. The first and last glyphs, the space and complete headings match the native masks. Four control frames and all pixels outside the affected fields match exactly. Both original slot selectors also passed offline checks for all seven stock areas and two invalid area values. The area-less fallback keeps one leading blank cell and the complete status. The six stock areas besides the North Sea and the fallback were checked offline. [Gameplay comparison](../{(VERIFY / verified.SHEET.name).as_posix()}) · [Offline area previews](../{(VERIFY / verified.OFFLINE.name).as_posix()})

The clean-input patch reproduces the exact ROM. Six startup holds, 24 protected name getters and 23 focused tests passed. All 114 accepted layers and the ASCII right-bound correction carry forward. The ledger stands at 27,700 credited records, with 276 stored shared entries open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env=parent.env | globals()
exec(compile(main,__file__+"::register","exec"),env)

if __name__=="__main__":
    env["main"]()

