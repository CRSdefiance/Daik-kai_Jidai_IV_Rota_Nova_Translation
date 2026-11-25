"""Register the Rafael ruins choices and cave-in wraps with the cumulative build."""

from types import SimpleNamespace

from scripts import register_rafael_B221_B240_20261122 as parent
from scripts import replay_rafael_B261_B280_20261122 as live
from scripts import verify_rafael_B261_B280_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B261-B280-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_B261_B280_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_B261_B280_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_B261_B280_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B261_B280_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (261,)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Revisited 21 Rafael records and carried forward 114 earlier decisions. The ruins review made four wrap-only fixes and two choice-caption revisions, with 15 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 3 and [m["count"] for m in rendered["menus"]] == [2, 3, 2]':
        'rendered["FE_panels"] == 17 and [m["count"] for m in rendered["menus"]] == [3, 2]',
    '[221, 221, 226, 235]': '[261, 261]',
    'for item in styles) == 29': 'for item in styles) == 16',
    'draft["contextual_records_revisited"] == 222 and draft["contextual_decisions_reused"] == 48':
        'draft["contextual_records_revisited"] == 21 and draft["contextual_decisions_reused"] == 114',
    'len(playback["holds"]) == 40 and len(playback["menus"]) == 7':
        'len(playback["holds"]) == 26 and len(playback["menus"]) == 5',
    'len(name_check["records"]) == 26': 'len(name_check["records"]) == 16',
    'len(group["commands"]) for group in groups.values()) == 343': 'len(group["commands"]) for group in groups.values()) == 353',
    'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check':
        'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 270': '== len(draft["records"]) == 135',
    '{"wording": 60, "glyph": 2, "retention": 208}': '{"wording": 2, "wrap-only": 4, "retention": 129}',
    'assert len(glyphs) == 2': 'assert not glyphs',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_B211_B220_predecessor': 'verified_rafael_B221_B240_predecessor',
    'len(batches) == 1014 and len(checks) == 349': 'len(batches) == 1015 and len(checks) == 350',
    'previously_localized_records=270, contextual_records_revisited=222, contextual_decisions_reused=48':
        'previously_localized_records=135, contextual_records_revisited=21, contextual_decisions_reused=114',
    'prose_revisions=60': 'prose_revisions=0',
    'wrap_only_revisions=0': 'wrap_only_revisions=4',
    'justified_retentions=160': 'justified_retentions=15',
    'text_display_revisions=2': 'text_display_revisions=0',
    'punctuation_glyph_corrections=2': 'punctuation_glyph_corrections=0',
    'choice_label_revisions=0': 'choice_label_revisions=2',
    'prior_records_reviewed=222, contextual_decisions_reused=48': 'prior_records_reviewed=21, contextual_decisions_reused=114',
    'contextual_nameplate_retentions=26': 'contextual_nameplate_retentions=16',
    'actual_menu_samples=7, actual_style_objects=4': 'actual_menu_samples=5, actual_style_objects=2',
    'initialized_Rafael_B221_B240=True': 'initialized_Rafael_B261_B280=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's ruins puzzle

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed SC0 blocks 261–280 and the revised ruins dialogue. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B221_B240", "rafael_B261_B280").replace(
    "verified_rafael_B261_B280_predecessor", "verified_rafael_B221_B240_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B221_B240': 'glob("staged_B261_B280',
    'Rafael_B221_B240_FOCUSED_ONLY.nds': 'Rafael_B261_B280_FOCUSED_ONLY.nds',
    "Preserve Rafael's letters, legends, and town exchanges": "Preserve Rafael's ruins puzzle and arrest assignments",
    notes: '''    DOC.write_text(f"""# Rafael's ruins puzzle and arrest assignments

The review revisits 21 native style variants and choice captions and carries forward 114 exact earlier decisions. The two cave-in tables retain all eight voice slots and their original warnings. Four variants now keep their second warning together, and the figurehead's two replies directly answer its question. The stone menu still follows the original front, left, and right sequence. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Native verification covers all four revised speech pages, 17 speakerless panels, 16 fixed nameplates, and five choice captions. Focused cold-boot excerpts verify {observed_count()} dialogue pages, five menu highlights, both cave-in displays and the figurehead's speakerless transitions. The menu VM and relocation checks verify the choice indices and branch controls offline. The focused excerpts exercise the displays. Natural encounter activation and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers, the ASCII right-bound correction and seven source-format controls. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B221_B240", "rafael_B261_B280")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
