"""Register the Sera, Espinosa and Sao Jorge dialogue checkpoint."""

from types import SimpleNamespace

from scripts import register_hodram_B0_B23_20261122 as parent
from scripts import replay_hodram_B54_B60_20261122 as live
from scripts import verify_hodram_B54_B60_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B54-B60-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B54_B60_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B54_B60_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B54_B60_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B54_B60_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = tuple(range(54, 61))
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Revisited 79 Hodram records from Sera's first words through the Espinosa and Sao Jorge scenes. The review changes 39 lines and three question glyphs, with 37 justified retentions. Three exact earlier decisions carry forward."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


glyph = parent.verification[parent.verification.index("    glyphs ="):parent.verification.index('    draft["punctuation_glyph_corrections"]')]
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 9': 'rendered["FE_panels"] == 1',
    'assert rendered["revised_speech_pages"] == 83': 'assert rendered["revised_speech_pages"] == 43',
    'draft["contextual_records_revisited"] == 195 and draft["contextual_decisions_reused"] == 6':
        'draft["contextual_records_revisited"] == 79 and draft["contextual_decisions_reused"] == 3',
    'len(playback["holds"]) == len(live.SELECTED) and not playback["menus"]':
        'len(playback["holds"]) == len(live.SELECTED) + 1 and not playback["menus"]',
    'assert [ident for ident, _ in playback["exact_elegy_holds"]] == live.ELEGY':
        'assert [(ident, page) for ident, page, _ in playback["exact_turn_and_following"]] == '
        '[(live.PAGE_TURN, 1), (live.PAGE_TURN, 2), ("DK4_MES_B60_R0015", 1)]',
    'len(name_check["records"]) == 20': 'len(name_check["records"]) == 10',
    'len(group["commands"]) for group in groups.values()) == 362': 'len(group["commands"]) for group in groups.values()) == 152',
    '== len(draft["records"]) == 201': '== len(draft["records"]) == 82',
    '{"wording": 80, "wrap-only": 3, "retention": 118}': '{"wording": 39, "glyph": 3, "retention": 40}',
    glyph: '''    glyphs = [row["id"] for row in draft["records"] if row["change_class"] == "glyph"
              and (row["previous_English"], row["english"]) == ("？", "?")]
    assert set(glyphs) == writer.author.GLYPHS
''',
})
startup_reference = parent.startup_reference

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1018 and len(checks) == 353': 'len(batches) == 1019 and len(checks) == 354',
    'previously_localized_records=201, contextual_records_revisited=195, contextual_decisions_reused=6':
        'previously_localized_records=82, contextual_records_revisited=79, contextual_decisions_reused=3',
    'prose_revisions=80': 'prose_revisions=39',
    'wrap_only_revisions=3': 'wrap_only_revisions=0',
    'justified_retentions=112': 'justified_retentions=37',
    'prior_records_reviewed=195, contextual_decisions_reused=6': 'prior_records_reviewed=79, contextual_decisions_reused=3',
    'contextual_nameplate_retentions=20': 'contextual_nameplate_retentions=10',
    'initialized_Hodram_B0_B23=True': 'initialized_Hodram_B54_B60=True',
    'text_display_revisions=0': 'text_display_revisions=3',
    'punctuation_glyph_corrections=0': 'punctuation_glyph_corrections=3',
    'two_page_count_explanations=0': 'two_page_count_explanations=1',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sera's first words and the Espinosa scenes

The [testing ROM](../../{ROM.as_posix()}) includes Sera's first words, the Espinosa confrontation, and Manuel's account of Sao Jorge. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B0_B23", "hodram_B54_B60").replace(
    "verified_hodram_B24_B53_predecessor", "verified_hodram_B0_B23_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged*/': 'glob("B54_B60_staged*/',
    'Hodram_B0_B23_FOCUSED_ONLY.nds': 'Hodram_B54_B60_FOCUSED_ONLY.nds',
    'Preserve Hodram’s opening battles and rescue candidate': 'Preserve the Sera and Espinosa candidate',
    notes: '''    DOC.write_text(f"""# Sera, Espinosa, and Manuel's account of Sao Jorge

The complete source packet covers 82 records. Three exact earlier decisions carry forward. The new review changes 39 lines, normalizes three full-width question marks, and retains 37 lines for individual reasons. Sera's uncertain pauses stay audible as she learns to thank Hodram and later confronts Espinosa. The townspeople speak for themselves. Manuel's experience of care in Sao Jorge leads into his faith and his vow to fight slavers. [Exact Japanese and registered review](../{REVIEW.as_posix()})

Stored verification covers all 152 commands in the seven blocks. The native and visual review covers all {native_count()} revised pages, the unchanged speakerless caption, and the nameplate getters for ten source roles and actors. The map handover now fits on one page. Manuel's account keeps two pages and uses a complete first-page sentence. Focused emulator excerpts verified {observed_count()} speech pages, the substituted names and silent panel, the revised handover, and the next keypress after Manuel's account. Original gameplay activation and hardware remain unvisited for these scenes. [Display evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves all 114 accepted layers and the ASCII right boundary correction. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B0_B23", "hodram_B54_B60")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-linked-dialogue", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
