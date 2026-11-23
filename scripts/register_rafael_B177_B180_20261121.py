"""Register the verified Cesare, Fernando, Manuel, and shipwright exchanges."""

from types import SimpleNamespace

from scripts import register_rafael_B170_B176_20261121 as parent
from scripts import replay_rafael_B177_B180_20261121 as live
from scripts import verify_rafael_B177_B180_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B177-B180-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_B177_B180_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_B177_B180_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_B177_B180_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B177_B180_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = writer.BLOCKS[0]
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Reviewed 183 Rafael records with 35 wording revisions, two glyph corrections, three wrap-only fixes, and 143 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 6 and not rendered["menus"]':
        'rendered["FE_panels"] == 1 and [m["count"] for m in rendered["menus"]] == [2, 2, 2, 2]',
    'len(playback["holds"]) == 29 and not playback["menus"] and len(playback["exact_sampled_page_turn"]) == 5':
        'len(playback["holds"]) == 26 and len(playback["menus"]) == 8 and len(playback["exact_sampled_page_turn"]) == 3',
    'len(name_check["records"]) == 13': 'len(name_check["records"]) == 9',
    'len(group["commands"]) for group in groups.values()) == 294': 'len(group["commands"]) for group in groups.values()) == 318',
    'startup = parent.parent.parent.parent.parent.parent.parent.startup_check':
        'startup = parent.parent.parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 190': '== len(draft["records"]) == 183',
    '{"wording": 56, "glyph": 6, "wrap-only": 4, "retention": 124}':
        '{"wording": 35, "glyph": 2, "wrap-only": 3, "retention": 143}',
    'assert len(glyphs) == 6': 'assert len(glyphs) == 2',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_B161_B169_predecessor': 'verified_rafael_B170_B176_predecessor',
    'len(batches) == 1009 and len(checks) == 344': 'len(batches) == 1010 and len(checks) == 345',
    'previously_localized_records=190': 'previously_localized_records=183',
    'prose_revisions=56': 'prose_revisions=35',
    'wrap_only_revisions=4': 'wrap_only_revisions=3',
    'justified_retentions=124': 'justified_retentions=143',
    'text_display_revisions=6': 'text_display_revisions=2',
    'punctuation_glyph_corrections=6': 'punctuation_glyph_corrections=2',
    'prior_records_reviewed=190': 'prior_records_reviewed=183',
    'contextual_nameplate_retentions=13': 'contextual_nameplate_retentions=9',
    'actual_menu_samples=0': 'actual_menu_samples=8',
    'initialized_Rafael_B170_B176=True': 'initialized_Rafael_B177_B180=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's ship-buying, coin-game, refitting, and sailing lessons

The [testing ROM](../../{ROM.as_posix()}) includes the contextual review of Rafael's SC0 blocks 177–180. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B170_B176", "rafael_B177_B180").replace(
    "verified_rafael_B177_B180_predecessor", "verified_rafael_B170_B176_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B170_B176': 'glob("staged_B177_B180',
    'Rafael_B170_B176_FOCUSED_ONLY.nds': 'Rafael_B177_B180_FOCUSED_ONLY.nds',
    "Preserve the Rafael Carlo, Cristina, Samwell, and Jam candidate": "Preserve the Rafael recruitment and optional tutorial candidate",
    notes: '''    DOC.write_text(f"""# Rafael's ship-buying, coin-game, refitting, and sailing lessons

The contextual pass covers 183 records in SC0 blocks 177–180, including both captions in four menus. Cesare recognizes the Elysion, asks to sail with her, and shares practical ship-buying advice. The one percent share and one-to-five-unit limit begin on the second page. Fernando's game explanation keeps the last-coin rule and the multiple-of-four-plus-one strategy. The tavern exchange retains Man and Woman as the two nameplates. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Manuel's advice distinguishes crew assignments, room effects, and the admiral's responsibility. The shipwright lesson makes the lateen, topsail, and slightly off-angle wind relationship readable as in-game advice. All eight choice captions keep their original slots.

Offline checks cover {native_count()} revised pages, the retained Extra Armor notice, nine speaker labels, and both text styles for every caption. Focused cold-boot play verified {observed_count()} speech pages, eight menu highlights, a two-page tutorial transition, and the return to port. The excerpt fixture uses the original data objects. Natural branch activation and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The registered candidate preserves 114 accepted layers, the right-bound correction, and seven source-format controls. Six startup comparisons, 17 regression tests, and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B170_B176", "rafael_B177_B180")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
