"""Register the Miracle Bullet Charm, treasure rumors, and the priest's blessing."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_hodram_B81_B89_20261122 as parent
from scripts import replay_hodram_B91_B110_20261122 as live
from scripts import verify_hodram_B91_B110_20261122 as display
from scripts import verify_hodram_B91_branches_20261122 as branches
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B91-B110-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B91_B110_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B91_B110_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B91_B110_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B91_B110_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (91, 92, 93, 95, 97, 100, 101, 102, 103, 104, 105, 108, 110)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Revisited 209 Hodram records across the Miracle Bullet Charm, Emilio's food scenes, treasure "
              "rumors and the priest's Proof of Conquest. The pass revises 59 lines and one wrap, with "
              "149 justified retentions and two exact earlier decisions carried forward.")
PRIOR_CHOICES = Path("translations/hodram_B91_B110_contextual_final_review_v1.json")
native_count = type(parent.native_count)(parent.native_count.__code__, parent.native_count.__globals__ | {"display": display})
observed_count = type(parent.observed_count)(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live": live})
pages_saved = type(parent.pages_saved)(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display": display})
alias_source = checked_text(getsource(parent.bind_choice_aliases), {'row["block"] == 87': 'row["block"] == 91'})

old_checks = parent.verification[parent.verification.index('    assert [m["highlight"]'):
                                 parent.verification.index('    assert playback["initialized_excerpts"]')]
glyph_check = parent.verification[parent.verification.index("    glyphs ="):
                                  parent.verification.index('    draft["historical_choice_credit"]')]
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 5': 'rendered["FE_panels"] == 7',
    'rendered["revised_speech_pages"] == 71 and rendered["alternate_name_width_pages"] == 12':
        'rendered["revised_speech_pages"] == 61 and rendered["alternate_name_width_pages"] == 0',
    'draft["contextual_records_revisited"] == 297 and draft["contextual_decisions_reused"] == 9':
        'draft["contextual_records_revisited"] == 209 and draft["contextual_decisions_reused"] == 2',
    'len(playback["holds"]) == len(live.SELECTED) - 1': 'len(playback["holds"]) == len(live.SELECTED)',
    old_checks: '''    branch_check = base.load(branches.PROOF)
    assert branch_check["candidate_sha256"] == candidate and branch_check["initialized_complete_script"]
    assert branch_check["exact_visible_notice_masks"] and not branch_check["natural_activation"]
    assert not branch_check["hardware_verified"]
    for answer, numbers in branches.NOTICE_PAIRS.items():
        assert [r["id"] for r in branch_check["outcomes"][answer]["notices"]] == [
            f"DK4_MES_B91_R{n:04d}" for n in numbers]
    assert [m["highlight"] for m in playback["menus"]] == [0, 1]
    assert all(m["block"] == 91 for m in playback["menus"])
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.SHORTER_TURN[0]}
    assert playback["dynamic_nameplates"] == sorted(display.DYNAMIC_ROLE)
    assert sum(h["system_FE"] for h in playback["holds"]) == 7
    assert pages_saved() == 5 and all(p["previous_pages"] == 2 and p["current_pages"] == 1
                                      for p in rendered["pagination_changes"])
    assert rendered["menus"][0]["record_ids"] == ["SC1_B91_CHOICE_112_0", "SC1_B91_CHOICE_112_1"]
''',
    'len(name_check["records"]) == 21': 'len(name_check["records"]) == 15',
    'for s in rendered["sheets"] + playback["sheets"]': 'for s in rendered["sheets"] + playback["sheets"] + branch_check["sheets"]',
    '(viewed | playback["evidence"]).items()': '(viewed | playback["evidence"] | branch_check["evidence"]).items()',
    'len(group["commands"]) for group in groups.values()) == 517': 'len(group["commands"]) for group in groups.values()) == 287',
    '== len(draft["records"]) == 306': '== len(draft["records"]) == 211',
    '{"wording": 68, "glyph": 2, "wrap-only": 1, "retention": 235}': '{"wording": 59, "wrap-only": 1, "retention": 151}',
    glyph_check: '''    assert not writer.author.GLYPHS
    draft["punctuation_glyph_corrections"] = []
    draft["complete_initialized_choice_replay"] = dict(path=str(branches.PROOF), sha256=base.digest(branches.PROOF))
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1023 and len(checks) == 358': 'len(batches) == 1024 and len(checks) == 359',
    'previously_localized_records=306': 'previously_localized_records=211',
    'contextual_records_revisited=297, contextual_decisions_reused=9':
        'contextual_records_revisited=209, contextual_decisions_reused=2',
    'prior_records_reviewed=297, contextual_decisions_reused=9': 'prior_records_reviewed=209, contextual_decisions_reused=2',
    'prose_revisions=68': 'prose_revisions=59',
    'justified_retentions=226': 'justified_retentions=149',
    'text_display_revisions=2': 'text_display_revisions=0',
    'punctuation_glyph_corrections=2': 'punctuation_glyph_corrections=0',
    'two_page_count_explanations=0': 'two_page_count_explanations=1',
    'contextual_nameplate_retentions=21': 'contextual_nameplate_retentions=15',
    'actual_menu_samples=2': 'actual_menu_samples=2, complete_choice_outcomes=2',
    'live.PROOF, display.PROOF, names.PROOF, args.visual_review':
        'live.PROOF, display.PROOF, names.PROOF, branches.PROOF, args.visual_review',
    'native_and_emulator_evidence_sha256=base.digest(live.PROOF),':
        'native_and_emulator_evidence_sha256=base.digest(live.PROOF),\n'
        '            complete_choice_replay_sha256=base.digest(branches.PROOF),',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's miracle charm, treasure rumors and Proof of Conquest

The [testing ROM](../../{ROM.as_posix()}) includes the 14 reviewed story blocks. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B81_B89", "hodram_B91_B110").replace("initialized_Hodram_B81_B89", "initialized_Hodram_B91_B110").replace(
    "verified_hodram_B71_B80_predecessor", "verified_hodram_B81_B89_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B81_B89_FOCUSED_ONLY.nds': 'Hodram_B91_B110_FOCUSED_ONLY.nds',
    '*earlier, *research)': '*earlier, *research, *sorted(stage.ROOT.parent.glob("B91_B110_staged*/branch_gameplay/Hodram_B91_COMPLETE_RESEARCH_ONLY.nds")))',
    'Preserve the settlement, recruitment, rescue and crown candidate':
        'Preserve the miracle, treasure and priest dialogue candidate',
    notes: '''    DOC.write_text(f"""# Hodram's miracle charm, treasure rumors and Proof of Conquest

Revisited 209 records from the clean Japanese and carried forward two exact earlier decisions. This pass revises 59 lines and one wrap, with 149 individual retentions. The sailor's apology and gift follow his challenge to Hodram's beliefs. Emilio's chewing and pursuit of the banana keep their distinct comic timing. Angelo starts the nukenin dispute, Samwell supplies the animal-themed rumors, and Julio stays unsure where the Minerva Shield lies. The priest's final question, test of resolve, directions about the two Map Keys and blessing keep their original progression. [Exact Japanese and per-record decisions](../{REVIEW.as_posix()})

Native and visual checks covered {native_count()} revised pages, seven speakerless panels, 16-cell captain-name variants, two choice captions and 15 nameplates. Five long speeches now fit on one page and Julio's shield story turns at a complete question. The archive check verified all 287 original commands. Focused emulator excerpts verified {observed_count()} dialogue pages and both menu highlights. Cold boots through the complete initialized charm script showed both characters' Luck notices after acceptance and both Spirit notices after declining. Original world triggers and hardware remain unvisited. [Display and emulator evidence](../{VERIFY.as_posix()})

The candidate preserves all 114 accepted layers, the ASCII right-bound correction and the registered regular-font F. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B81_B89", "hodram_B91_B110").replace("B81_B89_staged", "B91_B110_staged")


scope = parent.scope | globals()
for source in (alias_source, verification, build, commit):
    exec(compile(source, __file__ + "::registered-treasure-dialogue", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

