"""Derive the B203 atomic compiler with exact source and measured-scene guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.seal_lil_B203_references_v6046 import FLAGS
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('dk4tool/patch/lil_B202_editorial_v4.py');s=p.read_text(encoding='utf-8');a=s.index('FLAGS=');b=s.index('\ndef load',a)
    name1=next(x for x in s.splitlines() if "require(names['progressive_nameplate_values']" in x)
    name2=next(x for x in s.splitlines() if "require(len(names['native_eight_consumer_cases']" in x)
    title=next(x for x in s.splitlines() if "require(terms['source_item14']" in x)
    changes={
        s[a:b]:'FLAGS='+repr(FLAGS)+'\n',
        'B202':'B203','lil_B202_layout_v2':'lil_B203_layout_v2','lil_B202_profile':'lil_B203_profile',
        'translations/lil_B202_editorial_release_v4.json':'translations/lil_B203_editorial_release_v1.json',
        'SELECTORS={2,18,147,157}':'SELECTORS={2,76,170,254}',
        'all19':'all22',
        "len(native['cases'])==19":"len(native['cases'])==22",
        "native['current_original_macro_alignment_calls']==152":"native['current_original_macro_alignment_calls']==176",
        "native['complete_progressive_planes']==19":"native['complete_progressive_planes']==21",
        "native['complete_FE_logical_and_physical_planes']==0":"native['complete_FE_logical_and_physical_planes']==1",
        "len(native['negative_controls'])==21":"len(native['negative_controls'])==22",
        "len(approval['formatter_negatives'])==14 and len(approval['three_individual_rowcount_reasons'])==3":"len(approval['formatter_negatives'])==28 and len(approval['six_individual_rowcount_reasons'])==6",
        "len(stored['final_target_parity_cases'])==19":"len(stored['final_target_parity_cases'])==22",
        "stored['current_final_stored_macro_alignment_cases']==76 and stored['new_parity_macro_alignment_cases']==44 and stored['exact_byte_identical_reused_macro_alignment_cases']==32":"stored['current_final_stored_macro_alignment_cases']==88 and stored['new_parity_macro_alignment_cases']==40 and stored['exact_byte_identical_reused_macro_alignment_cases']==48",
        "len(controls['relocated_dispatch_cases'])==19":"len(controls['relocated_dispatch_cases'])==22",
        "len(controls['all7_source_current_target_control_leaves'])==7":"len(controls['all9_source_current_target_control_leaves'])==9",
        "controls['all19_progressive_and_zero_FE_objects_preserved'] and controls['no_FI_FA_FO_inherited']":"controls['all21_progressive_and_one_FE_object_preserved'] and controls['one_original_FI_zero_FA_FO_preserved']",
        "[('current',582),('research',574)]":"[('current',810),('research',764)]",
        name1:"    require(names['progressive_nameplate_values']=={'2':'Lil Argot','76':'Mikhail Letzel','170':'Mysterious Old Man'} and names['full_catalogue_values']=={'2':'Lil Argot','76':'Mikhail Volk Letzel','170':'Mysterious Old Man'},'distinct original name consumers required')",
        name2:"    require(len(names['native_six_consumer_cases']['rows'])==6 and [[f.get('Japanese') for f in r['fields']] for r in fields['source_name_fields']]==[['リル','アーゴット',None],['ミハイル','レッツェル','フォルク'],['謎の老人','国籍不明',None]] and fields['no_name_asset_or_runtime_change'] and fields['no_global_207_name_closure_or_new_name_completion_credit'],'exact clean name fields and no invented profession or nationality required')",
        "voices['fresh4_actor_names']['rows']}=={2:3,18:0,147:0,157:4}":"voices['fresh3_actor_names']['rows']}=={2:3,76:5,170:0}",
        'all four source voices required':'all three source voices required',
        title:"    require(terms['source_item18']['Japanese']=='漢方医の聖典' and terms['source_item18']['current_English']==\"Herbalist's Bible\" and terms['source_item18']['not_an_explicit_spoken_title'] and terms['all22_source_objects_observed'] and terms['following_source_item_terminology_lead']['current_wording_needs_contextual_terminology_revisit'],'unspoken title scope and following unresolved lead required')",
        "actual['actual_unique_speech_panels']==actual['complete_matching_observations']==19":"actual['actual_unique_speech_panels']==actual['complete_matching_observations']==22",
        "actual['complete_matching_holds']==74":"actual['complete_matching_holds']==86",
        "len(actual['actual_panels'])==19":"len(actual['actual_panels'])==22",
        "sum(len(p['holds']) for p in actual['actual_panels'])==74":"sum(len(p['holds']) for p in actual['actual_panels'])==86",
        'panels/74 native holds':'panels/86 native holds',
        '[35,35]':'[40,40]','[7657,7655]':'[8374,8373]',
        'len(timed)==22':'len(timed)==23',"len(actual['later_whole_RGB_differences'])==21":"len(actual['later_whole_RGB_differences'])==18",
        "[(106,-1,0x4000),(228,4,0x4000),(326,-5,0x4000)] and len(state['within_scene_RNG_differences'])==5":"[(208,-1,0x4000)] and len(state['within_scene_RNG_differences'])==0",
        "and not state['final_PRNG_equal']":"and state['final_PRNG_equal']",
        "and sample['representative_shared_rules_approved']":"and sample['generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350'] and state['generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350'] and sample['representative_shared_rules_approved']",
        'event202_activation':'event203_activation',
        'len(rows)==len(set(ids))==19':'len(rows)==len(set(ids))==22',
        "Counter(r['kind'] for r in rows)=={'progressive':19}":"Counter(r['kind'] for r in rows)=={'progressive':21,'system-FE':1}",
        "Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':13}":"Counter(r['editorial_decision'] for r in rows)=={'revise':9,'retain-wording':13}",
        'exact19 decisions/consumers':'exact22 decisions/consumers',
        '==202':'==203','[202]':'[203]','block=202':'block=203',
        "spec['source_bytes']==len(block)==588 and spec['source_logical_end']==586 and spec['research_bytes']==580 and spec['research_logical_end']==578":"spec['source_bytes']==len(block)==816 and spec['source_logical_end']==814 and spec['research_bytes']==768 and spec['research_logical_end']==768 and spec['source_alignment_tail_bytes']==2 and spec['target_alignment_tail_bytes']==0",
        "require(not macros,'B202 has no source FI/FA/FO')":"require(macros==Counter({b'FI':1}),'B203 requires one original FI and no FA/FO')",
        'end==586 and len(block)==588':'end==814 and len(block)==816',
        'mapped(end)==578':'mapped(end)==768','len(target)==580 and len(logical)==578':'len(target)==768 and len(logical)==768',
        "len(commands)==26 and sum(c['word']==0x4000 for c in commands)==19":"len(commands)==31 and sum(c['word']==0x4000 for c in commands)==22",
        '[(582,574)]':'[(810,764)]',
        "exact=[(162,'2a63'),(182,'2a63'),(322,'35480ea8'),(564,'00a0ffff01000e30'),(572,'2147'),(574,'00a0ffff1d000100'),(582,'00000000')]":"exact=[(334,'204812a8'),(738,'3547'),(740,'0360'),(742,'2e63'),(778,'00a0fffffaff0191'),(786,'00a0ffff01020260'),(794,'00a0ffff01001230'),(802,'00a0ffff1d000100'),(810,'00000000')]",
        '7 exact leaves required':'9 exact leaves required',
        '[0x632A,0x632A,0x4835,0xA000,0x4721,0xA000,0]':'[0x4820,0x4735,0x6003,0x632E,0xA000,0xA000,0xA000,0xA000,0]',
        'source_commands=26':'source_commands=31',
        'all19_progressive_zero_FE_no_macros_two632A_picture47xx_two_A000_and_single_end_preserved':'all21_progressive_one_FE_FI_resource632E_6003_picture47xx_four_A000_and_single_end_preserved',
        'actual_two_complete_B22_fixtures19_panels74_holds22_timings21_prompt_differences_unequal_PRNG_not_natural_activation':'actual_two_complete_B22_fixtures22_panels86_holds23_timings18_prompt_differences_equal_sampled_PRNG_not_natural_activation',
    }
    result=derive(str(p),'dk4tool/patch/lil_B203_editorial_v1.py',changes)
    root=Path('work/analysis/lil_B203_compiler_tools_v6047');root.mkdir(parents=True);save(root/'compiler_derivation.json',dict(tool=result,all22_source_objects_nine_leaves_and_exact816_inverse_guarded=True,complete_actual_native_scope_and_measured_differences_bound=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('B203 atomic compiler prepared;one guarded archive mutation after complete source/native/reference/actual checks.')
