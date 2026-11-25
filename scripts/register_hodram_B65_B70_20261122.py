"""Register Hodram's farewell and the complete linked Batavia exchanges."""

from types import SimpleNamespace

from scripts import register_hodram_B61_B64_20261122 as parent
from scripts import replay_hodram_B65_B70_20261122 as live
from scripts import verify_hodram_B65_B70_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B65-B70-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B65_B70_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B65_B70_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B65_B70_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B65_B70_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = tuple(range(65, 71))
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Revisited 125 Hodram records across six scenes. The review changes 47 lines and five punctuation glyphs, "
              "with 73 justified retentions and three exact carried decisions.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["revised_speech_pages"] == 40':
        'rendered["revised_speech_pages"] == 52 and rendered["alternate_name_width_pages"] == 15',
    'draft["contextual_records_revisited"] == 95 and draft["contextual_decisions_reused"] == 1':
        'draft["contextual_records_revisited"] == 125 and draft["contextual_decisions_reused"] == 3',
    '[(ident, page) for ident, page, _ in playback["exact_legend_argument"]] == '
    '[(ident, 1) for ident in live.legend_ids]':
        '[(ident, page) for ident, page, _ in playback["exact_long_speech_and_following"]] == '
        '[(ident, 1) for ident in live.long_speech]',
    '    assert playback["initialized_excerpts"]':
        '    assert set(playback["opaque_source_symbols"]) == display.SYMBOLS\n'
        '    assert {p["id"] for p in rendered["pagination_changes"]} == '
        '{f"DK4_MES_B67_R{n:04d}" for n in (66,165,168,172,238)}\n'
        '    assert pages_saved() == 5\n'
        '    assert playback["initialized_excerpts"]',
    'len(name_check["records"]) == 9': 'len(name_check["records"]) == 11',
    'len(group["commands"]) for group in groups.values()) == 151': 'len(group["commands"]) for group in groups.values()) == 241',
    '== len(draft["records"]) == 96': '== len(draft["records"]) == 128',
    '{"wording": 38, "glyph": 2, "retention": 56}': '{"wording": 47, "glyph": 5, "retention": 76}',
    '(("？", "?"), ("！", "!"))': '(("？", "?"), ("！？", "!?"))',
    '    draft["punctuation_glyph_corrections"] = glyphs':
        '    draft["punctuation_glyph_corrections"] = glyphs\n'
        '    draft["retained_opaque_source_symbols"] = dict(records=playback["opaque_source_symbols"], '
        'path=str(display.OPAQUE), sha256=base.digest(display.OPAQUE))',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1020 and len(checks) == 355': 'len(batches) == 1021 and len(checks) == 356',
    'previously_localized_records=96, contextual_records_revisited=95, contextual_decisions_reused=1':
        'previously_localized_records=128, contextual_records_revisited=125, contextual_decisions_reused=3',
    'prose_revisions=38': 'prose_revisions=47',
    'justified_retentions=55': 'justified_retentions=73',
    'prior_records_reviewed=95, contextual_decisions_reused=1': 'prior_records_reviewed=125, contextual_decisions_reused=3',
    'contextual_nameplate_retentions=9': 'contextual_nameplate_retentions=11',
    'text_display_revisions=2': 'text_display_revisions=5',
    'punctuation_glyph_corrections=2': 'punctuation_glyph_corrections=5',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sera's farewell and the Batavia exchanges

The [testing ROM](../../{ROM.as_posix()}) includes all six reviewed scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B61_B64", "hodram_B65_B70").replace("initialized_Hodram_B61_B64", "initialized_Hodram_B65_B70").replace(
    "verified_hodram_B54_B60_predecessor", "verified_hodram_B61_B64_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B61_B64_FOCUSED_ONLY.nds': 'Hodram_B65_B70_FOCUSED_ONLY.nds',
    'Preserve the candidate with Sera’s memories and the sea-king legend':
        'Preserve the candidate with Sera’s farewell and the Batavia exchanges',
    notes: '''    DOC.write_text(f"""# Sera's farewell and the Batavia exchanges

The source packet covers all 128 records. Three earlier decisions carry forward. The fresh pass preserves 73 lines for specific reasons, revises 47 lines, and corrects five reaction glyphs. Sera's brief, halting farewell follows the unexpected reunion. Maria and Hodram keep distinct approaches to Kuhn and Pereira. Camille's urgency gives way to relief, Lil's apology, and their decision to sail together again. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Five long speeches now fit on one page each. All {native_count()} revised pages and 15 name-width variants received native and visual checks, alongside 11 exact speaker labels. The 241 stored commands preserve source control flow. Focused emulator excerpts verified {observed_count()} pages, including the six unchanged symbol streams and the keypress after Hodram's long speech. Natural event activation and hardware remain unvisited for these scenes. [Display evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves all 114 accepted layers and the registered ASCII right boundary correction. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B61_B64", "hodram_B65_B70").replace("B61_B64_staged", "B65_B70_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-batavia-dialogue", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
