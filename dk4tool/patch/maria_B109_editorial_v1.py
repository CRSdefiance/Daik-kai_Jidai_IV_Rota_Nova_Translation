"""Source/runtime locked26 Maria speeches and the original packed UI prefix."""
import json
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.maria_B109_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.maria_B109_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
PATH='/data/SC3.DK4'
CONFIG='translations/maria_B109_editorial_release_v1.json'
SOURCE_PREFIX=bytes.fromhex('00450000008084468380')
BAD_PREFIX=bytes.fromhex('00450000004a616d2020')
EXPECTED_INDICES=[8,12,15,18,25,28,31,35,38,42,45,49,53,56,59,62,65,68,72,76,80,83,87,91,95,99]
def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def require(ok,reason):
    if not ok:raise ValueError('Maria B109 '+reason)
def apply_release(image,baseline,config_path=CONFIG):
    config=load(config_path);require(config.get('format')=='dk4-maria-B109-editorial-release-v1','unknown release format')
    for p,d in config['dependencies'].items():require(sha(Path(p).read_bytes())==d,'reviewed dependency differs:'+p)
    arm=image.read_file('/__arm9__.bin');source=image.read_file(PATH)
    require(sha(arm)==config['required_runtime_arm9_sha256'],'native runtime differs')
    require(sha(source)==config['source_SC3_sha256'] and sha(baseline.read_file(PATH))==config['canonical_SC3_sha256'],'current/canonical source differs')
    require(sha(Path(config['clean_ROM']).read_bytes())==config['clean_ROM_sha256'],'clean ROM differs')
    japanese=NdsImage.open(config['clean_ROM']).read_file(PATH);require(sha(japanese)==config['clean_SC3_sha256'],'clean Japanese script differs')
    doc,mapping=map(load,[config['manuscript'],config['reference_map']]);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and doc['formatting_review_pending'] is False,'editorial policy/gates differ')
    require(doc['reference_map']==config['reference_map'] and sha(Path(doc['reference_map']).read_bytes())==doc['reference_map_sha256'],'approved map differs')
    require(doc['required_runtime_ARM9_sha256']==sha(arm),'reviewed runtime differs')
    require(mapping['format']=='dk4-maria-B109-source-relocation-map-v1' and mapping['file_path']==PATH and mapping['block']==109,'map scope differs')
    require(mapping['required_runtime_ARM9_sha256']==sha(arm) and mapping['source_SC3_sha256']==sha(source) and mapping['target_SC3_sha256']==config['target_SC3_sha256'],'map runtime/source/target differs')
    for key in ['external_references_complete','preserve_record_parity','all34_source_command_boundaries26_complete_preambles8_source_non_speech_commands_verified','all26_final_targets104_macro_cases_and_independent_native_planes_verified','source_prefix_numeric_not_name_text','all302_other_SC3_blocks_every_other_file_component_exact','exact_inverse_recovers_predecessor_including_bad_prefix','source_EV3_event109_action110_dependency_and_original_loader_bound','focused_actual_B109_content_in_B33_entry_fixture_approved','source_event109_natural_activation_not_claimed','source_English_immediate_normal_Hangzhou_return_equal','no_open_translation_specific_display_or_control_finding']:
        require(mapping.get(key) is True,'missing reference gate:'+key)
    require(mapping['entry_point_offset']==8 and mapping['relative_skip_fixups']==[],'entry/relative scope differs')
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/maria_B109_layout_v2.py') and sha(Path(doc['native_formatter_module']).read_bytes())==doc['native_formatter_module_sha256'],'scoped formatter differs')
    native=load(doc['native_font_proof']);stored=load(doc['final_padding_proof']);ref=load(doc['relocated_control_proof']);actual=load(doc['representative_proof'])
    for key in ['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof']:
        require(sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],'reviewed proof binding differs:'+key)
    require(doc['final_padding_proof']==mapping['stored_target_proof'] and doc['relocated_control_proof']==mapping['reference_proof'] and doc['representative_proof']==mapping['actual_display_proof'],'map/proof paths differ')
    require(native['all26_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls']==208 and len(native['cases'])==26,'complete native planes/macros required')
    require(len(native['source_bound_formatter_negatives'])==14 and len(native['source_consumer_negative_controls'])==17 and all(x['rejected'] for x in native['source_bound_formatter_negatives']+native['source_consumer_negative_controls']),'native negative guards required')
    require(native['wordless_three_periods_complete_at_origin'] and native['all5_actual_English_panel_sheets_and_setup_transition_sheet_viewed'],'native visual review required')
    for s in native['review_sheets']:require(sha(Path(s['path']).read_bytes())==s['sha256'],'viewed sheet differs')
    require(stored['stored_target_macro_alignment_cases']==104 and len(stored['stored_target_cases'])==26,'stored target proof incomplete')
    require(ref['all303_loader_cache_hits606_parent_modes_each_image'] and ref['all26_stored_targets_reach_expected_original_progressive_consumer'],'loader/dispatch approval required')
    c=ref['relocated_C200'];require(ref['C200_source_owned9_writes_and_Maria_index54_preserved'] and c['source_owned_UI_request_words']==[1,54,13,0,0,0,1] and len(c['source_owned_UI_writes'])==9 and c['all_other4MiB_actor_roster_event_RNG_and_models_exact'],'source-owned Maria C200 request differs')
    require(actual['complete_matching_panels']==actual['complete_matching_holds']==26 and not actual['unmatched_capture_planes'],'complete actual content planes required')
    require(actual['B109_content_in_B33_entry_fixture_only'] and actual['source_event109_not_selected_or_earned'],'actual fixture scope differs')
    returns=native['source_and_English_immediate_normal_Hangzhou_return_exact'];require(len(returns)==2 and all(r['normal_Hangzhou_frame']==20200 and r['viewed'] for r in returns) and returns[0]['capture_sha256']==returns[1]['capture_sha256'],'immediate source/English normal return required')
    container=IlnkContainer.parse(source);oldblocks=list(container.blocks);block=container.blocks[109];jp=IlnkContainer.parse(japanese).blocks[109]
    require(len(oldblocks)==303 and sha(block)==mapping['source_block_sha256'] and sha(jp)==mapping['clean_block_sha256'],'whole block source lock differs')
    prefix=mapping['source_owned_control_repair'];require(prefix==dict(offset=8,bytes=10,before=BAD_PREFIX.hex(),after=SOURCE_PREFIX.hex(),five_physically_changed_byte_offsets=[13,14,15,16,17]),'source-owned numeric repair span differs')
    require(block[8:18]==BAD_PREFIX and jp[8:18]==SOURCE_PREFIX and block[:4]==jp[:4]==b'CS\1\1','CS0101/source numeric prefix differs')
    rows=doc['records'];require(len(rows)==26 and [r['source_record_index'] for r in rows]==EXPECTED_INDICES,'complete source speech scope differs')
    require(Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':10},'reviewed decisions differ')
    fonts={r['id']:r for r in native['cases']};texts={r['id']:r for r in mapping['text_records']};require(set(fonts)==set(texts)=={r['id'] for r in rows},'proof record coverage differs')
    commands=mapping['mapped_native_commands'];require(len(commands)==34 and sum(c['word']==0x4000 for c in commands)==26 and [c['word'] for c in commands if c['word']!=0x4000]==[0x4500,0x4684,0x6000,0x4621,0x6100,0x2000,0xC200,0],'source control command scope differs')
    byat={c['old_offset']:c for c in commands};profile=profile_for(arm,block);patches=[];changes=[]
    for r in rows:
        ident=r['id'];t=texts[ident];at=r['current_reference']['header_offset'];offset=r['current_reference']['offset'];raw=bytes.fromhex(r['source_hex']);old=bytes.fromhex(r['current_hex']);cmd=byat[at]
        require(r['file_path']==PATH and r['block']==109 and all(r['review'].values()),'record scope/review differs:'+ident)
        require(r['source_selector'] in [3,11,21,74] and raw[0]==old[0]==r['source_selector'],'static source selector differs:'+ident)
        require(cmd['word']==0x4000 and offset==at+5 and block[offset:offset+len(old)]==old and block[offset+len(old)]==0,'current exact reference differs:'+ident)
        ja=r['source_reference']['header_offset'];jo=r['source_reference']['offset'];require(jo==ja+5 and jp[jo:jo+len(raw)]==raw and jp[jo+len(raw)]==0,'clean exact reference differs:'+ident)
        require(block[at:at+6]==jp[ja:ja+6]==bytes.fromhex(r['source_complete_preamble_hex']),'complete presentation preamble differs:'+ident)
        require(all(raw.count(k.encode())==r['english'].count('{MACRO:'+k+'}')==0 for k in ['FI','FA','FO']),'source macro scope differs:'+ident)
        encoded=encode_relocatable_dialogue(raw,r['english'],profile);require(encoded.encoded.hex()==r['compiled_hex']==fonts[ident]['encoded_hex'],'reviewed compiled prose differs:'+ident)
        qa=audit_relocatable_dialogue_record(raw,r['english'],profile)
        for d in encoded.diagnostics:
            require(d.severity!='error' and (d.severity!='warning' or d.code in r.get('qa_waivers',[]) and r.get('qa_waiver_reason')),'unreviewed encoder finding:'+ident)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]) and r.get('qa_waiver_reason'))],'unreviewed layout finding:'+ident)
        require(encoded.encoded[0]==raw[0] and b'\0' not in encoded.encoded,'selector/NUL differs:'+ident)
        added=len(encoded.encoded[1:])%2!=len(old[1:])%2;value=encoded.encoded+(b' ' if added else b'')
        require(value.hex()==t['stored_text_hex'] and added==t['parity_space_added'],'stored target parity differs:'+ident)
        target=block[at:at+5]+value+b'\0';target+=b'\0'*(-len(target)%2)
        patches.append(dict(start=at,end=at+cmd['old_extent'],old=block[at:at+cmd['old_extent']],value=target))
        changes.append(dict(id=ident,block=109,old_offset=offset,new_offset=t['new_text_offset'],source_record_index=r['source_record_index'],source_selector=raw[0],decision=r['editorial_decision'],kind='speech',stored_target_hex=value.hex()))
    require(bytes.fromhex(texts['DK4_MES_B109_R0068']['stored_text_hex']).rstrip(b' ')==b'\3...','wordless source reaction differs')
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping owned spans')
    end=8+struct.unpack_from('<H',block,4)[0];require(not any(block[end:]),'nonzero unowned suffix')
    def mapped(at):
        delta=0
        for p in patches:
            require(not p['start']<at<p['end'],'unclassified interior reference')
            if at>=p['end']:delta+=len(p['value'])-len(p['old'])
        return at+delta
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));logical[8:18]=SOURCE_PREFIX
    require(len(logical)==mapped(end)<0x2400,'logical block size differs');struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+b'\0'*(-len(logical)%4)
    require(sha(target)==mapping['target_block_sha256'],'complete reviewed target differs')
    repaired=bytearray(block);repaired[8:18]=SOURCE_PREFIX
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(mapped(a)==b and mapped(a+c['old_extent'])-b==c['new_extent'],'mapped command boundary differs')
        require(repaired[a:a+6]==target[b:b+6] if c['word']==0x4000 else repaired[a:a+c['old_extent']]==target[b:b+c['new_extent']],'source command/preamble differs')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8);restored[8:18]=BAD_PREFIX
    for p in reversed(patches):a=mapped(p['start']);restored[a:a+len(p['value'])]=p['old']
    require(bytes(restored)==block[:end],'inverse does not restore all predecessor bytes')
    container.blocks[109]=target;result=container.to_bytes();require(sha(result)==config['target_SC3_sha256'],'complete SC3 target differs')
    require([n for n,(a,b) in enumerate(zip(oldblocks,container.blocks,strict=True)) if a!=b]==[109],'unrelated block changed')
    image.replace_file(PATH,result)
    return dict(source_SC3_sha256=sha(source),target_SC3_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=config['manuscript'],reference_map=config['reference_map'],changed_records=changes,blocks=[dict(block=109,source_bytes=len(block),target_bytes=len(target),source_sha256=sha(block),target_sha256=sha(target),source_commands=34,speeches=26,source_non_speech_commands=8,inverse_restores_every_predecessor_byte=True)],source_owned_numeric_prefix_repair=prefix,only_SC3_B109_changed=True,all302_other_SC3_blocks_unchanged=True,source_restored_UI_prefix_actual_content_tested_in_B33_entry=True,source_event109_not_selected_or_earned=True,native_code_and123040_staged_payload_unchanged=True)
