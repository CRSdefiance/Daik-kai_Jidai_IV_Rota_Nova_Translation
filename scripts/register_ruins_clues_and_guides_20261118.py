"""Register the ruin investigations with reviewed captions, cargo and story text."""

from pathlib import Path
from types import SimpleNamespace

from scripts import check_ruins_clues_and_guides_replay_20261118 as gameplay
from scripts import register_jungle_caves_20261118 as previous
from scripts import verify_ruins_clues_and_guides_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, parent = display.build, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-ruins-clues-and-guides-v1-20261118"
ROOT = Path("out/ruins_clues_and_guides_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Ruins_Clues_And_Guides_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_ruins_clues_and_guides_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_ruins_clues_and_guides_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
RAFAEL, LIL = previous.RAFAEL, previous.LIL
MARIA = Path("releases/all_routes_editorial_20261114_maria_final_wraps_candidate/verification/registered_review.json")
LATER_RETENTIONS = {"DK4_MES_B302_R0020": RAFAEL, "DK4_MES_B305_R0069": RAFAEL, "DK4_MES_B305_R0097": RAFAEL,
    "DK4_MES_B290_R0061": LIL, "DK4_MES_B291_R0062": LIL, "DK4_MES_B260_R0004": MARIA, "DK4_MES_B261_R0067": MARIA}
replay = SimpleNamespace(ROM=gameplay.prior_replay.ROM, ROOT=gameplay.prior_replay.ROOT,
                         LIVE=gameplay.OUTPUT, SETUP=gameplay.prior_replay.FIXTURE)


def observed_scene(stored, live):
    previous_stage = base.load(gameplay.prior_stage.PROOF)
    setup = base.load(replay.SETUP)
    assert base.digest(gameplay.prior_stage.ROM) == setup["reference_ROM_sha256"]
    assert setup["reference_ROM_sha256"] == live["candidate_sha256"] == previous_stage["candidate_sha256"]
    assert setup["original_scene_commands_exact"] and setup["whole_source_ROM_inverse"]
    groups = [next(g for g in receipt["groups"] if (g["route"], g["block"]) == (3, 264))
              for receipt in (previous_stage, stored)]
    before, after = [[c for c in g["commands"] if c["source_offset"] in setup["included_source_offsets"]]
                     for g in groups]
    assert groups[0]["after"] == setup["forest_sha256"]
    assert len(before) == len(after) == len(setup["included_source_offsets"])
    for a, b in zip(before, after, strict=True):
        assert (a["word"], a["source_offset"], a["stored"], a.get("target_command_index")) == (
            b["word"], b["source_offset"], b["stored"], b.get("target_command_index"))
    assert len({b["stored_offset"] - a["stored_offset"] for a, b in zip(before, after, strict=True)}) == 1
    old, new = map(base.NdsImage.open, (gameplay.prior_stage.ROM, stage.ROM))
    asset_paths = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(old.read_file(path) == new.read_file(path) for path in asset_paths)
    for image, group in zip((old, new), groups, strict=True):
        bank = native.IlnkContainer.parse(image.read_file("/data/SC3.DK4"))
        assert native.digest(bank.blocks[33]) == setup["current_host_sha256"]
        assert native.digest(bank.blocks[264]) == group["after"]
    return dict(replayed_sha256=live["candidate_sha256"], final_sha256=stored["candidate_sha256"],
        original_post_map_gate_commands_byte_exact=len(after), initialized_host_exact=True,
        common_runtime_renderer_assets_exact=True, original_map_gate_not_sampled=True)


def verified_gameplay(live):
    assert live["actual_initialized_Maria"] and not live["natural_activation"] and not live["hardware"]
    assert base.digest(live["native_menu_proof"]) == live["native_menu_proof_sha256"]
    menu = base.load(live["native_menu_proof"])
    assert menu["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    assert [(r["selected_label"], len(r["holds"])) for r in live["cases"]] == [("Push through", 9), ("Look around", 8)]
    for case in live["cases"]:
        assert all(base.digest(path) == digest for path, digest in case["evidence"].items())
        shots = [h["capture"] for h in case["holds"]] + [case["menu_capture"]]
        assert all(base.digest(shot["path"]) == shot["PNG_sha256"] for shot in shots)
    return [s for c in live["cases"] for s in c["sheets"]] + [menu["review_sheet"]]


bind_start = previous.bind_source.index('                if row["decision"] == "revision":')
bind_end = previous.bind_source.index('                else:', bind_start)
bind_source = checked_text(previous.bind_source, {
    previous.bind_source[bind_start:bind_end]:
        """                if row["decision"] == "revision":
                    scope = "Native renderer and direct visual check"
                    if word == 0x2100:
                        proof, = report["menu_proofs"]
                        assert ident in proof["option_ids"] and start == proof["candidate_menu_offset"]
                        assert base.digest(proof["menu_path"]) == proof["proof_sha256"]
                        assert base.load(proof["menu_path"])["native_choice_object_hex"] == raw.hex()
                        receipt = dict(path=proof["menu_path"], sha256=proof["proof_sha256"], id=ident)
                    else:
                        proof = revised[path, ident]
                        expected = bytes([selector]) + body
                        assert expected.hex() == proof.get("stored_hex", proof.get("target_hex"))
                        receipt = dict(path=str(display.PROOF), sha256=base.digest(display.PROOF), id=ident)
""",
    'if ident in visited or (word == 0x2100 and group["route"] == 3):':
        'if ident in visited or (word == 0x2100 and group["route"] == 3 and n == 264):',
})
verify_source = checked_text(previous.verify_source, {
    'assert candidate == live["candidate_sha256"] == startup["candidate_sha256"]':
        'assert candidate == startup["candidate_sha256"]\n    replay_binding = observed_scene(stored, live)',
    'native_proof["revision_count"] == 78 and native_proof["fresh_page_count"] == 41':
        'native_proof["revision_count"] == 77 and native_proof["fresh_page_count"] == 16',
    '== 87': '== 86',
    'len(draft["records"]) == 259': 'len(draft["records"]) == 350',
    '{"revision": 78, "retention": 181}': '{"revision": 79, "retention": 271}',
    "direct_visual_review=sheets": "direct_visual_review=sheets, representative_scene_rebind=replay_binding",
})
publish = previous.publish_source
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
doc = """    DOC.write_text(f\"\"\"# Ruin clues and map guides

Reviewed 350 records in 20 blocks across the four routes. The ledger records 79 revisions and 271 retentions. Rafael's guide keeps the map requirement clear. Lil's Angkor conversations retain the inscription's exact clue. Hodram's search keeps the testimony and the quest conditions distinct. Maria's two rewards specify gold, and the dead-end menu now says Push through or Look around. [Exact review ledger](../{REVIEW.as_posix()})

Native checks covered 69 revised progressive pages, eight speakerless notices, both captions and nine additional name-width examples. The final layouts keep the Angkor speech's closing phrase together and avoid an extra blank row on the Malacca notice. Original branch destinations, style aliases and runtime substitutions carry forward. [Final layout pages](../{(VERIFY / 'before_after_2.png').as_posix()})

Two initialized emulator runs showed Maria's dead-end menu. Push through led to the notice about missing sailors. Look around uncovered the path. Both led to the same arrival line. The final ROM preserves the replayed commands and runtime assets byte for byte. The earlier map gate, the other routes and unvisited variants received offline checks. Natural activation and hardware remain unverified. [Push through](../{(VERIFY / 'live_push_2.png').as_posix()}) [Look around](../{(VERIFY / 'live_look_1.png').as_posix()})

The clean-input patch reconstructs the exact candidate. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. The 350 records already had credit, so the total remains 27,700 with 276 shared keys still open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
"""
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: doc,
    'len(manifest["batches"]) == 863 and len(manifest["checks"]) == 198':
        'len(manifest["batches"]) == 864 and len(manifest["checks"]) == 199',
    "gameplay.MENU / \"menu_provider_and_planes.json\"": "display.MENU / \"menu_provider_and_planes.json\"",
    "release_stack_before_jungle_caves.json": "release_stack_before_ruins_clues_and_guides.json",
    "release_stack_with_jungle_caves.json": "release_stack_with_ruins_clues_and_guides.json",
    "verified_london_malacca_guild_assignments_predecessor=predecessor, jungle_caves_release=str(REVIEW)":
        "verified_jungle_caves_predecessor=predecessor, ruins_clues_and_guides_release=str(REVIEW)",
    "registered_jungle_caves_and_complete_parent_inverse": "registered_ruins_clues_and_guides_and_complete_parent_inverse",
    "jungle_caves_pipeline": "ruins_clues_and_guides_pipeline",
    "prose_revisions=78, justified_retentions=181": "prose_revisions=79, justified_retentions=271",
    "final_phrase_refinements_within_revised_prose=38": "final_phrase_refinements_within_revised_prose=16",
    "initialized_Maria_attack_and_run=True": "initialized_Maria_guide_choices=True",
    "The jungle crossings and cave escapes are reviewed across all four routes.":
        "The ruin clues and map guides are reviewed across all four routes.",
    'ledger["jungle_caves_20261118"]': 'ledger["ruins_clues_and_guides_20261118"]',
    "existing_credit=259": "existing_credit=350",
    "# Jungle crossings and cave escapes test candidate": "# Ruin clues and map guides test candidate",
    "includes the four jungle and cave sequences.": "includes the four ruin investigations and map guides.",
    "    candidates += [earlier / stage.ROM.name, earlier / replay.ROOT.name / replay.ROM.name]":
        "    candidates += [gameplay.prior_stage.ROM, earlier / stage.ROM.name, earlier / replay.ROOT.name / replay.ROM.name]",
    "Preserve jungle cave ROM or replay fixture": "Preserve ruin investigations ROM or replay fixture",
})
scope = previous.env | globals()
for text, label in ((bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(text, __file__ + "::" + label, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
