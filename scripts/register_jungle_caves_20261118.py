"""Register the four cave sequences with their exact clean-input reconstruction."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_jungle_caves_replay_20261118 as gameplay
from scripts import register_london_guild_assignments_20261118 as previous
from scripts import verify_jungle_caves_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, parent = display.build, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-jungle-caves-v1-20261118"
ROOT = Path("out/jungle_caves_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Jungle_And_Caves_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_jungle_caves_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_jungle_caves_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
RAFAEL = Path("releases/all_routes_editorial_20261114_rafael_quest_wraps_candidate/verification/registered_review.json")
LIL = Path("releases/all_routes_editorial_20261114_lil_final_wraps_candidate/verification/registered_review.json")
LATER_RETENTIONS = {"DK4_MES_B301_R0080": RAFAEL, "DK4_MES_B288_R0069": LIL}
replay = SimpleNamespace(ROM=gameplay.replay.ROM, ROOT=gameplay.replay.ROOT,
                         LIVE=gameplay.OUTPUT, SETUP=gameplay.replay.FIXTURE)


def verified_gameplay(live):
    assert live["actual_initialized_Maria"] and not live["natural_activation"] and not live["hardware"]
    assert base.digest(live["native_menu_proof"]) == live["native_menu_proof_sha256"]
    menu = base.load(live["native_menu_proof"])
    assert menu["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    attack, retreat = live["cases"]
    assert [(r["selected_label"], len(r["holds"])) for r in (attack, retreat)] == [("Attack!", 13), ("Run!", 10)]
    for case in (attack, retreat):
        assert all(base.digest(path) == digest for path, digest in case["evidence"].items())
        shots = [h["capture"] for h in case["holds"]] + [case["menu_capture"]]
        assert all(base.digest(shot["path"]) == shot["PNG_sha256"] for shot in shots)
    return [s for c in live["cases"] for s in c["sheets"]] + [menu["review_sheet"]]


bind_source = checked_text(getsource(previous.bind), {
    'visited = {row["id"] for row in live["holds"]}':
        'visited = {r["id"] for case in live["cases"] for r in case["holds"] if r["id"]}',
    'values = stage.paired.text_records(raw, word)': 'values = stage.paired.paired.text_records(raw, word)',
    'if ident in visited:': 'if ident in visited or (word == 0x2100 and group["route"] == 3):',
    ' and initialized Rafael replay': ' and initialized Maria replay',
    'initialized_rafael=live': 'initialized_maria=live | {"sheets": verified_gameplay(live)}',
})
verify_source = getsource(previous.verify)
play_start = verify_source.index('    assert live["initialized_Rafael"]')
play_end = verify_source.index("    assert base.digest(native_proof", play_start)
verify_source = checked_text(verify_source, {
    verify_source[play_start:play_end]:
        """    shown = verified_gameplay(live)
    assert native_proof["revision_count"] == 78 and native_proof["fresh_page_count"] == 41
    assert sum(len(item["pages"]) for r in native_proof["checked_records"] for item in r["layouts"]) == 87
""",
    ' + live["sheets"]': ' + shown',
    'len(draft["records"]) == 151': 'len(draft["records"]) == 259',
    '{"revision": 40, "retention": 111}': '{"revision": 78, "retention": 181}',
})

publish_source = getsource(previous.main)
doc_start = publish_source.index("    DOC.write_text")
doc_end = publish_source.index("    prefix =", doc_start)
doc = """    DOC.write_text(f\"\"\"# Jungle crossings and cave escapes

Reviewed 259 records across SC0 B301, SC1 B291, SC2 B288 and SC3 B259. The ledger records 78 revisions and 181 justified retentions. The crew warnings keep their different registers. The dialogue distinguishes a tiger that isn't following the party from a promise that it won't. Lil's jokes, the childlike objections, and the uncertain injury notices retain their original intent. [Exact review ledger](../{REVIEW.as_posix()})

Every revised record fits on one page. Native checks covered 87 pages including name-width cases, 19 revised style objects and the original aliases. The final phrasing keeps the moss warning together and lets the post-fight pause read as panting. The original speaker controls, menu order, branch destinations and runtime substitutions carry forward. [Final layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Two initialized emulator runs on Maria's sequence checked both options. Attack showed the warning, the change to close combat, and the injury notice. Run showed the immediate retreat reply, followed by the same exit dialogue. The other routes and unvisited crew variants received offline checks. Natural activation and hardware remain unverified. [Attack replay](../{(VERIFY / 'live_attack_2.png').as_posix()}) [Run replay](../{(VERIFY / 'live_run_2.png').as_posix()})

The clean-input patch reconstructs the exact candidate. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. The 259 records already had coverage credit, so the total remains 27,700 with 276 shared keys still open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
"""
publish_source = checked_text(publish_source, {
    publish_source[doc_start:doc_end]: doc,
    "len(manifest[\"batches\"]) == 862 and len(manifest[\"checks\"]) == 197":
        "len(manifest[\"batches\"]) == 863 and len(manifest[\"checks\"]) == 198",
    "replay.LIVE, replay.SETUP, args.visual_review":
        'replay.LIVE, replay.SETUP, gameplay.MENU / "menu_provider_and_planes.json", args.visual_review',
    'draft["initialized_rafael"]["sheets"]': 'draft["initialized_maria"]["sheets"]',
    "release_stack_before_guild_assignments.json": "release_stack_before_jungle_caves.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_jungle_caves.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_london_malacca_guild_assignments_predecessor=predecessor, jungle_caves_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_jungle_caves_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "jungle_caves_pipeline",
    "prose_revisions=40, justified_retentions=111": "prose_revisions=78, justified_retentions=181",
    "final_phrase_refinements_within_revised_prose=6": "final_phrase_refinements_within_revised_prose=38",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Maria_attack_and_run=True",
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "The jungle crossings and cave escapes are reviewed across all four routes.",
    'ledger["london_malacca_guild_assignments_20261118"]': 'ledger["jungle_caves_20261118"]',
    "existing_credit=151": "existing_credit=259",
    "# London and Malacca guild assignments test candidate": "# Jungle crossings and cave escapes test candidate",
    "includes all four reviewed assignments.": "includes the four jungle and cave sequences.",
    "Natural quest activation": "Natural scene activation",
    """    for version in (1, 2, 3):
        folder = stage.ROOT.with_name(f"research_v{version}")
        candidates.append(folder / stage.ROM.name)
        if version >= 2:
            candidates.append(folder / replay.ROOT.name / replay.ROM.name)
""":
        """    earlier = stage.ROOT.with_name("research_v1")
    candidates += [earlier / stage.ROM.name, earlier / replay.ROOT.name / replay.ROM.name]
""",
    "Preserve guild assignment ROM or replay fixture": "Preserve jungle cave ROM or replay fixture",
})
env = vars(previous) | globals()
for text, label in ((bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(text, __file__ + "::" + label, "exec"), env)


if __name__ == "__main__":
    env["main"]()
