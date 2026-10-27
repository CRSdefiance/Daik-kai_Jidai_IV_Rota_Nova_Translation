"""Apply and independently verify the B169 reference-ready handoff without credit."""
import os
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B169_references_v4247 import ROOT as CHECKPOINT, DOC, APPROVAL
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4248')

if __name__ == '__main__':
    assert not ROOT.exists()
    workspace = Path.cwd().resolve()
    receipt = read(CHECKPOINT/'staged_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():
        assert sha(Path(path).read_bytes()) == digest,path
    plan = read(CHECKPOINT/'mutation_plan.json')
    for item in plan:
        target,staged = Path(item['target']),Path(item['planned'])
        assert target.is_relative_to(workspace) and staged.is_relative_to(CHECKPOINT.resolve())
        assert sha(target.read_bytes()) == item['before_sha256']
        assert sha(staged.read_bytes()) == item['planned_sha256']
        assert staged.stat().st_size >= target.stat().st_size
    for item in plan:
        with Path(item['target']).open('r+b') as stream:
            stream.write(Path(item['planned']).read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(Path(item['target']).read_bytes()) == item['planned_sha256']
    lp = Path('translations/editorial_review_current_v1.json')
    ledger,before = read(lp),read(CHECKPOINT/(lp.name+'.before'))
    allowed = {'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
               'unfinished_editorial_scope_v4247','lil_B169_reference_reconciliation_v4247','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in allowed} == {k:v for k,v in ledger.items() if k not in allowed}
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    fresh,old = ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    for key in ['record_keys','record_IDs','integrated_record_keys','pending_record_keys']:
        assert fresh[key] == old[key]
    assert len({historical_key(r) for r in fresh['record_keys']}) == 5692
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5692,5656,36)
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed']) == (5695,5656,3595,2061)
    approval,doc = read(APPROVAL),read(DOC)
    assert approval['manuscripts'] == {str(DOC):sha(DOC.read_bytes())}
    mapping = read(doc['reference_map'])
    block = mapping['blocks'][0]
    assert block['block'] == 169 and len(block['text_records']) == 36
    assert len(block['command_map']) == 53 and len(block['relative_skip_fixups']) == 12 and len(block['target_native_skip_cases']) == 60
    assert block['original_declared_end_word_maps'] == [dict(source_offset=2558,target_offset=2584,extent=4,source_four_zero_bytes_exact=True)]
    assert mapping['source_effect_operand_hex_values'] == ['0029','0001'] and mapping['source_effect_operand_decimal_values'] == [41,1]
    amendment = Path(doc['source_effect_operand_notation_amendment'])
    assert sha(amendment.read_bytes()) == doc['source_effect_operand_notation_amendment_sha256']
    assert read(amendment)['source_command_hex'] == '00a0ffff29000100'
    images = [NdsImage.open(p) for p in ['work/clean.nds',doc['current_ROM'],'out/lil_B169_reference_v4236_RESEARCH_ONLY.nds']]
    blocks = [IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[169] for im in images]
    assert blocks[0][2550:2558] == blocks[1][2550:2558] == bytes.fromhex('00a0ffff29000100')
    effect = next(c for c in block['command_map'] if c['word']==0xA000)
    assert blocks[2][effect['new_offset']:effect['new_offset']+8].hex() == '00a0ffff29000100'
    refs = {r['id']:r for r in block['text_records']}
    for row in doc['records']:
        assert all(row['review'].values()) and row['full_clean_context_precedes_comparison']
        for data,at,value in [(blocks[0],row['source_reference']['offset'],row['source_hex']),
                              (blocks[1],row['current_reference']['offset'],row['current_hex']),
                              (blocks[2],refs[row['id']]['new_offset'],refs[row['id']]['target_hex'])]:
            raw = bytes.fromhex(value)
            assert data[at:at+len(raw)] == raw and data[at+len(raw)] == 0
            assert data[at-5:at+1].hex() == row['source_complete_preamble_hex']
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1] == row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    actual = read('work/analysis/lil_B169_actual_v4244/actual_progressive_three_predicates_full_effect_and_return.json')
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 33
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['offline_only_display_IDs'] == ['DK4_MES_B169_R0067','DK4_MES_B169_R0082','DK4_MES_B169_R0097']
    assert all((row['id'] in approval['actual_sampled_display_IDs']) == row['actual_B22_display_fixture_observed'] for row in doc['records'])
    visual = read('work/analysis/lil_B169_transition_review_v4245/all6_sheets_source_effect_and_paired_return_review.json')
    assert len(visual['all6_actual_sheets_viewed']) == 6 and len(visual['English_full_screen_views']) == 3 and len(visual['Japanese_full_screen_views']) == 2
    for view in visual['all6_actual_sheets_viewed']+visual['English_full_screen_views']+visual['Japanese_full_screen_views']:
        assert sha(Path(view['path']).read_bytes()) == view['sha256']
    assert len(visual['paired_source_English_whole_RGB_returns']) == 1
    stored = read(doc['final_padding_proof'])
    assert stored['current_final_stored_macro_alignment_cases'] == 144
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases']) == (100,44)
    promoted = read('translations/promoted_build.json')
    assert promoted['profile'] == 'all-routes-unified-v4204' and sha(Path(promoted['rom']).read_bytes()) == promoted['rom_sha256']
    pins_path = Path('translations/rom_retention_pins.json')
    pins,old_pins = read(pins_path),read(CHECKPOINT/(pins_path.name+'.before'))
    assert pins[:-3] == old_pins
    for pin in pins[-3:]:
        assert sha(Path(pin['path']).read_bytes()) in pin['reason']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4247')
    for case in ['clean_Japanese','reviewed_English']:
        assert read('work/analysis/lil_B169_display_run_v4242_'+case+'/terminal.json')['terminal']
    ROOT.mkdir(parents=True)
    result = dict(checkpoint='V4247',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5692,integrated=5656,pending=36,
        source_prose=5695,revised=3595,retained=2061,new_source_prose_reviews=0,new_completed_records=0,
        all_prior_completions_and_promoted_V4204_preserved=True,all36_exact_clean_current_target_references_and17_retentions_verified=True,
        all53_commands12_spans60_skips_and144_stored_cases_bound=True,source_A000_hex0029_0001_decimal41_1_notation_correction_bound=True,
        actual_two_B22_content_boots33_complete_planes_source_effect_and_normal_return_verified=True,
        three_conditional_remarks_explicitly_offline_only=True,all6_actual_sheets3_English_and2_Japanese_fullscreens_viewed=True,
        new_emulator_runs=2,ROMs_pinned=3,ROMs_deleted=0,registered_integration_startup_and_completion_still_pending=True,
        current_candidate=promoted['rom'],candidate_sha256=promoted['rom_sha256'],manifest_batches=544,accepted_layers=114,
        remaining_B170_B180_physical_speeches=231,all_jobs_terminal=True,full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'verified_handoff.json',result)
    save(CHECKPOINT/'checkpoint_receipt.json',{**receipt,'ledger_sha256':result['ledger_sha256'],
        'updated_files':{str(Path(r['target']).relative_to(workspace)):r['planned_sha256'] for r in plan}})
    print('V4247 independently verified:5692/5656/36;5695 source/prose. Complete B169 source/native/reference/representative approval;registered integration pending. Main V4204 unchanged;full goal active.')
