"""Register the reviewed desert and incense burner exchanges with an exact clean patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_maria_desert_20261118 as maria
from scripts import register_london_guild_assignments_20261118 as precedent
from scripts import replay_desert_censer_20261118 as rafael
from scripts import stage_desert_censer_20261118 as stage
from scripts import verify_desert_censer_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-desert-censer-v1-20261118"
ROOT = Path("out/desert_censer_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Desert_Censer_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_desert_censer_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_desert_censer_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
RAFAEL_ROOT = display.PRIOR_ROOT / rafael.ROOT.name
replay = SimpleNamespace(ROM=RAFAEL_ROOT / rafael.ROM.name, SETUP=RAFAEL_ROOT / rafael.SETUP.name,
                         LIVE=stage.ROOT / "combined_replay_verification.json")

LATER_RETENTIONS = {
    ident: Path(f"releases/all_routes_editorial_20261114_{route}_final_wraps_candidate"
                "/verification/registered_review.json")
    for ident, route in (
        ("DK4_MES_B330_R0037", "rafael"),
        ("DK4_MES_B314_R0014", "hodram"),
        ("DK4_MES_B316_R0065", "lil"),
    )
}

def bind_replays():
    earlier_replay = RAFAEL_ROOT / rafael.LIVE.name
    first, second = map(base.load, (earlier_replay, maria.OUTPUT))
    old, new = (base.NdsImage.open(path) for path in (display.PRIOR_ROOT / stage.ROM.name, stage.ROM))
    setup = base.load(replay.SETUP)
    earlier = display.PRIOR_ROOT / stage.ROM.name
    assert setup["candidate_sha256"] == first["candidate_sha256"] == base.digest(earlier)
    assert setup["fixture_sha256"] == first["fixture_sha256"] == base.digest(replay.ROM)
    assert second["candidate_sha256"] == base.digest(stage.ROM)
    dependencies = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(old.read_file(path) == new.read_file(path) for path in dependencies)
    file_path = "/data/SC0.DK4"
    before, after = (native.IlnkContainer.parse(rom.read_file(file_path)).blocks for rom in (old, new))
    assert native.digest(before[44][:40]) == native.digest(after[44][:40]) == setup["original_prefix_sha256"]
    staged = base.load(stage.PROOF)
    assert staged["candidate_sha256"] == second["candidate_sha256"]
    expected = {r["id"]: r for r in setup["selected"]}
    verified = set()
    for group in staged["groups"]:
        if group["file_path"] != file_path:
            continue
        block = group["block"]
        for command in group["commands"]:
            for ident in command["record_ids"]:
                if ident not in expected:
                    continue
                original = expected[ident]
                raw = bytes.fromhex(command["stored"])
                position = command["stored_offset"]
                assert original["block"] == block and command["word"] == 0x4000
                assert original["stored_command_hex"] == command["stored"] == after[block][position:position + len(raw)].hex()
                verified.add(ident)
    assert verified == expected.keys() and len(verified) == 19
    assert second["actual_initialized_Maria"] and second["selected_label"] == "Fight"
    assert len(first["holds"]) == 19 and len(second["holds"]) == 9
    assert not second["natural_activation"] and not second["hardware"]
    assert base.digest(second["native_menu_proof"]) == second["native_menu_proof_sha256"]
    menu = base.load(second["native_menu_proof"])
    assert base.digest(second["menu_capture"]["path"]) == second["menu_capture"]["PNG_sha256"]
    assert menu["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    assert all(base.digest(path) == digest for path, digest in second["evidence"].items())
    result = first | dict(
        candidate_sha256=second["candidate_sha256"],
        initialized_Maria=True,
        Maria_selected_label="Fight",
        holds=first["holds"] + second["holds"],
        sheets=first["sheets"] + second["sheets"] + menu["review_sheets"],
        evidence=first["evidence"] | second["evidence"] | {
            str(earlier_replay): base.digest(earlier_replay),
            str(maria.OUTPUT): base.digest(maria.OUTPUT),
            second["native_menu_proof"]: second["native_menu_proof_sha256"],
        },
        Rafael_replay_source_sha256=first["candidate_sha256"],
        Rafael_replay_exact_command_and_asset_reuse=dict(source_records=sorted(verified),
                                                       assets=list(dependencies), same_host_prefix=True),
    )
    assert not replay.LIVE.exists()
    base.save(replay.LIVE, result)


bind_source = checked_text(getsource(precedent.bind), {
    "stage.paired.text_records": "stage.paired.paired.text_records",
    'scope += " and initialized Rafael replay"': 'scope += " and initialized emulator replay"',
})
verify_source = checked_text(getsource(precedent.verify), {
    'live["actual_Castor_and_Rafael_macro_glyphs"]': 'live["actual_Rafael_macro_and_speakerless_FE"] and live["initialized_Maria"]',
    'len(live["holds"]) == 16': 'len(live["holds"]) == 28',
    'native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18':
        'native_proof["revision_count"] == 142 and 0 < native_proof["fresh_page_count"] < 154',
    '== 61': '== 154',
    'len(draft["records"]) == 151': 'len(draft["records"]) == 511',
    '{"revision": 40, "retention": 111}': '{"revision": 142, "retention": 369}',
})

publish = getsource(precedent.main)
doc_start = publish.index("    DOC.write_text")
doc_end = publish.index("    prefix =", doc_start)
pins_start = publish.index("    for version in (1, 2, 3):")
pins_end = publish.index("    for path in candidates:", pins_start)
publish_source = checked_text(publish, {
    publish[doc_start:doc_end]: '''    DOC.write_text(f"""# Desert encounters and the Goryeo Incense Burner

Reviewed 511 records in 16 story blocks across all four routes. The 142 revisions restore the celadon material in Rafael's exchange and keep the separate East Asia clue on Hodram's and Lil's routes. The desert scenes distinguish fighting, scaring the scorpions off and running. Lil's cactus scare and Maria's wolf encounter keep their different reactions and consequences. The ledger gives individual reasons for 369 retentions. [Exact review ledger](../{REVIEW.as_posix()})

Native checks covered every changed record, including five speakerless notices and four given-name substitutions tested at extra widths. Maria's long reminders about the map guardians now fit on one page and keep their short question tags with the preceding words. Visual review refined {len(display_proof['checked_records']) - len(display_proof['reused_records'])} layouts, including the cactus spine and the whispered instructions. The original choice labels, branch destinations, speaker controls and page transitions retain their native bindings. [Final layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

Rafael's initialized replay matched 19 original dialogue holds, including his name in the celadon exchange and injury notice, and the two separately advanced pauses in the fortune-teller's reading. The final revision preserves the 19 commands, the fixture's host prefix, the renderer and its assets byte for byte. Verisa remains the localized personal name for source actor 204, ヴェリーサ, and her full nameplate renders in the replay. Maria's replay of the final revisions matched nine dialogue holds and all three menu labels, with Fight selected through the response and arrival line. The map gate, natural event activation, unvisited alternatives and hardware remain unverified. [Rafael replay](../{(VERIFY / 'live_1.png').as_posix()}) [Maria replay](../{(VERIFY / 'live_fight_1.png').as_posix()}) [Verisa's exact name fields](../translations/rafael_B321_B342_scoped_names_final_v1.json)

The clean-input patch reconstructs the exact candidate. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. These records already had coverage credit. The total remains 27,700 with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
    publish[pins_start:pins_end]: """    candidates += [maria.game.ROM, stage.ROOT / "clean_rebuilt.nds",
                   display.PRIOR_ROOT / stage.ROM.name,
                   display.PRIOR_ROOT / "clean_rebuilt.nds",
                   display.PRIOR_ROOT / "censer" / rafael.ROM.name,
                   display.PRIOR_ROOT / maria.game.ROOT.name / maria.game.ROM.name]
""",
    'len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197':
        'len(manifest["batches"]) == 869 and len(manifest["checks"]) == 204',
    "release_stack_before_guild_assignments.json": "release_stack_before_desert_censer.json",
    "release_stack_with_guild_assignments.json": "release_stack_with_desert_censer.json",
    "verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW)":
        "verified_sakura_expeditions_macao_predecessor=predecessor, desert_censer_release=str(REVIEW)",
    "registered_london_malacca_guild_assignments_and_complete_parent_inverse":
        "registered_desert_censer_and_complete_parent_inverse",
    "london_malacca_guild_assignments_pipeline": "desert_censer_pipeline",
    "prose_revisions=40, justified_retentions=111": "prose_revisions=142, justified_retentions=369",
    "final_phrase_refinements_within_revised_prose=6":
        "final_phrase_refinements_within_revised_prose=len(display_proof['checked_records']) - len(display_proof['reused_records'])",
    "initialized_Rafael_guild_and_riddle=True": "initialized_Rafael_censer_and_injury=True, initialized_Maria_Fight=True",
    "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed.":
        "The desert encounters, Goryeo Incense Burner and Maria's map exchanges are reviewed across all four routes.",
    'ledger["london_malacca_guild_assignments_20261118"]': 'ledger["desert_censer_20261118"]',
    "existing_credit=151": "existing_credit=511",
    "# London and Malacca guild assignments test candidate": "# Desert and incense burner test candidate",
    "includes all four reviewed assignments.": "includes the reviewed desert encounters and incense burner exchanges.",
    "Natural quest activation": "Natural event activation",
    "Preserve guild assignment ROM or replay fixture": "Preserve desert and censer ROM or replay fixture",
})
scope = vars(precedent) | globals()
for text, label in ((bind_source, "bound-ledger"), (verify_source, "checked-release"), (publish_source, "register")):
    exec(compile(text, __file__ + "::" + label, "exec"), scope)

if __name__ == "__main__":
    if not replay.LIVE.exists():
        bind_replays()
    scope["main"]()
