"""Atomic B202 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B202_layout_v2 as codec
from dk4tool.dialogue.lil_B202_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B202_editorial_release_v3.json'
SELECTORS={2,18,147,157}
FLAGS=['all26_commands19_preambles7_opaque_leaves_complete_no_relative_or_menu', 'all588_predecessor_bytes_inverse_source586_target578_logical580_stored_two_tailzeros', 'all19_actual_panels74_complete_native_holds_match_source_regions', 'four_original_actors_voices_zero_FE_and_zero_FI_FA_FO_preserved', 'Sailor_progressive_alias_Retainer_catalogue_Charles_middle_field_and_Guildmaster_bound', 'Glassmaking_Guide_spoken_title_bound_clean_item14_widget_not_full_effect_approval', 'three_speech_duration22_start_return5_RNG21_prompt_differences_preserved', 'queried_native_groups_agree_PRNG_differs_no_broad_world_equivalence', 'following_B43_source_item_Local_Product_leads_uncredited_and_open', 'representative_shared_rules_approved_natural_activation_and_hardware_unclaimed']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B202 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B202-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all19_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'] and seal['all_measured_timing_RNG_state_and_prompt_differences_preserved'] and seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed references differ')
    require(mapping['format']=='dk4-lil-B202-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm) and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete source-bound map required')
    require(conf['required_map_flags']==FLAGS,'complete map flag list required')
    for flag in FLAGS:require(mapping.get(flag) is True,'map approval required:'+flag)
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof','source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','actual_proof','actor_terminology_reconciliation','contextual_reconciliation','actor_voice_contract']
    for k in keys:require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash differs:'+k)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B202_layout_v2.py') and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B202_profile.py'),'exact formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in keys[:6]]
    state=load(doc['postscene_native_state_proof']);actual=load(doc['actual_proof']);approval=load(conf['native_approval']);fields=load(doc['actor_terminology_reconciliation']);terms=load(doc['contextual_reconciliation']);voices=load(doc['actor_voice_contract'])
    require(len(native['cases'])==19 and native['current_original_macro_alignment_calls']==152 and native['complete_progressive_planes']==19 and native['complete_FE_logical_and_physical_planes']==0 and len(native['negative_controls'])==21 and all(r['rejected'] for r in native['negative_controls']),'complete native consumers required')
    require(approval['all19_five_gates_approved'] and len(approval['formatter_negatives'])==14 and len(approval['three_individual_rowcount_reasons'])==3,'formatter/rowcount approvals required')
    require(len(stored['final_target_parity_cases'])==19 and stored['current_final_stored_macro_alignment_cases']==76 and stored['new_parity_macro_alignment_cases']==44 and stored['exact_byte_identical_reused_macro_alignment_cases']==32 and stored['all19_final_targets_complete_native_planes_equal_reviewed_planes'],'final stored proof required')
    require(len(controls['relocated_dispatch_cases'])==19 and len(controls['all7_source_current_target_control_leaves'])==7 and len(controls['picture_and_short47xx_pairs'])==2 and controls['all19_progressive_and_zero_FE_objects_preserved'] and controls['no_FI_FA_FO_inherited'],'complete relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',582),('research',574)],'complete guarded end required')
    require(names['progressive_nameplate_values']=={'2':'Lil Argot','18':'Charles Rochefort','147':'Guildmaster','157':'Sailor'} and names['full_catalogue_values']=={'2':'Lil Argot','18':'Charles Jean Rochefort','147':'Guildmaster','157':'Retainer'},'distinct original names/aliases required')
    require(len(names['native_eight_consumer_cases']['rows'])==8 and fields['original_progressive_alias']['source']=='水夫' and fields['original_progressive_alias']['current']=='Sailor' and fields['original_progressive_alias']['selected_actor']==157 and fields['no_name_asset_or_runtime_change'] and fields['no_global_207_name_closure_or_new_name_completion_credit'],'source-defined alias scope required')
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh4_actor_names']['rows']}=={2:3,18:0,147:0,157:4},'all four source voices required')
    require(terms['source_item14']['Japanese']=='ガラスの製法辞典' and terms['source_item14']['current_English']=='Glassmaking Guide' and terms['all19_source_speeches_observed'] and terms['following_source_item_terminology_lead']['current_wording_needs_contextual_terminology_revisit'],'spoken title and following unresolved lead required')
    require(not actual['failures'] and not actual['paired_region_differences'] and actual['actual_unique_speech_panels']==actual['complete_matching_observations']==19 and actual['complete_matching_holds']==74 and actual['offline_only_source_indices']==[],'all19 actual panels/74 native holds required')
    require(len(actual['actual_panels'])==19 and [p['id'] for p in actual['actual_panels']]==mapping['actual_sampled_display_IDs'] and sum(len(p['holds']) for p in actual['actual_panels'])==74,'individual actual panels required')
    for panel,row in zip(actual['actual_panels'],doc['records'],strict=True):
        require(panel['id']==row['id'] and panel['prefix']==row['source_selector'] and panel['holds'] and panel['native_plane_sha256']==row['native_font_case']['whole_native_plane_sha256'],'actual panel identity/native plane differs')
        for hold in panel['holds']:require(hold['complete_ink_gray_masks_equal_native_plane'] and hold['upper_portrait_name_and_item_regions_equal_source'] and sha(Path(hold['capture']).read_bytes())==hold['capture_sha256'] and sha(Path(hold['clean_capture']).read_bytes())==hold['clean_capture_sha256'],'complete source-paired actual capture required')
    require([len(v['command_pairs']) for v in actual['versions']]==[35,35] and [v['fixture_exit_frame'] for v in actual['versions']]==[7657,7655] and actual['versions'][0]['input_schedule_sha256']==actual['versions'][1]['input_schedule_sha256'],'complete actual paths/input/return required')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(actual['versions'][0])==shape(actual['versions'][1]),'original command paths/results differ')
    expected_ids=[(r['id'],r['source_record_index'],r['source_selector']) for r in doc['records']];expected_offsets=[None]*9+[r['old_offset'] for r in mapping['blocks'][0]['command_map']]
    for version in actual['versions']:
        require([(r['id'],r['source_record_index'],r['prefix']) for r in version['selected_intervals']]==expected_ids and [r['source_offset'] for r in version['command_pairs']]==expected_offsets,'complete actual source identities differ')
        report=load(version['capture_report']);require(report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==13001,'actual cold-boot scope differs')
        for photo in report['frames_captured']:require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'sampled capture changed')
    timed=[dict(source=a,English=b) for a,b in zip(actual['versions'][0]['command_pairs'],actual['versions'][1]['command_pairs'],strict=True) if (a['start'],a['returned'])!=(b['start'],b['returned'])]
    require(actual['actual_timing_differences']==timed and len(timed)==22 and len(actual['later_whole_RGB_differences'])==21,'measured differences must remain explicit')
    require(state['actual_proof_sha256']==sample['actual_proof_sha256']==sha(Path(doc['actual_proof']).read_bytes()) and state['command_start_return_differences']==timed and state['later_whole_RGB_differences']==actual['later_whole_RGB_differences'],'measured proof bindings differ')
    require([(r['source_offset'],r['delta'],r['word']) for r in state['actual_command_duration_changes']]==[(106,-1,0x4000),(228,4,0x4000),(326,-5,0x4000)] and len(state['within_scene_RNG_differences'])==5,'source-specific speech timing/RNG witnesses required')
    require(state['native_final_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True) and state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal'] and state['no_causal_explanation_full_RAM_future_RNG_or_broad_simulation_equivalence_claim'],'honest measured state scope required')
    require(all(r['difference_bbox']==[224,360,240,376] and r['nontext_region_difference_bbox'] is None for r in actual['later_whole_RGB_differences']) and sample['all_later_differences_bounded_to_advance_prompt'],'unmodified later prompt differences required')
    require(sample['no_open_translation_specific_display_control_or_return_finding'] and sample['representative_shared_rules_approved'] and not sample['visual_review_pending'] and sample['no_causal_explanation_full_RAM_future_RNG_or_broad_simulation_equivalence_claim'] and sample['no_natural_event202_activation_original_location_earned_inventory_full_effects_full_route_or_hardware_claim'],'complete representative scope required')
    require(len(sample['viewed_sheets'])==6 and all(r['viewed'] and r['viewed_after_image_return'] and r['original_detail'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in sample['viewed_sheets']),'viewed actual and paired full screens required')
    require(not any(p.get('full_goal_complete') for p in [doc,mapping,seal,native,stored,controls,sample,state,approval]),'full editorial objective remains incomplete')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==19 and {r['source_selector'] for r in rows}==SELECTORS
        and Counter(r['kind'] for r in rows)=={'progressive':19}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':13},'exact19 decisions/consumers required')
    require(all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']) and [r['id'] for r in actual['actual_panels']]==ids
        and mapping['actual_sampled_display_IDs']==ids and sample['offline_only_display_IDs']==mapping['offline_only_display_IDs']==[],
        'all19 actual display IDs required')
    original_dispatch=load(doc['control_contract']);catalog=load(original_dispatch['registered_catalog_binding'])
    require(catalog['all467_rows_complete_keys_targets_route_masks_and_current_calls_verified'] and len(catalog['records'])==467 and all(c['registered_catalog_match'] is None for c in original_dispatch['speech_dispatch_cases']),'complete current name catalog binding required')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==202,'one exact block required')
    spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks)
    block,original=old_blocks[202],IlnkContainer.parse(japanese).blocks[202]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    require(spec['source_bytes']==len(block)==588 and spec['source_logical_end']==586 and spec['research_bytes']==580 and spec['research_logical_end']==578,'source/target extent metadata differs')
    require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in spec['mapped_native_commands']]==spec['command_map'],'both complete command maps must agree')
    fonts={c['id']:c for c in native['cases']};refs={r['id']:r for r in spec['text_records']}
    require(set(fonts)==set(refs)==set(ids),'native/reference coverage differs')
    require({c['id'] for c in controls['relocated_dispatch_cases']}==set(ids)
        and all(c['resolved_actor_ID']==(None if c['source_selector']==254 else c['source_selector']) and c['registered_catalog_match'] is None
            for c in controls['relocated_dispatch_cases']),'individual dispatch scope differs')
    patches=[];changes=[];macros=Counter()
    for row in rows:
        ident=row['id'];case,ref=fonts[ident],refs[ident];fe=row['kind']=='system-FE'
        require(row['actual_B22_display_fixture_observed'] and not row['offline_only_native_display_checked']
            and not row['current_native_UI_body_explicit_unexecuted_boundary'],'individual actual scope differs')
        require(case['complete_native_independent228x48_plane_equal' if fe else 'complete_native_independent216x64_plane_equal']
            and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and_within_four_rows']
            and case['one_native_page_consumes_complete_target'] and sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'complete native plane differs:'+ident)
        if fe:require(all(c['null_source_actor'] for p in case['current_native_macro_pipelines'] for c in p['cases']),'FE null actor differs')
        at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5 and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'complete source/current reference metadata differs:'+ident)
        require(row['source_reference']['block']==202 and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\0') and row['current_record_index']==block[:at].count(b'\0'),'complete source/current record identity differs:'+ident)
        require(row['block']==202 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
            and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}') and (raw[0]==254)==fe,'source selector differs:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0
            and row['current_text_hex']==old.hex(),'source/current text differs:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1]
            and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'complete preamble differs:'+ident)
        require(block[:at].count(b'\0')==row['record_index']==ref['record_index'] and ref['old_offset']==at and ref['old_length']==len(old)
            and row['native_display_consumer']==('original_null_actor_FE_24310_then5473C' if fe else 'original_progressive_54020'),'current reference differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])]
        require(sm==tm,'source substitution/order differs:'+ident);macros.update(sm)
        profile=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled English differs:'+ident)
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning'
            and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        require(not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries'),'unapproved inherited boundary exception')
        require(row.get('qa_waivers') in [None,['line-break-count']],'no additional safety waiver')
        require(row['native_font_case']==case,'approved native reference differs:'+ident)
        effective=old[1:]
        require(row['registered_runtime_catalog_entry'] is None,'no current B202 runtime override belongs here')
        old_prose=' '.join(effective.decode('cp932').split())
        logical_prose=row['english'].split('}',1)[1]
        for macro in ['FI','FA','FO']:logical_prose=logical_prose.replace('{MACRO:'+macro+'}',macro)
        require(row['effective_predecessor_paragraph']==old_prose,'effective predecessor differs:'+ident)
        require((logical_prose!=old_prose)==(row['editorial_decision']=='revise'),'revision/retention decision differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row.get('fresh_retained_wording_justification'),'individual retention reason required')
        require(not logical_prose.startswith('(') and not logical_prose.endswith(')'),'no private thought objects belong to B202')
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.append(dict(id=ident,block=202,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
    require(not macros,'B202 has no source FI/FA/FO')
    require(not spec['choice_commands'] and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps']
        and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases'],'invented control object')
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping text objects')
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            require(not p['start']<offset<p['end'],'interior text reference')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-(p['end']-p['start'])
        return offset+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(end==586 and len(block)==588 and block[end:]==bytes(2),'source logical tail differs')
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==578,'target logical extent differs')
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(len(target)==580 and len(logical)==578 and sha(target)==spec['target_block_sha256'],'target block differs')
    for change in changes:
        ref=refs[change['id']];at=mapped(change['old_offset'])
        require(at==change['new_offset']==ref['new_offset'] and target[:at].count(b'\0')==ref['new_record_index'],
            'relocated record offset/index differs:'+change['id'])
    commands=spec['mapped_native_commands'];require(len(commands)==26 and sum(c['word']==0x4000 for c in commands)==19,'command scope differs')
    for c in commands:
        a,b=c['old_offset'],c['new_offset']
        require(c['word']==struct.unpack_from('<H',block,a)[0]==struct.unpack_from('<H',target,b)[0],'opcode differs')
        require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'command boundary differs')
        require(not c['source_0100_ancestors'] and not c['target_0100_ancestors'],'invented ancestor')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'speech preamble differs')
        else:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'opaque leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([(c['old_offset'],c['new_offset']) for c in stops]==[(582,574)] and stops[-1]['new_offset']+4==len(logical),'single source tail endword required')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word']!=0x4000]
    exact=[(162,'2a63'),(182,'2a63'),(322,'35480ea8'),(564,'00a0ffff01000e30'),(572,'2147'),(574,'00a0ffff1d000100'),(582,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'7 exact leaves required')
    require([c['word'] for c in leaves]==[0x632A,0x632A,0x4835,0xA000,0x4721,0xA000,0],'numeric leaf scope differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse does not restore every predecessor byte')
    new_blocks=list(old_blocks);new_blocks[202]=target;result=IlnkContainer(new_blocks).to_bytes()
    require(sha(result)==conf['target_SC2_sha256'] and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[202],'whole SC2 target differs')
    # Every check above is read-only. This is the sole mutation.
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,
        blocks=[dict(block=202,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=0,
            source_commands=26,inverse_restores_every_original_logical_byte=True)],all335_other_SC2_blocks_unchanged=True,
        all19_progressive_zero_FE_no_macros_two632A_picture47xx_two_A000_and_single_end_preserved=True,
        actual_two_complete_B22_fixtures19_panels74_holds22_timings21_prompt_differences_unequal_PRNG_not_natural_activation=True,native_code_and123040_staged_payload_unchanged=True)
