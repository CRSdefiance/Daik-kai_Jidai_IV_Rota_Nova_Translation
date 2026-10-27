"""Prepare independent B171 completion audit with exact source/display/state scopes."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_final_audit_tools_v4358')
OLD=Path('scripts/verify_editorial_handoff_v4308b.py')
NEW=Path('scripts/verify_editorial_handoff_v4358.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    a=text.index("    assert spec['original2000_pause_and_resume_maps']");b=text.index('    control=read',a)
    old_source=text[a:b]
    new_source='''    assert not spec['original2000_pause_and_resume_maps'] and mapping['no_source_A000_or2000_pause']
    assert [r['word'] for r in spec['mapped_native_commands'] if r['word']!=0x4000]==[0x6000,0x4500,0x4621,0x61FF,0x6325,0xC200,0,0]
'''
    a=text.index("    assert repeat['paired_post_B170");b=text.index('    actual=read',a)
    old_repeat=text[a:b]
    new_repeat='''    assert repeat['paired_town11770_whole1A04_actor_models_and_captain2_equal']
    assert len(repeat['cross_language_command_timing_differences'])==22
    assert Counter(r['source']['word'] for r in repeat['cross_language_command_timing_differences'])=={0x4000:17,0x4621:1,0x61FF:1,0x6325:1,0xC200:1,0:1}
    assert repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
    assert all(all(r['component_equality'].values()) for r in repeat['paired_native_persistent_state_and_PRNG_samples'] if r['frame']<=16450)
    assert ledger['lil_B171_command_timing_count_amendment_v4349']==before['lil_B171_command_timing_count_amendment_v4349']
'''
    changes={
        old_source:new_source,old_repeat:new_repeat,
        'B170':'B171','lil_B170':'lil_B171','editorial_handoff_verification_v4308b':'editorial_handoff_verification_v4358',
        'completion_v4307':'completion_v4357','release_v4304':'release_v4354','all_routes_combined_v4251':'all_routes_combined_v4303',
        'lil_B170_reference_v4284':'lil_B171_reference_v4335','all-routes-unified-v4303':'all-routes-unified-v4353',
        'all-routes-unified-v4251':'all-routes-unified-v4303',
        'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33':'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37',
        '(1860,1752)':'(2120,2312)','in [2,25]':'in [2,25,81]',"{'FI':1,'FA':0,'FO':1}":"{'FI':1,'FA':0,'FO':0}",
        "stored['current_final_stored_macro_alignment_cases']==132":"stored['current_final_stored_macro_alignment_cases']==148",
        '(76,56)':'(88,60)',
        'source_offset=1852,target_offset=1742':'source_offset=2112,target_offset=2302',
        'source_offset=1856,target_offset=1746':'source_offset=2116,target_offset=2306',
        'all12_source_current_target_nonrelative_nonspeech_leaves':'all8_source_current_target_nonrelative_nonspeech_leaves',
        "len(control['all12_source_current_target_nonrelative_nonspeech_leaves'])==12":"len(control['all8_source_current_target_nonrelative_nonspeech_leaves'])==8",
        'native_four_consumer_cases':'native_six_consumer_cases','len(names)==4':'len(names)==6',
        'actual_v4293/actual_all33_pause_resources_A000_C200_and_first_end':'actual_v4342/actual_all37_dream_morning_presentations_resource_C200_and_first_end',
        "[('clean_Japanese',11257),('reviewed_English',11257)]":"[('clean_Japanese',11737),('reviewed_English',11735)]",
        "assert all(v['actual_source_A000_hex1019_2001']['result_words']==[3,0] for v in actual['versions'])":"assert all(v['actual_C200']['result_words']==[3,0] and [r['word'] for r in v['actual_presentation_commands']]==[0x6000,0x4500,0x4621,0x61FF] and [r['word'] for r in v['actual_resources']]==[0x6325] for v in actual['versions'])",
        'transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review':'transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review',
        'all6_actual_sheets_viewed':'all7_actual_sheets_viewed','==(6,4,3)':'==(7,6,4)',
        'startup_v4306':'startup_v4356','V4251':'V4303','registration_v4302b':'registration_v4352',
        "'promoted_main_build_v4289']":"'promoted_main_build_v4289','promoted_main_build_v4331']",
        'unfinished_editorial_scope_v4307':'unfinished_editorial_scope_v4357',
        'remaining_B171_B180':'remaining_B172_B180','V4307':'V4357',
        "len(manifest['batches'])==546":"len(manifest['batches'])==547",'manifest_batches=546':'manifest_batches=547',
        'actual_source_event170_selected':'actual_source_event171_selected',
        'all45_commands_zero_spans132_stored_cases_pause_resources_C200_both_ends_names_and_macros_bound':'all45_commands_zero_spans148_stored_cases_presentations_resource_C200_both_ends_names_and_macros_bound',
        'actual_two_B22_fixtures33_complete_planes_source_effect_and_normal_return_verified':'actual_two_B22_fixtures37_complete_planes_dream_morning_and_normal_return_verified',
        '546/114 stack':'547/114 stack',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    counts={'5725':'5762','5728':'5765','3635':'3659','2090':'2103','3872':'3909','4126':'4163','33':'37','21':'24','12':'13','198':'161'}
    text=re.sub(r'(?<!\d)(?:'+'|'.join(re.escape(k) for k in sorted(counts,key=len,reverse=True))+r')(?!\d)',lambda m:counts[m.group()],text)
    assert 'B170' not in text and '[170]' not in text
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        completion_audit_requires_sealed_release_and_startup=True,expected_completed=5762,expected_source_prose=5765,
        expected_revised=3659,expected_retained=2103,timing_split17_and5_preserved=True,full_goal_complete=False))
    print('Prepared independent B171 completion audit;5762 integrated and source/prose5765 expected after all gates.')
