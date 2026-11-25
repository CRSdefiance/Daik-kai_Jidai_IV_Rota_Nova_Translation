"""Register Rafael's Istanbul remedy and hidden-village dialogue."""

from types import SimpleNamespace

from scripts import register_rafael_B261_B280_20261122 as parent
from scripts import register_rafael_tradehouse_festival_20261121 as startup_reference
from scripts import replay_rafael_B306_B309_20261122 as live
from scripts import verify_rafael_B306_B309_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, workflow = writer.base, writer.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT,
                        review=SimpleNamespace(BLOCKS=writer.BLOCKS))
PROFILE = "all-routes-rafael-B306-B309-v1-20261122"
ROOT = parent.ROOT.with_name("rafael_B306_B309_registered_20261122")
ROM = ROOT / "Translation_DS_Rafael_B306_B309_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_B306_B309_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_B306_B309_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
CHANGED = writer.BLOCKS[0]
names = SimpleNamespace(PROOF=display.NAMES)
guard_spec = parent.guard_spec
CHECKPOINT = "Revisited 53 Rafael records in the Istanbul remedy and hidden-village exchanges. The review made 17 wording revisions and 36 justified retentions, and carried forward eight earlier decisions from the same scenes."


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def pages_saved():
    return sum(row["previous_pages"] - row["current_pages"] for row in base.load(display.PROOF)["pagination_changes"])


old_validation = parent.verification[parent.verification.index('    assert rendered["FE_panels"]'):
                                     parent.verification.index('    assert playback["initialized_excerpts"]')]
verification = checked_text(parent.verification, {
    old_validation: '''    assert not rendered["FE_panels"] and not rendered["menus"] and not rendered["style_objects"]
    assert rendered["revised_speech_pages"] == 17
    assert draft["contextual_records_revisited"] == 53 and draft["contextual_decisions_reused"] == 8
    assert len(playback["holds"]) == len(live.SELECTED) and not playback["menus"]
''',
    'len(name_check["records"]) == 16': 'len(name_check["records"]) == 5',
    'len(group["commands"]) for group in groups.values()) == 353': 'len(group["commands"]) for group in groups.values()) == 117',
    'startup = parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.startup_check':
        'startup = startup_reference.startup_check',
    '== len(draft["records"]) == 135': '== len(draft["records"]) == 61',
    '{"wording": 2, "wrap-only": 4, "retention": 129}': '{"wording": 17, "retention": 44}',
})

readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'len(batches) == 1015 and len(checks) == 350': 'len(batches) == 1016 and len(checks) == 351',
    'previously_localized_records=135, contextual_records_revisited=21, contextual_decisions_reused=114':
        'previously_localized_records=61, contextual_records_revisited=53, contextual_decisions_reused=8',
    'prose_revisions=0': 'prose_revisions=17',
    'wrap_only_revisions=4': 'wrap_only_revisions=0',
    'justified_retentions=15': 'justified_retentions=36',
    'choice_label_revisions=2': 'choice_label_revisions=0',
    'prior_records_reviewed=21, contextual_decisions_reused=114': 'prior_records_reviewed=53, contextual_decisions_reused=8',
    'contextual_nameplate_retentions=16': 'contextual_nameplate_retentions=5',
    'actual_menu_samples=5, actual_style_objects=2': 'actual_menu_samples=0, actual_style_objects=0',
    'initialized_Rafael_B261_B280=True': 'initialized_Rafael_B306_B309=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's Istanbul remedy and hidden-village dialogue

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed SC0 blocks 306–309. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_B261_B280", "rafael_B306_B309").replace(
    "verified_rafael_B221_B240_predecessor", "verified_rafael_B261_B280_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'glob("staged_B261_B280': 'glob("staged_B306_B309',
    'Rafael_B261_B280_FOCUSED_ONLY.nds': 'Rafael_B306_B309_FOCUSED_ONLY.nds',
    "Preserve Rafael's ruins puzzle and arrest assignments": "Preserve Rafael's Istanbul remedy and hidden-village candidate",
    notes: '''    DOC.write_text(f"""# Rafael's Istanbul remedy and the hidden village

The contextual review revisits 53 records and carries forward eight exact earlier decisions from the same scenes. It makes 17 wording revisions and retains 36 lines for documented reasons. The guildmaster introduces the cure as hearsay. The boy's recovery has matching wording in both treatment paths. Rafael's guess about China, Hua Tuo's Tonic, the rockslide and the cliff route keep their original meaning and level of certainty. [Japanese, installed English and registered decisions](../{REVIEW.as_posix()})

Native verification covers all 17 revised pages, 117 stored commands, five nameplates and 10 name getters. Focused cold-boot excerpts verify {observed_count()} dialogue pages, the mirrored recovery lines, Rafael's given-name substitution, and the return to port. Natural activation and hardware remain unvisited for this batch. [Native and gameplay evidence](../{VERIFY.as_posix()})

The cumulative candidate preserves 114 accepted layers, the ASCII right-bound correction and seven source-format controls. Six startup comparisons, 17 regression tests and exact clean-input reconstruction passed. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_B261_B280", "rafael_B306_B309")

scope = parent.scope | globals()
for source in (verification, build, commit):
    exec(compile(source, __file__ + "::registered-continuation", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
