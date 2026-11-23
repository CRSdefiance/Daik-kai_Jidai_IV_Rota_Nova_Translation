"""Register the Deck comments against the exact Lil Red Dye predecessor."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import TABLE_END
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_lil_red_dye_20261119 as parent
from scripts import register_rafael_sailing_modes_20261119 as scope_origin
from scripts import replay_deck_comments_20261119 as game
from scripts import stage_deck_comments_20261119 as stage
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-deck-comments-v1-20261119"
ROOT = Path("out/deck_comments_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Deck_Comments_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_deck_comments_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_deck_comments_20261119.md")
STARTUP, QA = game.STARTUP_PROOF, stage.ROOT / "registered_qa.xml"
VISUAL_REVIEW = stage.ROOT / "direct_visual_review.json"
CHECKPOINT = "The Deck personal, Shipwright and Doctor review records four revisions and 45 retentions, including a replay of Gerhard’s revised line."
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PLAYBACK)


def verify(registry, previous, viewed):
    stored, playback, boot = map(base.load, (stage.PROOF, game.PLAYBACK, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == playback["candidate_sha256"] == boot["candidate_sha256"]
    assert stored["parent_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["clean_input_sha256"] == previous["clean_input_sha256"] == base.digest(stage.CLEAN)
    assert stored["entire_parent_inverse"] and stored["allocation"]["complete_COMMON_and_ARM9_table_inverse"]
    assert all(base.digest(p) == sha for receipt in (playback, boot) for p, sha in receipt["evidence"].items())
    assert all(base.digest(p) == sha for p, sha in stored["source_proofs"].items())
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    sheets = stored["sheets"] + playback["sheets"]
    assert viewed == {s["path"]: s["sha256"] for s in sheets}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")] == [51, 0, 0, 2]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (old, new))
    arm, common = after[stage.ARM], after[stage.COMMON]
    start, table = stage.workflow.DIRECTORY_OFFSET, stage.workflow.TABLE_OFFSET
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {stage.ARM, stage.COMMON}
    assert arm[:start] == before[stage.ARM][:start] and arm[TABLE_END:] == before[stage.ARM][TABLE_END:]
    assert native.digest(arm) == stored["target_ARM9_sha256"] and native.digest(common) == stored["target_COMMON_sha256"]
    verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    for p in (stage.ARM, stage.COMMON):
        new.replace_file(p, before[p])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    before_arm = before[stage.ARM]
    source = stage.workflow.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))
    old_entries = stage.workflow.owned_entries(before[stage.COMMON], before_arm, native.digest(before_arm[start:table]))
    entries = stage.workflow.owned_entries(common, arm, native.digest(arm[start:table]))
    assert len(source) == len(old_entries) == len(entries) == 3668
    changed = [a.message_id for a, b in zip(old_entries, entries, strict=True) if a.text != b.text]
    assert changed == list(stage.EDITS) == [r["message_id"] for r in stored["native_display"]]
    assert stored["allocation"]["all_unselected_native_copy_spans_exact"]
    assert stored["allocation"]["all_41_blocks_fit_8KiB"]
    for case in stored["native_display"]:
        assert all(case[key] for key in ("complete_native_copy_macro_draw_and_ABI", "bitmap_and_input_guards_exact",
            "all_body_ink_inside_216x36", "independent_authored_words_at_x0_12px_rows_match_every_pixel"))

    pending = base.load(scope_origin.STORAGE)["records"]
    expected = base.load(parent.REVIEW)["shared_storage_scope"]
    assert len(pending) == expected["pending_records"] == 276
    assert base.digest(scope_origin.STORAGE) == expected["evidence_sha256"]
    assert sorted(row["message_ID"] for row in pending) == sorted(
        row["message_ID"] for row in base.load(stage.PENDING)["records"])
    for row in pending:
        n = row["message_ID"]
        assert row["current_hex"] == entries[n].text.hex() == old_entries[n].text.hex()
        assert row["current_reference"] == stage.workflow.reference(entries[n]) == stage.workflow.reference(old_entries[n])

    records = stored["records"]
    assert [row["message_ID"] for row in records] == list(stage.NUMBERS)
    assert [(h["message_id"], h["capture_frame"]) for h in playback["complete_holds"]] == [(1387, 4200), (1387, 4400)]
    assert playback["normal_return_frame"] == 4800 and not playback["hardware"]
    for row in records:
        n = row["message_ID"]
        assert row["source_hex"] == source[n].text.hex()
        assert row["current_hex"] == old_entries[n].text.hex()
        assert row["staged_hex"] == entries[n].text.hex()
        assert (n in changed) == (row["decision"] == "revision")
        assert row["source_reference"] == stage.workflow.reference(source[n])
        assert row["current_reference"] == stage.workflow.reference(old_entries[n])
        row["registered_reference"] = stage.workflow.reference(entries[n]) | dict(candidate_sha256=candidate)
        row["bounded_emulator_replay_observed"] = n == 1387
    review = {k: stored[k] for k in ("translation_policy", "target_locale", "encoder", "review_gates", "records")}
    review.update(candidate_sha256=candidate, checked_story_format_guard=controls, new_contextual_credit=0,
        shared_storage_scope=expected, direct_visual_review=viewed, observed_gameplay=playback,
        owned_common_directory_relocation=stored["allocation"], source_and_native_dependency_proofs=stored["source_proofs"])
    validate_natural_dialogue_batch(review)
    return stored, review, {stage.ARM: native.digest(arm), stage.COMMON: native.digest(common)}


publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
dependencies = publish[publish.index("    for source in ("):publish.index("                   *(Path(p) for p in base.load(args.visual_review))):")]
program = checked_text(publish, {
    'len(manifest["batches"]) == 913 and len(manifest["checks"]) == 248':
        'len(manifest["batches"]) == 914 and len(manifest["checks"]) == 249',
    "verified_story_item_titles_predecessor": "verified_lil_red_dye_predecessor",
    "lil_red_dye": "deck_comments",
    dependencies: "    for source in (stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review,\n",
    "owned_story_records=[row": "owned_shared_records=[row",
    "story_archives_sha256=archives": "target_COMMON_sha256=archives[stage.COMMON]",
    "changed_components=1": "changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]",
    "repository_tests=22": "repository_tests=49, legacy_fixture_tests_skipped=2",
    "prose_revisions=7, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=80":
        "prose_revisions=3, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=45",
    "text_display_revisions=7": "text_display_revisions=4",
    "name_consistency_revisions=3": "name_consistency_revisions=1",
    "initialized_complete_Lil_amsterdam_conversation=True": "initialized_Shipwright_comment_and_normal_return=True",
    "HELP_sha256=release": "ARM9_sha256=archives[stage.ARM], MESFILE_sha256=archives[stage.COMMON], HELP_sha256=release",
    "previously_localized_records=87": "previously_localized_records=49",
    "    candidates.append(game.play.FIXTURE)\n": "",
    "Preserve Red Dye ROM or reconstruction": "Preserve Deck comments ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Deck comments test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Deck comments and preceding cumulative fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Deck personal and work comments

Reviewed all 49 personal, Shipwright and Doctor comments against the clean Japanese and their original crew and role selectors. Yukihisa’s observation keeps “shines beautifully” together. Cesare’s appraisal and question tag, Gerhard’s spare-parts remark and Rafael’s reference to Clau each fit on one row. The other 45 comments have individual retention reasons, including deliberate pauses and complete reactions. [Exact review ledger](../{REVIEW.as_posix()})

All four changed pages passed native glyph, layout, crop and complete-word checks, including the period in the 36th cell of Rafael’s line. The original message lookup returned the full current bytes twice for every reviewed entry. A Copenhagen emulator replay with a disclosed room assignment fixture showed the revised Gerhard line in two complete holds and returned to town normally. The other three revisions received offline checks. Hardware remained unvisited. [Native and replay evidence](../{VERIFY.as_posix()})

The clean-input patch rebuilds the ROM byte for byte. Only COMMON and its ARM9 directory data change. The ASCII right-bound correction, all 114 accepted layers and all 276 pending shared payloads and locations carry forward. Six startup holds, 24 protected name getters and 49 focused tests passed. Two checks that require missing older ROM fixtures were skipped. The historical Deck explanation tests also require an unavailable V145 fixture. These records already had credit, and the ledger stays at 27,700. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)

if __name__ == "__main__":
    env["main"]()
