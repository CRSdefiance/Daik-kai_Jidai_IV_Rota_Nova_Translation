"""Register the verified full Square wording on the cumulative Deck candidate."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_deck_comments_20261119 as parent
from scripts import replay_square_label_wording_20261119 as game
from scripts import stage_square_label_wording_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-square-label-wording-v1-20261119"
ROOT = Path("out/square_label_wording_registered_20261119_v2")
ROM = ROOT / "Translation_DS_Square_Label_Wording_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_square_label_wording_candidate_v2")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PRESERVED_FIRST_ROM = ROOT.with_name("square_label_wording_registered_20261119_v1") / ROM.name
DOC = Path("docs/editorial_square_label_wording_20261119.md")
STARTUP, QA = game.STARTUP_PROOF, stage.ROOT / "registered_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "Seasonings and Textile Shop now appear in Lisbon Square, with both complete captions verified in gameplay."
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.GAME_PROOF)


def verify(registry, previous, viewed):
    stored, playback, boot = map(base.load, (stage.PROOF, game.GAME_PROOF, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == playback["candidate_sha256"] == boot["candidate_sha256"]
    assert stored["parent_sha256"] == playback["prior_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(stage.CLEAN) == stored["clean_input_sha256"] == previous["clean_input_sha256"]
    assert stored["entire_parent_inverse"]
    assert all(base.digest(p) == sha for r in (playback, boot) for p, sha in r["evidence"].items())
    assert all(base.digest(p) == sha for p, sha in stored["source_proofs"].items())
    assert stored["preserved_other_category_cases"] == 144 and stored["preserved_square_fallbacks"] == 241
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    assert len(playback["native_full_caption_masks"]) == 8
    assert playback["ordinary_lisbon_existing_save"] and playback["returned_to_lisbon_frame"] == 9550
    assert playback["all_dialogue_requests_exact"] and playback["no_pending_shared_requests"]
    sheets = stored["sheets"] + playback["sheets"]
    assert viewed == {s["path"]: s["sha256"] for s in sheets}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(p, 0)) for p in ("tests", "failures", "errors", "skipped")] == [29, 0, 0, 0]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, before, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (before, target))
    assert old.keys() == new.keys()
    assert {p for p in old if old[p] != new[p]} == {stage.ARM}
    arm, allocation = stage.transform(before, old[stage.ARM])
    assert arm == new[stage.ARM] and allocation == stored["allocation"]
    assert native.digest(arm) == stored["target_ARM9_sha256"]
    stage.verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    target.replace_file(stage.ARM, old[stage.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()

    records = stored["records"]
    assert [r["category"] for r in records] == list(range(18))
    assert {r["category"]: r["english"] for r in records if r["decision"] == "revision"} == stage.WORDS
    ids = []
    ja = clean.read_file(stage.ARM)
    for row in records:
        kind = row["category"]
        for product in row["clean_and_current_category_stock"]:
            index, field = product["product_ID"], product["source_name_field_offset"]
            assert field == stage.PRODUCT_NAMES + index*12
            raw_kind = ja[field+6]
            assert raw_kind == arm[field+6] and raw_kind != 9
            assert raw_kind - int(raw_kind > 9) == kind
            product["source_category_byte"] = raw_kind
            ids.append(index)
        row["registered_reference"] = row["current_reference"] | dict(candidate_sha256=candidate)
        row["file_path"] = stage.ARM
        row["emulator_caption_observed_in_lisbon"] = kind in (1, 4, 7, 8)
    assert sorted(ids) == list(range(stage.COUNT))
    review = {k: stored[k] for k in ("translation_policy", "target_locale", "encoder", "review_gates", "records")}
    review.update(candidate_sha256=candidate, checked_story_format_guard=controls, new_contextual_credit=0,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"], direct_visual_review=viewed,
        observed_gameplay=playback, owned_square_caption_selector=allocation, source_and_native_dependency_proofs=stored["source_proofs"])
    validate_natural_dialogue_batch(review)
    return stored, review, {stage.ARM: native.digest(arm)}


publish = parent.program
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 914 and len(manifest["checks"]) == 249':
        'len(manifest["batches"]) == 915 and len(manifest["checks"]) == 250',
    "verified_lil_red_dye_predecessor": "verified_deck_comments_predecessor",
    "deck_comments": "square_label_wording",
    "owned_shared_records=[row": "owned_caption_records=[row",
    "target_COMMON_sha256=archives[stage.COMMON])": "target_ARM9_sha256=archives[stage.ARM])",
    "changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]":
        "changed_components=1, target_ARM9_sha256=archives[stage.ARM]",
    "repository_tests=49, legacy_fixture_tests_skipped=2": "repository_tests=29, legacy_fixture_tests_skipped=0, reviewed_UI_labels=18",
    "prose_revisions=3, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=45":
        "prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=16",
    "text_display_revisions=4": "text_display_revisions=2",
    "name_consistency_revisions=1": "name_consistency_revisions=0",
    "initialized_Shipwright_comment_and_normal_return=True": "ordinary_Lisbon_Square_captions_and_return=True",
    "natural_activation=False, hardware=False": "natural_activation=True, hardware=False",
    "MESFILE_sha256=archives[stage.COMMON]": "MESFILE_sha256=previous['target_COMMON_sha256']",
    "previously_localized_records=49": "previously_localized_records=18, caption_revisions=2",
    "    for path in candidates:": "    candidates.append(PRESERVED_FIRST_ROM)\n    for path in candidates:",
    "Preserve Deck comments ROM or reconstruction": "Preserve Square label ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Square label wording test candidate

The [local ROM](../../{ROM.as_posix()}) includes the full Seasonings and Textile Shop captions and the preceding cumulative fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Square shop label wording

Reviewed all 18 Square captions against the clean Japanese and the original categories of all 124 trade goods. **Seasonings** replaces **Cond. Shop** and covers sugar, honey, salt and cooking oils. The Square menu supplies the retail context. **Textile Shop** replaces **Fiber Shop** and covers raw textile fibers as well as cloth. The 16 other labels have individual retention reasons. [Exact review ledger](../{REVIEW.as_posix()})

All 18 captions passed the native 64×12 render check. Both revisions use the original caption buffer and font. The Lisbon replay verified the full labels on the exact candidate and returned to town. Every changed pixel in the sampled frames stayed within the two caption fields, and the original dialogue requests matched. Other categories and invalid selectors received offline checks. Hardware remains unvisited. [Native and gameplay evidence](../{VERIFY.as_posix()})

The cumulative patch rebuilds the ROM byte for byte. Only the Square caption call and its small selector in retired scratch space change within ARM9. Every previous layer, the ASCII right-bound correction, the shared entries and all four story archives carry forward. Six startup holds, 24 protected name getters and 29 focused tests passed. Dialogue coverage remains 27,700. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
