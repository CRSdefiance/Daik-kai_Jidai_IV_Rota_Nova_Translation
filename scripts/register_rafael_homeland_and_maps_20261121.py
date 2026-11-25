"""Register Rafael's homeland encounters, Charlotte's message and map discoveries."""

from types import SimpleNamespace

from scripts import register_rafael_palace_and_alliance_20261121 as parent
from scripts import replay_rafael_homeland_and_maps_20261121 as live
from scripts import verify_rafael_homeland_and_maps_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, workflow = display.stage, parent.base, parent.native, parent.workflow
PROFILE = "all-routes-rafael-homeland-and-maps-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_homeland_and_maps_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Homeland_And_Maps_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_homeland_and_maps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_homeland_and_maps_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
CHANGED = tuple(range(150, 161))
CHECKPOINT = "Reviewed 287 Rafael records across eleven encounters, including 152 wording revisions, 18 punctuation glyph corrections, two wrap-only fixes and 115 justified retentions."
guard_spec = parent.guard_spec


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 6 and sorted(m["count"] for m in rendered["menus"]) == [2, 2, 2]':
        'rendered["FE_panels"] == 0 and sorted(m["count"] for m in rendered["menus"]) == [2]',
    'not rendered["style_objects"] and len(rendered["full_name_retention_cases"]) == 2':
        'not rendered["style_objects"] and not rendered["full_name_retention_cases"]',
    'len(playback["holds"]) == 43 and len(playback["menus"]) == 6 and playback["reused_speech_samples"] == 29':
        'len(playback["holds"]) == 37 and len(playback["menus"]) == 2 and playback["reused_speech_samples"] == 29',
    'len(name_check["records"]) == 13': 'len(name_check["records"]) == 14',
    'len(group["commands"]) for group in groups.values()) == 552': 'len(group["commands"]) for group in groups.values()) == 529',
    '    assert base.load(stage.GUARD)["source25_predecessor_receipt"] == prior_guard': '    assert prior_guard == guard_spec()',
    '''    terms = base.load(TERMS)
    assert terms["candidate_sha256"] == candidate and terms["ARM9_sha256"] == native.digest(arm)
    assert [row["installed"] for row in terms["terms"]] == ["Declare War", "Send Documents", "First Mate"]
''': '',
    'startup = parent.parent.parent.parent.startup_check': 'startup = parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 270': '== len(draft["records"]) == 287',
    '{"wording": 165, "retention": 105}': '{"wording": 170, "wrap": 2, "retention": 115}',
    '''    assert GLYPHS <= {row["id"] for row in draft["records"] if row["decision"] == "revision"}
    draft["punctuation_glyph_corrections"] = sorted(GLYPHS)''':
        '''    translation = str.maketrans({"！": "!", "？": "?", "…": "..."})
    glyphs = [r["id"] for r in draft["records"] if r["finding"] == "wording"
              and r["previous_English"].translate(translation).replace("!?", "?!") == r["english"]]
    assert len(glyphs) == 18
    draft["punctuation_glyph_corrections"] = glyphs''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_rescue_and_lessons_predecessor": "verified_rafael_palace_and_alliance_predecessor",
    "len(batches) == 1006 and len(checks) == 341": "len(batches) == 1007 and len(checks) == 342",
    "previously_localized_records=270, new_contextual_records=0, prose_revisions=160":
        "previously_localized_records=287, new_contextual_records=0, prose_revisions=152",
    "wrap_only_revisions=0, justified_retentions=105, name_label_revisions=0, text_display_revisions=5":
        "wrap_only_revisions=2, justified_retentions=115, name_label_revisions=0, text_display_revisions=18",
    "for source in (stage.PROOF, stage.GUARD, stage.GUARD_SC0, TERMS, STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, args.visual_review,":
        "for source in (stage.PROOF, STARTUP, QA, live.PROOF, display.PROOF, names.PROOF, args.visual_review,",
    "initialized_Rafael_palace_and_alliance=True": "initialized_Rafael_homeland_and_maps=True",
    "contextual_nameplate_retentions=13": "contextual_nameplate_retentions=14",
    "actual_menu_samples=6, actual_style_objects=0, exact_full_name_samples=2":
        "actual_menu_samples=2, actual_style_objects=0",
    "prior_records_reviewed=270": "prior_records_reviewed=287",
    "prose_revisions=160, punctuation_glyph_corrections=5, justified_retentions=105, wrap_only_revisions=0":
        "prose_revisions=152, punctuation_glyph_corrections=18, justified_retentions=115, wrap_only_revisions=2",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's homeland and map scenes

The [testing ROM](../../{ROM.as_posix()}) includes eleven reviewed scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_palace_and_alliance", "rafael_homeland_and_maps").replace(
    "verified_rafael_homeland_and_maps_predecessor", "verified_rafael_palace_and_alliance_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("palace_and_alliance_staged_v*/"': 'glob("homeland_and_maps_staged_v*/"',
    'glob("palace_and_alliance_staged_v*/focused_gameplay/Rafael_Palace_And_Alliance_RESEARCH_ONLY.nds")':
        'glob("homeland_and_maps_staged_v*/focused_gameplay/Rafael_Homeland_And_Maps_RESEARCH_ONLY.nds")',
    "Preserve the Rafael palace candidate": "Preserve the Rafael homeland candidate",
    notes: '''    DOC.write_text(f"""# Rafael's homeland and map scenes

The contextual pass covers 287 records across eleven encounters. The batch has 152 wording revisions, 18 punctuation glyph corrections, two wrap-only fixes and 115 justified retentions. The dispatch reports the Spanish king's accession to the Portuguese crown and the armed forces' apparent alignment. Pereira gives his obligations as governor, what he can offer against Kuhn and why he cannot fight Spain. Rafael treats the Proof of Conquest as his interpretation of Pereira's advice. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

The barkeep's choice preserves both results. The overheard exchanges keep separate the two officials' breakable cooperation, ambitions and suspicions. The map scenes preserve the regions, item names and the action that reveals each map. Charlotte's three panels start and end one quotation, and the private exchange preserves Eirene's name.

Native checks cover {native_count()} revised pages and both choice captions. Fourteen speaker labels have contextual decisions and exact name getter evidence. Focused emulator evidence covers {observed_count()} speech pages and two choice highlights. Eight pages were run from the final candidate. Twenty-nine earlier pages match the final installed text and renderer, including the three-part message. The excerpts also tested the return to port. Natural branch activation and hardware remain open. [Native and emulator evidence](../{VERIFY.as_posix()})

The seven exact format controls, six startup comparisons, 17 tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_palace_and_alliance", "rafael_homeland_and_maps")
scope = parent.scope | globals() | {"pages_saved": lambda: sum(
    row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])}
for code in (verification, build, commit):
    exec(compile(code, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
