"""Register the researched temple, supply and shipyard dialogue over Rafael's successor."""

from pathlib import Path

from scripts import check_temple_supply_shipyard_replay_20261118 as gameplay
from scripts import register_overland_passages_20261118 as previous
from scripts import verify_temple_supply_shipyard_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

stage, base, native, parent = display.build, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-temple-supply-shipyard-v1-20261118"
ROOT = Path("out/temple_supply_shipyard_registered_20261118_v2")
ROM = ROOT / "Translation_DS_All_Routes_Temple_Supply_Shipyard_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_temple_supply_shipyard_candidate_v2")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_temple_supply_shipyard_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
LATER_RETENTIONS = {
    **{f"DK4_MES_B{suffix}": previous.previous.LIL for suffix in
       ("303_R0006", "304_R0051", "305_R0185", "306_R0065", "307_R0026")},
    **{f"DK4_MES_B{suffix}": previous.previous.MARIA for suffix in ("271_R0287", "272_R0089")},
}
replay = gameplay.replay


def checked_captions(path, block, start, ident, raw, report):
    return previous.checked_captions(path, block, start, ident, raw, report)


def observed_scene(stored, live):
    before = base.load(gameplay.stage.PROOF)
    setup = base.load(replay.FIXTURE)
    assert base.digest(gameplay.stage.ROM) == setup["reference_ROM_sha256"]
    assert setup["reference_ROM_sha256"] == live["candidate_sha256"] == before["candidate_sha256"]
    assert setup["original_scene_commands_exact"] and setup["whole_source_ROM_inverse"]
    first, last = map(gameplay.maria_group, (before, stored))
    assert first["after"] == setup["forest_sha256"]
    old_commands, final_commands = [
        [command for command in scene["commands"] if command["source_offset"] in setup["included_source_offsets"]]
        for scene in (first, last)
    ]
    assert len(old_commands) == len(final_commands) == len(setup["included_source_offsets"])
    offset_delta = set()
    for old, new in zip(old_commands, final_commands, strict=True):
        assert (old["word"], old["source_offset"], old["stored"], old.get("target_command_index")) == (
            new["word"], new["source_offset"], new["stored"], new.get("target_command_index"))
        offset_delta.add(new["stored_offset"] - old["stored_offset"])
    assert len(offset_delta) == 1
    old, new = map(base.NdsImage.open, (gameplay.stage.ROM, stage.ROM))
    assert all(old.read_file(path) == new.read_file(path)
               for path in (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT"))
    for image, group in zip((old, new), (first, last), strict=True):
        bank = native.IlnkContainer.parse(image.read_file("/data/SC3.DK4"))
        assert native.digest(bank.blocks[33]) == setup["current_host_sha256"]
        assert native.digest(bank.blocks[274]) == group["after"]
    return dict(replayed_sha256=live["candidate_sha256"], final_sha256=stored["candidate_sha256"],
        original_post_map_gate_commands_byte_exact=len(final_commands), initialized_host_exact=True,
        common_runtime_renderer_assets_exact=True, original_map_gate_not_sampled=True)

def menu_sheets(report):
    return [menu["review_sheet"] for menu in report["menu_proofs"]]


audit = checked_text(previous.feedback, {
    '[("Pull him out yourself", 9), ("Call the others", 9)]':
        '[("Use the compass", len(gameplay.COMPASS)), ("Trust your instincts", len(gameplay.INSTINCT))]',
})
exec(compile(audit, __file__ + "::verified-initialized-navigation", "exec"), globals())

bind_source = checked_text(previous.bind_source, {
    'values = stage.paired.paired.text_records(raw, word)':
        'values = stage.review.paired.original.paired.text_records(raw, word)',
    'and n == 269': 'and n == 274',
})
verify_source = checked_text(previous.verify_source, {
    'assert candidate == live["candidate_sha256"] == startup["candidate_sha256"]':
        'assert candidate == startup["candidate_sha256"]\n    replay_binding = observed_scene(stored, live)',
    'direct_visual_review=sheets': 'direct_visual_review=sheets, representative_scene_rebind=replay_binding',
    'native_proof["revision_count"] == 159 and len(native_proof["reused_records"]) == 140 and native_proof["fresh_page_count"] == 22':
        'native_proof["revision_count"] == 115 and len(native_proof["reused_records"]) + native_proof["fresh_page_count"] == 115',
    '== 171': '== 115',
    'len(draft["records"]) == 519': 'len(draft["records"]) == 351',
    '{"revision": 164, "retention": 355}': '{"revision": 119, "retention": 232}',
})

publish = previous.publish_source
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
doc = """    DOC.write_text(f\"""# Temple, supply and shipyard exchanges

Reviewed 351 records in 19 blocks across Hodram, Lil and Maria. The ledger records 119 revisions and 232 justified retentions. Hodram keeps the warning about the Proof of Conquest distinct from the directions to the clan. Lil's six-line and seven-line map reminders now fit on one page, and the spice dialogue preserves one hold per spice, a single shipment and all nine goods. Maria's shipyard discussion retains the game's account of the carronade and each specialist's role. [Exact review ledger](../{REVIEW.as_posix()})

Native checks covered 111 revised progressive bodies, four notices and four captions. The revised menus read Enter the swamp or Go back for Hodram, and Use the compass or Trust your instincts for Maria. The visual follow-up refined 20 layouts. The stored audit verified the original branches and presentation controls. [Final layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Both navigation choices were observed in an initialized Maria sequence after the map gate. The compass branch shows her comparison with the midday sun. The instinct branch shows a day passing and the new fork. Both reach the discovery line. The replayed commands and runtime are byte-identical in the final ROM. The map gate, other routes and Jam's conditional lines received offline checks. Natural activation and hardware remain unverified. [Compass](../{(VERIFY / 'live_compass_2.png').as_posix()}) [Instinct](../{(VERIFY / 'live_hunch_2.png').as_posix()})

The clean-input patch reconstructs the exact candidate. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. The records already had credit. The ledger remains at 27,700 with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
\""", encoding="utf-8", newline="\\n")
"""
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: doc,
    'len(manifest["batches"]) == 865 and len(manifest["checks"]) == 200':
        'len(manifest["batches"]) == 867 and len(manifest["checks"]) == 202',
    'for sheet in caption["review_sheets"]:': 'for sheet in (caption["review_sheet"],):',
    "release_stack_before_overland_passages.json": "release_stack_before_temple_supply_shipyard.json",
    "release_stack_with_overland_passages.json": "release_stack_with_temple_supply_shipyard.json",
    "verified_ruins_clues_and_guides_predecessor=predecessor, overland_passages_release=str(REVIEW)":
        "verified_rafael_mosque_predecessor=predecessor, temple_supply_shipyard_release=str(REVIEW)",
    "registered_overland_passages_and_complete_parent_inverse":
        "registered_temple_supply_shipyard_and_complete_parent_inverse",
    "overland_passages_pipeline": "temple_supply_shipyard_pipeline",
    "prose_revisions=164, justified_retentions=355": "prose_revisions=119, justified_retentions=232",
    "final_phrase_refinements_within_revised_prose=19": "final_phrase_refinements_within_revised_prose=20",
    "initialized_Maria_quicksand_choices=True": "initialized_Maria_navigation_choices=True",
    '**{f"target_SC{i}_sha256": archives[f"/data/SC{i}.DK4"] for i in range(4)}':
        '**{f"target_SC{i}_sha256": archives.get(f"/data/SC{i}.DK4", previous[f"target_SC{i}_sha256"]) for i in range(4)}',
    "The overland forest and desert passages are reviewed across all four routes.":
        "Hodram's temple, Lil's supplies and Maria's shipyard exchanges are reviewed.",
    'ledger["overland_passages_20261118"]': 'ledger["temple_supply_shipyard_20261118"]',
    "existing_credit=519": "existing_credit=351",
    "# Overland passages test candidate": "# Temple, supply and shipyard test candidate",
    "includes the revised forest and desert expeditions, landmark tips and treasure clues.":
        "includes the revised temple, supply and shipyard exchanges.",
    '    earlier = stage.ROOT.with_name("research_v1")\n': '',
    "    candidates += [earlier / stage.ROM.name, earlier / replay.ROOT.name / replay.ROM.name]": "    candidates += [gameplay.stage.ROM, stage.ROOT.with_name('remaining_three_routes_research_v2') / stage.ROM.name]",
    "Preserve overland passages ROM or replay fixture": "Preserve temple, supply and shipyard ROM or replay fixture",
})
scope = previous.scope | globals() | {"replay": type("Replay", (), {
    "ROM": replay.ROM, "ROOT": replay.ROOT, "LIVE": gameplay.OUTPUT, "SETUP": replay.FIXTURE,
})}
for source, label in ((bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["main"]()






