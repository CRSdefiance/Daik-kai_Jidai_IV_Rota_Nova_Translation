"""Register the revised Yifa, crown, and Aziza dialogue cumulatively."""

from types import SimpleNamespace

from scripts import register_rafael_B177_B180_20261121 as parent
from scripts import replay_rafael_B181_B187_20261121 as live
from scripts import verify_rafael_B181_B187_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B181-B187-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_B181_B187_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_B181_B187_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_B181_B187_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B181_B187_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = writer.BLOCKS[0]
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Reviewed 227 Rafael records with 39 wording revisions, three glyph corrections, two wrap-only fixes, and 183 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 1 and [m["count"] for m in rendered["menus"]] == [2, 2, 2, 2]':
        'rendered["FE_panels"] == 13 and not rendered["menus"] and rendered["full_name_retention_cases"] == [display.FULL_NAME_ID]',
    'len(playback["holds"]) == 26 and len(playback["menus"]) == 8 and len(playback["exact_sampled_page_turn"]) == 3':
        'len(playback["holds"]) == 40 and not playback["menus"] and len(playback["exact_sampled_page_turn"]) == 5',
    'len(name_check["records"]) == 9': 'len(name_check["records"]) == 10',
    'len(group["commands"]) for group in groups.values()) == 318': 'len(group["commands"]) for group in groups.values()) == 308',
    'startup = parent.parent.parent.parent.parent.parent.parent.parent.startup_check':
        'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 183': '== len(draft["records"]) == 227',
    '{"wording": 35, "glyph": 2, "wrap-only": 3, "retention": 143}':
        '{"wording": 39, "glyph": 3, "wrap-only": 2, "retention": 183}',
    'assert len(glyphs) == 2': 'assert len(glyphs) == 3',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_B170_B176_predecessor': 'verified_rafael_B177_B180_predecessor',
    'len(batches) == 1010 and len(checks) == 345': 'len(batches) == 1011 and len(checks) == 346',
    'previously_localized_records=183': 'previously_localized_records=227',
    'prose_revisions=35': 'prose_revisions=39',
    'wrap_only_revisions=3': 'wrap_only_revisions=2',
    'justified_retentions=143': 'justified_retentions=183',
    'text_display_revisions=2': 'text_display_revisions=3',
    'punctuation_glyph_corrections=2': 'punctuation_glyph_corrections=3',
    'prior_records_reviewed=183': 'prior_records_reviewed=227',
    'contextual_nameplate_retentions=9': 'contextual_nameplate_retentions=10',
    'actual_menu_samples=8': 'actual_menu_samples=0',
    'initialized_Rafael_B177_B180=True': 'initialized_Rafael_B181_B187=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's Yifa, crown, and Aziza scenes

The [testing ROM](../../{ROM.as_posix()}) includes the contextual review of Rafael's SC0 blocks 181–187. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B177_B180", "rafael_B181_B187").replace(
    "verified_rafael_B181_B187_predecessor", "verified_rafael_B177_B180_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B177_B180': 'glob("staged_B181_B187',
    'Rafael_B177_B180_FOCUSED_ONLY.nds': 'Rafael_B181_B187_FOCUSED_ONLY.nds',
    "Preserve the Rafael recruitment and optional tutorial candidate": "Preserve the Rafael Yifa, crown, and Aziza candidate",
    notes: '''    DOC.write_text(f"""# Rafael's Yifa, crown, and Aziza scenes

The contextual pass covers 227 records in SC0 blocks 181–187. Yifa's challenge and later recruitment preserve her energy and Rafael's identification with her. Sanghyeon describes their shared teacher and his seniority, their sibling-like upbringing, and the end of their formal ties. Mihwa's terms stay tentative even when Julian calls them a promise. Both crown gifts and Reika's qualified account keep their individual source references. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Aziza's thirteen speakerless panels retain their native selector. Her greeting reserves room for the full company substitution, and Rafael's reply preserves both original name fields in order. The other pirates' responses and Claudio's reaction preserve the authority Aziza shows in the encounter.

Offline checks cover {native_count()} revised pages, all thirteen speakerless panels, ten nameplates, the company width, and full-name width. Focused cold-boot play verified {observed_count()} speech pages, the modal-to-named transitions, and the return to port. Both crown variants appear as excerpts. Natural route activation and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The registered candidate preserves 114 accepted layers, the right-bound correction, and seven source-format controls. Six startup comparisons, 17 regression tests, and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B177_B180", "rafael_B181_B187")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
