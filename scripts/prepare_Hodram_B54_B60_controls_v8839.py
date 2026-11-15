"""Source-lock original controls to seven blocks, FE/progressive consumers and six unforced queries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_control_tools_v8839');assert not root.exists()
    module=derive('dk4tool/patch/hodram_B31_B53_controls_v1.py','dk4tool/patch/hodram_B54_B60_controls_v1.py',{
        'own-V8704':'own-V8778','hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_native_guards_v1':'hodram_B54_B60_native_guards_v1',
        'Hodram_B52_registered_route_context_v8707':'Hodram_B31_B53_registered_route_context_v8781',
        'Hodram_B31_B53_source_controls_v8718':'Hodram_B54_B60_source_controls_v8791','current_V8704_Hodram_native_v8707':'current_V8778_Hodram_native_v8781',
        'Hodram_B31_B53_relocation_v8728':'Hodram_B54_B60_relocation_v8809','ownV8704':'ownV8778',
        '[31,53]':'[54,55,56,57,58,59,60]','{31,53}':'{54,55,56,57,58,59,60}','complete ordered two-block scope':'complete ordered seven-block scope',
        "require([r['source_selector'] for r in rows]==[34,34,113],'three original progressive actors')":"voices={r['source_selector']:r['original_voice_class'] for r in data['source_names']['ten_source_selector_voices']['rows']}\n    require(len(rows)==82 and {r['source_selector'] for r in rows}=={1,20,23,24,36,84,113,114,119,141,254},'82 original mixed-consumer records')",
        "len(g['all_target_commands'])==9":"len(g['all_target_commands'])=={54:7,55:3,56:7,57:11,58:98,59:14,60:12}[number]",
        '(4 if number==31 else 0)':'(24 if number==58 else 0)','all9commands andrelative sites':'all native commands andrelative sites',
        "prefix='Hodram-B31-B53-controls-'":"prefix='Hodram-B54-B60-controls-'",
        "[31,52,53,74],'four original event/dependency getters'":"[15,54,55,56,57,58,59,60,65,76,128,129,142],'thirteen original event/dependency getters'",
        "boundary=next(r for r in result['boundaries'] if r['kind']=='unexecuted-progressive-body')":"is_FE=raw[0]==254\n                boundary=next(r for r in result['boundaries'] if r['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))",
        "result['resolved_actor_ID']==raw[0] and result['source_voice_class']=={34:1,113:0}[raw[0]] and not result['FE_original_null_actor_calls']":"result['resolved_actor_ID']==(None if is_FE else raw[0]) and result['source_voice_class']==(None if is_FE else voices[raw[0]]) and bool(result['FE_original_null_actor_calls'])==is_FE",
        'original exact actor/voice/noFE':'original exact progressive actor/voice orFE null actor',
        "native['bodies']['revised_English'][ref['id']]['expanded_body'].hex()==raw[1:].hex()":"native['bodies']['revised_English'][ref['id']]['expanded_body'].hex()==raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet').hex()",
        "previous=src['source_raw_query_cases'][0]":"previous=next(r for r in src['source_raw_query_cases'] if r['offset']==original['offset'])",
        "previous['native_result']==[2,1,0,0,0,0]":"previous['native_result'] and result['native_result'][0]==2",
        "if r['block']==number)":"if r['block']==number and r['source_offset']==original['offset'])",
        "dict(block=number,**result)==declared":"dict(block=number,source_offset=original['offset'],**result)==declared",
        "len(dispatches)==3 and len(branches)==4 and sum(len(r['cases']) for r in branches)==20 and len(queries)==1 and len(opaque)==8 and len(ends)==50":"len(dispatches)==82 and len(branches)==24 and sum(len(r['cases']) for r in branches)==120 and len(queries)==6 and len(opaque)==33 and len(ends)==175",
        'complete two-block independent control coverage':'complete seven-block independent control coverage',
        'independent_final_dispatches=3,relative_sites=4,native_relative_cases=20,raw_query_cases=1,original_EV1_entries=4,opaque_structural_decode_pairs=8,normal_seeded_ends=50':'independent_final_dispatches=82,relative_sites=24,native_relative_cases=120,raw_query_cases=6,original_EV1_entries=13,opaque_structural_decode_pairs=33,normal_seeded_ends=175',
        'all18commands3preambles_query_branches_fullends_separate_tail_andboth_resultchannels_bound':'all152commands82preambles6queries24branches_FE_nullactor_macros_fullends_separate_tails_andboth_resultchannels_bound',
    })
    validation=derive('scripts/validate_Hodram_B31_B53_controls_v8757.py','scripts/validate_Hodram_B54_B60_controls_v8840.py',{
        'hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_controls_v1':'hodram_B54_B60_controls_v1',
        'review_Hodram_B31_B53_actual_v8744':'review_Hodram_B54_B60_actual_v8825',
        "ROOT=Path('work/analysis/Hodram_B31_B53_controls_validation_v8757')":"PROOFS={**PROOFS,'source_display':'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json','source_names':'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json','current':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json','source_controls':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json'}\nROOT=Path('work/analysis/Hodram_B54_B60_controls_validation_v8840')",
        'translations/hodram_B31_B53_editorial_manuscript_v5.json':'translations/hodram_B54_B60_editorial_manuscript_v4.json',
        'translations/hodram_B31_B53_speaker_name_review_v3.json':'translations/hodram_B54_B60_speaker_name_review_v2.json',
        'Hodram_B31_B53_native_validation_v8754':'Hodram_B54_B60_native_validation_v8838','Hodram_B31_B53_reference_validation_v8756':'Hodram_B54_B60_reference_validation_v8836',
        'dk4tool/patch/hodram_B31_B53_controls_v1.py':'dk4tool/patch/hodram_B54_B60_controls_v1.py',
        'B31/B53 production controls:':'B54-B60 production controls:','Frozen Hodram-B31-B53 contract changed':'Frozen Hodram-B54-B60 contract changed',
        'six_complete_source_andstored_native_pages_two_current_progressive_names_andall_independent_pixels_exact':'all167_complete_source_andstored_native_pages_ten_current_progressive_names_andall_independent_pixels_exact',
        'positive_complete18command_native_inventories_and3disjoint_source_current_final_references':'positive_complete152command_native_inventories_and82disjoint_source_current_final_references',
        "bytes.fromhex(binding['stored_hex'])[1:]==body":"bytes.fromhex(binding['stored_hex'])[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')==body",
        '==[3,4,20,1,4,8,50,50]':'==[82,24,120,6,13,33,175,50]',
        "53,b['target_blocks'][53][:-2]":"60,b['target_blocks'][60][:-2]",
        "['groups'][0]['relocated_skip_cases'][0]":"['groups'][4]['relocated_skip_cases'][0]",
        "['fresh_target_query_cases'][0]['native_result'].__setitem__(1,0)":"['fresh_target_query_cases'][0]['native_result'].__setitem__(1,1)",
        'Independent controls:3dispatches/20relative cases/1rawquery/8opaquepairs/50normalends/50callerfragments/4EV1getters pass;12semantic defects reject.No nativeglyph/capture replay,ROMcommit orcredit.':'Independent controls:82dispatches/120relative cases/6rawqueries/33opaquepairs/175normalends/50callerfragments/13EV1getters pass;12semantic defects reject.No nativeglyph/capture replay,ROMcommit orcredit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_controls.json',dict(module=module,validation=validation,all_original_current_context_instruction_ABI_input_output_scratch_canary_command_dispatch_voice_query_relative_event_fullterminal_resultchannel_andinverse_guards_preserved=True,FI_FA_expansions_andFE_nullactor_bound_without_global_runtimechanges=True,new_credit=0,full_goal_complete=False))
