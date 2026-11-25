"""Register the reviewed cliff, caves, offshore ruins and missing monk exchanges."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_caves_offshore_monk_replay_20261118 as gameplay
from scripts import register_london_guild_assignments_20261118 as precedent
from scripts import stage_caves_offshore_monk_20261118 as stage
from scripts import verify_caves_offshore_monk_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-caves-offshore-monk-v1-20261118"
ROOT = Path("out/caves_offshore_monk_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Caves_Offshore_Monk_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_caves_offshore_monk_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_caves_offshore_monk_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
RAFAEL = Path("releases/all_routes_editorial_20261114_rafael_final_wraps_candidate/verification/registered_review.json")
LATER_RETENTIONS = {f"DK4_MES_B{i}": RAFAEL for i in ("332_R0177", "333_R0152", "335_R0009")}
replay = SimpleNamespace(ROM=gameplay.FOG_ROM, LIVE=gameplay.LIVE, SETUP=gameplay.FOG_SETUP)

bind = getsource(precedent.bind)
revision = bind[bind.index('                if row["decision"] == "revision":'):
                bind.index("                else:\n                    assert payload")]
bind_source = checked_text(bind, {
    "stage.paired.text_records": "stage.paired.paired.text_records",
    revision: '''                if row["decision"] == "revision":
                    if word in stage.stage.MENU:
                        selection, = (m for m in live["menus"] if ident in m["native_receipt"]["option_ids"]
                                      and m["selected"] == row["english"])
                        manifest = selection["native_receipt"]
                        path_ref = manifest["menu_path"]
                        proof = base.load(path_ref)
                        assert raw.hex() == proof["native_choice_object_hex"]
                        assert proof["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
                        assert body.decode("ascii") == row["english"]
                        assert base.digest(path_ref) == manifest["proof_sha256"]
                        visited.add(ident)
                        scope = "Native typed choice, complete glyphs and direct visual check"
                        receipt = dict(path=path_ref, sha256=manifest["proof_sha256"], id=ident)
                    else:
                        proof = revised[path, ident]
                        expected = bytes([selector]) + body
                        assert expected.hex() == proof.get("stored_hex", proof.get("target_hex"))
                        scope = "Native renderer and direct visual check"
                        receipt = dict(path=str(display.PROOF), sha256=base.digest(display.PROOF), id=ident)
''',
    " and initialized Rafael replay": " and initialized emulator replay",
    "initialized_rafael=live": "initialized_story_replays=live",
})
verify_source = checked_text(getsource(precedent.verify), {
    'live["actual_Castor_and_Rafael_macro_glyphs"]':
        'live["initialized_Maria"] and live["two_fog_choices_confirmed"] and live["Verisa_entries_sampled_separately"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 13',
    '    assert native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18':
        '''    assert [m["selected"] for m in live["menus"]] == ["Keep going", "Push on anyway"]
    assert all(base.digest(m["capture"]["path"]) == m["capture"]["PNG_sha256"] for m in live["menus"])
    assert native_proof["revision_count"] == 158 and native_proof["fresh_page_count"] == 3''',
    "== 61": "== 161",
    'len(draft["records"]) == 151': 'len(draft["records"]) == 477',
    '{"revision": 40, "retention": 111}': '{"revision": 159, "retention": 318}',
    "    draft.update(approved_source25=":
        '''    assert sum(r.get("wrap_only", False) for r in draft["records"]) == 11
    assert sum(r["decision"] == "revision" and r["kind"] == "typed-choice-label" for r in draft["records"]) == 1
    draft.update(approved_source25=''',
})

publish = getsource(precedent.main)
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
pins_start = publish.index("    for version in (1, 2, 3):")
pins_end = publish.index("    for path in candidates:", pins_start)
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: '''    DOC.write_text(f"""# Cliff and cave routes, offshore ruins and the missing monk

Reviewed 477 source records in 14 blocks across all four routes. The ledger records 147 prose revisions, 11 wrap-only fixes, one choice-label revision and 318 justified retentions. Rafael's cliff joke still draws a skeptical reply. The snake and bat branches retain their different consequences, and the boat crossing preserves the guide's request to keep the ruins' location from the sailors. Hodram's reunion now echoes what the guide actually says about asking everyone who looks strong enough. [Exact review ledger](../{REVIEW.as_posix()})

Native checks covered 158 revised dialogue and notice bodies, a full set of name-width cases, and both fog menus. The visual pass refined 20 revised layouts. Verisa's warning now uses the available first line and the guide's request keeps the map to the ruins together. The earlier fog choice remains Keep going. The dead-end choice now reads Push on anyway. [Final crossing dialogue](../{(VERIFY / 'before_after_1.png').as_posix()}) [Both native menu captions](../{(VERIFY / 'fog_1984_captions.png').as_posix()})

Initialized gameplay confirmed both fog selections, five dialogue holds and Rafael's arrival response. Separate initialized replays checked all eight dialogue holds from Verisa's two original entry points on Maria's route. Verisa addresses Maria in the opening. The later replies show Rafael Castor with the fixed source selector. The final build reuses these observations where the tested commands and native dependencies are byte-identical. Natural event activation, the unselected branches and hardware remain unverified. [Rafael fog replay](../{(VERIFY / 'fog_live_1.png').as_posix()}) [Verisa's opening](../{(VERIFY / 'verisa_live_1.png').as_posix()}) [Verisa and Rafael](../{(VERIFY / 'reply_live_1.png').as_posix()})

The clean-input patch reconstructs the exact candidate. It carries all 114 accepted layers and the ASCII right-bound correction. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. These records already had coverage credit. The ledger remains at 27,700 with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
    publish[pins_start:pins_end]: '''    for folder in (gameplay.EARLIER, gameplay.REPLY_STAGE, display.PRIOR_ROOT, stage.ROOT):
        candidates.append(folder / stage.ROM.name)
        if (folder / "clean_rebuilt.nds").is_file():
            candidates.append(folder / "clean_rebuilt.nds")
    candidates += [gameplay.VERISA_CASES[0][1], gameplay.VERISA_CASES[1][1]]
''',
    'len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197':
        'len(manifest["batches"]) == 870 and len(manifest["checks"]) == 205',
    'draft["initialized_rafael"]["sheets"]': 'draft["initialized_story_replays"]["sheets"]',
    '        dest = VERIFY / Path(sheet["path"]).name':
        '''        origin = Path(sheet["path"])
        name = f"fog_{origin.parent.name}_captions.png" if origin.name == "native_caption_review.png" else origin.name
        dest = VERIFY / name''',
    "release_stack_before_guild_assignments.json": "release_stack_before_caves_offshore_monk.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_caves_offshore_monk.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_desert_censer_predecessor=predecessor, caves_offshore_monk_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_caves_offshore_monk_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "caves_offshore_monk_pipeline",
    "prose_revisions=40, justified_retentions=111":
        "prose_revisions=147, wrap_only_revisions=11, choice_label_revisions=1, justified_retentions=318",
    "final_phrase_refinements_within_revised_prose=6": "final_phrase_refinements_within_revised_prose=20",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Rafael_fog=True, initialized_Maria_Verisa=True",
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "The cliff and cave routes, offshore ruins, missing monk rumor and Verisa's exchanges are reviewed.",
    'ledger["london_malacca_guild_assignments_20261118"]': 'ledger["caves_offshore_monk_20261118"]',
    "existing_credit=151": "existing_credit=477",
    "# London and Malacca guild assignments test candidate": "# Caves, offshore ruins and missing monk test candidate",
    "includes all four reviewed assignments.":
        "includes the reviewed cliff and cave routes, offshore ruins exchanges and missing monk rumor.",
    "Natural quest activation": "Natural event activation",
    "Preserve guild assignment ROM or replay fixture": "Preserve caves, offshore ruins and monk ROM or replay fixture",
})
scope = vars(precedent) | globals()
for text, label in ((bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(text, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
