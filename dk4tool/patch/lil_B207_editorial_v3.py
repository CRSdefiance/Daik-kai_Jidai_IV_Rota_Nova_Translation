"""Atomic thirteen-record B207 release; all validation precedes its sole mutation."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B207_layout_v2 as codec
from dk4tool.dialogue.lil_B207_profile_v1 import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
PATH='/data/SC2.DK4'
CONFIG='translations/lil_B207_editorial_release_v3.json'
FLAGS=['all15_commands13_complete_preambles_two_opaque_leaves_no_relative_menu_FE_macro','all656_predecessor_bytes_inverse_source654_tail2_target612_tail0','all13_actual_panels51_native_holds_and_normal_port_return','Lil_Argot_Emilio_Ferog_source_context_name_retentions_style11_no_asset_change','same_current_ARM9_COMMON_all_components_and_ordinary_inputs_source_baseline_bound','all13_timing_three_RNG_six_prompt_RGB_and_different_final_PRNG_retained','five_native_groups_actor_equal_not_whole_state_or_future_sequence','source_uncertainty_personal_conditional_search_undecided_gift_food_joke_and_cheers_preserved','one_exact_it_if_boundary_three_individual_rowcount_reasons_no_blanket_waiver','natural_activation_original_location_earned_progress_full_effects_routes_hardware_unclaimed']
def load(p):return json.loads(Path(p).read_bytes())
def require(v,message):
    if not v:raise ValueError('Lil B207 '+message)

def validate_observations(doc,mapping,conf):
    """Bind individual native and actual consumers, preserving measured differences."""
    p={k:load(doc[k]) for k in ['native_font_proof','final_padding_proof','relocated_control_proof','loader_proof','source_census','termination_decode_proof','actual_proof','postscene_native_state_proof','representative_proof','native_approval','speaker_name_approval']}
    native,stored,controls,loader,census,ends,actual,state,view,approval,names=p.values()
    require(native['current_original_macro_alignment_calls']==104 and native['complete_progressive_planes']==13 and native['source_FE_planes']==0,'native consumer scope')
    require(approval['all13_five_gates_approved'] and approval['source_and_formatter_negative_controls']==31 and len(approval['three_individual_source_target_rowcount_reasons'])==3 and approval['one_reviewed_ordinary_boundary'],'individual formatter approval')
    require(stored['current_final_stored_macro_alignment_cases']==52 and stored['new_parity_macro_alignment_cases']==36 and stored['exact_byte_identical_reused_macro_alignment_cases']==16 and stored['new_parity_tail_planes']==9 and stored['all13_final_targets_complete_native_planes_equal_reviewed_planes'],'stored parity proof')
    require(len(controls['relocated_dispatch_cases'])==13 and len(controls['all2_source_current_target_nontext_leaves'])==2 and len(controls['fresh_current_target10_complete_end_cases'])==10 and controls['original_names_Lil_Argot_and_Emilio_Ferog_preserved'] and controls['no_natural_event_or_full_quest_inventory_or_eligibility_claim'],'control/name scope')
    require(loader['all336_whole_blocks_and672_modes_each_pass'] and loader['B207_fits_original_0x2400_cache'] and loader['SDK_IO_bridges_only_no_loader_or_cache_success_stub'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'],'loader/cache scope')
    require([r['ROM_sha256'] for r in loader['versions']]==[doc['current_ROM_sha256'],conf['reference_ROM_sha256']],'loader ROM identities')
    for r in loader['versions']:
        require(r['whole_SC2_loads_and_cache_hits']==336 and r['original_parent_modes']==672,'loader cases')
        for k in ['load','parent']:require(sha(Path(r[k+'_proof']).read_bytes())==r[k+'_sha256'],'loader evidence')
    require(census['all15_clean_current_target_commands_and_no_relative_sites_reexecuted'] and census['research_ROM_sha256']==conf['reference_ROM_sha256'] and census['blocks'][0]['mapped_commands']==mapping['blocks'][0]['mapped_native_commands'],'independent command census')
    require(ends['no_end_decode_zero_tail_dependency'] and ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',650),('research',608)],'guarded complete ends')
    require(names['two_native_name_planes_four_getters32_macro_alignments51_actual_header_holds_approved'] and names['source_specific_ASCII_flush_and_original_style11_bound'] and names['all_other_names_aliases_full_goal_and_later_technical_reaudit_open'],'contextual names')
    require(actual['actual_unique_speech_panels']==actual['actual_English_speech_observations']==13 and actual['complete_native_text_and_nameplate_holds']==51,'actual coverage')
    require(not any(actual[k] for k in ['failures','offline_only_display_IDs','command_result_differences','command_UI_word_differences','paired_nontext_region_differences']),'actual findings')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(ids==[r['id'] for r in actual['actual_panels']]==mapping['actual_sampled_display_IDs'] and mapping['offline_only_display_IDs']==[],'actual IDs')
    for panel,row in zip(actual['actual_panels'],rows,strict=True):
        require(panel['prefix']==row['source_selector'] and panel['name']=={2:'Lil Argot',14:'Emilio Ｆerog'}[row['source_selector']] and panel['native_plane_sha256']==row['native_font_case']['whole_native_plane_sha256'] and panel['holds'],'panel identity')
        for h in panel['holds']:
            require(all(h[k] for k in ['all216x64_ink_gray_pixels_equal_complete_native_plane','complete_current_style11_nameplate_glyphs_and_blank_guards_equal','both_versions_in_same_semantic_speech_at_this_frame','paired_upper_portrait_name_region_equal']) and sha(Path(h['capture']).read_bytes())==h['capture_sha256'],'complete actual body/name/source hold')
    left,right=actual['versions'];require([v['frames'] for v in [left,right]]==[11001,11001] and [v['exit_frame'] for v in [left,right]]==[5976,5974] and all(len(v['command_pairs'])==24 for v in [left,right]),'actual run extents')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(left)==shape(right),'actual command results')
    expected=[None]*9+[r['old_offset'] for r in mapping['blocks'][0]['command_map']]
    for v in [left,right]:
        require([r['source_offset'] for r in v['command_pairs']]==expected and [(r['id'],r['source_record_index'],r['prefix']) for r in v['speech_intervals']]==[(r['id'],r['source_record_index'],r['source_selector']) for r in rows],'actual complete source identities')
        report=load(v['capture_report']);require(report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==11001,'cold-boot input scope')
    timing=[];rng=[]
    for a,b in zip(left['command_pairs'],right['command_pairs'],strict=True):
        identity=dict(source_offset=a['source_offset'],word=a['word'])
        if [a['start'],a['returned']]!=[b['start'],b['returned']]:timing.append(dict(**identity,Japanese=[a['start'],a['returned']],English=[b['start'],b['returned']]))
        if [a['before_RNG'],a['after_RNG']]!=[b['before_RNG'],b['after_RNG']]:rng.append(dict(**identity,Japanese=[a['before_RNG'],a['after_RNG']],English=[b['before_RNG'],b['after_RNG']]))
    require(actual['command_timing_differences']==timing and len(timing)==13 and actual['command_RNG_differences']==rng and len(rng)==3,'all timing/RNG witnesses')
    later=[r for r in actual['postscene_whole_RGB_comparisons'] if not r['whole_RGB_equal']]
    require(later==actual['later_whole_RGB_differences']==state['all_six_unmasked_later_differences'] and len(later)==6 and all(224<=r['whole_RGB_difference_bbox'][0]<r['whole_RGB_difference_bbox'][2]<=240 and 360<=r['whole_RGB_difference_bbox'][1]<r['whole_RGB_difference_bbox'][3]<=376 for r in later),'unmasked six prompt differences')
    require(state['five_native_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True) and state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal'] and state['final_PRNG_seeds']==[940971730,2496127907] and state['no_whole_RAM_future_sequence_broad_simulation_or_complete_timing_cause_claim'],'bounded final state and different seed')
    require(view['actual_proof_sha256']==state['actual_proof_sha256']==sha(Path(doc['actual_proof']).read_bytes()) and not view['visual_review_pending'] and view['no_open_translation_specific_display_control_or_return_finding'] and view['all13_timing_three_interval_RNG_six_prompt_RGB_and_final_PRNG_differences_retained'] and view['broad_postscene_full_RAM_future_world_equivalence_unproven'] and view['natural_event207_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed'] and view['final11001_both_following_B120_still_active_black_upper'],'honest representative scope')
    require(len(view['viewed_sheets'])==5 and all(r['viewed'] and r['viewed_after_image_return'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in view['viewed_sheets']),'five viewed sheets')
    require(actual['source_and_English_same_ARM9_COMMON_components_all_other_files_all335_other_blocks_and_input_schedules'] and actual['no_capture_masking_pixel_edit_or_retiming'] and actual['all_jobs_terminal_and_reaped'],'paired code/input provenance')
    require(not any(d.get('full_goal_complete') for d in [doc,mapping,*p.values()]),'full goal remains open')
    return p

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf.get('format')=='dk4-lil-B207-editorial-release-v3','release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical SC2')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean SC2')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']];validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records']),'individual five-gate manuscript')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed map')
    require(seal['all13_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'] and seal['all_measured_timing_RNG_state_and_RGB_scopes_preserved'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'seal')
    require(mapping['format']=='dk4-lil-B207-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm) and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'source-bound map')
    require(mapping.keys()>=set(conf['required_map_flags']) and all(mapping[k] is True for k in conf['required_map_flags']),'all map approvals')
    require(conf['required_map_flags']==FLAGS,'complete flag contract')
    for k in ['native_font_proof','final_padding_proof','relocated_control_proof','loader_proof','source_census','termination_decode_proof','actual_proof','postscene_native_state_proof','representative_proof','native_approval','speaker_name_approval','scoped_profile_module','native_formatter_module']:
        require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash:'+k)
    require(Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B207_profile_v1.py') and Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B207_layout_v2.py'),'exact scoped formatter')
    proofs=validate_observations(doc,mapping,conf);rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==13 and Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':7} and Counter(r['source_selector'] for r in rows)=={2:6,14:7} and all(r['kind']=='progressive' for r in rows),'exact thirteen decisions/actors')
    require(doc['broader207_name_and_full_editorial_scope_remain_open'] and doc['existing88_Christina23_Cristina_individual_consumer_queue_remains_open'],'open name/alias scope')
    require(len(mapping['blocks'])==1,'one block');spec=mapping['blocks'][0];blocks=list(IlnkContainer.parse(source).blocks);block=blocks[207];original=IlnkContainer.parse(japanese).blocks[207]
    require(len(blocks)==336 and spec['block']==207 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block')
    require((spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'],spec['source_alignment_tail_bytes'],spec['target_alignment_tail_bytes'])==(656,654,612,612,2,0),'exact extents')
    commands=spec['mapped_native_commands'];require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in commands]==spec['command_map'],'independent command agreement')
    require(not any(spec[k] for k in ['choice_commands','actor_style_commands','original2000_pause_and_resume_maps','relative_skip_fixups','target_native_skip_cases']),'no invented controls')
    fonts={r['id']:r for r in proofs['native_font_proof']['cases']};refs={r['id']:r for r in spec['text_records']};stored={r['id']:r for r in proofs['final_padding_proof']['final_target_parity_cases']};dispatch={r['id']:r for r in proofs['relocated_control_proof']['relocated_dispatch_cases']}
    require(set(fonts)==set(refs)==set(stored)==set(dispatch)==set(ids),'complete individual proof sets')
    profile=profile_for(arm,block);patches=[];changes=[];boundaries=0;rowcount=0
    for row in rows:
        ident=row['id'];case,ref,st,di=[d[ident] for d in [fonts,refs,stored,dispatch]];at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['block']==207 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0] and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}'),'selector:'+ident)
        for side,bank,offset,value,idx in [('source',original,sa,raw,row['source_record_index']),('current',block,at,old,row['current_record_index'])]:
            r=row[side+'_reference'];require((r['block']==207 and r['record_index']==idx if side=='source' else row['block']==207) and idx==bank[:offset].count(b'\0') and r['bytes']==len(value) and r['header_offset']==offset-5 and bank[offset:offset+len(value)]==value and bank[offset+len(value)]==0,'source/current reference:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1] and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'preamble:'+ident)
        require(row['record_index']==row['current_record_index']==ref['record_index'] and ref['old_offset']==at and ref['old_length']==len(old) and row['current_text_hex']==old.hex(),'current record:'+ident)
        require(not re.findall(rb'FI|FA|FO|FU',raw[1:]) and '{MACRO:' not in row['english'] and not any(t in row['english'] for t in ['{LB','{ALIGN','{PAD}']),'no authored controls/macros')
        encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and row['native_font_case']==case,'compiled/native agreement:'+ident)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not (i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved layout:'+ident)
        require(row.get('qa_waivers') in [None,['line-break-count']],'no safety waiver');rowcount+=bool(row.get('qa_waivers'))
        require(row.get('reviewed_ordinary_boundaries',[])==qa.get('reviewed_ordinary_boundaries',[]),'exact ordinary boundary');boundaries+=len(row.get('reviewed_ordinary_boundaries',[]))
        require(all(case[k] for k in ['complete_native_independent216x64_plane_equal','all_first_final_internal_glyphs_in_order_and_unique_cells','all_visible_origins_zero_and_within_four_rows','one_native_page_consumes_complete_target']) and sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'complete glyphs/bounds/page:'+ident)
        require(row['actual_B22_display_fixture_observed'] and not row['offline_only_native_display_checked'] and not row['current_native_UI_body_explicit_unexecuted_boundary'] and row['native_display_consumer']=='original_progressive_54020','individual actual scope')
        oldprose=' '.join(old[1:].decode('cp932').split());prose=row['english'].split('}',1)[1]
        require(row['effective_predecessor_paragraph']==oldprose and (prose!=oldprose)==(row['editorial_decision']=='revise'),'decision:'+ident)
        require(row['editorial_decision']!='retain-wording' or row.get('fresh_retained_wording_justification'),'retention reason')
        require(row['registered_runtime_catalog_entry'] is None and row['previous_registered_catalog_entry'] is None and di['registered_catalog_match'] is None and di['resolved_actor_ID']==di['source_selector']==raw[0] and di['source_voice_class']=={2:3,14:6}[raw[0]],'current catalogue/voice')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex']==st['stored_target_hex']==di['stored_target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added']==st['parity_space_added'] and st['complete_final_target_native_plane_equals_reviewed_plane'] and st['tail_padding_consumed_without_blank_page_or_lost_glyph'] and st['native_plane_sha256']==case['whole_native_plane_sha256'],'stored plane/parity:'+ident)
        require(len(st['current_final_target_macro_alignment_cases']['cases'])==4,'stored alignment')
        patches.append(dict(start=at,end=at+len(old),value=value,old=old));changes.append(dict(id=ident,block=207,kind='progressive',old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(boundaries==1 and rowcount==3,'one exact boundary/three row reasons')
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlap')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'interior reference')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-(p['end']-p['start'])
        return offset+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==654 and len(block)==656 and block[end:]==bytes(2),'source end/tail')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==612,'target logical extent');struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)
    require(sha(target)==spec['target_block_sha256'],'target hash')
    for c in changes:
        r=refs[c['id']];at=mapped(c['old_offset']);require(at==c['new_offset']==r['new_offset']==stored[c['id']]['stored_offset']==dispatch[c['id']]['new_offset'] and target[:at].count(b'\0')==r['new_record_index'],'integrated reference:'+c['id'])
    require(len(commands)==15 and sum(c['word']==0x4000 for c in commands)==13,'15 commands')
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0] and mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command extent')
        require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'no ancestors')
        require(block[a:a+(6 if c['word']==0x4000 else c['old_native_extent'])]==target[b:b+(6 if c['word']==0x4000 else c['new_native_extent'])],'opaque/preamble preservation')
    leaves=[c for c in commands if c['word']!=0x4000]
    require([(c['old_offset'],c['new_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==[(642,600,'00a0ffff29000110'),(650,608,'00000000')],'one exact A000 and complete end')
    require([(c['old_offset'],c['new_offset'],4) for c in leaves if c['word']==0]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'declared end map')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)+block[end:]==block,'every656 predecessor byte inverse')
    newblocks=list(blocks);newblocks[207]=target;result=IlnkContainer(newblocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(blocks,newblocks,strict=True)) if a!=b]==[207],'sole target block')
    image.replace_file(PATH,result)
    return dict(manuscript=conf['manuscript'],reference_map=conf['reference_map'],source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),changed_records=changes,blocks=[dict(block=207,source_bytes=656,target_bytes=612,source_logical_end=654,target_logical_end=612,relative_operands=0,source_commands=15,inverse_restores_every_original_stored_byte=True)],all335_other_SC2_blocks_unchanged=True,all13_progressive_complete_preambles_one_A000_complete_end_and_zero_macros_preserved=True,native_code_and123264_staged_payload_unchanged=True,actual13_panels51_holds_and_return_approved_with_measured_timing_RNG_prompt_and_different_final_seed_scope=True,full_goal_complete=False)
