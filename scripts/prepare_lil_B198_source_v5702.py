"""Prepare exact current mapping and original consumers for the clean Namahage scene."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B198_source_tools_v5702')
SOURCE='work/analysis/lil_B198_source_v5702/all17_clean_current_complete_context.json'
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B195_source_v5541.py','scripts/map_lil_B198_source_v5702.py',{
        'B195':'B198','source_v5541':'source_v5702','verification_v5537':'verification_v5698',
        'work/analysis/lil_B195_clean_context_v5540/all20_clean_exchange_and_fresh_glosses.json':'work/analysis/lil_B198_clean_context_v5701/all17_clean_exchange_fresh_glosses_and_Namahage_scope.json',
        'len(known)==6135':'len(known)==6215','blocks[195]':'blocks[198]','block=195':'block=198',
        'len(old)==23 and len(spoken)==20':'len(old)==37 and len(spoken)==17',
        '[92,103,119,254]':'[12,15,254]','[92,103,119]':'[12,15]',
        '==[0xA000,0xC200,0]':'==[0x6000,0x4500,0x633F,0xA000,0x623F,0x4621,0x61FF,0x8000,0x4835,0x8000,0xA000,0]',
        'lil_B194_runs_v5533':'lil_B197_runs_v5694','physical_speeches=20':'physical_speeches=17','FE_panels=1,relative_sites=0':'FE_panels=6,relative_sites=8',
        'all20':'all17','total_editorial_objects=20,speech_objects=20,ordinary_source_speeches=19,system_FE_panels=1':'total_editorial_objects=17,speech_objects=17,ordinary_source_speeches=11,system_FE_panels=6',
        'source_native_commands=23':'source_native_commands=37','source_A000=1,source_C200=1,source_relative_sites=0,source_predicates=0':'source_A000=2,source_C200=0,source_relative_sites=8,source_predicates=2',
        'B195 bound:20 complete speeches,23 linear commands,A000/C200/end;three source actors and current V5531 opening snapshot. No credit.':
        'B198 bound:17 complete speeches,six unattributed speaking FE/11 progressive,37 commands/eight relative sites/two predicates;two source actors and actual V5692 opening snapshot.No old-English speech comparison or credit.'})]
    shared={'B197':'B198','source_v5647':'source_v5702','all24_clean_current_complete_context_with_three_choice_labels':'all17_clean_current_complete_context'}
    rows.append(derive('scripts/reconcile_lil_B197_voices_v5648.py','scripts/reconcile_lil_B198_voices_v5703.py',{
        **shared,'voices_v5648':'voices_v5703','[21,169]':'[12,15]','V5637':'V5692'}))
    rows.append(derive('scripts/prove_lil_B197_dispatches_v5649.py','scripts/prove_lil_B198_dispatches_v5704.py',{
        **shared,'dispatches_v5649':'dispatches_v5704','voices_v5648':'voices_v5703',
        'Bind42 source/current speech calls and11 exact':'Bind34 source/current speech calls and12 exact',
        'len(cases)==42':'len(cases)==34','len(leaves)==11':'len(leaves)==12',
        "sum(c['source_selector']==254 for c in cases)==2":"sum(c['source_selector']==254 for c in cases)==12",
        'all21_source_current_dispatches_no_macros_and11_control_leaves':'all17_source_current_dispatches_no_macros_and12_control_leaves',
        'all11_nonrelative':'all12_nonrelative','one_FE_source_object_use_original_null_actor_path':'six_FE_spoken_voice_objects_use_original_null_actor_path',
        '42 source/current dispatches':'34 source/current dispatches','one FE/null-actor object':'six speaking FE/null-actor objects','All11':'All12'}))
    rows.append(derive('scripts/prove_lil_B197_entry_v5650.py','scripts/prove_lil_B198_entry_v5705.py',{
        **shared,'entry_v5650':'entry_v5705','voices_v5648':'voices_v5703','[197]':'[198]'}))
    rows.append(derive('scripts/prove_lil_B197_branches_v5651.py','scripts/prove_lil_B198_branches_v5706.py',{
        **shared,'branches_v5651':'branches_v5706','len(edges)==6':'len(edges)==8','len(cases)==60':'len(cases)==80'}))
    rows.append(derive('scripts/prove_lil_B197_names_v5652.py','scripts/prove_lil_B198_names_v5707.py',{
        **shared,'names_v5652':'names_v5707','voices_v5648':'voices_v5703','[21,169]':'[12,15]'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_mapping_and_native_consumers.json',dict(tools=rows,
        source_speeches=17,progressive=11,unattributed_spoken_FE=6,static_selectors=[12,15],macros=0,
        commands=37,relative_sites=8,predicates=2,nonrelative_nonspeech_leaves=12,choices=0,
        source_transition_words_and_picture_resource_predicate_semantics_still_pending=True,
        no_prior_English_speech_comparison_ROM_or_credit_change=True,full_goal_complete=False))
