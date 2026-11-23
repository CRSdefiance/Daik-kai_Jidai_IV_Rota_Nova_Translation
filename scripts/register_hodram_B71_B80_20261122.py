"""Register the revised Hangzhou and wartime dialogue in the cumulative release."""

from types import SimpleNamespace

from scripts import register_hodram_B65_B70_20261122 as parent
from scripts import replay_hodram_B71_B80_20261122 as live
from scripts import verify_hodram_B71_B80_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B71-B80-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B71_B80_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B71_B80_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B71_B80_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B71_B80_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = tuple(range(71, 81))
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Revisited 140 Hodram records from the Hangzhou summons through Sera's return. The review revises 50 lines "
              "and one punctuation glyph, with 89 justified retentions and four exact decisions carried forward.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


old_turn = next(line for line in parent.verification.splitlines() if 'playback["exact_long_speech_and_following"]' in line)
old_counts = next(line for line in parent.verification.splitlines() if 'for n in (66,165,168,172,238)' in line)
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 0': 'rendered["FE_panels"] == 4',
    'rendered["revised_speech_pages"] == 52 and rendered["alternate_name_width_pages"] == 15':
        'rendered["revised_speech_pages"] == 53 and rendered["alternate_name_width_pages"] == 9',
    'draft["contextual_records_revisited"] == 125 and draft["contextual_decisions_reused"] == 3':
        'draft["contextual_records_revisited"] == 140 and draft["contextual_decisions_reused"] == 4',
    'len(playback["holds"]) == len(live.SELECTED)': 'len(playback["holds"]) == len(live.SELECTED) + 2',
    old_turn: '''    for turn, (changed, following) in zip(playback["exact_two_page_transitions"], live.PAGE_TURNS, strict=True):
        assert [(ident, page) for ident, page, _ in turn] == [(changed, 1), (changed, 2), (following, 1)]
    assert sum(h["system_FE"] for h in playback["holds"]) == 4''',
    old_counts: '''    assert {p["id"] for p in rendered["pagination_changes"]} == {
        f"DK4_MES_B{b}_R{n:04d}" for b, n in ((74,58),(77,36),(77,45),(79,14),(79,61),(79,67),(79,71))}
    letter = {row["id"]: row["english"] for row in draft["records"] if row["block"] == 77}
    for a, b in ((33, 42), (36, 45)):
        intro = letter[f"DK4_MES_B77_R{a:04d}"].split("'", 2)
        other = letter[f"DK4_MES_B77_R{b:04d}"].split("'", 2)
        assert len(intro) == len(other) == 3 and intro[1] == other[1]
        assert (intro[0], intro[2]) != (other[0], other[2])''',
    'assert pages_saved() == 5': 'assert pages_saved() == 7',
    'len(group["commands"]) for group in groups.values()) == 241': 'len(group["commands"]) for group in groups.values()) == 337',
    '== len(draft["records"]) == 128': '== len(draft["records"]) == 144',
    '{"wording": 47, "glyph": 5, "retention": 76}': '{"wording": 50, "glyph": 1, "retention": 93}',
    'in (("？", "?"), ("！？", "!?"))': '== ("…?", "...?")',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1021 and len(checks) == 356': 'len(batches) == 1022 and len(checks) == 357',
    'previously_localized_records=128, contextual_records_revisited=125, contextual_decisions_reused=3':
        'previously_localized_records=144, contextual_records_revisited=140, contextual_decisions_reused=4',
    'prose_revisions=47': 'prose_revisions=50',
    'justified_retentions=73': 'justified_retentions=89',
    'prior_records_reviewed=125, contextual_decisions_reused=3': 'prior_records_reviewed=140, contextual_decisions_reused=4',
    'text_display_revisions=5': 'text_display_revisions=1',
    'punctuation_glyph_corrections=5': 'punctuation_glyph_corrections=1',
    'two_page_count_explanations=0': 'two_page_count_explanations=2',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hangzhou, the king's letter and Sera's return

The [testing ROM](../../{ROM.as_posix()}) includes the ten reviewed story blocks. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B65_B70", "hodram_B71_B80").replace("initialized_Hodram_B65_B70", "initialized_Hodram_B71_B80").replace(
    "verified_hodram_B61_B64_predecessor", "verified_hodram_B65_B70_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B65_B70_FOCUSED_ONLY.nds': 'Hodram_B71_B80_FOCUSED_ONLY.nds',
    'Preserve the candidate with Sera’s farewell and the Batavia exchanges':
        'Preserve the Hangzhou, royal letter and Sera return candidate',
    notes: '''    DOC.write_text(f"""# Hangzhou, the king's letter and Sera's return

The complete source packet covers 144 records. Four earlier decisions carry forward. The review updates 50 lines and one reaction glyph and identifies 89 lines whose wording already works. Maria's bargain retains the term wako and the offer of trading rights. Gerhard and Charles read the same formal order and keep distinct voices outside the quotation. Hayreddin retains his pride and shame. Sera returns with her compatriots, speaks in short beats, and chooses to stay. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Seven passages now fit on one page each. Two still need a continuation page, with complete sentences at each turn. The stored checks cover 337 commands. Native and visual review covers {native_count()} revised pages, nine variant pages for custom names, four speakerless notices and 11 speaker labels. Focused emulator excerpts verified {observed_count()} pages, both remaining two-page transitions, the four notices and Sera and Sirwood's three symbol passages. Natural triggers and hardware remain unvisited for these scenes. [Display verification](../{VERIFY.as_posix()})

The candidate preserves 114 accepted layers and the registered ASCII right boundary correction. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B65_B70", "hodram_B71_B80").replace("B65_B70_staged", "B71_B80_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-war-dialogue", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
