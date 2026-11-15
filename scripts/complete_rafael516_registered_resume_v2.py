"""Credit the two disjoint reviewed batches once after full registered release verification."""
import gzip
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Rafael516_resume_release_verified_v2_20261105')
LEDGER = Path('translations/editorial_review_current_v1.json')
FINAL = Path('translations/rafael516_integrated_final_review_v2.json')
FAMILY = 'Rafael_SC0_B85_B120_contextual_integrated_20261105'
KEY261 = 'Rafael_SC0_B85_B100_contextual_20261105'
KEY255 = 'Rafael_SC0_B101_B120_clean_20261105'
CONTEXT = 'contextual_story_natural_dialogue_pass_v1871'


def main():
    assert not FINAL.exists() and not (ROOT / 'completion_checkpoint.json').exists()
    rp, sp, np = [ROOT / p for p in ['registered_release_verification.json',
        'own_registered_startup_verification.json', 'own_Fernan_name_getter_verification.json']]
    release, startup, names = map(load, [rp, sp, np])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(sp.read_bytes()) == release['own_registered_startup_sha256']
    candidate = Path(release['candidate'])
    assert sha(candidate.read_bytes()) == release['candidate_sha256'] == startup['candidate_sha256'] == names['runtime']['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes() == candidate.read_bytes()
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (680, 114, 26)
    assert release['all_eight_registered_final_stages_preserved'] and release['exact_all_integrated_references_bound']
    registry = Path('translations/release_stack.json')
    assert sha(registry.read_bytes()) == release['registry_sha256']
    assert startup['actual_captain_getter'] == startup['actual_route_word'] == 0
    assert names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    for path in ['work/analysis/Rafael516_resume_release_verify_gc_v2_20261105/completion.json',
                 'work/analysis/Rafael516_resume_startup_gc_v2_20261105/completion.json',
                 'work/analysis/Rafael516_resume_Fernan_gc_v2_20261105/completion.json']:
        t = load(path)
        assert t['terminal'] and t['completed_without_exception'] and t['all_locked_sources_unchanged']
        assert not t['garbage_collection']['errors']
    bp = Path(release['exact_record_bindings'])
    assert sha(bp.read_bytes()) == release['exact_record_bindings_sha256']
    bindings = load(bp)['records']
    prep = load(release['preparation'])
    originals = {}
    for config in prep['configs']:
        conf = load(config)
        path = Path(conf['manuscript'])
        assert all(all(r['review'].values()) and len(r['review']) == 5 for r in load(path)['records'])
        for row in load(path)['records']:
            key = row['file_path'], row['id']
            assert key not in originals
            originals[key] = row, path
    rows, cleared = [], []
    intake_holds = {'native_name_term_full_preamble_andfresh_display_pending',
        'native_caption_geometry_selection_anddisplay_pending', 'source_name_term_control_andformatting_binding_pending',
        'source_context_localization_formatting_gates_pending', 'native_name_controls_andfresh_formatting_pending',
        'all_five_review_gates_pending', 'native_complete_choice_object_binding_pending'}
    for bound in bindings:
        original, origin = originals[(bound['file_path'], bound['id'])]
        assert all(bound[k] == original[k] for k in ['source_reference', 'source_hex', 'current_reference',
            'current_hex', 'decision', 'finding', 'review'])
        row = deepcopy(original)
        row['planned_integrated_reference'] = bound['registered_reference']
        for key in intake_holds:
            if row.get(key):
                row[key] = False
                cleared.append(dict(id=row['id'], superseded_intake_hold=key))
        row.update(registered_integration_pending=False, registered_release_andcompletion_credit_pending=False,
            new_source_credit_eligible=True, registered_target_ROM=str(candidate),
            registered_target_ROM_sha256=release['candidate_sha256'], source_review_manuscript=str(origin),
            source_review_manuscript_sha256=sha(origin.read_bytes()))
        rows.append(row)
    keys = [dict(file_path=r['file_path'], id=r['id']) for r in rows]
    assert len(rows) == len({(r['file_path'], r['id']) for r in rows}) == 516
    assert (sum(r['decision'] == 'revision' for r in rows), sum(r['decision'] == 'retention' for r in rows)) == (246, 270)
    before = LEDGER.read_bytes()
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 11845 and not prior['full_goal_complete']
    assert prior['current_integrated_candidate']['sha256'] == release['parent_sha256']
    assert all(prior[k]['new_credit'] == 0 for k in [KEY261, KEY255, 'Rafael516_registered_cumulative_20261105'])
    assert FAMILY not in prior and not any(u['id'] == FAMILY for u in prior['coverage_units'])
    context = deepcopy(prior[CONTEXT])
    oldkeys = {(r['file_path'], r['id']) for r in context['record_keys']}
    assert len(oldkeys) == len(context['integrated_record_keys']) == 11845
    assert not oldkeys & {(r['file_path'], r['id']) for r in keys}
    scope = dict(source_variants=498, native_body_pages=504, typed_labels=18,
        observed_source_variants=118, observed_body_pages=121, offline_only_source_variants=380,
        per_batch_observation_scope=release['batches'], own_registered_startup_frames=4001,
        exact_same_ROM_startup_capture_reused=True, new_startup_emulator_run=False,
        natural_conditional_activation=False, original_locations=False, full_route=False, hardware=False,
        full_catalogue_UI_unvisited=True, guide_photos=False)
    save(FINAL, dict(format='dk4-composite-integrated-editorial-review-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', records=rows, records_count=516, new_source_records=516,
        proposed_new_revisions=246, justified_new_retentions=270, all516_individual_five_gates_pass=True,
        target_ROM=str(candidate), target_ROM_sha256=release['candidate_sha256'],
        registered_release=str(rp), registered_release_sha256=sha(rp.read_bytes()), actual_verification_scope=scope,
        cleared_superseded_intake_flags=cleared,
        superseded_intake_flags_cleared_only_after_complete_registered_source_current_controls_storage_display_binding=True,
        wording_source_current_findings_decisions_andall_five_gates_preserved=True,
        full_goal_complete=False, new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [bp, rp, sp, np, Path(__file__)]}))
    family = dict(id=FAMILY, kind='story-contextual-records', records=516, record_keys=keys,
        final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()), revised_count=246, retained_count=270,
        fresh_revisions=246, fresh_retentions=270, actual_verification_scope=scope, integrated_record_bindings=str(bp))
    ledger = dict(prior)
    ledger['completed_editorial_families'] = [*prior['completed_editorial_families'], family]
    ledger['coverage_units'] = [*prior['coverage_units'], dict(**family,
        status='complete-contextual-native-stored-representative-registered-release', completion_credit_added=516,
        release_verification=str(rp), release_verification_sha256=sha(rp.read_bytes()), full_goal_complete=False)]
    for field, number in [('records_editorially_completed', 516), ('records_revised_and_integrated', 246),
                         ('retained_wordings_editorially_completed', 270), ('records_with_source_and_prose_pass', 516),
                         ('records_with_source_prose_drafts', 516)]:
        ledger[field] += number
    for field in ['record_keys', 'integrated_record_keys']:
        context[field].extend(keys)
    context['record_IDs'].extend(r['id'] for r in rows)
    context['fresh_pass_records_explicitly_reread'] += 516
    context['fresh_pass_records_integrated'] += 516
    context.update(latest_completed_family=FAMILY, latest_final_review=str(FINAL))
    context['reconciled_families'].append(dict(id=FAMILY, records=516, final_review=str(FINAL), new_revisions=246,
        justified_retentions=270, new_completed_records=516, historical_reconciliation_only=False, actual_verification_scope=scope))
    ledger[CONTEXT] = context
    completed = dict(registered_integration_pending=False, completed_in_combined_family=FAMILY,
        registered_release_verification=str(rp), registered_release_verification_sha256=sha(rp.read_bytes()),
        own_registered_startup=str(sp), own_registered_startup_sha256=sha(sp.read_bytes()),
        own_Fernan_name_getters=str(np), own_Fernan_name_getters_sha256=sha(np.read_bytes()), main_unchanged=True)
    for key, count in [(KEY261, 261), (KEY255, 255)]:
        ledger[key] = {**prior[key], **completed, 'new_credit': count, 'completion_credit_added': count,
            'all_fifth_formatting_gates_pending': False, 'all_five_registered_review_gates_pass': True}
    ledger['Rafael516_registered_cumulative_20261105'] = {
        **prior['Rafael516_registered_cumulative_20261105'], **completed, 'new_credit': 0,
        'final_candidate_patch_startup_andcredit_pending': False, 'registered_continuation_needed': False,
        'original_failed_build_preserved': True, 'completed_via_explicit_registered_resume_profile': release['profile'],
        'total_new_source_records_credited_as_combined_family': 516}
    ledger[FAMILY] = dict(**completed, new_credit=0, total_new_source_records_credited=516,
        final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()))
    current = deepcopy(prior['current_integrated_candidate'])
    current.update(path=str(candidate), sha256=release['candidate_sha256'], profile=release['profile'],
        SC0_sha256=release['target_SC0_sha256'], patch=release['patch'], patch_sha256=release['patch_sha256'],
        manifest=release['manifest'], manifest_sha256=release['manifest_sha256'], registered_release_verification=str(rp),
        experimental_not_promoted=True, own_registered_startup_verified=True, clean_input_patch_byte_exact=True)
    ledger['current_integrated_candidate'] = current
    ledger['latest_checkpoint'] = ('Rafael516 registered and credited once:12361 completions/7082 revisions/5279 retentions;'
        '680 entries/114 accepted layers/eight stages/exact clean patch/own same-identity startup/Fernan getters pass. '
        'The canonical checkpoint was reused explicitly. Rafael351 remains research-ready for next integration;main/full scope unchanged.')
    allowed = {'completed_editorial_families', 'coverage_units', 'records_editorially_completed', 'records_revised_and_integrated',
        'retained_wordings_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
        CONTEXT, KEY261, KEY255, 'Rafael516_registered_cumulative_20261105', FAMILY, 'current_integrated_candidate', 'latest_checkpoint'}
    assert {k: v for k, v in ledger.items() if k not in allowed} == {k: v for k, v in prior.items() if k not in allowed}
    for field in ['record_keys', 'integrated_record_keys', 'record_IDs', 'reconciled_families']:
        assert context[field][:len(prior[CONTEXT][field])] == prior[CONTEXT][field]
    assert len(context['record_keys']) == len(context['integrated_record_keys']) == ledger['records_editorially_completed'] == 12361
    assert (ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (7082, 5279)
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 12364
    backup = ROOT / 'ledger_before_completion.json.gz'
    assert not backup.exists()
    backup.write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    encoded = encode_ledger(ledger)
    pending = LEDGER.with_name('editorial_review_current.Rafael516_resume_v2.pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == before
    pending.write_bytes(encoded)
    save(ROOT / 'completion_mutation_plan.json', dict(ledger_before_sha256=sha(before), ledger_after_sha256=sha(encoded),
        pending=str(pending), family=FAMILY, new_credit=516, all_unrelated_keys_andearlier_record_prefixes_exact=True))
    os.replace(pending, LEDGER)
    assert LEDGER.read_bytes() == encoded
    save(ROOT / 'completion_checkpoint.json', dict(family=FAMILY, new_credit=516,
        counts=dict(completed=12361, revised=7082, retained=5279), source_prose_draft_historical_counts=12364,
        ledger_before_sha256=sha(before), ledger_after_sha256=sha(encoded),
        all_unrelated_keys_andearlier_record_prefixes_exact=True, main_unchanged=True, full_goal_complete=False,
        registered_release=str(rp), registered_release_sha256=sha(rp.read_bytes()), guide_photos=False))
    print('Credited516 unique source objects once:12361 completed/7082 revisions/5279 retentions. Main unchanged;351 research-ready next. Full goal active.')


if __name__ == '__main__':
    main()
