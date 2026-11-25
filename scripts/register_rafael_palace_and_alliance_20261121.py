"""Register Rafael's palace, naval combat lesson and alliance dialogue."""

from types import SimpleNamespace

from scripts import register_rafael_rescue_and_lessons_20261121 as parent
from scripts import replay_rafael_palace_and_alliance_20261121 as live
from scripts import verify_rafael_palace_and_alliance_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, workflow = display.stage, parent.base, parent.native, parent.workflow
PROFILE = "all-routes-rafael-palace-and-alliance-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_palace_and_alliance_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Palace_And_Alliance_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_palace_and_alliance_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_palace_and_alliance_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
TERMS = EVIDENCE / "campaign_lesson_terms.json"
names = SimpleNamespace(PROOF=display.NAMES)
CHANGED = tuple(range(141, 150))
GLYPHS = {"DK4_MES_B143_R0311", "DK4_MES_B145_R0093", "DK4_MES_B145_R0140",
          "DK4_MES_B147_R0062", "DK4_MES_B148_R0017"}
CHECKPOINT = "Reviewed 270 Rafael records across nine encounters, with 160 wording revisions, five punctuation glyph corrections and 105 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def guard_spec():
    return dict(path=str(stage.GUARD), sha256=base.digest(stage.GUARD))


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 15 and sorted(m["count"] for m in rendered["menus"]) == [2, 2, 2, 2, 2]':
        'rendered["FE_panels"] == 6 and sorted(m["count"] for m in rendered["menus"]) == [2, 2, 2]',
    'len(rendered["style_objects"]) == 6 and sum(len(o["slot_owner_sets"]) for o in rendered["style_objects"]) == 34':
        'not rendered["style_objects"] and len(rendered["full_name_retention_cases"]) == 2',
    'len(playback["holds"]) == 43 and len(playback["menus"]) == 4 and playback["prior_speech_samples_reused"] == 39':
        'len(playback["holds"]) == 43 and len(playback["menus"]) == 6 and playback["reused_speech_samples"] == 29',
    'len(name_check["records"]) == 22': 'len(name_check["records"]) == 13',
    'len(group["commands"]) for group in groups.values()) == 544': 'len(group["commands"]) for group in groups.values()) == 552',
    '    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]\n'
    '    controls = bind_registered_story_percent_guard(guard)(source, final)':
        '    prior_guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]\n'
        '    assert base.load(stage.GUARD)["source25_predecessor_receipt"] == prior_guard\n'
        '    controls = bind_registered_story_percent_guard(guard_spec())(source, final)',
    '    assert controls == stored["source25"]':
        '''    assert controls == stored["source25"] and controls["total_exact_source_bound_relocated_leading25_count"] == 7
    terms = base.load(TERMS)
    assert terms["candidate_sha256"] == candidate and terms["ARM9_sha256"] == native.digest(arm)
    assert [row["installed"] for row in terms["terms"]] == ["Declare War", "Send Documents", "First Mate"]''',
    'startup = parent.parent.parent.startup_check': 'startup = parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 351': '== len(draft["records"]) == 270',
    '{"wording": 146, "wrap": 1, "retention": 204}': '{"wording": 165, "retention": 105}',
    '''    coverage = rendered["prior_ordinary_sailing_coverage"]
    assert len(coverage["exact_prior_observed_record_ids"]) == 40
    assert base.digest(coverage["path"]) == coverage["sha256"]
    draft["prior_ordinary_sailing_coverage"] = coverage''':
        '''    assert GLYPHS <= {row["id"] for row in draft["records"] if row["decision"] == "revision"}
    draft["punctuation_glyph_corrections"] = sorted(GLYPHS)''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_ruins_and_proof_predecessor": "verified_rafael_rescue_and_lessons_predecessor",
    "len(batches) == 1005 and len(checks) == 340": "len(batches) == 1006 and len(checks) == 341",
    "previously_localized_records=351, new_contextual_records=0, prose_revisions=146":
        "previously_localized_records=270, new_contextual_records=0, prose_revisions=160",
    "wrap_only_revisions=1, justified_retentions=204, name_label_revisions=0, text_display_revisions=0":
        "wrap_only_revisions=0, justified_retentions=105, name_label_revisions=0, text_display_revisions=5",
    "choice_label_revisions=2, name_consistency_revisions=0": "choice_label_revisions=0, name_consistency_revisions=0",
    "choice_label_revisions=2, pagination_fixes=pages_saved()": "choice_label_revisions=0, pagination_fixes=pages_saved()",
    "    with mapped(base.REGISTRY) as data:\n        write_update(data, registry_next,":
        '    profile["source25_multiarchive_guard"] = guard_spec()\n'
        "    with mapped(base.REGISTRY) as data:\n        write_update(data, registry_next,",
    "for source in (stage.PROOF, STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, args.visual_review,":
        "for source in (stage.PROOF, stage.GUARD, stage.GUARD_SC0, TERMS, STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, args.visual_review,",
    "initialized_Rafael_rescue_and_lessons=True": "initialized_Rafael_palace_and_alliance=True",
    "contextual_nameplate_retentions=22": "contextual_nameplate_retentions=13",
    "actual_menu_samples=4, actual_style_objects=4, exact_prior_ordinary_sailing_records=40":
        "actual_menu_samples=6, actual_style_objects=0, exact_full_name_samples=2",
    "prior_records_reviewed=351": "prior_records_reviewed=270",
    "prose_revisions=146, justified_retentions=204, wrap_only_revisions=1":
        "prose_revisions=160, punctuation_glyph_corrections=5, justified_retentions=105, wrap_only_revisions=0",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's palace and alliance scenes

The [testing ROM](../../{ROM.as_posix()}) includes nine reviewed scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_rescue_and_lessons", "rafael_palace_and_alliance").replace(
    "verified_rafael_palace_and_alliance_predecessor", "verified_rafael_rescue_and_lessons_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_v*/"': 'glob("palace_and_alliance_staged_v*/"',
    'glob("staged_v*/focused_gameplay/Rafael_Rescue_And_Lessons_RESEARCH_ONLY.nds")':
        'glob("palace_and_alliance_staged_v*/focused_gameplay/Rafael_Palace_And_Alliance_RESEARCH_ONLY.nds")',
    "Preserve the Rafael rescue candidate": "Preserve the Rafael palace candidate",
    notes: '''    DOC.write_text(f"""# Rafael's palace and alliance scenes

The review covers 270 records across nine encounters. There are 160 wording revisions, five punctuation glyph corrections and 105 justified retentions. Albuquerque's orders preserve Espinosa's region, the role of the military investigation, the exact 50,000 gold grant and the limits on direct intervention. Silveira's lesson explains the two ways to start a war and when a victory lets the player take a contract and invest. It retains the special rule for a rival's home base. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

The tablet exchanges keep the exact item names and make clear when a map appears. Eirene explains her alias and why she chose to disguise herself. In Uddin's two outcomes, the reply opens either the Nagalpur agreement with its later nonaggression pact or the competition for the Indian Ocean. All three typed menus kept their installed captions and result slots.

Native checks covered {native_count()} revised speech and notice pages, all six captions and both full-name substitutions. Six speeches now fit on one page. The focused emulator proof covers {observed_count()} pages and six menu highlights, including 14 pages replayed on the final candidate and 29 earlier samples with identical installed text and rendering dependencies. Thirteen nameplates and role labels were reviewed. The original four-archive format check passed with all seven source-bound speaker controls. Natural branch activation and hardware still await gameplay coverage. [Native and emulator evidence](../{VERIFY.as_posix()})

Six startup comparisons, 17 tests and the exact clean-input rebuild passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_rescue_and_lessons", "rafael_palace_and_alliance")
scope = parent.scope | globals() | {"pages_saved": lambda: sum(
    row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])}
for code in (verification, build, commit):
    exec(compile(code, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
