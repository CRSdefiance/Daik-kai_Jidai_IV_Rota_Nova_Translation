"""Register the Sakura, forest expedition and Macao dialogues with an exact patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_london_guild_assignments_20261118 as previous
from scripts import replay_sakura_expeditions_macao_20261118 as gameplay
from scripts import verify_sakura_expeditions_macao_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

stage, base, native, parent = display.build, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-sakura-expeditions-macao-v1-20261118"
ROOT = Path("out/sakura_expeditions_macao_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Sakura_Expeditions_Macao_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_sakura_expeditions_macao_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_sakura_expeditions_macao_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
RAFAEL = Path("releases/all_routes_editorial_20261114_rafael_final_wraps_candidate/verification/registered_review.json")
MARIA = Path("releases/all_routes_editorial_20261114_maria_final_wraps_candidate/verification/registered_review.json")
LATER_RETENTIONS = {
    **{f"DK4_MES_B{i}": RAFAEL for i in ("322_R0051", "322_R0068", "325_R0265")},
    **{f"DK4_MES_B{i}": MARIA for i in ("275_R0091", "275_R0128", "277_R0139", "279_R0038")},
}
replay = SimpleNamespace(ROOT=gameplay.ROOT, ROM=gameplay.ROM, SETUP=gameplay.SETUP,
                         LIVE=stage.ROOT/"combined_replay_verification.json")


def bind_replays(store=False):
    rafael, maria = map(base.load, (gameplay.LIVE, gameplay.MACAO.LIVE))
    assert rafael["initialized_Rafael"] and rafael["actual_Rafael_macro_and_speakerless_FE"]
    assert maria["initialized_Maria"] and maria["observed_dialogue_fee_only"]
    for report in (rafael, maria):
        assert report["exact_original_commands"] and not report["natural_activation"] and not report["hardware"]
        assert all(base.digest(path) == sha for path, sha in report["evidence"].items())
        assert all(base.digest(r["capture"]["path"]) == r["capture"]["PNG_sha256"] for r in report["holds"])
    assert len(rafael["holds"]) == 17 and len(maria["holds"]) == 14
    assert rafael["candidate_sha256"] == maria["candidate_sha256"] == base.digest(stage.ROM)
    reports = dict(candidate_sha256=rafael["candidate_sha256"], initialized_Rafael=True,
        initialized_Maria=True, natural_activation=False, hardware=False, exact_original_commands=True,
        actual_Rafael_macro_and_speakerless_FE=True, observed_macao_fee=True,
        holds=rafael["holds"]+maria["holds"], sheets=rafael["sheets"]+maria["sheets"],
        evidence=rafael["evidence"] | maria["evidence"],
        rafael_report=dict(path=str(gameplay.LIVE), sha256=base.digest(gameplay.LIVE)),
        maria_report=dict(path=str(gameplay.MACAO.LIVE), sha256=base.digest(gameplay.MACAO.LIVE)))
    if store:
        assert not replay.LIVE.exists()
        base.save(replay.LIVE, reports)
    return reports


bind_source = checked_text(getsource(previous.bind), {
    'values = stage.paired.text_records(raw, word)': 'values = stage.paired.paired.text_records(raw, word)',
    " and initialized Rafael replay": " and initialized emulator replay",
    "initialized_rafael=live": "initialized_rafael_and_maria=live",
})
verify_source = checked_text(getsource(previous.verify), {
    'live["actual_Castor_and_Rafael_macro_glyphs"]': 'live["actual_Rafael_macro_and_speakerless_FE"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 31',
    'native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18':
        'native_proof["revision_count"] == 129 and native_proof["fresh_page_count"] == 9',
    '== 61': '== 135',
    'len(draft["records"]) == 151': 'len(draft["records"]) == 527',
    '{"revision": 40, "retention": 111}': '{"revision": 129, "retention": 398}',
})

publish = getsource(previous.main)
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
doc = """    DOC.write_text(f\"""# Sakura, forest expeditions and Macao

Reviewed 527 records in 19 blocks across all four routes, with 129 revisions and 398 justified retentions. Sakura's visits retain chintz, sake and the change in who tells the story. The forest choices preserve each route's consequences and the crew's different reactions. The Macao inquiry restores 1,000 gold coins as the fee, keeps the former smuggler distinct from the informant, and preserves Maria's reasoning about the impostor delegation. [Exact review ledger](../{REVIEW.as_posix()})

The native audit checked 122 revised progressive bodies, seven notices and the additional custom-name widths. Lil's illustrated-map rumor and the Ming defense argument now fit on one page each. The visual review refined nine more layouts. The choices, speaker selectors, substitutions, branch destinations and accepted runtime layer passed stored checks. [Final layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Initialized emulator runs covered 17 Rafael excerpts and all 14 Macao inquiry speeches. The captured frames show complete text, the live Rafael substitution, the speakerless notices, and the 1,000-gold-coin fee. The distinct Macao portraits both display Patron. The former smuggler uses selector 102, which also labels the unrelated wine-scene patron on Rafael's route. The source reuses that part, and the dialogue identifies each speaker's role in context. The event ran in an initialized fixture. Normal triggering, the fee's effect on money, unvisited branches and hardware remain unverified. [Rafael sample](../{(VERIFY / 'live_1.png').as_posix()}) [Macao sample](../{(VERIFY / 'macao_live_1.png').as_posix()})

The clean-input patch reconstructs the exact candidate. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. These records already had credit. The ledger remains at 27,700 with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
\""", encoding="utf-8", newline="\\n")
"""
first = publish.index("    for version in (1, 2, 3):")
after = publish.index("    for path in candidates:", first)
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: doc,
    'draft["initialized_rafael"]["sheets"]': 'draft["initialized_rafael_and_maria"]["sheets"]',
    publish[first:after]: "    candidates += [gameplay.MACAO.ROM, display.PRIOR_ROOT / stage.ROM.name]\n",
    'len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197':
        'len(manifest["batches"]) == 868 and len(manifest["checks"]) == 203',
    "    base.save(REVIEW, draft)":
        """    for source in (gameplay.MACAO.LIVE, gameplay.MACAO.FIXTURE):
        folder = VERIFY / "macao_replay"
        folder.mkdir(exist_ok=True)
        copyfile(source, folder / source.name)
        assert base.digest(source) == base.digest(folder / source.name)
    base.save(REVIEW, draft)""",
    "release_stack_before_guild_assignments.json": "release_stack_before_sakura_expeditions_macao.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_sakura_expeditions_macao.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_temple_supply_shipyard_predecessor=predecessor, sakura_expeditions_macao_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_sakura_expeditions_macao_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "sakura_expeditions_macao_pipeline",
    "prose_revisions=40, justified_retentions=111": "prose_revisions=129, justified_retentions=398",
    "final_phrase_refinements_within_revised_prose=6": "final_phrase_refinements_within_revised_prose=9",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Rafael_Sakura_and_Maria_Macao=True",
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "The Sakura visits, forest expeditions and Macao inquiry are reviewed across all four routes.",
    'ledger["london_malacca_guild_assignments_20261118"]': 'ledger["sakura_expeditions_macao_20261118"]',
    "existing_credit=151": "existing_credit=527",
    "# London and Malacca guild assignments test candidate": "# Sakura, forest expeditions and Macao test candidate",
    "includes all four reviewed assignments.": "includes the revised Sakura visits, forest expeditions and Macao inquiry.",
    "Natural quest activation": "Natural scene activation",
    "Preserve guild assignment ROM or replay fixture": "Preserve Sakura, expedition and Macao ROM or replay fixture",
})
scope = vars(previous) | globals()
for source, label in ((bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["main"]()




