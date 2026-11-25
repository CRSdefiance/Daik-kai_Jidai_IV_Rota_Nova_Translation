"""Register Rafael's reviewed item leads, riddle scenes and Proof of Conquest clues."""

from inspect import getsource
from types import SimpleNamespace

from scripts import register_rafael_followup_encounters_20261121 as parent
from scripts import replay_rafael_ruins_and_proof_20261121 as live
from scripts import verify_rafael_ruins_and_proof_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, workflow = display.stage, parent.base, parent.native, parent.workflow
PROFILE = "all-routes-rafael-ruins-and-proof-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_ruins_and_proof_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Ruins_And_Proof_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_ruins_and_proof_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_ruins_and_proof_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
CHECKPOINT = "Reviewed 255 Rafael records across 18 encounters, with 143 wording revisions, four wrap-only fixes and 108 justified retentions."


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


verification = checked_text(getsource(parent.verify), {
    'rendered["FE_panels"] == 7 and sorted(m["count"] for m in rendered["menus"]) == [2, 2, 2]':
        'rendered["FE_panels"] == 22 and sorted(m["count"] for m in rendered["menus"]) == [3, 3, 3, 3]',
    '''    assert len(playback["holds"]) >= 38 and len(playback["menus"]) == 2 and len(playback["exact_sampled_page_turn"]) == 4''':
        '''    assert len(rendered["style_objects"]) == 2
    assert len(playback["holds"]) >= 33 and len(playback["menus"]) == 5 and len(playback["exact_sampled_page_turn"]) == 3''',
    'len(name_check["records"]) == 20': 'len(name_check["records"]) == 18',
    'len(group["commands"]) for group in groups.values()) == 435': 'len(group["commands"]) for group in groups.values()) == 404',
    'startup = parent.startup_check': 'startup = parent.parent.startup_check',
    '== len(draft["records"]) == 261': '== len(draft["records"]) == 255',
    '''        else:
            position, value = 5, raw[5:raw.index(0, 6)]
            assert value[0] == selector''':
        '''        elif command["word"] == 0x4100:
            position = proof["body_offset"] - at
            value = bytes.fromhex(proof["body_hex"])
            assert position >= 20 and raw[position:position+len(value)+1] == value + b"\\0"
            assert proof["style_slots"] == row["native_slots"]
        else:
            position, value = 5, raw[5:raw.index(0, 6)]
            assert value[0] == selector''',
    '{"wording": 159, "wrap": 2, "retention": 100}': '{"wording": 143, "wrap": 4, "retention": 108}',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_gerhard_tutorial_predecessor": "verified_rafael_followup_encounters_predecessor",
    "len(batches) == 1003 and len(checks) == 338": "len(batches) == 1004 and len(checks) == 339",
    "original_command_maps_FE_and_choice_slots_preserved=True": "command_maps_FE_choice_slots_and_actor_style_aliases_preserved=True",
    "previously_localized_records=261, new_contextual_records=0, prose_revisions=159":
        "previously_localized_records=255, new_contextual_records=0, prose_revisions=143",
    "wrap_only_revisions=2, justified_retentions=100": "wrap_only_revisions=4, justified_retentions=108",
    "choice_label_revisions=0": "choice_label_revisions=2",
    "initialized_Rafael_followup_encounters=True": "initialized_Rafael_ruins_and_proof=True",
    "contextual_nameplate_retentions=20": "contextual_nameplate_retentions=18",
    "actual_menu_samples=2": "actual_menu_samples=5, actual_style_objects=2",
    "prior_records_reviewed=261": "prior_records_reviewed=255",
    "prose_revisions=159, justified_retentions=100, wrap_only_revisions=2":
        "prose_revisions=143, justified_retentions=108, wrap_only_revisions=4",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's ruin encounters and Proof of Conquest clues

The [testing ROM](../../{ROM.as_posix()}) includes 18 contextual scene reviews. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_followup_encounters", "rafael_ruins_and_proof").replace(
    "verified_rafael_ruins_and_proof_predecessor", "verified_rafael_followup_encounters_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    '    for path in (ROM, stage.ROM, parent.ROM, earlier / stage.ROM.name, *prior_roms,':
        '''    intermediate = stage.ROOT.with_name("staged_v2")
    for path in (ROM, stage.ROM, parent.ROM, earlier / stage.ROM.name, *prior_roms,
                 intermediate / stage.ROM.name, intermediate / "focused_gameplay/Rafael_Ruins_And_Proof_RESEARCH_ONLY.nds",''',
    "Preserve the Rafael encounters candidate, predecessor, staged ROM and focused fixture":
        "Preserve the Rafael ruins candidate, predecessor, staged ROM and focused fixture",
    notes: '''    DOC.write_text(f"""# Rafael's ruin encounters and Proof of Conquest clues

The review covers 255 records across 18 complete encounters. There are 143 wording revisions, four wrap-only fixes and 108 justified retentions. The full Sphinx riddle, the Colosseum's two starting quantities and the jar puzzle's left-hand instruction and rightward tilt are explicit. Item, place and character names use the registered forms. Eighteen speaker names and role labels were reviewed and retained. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Native checks cover {native_count()} revised pages, all 22 speakerless panels, all 12 captions in four choice menus, and the 14 physical companion lines across two eight-slot objects. Four formerly two-page speeches now fit on one page. The emulator fixture used the exact installed commands to show {observed_count()} speech pages, both companion objects and five highlights across the Colosseum and jar menus. It also verified that Julio's shield rumor and Samwell's cooking joke each advance to the next line in one press. Natural story activation and hardware remain untested. [Native and emulator evidence](../{VERIFY.as_posix()})

The build preserves the original branch destinations, choice slots, shared companion slots and ASCII right-bound correction. Six startup holds, 24 protected name getters, 17 tests and exact clean-input reconstruction passed. These records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_followup_encounters", "rafael_ruins_and_proof")
scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

