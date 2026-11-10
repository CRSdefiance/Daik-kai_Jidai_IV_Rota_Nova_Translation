"""Prepare exact B203 relocation/reference checks from verified V6032."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B203_reference_tools_v6034')
PARENT=Path('out/all_routes_combined_v5998_candidate.nds')
ROM=Path('out/lil_B203_reference_v6037_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B203_relocation_v6035/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v6033/verified_handoff.json')
    assert prior['B203_native_approved_uncredited_objects']==22 and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256'] and sha(PARENT.read_bytes())==prior['candidate_sha256']
    registry=read('translations/release_stack.json');profile=registry['profiles'][prior['profile']]
    assert profile['status']=='experimental' and profile['lil_B202_editorial']=='translations/lil_B202_editorial_release_v4.json' and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    tools=[derive('scripts/research_lil_B202_relocation_v5983.py','scripts/research_lil_B203_relocation_v6035.py',{
        'B202':'B203','relocation_v5983':'relocation_v6035','v5947_candidate':'v5998_candidate','number==202':'number==203',
        "end_maps[0]['source_offset']==582":"end_maps[0]['source_offset']==810",'==19':'==22',
        "sum(len(r['command_map']) for r in results)==26":"sum(len(r['command_map']) for r in results)==31",
        '[202]':'[203]','source_FE_system_objects=0':'source_FE_system_objects=1','all19speech':'all22speech','26commands/19speech':'31commands/22speech','all588':'all816',
    })]
    tools.append(derive('scripts/prove_lil_B202_stored_v5984.py','scripts/prove_lil_B203_stored_v6036.py',{
        'B202':'B203','stored_v5984':'stored_v6036','relocation_v5983':'relocation_v6035','voices_v5960':'voices_v6011',
        '[2,18,147,157]':'[2,76,170,254]',"sum(c['consumer']=='FE-paper' for c in cases)==0":"sum(c['consumer']=='FE-paper' for c in cases)==1",
        'len(cases)==19':'len(cases)==22','fresh+reused==76':'fresh+reused==88','all19':'all22','targets76':'targets88',
        'current_final_stored_macro_alignment_cases=76':'current_final_stored_macro_alignment_cases=88',
        'stored_targets=19,progressive=19,FE=0,macro_cases=76':'stored_targets=22,progressive=21,FE=1,macro_cases=88',
        'actual_English_B202_inn_picture_gift_stat_and_end_reachability_unexecuted':'actual_English_B203_book_picture_negotiation_stat_and_end_reachability_unexecuted',
    }))
    shared={'B202':'B203','prepare_lil_B202_references_v5982':'prepare_lil_B203_references_v6034'}
    tools.append(derive('scripts/create_lil_B202_reference_v5985.py','scripts/create_lil_B203_reference_v6037.py',{
        **shared,'V5947':'V5998','research_v5985':'research_v6037','stored_v5984':'stored_v6036','verification_v5981':'verification_v6033',
        'all19':'all22','targets76':'targets88',"['current_final_stored_macro_alignment_cases']==76":"['current_final_stored_macro_alignment_cases']==88",'current_final_stored_macro_alignment_cases=76':'current_final_stored_macro_alignment_cases=88','==[202]':'==[203]',
    }))
    tools.append(derive('scripts/verify_lil_B202_loader_v5986.py','scripts/verify_lil_B203_loader_v6038.py',{
        **shared,'V5947':'V5998','loader_v5986':'loader_v6038','research_v5985':'research_v6037',
        'work/analysis/lil_B201_loader_v5935/whole_SC2_and_B201_initial_entry_proof.json':'work/analysis/lil_B202_loader_v5986/whole_SC2_and_B202_initial_entry_proof.json',
    }))
    tools.append(derive('scripts/verify_lil_B202_references_v5987.py','scripts/verify_lil_B203_references_v6039.py',{
        **shared,'reference_census_v5987':'reference_census_v6039','loader_v5986':'loader_v6038','[202]':'[203]',
        '26-command':'31-command',"sum(len(r['mapped_commands'])for r in result)==26":"sum(len(r['mapped_commands'])for r in result)==31",'all26':'all31','native_commands_each=26':'native_commands_each=31',
    }))
    tools.append(derive('scripts/prove_lil_B202_ends_v5988.py','scripts/prove_lil_B203_ends_v6040.py',{
        **shared,'ends_v5988':'ends_v6040','n==202':'n==203',
    }))
    tools.append(derive('scripts/prove_lil_B202_relocated_controls_v5989.py','scripts/prove_lil_B203_relocated_controls_v6041.py',{
        **shared,'relocated_controls_v5989':'relocated_controls_v6041','blocks[202]':'blocks[203]',
        'all7_source_current_nonspeech_leaves':'all9_source_current_nonspeech_leaves','[0x4835,0x4721]':'[0x4820,0x4735]','word==0x4835':'word==0x4820',
        "expected,match=env['expanded_current_body'](value[1:]);assert match is None":"expected,match=env['expanded_current_body'](value[1:]);assert match is None;expected=expected.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')",
        "assert not any(m in value[1:] for m in [b'FI',b'FA',b'FO'])":"assert all(bytes.fromhex(rows[r['id']]['source_hex'])[1:].count(m)==value[1:].count(m) for m in [b'FI',b'FA',b'FO'])",
        'len(dispatches)==19':'len(dispatches)==22',"sum(r['resolved_actor_ID'] is None for r in dispatches)==0":"sum(r['resolved_actor_ID'] is None for r in dispatches)==1",'len(leaves)==7':'len(leaves)==9',
        "sum(r['word']==0xA000 for r in leaves)==2":"sum(r['word']==0xA000 for r in leaves)==4",
        "assert len(cp['ten_distinct_632A_decoder_boundary_cases'])==10 and cp['original632A_word_two_exact_source_sites']==[162,182] and len(cp['source_two_A000_structural_pairs'])==2":"assert len(cp['one_resource632E_ten_boundary_cases'])==10 and len(cp['source6003_ten_boundary_cases'])==10 and len(cp['source_four_A000_structural_pairs'])==4",
        'all19_dispatches_one_picture_one47xx_pair_and7_exact_leaves':'all22_dispatches_one_picture_one47xx_pair_and9_exact_leaves',
        'all7_source_current_target_control_leaves':'all9_source_current_target_control_leaves',
        'original10_unique632A_boundary_cases_two_word_sites_and_two_structural_pairs_reused_by_exact_bytes_and_current_snapshot':'original10_resource632E10_6003_boundary_cases_and_four_A000_pairs_reused_by_exact_bytes_and_current_snapshot',
        'all19_progressive_and_zero_FE_objects_preserved=True,no_FI_FA_FO_inherited=True':'all21_progressive_and_one_FE_object_preserved=True,one_original_FI_zero_FA_FO_preserved=True',
        'original_names_and_Sailor_catalogue_alias_preserved':'original_names_and_Mikhail_progressive_catalogue_distinction_preserved',
        'Bind19 relocated B202 dispatches and all twelve source-owned control leaves.':'Bind22 relocated B203 dispatches and all nine source-owned control leaves.',
        '19 relocated dispatches,one picture/one47xx pair and7 exact leaves pass;no macros/2000 pause. English scene next.':'22 relocated dispatches,one picture/one47xx pair and9 exact leaves pass;one FE/FI,no2000 pause. English scene next.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),source_commands=31,source_speeches=22,source_relative_sites=0,source_tailzeros=2,source_FE_panels=1,previous_goal_turn_classification='progress',full_goal_complete=False))
    print('B203 seven reference tools prepared;31 commands/22 objects/nine leaves/end810. Parent loader reused only by exact complete ROM hash.')
