"""Register the source-bound shore and white-whale phrase-wrap revisions."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_deck_phrase_wraps_20261121 as parent
from scripts import register_sailing_help_20261120 as startup_release
from scripts import replay_shore_phrase_wraps_20261121 as live
from scripts import stage_shore_phrase_wraps_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-shore-phrase-wraps-v1-20261121'
ROOT = Path('out/shore_phrase_wraps_registered_20261121_v1')
ROM = ROOT / 'Translation_DS_Shore_Phrase_Wraps_20261121_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261121_shore_phrase_wraps_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_shore_phrase_wraps_registered_20261121.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'qa.xml'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Reviewed 41 shore and whale reports, revised 11 pages, and verified the attack report and return to sailing.'
PENDING = parent.PENDING


def verify(registry, previous, viewed):
    stored, actual = map(base.load, (stage.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == actual['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['full_parent_inverse'] and stored['staged_reconstruction_byte_exact']
    assert stored['patch_sha256'] == base.digest(stage.PATCH)
    assert stage.REBUILT.read_bytes() == stage.ROM.read_bytes()
    assert viewed == {s['path']: s['sha256'] for s in [*stored['sheets'], actual['sheet']]}
    assert all(base.digest(p) == digest for p, digest in (viewed | actual['evidence'] | stored['source_receipts']).items())
    assert actual['actual_emulator'] and actual['return_frame'] == live.RETURN and actual['selector_restored']
    assert actual['revised_message_ID'] == live.ATTACK and not actual['hardware']
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    clean, old, image = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    before, after = map(batch.files, (old, image))
    assert before.keys() == after.keys()
    assert {key for key in before if before[key] != after[key]} == {stage.COMMON}
    arm = after[stage.ARM]
    assert batch.digest(arm) == stored['target_ARM9_sha256'] == previous['target_ARM9_sha256']
    assert batch.digest(after[stage.COMMON]) == stored['target_COMMON_sha256']
    portrait = stage.portrait
    directory = batch.digest(arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET])
    old_rows, now_rows = [portrait.owned_entries(files[stage.COMMON], arm, directory) for files in (before, after)]
    assert len(old_rows) == len(now_rows) == 3668
    assert {a.message_id for a, b in zip(old_rows, now_rows, strict=True) if a.text != b.text} == stage.EDITS.keys()
    pending = base.load(PENDING)['records']
    assert len(pending) == stored['unchanged_pending_records'] == 276
    for row in pending:
        now = now_rows[row['message_ID']]
        assert portrait.reference(now) == row['current_reference'] and now.text.hex() == row['current_hex']
    image.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    guards = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guards)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    starter = startup_release.env['startup_check'].startup_proof
    FunctionType(starter.__code__, starter.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(
        previous, candidate, arm)

    records = stored['records']
    assert len(records) == 41 and sum(r['decision'] == 'revision' for r in records) == 9
    assert {r['message_ID'] for r in records if r['decision'] == 'wrap revision'} == {2243, 2355}
    assert {r['message_ID'] for r in records if r['decision'] == 'retention'} == stage.RETAIN.keys()
    for row in records:
        n = row['message_ID']
        assert now_rows[n].text.hex() == row['staged_hex']
        assert portrait.reference(now_rows[n]) == row['staged_reference']
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['gameplay_observed'] = n == actual['revised_message_ID']
    draft = dict(translation_policy=stored['translation_policy'], target_locale=stored['target_locale'],
                 encoder=stored['encoder'], review_gates=stored['review_gates'], records=records,
                 candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'],
                 checked_story_format_guard=controls, unchanged_pending_records=276,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'],
                 allocation=stored['allocation'], pending_source_receipt_sha256=base.digest(PENDING),
                 focused_replay=actual, visual_review_receipt=viewed, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.COMMON: stored['target_COMMON_sha256']}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 955 and len(manifest["checks"]) == 290':
        'len(manifest["batches"]) == 956 and len(manifest["checks"]) == 291',
    'release_stack_before_deck_phrase_wraps.json': 'release_stack_before_shore_phrase_wraps.json',
    'release_stack_with_deck_phrase_wraps.json': 'release_stack_with_shore_phrase_wraps.json',
    'verified_bubble_predecessor=predecessor, deck_phrase_wraps_release=str(REVIEW)':
        'verified_deck_predecessor=predecessor, shore_phrase_wraps_release=str(REVIEW)',
    'registered_deck_phrase_wraps_and_complete_parent_inverse': 'registered_shore_phrase_wraps_and_complete_parent_inverse',
    'manifest["deck_phrase_wraps_pipeline"]': 'manifest["shore_phrase_wraps_pipeline"]',
    'owned_message_IDs=sorted(stage.EDIT), target_COMMON_sha256=archives[stage.COMMON], target_ARM9_sha256=archives[stage.ARM]':
        'owned_message_IDs=sorted(stage.EDITS), target_COMMON_sha256=archives[stage.COMMON]',
    'changed_components=2, target_COMMON_sha256=archives[stage.COMMON], target_ARM9_sha256=archives[stage.ARM]':
        'changed_components=1, target_COMMON_sha256=archives[stage.COMMON]',
    'previously_localized_records=10, new_contextual_records=0, prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'previously_localized_records=41, new_contextual_records=0, prose_revisions=9, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=30',
    'focused_gerhard_holds=2, normal_town_return=True, disposable_room_assignment=True':
        'focused_shore_attack=True, normal_sailing_return=True, variant_selector_restored=True',
    'ledger["deck_phrase_wraps_20261121"]': 'ledger["shore_phrase_wraps_20261121"]',
    'prior_records_reviewed=10, actual_gameplay_records=1, new_contextual_credit=0,\n        prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'prior_records_reviewed=41, actual_gameplay_records=1, new_contextual_credit=0,\n        prose_revisions=9, spacing_revisions=0, wrap_only_revisions=2, justified_retentions=30',
    'Preserve the Deck phrase-wrap candidate or reconstruction': 'Preserve the shore phrase-wrap candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Shore report phrase-wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises eleven expedition and whale reports. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Shore and whale report phrase wraps

Reviewed 41 reports in seven native dialogue groups. Nine received prose revisions, two were rewrapped with their wording intact, and 30 retain their wording and layout. The changes cover a friendly invitation, the shore attack, the outbreak after an animal attack, the bottomless bog and the glint where the white whale dived. [Exact clean, prior and registered references](../{REVIEW.as_posix()})

All 41 reports passed native portrait checks, and every revised page was visually reviewed. A DeSmuME replay used the copied Search save and recorded shoreline setup. It temporarily selected the revised attack wording, then restored the original selector before the sailor-loss notice and verified the return to sailing. The remaining variants received offline checks. Hardware remains unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the candidate byte for byte. Only COMMON changes. All 114 accepted layers, the ASCII right-bound fix and the locations and payloads of the 276 pending mapped shared records carry forward. Six startup holds, 24 protected getters and 17 focused tests passed. Sixteen leads remain in the separate early-wrap scan. [Registered candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register-shore-phrase-wraps', 'exec'), env)


if __name__ == '__main__':
    env['main']()

