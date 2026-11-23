"""Register the Lil and Maria trade exchanges after native and visual review."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_london_guild_assignments_20261118 as precedent
from scripts import stage_late_trade_exchanges_20261118 as stage
from scripts import verify_late_trade_exchanges_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-late-trade-exchanges-v1-20261118"
ROOT = Path("out/late_trade_exchanges_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Late_Trade_Exchanges_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_late_trade_exchanges_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_late_trade_exchanges_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
EARLIER = stage.ROOT.with_name("research_v2")
PHYSICAL = EARLIER / "trade_initialized"
replay = SimpleNamespace(
    ROM=PHYSICAL / "lil/Lil_Trade_Excerpts_RESEARCH_ONLY.nds",
    MARIA_ROM=PHYSICAL / "maria/Maria_Trade_Excerpts_RESEARCH_ONLY.nds",
    SETUP=PHYSICAL / "trade_fixture.json",
    MARIA_SETUP=PHYSICAL / "maria/fixture.json",
    LIVE=stage.ROOT / "trade_replay_bound.json",
)
LATER_RETENTIONS = {
    "DK4_MES_B319_R0030": Path("releases/all_routes_editorial_20261114_lil_final_wraps_candidate/verification/registered_review.json")
}


def bind_replays():
    captured = PHYSICAL / "trade_replay.json"
    live = base.load(captured)
    source = EARLIER / stage.ROM.name
    assert base.digest(source) == live["candidate_sha256"]
    before, after = (base.NdsImage.open(path) for path in (source, stage.ROM))
    assets = (native.ARM, "/GRP/KANJI.FNT", "/COMMON/MESFILE.DK4")
    assert all(before.read_file(path) == after.read_file(path) for path in assets)
    staged = base.load(stage.PROOF)
    assert staged["candidate_sha256"] == base.digest(stage.ROM)
    groups = {(g["route"], g["block"]): g for g in staged["groups"]}
    linked = set()
    for route, host, setup_path, fixture in (
        (2, 22, replay.SETUP, replay.ROM), (3, 33, replay.MARIA_SETUP, replay.MARIA_ROM),
    ):
        setup = base.load(setup_path)
        assert setup["candidate_sha256"] == live["candidate_sha256"]
        assert setup["fixture_sha256"] == base.digest(fixture)
        assert setup["exact_original_commands"] and setup["whole_source_ROM_inverse"]
        archive = f"/data/SC{route}.DK4"
        old_blocks, new_blocks = (native.IlnkContainer.parse(rom.read_file(archive)).blocks for rom in (before, after))
        assert old_blocks[host] == new_blocks[host] and setup["host_sha256"] == native.digest(new_blocks[host])
        for row in setup["selected"]:
            block, ident = row["block"], row["id"]
            group = groups[route, block]
            assert native.digest(new_blocks[block]) == group["after"]
            command = next(c for c in group["commands"] if c["record_ids"] == [ident])
            offset = command["stored_offset"]
            exact = bytes.fromhex(row["stored_command_hex"])
            assert command["stored"] == exact.hex() == new_blocks[block][offset:offset + len(exact)].hex()
            linked.add((route, ident))
    assert linked == {(r["route"], r["id"]) for r in live["holds"]} and len(linked) == 19
    result = live | dict(candidate_sha256=staged["candidate_sha256"], replayed_ROM_sha256=live["candidate_sha256"],
                         same_host_blocks_and_native_assets=True, all_19_commands_exact_in_final=True)
    result["evidence"][str(captured)] = base.digest(captured)
    if replay.LIVE.exists():
        assert base.load(replay.LIVE) == result
    else:
        base.save(replay.LIVE, result)


bind_source = checked_text(getsource(precedent.bind), {
    "stage.paired.text_records": "stage.paired.paired.text_records",
    "initialized Rafael replay": "initialized Lil or Maria replay",
    "initialized_rafael=live": "initialized_trade_excerpts=live",
})
verify_source = checked_text(getsource(precedent.verify), {
    "    stored, native_proof, live, startup =": "    bind_replays()\n    stored, native_proof, live, startup =",
    'live["initialized_Rafael"] and live["exact_original_commands"] and live["actual_Castor_and_Rafael_macro_glyphs"]':
        'live["initialized_Lil_and_Maria"] and live["actual_substitution_and_FE_receipt"] and live["all_19_commands_exact_in_final"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 19',
    'native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18':
        'native_proof["revision_count"] == 42 and native_proof["fresh_page_count"] == 48',
    "== 61": "== 48",
    '    assert base.digest(native_proof["prior_proof"]["path"]) == native_proof["prior_proof"]["sha256"]\n': "",
    'native_proof["previous_sheets"] + native_proof["contact_sheets"]': 'native_proof["contact_sheets"]',
    'len(draft["records"]) == 151': 'len(draft["records"]) == 74',
    '{"revision": 40, "retention": 111}': '{"revision": 42, "retention": 32}',
})
publish = getsource(precedent.main)
pins = publish[publish.index("    for version in (1, 2, 3):"):publish.index("    for path in candidates:")]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index("    base.save(PACKAGE / \"checksums.json\"")]
publish_source = checked_text(publish, {
    'len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197':
        'len(manifest["batches"]) == 872 and len(manifest["checks"]) == 207',
    'display.PROOF, replay.LIVE, replay.SETUP, args.visual_review':
        'display.PROOF, replay.LIVE, replay.SETUP, replay.MARIA_SETUP, args.visual_review',
    'draft["initialized_rafael"]': 'draft["initialized_trade_excerpts"]',
    "release_stack_before_guild_assignments.json": "release_stack_before_late_trade.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_late_trade.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_warrior_village_handovers_predecessor=predecessor, late_trade_exchanges_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_late_trade_exchanges_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "late_trade_exchanges_pipeline",
    "prose_revisions=40, justified_retentions=111": "prose_revisions=42, justified_retentions=32",
    "final_phrase_refinements_within_revised_prose=6": "final_phrase_refinements_within_revised_prose=4",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Lil_and_Maria_trade_excerpts=True",
    'archives[f"/data/SC{i}.DK4"]': 'archives.get(f"/data/SC{i}.DK4", previous[f"target_SC{i}_sha256"])',
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "Lil's Genoa tomato quest and Maria's Sao Jorge supply exchanges are reviewed.",
    "london_malacca_guild_assignments_20261118": "late_trade_exchanges_20261118",
    "existing_credit=151": "existing_credit=74",
    pins: '''    candidates += [replay.MARIA_ROM, stage.ROOT / "clean_rebuilt.nds"]
    for version in (1, 2):
        folder = stage.ROOT.with_name(f"research_v{version}")
        candidates += [folder / stage.ROM.name, folder / "clean_rebuilt.nds"]
''',
    "Preserve guild assignment ROM or replay fixture": "Preserve late-trade ROM or replay fixture",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Late-trade exchanges test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative review through Lil's Genoa tomato quest and Maria's Sao Jorge supply exchanges.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits user acceptance. Natural quest activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Lil and Maria's late trade exchanges

Reviewed 74 records in eight story blocks. Lil pushes back when the trader calls her “little lady.” The Genoa guild exchange preserves her instructions to put a chapel on the ship, assign a missionary and give away trade goods in the square. Maria's requests specify five holds of armor, five of guns and two of cannons. The receipt once again says 77,000 gold coins. The ledger records 42 revisions and gives individual reasons for 32 retentions. [Exact source and candidate references](../{REVIEW.as_posix()})

Native checks and direct visual review covered 48 pages across all 42 revisions, including the speakerless receipt and expanded surname and company names at short and maximum widths. Each revised record fits on one page. The Havana instruction keeps “stop by” together, and the guildmaster's “will you?” stays with his request. The rebuild preserves the original speaker selectors, branches, runtime substitutions and the ASCII right-bound correction. [Final native layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Initialized emulator excerpts matched 19 dialogue holds. Lil's lines displayed “Argot Co.” and “Argot.” Maria's replay displayed her cannon confirmation, the 77,000-gold-coin receipt and the Sao Jorge notice. The final candidate preserves the replayed commands, entry blocks and renderer assets byte for byte. Natural activation, unvisited branches, cargo and payment accounting, and hardware remain unverified. [Lil excerpts](../{(VERIFY / 'lil_live_1.png').as_posix()}) [Maria excerpts](../{(VERIFY / 'maria_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. These 74 records already had coverage credit. The total remains 27,700, with 276 shared keys awaiting review or display classification. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
scope = vars(precedent) | globals()
for code, label in ((bind_source, "exact-records"), (verify_source, "release-gates"), (publish_source, "register")):
    exec(compile(code, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
