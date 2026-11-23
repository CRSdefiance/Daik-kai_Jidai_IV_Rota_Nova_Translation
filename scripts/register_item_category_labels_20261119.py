"""Register the verified Source Item label on the cumulative release."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_tavern_strategist_followup_20261119 as parent
from scripts import stage_item_category_labels_20261119 as stage
from scripts import verify_item_category_labels_20261119 as offline
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-item-category-labels-v1-20261119"
ROOT = Path("out/item_category_labels_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Item_Category_Labels_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_item_category_labels_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_item_category_labels_20261119.md")
STARTUP, QA = offline.STARTUP, stage.ROOT / "supported_qa.xml"
CHECKPOINT = "The item screens now use Source Item, matching Help and the Market dialogue."
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=offline.LIVE)


def verify(registry, previous, viewed):
    stored, display, live, boot = map(base.load, (stage.PROOF, offline.PROOF, offline.LIVE, STARTUP))
    candidate = base.digest(stage.ROM)
    assert all(p["candidate_sha256"] == candidate for p in (stored, display, live, boot))
    assert display["staged_sha256"] == base.digest(stage.PROOF)
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == stored["previous_sha256"]
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_input_sha256"]
    assert stored["entire_parent_inverse"] and (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    assert all(base.digest(p) == sha for p, sha in stored["source_proofs"].items())
    assert all(base.digest(p) == sha for r in (live, boot) for p, sha in r["evidence"].items())
    assert len(display["cases"]) == 124 and display["both_native_item_consumers"]
    assert display["other_pixels_and_parameters_exact"] and display["category_11_exact_unchanged_slot"]
    assert [r["item"] for r in live["observed"]] == ["Pumpkin Seeds", "Tomato Seedling"]
    assert live["complete_gallery_menu_labels_after_back"] and not live["hardware"]
    captures = live["observed"] + [live["returned"]]
    assert viewed == ({r["path"]: r["sha256"] for r in display["sheets"]} |
                      {r["path"]: r["PNG_sha256"] for r in captures})
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [34, 0, 0, 0]

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    arm, prev_arm = after[stage.ARM], before[stage.ARM]
    common_sha = native.digest(after[stage.COMMON])
    assert common_sha == previous["target_COMMON_sha256"] == stored["target_COMMON_sha256"]
    assert native.digest(arm) == stored["target_ARM9_sha256"]
    verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    slot = stored["slot"]
    start, old_bytes, new_bytes = slot["offset"], bytes.fromhex(slot["old_hex"]), bytes.fromhex(slot["new_hex"])
    end = start + len(old_bytes)
    assert len(old_bytes) == len(new_bytes) and arm[start:end] == new_bytes and prev_arm[start:end] == old_bytes
    assert arm[:start] + old_bytes + arm[end:] == prev_arm
    snapshot = Path(boot["read_only_snapshot"]["path"]).read_bytes()
    resident = slot["pointer"] - stage.BASE
    assert snapshot[resident:resident + len(new_bytes)] == new_bytes
    help_offset = after["/COMMON/HELP.DK4"].index(b"{Source Item:")
    lil_bytes = IlnkContainer.parse(after["/data/SC2.DK4"]).blocks[43]
    lil_sentences = (b"got\n a source item", b"A source item won't work just",
                     b"Bring a source item that suits")
    related = [dict(file_path="/COMMON/HELP.DK4", offset=help_offset, compiled_text="Source Item")]
    related.extend(dict(file_path="/data/SC2.DK4", zero_based_block=43, offset=lil_bytes.index(text),
                        compiled_hex=text.hex()) for text in lil_sentences)
    new.replace_file(stage.ARM, prev_arm)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    source = clean.read_file(stage.ARM)
    records = stored["records"]
    assert len(records) == 13 and [r["id"] for r in records if r["decision"] == "revision"] == ["ITEM_CATEGORY_00"]
    by_category = {r["category"] for r in display["cases"]}
    for row in records:
        source_ref, ref = row["source_reference"], row["current_reference"]
        assert stage.word(source, source_ref["field"]) == source_ref["source_pointer"]
        assert stage.cstring(source, source_ref["source_pointer"] - stage.BASE).hex() == row["source_hex"]
        offset = ref["ARM9_offset"]
        assert stage.cstring(prev_arm, offset).hex() == row["current_hex"]
        assert stage.cstring(arm, offset).hex() == row["compiled_hex"]
        row["review"]["formatting"] = True
        row["gameplay_observed"] = row["id"] == "ITEM_CATEGORY_00"
        row["native_item_panel_verified"] = row["id"] in by_category
        row["registered_reference"] = ref | dict(candidate_sha256=candidate, exact_stored_hex=row["compiled_hex"])
    prior_review = base.load(parent.REVIEW)
    assert prior_review["shared_storage_scope"]["exact_payloads_and_locations"]
    review = {key: stored[key] for key in ("translation_policy", "target_locale", "encoder", "review_gates", "records")}
    review.update(candidate_sha256=candidate, checked_story_format_guard=controls, new_contextual_credit=0,
        shared_storage_scope=prior_review["shared_storage_scope"], direct_visual_review=viewed,
        observed_gameplay=live, native_display_sha256=base.digest(offline.PROOF), slot=slot,
        matching_current_terminology=related)
    validate_natural_dialogue_batch(review)
    return stored, review, {stage.ARM: native.digest(arm), stage.COMMON: common_sha}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 901 and len(manifest["checks"]) == 236':
        'len(manifest["batches"]) == 902 and len(manifest["checks"]) == 237',
    '"tavern_strategist_followup_20261119" not in ledger': '"item_category_labels_20261119" not in ledger',
    "release_stack_before_tavern_strategist_followup.json": "release_stack_before_item_category_labels.json",
    "release_stack_with_tavern_strategist_followup.json": "release_stack_with_item_category_labels.json",
    "verified_hodram_early_confrontations_predecessor": "verified_tavern_strategist_predecessor",
    "tavern_strategist_followup_release": "item_category_labels_release",
    "registered_tavern_strategist_followup_and_complete_parent_inverse": "registered_item_category_labels_and_complete_parent_inverse",
    "tavern_strategist_followup_pipeline": "item_category_labels_pipeline",
    "owned_shared_records=[row": "owned_item_category_records=[row",
    "changed_internal_files=sorted(archives)": "changed_internal_files=[stage.ARM]",
    "changed_components=2": "changed_components=1",
    "prose_revisions=15": "prose_revisions=0",
    "justified_retentions=91": "justified_retentions=12",
    "name_label_revisions=0, text_display_revisions=15": "name_label_revisions=1, text_display_revisions=1",
    "initialized_London_Schemes_and_cancellations=True": "initialized_Gallery_item_labels_and_return=True",
    "previously_localized_records=106": "previously_localized_records=13, item_category_label_revisions=1",
    'ledger["tavern_strategist_followup_20261119"]': 'ledger["item_category_labels_20261119"]',
    "Preserve Tavern follow-up ROM or clean reconstruction": "Preserve item category ROM or clean reconstruction",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Item Category Labels test candidate

The [local ROM](../../{ROM.as_posix()}) labels specialty-producing items **Source Item** on the item cards. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte. The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Item category labels

The category printed next to Pumpkin Seeds and similar items now reads **Source Item**. The clean Japanese uses 原産物 in the item category, the Help article and Lil’s Market exchange. These items can add a trade specialty to a suitable town. “Local Product” suggested a trade good already sold there. The other 12 categories retain their existing English with individual source-based reasons. [Exact review ledger](../{REVIEW.as_posix()})

Offline checks covered 124 native renders in both item panels and bitmap modes, including all 20 Source Items. The category changed within its own column. Names, prices, advice, icons and surrounding fields retain their previous data. The reserved “Other” category has no item among the 218 stock entries and its existing slot remains byte-identical. [Native proof](../{(VERIFY / verified.PROOF.name).as_posix()})

With an initialized collection save, the emulator showed the complete **Source Item** label for Pumpkin Seeds and Tomato Seedling. Back returned to the Gallery menu. The compact item panel received offline coverage. Six startup checkpoints, 24 protected name getters and 34 focused tests passed. The clean-input patch reconstructs the candidate byte for byte. The earlier 27,700 credited reviews carry forward. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(main, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
