"""Register Hodram's farewell, retirement and recruitment scenes."""

from types import FunctionType, SimpleNamespace

from scripts import register_hodram_B131_B150_20261122 as parent
from scripts import replay_hodram_B151_B160_20261122 as live
from scripts import verify_hodram_B151_B160_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B151-B160-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B151_B160_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B151_B160_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B151_B160_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B151_B160_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Revisited 331 Hodram records through the farewell, retirement and four recruitment scenes. "
              "The pass revises 112 turns and records 219 justified retentions. Carlo's explanation and "
              "Julio's trade advice use the available width and each now fits on one page.")
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = FunctionType(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})


def historical_credit(draft):
    assert all(row["kind"] in {"progressive", "system-FE"} for row in draft["records"])
    assert all(row["id"].startswith("DK4_MES_B") for row in draft["records"])
    return {"by_census_id": {}, "direct_keys": len(draft["records"])}


start = parent.verification.index('    assert rendered["FE_panels"]')
end = parent.verification.index('    assert playback["initialized_excerpts"]')
glyph = parent.verification[parent.verification.index("    glyphs ="):
                            parent.verification.index('    draft["historical_source_credit"]')]
verification = checked_text(parent.verification, {
    parent.verification[start:end]: '''    assert rendered["FE_panels"] == 25 and not rendered["menus"] and not rendered["style_objects"]
    assert rendered["revised_speech_pages"] == 112 and rendered["alternate_name_width_pages"] == 6
    assert draft["contextual_records_revisited"] == 331 and draft["contextual_decisions_reused"] == 0
    assert len(playback["holds"]) == 65 and not playback["menus"] and not playback["observed_style_owners"]
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.CARLO_TURN[0]}
    assert all(any(p["id"] == ident and p["current_pages"] == 1 for p in rendered["pagination_changes"])
               for ident in ("DK4_MES_B158_R0195", "DK4_MES_B160_R0230"))
''',
    'len(name_check["records"]) == 17': 'len(name_check["records"]) == 27',
    'len(group["commands"]) for group in groups.values()) == 650': 'len(group["commands"]) for group in groups.values()) == 568',
    '== len(draft["records"]) == 350': '== len(draft["records"]) == 331',
    '{"wording": 110, "wrap-only": 1, "glyph": 3, "retention": 236}': '{"wording": 112, "retention": 219}',
    glyph: '''    farewell = [row for row in draft["records"]
                if row["block"] == 156 and row["source_selector"] == 254 and row["decision"] == "revision"]
    assert len(farewell) == 4 and all("before" in draft["planned_FE"][row["id"]] for row in farewell)
    draft["staged_farewell_position_revisions"] = [row["id"] for row in farewell]
''',
    'bind_historical_credit(draft)': 'historical_credit(draft)',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1026 and len(checks) == 361': 'len(batches) == 1027 and len(checks) == 362',
    'previously_localized_records=350': 'previously_localized_records=331',
    'contextual_records_revisited=350': 'contextual_records_revisited=331',
    'prior_records_reviewed=350': 'prior_records_reviewed=331',
    'prose_revisions=110': 'prose_revisions=112',
    'justified_retentions=236': 'justified_retentions=219',
    'text_display_revisions=3': 'text_display_revisions=0',
    'punctuation_glyph_corrections=3': 'punctuation_glyph_corrections=0',
    'wrap_only_revisions=1': 'wrap_only_revisions=0',
    'contextual_nameplate_retentions=17': 'contextual_nameplate_retentions=27',
    'actual_menu_samples=10': 'actual_menu_samples=0',
    'actual_style_objects=1': 'actual_style_objects=0',
    'name_label_revisions=1': 'name_label_revisions=0',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's farewell, retirement and new recruits

The [testing ROM](../../{ROM.as_posix()}) includes the new Hodram edits and the earlier cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B131_B150", "hodram_B151_B160").replace("initialized_Hodram_B131_B150", "initialized_Hodram_B151_B160").replace(
    "verified_hodram_B111_B130_predecessor", "verified_hodram_B131_B150_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B131_B150_FOCUSED_ONLY.nds': 'Hodram_B151_B160_FOCUSED_ONLY.nds',
    'Preserve the Hodram crew lessons and Sera candidate': 'Preserve the Hodram farewell and recruitment candidate',
    notes: '''    DOC.write_text(f"""# Hodram's farewell, retirement and new recruits

Revisited 331 records from the clean Japanese, including the audiences, Sera's farewell, Hodram's retirement and the recruitment of Al, Angelo, Ian and Carlo. The pass revises 112 turns and records 219 individual retentions. It keeps Ian's composure through the tavern confrontation and Carlo's change of tone from bargaining to concern. Sera's farewell keeps its original staggered text placement. The 27 reviewed speaker names and roles retain their established forms. [Exact sources and individual decisions](../{REVIEW.as_posix()})

The native checks cover 568 commands, 25 speakerless panels and {native_count()} revised pages. The prose and wrap edits save {pages_saved()} page turns. The focused emulator replay verifies {observed_count()} pages, including the staged farewell, the approved names and substitutions, a retained two-page exchange and Carlo's direct transition to the following turn. Natural triggers, other conditional paths and hardware remain unvisited. [Native and gameplay evidence](../{VERIFY.as_posix()})

The registered build preserves 114 accepted layers and the ASCII right-bound correction. The clean-input patch rebuilt the ROM exactly. The startup comparison and 17 regression tests passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B131_B150", "hodram_B151_B160").replace("B131_B150_staged", "B151_B160_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-Hodram-farewell-and-recruits", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

