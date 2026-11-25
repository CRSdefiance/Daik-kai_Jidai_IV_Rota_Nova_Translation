"""Register the Black Sea, recruitment, rescue, and Silla Gold Crown review."""

from pathlib import Path
from types import SimpleNamespace

from scripts import register_hodram_B71_B80_20261122 as parent
from scripts import replay_hodram_B81_B89_20261122 as live
from scripts import verify_hodram_B81_B89_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B81-B89-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B81_B89_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B81_B89_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B81_B89_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B81_B89_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (81, 82, 84, 85, 86, 87, 88, 89)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Revisited 297 Hodram records across the Black Sea settlement, recruitment, rescue and crown scenes. "
              "The review revises 68 lines, corrects two glyphs and improves one wrap, "
              "with 226 justified retentions and nine exact decisions carried forward.")
PRIOR_CHOICES = Path("translations/hodram_B81_B89_contextual_final_review_v1.json")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


def bind_choice_aliases(draft):
    old = {row["id"]: row for row in base.load(PRIOR_CHOICES)["records"]
           if row["block"] == 87 and row["kind"] == "typed-choice-label"}
    aliases = {}
    for row in draft["records"]:
        if row["kind"] != "typed-choice-label":
            continue
        ident = row["id"]
        alias = ident.replace("_CHOICE_", "_NATIVE_CHOICE_")
        prior = old.pop(alias)
        assert all(prior["review"].values()) and row["decision"] == "retention"
        assert row["english"] == prior["english"] and row["source_hex"] == prior["source_hex"]
        for field in ("offset", "command_offset"):
            assert row["source_reference"][field] == prior["source_reference"][field]
        assert row["native_slots"] == [prior["source_reference"]["source_index"]]
        aliases[ident] = alias
    assert not old and len(aliases) == 2
    return dict(prior_review=str(PRIOR_CHOICES), prior_sha256=base.digest(PRIOR_CHOICES), by_census_id=aliases)


old_turns = parent.verification[parent.verification.index("    for turn, (changed, following)"):
                                parent.verification.index('    assert set(playback["opaque_source_symbols"])')]
old_pages = parent.verification[parent.verification.index('    assert {p["id"]'):
                                parent.verification.index('    assert playback["initialized_excerpts"]')]
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 4 and not rendered["menus"] and not rendered["style_objects"]':
        'rendered["FE_panels"] == 5 and len(rendered["menus"]) == 1 and not rendered["style_objects"]',
    'rendered["revised_speech_pages"] == 53 and rendered["alternate_name_width_pages"] == 9':
        'rendered["revised_speech_pages"] == 71 and rendered["alternate_name_width_pages"] == 12',
    'draft["contextual_records_revisited"] == 140 and draft["contextual_decisions_reused"] == 4':
        'draft["contextual_records_revisited"] == 297 and draft["contextual_decisions_reused"] == 9',
    'len(playback["holds"]) == len(live.SELECTED) + 2 and not playback["menus"]':
        'len(playback["holds"]) == len(live.SELECTED) - 1 and len(playback["menus"]) == 2',
    old_turns: '''    assert [m["highlight"] for m in playback["menus"]] == [0, 1]
    assert all(m["block"] == 87 for m in playback["menus"])
    assert len(playback["exact_name_introductions"]) == 4
    assert sum(h["system_FE"] for h in playback["holds"]) == 5
''',
    old_pages: '''    assert rendered["pagination_changes"] == [
        dict(id="DK4_MES_B85_R0018", previous_pages=2, current_pages=1)]
    assert pages_saved() == 1
    assert rendered["menus"][0]["record_ids"] == ["SC1_B87_CHOICE_302_0", "SC1_B87_CHOICE_302_1"]
''',
    'len(name_check["records"]) == 11': 'len(name_check["records"]) == 21',
    'len(group["commands"]) for group in groups.values()) == 337': 'len(group["commands"]) for group in groups.values()) == 517',
    '== len(draft["records"]) == 144': '== len(draft["records"]) == 306',
    '{"wording": 50, "glyph": 1, "retention": 93}': '{"wording": 68, "glyph": 2, "wrap-only": 1, "retention": 235}',
    '== ("…?", "...?")': '== ("FI…", "FI...")',
    '    draft["encoder"]': '    draft["historical_choice_credit"] = bind_choice_aliases(draft)\n    draft["encoder"]',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1022 and len(checks) == 357': 'len(batches) == 1023 and len(checks) == 358',
    'previously_localized_records=144, contextual_records_revisited=140, contextual_decisions_reused=4':
        'previously_localized_records=306, contextual_records_revisited=297, contextual_decisions_reused=9',
    'prose_revisions=50': 'prose_revisions=68',
    'justified_retentions=89': 'justified_retentions=226',
    'prior_records_reviewed=140, contextual_decisions_reused=4': 'prior_records_reviewed=297, contextual_decisions_reused=9',
    'text_display_revisions=1': 'text_display_revisions=2',
    'wrap_only_revisions=0': 'wrap_only_revisions=1',
    'punctuation_glyph_corrections=1': 'punctuation_glyph_corrections=2',
    'two_page_count_explanations=2': 'two_page_count_explanations=0',
    'contextual_nameplate_retentions=11': 'contextual_nameplate_retentions=21',
    'actual_menu_samples=0': 'actual_menu_samples=2',
    '    assert all((row["file_path"], row["id"]) in credited for row in draft["records"])':
        '    aliases = draft["historical_choice_credit"]["by_census_id"]\n'
        '        assert all((row["file_path"], aliases.get(row["id"], row["id"])) in credited for row in draft["records"])',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# The Black Sea, recruitment and the Silla Gold Crown

The [testing ROM](../../{ROM.as_posix()}) includes the nine reviewed story blocks. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B71_B80", "hodram_B81_B89").replace("initialized_Hodram_B71_B80", "initialized_Hodram_B81_B89").replace(
    "verified_hodram_B65_B70_predecessor", "verified_hodram_B71_B80_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B71_B80_FOCUSED_ONLY.nds': 'Hodram_B81_B89_FOCUSED_ONLY.nds',
    'Preserve the Hangzhou, royal letter and Sera return candidate':
        'Preserve the settlement, recruitment, rescue and crown candidate',
    notes: '''    DOC.write_text(f"""# The Black Sea, recruitment and the Silla Gold Crown

Reviewed the full 306-record packet, including nine exact earlier decisions. This pass revises 68 lines, corrects two glyphs and fixes one wrap, with 226 individual retentions. Cristina's refusal of an arranged marriage stays firm. Her gratitude after Mivor's rescue leaves the relationship open. Janus's request stays at 1,000 gold and both captions retain their original wording and order. The complete exchanges distinguish Emilio's show from the main act, Yukihisa's polite intervention from Kurushima's accusations, and Julian's reason for wanting the crown. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Native and visual verification covers {native_count()} revised pages, 12 name-width variants, five speakerless panels, two choice captions and 21 nameplates. Cristina's first objection now fits on one page. All 517 original commands remain verified, including the menu's branch destinations. Focused emulator excerpts verified {observed_count()} dialogue pages and both menu highlights. The original scene triggers, choice outcomes in this candidate, and hardware remain unvisited. [Display verification](../{VERIFY.as_posix()})

The candidate preserves all 114 accepted layers, the registered ASCII right-bound correction and Emilio's regular-font F. Six startup comparisons, 17 regression tests, and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B71_B80", "hodram_B81_B89").replace("B71_B80_staged", "B81_B89_staged")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-recruitment-dialogue", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
