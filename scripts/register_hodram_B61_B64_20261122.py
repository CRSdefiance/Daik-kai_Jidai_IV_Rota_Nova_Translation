"""Register Sera's memories, the Nagarpur procession and the sea-king legend."""

from types import SimpleNamespace

from scripts import register_hodram_B54_B60_20261122 as parent
from scripts import replay_hodram_B61_B64_20261122 as live
from scripts import verify_hodram_B61_B64_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B61-B64-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B61_B64_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B61_B64_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B61_B64_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B61_B64_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = tuple(range(61, 65))
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
startup_reference = parent.startup_reference
CHECKPOINT = ("Revisited 95 Hodram records in four scenes through the sea-king legend. "
              "The review changes 38 lines and two punctuation glyphs, with 55 justified retentions. "
              "One exact earlier decision carries forward.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 1': 'rendered["FE_panels"] == 0',
    'rendered["revised_speech_pages"] == 43': 'rendered["revised_speech_pages"] == 40',
    'draft["contextual_records_revisited"] == 79 and draft["contextual_decisions_reused"] == 3':
        'draft["contextual_records_revisited"] == 95 and draft["contextual_decisions_reused"] == 1',
    'len(playback["holds"]) == len(live.SELECTED) + 1': 'len(playback["holds"]) == len(live.SELECTED)',
    '[(ident, page) for ident, page, _ in playback["exact_turn_and_following"]] == '
    '[(live.PAGE_TURN, 1), (live.PAGE_TURN, 2), ("DK4_MES_B60_R0015", 1)]':
        '[(ident, page) for ident, page, _ in playback["exact_legend_argument"]] == '
        '[(ident, 1) for ident in live.legend_ids]',
    'len(name_check["records"]) == 10': 'len(name_check["records"]) == 9',
    'len(group["commands"]) for group in groups.values()) == 152': 'len(group["commands"]) for group in groups.values()) == 151',
    '== len(draft["records"]) == 82': '== len(draft["records"]) == 96',
    '{"wording": 39, "glyph": 3, "retention": 40}': '{"wording": 38, "glyph": 2, "retention": 56}',
    '(row["previous_English"], row["english"]) == ("？", "?")':
        '(row["previous_English"], row["english"]) in (("？", "?"), ("！", "!"))',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1019 and len(checks) == 354': 'len(batches) == 1020 and len(checks) == 355',
    'previously_localized_records=82, contextual_records_revisited=79, contextual_decisions_reused=3':
        'previously_localized_records=96, contextual_records_revisited=95, contextual_decisions_reused=1',
    'prose_revisions=39': 'prose_revisions=38',
    'justified_retentions=37': 'justified_retentions=55',
    'prior_records_reviewed=79, contextual_decisions_reused=3': 'prior_records_reviewed=95, contextual_decisions_reused=1',
    'contextual_nameplate_retentions=10': 'contextual_nameplate_retentions=9',
    'text_display_revisions=3': 'text_display_revisions=2',
    'punctuation_glyph_corrections=3': 'punctuation_glyph_corrections=2',
    'two_page_count_explanations=1': 'two_page_count_explanations=0',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sera's memories, Nagarpur and the sea-king legend

The [testing ROM](../../{ROM.as_posix()}) includes four reviewed scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B54_B60", "hodram_B61_B64").replace("initialized_Hodram_B54_B60", "initialized_Hodram_B61_B64").replace(
    "verified_hodram_B0_B23_predecessor", "verified_hodram_B54_B60_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B54_B60_FOCUSED_ONLY.nds': 'Hodram_B61_B64_FOCUSED_ONLY.nds',
    'Preserve the Sera and Espinosa candidate': 'Preserve the candidate with Sera’s memories and the sea-king legend',
    notes: '''    DOC.write_text(f"""# Sera's memories, Nagarpur and the sea-king legend

The complete source packet covers 96 records. One exact earlier decision carries forward. The review changes 38 lines, corrects two full-width punctuation glyphs, and retains 55 lines for individual reasons. The revised English keeps Hodram's initial guesses separate from what Sera confirms. Nagarpur shows off his wealth, and Sera's account of the sea king keeps her hesitations. Hodram moves from laughing at the story to apologizing for hurting her. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Stored verification covers all 151 commands in the four blocks. Native and visual checks cover {native_count()} revised pages, the three name-width alternates, and the nine speaker labels. Focused emulator excerpts verified {observed_count()} speech pages, both punctuation changes, and the shifts in tone as Sera remembers the fires and takes Hodram's mockery personally. The original scene triggers and hardware remain unvisited for these scenes. [Display evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves all 114 accepted layers and the ASCII right boundary correction. Six startup comparisons, 17 regression tests, and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B54_B60", "hodram_B61_B64").replace("B54_B60_staged", "B61_B64_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-linked-dialogue", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
