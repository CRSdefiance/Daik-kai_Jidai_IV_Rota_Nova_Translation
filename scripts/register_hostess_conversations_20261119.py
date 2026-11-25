"""Register the hostess review after native layout and representative tavern checks."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import prepare_all_routes_promotion_20261111 as runtime_guard
from scripts import register_departure_warnings_20261119 as parent
from scripts import replay_hostess_conversations_20261119 as game
from scripts import stage_hostess_conversations_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-hostess-conversations-v1-20261119"
ROOT = Path("out/hostess_conversations_registered_20261119_v1")
ROM = ROOT / "Translation_DS_Hostess_Conversations_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_hostess_conversations_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_hostess_conversations_20261119.md")
STARTUP, QA = game.STARTUP_PROOF, stage.ROOT / "registered_qa.xml"
CHECKPOINT = "Tavern hostess introductions, chat and gifts received 31 contextual reviews and four revised replies."
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PLAYBACK)


def verify(registry, previous, viewed):
    staged, playback, boot = map(base.load, (stage.PROOF, game.PLAYBACK, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == staged["candidate_sha256"] == playback["candidate_sha256"] == boot["candidate_sha256"]
    assert staged["parent_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(stage.CLEAN) == staged["clean_input_sha256"] == previous["clean_input_sha256"]
    assert staged["entire_parent_inverse"] and staged["visual_layout_cases"] == 273
    assert all(base.digest(p) == sha for receipt in (playback, boot) for p, sha in receipt["evidence"].items())
    assert all(base.digest(p) == sha for p, sha in staged["source_proofs"].items())
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    assert playback["ordinary_inputs"] and not playback["hardware"] and playback["normal_town_return"]
    observed = {row["message_ID"] for row in playback["hostess_holds"]}
    assert observed == {827, 992} and playback["observed_revised_IDs"] == [992]
    assert not playback["pending_shared_requests"]
    assert viewed == {s["path"]: s["sha256"] for s in staged["sheets"] + playback["sheets"]}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(p, 0)) for p in ("tests", "failures", "errors", "skipped")] == [51, 0, 0, 2]
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, parent_rom, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (parent_rom, target))
    assert old.keys() == new.keys()
    assert {p for p in old if old[p] != new[p]} == {stage.COMMON}
    assert native.digest(new[stage.COMMON]) == staged["target_COMMON_sha256"]
    arm = new[stage.ARM]
    runtime_guard.verify_runtime(arm, previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    target.replace_file(stage.COMMON, old[stage.COMMON])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    w = stage.workflow
    directory = native.digest(arm[w.DIRECTORY_OFFSET:w.TABLE_OFFSET])
    before, installed = [w.owned_entries(files[stage.COMMON], arm, directory) for files in (old, new)]
    assert {r.message_id for r, q in zip(before, installed, strict=True) if r.text != q.text} == stage.EDITS.keys()
    ja = w.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))
    pending = base.load(stage.PENDING)["records"]
    assert len(pending) == 276
    assert all(r["current_reference"] == w.reference(installed[r["message_ID"]]) and
               r["current_hex"] == installed[r["message_ID"]].text.hex() for r in pending)
    records = staged["records"]
    assert [r["message_ID"] for r in records] == list(range(989, 1020))
    for row in records:
        n = row["message_ID"]
        assert row["source_hex"] == ja[n].text.hex() and row["current_hex"] == before[n].text.hex()
        assert row["staged_hex"] == installed[n].text.hex()
        row["registered_reference"] = w.reference(installed[n]) | dict(candidate_sha256=candidate)
        row["observed_in_lisbon"] = n in observed
    review = {k: staged[k] for k in ("translation_policy", "target_locale", "encoder", "review_gates", "records")}
    review.update(candidate_sha256=candidate, checked_story_format_guard=controls, new_contextual_credit=0,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"], direct_visual_review=viewed,
        observed_gameplay=playback, source_and_native_dependency_proofs=staged["source_proofs"])
    validate_natural_dialogue_batch(review)
    return staged, review, {stage.COMMON: native.digest(new[stage.COMMON])}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
program = checked_text(publish, {
    'len(manifest["batches"]) == 916 and len(manifest["checks"]) == 251':
        'len(manifest["batches"]) == 917 and len(manifest["checks"]) == 252',
    "verified_square_label_wording_predecessor": "verified_departure_warnings_predecessor",
    "departure_warnings": "hostess_conversations",
    "prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=18":
        "prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=27",
    "text_display_revisions=5": "text_display_revisions=4",
    "initialized_Lisbon_crew_warning_and_return=True": "ordinary_Lisbon_tavern_and_return=True",
    "natural_activation=False, hardware=False": "natural_activation=True, hardware=False",
    "previously_localized_records=23": "previously_localized_records=31",
    "Preserve departure warning ROM or reconstruction": "Preserve hostess dialogue ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Tavern hostess dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised hostess replies and preceding cumulative fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Tavern hostess conversations

The 31 source-bound reviews cover introductions, ordinary conversation, special gifts and city-specific replies. Four revised turns preserve Julia’s fado, the younger siblings waiting at home, the calming garden routine and the challenge to keeping women at home. Twenty-seven retentions preserve the individual voices and the three formatter signatures. [Exact review ledger](../{REVIEW.as_posix()})

All 273 name and layout cases were checked through the original formatter. The four revised pages passed native glyph, wrapping, bounds and visual checks. An ordinary Lisbon Tavern replay from an existing save verified Julia’s nameplate, her greeting with Hodram’s name, three full displays of the revised fado reply, and the return to town. The other three revised replies received offline checks. Hardware remains unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

Only four reviewed COMMON slots change. The clean-input patch rebuilds the ROM byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed, with two optional older ROM fixture tests skipped. The dialogue tally remains 27,700 and the 276 open shared entries retain their positions and contents. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = parent.env | globals()
exec(compile(program, __file__ + "::register", "exec"), env)


if __name__ == "__main__":
    env["main"]()
