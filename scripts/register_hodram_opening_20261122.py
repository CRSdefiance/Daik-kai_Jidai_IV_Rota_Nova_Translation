"""Register the reviewed Hodram exchanges and their clean-input patch."""

from types import SimpleNamespace

from scripts import register_rafael_B306_B309_20261122 as parent
from scripts import replay_hodram_opening_20261122 as live
from scripts import verify_hodram_opening_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B24-B53-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B24_B53_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B24_B53_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B24_B53_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B24_B53_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (24, 25, 26, 27, 41, 42, 44, 46, 47, 48, 49, 50, 52, 53)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Revisited 118 early Hodram lines, with 54 wording revisions and 64 justified retentions. The exact B24–53 packet also carries 193 recent decisions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


def verify_existing_credit(records, credited):
    census = base.load(writer.paired.CENSUS)
    assert not census["missing"] and not census["legacy_source_bindings_not_exact"]
    source = {row["id"]: row for row in census["records"]}
    missing = {row["id"]: row for row in records if (row["file_path"], row["id"]) not in credited}
    assert set(missing) == {"SC1_B49_CHOICE_574_0", "SC1_B49_CHOICE_574_1",
                            "SC1_B52_CHOICE_68_0", "SC1_B52_CHOICE_68_1"}
    result = {}
    for ident, row in missing.items():
        origin = source[ident]
        binding, = origin["exact_credited_source_bindings"]
        assert row["kind"] == "typed-choice-label" and row["decision"] == "retention"
        assert row["block"] == origin["block"] == binding["block"]
        assert row["source_hex"] == origin["source_hex"] == binding["source_hex"]
        assert row["source_reference"]["offset"] == origin["source_reference"]["offset"] == binding["offset"]
        assert (row["file_path"], binding["id"]) in credited
        result[ident] = binding
    return result


verification = checked_text(parent.verification, {
    'assert not rendered["FE_panels"] and not rendered["menus"] and not rendered["style_objects"]':
        'assert rendered["FE_panels"] == 9 and len(rendered["menus"]) == 2 and len(rendered["style_objects"]) == 1',
    'assert rendered["revised_speech_pages"] == 17': 'assert rendered["revised_speech_pages"] == 54',
    'draft["contextual_records_revisited"] == 53 and draft["contextual_decisions_reused"] == 8':
        'draft["contextual_records_revisited"] == 118 and draft["contextual_decisions_reused"] == 2',
    'len(playback["holds"]) == len(live.SELECTED) and not playback["menus"]':
        'len(playback["holds"]) == len(live.SELECTED) - 2 and len(playback["menus"]) == 4',
    'len(name_check["records"]) == 5': 'len(name_check["records"]) == 10',
    '    assert viewed ==': '''    aliases = base.load(live.ALIASES)
    assert aliases["candidate_sha256"] == candidate and aliases["gameplay_report_sha256"] == base.digest(live.PROOF)
    assert aliases["exact_full_nameplate_glyphs"]
    assert viewed ==''',
    'len(group["commands"]) for group in groups.values()) == 117': 'len(group["commands"]) for group in groups.values()) == 305',
    'tuple(groups) == stage.review.BLOCKS[0]': 'tuple(groups) == stage.review.BLOCKS[1]',
    '== len(draft["records"]) == 61': '== len(draft["records"]) == 120',
    '{"wording": 17, "retention": 44}': '{"wording": 54, "retention": 66}',
    '    validate_natural_dialogue_batch(draft)':
        '    draft["encoder"] = "dialogue-relocatable-v1"\n    validate_natural_dialogue_batch(draft)',
})
startup_reference = parent.startup_reference

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1016 and len(checks) == 351': 'len(batches) == 1017 and len(checks) == 352',
    'previously_localized_records=61, contextual_records_revisited=53, contextual_decisions_reused=8':
        'previously_localized_records=120, contextual_records_revisited=118, contextual_decisions_reused=2',
    'prose_revisions=17': 'prose_revisions=54',
    'justified_retentions=36': 'justified_retentions=64',
    'prior_records_reviewed=53, contextual_decisions_reused=8': 'prior_records_reviewed=118, contextual_decisions_reused=2',
    'contextual_nameplate_retentions=5': 'contextual_nameplate_retentions=10',
    'actual_menu_samples=0, actual_style_objects=0': 'actual_menu_samples=4, actual_style_objects=1',
    'initialized_Rafael_B306_B309=True': 'initialized_Hodram_B24_B53=True',
    'assert len(credited) == 27700 and all((r["file_path"], r["id"]) in credited for r in draft["records"])':
        'assert len(credited) == 27700\n        prior_caption_keys = verify_existing_credit(draft["records"], credited)',
    'observed_Rafael_panels=observed_count()': 'observed_Hodram_panels=observed_count(), credited_choice_aliases=prior_caption_keys',
    'STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, args.visual_review,':
        'STARTUP, QA, live.PROOF, live.ALIASES, display.PROOF, names.PROOF, args.visual_review,',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's early exchanges

The [testing ROM](../../{ROM.as_posix()}) includes Hodram's reviewed Baltic speech, Lil's North Sea challenge, and early encounters. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B306_B309", "hodram_B24_B53").replace(
    "verified_rafael_B261_B280_predecessor", "verified_rafael_B306_B309_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B306_B309*/"': 'glob("staged*/"',
    'glob("staged_B306_B309*/focused_gameplay/Rafael_B306_B309_FOCUSED_ONLY.nds"':
        'glob("staged*/focused_gameplay/Hodram_B24_B53_FOCUSED_ONLY.nds"',
    "Preserve Rafael's Istanbul remedy and hidden-village candidate": "Preserve the early Hodram contextual candidate",
    notes: '''    DOC.write_text(f"""# Hodram's Baltic speech and Lil's North Sea challenge

The complete B24–53 packet ties 311 records to the clean Japanese and the prior candidate. It carries 193 recent decisions, including the combat lesson, Baltic trade lesson and Alexandria warning. The fresh pass records 54 wording revisions and 64 individual retentions. It restores differences among the monster-fish reactions, preserves the scope of Sweden's naval plans, and keeps Lil's argument, contest and barter distinct. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Stored checks cover 305 commands in the 15 reviewed blocks, including all seven lookout bodies and their eight-slot map. Native display checks cover all 54 revised pages, four captions, nine speakerless panels and ten fixed nameplates. Focused emulator excerpts show {observed_count()} dialogue pages and four menu highlights. Original branch destinations were tested offline. Natural triggering and hardware remain unvisited for this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers, the ASCII right-bound correction and seven source-format controls. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B306_B309", "hodram_B24_B53")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-Hodram-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
