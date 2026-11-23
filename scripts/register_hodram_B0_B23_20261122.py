"""Register Hodram's opening exchanges and preserve the exact clean-input patch."""

from types import SimpleNamespace

from scripts import register_hodram_opening_20261122 as parent
from scripts import replay_hodram_B0_B23_20261122 as live
from scripts import verify_hodram_B0_B23_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B0-B23-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B0_B23_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B0_B23_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B0_B23_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B0_B23_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 21, 22, 23)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Revisited 195 Hodram opening records, with 80 wording revisions, three wrap-only fixes, and 112 justified retentions. Six earlier decisions carry forward."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


alias_check = parent.verification[parent.verification.index("    aliases ="):
                                  parent.verification.index("    assert viewed ==")]
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 9 and len(rendered["menus"]) == 2 and len(rendered["style_objects"]) == 1':
        'rendered["FE_panels"] == 9 and not rendered["menus"] and not rendered["style_objects"]',
    'rendered["revised_speech_pages"] == 54': 'rendered["revised_speech_pages"] == 83',
    'draft["contextual_records_revisited"] == 118 and draft["contextual_decisions_reused"] == 2':
        'draft["contextual_records_revisited"] == 195 and draft["contextual_decisions_reused"] == 6',
    'len(playback["holds"]) == len(live.SELECTED) - 2 and len(playback["menus"]) == 4':
        'len(playback["holds"]) == len(live.SELECTED) and not playback["menus"]\n'
        '    assert [ident for ident, _ in playback["exact_elegy_holds"]] == live.ELEGY',
    'len(name_check["records"]) == 10': 'len(name_check["records"]) == 20',
    'len(group["commands"]) for group in groups.values()) == 305': 'len(group["commands"]) for group in groups.values()) == 362',
    '== len(draft["records"]) == 120': '== len(draft["records"]) == 201',
    '{"wording": 54, "retention": 66}': '{"wording": 80, "wrap-only": 3, "retention": 118}',
    alias_check: "",
})
startup_reference = parent.startup_reference

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1017 and len(checks) == 352': 'len(batches) == 1018 and len(checks) == 353',
    'previously_localized_records=120, contextual_records_revisited=118, contextual_decisions_reused=2':
        'previously_localized_records=201, contextual_records_revisited=195, contextual_decisions_reused=6',
    'prose_revisions=54': 'prose_revisions=80',
    'wrap_only_revisions=0': 'wrap_only_revisions=3',
    'justified_retentions=64': 'justified_retentions=112',
    'prior_records_reviewed=118, contextual_decisions_reused=2': 'prior_records_reviewed=195, contextual_decisions_reused=6',
    'contextual_nameplate_retentions=10': 'contextual_nameplate_retentions=20',
    'actual_menu_samples=4, actual_style_objects=1': 'actual_menu_samples=0, actual_style_objects=0',
    'initialized_Hodram_B24_B53=True': 'initialized_Hodram_B0_B23=True',
    'live.PROOF, live.ALIASES, display.PROOF': 'live.PROOF, display.PROOF',
    'prior_caption_keys = verify_existing_credit(draft["records"], credited)':
        'assert all((row["file_path"], row["id"]) in credited for row in draft["records"])',
    ', credited_choice_aliases=prior_caption_keys': '',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's opening battles and rescue scenes

The [testing ROM](../../{ROM.as_posix()}) includes the early encounters, Sera's rescue, Manuel's elegy and Aziza's mutiny and recruitment. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B24_B53", "hodram_B0_B23").replace(
    "verified_rafael_B306_B309_predecessor", "verified_hodram_B24_B53_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B24_B53_FOCUSED_ONLY.nds': 'Hodram_B0_B23_FOCUSED_ONLY.nds',
    'Preserve the early Hodram contextual candidate': 'Preserve Hodram’s opening battles and rescue candidate',
    notes: '''    DOC.write_text(f"""# Hodram's early encounters, Sera's rescue, and Aziza's mutiny

The complete source packet covers 201 records. Six earlier decisions match exactly, 112 new decisions retain wording and layout for individual reasons, 80 update the wording, and three fix wraps while retaining the words. Sera's freedom to leave and silent reactions stay intact. Manuel's elegy keeps its repeated refrain and three separate panels. Aziza's change of heart remains tied to her father's keepsake and her crew's betrayal. [Exact Japanese and registered review](../{REVIEW.as_posix()})

Stored verification covers 362 commands in 22 blocks. Native and visual checks cover all {native_count()} revised pages, wider name and fleet substitutions, nine retained speakerless panels, and 20 named or role-based headers. Focused initialized Hodram excerpts verify {observed_count()} dialogue pages, including the displayed fleet name, the alternating silent and named rescue panels, all three elegy panels advanced in order, and the return to port. The inherited source branching was checked offline. Natural activation and hardware remain unvisited for this batch. [Display evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers and the ASCII right boundary correction. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B24_B53", "hodram_B0_B23")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-Hodram-opening", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
