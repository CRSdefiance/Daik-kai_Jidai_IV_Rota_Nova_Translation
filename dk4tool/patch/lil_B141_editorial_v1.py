"""Exact-source14-speech/13-span polder funding release with guarded native evidence."""
import json,struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.lil_B141_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.lil_B141_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
PATH='/data/SC2.DK4'
CONFIG='translations/lil_B141_editorial_release_v1.json'
INDICES=[15,26,41,47,50,54,58,63,66,69,73,77,80,84]
def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def require(ok,reason):
    if not ok:raise ValueError('Lil B141 '+reason)
def apply_release(image,baseline,config_path=CONFIG):
    config=load(config_path);require(config.get('format')=='dk4-lil-B141-editorial-release-v1','unknown release format')
    for p,d in config['dependencies'].items():require(sha(Path(p).read_bytes())==d,'reviewed dependency differs:'+p)
    arm=image.read_file('/__arm9__.bin');source=image.read_file(PATH);require(sha(arm)==config['required_runtime_arm9_sha256'],'native runtime differs')
    require(sha(source)==config['source_SC2_sha256'] and sha(baseline.read_file(PATH))==config['canonical_SC2_sha256'],'current/canonical source differs')
    require(sha(Path(config['clean_ROM']).read_bytes())==config['clean_ROM_sha256'],'clean ROM differs');japanese=NdsImage.open(config['clean_ROM']).read_file(PATH);require(sha(japanese)==config['clean_SC2_sha256'],'clean source script differs')
    doc,mapping=map(load,[config['manuscript'],config['reference_map']]);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and doc['formatting_review_pending'] is False,'editorial policy/gates differ')
    require(doc['required_runtime_ARM9_sha256']==sha(arm) and doc['reference_map']==config['reference_map'] and sha(Path(doc['reference_map']).read_bytes())==doc['reference_map_sha256'],'map/runtime binding differs')
    require(mapping['format']=='dk4-lil-B141-source-relocation-map-v1' and mapping['entry_point_offset']==8 and mapping['required_runtime_ARM9_sha256']==sha(arm) and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==config['target_SC2_sha256'],'complete source reference map required')
    for k in ['external_references_complete','preserve_record_parity','all37_source_current_target_commands_and13_relative_sites_verified','all65_target_skip_cases_preserve_original_boundaries','all14_active_speech_targets_preserved','all3_predicates_and7_monetary_boundary_cases_preserved','all4_A000_source_operands_exact','opaque630A_source_operand_and_original_boundary_preserved','C200_source_index0_nine_UI_writes_and_unowned_RAM_preserved','both_funding_paths_end_at_in_block0000_terminator','no_zero_cache_tail_dependency','no_FE_source00_2100_2000_dynamic_or4100_objects','representative_shared_rules_approved']:require(mapping.get(k) is True,'missing reference gate:'+k)
    require(mapping['original_source_threshold_gold']==1000000 and mapping['original_source_payment_gold']==900000,'threshold/payment distinction differs')
    for k in ['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_proof']:require(sha(Path(doc[k]).read_bytes())==doc[k+'_sha256'],'proof binding differs:'+k)
    require(doc['representative_proof']==mapping['representative_proof'] and doc['termination_proof']==mapping['termination_proof'],'map/proof paths differ')
    representative=load(doc['representative_proof']);require(representative['no_open_translation_specific_display_or_control_finding'] and representative['individual_conditional_visits_not_required_under_user_policy'] and representative['current_ARM9_COMMON_EV2_font_and_source_B22_B24_B74_exact'] and representative['all_C200_shared_nontext_assets_exact_prior_actual_binding'] and representative['all14_final_planes56_macros_and_focused_financial_native_cases_pass'] and representative['no_zero_tail_dependency'] and representative['actual_selected_B141_IDs']==[] and representative['new_emulator_runs']==0,'source-bound representative approval required')
    native=load(doc['native_font_proof']);require(len(native['cases'])==14 and native['current_original_macro_alignment_calls']==112 and native['all14_current_native_speech_planes_pass'],'complete native planes/macros required')
    require(len(native['source_bound_formatter_negatives'])==14 and len(native['source_consumer_negative_controls'])==17 and all(c['rejected'] for c in native['source_bound_formatter_negatives']+native['source_consumer_negative_controls']),'native guard negatives required')
    for s in native['review_sheets']:require(sha(Path(s['path']).read_bytes())==s['sha256'] and s['review'].startswith('Viewed final'),'viewed native sheet differs')
    padding=load(doc['final_padding_proof']);require(padding['current_final_padded_macro_alignment_cases']==56 and len(padding['final_target_parity_cases'])==14 and padding['all14_final_targets_complete_native_planes_equal_reviewed_planes'],'stored target proof incomplete')
    controls=load(doc['relocated_control_proof']);require(len(controls['relocated_dispatch_cases'])==14 and len(controls['relocated_predicate_pairs'])==3 and controls['all3_source_predicates_and7_monetary_cases_semantically_preserved'] and controls['all14_expected_progressive_consumers_and_FI_text_exact'],'relocated source consumers/predicates required')
    pairs=controls['relocated_predicate_pairs'];require({p['cases'][0]['source_command_hex'] for p in pairs}=={'0080ffff0e0001a1','0080ffff09fe0030','0080ffff14fe0030'},'exact source predicates required')
    for p in pairs:
        require(len(p['cases'])==2 and p['cases'][0]['source_command_hex']==p['cases'][1]['source_command_hex'] and p['cases'][0]['native_result']==p['cases'][1]['native_result'],'predicate operands/results changed')
    ui=controls['relocated_C200_pairs'];require(len(ui)==1 and len(ui[0]['cases'])==2,'C200 source-target pair required')
    for p in ui[0]['cases']:require(p['source_command_hex']=='00c2' and p['native_extent']==2 and p['native_result'][0]==3 and p['source_owned_UI_request_words']==[1,0,13,0,0,0,1] and len(p['source_owned_UI_writes'])==9 and p['all_other4MiB_actor_roster_event_RNG_and_models_exact'] and p['native_presentation_resource_bodies_not_executed'],'C200 source-owned contract differs')
    require(ui[0]['cases'][0]['source_owned_UI_writes']==ui[0]['cases'][1]['source_owned_UI_writes'],'C200 writes differ')
    financial=controls['relocated_financial_boundary_cases'];require([c['input_funds'] for c in financial]==[0,899999,900000,999999,1000000,1000001,2000000],'seven monetary boundary cases required')
    for c in financial:
        v=c['input_funds'];p=c['relocated_payment'];require(c['relocated_source_predicate']['native_result']==[2,0 if v<1000000 else 1 if v==1000000 else 2,0,0,0,0] and p['source_command_hex']=='00a0ffffbdff0191' and p['before_funds']==v and p['after_funds']==max(0,v-900000) and p['all_other4MiB_actor_roster_event_RNG_models_ABI_input_owner_and_output_guards_exact'],'source monetary semantics changed')
    tail=load(doc['termination_proof']);require(len(tail['cases'])==36 and tail['all36_original_parent_VM_tail_cases_return_before_unowned_cache_bytes'] and tail['whole_loader_preserves_post_payload_canaries_instead_of_zeroing_them'] and tail['original_VM_return_address']==0x02023F7C and tail['outer_event_parent_continuation_not_executed'],'in-block original VM termination proof required')
    require((tail['source_insufficient_jump_target'],tail['target_insufficient_jump_target'],tail['source_logical_end'],tail['target_logical_end'])==(970,894,974,898),'source/target terminator distinction differs')
    container=IlnkContainer.parse(source);oldblocks=list(container.blocks);jp=IlnkContainer.parse(japanese).blocks[141];require(len(oldblocks)==336 and len(mapping['blocks'])==1,'one-block source scope required');spec=mapping['blocks'][0];block=oldblocks[141]
    require(spec['block']==141 and sha(block)==spec['source_block_sha256'] and not spec['choice_commands'] and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'],'exact source block/kinds required')
    require(spec['inverse_restoration_recovers_every_original_logical_byte'] and spec['entry_point_offset']==8,'source inverse/entry required')
    rows=doc['records'];require(len(rows)==14 and [r['source_record_index'] for r in rows]==INDICES and Counter(r['editorial_decision'] for r in rows)=={'revise':7,'retain-wording':7},'reviewed speech/decision coverage differs')
    fonts={c['id']:c for c in native['cases']};texts={r['id']:r for r in spec['text_records']};require(set(texts)==set(fonts)=={r['id'] for r in rows},'proof record coverage differs');profile=profile_for(arm,block);patches=[];changes=[]
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B141_layout_v2.py') and sha(Path(doc['native_formatter_module']).read_bytes())==doc['native_formatter_module_sha256'],'approved formatter required')
    for r in rows:
        ident=r['id'];t=texts[ident];at=r['current_reference']['offset'];old=bytes.fromhex(r['current_hex']);raw=bytes.fromhex(r['source_hex']);ja=r['source_reference']['offset']
        require(r['file_path']==PATH and r['block']==141 and all(r['review'].values()),'record source/review differs:'+ident)
        require(block[at:at+len(old)]==old and block[at+len(old)]==0 and jp[ja:ja+len(raw)]==raw and jp[ja+len(raw)]==0,'exact clean/current reference differs:'+ident)
        require(block[at-5:at+1]==jp[ja-5:ja+1]==bytes.fromhex(r['source_complete_preamble_hex']) and raw[0]==r['source_selector'] in [2,9,20,171],'complete static preamble differs:'+ident)
        require(all(raw.count(k.encode())==r['english'].count('{MACRO:'+k+'}') for k in ['FI','FA','FO']),'source macro count differs:'+ident)
        encoded=encode_relocatable_dialogue(raw,r['english'],profile);require(encoded.encoded.hex()==r['compiled_hex']==fonts[ident]['encoded_hex'],'approved compiled prose differs:'+ident)
        for d in encoded.diagnostics:require(d.severity!='error' and (d.severity!='warning' or d.code in r.get('qa_waivers',[]) and r.get('qa_waiver_reason')),'unreviewed encoder finding:'+ident)
        qa=audit_relocatable_dialogue_record(raw,r['english'],profile);require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]) and r.get('qa_waiver_reason'))],'unapproved layout finding:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b'';require(value.hex()==t['target_hex'] and pad==t['parity_space_added'] and b'\0' not in value,'stored target parity/control differs:'+ident)
        patches.append(dict(start=at,end=at+len(old),old=old,value=value));changes.append(dict(id=ident,block=141,old_offset=at,new_offset=t['new_offset'],kind='speech',source_record_index=r['source_record_index'],decision=r['editorial_decision'],stored_target_hex=value.hex()))
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping owned text spans')
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            require(not p['start']<at<p['end'],'unclassified interior reference')
            if at==p['start']:return at+delta
            delta+=len(p['value'])-len(p['old'])
        return at+delta
    end=8+struct.unpack_from('<H',block,4)[0];require(not any(block[end:]),'nonzero source alignment padding');parts=[];last=0
    for p in patches:parts.extend([block[last:p['start']],p['value']]);last=p['end']
    parts.append(block[last:end]);logical=bytearray(b''.join(parts));edges=spec['relative_skip_fixups'];require(len(edges)==13 and len(spec['target_native_skip_cases'])==65 and len(logical)==mapped(end)<0x2400,'complete source relocation required')
    for e in edges:
        a=mapped(e['offset']);target=mapped(e['matched_skip_target']);span=target-a-4;require(a==e['new_offset'] and target==e['new_matched_skip_target'] and span==e['target_span'] and struct.unpack_from('<H',block,e['span_field_offset'])[0]==e['source_span'] and 0<=span<=65535 and span%2==0,'relative source target differs');struct.pack_into('<H',logical,a+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+b'\0'*(-len(logical)%4);require(sha(target)==spec['target_block_sha256'],'complete approved target differs')
    commands=spec['mapped_native_commands'];require(len(commands)==37 and sum(c['word']==0x4000 for c in commands)==14 and sum(c['word']==0xA000 for c in commands)==4 and sum(c['word']==0x630A for c in commands)==1,'complete original command scope required')
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(mapped(a)==b and mapped(a+c['old_native_extent'])-b==c['new_native_extent'],'mapped command boundary differs')
        if c['word']==0x4000:require(block[a:a+6]==target[b:b+6],'complete relocated speech preamble differs')
        elif c['word'] in [0x100,0x200,0x300,0x400]:require(block[a:a+2]==target[b:b+2],'relative opcode differs')
        else:require(block[a:a+c['old_native_extent']]==target[b:b+c['new_native_extent']],'source numeric effect/leaf command differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for e in edges:struct.pack_into('<H',restored,e['new_offset']+2,e['source_span'])
    for p in reversed(patches):a=mapped(p['start']);restored[a:a+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end],'inverse does not recover every predecessor byte');container.blocks[141]=target;result=container.to_bytes();require(sha(result)==config['target_SC2_sha256'],'whole SC2 target differs')
    require([n for n,(a,b) in enumerate(zip(oldblocks,container.blocks,strict=True)) if a!=b]==[141],'unrelated SC2 block changed');image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=config['manuscript'],reference_map=config['reference_map'],changed_records=changes,blocks=[dict(block=141,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),target_bytes=len(target),relative_operands=13,source_commands=37,inverse_restores_every_original_logical_byte=True)],all335_other_SC2_blocks_unchanged=True,source_threshold_gold=1000000,source_payment_gold=900000,all14_speeches13_relative_operands3_predicates_and_original_effects_preserved=True,both_funding_paths_terminate_inside_payload_without_zero_tail_dependency=True,native_code_and123040_staged_payload_unchanged=True)
