"""Register the reviewed rescue, companion and lesson dialogue over the existing stack."""

from types import SimpleNamespace

from scripts import register_rafael_ruins_and_proof_20261121 as parent
from scripts import replay_rafael_rescue_and_lessons_20261121 as live
from scripts import verify_rafael_rescue_and_lessons_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, workflow = display.stage, parent.base, parent.native, parent.workflow
PROFILE = "all-routes-rafael-rescue-and-lessons-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_rescue_and_lessons_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Rescue_And_Lessons_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_rescue_and_lessons_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_rescue_and_lessons_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
CHECKPOINT = "Reviewed 351 Rafael records across 18 encounters, with 146 wording revisions, one wrap-only fix and 204 justified retentions."
CHANGED = (121, 122, 123, 124, 125, 126, 127, 128, 129, 132, 133, 134, 135, 136, 138, 139)



def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 22 and sorted(m["count"] for m in rendered["menus"]) == [3, 3, 3, 3]':
        'rendered["FE_panels"] == 15 and sorted(m["count"] for m in rendered["menus"]) == [2, 2, 2, 2, 2]',
    'len(rendered["style_objects"]) == 2':
        'len(rendered["style_objects"]) == 6 and sum(len(o["slot_owner_sets"]) for o in rendered["style_objects"]) == 34',
    'len(playback["holds"]) >= 33 and len(playback["menus"]) == 5':
        'len(playback["holds"]) == 43 and len(playback["menus"]) == 4 and playback["prior_speech_samples_reused"] == 39',
    'len(name_check["records"]) == 18': 'len(name_check["records"]) == 22',
    'blocks == list(stage.review.BLOCKS[0])': 'blocks == list(CHANGED)',
    '    for n in blocks:\n        group = groups[n]':
        '    assert tuple(groups) == stage.review.BLOCKS[0]\n    for n, group in groups.items():',
    'len(group["commands"]) for group in groups.values()) == 404': 'len(group["commands"]) for group in groups.values()) == 544',
    'startup = parent.parent.startup_check': 'startup = parent.parent.parent.startup_check',
    '== len(draft["records"]) == 255': '== len(draft["records"]) == 351',
    '{"wording": 143, "wrap": 4, "retention": 108}': '{"wording": 146, "wrap": 1, "retention": 204}',
    '    validate_natural_dialogue_batch(draft)':
        '''    coverage = rendered["prior_ordinary_sailing_coverage"]
    assert len(coverage["exact_prior_observed_record_ids"]) == 40
    assert base.digest(coverage["path"]) == coverage["sha256"]
    draft["prior_ordinary_sailing_coverage"] = coverage
    validate_natural_dialogue_batch(draft)''',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_followup_encounters_predecessor": "verified_rafael_ruins_and_proof_predecessor",
    "len(batches) == 1004 and len(checks) == 339": "len(batches) == 1005 and len(checks) == 340",
    "previously_localized_records=255, new_contextual_records=0, prose_revisions=143":
        "previously_localized_records=351, new_contextual_records=0, prose_revisions=146",
    "wrap_only_revisions=4, justified_retentions=108": "wrap_only_revisions=1, justified_retentions=204",
    "initialized_Rafael_ruins_and_proof=True": "initialized_Rafael_rescue_and_lessons=True",
    "contextual_nameplate_retentions=18": "contextual_nameplate_retentions=22",
    "actual_menu_samples=5, actual_style_objects=2":
        "actual_menu_samples=4, actual_style_objects=4, exact_prior_ordinary_sailing_records=40",
    "prior_records_reviewed=255": "prior_records_reviewed=351",
    "prose_revisions=143, justified_retentions=108, wrap_only_revisions=4":
        "prose_revisions=146, justified_retentions=204, wrap_only_revisions=1",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's rescue encounters and lessons

The [testing ROM](../../{ROM.as_posix()}) includes 18 contextual scene reviews. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_ruins_and_proof", "rafael_rescue_and_lessons").replace(
    "verified_rafael_rescue_and_lessons_predecessor", "verified_rafael_ruins_and_proof_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
pin_start = parent.commit.index('    earlier = stage.ROOT.with_name')
pin_end = parent.commit.index('        absolute =', pin_start)
commit = checked_text(parent.commit, {
    parent.commit[pin_start:pin_end]:
        '''    earlier = sorted(stage.ROOT.parent.glob("staged_v*/" + stage.ROM.name))
    research = sorted(stage.ROOT.parent.glob("staged_v*/focused_gameplay/Rafael_Rescue_And_Lessons_RESEARCH_ONLY.nds"))
    for path in (ROM, parent.ROM, *earlier, *research):
''',
    "Preserve the Rafael ruins candidate, predecessor, staged ROM and focused fixture":
        "Preserve the Rafael rescue candidate, predecessor, staged ROM and focused fixture",
    notes: '''    DOC.write_text(f"""# Rafael's rescue encounters and lessons

Reviewed 351 records across 18 encounters. The batch has 146 wording revisions, one wrap-only fix and 204 justified retentions. The rescue identifies the man as the child's grandfather and keeps 10 original companion bodies distinct. The statue encounter distinguishes recognizing a figurehead from suggesting that a statue could be used as one. Maria's exchange identifies the bandit's grievance, her response to indiscriminate attacks and the reason she offers him a place aboard. The revised paragraphs remove one unnecessary page turn and correct duplicate punctuation after the company name. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

The sailing, trade, recruitment and route lessons use the installed controls and labels. Earlier ordinary Lisbon gameplay remains applicable to 40 byte-identical speech commands with exact renderer and event dependencies. The focused gameplay proof covers {observed_count()} speech pages, including four replayed from Maria's exchange on this candidate and 39 byte-identical samples from the previous candidate. The reused evidence includes four companion objects and four highlights across the steering and Guiding Staff choices. Other new wording and branch outcomes remain unvisited in ordinary play. Hardware verification remains open. [Native and emulator evidence](../{VERIFY.as_posix()})

Native checks cover {native_count()} revised pages, all 15 speakerless panels, 10 captions, 34 physical personality bodies and 22 current names and roles. Six startup holds, 24 protected name getters, 17 tests and exact clean-input reconstruction passed. All earlier editorial credit carries forward. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)

Maria's company name and the start of her answer stay together on the first row. The line allows a 16-character base name plus the four-character company suffix. The second row keeps "who I'm with" together.
""", encoding="utf-8")
''',
}).replace("rafael_ruins_and_proof", "rafael_rescue_and_lessons")
scope = parent.scope | globals() | {"pages_saved": lambda: sum(
    row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])}
for code in (verification, build, commit):
    exec(compile(code, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

