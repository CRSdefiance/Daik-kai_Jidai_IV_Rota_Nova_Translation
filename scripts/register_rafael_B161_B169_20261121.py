"""Register Rafael's audience, letter and recruitment exchanges cumulatively."""

from types import SimpleNamespace

from scripts import register_rafael_homeland_and_maps_20261121 as parent
from scripts import replay_rafael_B161_B169_20261121 as live
from scripts import verify_rafael_B161_B169_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B161-B169-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_B161_B169_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_B161_B169_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_B161_B169_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B161_B169_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = writer.BLOCKS[0]
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Reviewed 368 Rafael records with 91 wording revisions, six punctuation glyph corrections, five wrap-only fixes, and 266 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 0 and sorted(m["count"] for m in rendered["menus"]) == [2]':
        'rendered["FE_panels"] == 30 and not rendered["menus"]',
    'not rendered["style_objects"] and not rendered["full_name_retention_cases"]':
        'not rendered["style_objects"]',
    'len(playback["holds"]) == 37 and len(playback["menus"]) == 2 and playback["reused_speech_samples"] == 29 and len(playback["exact_sampled_page_turn"]) == 3':
        'len(playback["holds"]) == 29 and not playback["menus"] and len(playback["exact_sampled_page_turn"]) == 4',
    'len(name_check["records"]) == 14': 'len(name_check["records"]) == 31',
    'len(group["commands"]) for group in groups.values()) == 529': 'len(group["commands"]) for group in groups.values()) == 781',
    'startup = parent.parent.parent.parent.parent.startup_check': 'startup = parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 287': '== len(draft["records"]) == 368',
    '{"wording": 170, "wrap": 2, "retention": 115}': '{"revision": 102, "retention": 266, "wrap_only": 5}',
    'if r["finding"] == "wording"': 'if r["decision"] == "revision" and r.get("change_class") != "wrap-only"',
    'assert len(glyphs) == 18': 'assert len(glyphs) == 6',
    '    validate_natural_dialogue_batch(draft)':
        '    assert draft["encoder"] == "registered-native-story-objects"\n'
        '    draft.update(encoder="dialogue-relocatable-v1", stored_writer="registered-native-story-objects")\n'
        '    validate_natural_dialogue_batch(draft)',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_palace_and_alliance_predecessor': 'verified_rafael_homeland_and_maps_predecessor',
    'len(batches) == 1007 and len(checks) == 342': 'len(batches) == 1008 and len(checks) == 343',
    'previously_localized_records=287': 'previously_localized_records=368',
    'prose_revisions=152': 'prose_revisions=91',
    'wrap_only_revisions=2': 'wrap_only_revisions=5',
    'justified_retentions=115': 'justified_retentions=266',
    'text_display_revisions=18': 'text_display_revisions=6',
    'punctuation_glyph_corrections=18': 'punctuation_glyph_corrections=6',
    'prior_records_reviewed=287': 'prior_records_reviewed=368',
    'contextual_nameplate_retentions=14': 'contextual_nameplate_retentions=31',
    'actual_menu_samples=2': 'actual_menu_samples=0',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's audience, letter and recruitment scenes

The [testing ROM](../../{ROM.as_posix()}) includes the contextual review of Rafael's SC0 blocks 161–169. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_homeland_and_maps", "rafael_B161_B169").replace(
    "verified_rafael_B161_B169_predecessor", "verified_rafael_homeland_and_maps_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("homeland_and_maps_staged_v*/"': 'glob("staged_B161_B169*/"',
    'glob("homeland_and_maps_staged_v*/focused_gameplay/Rafael_Homeland_And_Maps_RESEARCH_ONLY.nds")':
        'glob("staged_B161_B169*/focused_gameplay/Rafael_B161_B169_FOCUSED_ONLY.nds")',
    "Preserve the Rafael homeland candidate": "Preserve the Rafael audience and recruitment candidate",
    notes: '''    DOC.write_text(f"""# Rafael's audience, letter and recruitment scenes

The contextual pass covers all 368 utterances in SC0 blocks 161–169. The Crown's statement keeps the Pope's expected role and the condition of showing him all seven Proofs. Rafael's full name stands on its own in the audience. Eirene's headings, pensive breaks and the alternating placement with Claudio survive. Charlotte's beginner Portuguese, pronunciation aid and signature preserve their source staging. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Al's recruitment preserves his refusal to run errands and his eventual choice to sail. Angelo's apology leads into the invitation, and Ian's response to the patrons preserves his restraint and self-possession. The wrap fixes keep Claudio's tag, the Brass Lamp reveal and the condition across the page turn intact. Julio's trade advice distinguishes market share from cargo space.

Native checks cover {native_count()} revised pages, all 30 speakerless panels and 31 retained names and role labels. Focused cold-boot emulator excerpts cover {observed_count()} pages, including name substitution, the two-page turn, the return from a speakerless panel to dialogue and the exit to port. Conditional branches and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The registered candidate preserves 114 accepted layers, the right-bound fix, and seven source-format controls. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_homeland_and_maps", "rafael_B161_B169")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
