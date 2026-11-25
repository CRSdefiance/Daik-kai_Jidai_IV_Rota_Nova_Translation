"""Register the warrior trials, villages, fog branches and monk accounts."""

from pathlib import Path
from types import SimpleNamespace

from scripts import check_warrior_village_handovers_replay_20261118 as gameplay
from scripts import register_caves_offshore_monk_20261118 as precedent
from scripts import stage_warrior_village_handovers_20261118 as stage
from scripts import verify_warrior_village_handovers_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-warrior-village-handovers-v1-20261118"
ROOT = Path("out/warrior_village_handovers_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Warrior_Village_Handovers_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_warrior_village_handovers_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_warrior_village_handovers_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
replay = SimpleNamespace(ROM=gameplay.TRIAL_ROM, LIVE=gameplay.LIVE, SETUP=gameplay.TRIAL_SETUP)


def review_path(name, date):
    return Path(f"releases/all_routes_editorial_{date}_{name}_candidate/verification/registered_review.json")


TOWN = review_path("town_quest_exchanges_v2", "20261115")
RAFAEL = review_path("rafael_final_wraps", "20261114")
LIL = review_path("lil_final_wraps", "20261114")
MARIA = review_path("maria_final_wraps", "20261114")
LATER_RETENTIONS = {
    **{f"DK4_MES_B{i}": RAFAEL for i in ("336_R0066", "336_R0109", "341_R0006", "342_R0078", "342_R0118")},
    **{f"DK4_MES_B{i}": TOWN for i in ("339_R0005", "339_R0013", "339_R0030", "340_R0006",
        "320_R0016", "320_R0024", "320_R0028", "321_R0006", "331_R0005", "331_R0024", "331_R0028",
        "332_R0006", "299_R0023", "300_R0005")},
    "DK4_MES_B335_R0089": LIL,
    "DK4_MES_B296_R0123": MARIA,
}

verify_source = checked_text(precedent.verify_source, {
    'live["initialized_Maria"] and live["two_fog_choices_confirmed"] and live["Verisa_entries_sampled_separately"]':
        'live["initialized_Hodram"] and live["both_fog_choices_confirmed"] and live["actual_Rafael_macro_and_speakerless_FE"]',
    'len(live["holds"]) == 13': 'len(live["holds"]) == 37',
    'native_proof["revision_count"] == 158 and native_proof["fresh_page_count"] == 3':
        'native_proof["revision_count"] == 167 and 0 < native_proof["fresh_page_count"] < 170',
    "== 161": "== 170",
    'len(draft["records"]) == 477': 'len(draft["records"]) == 550',
    '{"revision": 159, "retention": 318}': '{"revision": 168, "retention": 382}',
    'for r in draft["records"]) == 11': 'for r in draft["records"]) == 5',
})

publish = precedent.publish_source
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
pins_start = publish.index("    for folder in (gameplay.EARLIER,")
pins_end = publish.index("    for path in candidates:", pins_start)
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: '''    DOC.write_text(f"""# Warrior trials, village handovers and monk accounts

Reviewed 550 source records in 29 story blocks across all four routes. The ledger records 162 prose and notice revisions, five wrap-only fixes, one menu-label revision and 382 justified retentions. The trials use the same three qualities for the title of greatest warrior. Rafael's training keeps the knife, the skill-dependent responses and the named map. The village exchanges preserve the difference between bartering the Sextant and accepting an entrusted object. [Exact review ledger](../{REVIEW.as_posix()})

The monk's story keeps the elder's uncertain account of the alchemy and the drinking water, then lets the conversation turn from Charles's excitement to the monk's death. Maria's guardian encounter preserves Escante's two distinct outcomes and the guardian's reason for trusting her. The speakerless receipts retain all available gold versus 1,000 gold coins for the survey, and specify 65,000 gold coins for the ghost ship and 5,000 for the advance. [Native pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Native checks covered 167 revised dialogue and notice bodies plus both fog menus. The visual pass refined {display_proof['fresh_page_count']} layouts. Initialized emulator playback matched 30 Rafael training panels, including the Tlaloc Knife handover and the named Agility increase. Those exact commands and their host block and assets were preserved in the final build. A fresh Hodram replay confirmed Keep going and Push on anyway through seven dialogue and notice panels. Growth and inventory accounting, natural activation, unvisited branches and hardware remain unverified. [Rafael preview](../{(VERIFY / 'live_4.png').as_posix()}) [Hodram preview](../{(VERIFY / 'hodram_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. These records already had credit. The ledger remains at 27,700 with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
    publish[pins_start:pins_end]: '''    candidates += [gameplay.EARLIER / stage.ROM.name,
                   gameplay.EARLIER / gameplay.game.HODRAM_ROOT.name / gameplay.game.HODRAM_ROM.name,
                   gameplay.game.HODRAM_ROM, stage.ROOT / "clean_rebuilt.nds"]
''',
    'len(manifest["batches"]) == 870 and len(manifest["checks"]) == 205':
        'len(manifest["batches"]) == 871 and len(manifest["checks"]) == 206',
    "release_stack_before_caves_offshore_monk.json": "release_stack_before_warrior_village_handovers.json",
    "release_stack_with_caves_offshore_monk.json": "release_stack_with_warrior_village_handovers.json",
    "verified_desert_censer_predecessor=predecessor, caves_offshore_monk_release=str(REVIEW)":
        "verified_caves_offshore_monk_predecessor=predecessor, warrior_village_handovers_release=str(REVIEW)",
    "registered_caves_offshore_monk_and_complete_parent_inverse":
        "registered_warrior_village_handovers_and_complete_parent_inverse",
    "caves_offshore_monk_pipeline": "warrior_village_handovers_pipeline",
    "prose_revisions=147, wrap_only_revisions=11, choice_label_revisions=1, justified_retentions=318":
        "prose_revisions=162, wrap_only_revisions=5, choice_label_revisions=1, justified_retentions=382",
    "final_phrase_refinements_within_revised_prose=20":
        "final_phrase_refinements_within_revised_prose=display_proof['fresh_page_count']",
    "initialized_Rafael_fog=True, initialized_Maria_Verisa=True":
        "initialized_Rafael_warrior_trial=True, initialized_Hodram_fog=True",
    "The cliff and cave routes, offshore ruins, missing monk rumor and Verisa's exchanges are reviewed.":
        "The warrior trials, village handovers, monk accounts and remaining fog branches are reviewed.",
    'ledger["caves_offshore_monk_20261118"]': 'ledger["warrior_village_handovers_20261118"]',
    "existing_credit=477": "existing_credit=550",
    "# Caves, offshore ruins and missing monk test candidate": "# Warrior trials and village handovers test candidate",
    "includes the reviewed cliff and cave routes, offshore ruins exchanges and missing monk rumor.":
        "includes the reviewed warrior trials, fog decisions, village handovers and monk accounts.",
    "Preserve caves, offshore ruins and monk ROM or replay fixture": "Preserve warrior and village ROM or replay fixture",
})
scope = precedent.scope | globals()
for text, label in ((precedent.bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(text, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
