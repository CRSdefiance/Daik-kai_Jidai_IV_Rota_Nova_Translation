"""Independent pending7 ledger/source/native/gate and unchanged release audit."""
from pathlib import Path
from collections import Counter
from PIL import Image
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v2661')
CHECKPOINT = Path('work/analysis/admiral_shot_checkpoint_v2660')
IDS = set(range(1924,1931))

if __name__ == '__main__':
    assert not ROOT.exists()
    receiptpath = CHECKPOINT/'checkpoint_receipt.json'; receipt = read(receiptpath)
    lp = Path('translations/editorial_review_current_v1.json'); ledger = read(lp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items(): assert sha(Path(p).read_bytes()) == digest, (group,p)
    before = read(CHECKPOINT/'editorial_review_current_v1.json.before')
    prior_audit = read(receipt['prior_ledger_audit'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes()) == prior_audit['ledger_sha256'] == receipt['prior_ledger_sha256']
    prior_receipt = read(prior_audit['handoff_receipt'])
    for p,digest in prior_receipt['updated_files'].items():
        backup = CHECKPOINT/(Path(p).name+'.before')
        assert sha((backup if backup.exists() else Path(p)).read_bytes()) == digest, p
    f = ledger['contextual_story_natural_dialogue_pass_v1871']
    keys = {(r['file_path'],r['id']) for r in f['record_keys']}
    integrated = {(r['file_path'],r['id']) for r in f['integrated_record_keys']}
    pending = {(r['file_path'],r['id']) for r in f['pending_record_keys']}
    historical = {historical_key(r) for family in ledger['completed_editorial_families'] for r in family['records']}
    expected = {('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') for n in IDS}
    oldkeys = {(r['file_path'],r['id']) for r in before['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(keys) == len(f['record_keys']) == len(f['record_IDs']) == 2150
    assert integrated == historical == oldkeys and len(integrated) == 2143
    assert pending == expected == keys-integrated and not pending & integrated
    assert (f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release']) == (2150,2143,7)
    assert Counter(p for p,n in keys) == {'/COMMON/MESFILE.DK4':1493,'/data/SC2.DK4':429,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert f['historical_completed_records_outside_reconciled_fresh_pass'] == 0 and f['all_historical_completions_freshly_reconciled']
    assert len(f['pending_contextual_families']) == 1 and f['pending_contextual_families'][0]['records'] == 7
    for field in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
                  'retained_wordings_editorially_completed','source_prose_reviewed_counts_by_file',
                  'reviewed_but_incomplete_COMMON_IDs','current_integrated_candidate']:
        assert ledger[field] == before[field], field
    assert ledger['records_editorially_completed'] == 2143 and ledger['records_revised_and_integrated'] == 1498
    assert ledger['retained_wordings_editorially_completed'] == 645 and sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 2259
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs']) == 116 and IDS <= set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    docpath = Path(f['latest_contextual_manuscript']); doc = read(docpath)
    validate_natural_dialogue_batch(doc)
    assert doc['distinct_post_shot_transition_pending'] and doc['all_seven_native_previews_viewed'] and not doc['formatting_review_pending']
    assert doc['completion_credit_added'] == 0 and doc['revised_IDs'] == [] and doc['retained_count'] == 7
    fontpath = Path(doc['current_native_font_proof']); gatepath = Path(doc['focused_original_gate_proof'])
    font,gate = read(fontpath),read(gatepath)
    assert sha(fontpath.read_bytes()) == doc['current_native_font_proof_sha256']
    assert sha(gatepath.read_bytes()) == doc['focused_original_gate_proof_sha256']
    image = NdsImage.open(doc['current_ROM']); clean = NdsImage.open('work/clean.nds')
    arm,common = image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    en = current_entries(common,arm); jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    def ref(r):
        return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),
            record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for row in doc['records']:
        n = row['message_id']; assert n in IDS and all(row['review'].values())
        assert row['editorial_decision'] == 'retain-wording' and row['source_meaning'] and row['localization_note'] and row['fresh_retained_wording_justification']
        assert row['source_hex'] == jp[n].text.hex() and row['source_Japanese'] == jp[n].text.decode('cp932')
        assert row['source_reference'] == ref(jp[n]) and row['current_reference'] == ref(en[n])
        assert compiled(row) == en[n].text == bytes.fromhex(row['current_hex'])
        assert row['native_argument_count'] == 0 and row['source_family'] == 'admiral_shot' and not row['new_current_visit']
    assert len(font['cases']) == 7 and {c['message_ID'] for c in font['cases']} == IDS
    for c in font['cases']:
        p = Path(c['preview']); assert sha(p.read_bytes()) == c['preview_sha256'] and Image.open(p).size == (228,64)
        assert c['complete_current_native_and_independent_plane_equal'] and c['current_font_mask_equals_historical_reference']
        assert 1 <= len(c['lines']) <= 4 and all(0 < len(line) <= 35 for line in c['lines'])
        assert c['compiled_hex'] == en[c['message_ID']].text.hex()
    pipelines = font['all8_original_role7_speech_pipelines']
    assert len(pipelines) == 8 and {c['source_voice'] for c in pipelines} == set(range(8))
    for p in pipelines:
        n = p['message_ID']; pipeline = p['native_pipeline']
        assert pipeline['input_hex'] == pipeline['loaded_template_hex'] == en[n].text.hex()
        assert pipeline['formatted_hex'] == next(c['formatted_hex'] for c in font['cases'] if c['message_ID'] == n)
        if p['source_voice'] == 1:
            assert p['original_actor_choice']['actor_ID'] == 16 and p['original_actor_choice']['original_minus1_fallback']
            assert p['CPU_only_voice_fixture']['no_roster_fixture'] and p['CPU_only_voice_fixture']['physical_Lookout_remains_unassigned']
        else:
            assert len(p['CPU_only_voice_fixture']['one_roster_byte_changed']) == 1
            assert p['CPU_only_voice_fixture']['all_actor_objects_skills_RNG_and_other4MiB_bytes_exact']
    assert len(font['all14_cold_warm_copies']) == len(font['invalid_compiler_inputs_rejected']) == 14
    assert font['findings'] == [] and font['all_executed_pipeline_instructions_current_ROM_byte_exact'] and font['all_original_actor_models_unchanged']
    assert font['blank_space_glyph_zero_ink'] and len(gate['exclusion_cases']) == len(gate['threshold_cases']) == 3
    assert len(gate['post_RNG_arithmetic_cases']) == 20 and gate['no_new_actual_event_or_current_emulator_run']
    for c in [*gate['exclusion_cases'],*gate['threshold_cases'],*gate['post_RNG_arithmetic_cases']]:
        assert c['all_main4MiB_bytes_unchanged'] and c['no_RNG_effect_speech_or_outcome_called'] and c['all_executed_instructions_current_exact']
    for c in gate['post_RNG_arithmetic_cases']:
        assert c['accepted_comparison'] == (c['draw_value'] <= c['computed_role_metric']//10)
        assert c['not_original_chance_draw_or_gameplay_eligibility']
    manifestpath = Path(doc['current_ROM']).with_suffix('.manifest.json'); manifest = read(manifestpath)
    stage = manifest['relocations']['/COMMON/MESFILE.DK4']['reinforcement_sniping_editorial']
    cp = Path(stage['release_config']); config = read(cp); mp = Path(config['manuscript'])
    assert sha(cp.read_bytes()) == stage['release_config_sha256'] and sha(mp.read_bytes()) == config['manuscript_sha256']
    assert IDS <= set(stage['proof']['reviewed_native_IDs'])
    registered = {r['message_id']:r for r in read(mp)['records']}
    assert all(registered[n]['english'] == next(r['english'] for r in doc['records'] if r['message_id'] == n) for n in IDS)
    releasepath = Path('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json'); release = read(releasepath)
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256'] == receipt['candidate_sha256'] == release['candidate_sha256']
    assert sha(arm) == release['ARM9_sha256'] and sha(common) == release['COMMON_sha256']
    assert sha(manifestpath.read_bytes()) == release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256'] == receipt['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and sha(Path('work/clean.nds').read_bytes()) == release['clean_input_sha256']
    assert sha(Path(manifest['base_rom']).read_bytes()) == manifest['base_sha256']
    registry = read('translations/release_stack.json')
    assert sha(Path('translations/release_stack.json').read_bytes()) == manifest['release_stack_sha256']
    assert len(manifest['batches']) == 493 and len(registry['accepted_layers']) == 114 and registry['latest_promoted_build']['profile'] == 'all-routes-unified-v1492'
    handoff = Path('docs/editorial_handoff_current.md').read_text()
    assert handoff.startswith('# Current editorial handoff - V2660') and '2150 reread /2143 integrated-reconciled /7pending' in handoff
    assert 'post-shot outcome transition remain pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V2660',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        fresh_records=2150,fresh_integrated=2143,fresh_pending=7,new_completed_records=0,new_revisions=0,
        historical_completed=2143,source_prose=2259,incomplete_COMMON=116,
        pending7_exact_clean_current_registered_owner_native_fonts_voices_and_gate_scopes_verified=True,
        historical_set_equal_integrated_keys_and_pending7_disjoint=True,
        prior_ledger_and_updated_file_backup_chain_verified=True,
        handoff_receipt=str(receiptpath),handoff_receipt_sha256=sha(receiptpath.read_bytes()),
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        no_ROM_registry_profile_manifest_or_patch_change=True,prior_clean_input_reconstruction_proof_still_bound=True,
        distinct_post_shot_runtime_transition_pending=True,new_emulator_runs=0,all_jobs_terminal=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V2660 audit passes:2150reread/2143reconciled/7pending;exact source/native/owner and evidence scopes verified;ROM/patch unchanged.')
