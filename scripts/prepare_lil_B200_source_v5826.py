"""Bind B200's own19 speeches/two actors/two distinct FE roles without inherited semantics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B200_source_tools_v5826')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B199':'B200','source_v5767':'source_v5826','all31_clean_current_complete_context':'all19_clean_current_complete_context'}
    tools=[derive('scripts/map_lil_B199_source_v5767.py','scripts/map_lil_B200_source_v5826.py',{
        **shared,'verification_v5762':'verification_v5822',
        'work/analysis/lil_B199_clean_context_v5765/all31_clean_portrait_chase_found_book_and_misunderstood_gift_glosses.json':
        'work/analysis/lil_B200_clean_context_v5825/all19_clean_collapse_inn_recovery_declined_reward_and_Charm_glosses.json',
        'len(known)==6232':'len(known)==6263','blocks[199]':'blocks[200]','block=199':'block=200',
        'len(old)==47 and len(spoken)==31':'len(old)==31 and len(spoken)==19',
        '[2,9,22,254]':'[19,172,254]','[2,9,22]':'[19,172]',
        '[0x4631,0x0505,0x2000,0x632D,0x4621,0x630B,0x632A,0x0503,0x4821,0x4735,0x632B,0x4630,0x4895,0xA000,0x4720,0]':
        '[0x632D,0x4301,0x4600,0x4381,0x4830,0x4735,0x6003,0x632E,0xA000,0xA000,0x4640,0]',
        'macros==dict(FI=1,FA=0,FO=0)':'macros==dict(FI=0,FA=0,FO=0)',
        'lil_B198_runs_v5758':'lil_B199_runs_v5818','physical_speeches=31':'physical_speeches=19',
        'FE_panels=1,relative_sites=0':'FE_panels=2,relative_sites=0',
        'total_editorial_objects=31,speech_objects=31,ordinary_source_speeches=30,system_FE_panels=1':
        'total_editorial_objects=19,speech_objects=19,ordinary_source_speeches=17,system_FE_panels=2',
        'source_native_commands=47':'source_native_commands=31','source_A000=1':'source_A000=2','all31_clean_first':'all19_clean_first',
        'B199 bound:31 speeches/one sound-effect FE/30 progressive,47 commands/one FI/one2000 pause;three source actors and actual V5756 opening snapshot.No old-English speech comparison or credit.':
        'B200 bound:19 speeches/two distinct FE/17 progressive,31 commands/no FI;two source actors and actual V5816 opening snapshot.No old-English speech comparison or credit.'})]
    tools.append(derive('scripts/reconcile_lil_B199_voices_v5768.py','scripts/reconcile_lil_B200_voices_v5827.py',{
        **shared,'voices_v5768':'voices_v5827','[2,9,22]':'[19,172]','len(fresh)==3':'len(fresh)==2',
        'fresh3_actor_names':'fresh2_actor_names','three_source_selectors':'two_source_selectors','V5756':'V5816'}))
    tools.append(derive('scripts/prove_lil_B199_dispatches_v5769.py','scripts/prove_lil_B200_dispatches_v5828.py',{
        **shared,'dispatches_v5769':'dispatches_v5828','voices_v5768':'voices_v5827',
        'len(cases)==62':'len(cases)==38','len(leaves)==16':'len(leaves)==12',
        "sum(c['source_selector']==254 for c in cases)==2":"sum(c['source_selector']==254 for c in cases)==4",
        'all31_source_current_dispatches_one_FI_and16_control_leaves':'all19_source_current_dispatches_no_macros_and12_control_leaves',
        'all16_nonrelative':'all12_nonrelative','all3_static_actors':'all2_static_actors',
        'one_FE_sound_effect_object_uses_original_null_actor_path':'two_distinct_FE_objects_use_original_null_actor_path',
        'Bind62 source/current speech calls and16':'Bind38 source/current speech calls and12',
        '62 source/current dispatches pass:three static actors,one sound-effect FE/null-actor object,one FI/no FA/FO. All16':
        '38 source/current dispatches pass:two static actors,two distinct FE/null-actor objects,no FI/FA/FO. All12'}))
    tools.append(derive('scripts/prove_lil_B199_entry_v5770.py','scripts/prove_lil_B200_entry_v5829.py',{
        **shared,'entry_v5770':'entry_v5829','voices_v5768':'voices_v5827','[199]':'[200]'}))
    tools.append(derive('scripts/prove_lil_B199_branches_v5771.py','scripts/prove_lil_B200_branches_v5830.py',{
        **shared,'branches_v5771':'branches_v5830'}))
    tools.append(derive('scripts/prove_lil_B199_names_v5772.py','scripts/prove_lil_B200_names_v5831.py',{
        **shared,'names_v5772':'names_v5831','voices_v5768':'voices_v5827',
        'current207_catalog_eight_voices_and_three_source_selectors':'current207_catalog_eight_voices_and_two_source_selectors',
        '[2,9,22]':'[19,172]',"len(native['rows'])==6":"len(native['rows'])==4",'fresh3_actor_names':'fresh2_actor_names',
        'native_six_consumer_cases':'native_four_consumer_cases','six_original_progressive':'four_original_progressive',
        'Six source-owned':'Four source-owned'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_mapping_and_native_consumers.json',dict(tools=tools,
        source_speeches=19,progressive=17,FE_sound_effects=1,FE_stat_notifications=1,static_selectors=[19,172],FI=0,FA=0,FO=0,
        commands=31,relative_sites=0,predicates=0,nonrelative_nonspeech_leaves=12,choices=0,
        source_transition_picture_and_effect_semantics_still_pending=True,
        no_prior_English_speech_comparison_ROM_or_credit_change=True,full_goal_complete=False))
    print('B200 source mapping/two native voice identities/38 dispatches/entry/no-relative/four name consumers prepared. All native integer constants preserved;no credit.')
