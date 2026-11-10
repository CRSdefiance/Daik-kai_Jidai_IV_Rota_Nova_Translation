"""Credit the registered mixed-object batch once, after exact patch and own startup."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B111_B130_release_verified_20261102')
LEDGER = Path('translations/editorial_review_current_v1.json')
FINAL = Path('translations/hodram_B111_B130_contextual_final_review_v1.json')
RELEASE = ROOT / 'registered_release_verification.json'
STARTUP = ROOT / 'own_registered_startup_verification.json'
FAMILY = 'Hodram_SC1B111_B130_complete_contextual_release_20261102'


def main():
    doc, release, startup = map(load, [FINAL, RELEASE, STARTUP])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert sha(STARTUP.read_bytes()) == release['own_registered_startup_sha256']
    assert release['candidate_sha256'] == startup['candidate_sha256'] == sha(Path(release['candidate']).read_bytes())
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (658, 114, 22)
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert sha(Path(release['exact_clean_reconstruction']).read_bytes()) == release['candidate_sha256']
    assert len(doc['records']) == 323 and (doc['revised'], doc['retained']) == (239, 84)
    image = NdsImage.open(release['candidate'])
    archive = image.read_file(doc['file_path'])
    blocks = IlnkContainer.parse(archive).blocks
    pixels = load('work/analysis/Hodram_B111_B130_actual_pixels_20261102/focused_actual_pixels.json')
    observed = {}
    for row in pixels['body_pages']:
        observed.setdefault(row['id'], []).append(row)
    bindings = []
    for row in doc['records']:
        assert all(row['review'][g] for g in doc['review_gates'])
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
                offset = int.from_bytes(header[2 + 2*index:4 + 2*index], 'little')
                assert command + 20 + offset == at
        elif row['kind'] == 'typed-choice-label':
            command, index = reference['command_offset'], row['source_index']
            count = row['source_count']
            assert count == 3 and int.from_bytes(block[command:command + 2], 'little') == 0x2200
            offset = int.from_bytes(block[command + 2 + 2*index:command + 4 + 2*index], 'little')
            assert command + 2 + 2*count + offset == at
            samples = [dict(**sample, source_index=index) for sample in pixels['menu_samples'] if sample['block'] == row['block']]
        else:
            assert block[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
        bindings.append(dict(
            id=row['id'], file_path=row['file_path'], kind=row['kind'],
            source_reference=row['source_reference'], source_hex=row['source_hex'],
            current_reference=row['current_reference'], current_hex=row['current_hex'],
            registered_reference=reference, registered_stored_hex=raw.hex(),
            registered_ROM_sha256=release['candidate_sha256'], decision=row['decision'],
            finding=row['finding'], localization_note=row['localization_note'],
            retention_reason=row['retention_reason'], review=row['review'],
            actual_ID_bound_samples=samples,
            offline_complete_display_andrepresentative_gameplay_distinguished=True))
    scope = dict(
        initialized_fixture_runs=5, fixture_frames=51005, own_registered_startup_frames=4001,
        explicitly_pixel_bound_speech_pages=21, explicitly_bound_menu_caption_instances=9,
        actual_name_headers=5, directly_viewed_actual_sheets=25,
        source_personality4_Rafael0_FI_Follower_menu_highlights_and59_branch_observed=True,
        unvisited_andfixture_limits='See work/analysis/Hodram_B111_B130_checked_20261102b/actual_review.json. Other conditional paths, personality classes, four other menus and Diogo full-catalogue UI retain offline scope. No natural activation, earned chronology, full-route, hardware or live backing-ownership claim.')
    binding_path = ROOT / 'integrated_record_bindings.json'
    assert not binding_path.exists()
    binding_doc = dict(candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
                       records=bindings, final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()),
                       actual_verification_scope=scope, new_credit=0)
    before = LEDGER.read_bytes()
    ledger = load(LEDGER)
    assert ledger['records_editorially_completed'] == 8204
    assert not any(r['id'] == FAMILY for r in ledger['coverage_units'])
    context = ledger['contextual_story_natural_dialogue_pass_v1871']
    keys = [dict(file_path=r['file_path'], id=r['id']) for r in doc['records']]
    existing = {(r['file_path'], r['id']) for r in context['record_keys']}
    assert len(existing) == len(context['integrated_record_keys']) == 8204
    assert not existing & {(r['file_path'], r['id']) for r in keys}
    backup = ROOT / 'ledger_before_completion.json'
    assert not backup.exists()
    family = dict(id=FAMILY, file_path=doc['file_path'], blocks=doc['blocks'],
                  record_IDs=[r['id'] for r in doc['records']], records=323,
                  ordinary_speeches=260, personality_alternatives=48, personality_alias_slots=64,
                  typed_choices=15, typed_choice_commands=5, final_review=str(FINAL),
                  revised_count=239, retained_count=84, fresh_revisions=239, fresh_retentions=84,
                  page_findings_resolved=7, FE_blank_rows_resolved=2, phrase_findings_resolved=2,
                  additional_name_metadata_fields=2, actual_verification_scope=scope,
                  integrated_record_bindings=str(binding_path))
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append(dict(**family,
        status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=323, final_review_sha256=sha(FINAL.read_bytes()),
        release_verification=str(RELEASE), release_verification_sha256=sha(RELEASE.read_bytes()),
        full_goal_complete=False))
    for key, amount in [('records_editorially_completed', 323), ('records_revised_and_integrated', 239),
                        ('retained_wordings_editorially_completed', 84), ('records_with_source_and_prose_pass', 323),
                        ('records_with_source_prose_drafts', 323)]:
        ledger[key] += amount
    context['record_keys'].extend(keys)
    context['integrated_record_keys'].extend(keys)
    context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread'] += 323
    context['fresh_pass_records_integrated'] += 323
    context['latest_completed_family'], context['latest_final_review'] = FAMILY, str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY, records=323, ordinary_speeches=260,
        personality_alternatives=48, typed_choices=15, final_review=str(FINAL), new_revisions=239,
        justified_retentions=84, new_completed_records=323, historical_reconciliation_only=False,
        actual_optional_event_selected=False, actual_verification_scope=scope))
    ledger['Hodram_B111_B130_five_gate_research_20261102'].update(
        registered_release_andcompletion_credit_pending=False, completion_credit_added=323,
        current_registered_ROM_andmain_unchanged=False, main_unchanged=True,
        build_session=28425, build_status='complete', build_exit_code=0,
        release_verification=str(RELEASE), release_verification_sha256=sha(RELEASE.read_bytes()))
    ledger['current_integrated_candidate'] = dict(path=release['candidate'], sha256=release['candidate_sha256'],
        profile=release['profile'], MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')), patch=release['patch'], patch_sha256=release['patch_sha256'],
        manifest=release['manifest'], manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE), experimental_not_promoted=True,
        own_registered_startup_verified=True, clean_input_patch_byte_exact=True)
    next_packet = Path('work/analysis/Hodram_B131_B150_clean_20261102/clean_source_packet.json')
    ledger['Hodram_B131_B150_clean_next_20261102'] = dict(packet=str(next_packet), packet_sha256=sha(next_packet.read_bytes()),
        ordinary_speeches=311, clean_only=True, earlier_English_unconsulted=True,
        all311_ordinary_clean_meanings_read=True, embedded_styles_andmenus_pending=True,
        ordinary_meanings_checkpoint='work/analysis/Hodram_B131_B150_clean_20261102/ordinary_meanings_checkpoint.json',
        B137_previously_completed_excluded=True, new_credit=0)
    ledger['latest_checkpoint'] = 'Registered B111-B130/names verified:323 once-only completions;8527 completed.239 revisions/84 retentions,seven page fixes,two FE blank rows,two short phrases,two name fields.658 entries/114 accepted layers/22 checks,exact clean patch and own startup pass. Main unchanged. Next311 ordinary clean speeches plus embedded objects pending intake;B137 already credited. Full goal active;no guide photos.'
    counts = Counter(r['file_path'] for r in context['record_keys'])
    assert counts['/data/SC1.DK4'] == 1447
    assert len(context['record_keys']) == len(context['integrated_record_keys']) == ledger['records_editorially_completed'] == 8527
    assert (ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5360, 3167)
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 8530
    assert ledger['current_native_relocation_reference'] == load(LEDGER)['current_native_relocation_reference']
    assert not ledger['full_goal_complete'] and LEDGER.read_bytes() == before
    save(binding_path, binding_doc)
    ledger['coverage_units'][-1]['integrated_record_bindings_sha256'] = sha(binding_path.read_bytes())
    backup.write_bytes(before)
    save(LEDGER, ledger)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    work = Path('work/analysis/Hodram_B111_B130_registered_build_20261102')
    for path in sorted(work.rglob('*.nds')):
        absolute = str(path.resolve())
        if not any(r['path'] == absolute for r in pins):
            pins.append(dict(path=absolute, reason='Preserve registered B111-B130 reconstruction stage;all ROMs retained. SHA256 ' + sha(path.read_bytes())))
    save(pins_path, pins)
    save(ROOT / 'completion_checkpoint.json', dict(family=FAMILY, new_credit=323,
        counts=dict(completed=8527, source_prose_anddrafts=8530, integrated_revisions=5360, retentions=3167),
        completed_by_file=dict(counts), candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
        release_verification=str(RELEASE), release_verification_sha256=sha(RELEASE.read_bytes()),
        own_startup=str(STARTUP), own_startup_sha256=sha(STARTUP.read_bytes()),
        all_generated_ROMs_andprior_work_preserved=True, main_unchanged=True, full_goal_complete=False))
    print('323 once-only completions:8527 total;5360 revisions/3167 retentions. Main unchanged;full goal active.')


if __name__ == '__main__':
    main()
