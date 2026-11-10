"""Bind B199's own31 speeches,one FI and16 exact control leaves to current V5756."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_source_tools_v5767')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B198':'B199','source_v5702':'source_v5767','all17_clean_current_complete_context':'all31_clean_current_complete_context'}
    rows=[derive('scripts/map_lil_B198_source_v5702.py','scripts/map_lil_B199_source_v5767.py',{
        **shared,'verification_v5698':'verification_v5762',
        'work/analysis/lil_B198_clean_context_v5701/all17_clean_exchange_fresh_glosses_and_Namahage_scope.json':
        'work/analysis/lil_B199_clean_context_v5765/all31_clean_portrait_chase_found_book_and_misunderstood_gift_glosses.json',
        'len(known)==6215':'len(known)==6232','blocks[198]':'blocks[199]','block=198':'block=199',
        'len(old)==37 and len(spoken)==17':'len(old)==47 and len(spoken)==31',
        "gloss['read_no_predecessor_English']":"gloss['prior_English_speech_unread']",
        '[12,15,254]':'[2,9,22,254]','[12,15]':'[2,9,22]',
        '[0x6000,0x4500,0x633F,0xA000,0x623F,0x4621,0x61FF,0x8000,0x4835,0x8000,0xA000,0]':
        '[0x4631,0x0505,0x2000,0x632D,0x4621,0x630B,0x632A,0x0503,0x4821,0x4735,0x632B,0x4630,0x4895,0xA000,0x4720,0]',
        'macros==dict(FI=0,FA=0,FO=0)':'macros==dict(FI=1,FA=0,FO=0)',
        'lil_B197_runs_v5694':'lil_B198_runs_v5758','physical_speeches=17':'physical_speeches=31',
        'FE_panels=6,relative_sites=8':'FE_panels=1,relative_sites=0',
        'total_editorial_objects=17,speech_objects=17,ordinary_source_speeches=11,system_FE_panels=6':
        'total_editorial_objects=31,speech_objects=31,ordinary_source_speeches=30,system_FE_panels=1',
        'source_native_commands=37':'source_native_commands=47',
        'source_A000=2,source_C200=0,source_relative_sites=8,source_predicates=2':'source_A000=1,source_C200=0,source_relative_sites=0,source_predicates=0',
        'all17_clean_first':'all31_clean_first',
        'B198 bound:17 complete speeches,six unattributed speaking FE/11 progressive,37 commands/eight relative sites/two predicates;two source actors and actual V5692 opening snapshot.No old-English speech comparison or credit.':
        'B199 bound:31 speeches/one sound-effect FE/30 progressive,47 commands/one FI/one2000 pause;three source actors and actual V5756 opening snapshot.No old-English speech comparison or credit.'})]
    rows.append(derive('scripts/reconcile_lil_B198_voices_v5703.py','scripts/reconcile_lil_B199_voices_v5768.py',{
        **shared,'voices_v5703':'voices_v5768','[12,15]':'[2,9,22]','len(fresh)==2':'len(fresh)==3',
        'fresh2_actor_names':'fresh3_actor_names','two_source_selectors':'three_source_selectors','V5692':'V5756'}))
    rows.append(derive('scripts/prove_lil_B198_dispatches_v5704.py','scripts/prove_lil_B199_dispatches_v5769.py',{
        **shared,'dispatches_v5704':'dispatches_v5769','voices_v5703':'voices_v5768',
        'len(cases)==34':'len(cases)==62','len(leaves)==12':'len(leaves)==16',
        "sum(c['source_selector']==254 for c in cases)==12":"sum(c['source_selector']==254 for c in cases)==2",
        'all17_source_current_dispatches_no_macros_and12_control_leaves':'all31_source_current_dispatches_one_FI_and16_control_leaves',
        'all12_nonrelative':'all16_nonrelative','all2_static_actors':'all3_static_actors',
        'six_FE_spoken_voice_objects_use_original_null_actor_path':'one_FE_sound_effect_object_uses_original_null_actor_path',
        'Bind34 source/current speech calls and12':'Bind62 source/current speech calls and16',
        '34 source/current dispatches pass:two static actors,six speaking FE/null-actor objects,no FI/FA/FO. All12':
        '62 source/current dispatches pass:three static actors,one sound-effect FE/null-actor object,one FI/no FA/FO. All16'}))
    rows.append(derive('scripts/prove_lil_B198_entry_v5705.py','scripts/prove_lil_B199_entry_v5770.py',{
        **shared,'entry_v5705':'entry_v5770','voices_v5703':'voices_v5768','[198]':'[199]'}))
    rows.append(derive('scripts/prove_lil_B198_branches_v5706.py','scripts/prove_lil_B199_branches_v5771.py',{
        **shared,'branches_v5706':'branches_v5771','len(edges)==8':'len(edges)==0','len(cases)==80':'len(cases)==0'}))
    rows.append(derive('scripts/prove_lil_B198_names_v5707.py','scripts/prove_lil_B199_names_v5772.py',{
        **shared,'names_v5707':'names_v5772','voices_v5703':'voices_v5768',
        'current207_catalog_eight_voices_and_two_source_selectors':'current207_catalog_eight_voices_and_three_source_selectors',
        '[12,15]':'[2,9,22]',"len(native['rows'])==4":"len(native['rows'])==6",'fresh2_actor_names':'fresh3_actor_names',
        'native_four_consumer_cases':'native_six_consumer_cases','four_original_progressive':'six_original_progressive',
        'Four source-owned':'Six source-owned'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_mapping_and_native_consumers.json',dict(tools=rows,
        source_speeches=31,progressive=30,FE_sound_effects=1,static_selectors=[2,9,22],FI=1,FA=0,FO=0,
        commands=47,relative_sites=0,predicates=0,source2000_pause_sites=1,nonrelative_nonspeech_leaves=16,choices=0,
        source_transition_picture_and_effect_semantics_still_pending=True,
        no_prior_English_speech_comparison_ROM_or_credit_change=True,full_goal_complete=False))
    print('B199 mapping/three voice identities/62dispatches/entry/no-relative/six name consumers prepared. Source controls and complete context still pending;no credit.')
