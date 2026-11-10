"""Credit 435 reviewed objects once after the complete registered release passes."""
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

ROOT = Path('work/analysis/Hodram_B171_B190_release_verified_20261104')
LEDGER = Path('translations/editorial_review_current_v1.json')
FINAL = Path('translations/hodram_B171_B190_contextual_final_review_v1.json')
RELEASE = ROOT / 'registered_release_verification.json'
STARTUP = ROOT / 'own_registered_startup_verification.json'
ACTUAL = Path('work/analysis/Hodram_B171_B190_checked_20261104/actual_review.json')
PIXELS = Path('work/analysis/Hodram_B171_B190_actual_pixels_v2_20261104/focused_actual_pixels.json')
FAMILY = 'Hodram_SC1B171_B190_complete_contextual_release_20261104'
KEY = 'Hodram_B171_B190_clean_next_20261102'


if __name__ == '__main__':
    assert not (ROOT / 'completion_checkpoint.json').exists()
    doc, release, startup, actual, pixels = map(load, [FINAL, RELEASE, STARTUP, ACTUAL, PIXELS])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(STARTUP.read_bytes()) == release['own_registered_startup_sha256']
    assert release['candidate_sha256'] == startup['candidate_sha256'] == sha(Path(release['candidate']).read_bytes())
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes() == Path(release['candidate']).read_bytes()
    manifest = load(release['manifest'])
    assert all(manifest['checks'].values()) and release['accepted_layers'] == 114
    assert release['complete_stack_entries'] == 663 and release['all_six_registered_final_stages_preserved']
    assert (len(doc['records']), doc['proposed_revisions'], doc['wording_retentions']) == (435, 195, 240)
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert actual['focused_actual_pixels_sha256'] == sha(PIXELS.read_bytes())
    assert pixels['all_required_distinct_display_cases_match'] and actual['all_review_sheets_directly_viewed']
    assert pixels['full_pirate30_andtown130_native_body_sequence_matches_copied_source_commands']
    intervals = dict(sail=(2816, 10247), pirate=(2817, 11208), town=(2816, 35209), refusal=(2816, 5686))
    assert len(pixels['body_pages']) == 413 and all(intervals[s['run']][0] <= s['frame'] < intervals[s['run']][1] for s in pixels['body_pages'])
    image = NdsImage.open(release['candidate'])
    archive = image.read_file(doc['file_path'])
    blocks = IlnkContainer.parse(archive).blocks
    bindings = []
    for row in doc['records']:
        assert all(row['review'][g] is True for g in doc['review_gates'])
        reference = deepcopy(row['planned_integrated_reference'])
        raw = bytes.fromhex(reference.pop('exact_stored_hex'))
        at, block = reference['offset'], blocks[row['block']]
        assert block[at:at + len(raw) + 1] == raw + b'\0'
        assert sha(archive) == reference['target_archive_sha256'] and block[:at].count(b'\0') == reference['record_index']
        if row['kind'] == 'typed-choice-label':
            command, index = reference['command_offset'], row['source_index']
            assert row['source_count'] == 2 and int.from_bytes(block[command:command + 2], 'little') == 0x2100
            offset = int.from_bytes(block[command + 2 + 2 * index:command + 4 + 2 * index], 'little')
            assert command + 6 + offset == at and row['block'] == 171
            samples = [dict(**s, source_index=index) for s in pixels['menu_samples']]
            equivalent = []
        else:
            assert block[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
            samples, equivalent = [], []
            for sample in pixels['body_pages']:
                ordered = sample['ordered_fixture_record_id']
                candidates = sample['native_equivalent_candidates']
                if ordered == row['id'] or (ordered is None and len(candidates) == 1 and candidates[0]['id'] == row['id']):
                    samples.append(sample)
                elif ordered is None and sample['ambiguous_occurrence'] and any(c['id'] == row['id'] for c in candidates):
                    equivalent.append(sample)
        bindings.append(dict(id=row['id'], file_path=row['file_path'], kind=row['kind'],
            source_reference=row['source_reference'], source_hex=row['source_hex'],
            current_reference=row['current_reference'], current_hex=row['current_hex'],
            registered_reference=reference, registered_stored_hex=raw.hex(), registered_ROM_sha256=release['candidate_sha256'],
            decision=row['decision'], finding=row['finding'], localization_note=row['localization_note'],
            retention_reason=row['retention_reason'], review=row['review'], actual_source_orunique_plane_bound_samples=samples,
            ambiguous_plane_equivalences_not_individual_occurrence_proof=equivalent,
            offline_complete_display_andrepresentative_gameplay_distinguished=True))
    binding_path = ROOT / 'integrated_record_bindings.json'
    assert not binding_path.exists()
    before = LEDGER.read_bytes()
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 9498 and not prior['full_goal_complete']
    assert prior['current_integrated_candidate']['sha256'] == release['parent_sha256']
    assert not any(r['id'] == FAMILY for r in prior['coverage_units'])
    context = deepcopy(prior['contextual_story_natural_dialogue_pass_v1871'])
    keys = [dict(file_path=r['file_path'], id=r['id']) for r in doc['records']]
    existing = {(r['file_path'], r['id']) for r in context['record_keys']}
    assert len(existing) == len(context['integrated_record_keys']) == 9498
    assert not existing & {(r['file_path'], r['id']) for r in keys}
    scope = dict(initialized_fixture_runs=5, fixture_frames=85005, own_registered_startup_frames=4001,
        captured_body_planes_matched=413, native_record_page_observations=188, actual_name_headers=27,
        complete_menu_highlights=2, reviewed_actual_sheets=8,
        actual_review=str(ACTUAL), actual_review_sha256=sha(ACTUAL.read_bytes()),
        unvisited_andfixture_limits=actual['unvisited'], ordered_town130_andpirate30_source_calls=True,
        duplicate_pixels_alone_not_exact_occurrence=True, natural_activation=False, hardware=False, guide_photos=False)
    family = dict(id=FAMILY, file_path=doc['file_path'], blocks=doc['blocks'], record_IDs=[r['id'] for r in doc['records']],
        records=435, ordinary_speeches=433, personality_alternatives=0, typed_choices=2, typed_choice_commands=1,
        final_review=str(FINAL), revised_count=195, retained_count=240, fresh_revisions=195, fresh_retentions=240,
        layout_findings_resolved=15, scoped_name_term_decisions=49, native_name_strings=31,
        actual_verification_scope=scope, integrated_record_bindings=str(binding_path))
    ledger = dict(prior)
    ledger['completed_editorial_families'] = [*prior['completed_editorial_families'], family]
    ledger['coverage_units'] = [*prior['coverage_units'], dict(**family,
        status='complete-contextual-native-stored-representative-registered-release', completion_credit_added=435,
        final_review_sha256=sha(FINAL.read_bytes()), release_verification=str(RELEASE),
        release_verification_sha256=sha(RELEASE.read_bytes()), full_goal_complete=False)]
    for key, amount in [('records_editorially_completed', 435), ('records_revised_and_integrated', 195),
        ('retained_wordings_editorially_completed', 240), ('records_with_source_and_prose_pass', 435), ('records_with_source_prose_drafts', 435)]:
        ledger[key] += amount
    context['record_keys'].extend(keys)
    context['integrated_record_keys'].extend(keys)
    context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread'] += 435
    context['fresh_pass_records_integrated'] += 435
    context['latest_completed_family'], context['latest_final_review'] = FAMILY, str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY, records=435, ordinary_speeches=433, personality_alternatives=0,
        typed_choices=2, final_review=str(FINAL), new_revisions=195, justified_retentions=240,
        new_completed_records=435, historical_reconciliation_only=False, actual_optional_event_selected=False, actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871'] = context
    entry = deepcopy(prior[KEY])
    entry.update(completion_credit_added=435, new_credit=435, registered_release_pending=False,
        formatting_visual_stored_gameplay_andregistered_release_pending=False,
        stored_reconstruction_gameplay_andregistered_release_pending=False, representative_gameplay_andregistered_release_pending=False,
        native_identity_andterms_still_pending=False, remaining_current_English_comparisons=0,
        all435_source_current_final_refs_andfive_gates=str(binding_path),
        registered_build=dict(session=42463, started=True, terminal=True, exit_code=0), no_live_job=True,
        registered_release_verification=str(RELEASE), registered_release_verification_sha256=sha(RELEASE.read_bytes()),
        own_registered_startup=str(STARTUP), own_registered_startup_sha256=sha(STARTUP.read_bytes()),
        source_intake_flags_are_historical_current_status_supersedes=True, main_unchanged=True)
    ledger[KEY] = entry
    ledger['current_integrated_candidate'] = dict(path=release['candidate'], sha256=release['candidate_sha256'], profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')), ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        patch=release['patch'], patch_sha256=release['patch_sha256'], manifest=release['manifest'], manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE), experimental_not_promoted=True,
        own_registered_startup_verified=True, clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint'] = 'Registered B171–B190 verified and credited once: 435 reviews, 195 revisions and 240 retentions; 9933 complete. All 439 pages and 15 layout fixes pass. Exact clean patch and own startup pass. Full scope/main/ROMs preserved; next clean B191–B210 meanings saved; no guide photos.'
    counts = Counter(r['file_path'] for r in context['record_keys'])
    assert counts['/data/SC1.DK4'] == 2853
    assert len(context['record_keys']) == len(context['integrated_record_keys']) == ledger['records_editorially_completed'] == 9933
    assert (ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (6004, 3929)
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 9936
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
    temporary = LEDGER.with_name('editorial_review_current_v1.pending_B171_B190_completion.json')
    assert not temporary.exists() and LEDGER.read_bytes() == before
    temporary.write_bytes(staged)
    os.replace(temporary, LEDGER)
    assert sha(LEDGER.read_bytes()) == sha(staged)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path in Path('work/analysis/Hodram_B171_B190_registered_build_20261104').rglob('*.nds'):
        absolute = str(path.resolve())
        if not any(r['path'] == absolute for r in pins):
            pins.append(dict(path=absolute, reason='Preserve registered B171–B190 build stage; all ROMs retained. SHA256 ' + sha(path.read_bytes())))
    save(pins_path, pins)
    save(ROOT / 'completion_checkpoint.json', dict(family=FAMILY, new_credit=435,
        counts=dict(completed=9933, source_prose_anddrafts=9936, integrated_revisions=6004, retentions=3929),
        completed_by_file=dict(counts), candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
        release_verification=str(RELEASE), release_verification_sha256=sha(RELEASE.read_bytes()),
        own_startup=str(STARTUP), own_startup_sha256=sha(STARTUP.read_bytes()), ledger_sha256=sha(staged),
        prior_ledger_bytes_sha256=sha(before), all_prior_records_andunrelated_scope_preserved=True,
        all_generated_ROMs_andprior_work_preserved=True, main_unchanged=True, full_goal_complete=False, guide_photos=False))
    print('435 once-only completions: 9933 total; 6004 revisions/3929 retentions. Main unchanged; full goal active.')
