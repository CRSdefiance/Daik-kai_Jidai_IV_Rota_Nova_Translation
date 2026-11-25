"""Register the reviewed Carlo, Cristina, Samwell, and Jam scenes cumulatively."""

from types import SimpleNamespace

from scripts import register_rafael_B161_B169_20261121 as parent
from scripts import replay_rafael_B170_B176_20261121 as live
from scripts import verify_rafael_B170_B176_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B170-B176-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_B170_B176_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_B170_B176_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_B170_B176_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B170_B176_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = (170, 171, 172, 173, 176)
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Reviewed 190 Rafael records with 56 wording revisions, six glyph corrections, four wrap-only fixes, and 124 justified retentions."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


verification = checked_text(parent.verification, {
    'rendered["FE_panels"] == 30': 'rendered["FE_panels"] == 6',
    'len(playback["exact_sampled_page_turn"]) == 4': 'len(playback["exact_sampled_page_turn"]) == 5',
    'len(name_check["records"]) == 31': 'len(name_check["records"]) == 13',
    'len(group["commands"]) for group in groups.values()) == 781': 'len(group["commands"]) for group in groups.values()) == 294',
    'startup = parent.parent.parent.parent.parent.parent.startup_check': 'startup = parent.parent.parent.parent.parent.parent.parent.startup_check',
    '== len(draft["records"]) == 368': '== len(draft["records"]) == 190',
    '{"revision": 102, "retention": 266, "wrap_only": 5}': '{"wording": 56, "glyph": 6, "wrap-only": 4, "retention": 124}',
    '''    translation = str.maketrans({"！": "!", "？": "?", "…": "..."})
    glyphs = [r["id"] for r in draft["records"] if r["decision"] == "revision" and r.get("change_class") != "wrap-only"
              and r["previous_English"].translate(translation).replace("!?", "?!") == r["english"]]''':
        '''    glyphs = [r["id"] for r in draft["records"] if r.get("change_class") == "glyph"
              and r["previous_English"] in ("…", "……") and r["english"] == "..."]''',
    '    assert draft["encoder"] == "registered-native-story-objects"\n'
    '    draft.update(encoder="dialogue-relocatable-v1", stored_writer="registered-native-story-objects")\n': '',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_rafael_homeland_and_maps_predecessor': 'verified_rafael_B161_B169_predecessor',
    'len(batches) == 1008 and len(checks) == 343': 'len(batches) == 1009 and len(checks) == 344',
    'previously_localized_records=368': 'previously_localized_records=190',
    'prose_revisions=91': 'prose_revisions=56',
    'wrap_only_revisions=5': 'wrap_only_revisions=4',
    'justified_retentions=266': 'justified_retentions=124',
    'prior_records_reviewed=368': 'prior_records_reviewed=190',
    'contextual_nameplate_retentions=31': 'contextual_nameplate_retentions=13',
    'initialized_Rafael_homeland_and_maps=True': 'initialized_Rafael_B170_B176=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's Carlo, Cristina, Samwell, and Jam scenes

The [testing ROM](../../{ROM.as_posix()}) includes the contextual review of Rafael's SC0 blocks 170–176. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B161_B169", "rafael_B170_B176").replace(
    "verified_rafael_B170_B176_predecessor", "verified_rafael_B161_B169_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B161_B169': 'glob("staged_B170_B176',
    'Rafael_B161_B169_FOCUSED_ONLY.nds': 'Rafael_B170_B176_FOCUSED_ONLY.nds',
    "Preserve the Rafael audience and recruitment candidate": "Preserve the Rafael Carlo, Cristina, Samwell, and Jam candidate",
    notes: '''    DOC.write_text(f"""# Rafael's Carlo, Cristina, Samwell, and Jam scenes

The contextual pass covers 190 records in SC0 blocks 170–176. Carlo's bargaining turns into practical concern and later a family disclosure. His account keeps the regret and the crew's explicit offer of a new family. Cristina's dance restores all three independent patron headings. Claudio's apology preserves her established kinship with Julio and his recognition of her as a crewmate. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Samwell's cooking audition keeps the dish unnamed, his pride intact, and the humor in Claudio's reply to the proverb. The missing-ship exchange keeps the port worker's explanation and Rafael's fascination with the unknown sailor. Jam keeps the repeated cheer, his name spelling, the spoken English and French flourishes, and the reversal after his mock refusal. The two short follow-ups keep separate native references.

Native checks cover {native_count()} revised pages, all six speakerless panels, and 13 names and roles. The focused cold-boot replay verified {observed_count()} pages, including the dance audience and the move from applause back to dialogue. The gameplay fixture returned to port. Conditional branches and hardware remain unvisited in this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The registered candidate preserves 114 accepted layers, the right-bound correction, and seven source-format controls. Six startup comparisons, 17 regression tests, and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B161_B169", "rafael_B170_B176")

scope = parent.scope | globals()
for script in (verification, build, commit):
    exec(compile(script, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
