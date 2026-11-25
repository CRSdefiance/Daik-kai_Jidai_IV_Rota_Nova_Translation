"""Register the source-reviewed forest and desert expeditions."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_overland_passages_replay_20261118 as gameplay
from scripts import register_ruins_clues_and_guides_20261118 as previous
from scripts import verify_overland_passages_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

stage, base, native, parent = display.build, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-overland-passages-v1-20261118"
ROOT = Path("out/overland_passages_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Overland_Passages_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_overland_passages_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_overland_passages_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.paired.ROOT / "supported_qa.xml"
LATER_RETENTIONS = {"DK4_MES_B299_R0399": previous.LIL, "DK4_MES_B267_R0108": previous.MARIA}
replay = SimpleNamespace(ROM=gameplay.replay.ROM, ROOT=gameplay.replay.ROOT,
                         LIVE=gameplay.OUTPUT, SETUP=gameplay.replay.FIXTURE)

feedback = checked_text(
    getsource(previous.verified_gameplay), {
        '[("Push through", 9), ("Look around", 8)]':
            '[("Pull him out yourself", 9), ("Call the others", 9)]',
        ' + [menu["review_sheet"]]': '',
    })
exec(compile(feedback, __file__ + "::verified-holds", "exec"), globals())


def checked_captions(path, block, start, ident, raw, report):
    proof, = [p for p in report["menu_proofs"]
              if (p["current_archive"], p["block"], p["candidate_menu_offset"]) == (path, block, start)]
    assert ident in proof["option_ids"] and base.digest(proof["menu_path"]) == proof["proof_sha256"]
    data = base.load(proof["menu_path"])
    encoded = (data["native_choice_object_hex"] if "native_choice_object_hex" in data
               else data["menus"][0]["target_object_hex"])
    assert encoded == raw.hex()
    return dict(path=proof["menu_path"], sha256=proof["proof_sha256"], id=ident)


bind_start = previous.bind_source.index("                    if word == 0x2100:")
bind_end = previous.bind_source.index("                    else:", bind_start)
bind_source = checked_text(previous.bind_source, {
    previous.bind_source[bind_start:bind_end]:
        """                    if word in stage.stage.MENU:
                        receipt = checked_captions(path, n, start, ident, raw, report)
""",
    'if ident in visited or (word == 0x2100 and group["route"] == 3 and n == 264):':
        'if ident in visited or (word == 0x2100 and group["route"] == 3 and n == 269):',
})
verify_source = checked_text(previous.previous.verify_source, {
    'native_proof["revision_count"] == 78 and native_proof["fresh_page_count"] == 41':
        'native_proof["revision_count"] == 159 and len(native_proof["reused_records"]) == 140 and native_proof["fresh_page_count"] == 22',
    '== 87': '== 171',
    'native_proof["previous_sheets"] + native_proof["contact_sheets"] + shown':
        'menu_sheets(native_proof) + native_proof["previous_sheets"] + native_proof["contact_sheets"] + shown',
    'len(draft["records"]) == 259': 'len(draft["records"]) == 519',
    '{"revision": 78, "retention": 181}': '{"revision": 164, "retention": 355}',
})


def menu_sheets(report):
    return [sheet for menu in report["menu_proofs"] for sheet in menu["review_sheets"]]


publish = previous.publish_source
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
doc = """    DOC.write_text(f\"""# Overland passages

Reviewed 519 records across 16 blocks. The ledger records 164 revisions and 355 justified retentions. Clau, Gerhard and Xien respond differently to the bog rescues. Lil's panic and Camille's response keep the original pace. The Colosseum guide gives the group a warmer lead, and the dancer presents the mosque and its treasure as hearsay. Rafael's three-way dune menu now says Climb the dune, Detour right and Detour left. [Exact review ledger](../{REVIEW.as_posix()})

Native checks covered 145 revised progressive bodies, 14 revised notices, five revised captions and 12 additional custom-name width layouts. The formatter keeps both rescue questions together with long names. The visual pass refined 19 layouts. Actor and style selectors, native substitutions, branch destinations and page limits were checked against the stored ROM. [Final layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Both quicksand choices were observed in the initialized Maria emulator scene. Pull him out yourself led to Maria's own fatigue notice. Call the others led to the crew's fatigue notice. Both returned to the expedition and matched the arrival line. The map gate was skipped in the fixture. Rafael's three-choice menu, other routes and unvisited alternatives received offline checks. Natural activation and hardware remain unverified. [Solo rescue](../{(VERIFY / 'live_pull_1.png').as_posix()}) [Group rescue](../{(VERIFY / 'live_call_1.png').as_posix()})

The clean-input patch reconstructs the exact candidate. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. These records already had credit. The ledger remains at 27,700, with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
\""", encoding="utf-8", newline="\\n")
"""
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: doc,
    'len(manifest["batches"]) == 864 and len(manifest["checks"]) == 199':
        'len(manifest["batches"]) == 865 and len(manifest["checks"]) == 200',
    'display.MENU / "menu_provider_and_planes.json", ': '',
    '    base.save(REVIEW, draft)':
        """    for caption in display_proof["menu_proofs"]:
        folder = VERIFY / ("menu_" + Path(caption["menu_path"]).parent.name)
        folder.mkdir()
        proof = Path(caption["menu_path"])
        copyfile(proof, folder / proof.name)
        assert base.digest(folder / proof.name) == caption["proof_sha256"]
        for sheet in caption["review_sheets"]:
            source = Path(sheet["path"])
            copyfile(source, folder / source.name)
            assert base.digest(folder / source.name) == sheet["sha256"]
    base.save(REVIEW, draft)""",
    "release_stack_before_ruins_clues_and_guides.json": "release_stack_before_overland_passages.json",
    "release_stack_with_ruins_clues_and_guides.json": "release_stack_with_overland_passages.json",
    "verified_jungle_caves_predecessor=predecessor, ruins_clues_and_guides_release=str(REVIEW)":
        "verified_ruins_clues_and_guides_predecessor=predecessor, overland_passages_release=str(REVIEW)",
    "registered_ruins_clues_and_guides_and_complete_parent_inverse":
        "registered_overland_passages_and_complete_parent_inverse",
    "ruins_clues_and_guides_pipeline": "overland_passages_pipeline",
    "prose_revisions=79, justified_retentions=271": "prose_revisions=164, justified_retentions=355",
    "final_phrase_refinements_within_revised_prose=16": "final_phrase_refinements_within_revised_prose=19",
    "initialized_Maria_guide_choices=True": "initialized_Maria_quicksand_choices=True",
    "The ruin clues and map guides are reviewed across all four routes.":
        "The overland forest and desert passages are reviewed across all four routes.",
    'ledger["ruins_clues_and_guides_20261118"]': 'ledger["overland_passages_20261118"]',
    "existing_credit=350": "existing_credit=519",
    "# Ruin clues and map guides test candidate": "# Overland passages test candidate",
    "includes the four ruin investigations and map guides.":
        "includes the revised forest and desert expeditions, landmark tips and treasure clues.",
    "    candidates += [gameplay.prior_stage.ROM, earlier / stage.ROM.name, earlier / replay.ROOT.name / replay.ROM.name]": "    candidates += [earlier / stage.ROM.name, earlier / replay.ROOT.name / replay.ROM.name]",
    "Preserve ruin investigations ROM or replay fixture": "Preserve overland passages ROM or replay fixture",
})
scope = previous.scope | globals()
for source, label in ((bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()



