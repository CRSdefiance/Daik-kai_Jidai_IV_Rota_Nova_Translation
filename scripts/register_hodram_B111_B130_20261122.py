"""Register the cathedral, villages, ruins, sailing lesson and Diogo encounter."""

from pathlib import Path
from types import SimpleNamespace

from scripts import register_hodram_B91_B110_20261122 as parent
from scripts import replay_hodram_B111_B130_20261122 as live
from scripts import verify_hodram_B111_B130_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-hodram-B111-B130-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_B111_B130_registered_20261122")
ROM = ROOT / "Translation_DS_Hodram_B111_B130_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_B111_B130_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_B111_B130_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (111,112,114,115,116,117,119,120,121,122,123,124,125,126,127,129,130)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec, startup_reference = parent.guard_spec, parent.startup_reference
CHECKPOINT = ("Revisited 323 Hodram records across Santiago Cathedral, the riddles and villages, "
              "the sailing lesson and the confrontation with Diogo. The pass revises 65 lines, "
              "corrects two punctuation glyphs and improves three wraps, with 253 justified retentions.")
PRIOR_CHOICES = Path("translations/hodram_B111_B130_contextual_final_review_v1.json")
native_count = type(parent.native_count)(parent.native_count.__code__, parent.native_count.__globals__ | {"display":display})
observed_count = type(parent.observed_count)(parent.observed_count.__code__, parent.observed_count.__globals__ | {"live":live})
pages_saved = type(parent.pages_saved)(parent.pages_saved.__code__, parent.pages_saved.__globals__ | {"display":display})
alias_source = checked_text(parent.alias_source, {
    'row["block"] == 91 and row["kind"] == "typed-choice-label"': 'row["kind"] == "typed-choice-label"',
    'len(aliases) == 2': 'len(aliases) == 15',
})
old_checks = parent.verification[parent.verification.index("    branch_check ="):
                                 parent.verification.index('    assert playback["initialized_excerpts"]')]
verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 7 and len(rendered["menus"]) == 1 and not rendered["style_objects"]':
        'rendered["FE_panels"] == 35 and len(rendered["menus"]) == 5 and len(rendered["style_objects"]) == 8',
    'rendered["revised_speech_pages"] == 61 and rendered["alternate_name_width_pages"] == 0':
        '''rendered["revised_speech_pages"] == 70 and rendered["alternate_name_width_pages"] == 3
    assert sum(len(g["slot_owner_sets"]) for g in rendered["style_objects"]) == 48
    assert all(sum(map(len, g["slot_owner_sets"])) == 8 for g in rendered["style_objects"])''',
    'draft["contextual_records_revisited"] == 209 and draft["contextual_decisions_reused"] == 2':
        'draft["contextual_records_revisited"] == 323 and draft["contextual_decisions_reused"] == 0',
    'len(playback["holds"]) == len(live.SELECTED) and len(playback["menus"]) == 2':
        'len(playback["holds"]) == len(live.SELECTED)-3 == 62 and len(playback["menus"]) == 9',
    old_checks: '''    assert [(m["block"],m["highlight"]) for m in playback["menus"]] == [
        (block, slot) for block in live.MENU_BLOCKS for slot in range(3)]
    assert set(playback["page_transitions"]) == {live.PAGE_TURN[0], live.DIOGO_TURN[0]}
    assert len(playback["observed_style_owners"]) == 2 and pages_saved() == 5
    assert sum(h["system_FE"] for h in playback["holds"]) == 13
    assert sorted((m["block"],m["count"]) for m in rendered["menus"]) == [
        (114,3),(114,3),(114,3),(118,3),(119,3)]
''',
    'len(name_check["records"]) == 15': 'len(name_check["records"]) == 24',
    ' + branch_check["sheets"]': '',
    ' | branch_check["evidence"]': '',
    'len(group["commands"]) for group in groups.values()) == 287': 'len(group["commands"]) for group in groups.values()) == 562',
    '== len(draft["records"]) == 211': '== len(draft["records"]) == 323',
    '{"wording": 59, "wrap-only": 1, "retention": 151}': '{"wording": 65, "wrap-only": 3, "glyph": 2, "retention": 253}',
    '''    assert not writer.author.GLYPHS
    draft["punctuation_glyph_corrections"] = []
    draft["complete_initialized_choice_replay"] = dict(path=str(branches.PROOF), sha256=base.digest(branches.PROOF))
''': '''    glyphs = [row["id"] for row in draft["records"] if row["change_class"] == "glyph"
              and (row["previous_English"], row["english"]) == ("…", "...")]
    assert glyphs == ["DK4_MES_B123_R0127", "DK4_MES_B123_R0142"]
    draft["punctuation_glyph_corrections"] = glyphs
''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1024 and len(checks) == 359': 'len(batches) == 1025 and len(checks) == 360',
    'previously_localized_records=211': 'previously_localized_records=323',
    'contextual_records_revisited=209, contextual_decisions_reused=2':
        'contextual_records_revisited=323, contextual_decisions_reused=0',
    'prior_records_reviewed=209, contextual_decisions_reused=2':
        'prior_records_reviewed=323, contextual_decisions_reused=0',
    'prose_revisions=59': 'prose_revisions=65',
    'justified_retentions=149': 'justified_retentions=253',
    'text_display_revisions=0': 'text_display_revisions=2',
    'punctuation_glyph_corrections=0': 'punctuation_glyph_corrections=2',
    'wrap_only_revisions=1': 'wrap_only_revisions=3',
    'two_page_count_explanations=1': 'two_page_count_explanations=sum(len(t)==3 for t in base.load(live.PROOF)["page_transitions"].values())',
    'contextual_nameplate_retentions=15': 'contextual_nameplate_retentions=24',
    'actual_menu_samples=2, complete_choice_outcomes=2': 'actual_menu_samples=9',
    'actual_style_objects=0': 'actual_style_objects=2',
    'names.PROOF, branches.PROOF, args.visual_review': 'names.PROOF, args.visual_review',
    'complete_choice_replay_sha256=base.digest(branches.PROOF), ': '',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's villages, riddles, sailing lesson and New World encounter

The [testing ROM](../../{ROM.as_posix()}) includes all previously registered layers and the new dialogue review. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("hodram_B91_B110","hodram_B111_B130").replace("initialized_Hodram_B91_B110","initialized_Hodram_B111_B130").replace(
    "verified_hodram_B81_B89_predecessor","verified_hodram_B91_B110_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'Hodram_B91_B110_FOCUSED_ONLY.nds': 'Hodram_B111_B130_FOCUSED_ONLY.nds',
    ', *sorted(stage.ROOT.parent.glob("B91_B110_staged*/branch_gameplay/Hodram_B91_COMPLETE_RESEARCH_ONLY.nds"))': '',
    'Preserve the miracle, treasure and priest dialogue candidate': 'Preserve the Hodram villages, riddles and sailing candidate',
    notes: '''    DOC.write_text(f"""# Hodram's villages, riddles, sailing lesson and New World encounter

Reviewed 323 records, with 65 wording revisions, two punctuation glyph fixes, three wrap-only changes and 253 justified retentions. The cathedral visit and village rescue preserve the speakers' relationships. The Sphinx and Colosseum retain the original riddle logic and choices. Maria's exchange at Sao Jorge distinguishes the people responsible for slave trading and plunder from the general population. Rafael addresses Hodram by the original substitution in the knife scene. Diogo greets Hodram by surname without inventing a rank. [Exact source, stored text and decisions](../{REVIEW.as_posix()})

Native checks covered all 562 inventoried commands in the 19 dialogue blocks, along with 48 physical style bodies across 64 slots, 15 menu captions, 35 speakerless panels, 24 nameplates and {native_count()} revised pages. The second Sphinx riddle keeps its final question together. The sailing tutorial keeps key controls and stop instructions readable. Initialized emulator excerpts verified {observed_count()} pages, three positions each in three menus, two B125 voice variants, the Rafael and Hodram identities, and the transition to the next speaker after Maria's and Diogo's speeches. Five speeches now fit on one page. Natural triggers and hardware remain unvisited. [Native and gameplay evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves all 114 accepted layers, the ASCII right-bound correction and the existing name glyph fixes. The startup comparison, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("hodram_B91_B110","hodram_B111_B130").replace("B91_B110_staged","B111_B130_staged")


scope = parent.scope | globals()
for source in (alias_source, verification, build, commit):
    exec(compile(source, __file__ + "::registered-riddles-and-sailing", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

