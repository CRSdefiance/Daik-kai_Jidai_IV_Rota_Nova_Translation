"""Register the revised regional map and Proof dialogue."""

from pathlib import Path
from types import SimpleNamespace

from scripts import register_story_phrase_continuity_20261118 as previous
from scripts import replay_regional_proof_dialogue_20261118 as fixtures
from scripts import stage_regional_proof_dialogue_20261118 as stage
from scripts import verify_regional_proof_dialogue_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-regional-proof-dialogue-v1-20261118"
ROOT = Path("out/regional_proof_dialogue_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Regional_Proof_Dialogue_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_regional_proof_dialogue_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_regional_proof_dialogue_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
EARLIER = stage.ROOT.with_name("research_v1")
replay = SimpleNamespace(**{name: EARLIER / getattr(fixtures, name).relative_to(stage.ROOT)
                           for name in ("LIL_ROM", "MARIA_ROM", "LIL_SETUP", "MARIA_SETUP")},
                         LIVE=stage.ROOT / "replay_bound_to_final.json")


def bind_replays():
    earlier_receipt = EARLIER / fixtures.LIVE.relative_to(stage.ROOT)
    live = base.load(earlier_receipt)
    earlier_rom = EARLIER / stage.ROM.name
    assert live["candidate_sha256"] == base.digest(earlier_rom)
    before, after = (base.NdsImage.open(path) for path in (earlier_rom, stage.ROM))
    old, final = map(native.files, (before, after))
    assert old.keys() == final.keys()
    path = "/data/SC0.DK4"
    assert {name for name in old if old[name] != final[name]} == {path}
    a, b = (native.IlnkContainer.parse(data[path]).blocks for data in (old, final))
    assert [n for n, (left, right) in enumerate(zip(a, b, strict=True)) if left != right] == [160]
    for setup, fixture in ((replay.LIL_SETUP, replay.LIL_ROM), (replay.MARIA_SETUP, replay.MARIA_ROM)):
        receipt = base.load(setup)
        assert receipt["candidate_sha256"] == live["candidate_sha256"]
        assert receipt["whole_source_ROM_inverse"] and receipt["exact_original_commands"]
        assert receipt["fixture_sha256"] == base.digest(fixture)
    result = live | dict(candidate_sha256=base.digest(stage.ROM),
                         observed_on_candidate_sha256=live["candidate_sha256"],
                         replay_dependencies_exact_in_final=True, final_only_modified_story_block="SC0 B160")
    result["evidence"] = live["evidence"] | {str(earlier_receipt): base.digest(earlier_receipt)}
    if replay.LIVE.exists():
        assert base.load(replay.LIVE) == result
    else:
        base.save(replay.LIVE, result)

bind = checked_text(previous.bind_source, {
    "stage.paired.paired.text_records": "stage.paired.text_records",
    "len(retentions) == 4": "len(retentions) == 73",
    "Rafael or Hodram replay": "Lil or Maria replay",
    "Byte-identical retention with fresh native and visual checks":
        "Byte-identical retention with complete native rendering check",
})
verify = checked_text(previous.verify_source, {
    "    stored, native_proof, live, startup =": "    bind_replays()\n    stored, native_proof, live, startup =",
    'live["initialized_Rafael_and_Hodram"] and live["exact_original_commands"] and live["actual_given_name_and_pagination"]':
        'live["initialized_Lil_and_Maria"] and live["exact_original_commands"] and live["actual_given_name_and_exact_quest_title"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 14',
    'native_proof["revision_count"] == 27 and native_proof["fresh_page_count"] == 39 and native_proof["retention_page_count"] == 4':
        'native_proof["revision_count"] == 14 and native_proof["fresh_page_count"] == 20 and len(native_proof["retained_records"]) == 73',
    "== 39": "== 20",
    '{"DK4_MES_B143_R0380": [2, 1]}': '{"DK4_MES_B47_R0140": [1, 1]}',
    'len(draft["records"]) == 31': 'len(draft["records"]) == 87',
    '{"revision": 27, "retention": 4}': '{"revision": 14, "retention": 73}',
    '{"prose": 19, "wrap": 8, "retention": 4}': '{"prose": 14, "retention": 73}',
})
publish = previous.publish_source
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index("    base.save(PACKAGE / \"checksums.json\"")]
main = checked_text(publish, {
    'len(manifest["batches"]) == 874 and len(manifest["checks"]) == 209':
        'len(manifest["batches"]) == 876 and len(manifest["checks"]) == 211',
    "replay.LIVE, replay.SETUP, replay.HODRAM_SETUP, args.visual_review":
        "replay.LIVE, replay.LIL_SETUP, replay.MARIA_SETUP, args.visual_review",
    "release_stack_before_story_phrase_continuity.json": "release_stack_before_regional_proof_dialogue.json",
    "release_stack_with_story_phrase_continuity.json": "release_stack_with_regional_proof_dialogue.json",
    "verified_story_tag_wraps_predecessor": "verified_story_followup_predecessor",
    "story_phrase_continuity_release": "regional_proof_dialogue_release",
    "registered_story_phrase_continuity_and_complete_parent_inverse":
        "registered_regional_proof_dialogue_and_complete_parent_inverse",
    "story_phrase_continuity_pipeline": "regional_proof_dialogue_pipeline",
    "prose_revisions=19, wrap_only_revisions=8, justified_retentions=4":
        "prose_revisions=14, wrap_only_revisions=0, justified_retentions=73",
    "text_display_revisions=27, pagination_fixes=1": "text_display_revisions=14, pagination_fixes=0",
    "initialized_Rafael_and_Hodram_story_excerpts": "initialized_Lil_and_Maria_regional_Proof_excerpts",
    'archives[f"/data/SC{i}.DK4"]': 'archives.get(f"/data/SC{i}.DK4", previous[f"target_SC{i}_sha256"])',
    "Thirty-one phrase-wrap leads are reviewed, including Rafael's sea-battle tutorial.":
        "Regional Proof and map dialogue is reviewed, including Maria's handover after Espinosa.",
    "story_phrase_continuity_20261118": "regional_proof_dialogue_20261118",
    "existing_credit=31": "existing_credit=87",
    'candidates = [ROM, stage.ROM, replay.ROM]\n    candidates += [replay.HODRAM_ROM, stage.ROOT / "clean_rebuilt.nds"]':
        'candidates = [ROM, stage.ROM, replay.LIL_ROM, replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds",\n'
        '                  EARLIER / stage.ROM.name, EARLIER / "clean_rebuilt.nds"]',
    "Preserve phrase-continuity ROM or replay fixture": "Preserve regional Proof dialogue ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Regional Proof dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative work through the regional map and Proof exchanges.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Regional Proof and map dialogue

Reviewed 87 records across nine story blocks. The ledger records 14 wording revisions and 73 justified retentions. The handover after Espinosa uses “Africa's Proof of Conquest” and distinguishes the thing Espinosa had from the Proof he sought. The coin, blade, Bamboo Craft and Patterned Cloth exchanges distinguish each map from its destination. “East Asia's Proof” stays where the next speaker identifies the same item in full. Maria's exchange keeps her refusal to force the villager to give up the Proof, and Xien's warning keeps the danger to the people in view. [Exact review ledger](../{REVIEW.as_posix()})

The original renderer checked all 14 revised pages, six additional name-width examples and the 73 exact retentions. Every revised and name-width page was visually inspected. The original controls, name-catalog routing and name substitutions remain intact. Initialized emulator excerpts matched 14 panels across Lil's and Maria's routes, including Camille addressing Lil, Xien addressing Maria and the corrected Proof title. The final Rafael-only line edit preserves both replayed route archives and their runtime assets byte for byte. The replay used the existing system-only unlock for Maria. Natural activation, inventory effects, quest outcomes and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Lil replay](../{(VERIFY / 'lil_live_1.png').as_posix()}) · [Maria replay](../{(VERIFY / 'maria_live_1.png').as_posix()})

The patch reconstructs the full candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup frames, 24 protected name getters and 32 targeted tests passed. These 87 records already had credit. The ledger remains at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = vars(previous.precedent) | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
