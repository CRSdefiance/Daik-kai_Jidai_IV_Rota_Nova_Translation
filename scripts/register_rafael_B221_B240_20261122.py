"""Register the full Rafael B221–240 packet and its exact clean-input patch."""

from types import SimpleNamespace

from scripts import register_rafael_B211_B220_20261122 as parent
from scripts import replay_rafael_B221_B240_20261122 as live
from scripts import verify_rafael_B221_B240_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B221-B240-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_B221_B240_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_B221_B240_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_B221_B240_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B221_B240_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (221, 222, 223, 224, 227, 228, 229, 230, 232, 233, 234, 235, 236, 237, 238, 239)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Revisited 222 Rafael records and carried forward 48 earlier decisions. The review made 60 wording revisions and two punctuation glyph corrections, with 160 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


validation_section = parent.verification[parent.verification.index("    assert not rendered["):
                                          parent.verification.index('    assert len(playback["holds"])')]
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 19 and [m["count"] for m in rendered["menus"]] == [2, 2, 2]':
        'rendered["FE_panels"] == 3 and [m["count"] for m in rendered["menus"]] == [2, 3, 2]',
    validation_section: '''    styles = rendered["style_objects"]
    assert [item["block"] for item in styles] == [221, 221, 226, 235]
    assert sum(len(item["slot_owner_sets"]) for item in styles) == 29
    assert draft["contextual_records_revisited"] == 222 and draft["contextual_decisions_reused"] == 48
''',
    'len(playback["holds"]) == len(live.SELECTED) - 3 and len(playback["menus"]) == 6':
        'len(playback["holds"]) == 40 and len(playback["menus"]) == 7',
    'len(name_check["records"]) == 19': 'len(name_check["records"]) == 26',
    'len(group["commands"]) for group in groups.values()) == 325': 'len(group["commands"]) for group in groups.values()) == 343',
    'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check':
        'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 224': '== len(draft["records"]) == 270',
    '{"wording": 45, "glyph": 1, "wrap-only": 5, "retention": 173}':
        '{"wording": 60, "glyph": 2, "retention": 208}',
    'assert len(glyphs) == 1': 'assert len(glyphs) == 2',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_B208_B210_predecessor': 'verified_rafael_B211_B220_predecessor',
    'len(batches) == 1013 and len(checks) == 348': 'len(batches) == 1014 and len(checks) == 349',
    'previously_localized_records=224, contextual_records_revisited=192, contextual_decisions_reused=32':
        'previously_localized_records=270, contextual_records_revisited=222, contextual_decisions_reused=48',
    'prose_revisions=45': 'prose_revisions=60',
    'wrap_only_revisions=5': 'wrap_only_revisions=0',
    'justified_retentions=141': 'justified_retentions=160',
    'text_display_revisions=1': 'text_display_revisions=2',
    'punctuation_glyph_corrections=1': 'punctuation_glyph_corrections=2',
    'prior_records_reviewed=192, contextual_decisions_reused=32': 'prior_records_reviewed=222, contextual_decisions_reused=48',
    'contextual_nameplate_retentions=19': 'contextual_nameplate_retentions=26',
    'actual_menu_samples=6, actual_style_objects=0': 'actual_menu_samples=7, actual_style_objects=4',
    'initialized_Rafael_B211_B220=True': 'initialized_Rafael_B221_B240=True',
    'STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, REBOUND, args.visual_review,': 'STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, args.visual_review,',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's letters, legends, and town exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the contextual review of Rafael's SC0 blocks 221–240. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B211_B220", "rafael_B221_B240").replace(
    "verified_rafael_B221_B240_predecessor", "verified_rafael_B211_B220_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B211_B220': 'glob("staged_B221_B240',
    'Rafael_B211_B220_FOCUSED_ONLY.nds': 'Rafael_B221_B240_FOCUSED_ONLY.nds',
    "Preserve the Rafael portrait, castle, parrot, and item candidate": "Preserve Rafael's letters, legends, and town exchanges",
    notes: '''    DOC.write_text(f"""# Rafael's letters, legends, and town exchanges

The review revisits 222 records and carries forward 48 exact earlier decisions from B225, B226 and B240. Yukihisa's letter preserves the reported curse and the uncertain location of the blade. Janus's and Ian's signatures retain their layout. The style tables keep the original eight slots and all aliases. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

The townsman's account of the Crusades, Al Shin's praise for Saladin and Gerhard's interpretation of Charles Martel remain in their own voices. Manuel's comments leave Iceland and northern Europe as tentative readings of different rumors. Vivian's claim about Excalibur and the barkeep's skepticism remain distinct. The child playing opposite Charles Martel in B237 still uses actor 151. That actor's wider nameplate and catalogue review remains open.

Native verification covers {native_count()} revised pages, four style tables, three speakerless panels, 26 nameplates and seven choice captions. Focused cold-boot excerpts verify {observed_count()} dialogue pages, seven choice highlights, four actor-style selections, the original signatures and the transition after Saladin's two-page account. Natural encounter activation and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers, the ASCII right-bound correction and seven source-format controls. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B211_B220", "rafael_B221_B240")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
