"""Register Recruit Crew wording and regular-width numbers over Palace Help."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_amsterdam_tavern_editorial_20261120 as startup_check
from scripts import register_palace_help_20261120 as parent
from scripts import replay_recruit_crew_20261120 as replay
from scripts import stage_recruit_crew_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = stage.base, stage.batch
PROFILE = 'all-routes-recruit-crew-v1-20261120'
ROOT = Path('out/recruit_crew_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Recruit_Crew_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_recruit_crew_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_recruit_crew_registered_20261120.md')
STARTUP = stage.ROOT / 'own_startup_verification.json'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
QA = stage.ROOT.with_name('recruit_crew_20261120') / 'qa.xml'
WORKLIST = Path('translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_worklist_20261120_v1.json')
CHECKPOINT = 'Recruit Crew now uses regular-width numbers for the quote, volunteers, and both follow-up questions.'


def verify(registry, previous, viewed):
    stored, native, game = map(base.load, (stage.PROOF, stage.NATIVE, replay.RESULT))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == native['candidate_sha256'] == game['candidate_sha256']
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == stored['parent_sha256'] == game['parent_sha256']
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    assert stored['whole_parent_inverse'] and stored['clean_input_patch_byte_exact']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == stored['clean_input_patch_sha256']
    assert all(base.digest(path) == sha for path, sha in game['evidence'].items())
    assert viewed == game['sheets'] and len(viewed) == 4
    assert all(base.digest(path) == sha for path, sha in viewed.items())
    assert [r['frame'] for r in game['paired_pages']] == list(replay.PAIRED)
    assert (game['charge'], game['volunteers'], game['spare_berths']) == (1573, 34, 51)
    assert game['ordinary_Istanbul_recruitment'] and game['full_recruitment_and_return_observed']
    assert len(native['original_ring_cases']) == 928 and len(native['original_voice_cases']) == 200
    assert len(native['supplied_threshold_paths']) == 5 and native['native_preview_count'] == 59
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM, stage.COMMON}
    original, arm = before[stage.ARM], after[stage.ARM]
    patched, sites = stage.patch(original, clean.read_file(stage.ARM))
    assert patched == arm and sites == stored['calls']
    common = after[stage.COMMON]
    assert batch.digest(arm) == stored['target_ARM9_sha256'] and batch.digest(common) == stored['target_COMMON_sha256']
    new.replace_file(stage.ARM, original)
    new.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())

    current, target = stage.catalogue(original, before[stage.COMMON]), stage.catalogue(arm, common)
    assert len(current) == len(target) == 3668
    assert {i for i in range(3668) if current[i].text != target[i].text} == stage.EDITS.keys()
    pending = base.load(WORKLIST)
    assert len(pending['records']) == 276
    for r in pending['records']:
        n = r['message_ID']
        assert batch.reference(current[n]) == batch.reference(target[n]) == r['current_reference']
        assert current[n].text.hex() == target[n].text.hex() == r['current_hex']
    check_startup = FunctionType(startup_check.startup_proof.__code__, startup_check.startup_proof.__globals__ |
                                 {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})
    check_startup(previous, candidate, arm)

    records = native['records']
    assert [r['message_ID'] for r in records] == list(stage.RECORDS)
    for row in records:
        n = row['message_ID']
        assert current[n].text.hex() == row['current_hex'] and target[n].text.hex() == row['final_hex']
        assert batch.reference(current[n]) == row['current_reference'] and batch.reference(target[n]) == row['final_reference']
        row['registered_reference'] = row['final_reference'] | {'candidate_sha256': candidate}
    draft = dict(candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'], records=records,
        translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(batch.GATES), checked_story_format_guard=controls, unchanged_pending_records=276,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], number_calls=sites,
        observed_gameplay=game, native_display=str(stage.NATIVE), new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.ARM: batch.digest(arm), stage.COMMON: batch.digest(common)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 949 and len(manifest["checks"]) == 284':
        'len(manifest["batches"]) == 950 and len(manifest["checks"]) == 285',
    'stage.PROOF, stage.PLAN, STARTUP, QA, replay.LIVE, replay.NAV, args.visual_review,':
        'stage.PROOF, stage.NATIVE, STARTUP, QA, replay.RESULT, args.visual_review,',
    'release_stack_before_palace_help.json': 'release_stack_before_recruit_crew.json',
    'release_stack_with_palace_help.json': 'release_stack_with_recruit_crew.json',
    'verified_load_confirmation_predecessor=predecessor, palace_help_release=str(REVIEW)':
        'verified_palace_help_predecessor=predecessor, recruit_crew_release=str(REVIEW)',
    'registered_palace_help_and_complete_parent_inverse': 'registered_recruit_crew_and_complete_parent_inverse',
    'manifest["palace_help_pipeline"]': 'manifest["recruit_crew_pipeline"]',
    'if file == stage.HELP:': 'if file == stage.COMMON:',
    'native_and_emulator_evidence_sha256=base.digest(replay.LIVE)': 'native_and_emulator_evidence_sha256=base.digest(replay.RESULT)',
    'owned_help_pages=base.load(stage.PLAN)["owned_topic_ids"], target_HELP_sha256=archives[stage.HELP]':
        'number_calls=stored["calls"], target_ARM9_sha256=archives[stage.ARM], owned_COMMON_allocations=stored["COMMON_allocations"]',
    'changed_components=1, target_HELP_sha256=archives[stage.HELP]':
        'changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]',
    'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=previous["target_COMMON_sha256"]':
        'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=archives[stage.COMMON]',
    'reviewed_UI_labels=6, previously_localized_records=9, new_contextual_records=0, prose_revisions=6, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3':
        'reviewed_UI_labels=0, previously_localized_records=37, new_contextual_records=0, prose_revisions=11, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=26',
    'name_label_revisions=0, text_display_revisions=0, pagination_fixes=0':
        'name_label_revisions=0, text_display_revisions=4, pagination_fixes=0',
    'ordinary_palace_help_9_pages=True, continuation_backlinks_and_history=True':
        'ordinary_Istanbul_recruit_crew=True, spare_berths_observed=True, shortfall_offline_only=True',
    'ledger["palace_help_20261120"]': 'ledger["recruit_crew_20261120"]',
    'prior_records_reviewed=9, actual_help_pages=9, new_contextual_credit=0,\n        prose_revisions=6, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3, text_display_revisions=0':
        'prior_records_reviewed=37, actual_paired_states=4, new_contextual_credit=0,\n        prose_revisions=11, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=26, text_display_revisions=4',
    'Preserve the Palace Help candidate or reconstruction': 'Preserve the Recruit Crew candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Recruit Crew testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises eleven recruiting lines and uses regular-width numbers in all four recruiting displays. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Recruit Crew wording and numbers

Recruit Crew now uses regular-width digits for the gold quote, number of volunteers, crew shortfall and spare berths. Four revised quotes keep the amount and “gold” together across the tested range. Seven shortfall versions say how many sailors are still needed and offer to recruit again in each voice. The other 26 lines retain their wording. [Source and review ledger](../{REVIEW.as_posix()})

Paired ordinary Istanbul runs verified the 1,573-gold charge, 34 volunteers, 51 spare berths and the town return. Eight other full screen captures matched the preceding build. Offline checks covered the shortfall branch, all five original voice tables, 928 number-buffer cases and 59 complete rendered pages. Hardware, the alternate dialogue voices and the shortfall branch were outside the emulator replay. [Emulator comparison](../{(VERIFY / replay.SHEET.name).as_posix()})

Six startup holds, 24 protected name getters and 17 focused tests passed. The clean-input patch reconstructs the cumulative candidate byte for byte. The ledger retains 27,700 credited reviews and 276 stored shared keys to classify. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
