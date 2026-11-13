"""Credit642 reviews once, only after registered patch and candidate-own startup pass."""
import gzip
import os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B151_B170_release_verified_20261102')
LEDGER = Path('translations/editorial_review_current_v1.json')
FINAL = Path('translations/hodram_B151_B170_contextual_final_review_v1.json')
RELEASE = ROOT / 'registered_release_verification.json'
STARTUP = ROOT / 'own_registered_startup_verification.json'
FAMILY = 'Hodram_SC1B151_B170_complete_contextual_release_20261102'
KEY = 'Hodram_B151_B170_clean_next_20261102'


def main():
    assert not (ROOT / 'completion_checkpoint.json').exists()
    doc, release, startup = map(load, [FINAL, RELEASE, STARTUP])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert sha(STARTUP.read_bytes()) == release['own_registered_startup_sha256']
    assert release['candidate_sha256'] == startup['candidate_sha256'] == sha(Path(release['candidate']).read_bytes())
    manifest = load(release['manifest'])
    assert all(manifest['checks'].values()) and release['accepted_layers'] == 114
    assert manifest['checks']['registered_owned_static_text_and_complete_parent_target_inverse']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert sha(Path(release['exact_clean_reconstruction']).read_bytes()) == release['candidate_sha256']
    assert (len(doc['records']), doc['proposed_revisions'], doc['wording_retentions']) == (642, 269, 373)
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image = NdsImage.open(release['candidate'])
    archive = image.read_file(doc['file_path'])
    blocks = IlnkContainer.parse(archive).blocks
    pixels = load('work/analysis/Hodram_B151_B170_actual_pixels_20261102/focused_actual_pixels.json')
    # All matched body captures precede the fixtures' following content. Pixel
    # equivalence alone must never reclassify a later opening/port line as a
    # particular target occurrence.
    target_capture_limits = dict(cinematic=(2816, 13300), focused=(2816, 9054), second=(4006, 6653))
    assert all(target_capture_limits[s['run']][0] <= s['frame'] < target_capture_limits[s['run']][1]
        for s in pixels['body_pages'])
    actual_path = Path('work/analysis/Hodram_B151_B170_checked_20261102/actual_review.json')
    actual = load(actual_path)
    bindings = []
    for row in doc['records']:
        assert all(row['review'][g] is True for g in doc['review_gates'])
        reference = deepcopy(row['planned_integrated_reference'])
        raw = bytes.fromhex(reference.pop('exact_stored_hex'))
        at, block = reference['offset'], blocks[row['block']]
        assert block[at:at + len(raw) + 1] == raw + b'\0' and sha(archive) == reference['target_archive_sha256']
        assert block[:at].count(b'\0') == reference['record_index']
        if row['kind'] == 'typed-choice-label':
            command, index = reference['command_offset'], row['source_index']
            assert row['source_count'] == 2 and int.from_bytes(block[command:command + 2], 'little') == 0x2100
            offset = int.from_bytes(block[command + 2 + 2 * index:command + 4 + 2 * index], 'little')
            assert command + 6 + offset == at
            samples = [dict(**s, source_index=index) for s in pixels['menu_samples']] if row['source_command_offset'] == 1314 and row['block'] == 170 else []
            equivalent = []
        else:
            assert block[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
            samples = [s for s in pixels['body_pages'] if len(s['native_equivalent_candidates']) == 1 and s['native_equivalent_candidates'][0]['id'] == row['id']]
            equivalent = [s for s in pixels['body_pages'] if s['ambiguous_occurrence'] and any(c['id'] == row['id'] for c in s['native_equivalent_candidates'])]
        bindings.append(dict(id=row['id'], file_path=row['file_path'], kind=row['kind'],
            source_reference=row['source_reference'], source_hex=row['source_hex'],
            current_reference=row['current_reference'], current_hex=row['current_hex'],
            registered_reference=reference, registered_stored_hex=raw.hex(), registered_ROM_sha256=release['candidate_sha256'],
            decision=row['decision'], finding=row['finding'], localization_note=row['localization_note'],
            retention_reason=row['retention_reason'], review=row['review'], actual_unique_plane_bound_samples=samples,
            ambiguous_plane_equivalences_not_individual_occurrence_proof=equivalent,
            offline_complete_display_andrepresentative_gameplay_distinguished=True))
    binding_path = ROOT / 'integrated_record_bindings.json'
    assert not binding_path.exists()
    before = LEDGER.read_bytes()
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 8856 and not prior['full_goal_complete']
    assert prior['current_integrated_candidate']['sha256'] == release['parent_sha256']
    assert not any(r['id'] == FAMILY for r in prior['coverage_units'])
    context = deepcopy(prior['contextual_story_natural_dialogue_pass_v1871'])
    keys = [dict(file_path=r['file_path'], id=r['id']) for r in doc['records']]
    existing = {(r['file_path'], r['id']) for r in context['record_keys']}
    assert len(existing) == len(context['integrated_record_keys']) == 8856
    assert not existing & {(r['file_path'], r['id']) for r in keys}
    scope = dict(initialized_fixture_runs=3, fixture_frames=43003, own_registered_startup_frames=4001,
        captured_body_planes_matched=134, native_record_page_equivalences=74, actual_name_headers=9,
        menu_caption_instances=4, directly_viewed_actual_sheets=6,
        actual_review=str(actual_path), actual_review_sha256=sha(actual_path.read_bytes()),
        unvisited_andfixture_limits=actual['unvisited'], duplicate_text_not_exact_occurrence=True,
        natural_activation=False, hardware=False, guide_photos=False)
    family = dict(id=FAMILY, file_path=doc['file_path'], blocks=doc['blocks'], record_IDs=[r['id'] for r in doc['records']],
        records=642, ordinary_speeches=634, personality_alternatives=0, typed_choices=8, typed_choice_commands=4,
        final_review=str(FINAL), revised_count=269, retained_count=373, fresh_revisions=269, fresh_retentions=373,
        layout_findings_resolved=26, scoped_name_term_decisions=39, native_name_strings=41,
        separately_owned_static_fields=2, static_owned_span_bytes=15, static_changed_bytes=12,
        actual_verification_scope=scope, integrated_record_bindings=str(binding_path))
    ledger = dict(prior)
    ledger['completed_editorial_families'] = [*prior['completed_editorial_families'], family]
    ledger['coverage_units'] = [*prior['coverage_units'], dict(**family,
        status='complete-contextual-native-stored-representative-registered-release', completion_credit_added=642,
        final_review_sha256=sha(FINAL.read_bytes()), release_verification=str(RELEASE),
        release_verification_sha256=sha(RELEASE.read_bytes()), full_goal_complete=False)]
    for key, amount in [('records_editorially_completed', 642), ('records_revised_and_integrated', 269),
        ('retained_wordings_editorially_completed', 373), ('records_with_source_and_prose_pass', 642), ('records_with_source_prose_drafts', 642)]:
        ledger[key] += amount
    context['record_keys'].extend(keys)
    context['integrated_record_keys'].extend(keys)
    context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread'] += 642
    context['fresh_pass_records_integrated'] += 642
    context['latest_completed_family'], context['latest_final_review'] = FAMILY, str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY, records=642, ordinary_speeches=634, personality_alternatives=0,
        typed_choices=8, final_review=str(FINAL), new_revisions=269, justified_retentions=373,
        new_completed_records=642, historical_reconciliation_only=False, actual_optional_event_selected=False,
        actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871'] = context
    entry = deepcopy(prior[KEY])
    entry.update(completion_credit_added=642, new_credit=642, registered_release_andcompletion_credit_pending=False,
        registered_integration_exact_clean_input_patch_andown_startup_pending=False,
        all642_fifth_formatting_gates_pending=False, representative_English_gameplay_andregistered_cumulative_release_pending=False,
        pending_actual_menu_controller=False, new_two_page_spacing_gameplay_pending=False,
        pending_static_label_integration=0, pending_static_text_proposals=0, pending_static_owned_prefix_bytes=0,
        pending_static_label_widget_compatibility_oractual_tests=False, static_label_ROM_mutation=True,
        static_labels_compact_source_envelope_andnative_consumer_qualified=True, static_city_ship_widgets_unvisited=True,
        B156_cinematic_geometry_andall642_formatting_pending=False,
        scoped_names_andAbkhaz_Abhaz_cross_consumer_localization_pending=False,
        separate_Elysion_code_literal_still_Japanese_pending_consumer_scope=False,
        all642_source_current_final_refs_andfive_gates=str(binding_path), actual_review=str(actual_path),
        actual_English_coldboot_frames=43003, actual_English_runs=3, actual_sheets=6,
        Rafael0_headers_observed=True, full_catalogue_UI_andstatic_label_widgets_unvisited=True,
        registered_release_verification=str(RELEASE), registered_release_verification_sha256=sha(RELEASE.read_bytes()),
        source_intake_flags_are_historical_current_status_supersedes=True, main_unchanged=True)
    ledger[KEY] = entry
    ledger['current_integrated_candidate'] = dict(path=release['candidate'], sha256=release['candidate_sha256'], profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')), ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        patch=release['patch'], patch_sha256=release['patch_sha256'], manifest=release['manifest'], manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE), experimental_not_promoted=True,
        own_registered_startup_verified=True, clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint'] = 'Registered B151–B170 verified and credited once:642 reviews/269 revisions/373 retentions;9498 complete.650 pages/26 layout fixes;Abkhaz/Elysion15 owned bytes/12 changed after all prior runtime/name stages. Exact clean patch/own startup pass. Full scope/main/ROMs preserved;continue clean-first B171 onward;no guide photos.'
    counts = Counter(r['file_path'] for r in context['record_keys'])
    assert counts['/data/SC1.DK4'] == 2418
    assert len(context['record_keys']) == len(context['integrated_record_keys']) == ledger['records_editorially_completed'] == 9498
    assert (ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5809, 3689)
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 9501
    allowed = {'completed_editorial_families', 'coverage_units', 'records_editorially_completed', 'records_revised_and_integrated',
        'retained_wordings_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
        'contextual_story_natural_dialogue_pass_v1871', KEY, 'current_integrated_candidate', 'latest_checkpoint'}
    assert {k: v for k, v in ledger.items() if k not in allowed} == {k: v for k, v in prior.items() if k not in allowed}
    for name in ['record_keys', 'integrated_record_keys', 'record_IDs', 'reconciled_families']:
        old = prior['contextual_story_natural_dialogue_pass_v1871'][name]
        assert context[name][:len(old)] == old
    save(binding_path, dict(candidate=release['candidate'], candidate_sha256=release['candidate_sha256'], records=bindings,
        final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()), actual_verification_scope=scope))
    ledger['coverage_units'][-1]['integrated_record_bindings_sha256'] = sha(binding_path.read_bytes())
    backup = ROOT / 'ledger_before_completion.json.gz'
    assert not backup.exists()
    backup.write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    staged = encode_ledger(ledger)
    temporary = LEDGER.with_name('editorial_review_current_v1.pending_B151_B170_completion.json')
    assert not temporary.exists() and LEDGER.read_bytes() == before
    temporary.write_bytes(staged)
    os.replace(temporary, LEDGER)
    assert sha(LEDGER.read_bytes()) == sha(staged)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path in Path('work/analysis/Hodram_B151_B170_registered_build_20261102').rglob('*.nds'):
        absolute = str(path.resolve())
        if not any(r['path'] == absolute for r in pins):
            pins.append(dict(path=absolute, reason='Preserve registered B151–B170 build stage;all ROMs retained. SHA256 ' + sha(path.read_bytes())))
    save(pins_path, pins)
    save(ROOT / 'completion_checkpoint.json', dict(family=FAMILY, new_credit=642,
        counts=dict(completed=9498, source_prose_anddrafts=9501, integrated_revisions=5809, retentions=3689),
        completed_by_file=dict(counts), candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
        release_verification=str(RELEASE), release_verification_sha256=sha(RELEASE.read_bytes()),
        own_startup=str(STARTUP), own_startup_sha256=sha(STARTUP.read_bytes()), ledger_sha256=sha(staged),
        prior_ledger_bytes_sha256=sha(before), all_prior_records_andunrelated_scope_preserved=True,
        all_generated_ROMs_andprior_work_preserved=True, main_unchanged=True, full_goal_complete=False, guide_photos=False))
    print('642 once-only completions:9498 total;5809 revisions/3689 retentions. Main unchanged;full goal active.')


if __name__ == '__main__':
    main()
