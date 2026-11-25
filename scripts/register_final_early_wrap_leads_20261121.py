"""Register the verified remaining early-wrap revisions."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_item_advice_phrase_wraps_20261121 as parent
from scripts import register_sailing_help_20261120 as startup_release
from scripts import replay_final_early_wrap_leads_20261121 as live
from scripts import stage_final_early_wrap_leads_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, portrait = parent.base, parent.batch, stage.portrait
PROFILE = 'all-routes-final-early-wrap-leads-v1-20261121'
ROOT = Path('out/final_early_wrap_leads_registered_20261121_v1')
ROM = ROOT / 'Translation_DS_Early_Wrap_Leads_20261121_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261121_final_early_wrap_leads_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_final_early_wrap_leads_registered_20261121.md')
NATIVE = stage.ROOT / 'refit_native/native_font_verification.json'
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'qa.xml'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Revised five confirmed early wraps in mutiny, Auto Move, Refit and the shark encounter.'
PENDING = stage.PENDING


def verify(registry, previous, viewed):
    stored, actual, refit = map(base.load, (stage.PROOF, live.PROOF, NATIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == actual['candidate_sha256'] == refit['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['whole_parent_inverse'] and stored['exact_clean_reconstruction']
    assert stored['patch_sha256'] == base.digest(stage.PATCH)
    assert stage.REBUILT.read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.PROOF) == refit['manuscript_sha256']
    assert viewed == {s['path']: s['sha256'] for s in [*stored['sheets'], *refit['review_sheets'], actual['sheet']]}
    assert all(base.digest(p) == v for p, v in (viewed | actual['evidence'] | stored['source_receipts']).items())
    assert actual['actual_emulator'] and actual['original_raise_choice_and_item'] and actual['sailing_return']
    assert not actual['hardware'] and not actual['natural_shark_battle'] and actual['original_roster_and_code_restored']
    assert [r['message_ID'] for r in actual['original_exchange_before_choice']] == [2448, 2449, 2450]
    assert [r['message_id'] for r in refit['records']] == [1253, 1273]
    assert all(r['complete_independent_font_plane_equal'] and r['all_body_rows_start_at_x0_and_fit_first60_rows']
               and r['text_and_pixel_guards_and_ABI_preserved'] for r in refit['records'])
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    clean, old, image = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256']
    before, after = map(batch.files, (old, image))
    assert before.keys() == after.keys()
    assert {key for key in before if before[key] != after[key]} == {stage.COMMON}
    arm = after[stage.ARM]
    assert batch.digest(arm) == previous['target_ARM9_sha256'] == stored['target_ARM9_sha256']
    assert batch.digest(after[stage.COMMON]) == stored['target_COMMON_sha256']
    image.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    directory = batch.digest(arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET])
    old_rows, now_rows = [portrait.owned_entries(files[stage.COMMON], arm, directory) for files in (before, after)]
    assert len(old_rows) == len(now_rows) == 3668
    assert {a.message_id for a, b in zip(old_rows, now_rows, strict=True) if a.text != b.text} == stage.EDITS.keys()
    pending = base.load(PENDING)['records']
    assert len(pending) == stored['unchanged_pending'] == 276
    observed_shifts = {}
    for row in pending:
        n = row['message_ID']
        a, b = row['current_reference'], portrait.reference(now_rows[n])
        assert portrait.reference(old_rows[n]) == a and now_rows[n].text.hex() == row['current_hex']
        assert a | {'record_index': b['record_index']} == b
        if a != b:
            observed_shifts[str(n)] = dict(before=a, after=b)
    assert observed_shifts == stored['pending_index_shifts']
    legacy = stored['retained_legacy_117']
    assert legacy['status'] == 'display owner unconfirmed'
    assert old_rows[117] == now_rows[117] and portrait.reference(now_rows[117]) == legacy['exact_reference_after']
    guards = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guards)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    starter = startup_release.env['startup_check'].startup_proof
    FunctionType(starter.__code__, starter.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(
        previous, candidate, arm)

    records = stored['records']
    assert len(records) == 37 and {r['message_ID'] for r in records if r['decision'] == 'revision'} == stage.EDITS.keys()
    refit_records = {r['message_id']: r for r in refit['records']}
    for row in records:
        n = row['message_ID']
        assert now_rows[n].text.hex() == row['staged_hex']
        assert portrait.reference(now_rows[n]) == row['staged_reference']
        if n in refit_records:
            assert refit_records[n]['compiled_hex'] == row['staged_hex'] + '00'
            assert refit_records[n]['lines'] == row['visible_lines']
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['gameplay_observed'] = n in (2448, 2449, 2450)
    draft = dict(translation_policy=stored['translation_policy'], target_locale=stored['target_locale'],
                 encoder=stored['encoder'], review_gates=stored['review_gates'], records=records,
                 candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'],
                 checked_story_format_guard=controls, unchanged_pending_payloads_and_native_locations=276,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'],
                 pending_source_receipt_sha256=base.digest(PENDING), shifted_pending_record_indices=observed_shifts,
                 focused_replay=actual, visual_review_receipt=viewed, unopened_legacy_notice=legacy,
                 new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.COMMON: stored['target_COMMON_sha256']}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 958 and len(manifest["checks"]) == 293':
        'len(manifest["batches"]) == 959 and len(manifest["checks"]) == 294',
    'stage.PROOF, STARTUP, QA, live.PROOF, args.visual_review,': 'stage.PROOF, STARTUP, QA, live.PROOF, NATIVE, args.visual_review,',
    'release_stack_before_item_advice_phrase_wraps.json': 'release_stack_before_final_early_wrap_leads.json',
    'release_stack_with_item_advice_phrase_wraps.json': 'release_stack_with_final_early_wrap_leads.json',
    'verified_shore_loss_predecessor=predecessor, item_advice_phrase_wraps_release=str(REVIEW)':
        'verified_item_advice_predecessor=predecessor, final_early_wrap_leads_release=str(REVIEW)',
    'registered_item_advice_phrase_wraps_and_complete_parent_inverse': 'registered_final_early_wrap_leads_and_complete_parent_inverse',
    'manifest["item_advice_phrase_wraps_pipeline"]': 'manifest["final_early_wrap_leads_pipeline"]',
    'previously_localized_records=49, new_contextual_records=0, prose_revisions=17, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=31':
        'previously_localized_records=37, new_contextual_records=0, prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=32',
    'focused_lisbon_items=3, revised_replies_observed=2, original_items_and_town_return=True':
        'focused_shark_dialogue=3, revised_replies_observed=1, original_raise_choice_and_sailing_return=True',
    'ledger["item_advice_phrase_wraps_20261121"]': 'ledger["final_early_wrap_leads_20261121"]',
    'prior_records_reviewed=49, actual_gameplay_records=3, new_contextual_credit=0,\n        prose_revisions=17, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=31, text_display_revisions=0':
        'prior_records_reviewed=37, actual_gameplay_records=3, new_contextual_credit=0,\n        prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=32, text_display_revisions=0',
    'Preserve the revised item-advice candidate or reconstruction': 'Preserve the early-wrap candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Early-wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises five early-wrap entries. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Early wraps in dialogue and Refit help

Reviewed 37 related entries. Five received prose and wrap revisions, and 32 were retained. The Surveyor’s warning and Samwell’s proposal fit on one row. The longer mutiny response and both Refit help panels keep their phrases intact. [Exact source and registered decisions](../{REVIEW.as_posix()})

All changed pages passed native pixel and visual checks. A focused emulator replay initialized the original shark exchange, then verified Samwell’s proposal and Al’s response, the Raise It choice, the Baby Shark reward and the return to sailing. The setup restored the actor roster and code in the disposable emulator state. The other four revisions received offline checks. Hardware was outside this pass. [Native and emulator evidence](../{VERIFY.as_posix()})

The clean-input patch reconstructs the ROM byte for byte. Only COMMON changes. All 114 accepted layers, the earlier ASCII changes and the runtime locations and bytes of 276 pending shared records carry forward. Six startup holds, 24 protected getters and 17 focused tests passed. COMMON 117 remains in the display-owner worklist until its runtime path is established. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register-final-early-wrap-leads', 'exec'), env)


if __name__ == '__main__':
    env['main']()

