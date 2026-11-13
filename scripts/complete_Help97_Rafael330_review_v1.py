"""Credit427 unique source objects only after registered release/patch/own-RAM checks."""
import gzip
import os
import time
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Help97_Rafael330_release_verified_20261105')
LEDGER = Path('translations/editorial_review_current_v1.json')
FINAL = Path('translations/Help97_Rafael330_integrated_final_review_v1.json')
FAMILY = 'shared_HELP97_Rafael_SC0_B81_B84_complete_contextual_release_20261105'
KEY30 = 'shared_HELP_T103_T132_contextual_20261104'
KEY67 = 'shared_HELP_T133_T201_contextual_20261105'
KEY33 = 'shared_HELP33_Speech_amendment_20261105'
COMBINED = 'Help97_Rafael330_registered_cumulative_20261105'
RAFAEL = 'Rafael_SC0_B81_B84_contextual_integrated_20261105'

if __name__ == '__main__':
    assert not FINAL.exists() and not (ROOT/'completion_checkpoint.json').exists()
    rp, sp, np = [ROOT/p for p in ['registered_release_verification.json', 'own_registered_startup_verification.json', 'own_Fernan_name_getter_verification.json']]
    release, startup, names = map(load, [rp, sp, np])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(sp.read_bytes()) == release['own_registered_startup_sha256']
    candidate = Path(release['candidate'])
    assert sha(candidate.read_bytes()) == release['candidate_sha256'] == startup['candidate_sha256'] == names['runtime']['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes() == candidate.read_bytes()
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (678, 114, 26)
    assert release['all_eight_registered_final_stages_preserved'] and release['all427_exact_integrated_references_bound']
    assert sha(Path('translations/release_stack.json').read_bytes()) == release['registry_sha256']
    assert startup['actual_captain_getter'] == startup['actual_route_word'] == 0
    assert startup['changed_HELP_andSC0_exact_composite_refs_bound']
    assert names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    bp, cp = map(Path, [release['exact_record_bindings'], release['composite_page_coverage']])
    assert sha(bp.read_bytes()) == release['exact_record_bindings_sha256']
    assert sha(cp.read_bytes()) == release['composite_page_coverage_sha256']
    bindings, coverage = map(load, [bp, cp])
    assert len(bindings['records']) == 428 and not coverage['all_content_observed_on_one_final_ROM']
    prep = load(release['preparation'])
    selected = {}
    for config in prep['configs']:
        conf = load(config)
        path = Path(conf['manuscript'])
        doc = load(path)
        for row in doc['records']:
            key = row['file_path'], row['id']
            assert key not in selected and all(row['review'].values())
            selected[key] = (row, path)
    rows = []
    for bound in bindings['records']:
        row, origin = selected[(bound['file_path'], bound['id'])]
        assert all(bound[k] == row[k] for k in ['source_reference', 'source_hex', 'current_reference', 'current_hex', 'decision'])
        final = deepcopy(row)
        if 'registered_pages' in bound:
            final['planned_stored_pages'] = bound['registered_pages']
        else:
            final['planned_integrated_reference'] = bound['registered_reference']
        final.update(new_source_credit_eligible=bound['new_source_credit_eligible'],
            registered_target_ROM=str(candidate), registered_target_ROM_sha256=release['candidate_sha256'],
            registered_integration_pending=False, registered_release_andcompletion_credit_pending=False,
            source_review_manuscript=str(origin), source_review_manuscript_sha256=sha(origin.read_bytes()))
        rows.append(final)
    new = [r for r in rows if r['new_source_credit_eligible']]
    assert (len(new), sum(r['decision'] == 'revision' for r in new), sum(r['decision'] == 'retention' for r in new)) == (427, 191, 236)
    before = LEDGER.read_bytes()
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 11418 and not prior['full_goal_complete']
    assert prior['current_integrated_candidate']['sha256'] == release['parent_sha256']
    for key in [KEY30, KEY67, KEY33, COMBINED]:
        assert prior[key].get('new_credit', 0) == 0
    assert RAFAEL not in prior and not any(r['id'] == FAMILY for r in prior['coverage_units'])
    contextkey = 'contextual_story_natural_dialogue_pass_v1871'
    context = deepcopy(prior[contextkey])
    keys = [dict(file_path=r['file_path'], id=r['id']) for r in new]
    oldkeys = {(r['file_path'], r['id']) for r in context['record_keys']}
    assert len(oldkeys) == len(context['integrated_record_keys']) == 11418
    assert not oldkeys & {(r['file_path'], r['id']) for r in keys}
    amendments = [r for r in rows if not r['new_source_credit_eligible']]
    assert len(amendments) == 1 and amendments[0]['id'] == 'HELP_TOPIC_33'
    assert (amendments[0]['file_path'], amendments[0]['id']) in oldkeys
    save(FINAL, dict(format='dk4-composite-integrated-editorial-review-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        records=rows, records_count=428, new_source_records=427, proposed_new_revisions=191, justified_new_retentions=236,
        previously_credited_amendments=[33], all428_individual_five_gates_pass=True, target_ROM=str(candidate), target_ROM_sha256=release['candidate_sha256'],
        registered_release=str(rp), registered_release_sha256=sha(rp.read_bytes()), composite_page_coverage=str(cp), composite_page_coverage_sha256=sha(cp.read_bytes()),
        reference_policy='Each source/current reference keeps its original comparison ROM. Final stored offsets are rebound. Composite Help observations and initialized Rafael fixtures are not a natural final-ROM playthrough.',
        full_goal_complete=False, new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [bp, cp, rp, sp, np, Path(__file__)]}))
    scope = dict(composite_provenance=str(cp), composite_provenance_sha256=sha(cp.read_bytes()),
        help=coverage['help'], story=coverage['story'], own_registered_Rafael_startup_frames=4001,
        all_content_observed_on_one_final_ROM=False, natural_story_activation=False, full_route=False, hardware=False, guide_photos=False)
    family = dict(id=FAMILY, kind='help-and-story-contextual-records', records=427, help_articles=97, source_speeches=325, typed_choices=5,
        record_keys=keys, final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()), revised_count=191, retained_count=236,
        fresh_revisions=191, fresh_retentions=236, actual_verification_scope=scope, integrated_record_bindings=str(bp))
    ledger = dict(prior)
    ledger['completed_editorial_families'] = [*prior['completed_editorial_families'], family]
    ledger['coverage_units'] = [*prior['coverage_units'], dict(**family, status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=427, release_verification=str(rp), release_verification_sha256=sha(rp.read_bytes()), full_goal_complete=False)]
    for key, n in [('records_editorially_completed', 427), ('records_revised_and_integrated', 191), ('retained_wordings_editorially_completed', 236),
                   ('records_with_source_and_prose_pass', 427), ('records_with_source_prose_drafts', 427)]:
        ledger[key] += n
    for field in ['record_keys', 'integrated_record_keys']:
        context[field].extend(keys)
    context['record_IDs'].extend(r['id'] for r in new)
    context['fresh_pass_records_explicitly_reread'] += 427
    context['fresh_pass_records_integrated'] += 427
    context['latest_completed_family'] = FAMILY
    context['latest_final_review'] = str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY, records=427, help_articles=97, final_review=str(FINAL), new_revisions=191,
        justified_retentions=236, new_completed_records=427, historical_reconciliation_only=False, actual_verification_scope=scope))
    ledger[contextkey] = context
    completed = dict(registered_integration_pending=False, registered_build_live=False, build_live=False,
        build_terminal=True, build_exit_code=0, completed_in_combined_family=FAMILY,
        registered_release_verification=str(rp), registered_release_verification_sha256=sha(rp.read_bytes()),
        own_registered_startup=str(sp), own_registered_startup_sha256=sha(sp.read_bytes()),
        own_Fernan_name_getters=str(np), own_Fernan_name_getters_sha256=sha(np.read_bytes()), main_unchanged=True)
    for key, count in [(KEY30, 30), (KEY67, 67)]:
        ledger[key] = {**prior[key], **completed, 'new_credit': count, 'completion_credit_added': count}
    for key in [KEY33, COMBINED]:
        ledger[key] = {**prior[key], **completed, 'new_credit': 0,
            'registered_manifest_patch_RAM_binding_andonce_only_credit_pending': False,
            'total_new_source_records_credited_as_combined_family': 427 if key == COMBINED else 0}
    ledger[RAFAEL] = dict(**completed, new_credit=330, completion_credit_added=330, source_speeches=325, source_choice_labels=5,
        proposed_revisions=174, justified_retentions=156, final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()))
    image = NdsImage.open(candidate)
    ledger['current_integrated_candidate'] = dict(path=str(candidate), sha256=release['candidate_sha256'], profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')), ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        HELP_sha256=release['target_HELP_sha256'], SC0_sha256=release['target_SC0_sha256'], patch=release['patch'], patch_sha256=release['patch_sha256'],
        manifest=release['manifest'], manifest_sha256=release['manifest_sha256'], registered_release_verification=str(rp),
        experimental_not_promoted=True, own_registered_startup_verified=True, clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint'] = 'Help97 andRafael330 integrated once:11845 completions/6836 revisions/5009 retentions;Coerce33 amendment earns no duplicate credit.678 entries/114 layers/eight stages/exact clean patch/own startup/Fernan getters pass. Next Rafael261 formatting/storage work continues;main andfull scope unchanged.'
    assert len(context['record_keys']) == len(context['integrated_record_keys']) == ledger['records_editorially_completed'] == 11845
    assert (ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (6836, 5009)
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 11848
    allowed = {'completed_editorial_families', 'coverage_units', 'records_editorially_completed', 'records_revised_and_integrated',
        'retained_wordings_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts', contextkey,
        KEY30, KEY67, KEY33, COMBINED, RAFAEL, 'current_integrated_candidate', 'latest_checkpoint'}
    assert {k: v for k, v in ledger.items() if k not in allowed} == {k: v for k, v in prior.items() if k not in allowed}
    for field in ['record_keys', 'integrated_record_keys', 'record_IDs', 'reconciled_families']:
        assert context[field][:len(prior[contextkey][field])] == prior[contextkey][field]
    backup = ROOT/'ledger_before_completion.json.gz'
    assert not backup.exists()
    backup.write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    encoded = encode_ledger(ledger)
    pending = LEDGER.with_name('editorial_review_current.Help97_Rafael330_completion.pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == before
    pending.write_bytes(encoded)
    save(ROOT/'completion_mutation_plan.json', dict(ledger_before_sha256=sha(before), ledger_after_sha256=sha(encoded),
        pending=str(pending), family=FAMILY, new_credit=427, all_unrelated_keys_andearlier_record_prefixes_exact=True))
    for attempt in range(5):
        try:
            os.replace(pending, LEDGER)
            break
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.25)
    assert LEDGER.read_bytes() == encoded
    save(ROOT/'completion_checkpoint.json', dict(family=FAMILY, new_credit=427, counts=dict(completed=11845, revised=6836, retained=5009),
        ledger_before_sha256=sha(before), ledger_after_sha256=sha(encoded), all_unrelated_keys_andearlier_record_prefixes_exact=True,
        source_prose_draft_historical_counts=11848, main_unchanged=True, full_goal_complete=False, guide_photos=False))
    print('Credited427 unique source objects once:11845 completed/6836 revisions/5009 retentions. Main unchanged;full goal active.')
