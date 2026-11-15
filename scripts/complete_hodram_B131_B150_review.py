"""Credit this complete registered batch once after exact clean patch and own startup."""
import gzip
from collections import Counter
from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B131_B150_release_verified_20261102')
LEDGER = Path('translations/editorial_review_current_v1.json')
FINAL = Path('translations/hodram_B131_B150_contextual_final_review_v1.json')
RELEASE = ROOT / 'registered_release_verification.json'
STARTUP = ROOT / 'own_registered_startup_verification.json'
FAMILY = 'Hodram_SC1B131_B150_complete_contextual_release_20261102'


def main():
    doc, release, startup = map(load, [FINAL, RELEASE, STARTUP])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert sha(STARTUP.read_bytes()) == release['own_registered_startup_sha256']
    assert release['candidate_sha256'] == startup['candidate_sha256'] == sha(Path(release['candidate']).read_bytes())
    manifest = load(release['manifest'])
    assert len(manifest['batches']) == release['complete_stack_entries'] == 660
    assert all(manifest['checks'].values()) and release['accepted_layers'] == 114
    assert manifest['checks']['registered_grouped_owned_name_fields_and_complete_parent_target_inverse']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert sha(Path(release['exact_clean_reconstruction']).read_bytes()) == release['candidate_sha256']
    assert len(doc['records']) == 329 and (doc['revised'], doc['retained']) == (180, 149)
    main_path = Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(main_path.read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image = NdsImage.open(release['candidate'])
    archive = image.read_file(doc['file_path'])
    blocks = IlnkContainer.parse(archive).blocks
    pixels = load('work/analysis/Hodram_B131_B150_actual_pixels_20261102/focused_actual_pixels.json')
    observed, equivalent = {}, {}
    for sample in pixels['body_pages']:
        candidates = sample['native_equivalent_candidates']
        for item in candidates:
            equivalent.setdefault(item['id'], []).append(sample)
        if len(candidates) == 1:
            observed.setdefault(candidates[0]['id'], []).append(sample)
    bindings = []
    for row in doc['records']:
        assert all(row['review'][g] is True for g in doc['review_gates'])
        reference = deepcopy(row['planned_integrated_reference'])
        raw = bytes.fromhex(reference.pop('exact_stored_hex'))
        block, at = blocks[row['block']], reference['offset']
        assert block[at:at + len(raw) + 1] == raw + b'\0'
        assert sha(archive) == reference['target_archive_sha256']
        assert block[:at].count(b'\0') == reference['record_index']
        samples = observed.get(row['id'], [])
        if reference.get('virtual_prefix_not_stored'):
            command = reference['command_offset']
            header = bytes.fromhex(reference['final_header_hex'])
            assert len(header) == 20 and block[command:command + 20] == header
            assert int.from_bytes(header[:2], 'little') == 0x4100
            for index in reference['source_style_indices']:
                offset = int.from_bytes(header[2 + 2 * index:4 + 2 * index], 'little')
                assert command + 20 + offset == at
        elif row['kind'] == 'typed-choice-label':
            command, index = reference['command_offset'], row['source_index']
            count = row['source_count']
            assert count == 2 and int.from_bytes(block[command:command + 2], 'little') == 0x2100
            offset = int.from_bytes(block[command + 2 + 2 * index:command + 4 + 2 * index], 'little')
            assert command + 2 + 2 * count + offset == at
            samples = [dict(**sample, source_index=index) for sample in pixels['menu_samples']] if row['block'] == 136 else []
        else:
            assert block[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
        bindings.append(dict(id=row['id'], file_path=row['file_path'], kind=row['kind'],
            source_reference=row['source_reference'], source_hex=row['source_hex'], current_reference=row['current_reference'], current_hex=row['current_hex'],
            registered_reference=reference, registered_stored_hex=raw.hex(), registered_ROM_sha256=release['candidate_sha256'],
            decision=row['decision'], finding=row['finding'], localization_note=row['localization_note'], retention_reason=row['retention_reason'], review=row['review'],
            actual_unique_plane_bound_samples=samples,
            ambiguous_plane_equivalences_not_individual_occurrence_proof=[s for s in equivalent.get(row['id'], []) if s['ambiguous_occurrence']],
            offline_complete_display_andrepresentative_gameplay_distinguished=True))
    scope = dict(initialized_fixture_runs=5, fixture_frames=59005, source_control_runs=1, source_control_frames=5001,
        own_registered_startup_frames=4001, captured_body_planes_matched=83, native_record_page_equivalences=75,
        menu_caption_instances=4, actual_name_headers=2, directly_viewed_actual_sheets=19,
        source_personality4_Rafael0_FI_two_highlights_decline_branch_FE_headings_pause_andport_returns_observed=True,
        unvisited_andfixture_limits='See work/analysis/Hodram_B131_B150_checked_20261102/actual_review.json. B133 clean-Japanese control reproduces the initialized fixture C600 battle fault;natural battle activation/transition is unvisited. Other conditional paths,seven personality classes,four menus andthree changed full-catalogue UIs remain offline-only. Identical text equivalence does not establish a particular source occurrence. No earned chronology,full-route,hardware orlive backing-ownership claim.')
    binding_path = ROOT / 'integrated_record_bindings.json'
    assert not binding_path.exists()
    binding_doc = dict(candidate=release['candidate'], candidate_sha256=release['candidate_sha256'], records=bindings,
        final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()), actual_verification_scope=scope, new_credit=0)
    before = LEDGER.read_bytes()
    ledger = load(LEDGER)
    original = deepcopy(ledger)
    assert ledger['records_editorially_completed'] == 8527 and not ledger['full_goal_complete']
    assert not any(r['id'] == FAMILY for r in ledger['coverage_units'])
    context = ledger['contextual_story_natural_dialogue_pass_v1871']
    keys = [dict(file_path=r['file_path'], id=r['id']) for r in doc['records']]
    existing = {(r['file_path'], r['id']) for r in context['record_keys']}
    assert len(existing) == len(context['integrated_record_keys']) == 8527
    assert not existing & {(r['file_path'], r['id']) for r in keys}
    family = dict(id=FAMILY, file_path=doc['file_path'], blocks=doc['blocks'], record_IDs=[r['id'] for r in doc['records']], records=329,
        ordinary_speeches=311, personality_alternatives=8, personality_alias_slots=8, typed_choices=10, typed_choice_commands=5,
        final_review=str(FINAL), revised_count=180, retained_count=149, fresh_revisions=180, fresh_retentions=149,
        layout_findings_resolved=23, scoped_name_decisions=20, additional_name_metadata_fields=2, additional_name_field_owners=3,
        name_bytes_changed=4, actual_verification_scope=scope, integrated_record_bindings=str(binding_path))
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append(dict(**family, status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=329, final_review_sha256=sha(FINAL.read_bytes()), release_verification=str(RELEASE),
        release_verification_sha256=sha(RELEASE.read_bytes()), full_goal_complete=False))
    for key, amount in [('records_editorially_completed', 329), ('records_revised_and_integrated', 180),
                        ('retained_wordings_editorially_completed', 149), ('records_with_source_and_prose_pass', 329), ('records_with_source_prose_drafts', 329)]:
        ledger[key] += amount
    context['record_keys'].extend(keys)
    context['integrated_record_keys'].extend(keys)
    context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread'] += 329
    context['fresh_pass_records_integrated'] += 329
    context['latest_completed_family'], context['latest_final_review'] = FAMILY, str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY, records=329, ordinary_speeches=311, personality_alternatives=8, typed_choices=10,
        final_review=str(FINAL), new_revisions=180, justified_retentions=149, new_completed_records=329,
        historical_reconciliation_only=False, actual_optional_event_selected=False, actual_verification_scope=scope))
    ledger['Hodram_B131_B150_five_gate_research_20261102'].update(registered_release_andcompletion_credit_pending=False,
        completion_credit_added=329, current_registered_ROM_andmain_unchanged=False, main_unchanged=True,
        build_session=3816, build_status='complete', build_exit_code=0,
        release_verification=str(RELEASE), release_verification_sha256=sha(RELEASE.read_bytes()))
    ledger['current_integrated_candidate'] = dict(path=release['candidate'], sha256=release['candidate_sha256'], profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')), ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        patch=release['patch'], patch_sha256=release['patch_sha256'], manifest=release['manifest'], manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE), experimental_not_promoted=True, own_registered_startup_verified=True, clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint'] = 'Registered B131–B150/names verified:329 once-only completions;8856 completed.180 revisions/149 retentions,23 layout fixes,three name corrections in four bytes.660 entries/114 accepted layers,exact clean patch andown startup pass. Main unchanged;continue clean-first B151 onward andall remaining prose families. B133 initialized battle limit source-controlled;full goal active;no guide photos.'
    counts = Counter(r['file_path'] for r in context['record_keys'])
    assert counts['/data/SC1.DK4'] == 1776
    assert len(context['record_keys']) == len(context['integrated_record_keys']) == ledger['records_editorially_completed'] == 8856
    assert (ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5540, 3316)
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 8859
    assert ledger['current_native_relocation_reference'] == original['current_native_relocation_reference']
    allowed = {'completed_editorial_families', 'coverage_units', 'records_editorially_completed', 'records_revised_and_integrated',
        'retained_wordings_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
        'contextual_story_natural_dialogue_pass_v1871', 'Hodram_B131_B150_five_gate_research_20261102', 'current_integrated_candidate', 'latest_checkpoint'}
    assert {k: v for k, v in ledger.items() if k not in allowed} == {k: v for k, v in original.items() if k not in allowed}
    for name in ['record_keys', 'integrated_record_keys', 'record_IDs', 'reconciled_families']:
        old = original['contextual_story_natural_dialogue_pass_v1871'][name]
        assert context[name][:len(old)] == old
    save(binding_path, binding_doc)
    ledger['coverage_units'][-1]['integrated_record_bindings_sha256'] = sha(binding_path.read_bytes())
    backup = ROOT / 'ledger_before_completion.json.gz'
    assert not backup.exists()
    backup.write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    staged = encode_ledger(ledger)
    assert LEDGER.read_bytes() == before
    LEDGER.write_bytes(staged)
    assert sha(LEDGER.read_bytes()) == sha(staged)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    work = Path('work/analysis/Hodram_B131_B150_registered_build_20261102')
    for path in sorted(work.rglob('*.nds')):
        absolute = str(path.resolve())
        if not any(r['path'] == absolute for r in pins):
            pins.append(dict(path=absolute, reason='Preserve registered B131–B150 reconstruction stage;all ROMs retained. SHA256 ' + sha(path.read_bytes())))
    save(pins_path, pins)
    save(ROOT / 'completion_checkpoint.json', dict(family=FAMILY, new_credit=329,
        counts=dict(completed=8856, source_prose_anddrafts=8859, integrated_revisions=5540, retentions=3316), completed_by_file=dict(counts),
        candidate=release['candidate'], candidate_sha256=release['candidate_sha256'], release_verification=str(RELEASE),
        release_verification_sha256=sha(RELEASE.read_bytes()), own_startup=str(STARTUP), own_startup_sha256=sha(STARTUP.read_bytes()),
        ledger_sha256=sha(staged), prior_ledger_bytes_sha256=sha(before), all_prior_records_andunrelated_scope_preserved=True,
        all_generated_ROMs_andprior_work_preserved=True, main_unchanged=True, full_goal_complete=False))
    print('329 once-only completions:8856 total;5540 revisions/3316 retentions. Main unchanged;full goal active.')


if __name__ == '__main__':
    main()
