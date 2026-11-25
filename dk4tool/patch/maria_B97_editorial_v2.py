"""Atomic clean-source B97 localization;original controls and exact two-page contract stay fixed."""
import json,re,struct
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.maria_B97_profile import profile_for
from dk4tool.dialogue import maria_B97_layout_v2 as codec
from dk4tool.patch.grand_race_menu_release import sha
PATH='/data/SC3.DK4'
CONFIG='translations/maria_B97_editorial_release_v1.json'
INDICES=[5,9,13,16,19,22,26,30,33,37,40,43,46,49,53,57,61,64,68,72,75,78,81,85,88,92,96,100,103,107,114,117]
FLAGS=['external_references_complete','preserve_record_parity','all40_source_commands32_complete_preambles8_exact_leaves_verified','all32_final_stored_targets128_macro_cases_and_native_planes_verified','one_source_FO31_progressive_one_FE_and_source72_two_pages_preserved','all302_other_SC3_blocks_every_other_file_component_and_original_B33_exact','exact_inverse_recovers_all_predecessor_bytes_including_tail','source_EV3_event97_action98_and_original_block_index_loader_bound','focused_actual_B97_content_in_B33_fixture_approved','source_event97_natural_eligibility_and_earned_inventory_not_claimed','no_open_translation_specific_display_or_control_finding','final_RGB_actor_and_PRNG_inequality_disclosed']

def load(path):return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Maria B97 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf.get('format')=='dk4-maria-B97-editorial-release-v1','unknown config format')
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'reviewed dependency differs:'+path)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC3_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC3_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'current runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM differs')
    clean=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(clean)==conf['clean_SC3_sha256'],'clean Japanese script differs')
    doc,mapping=load(conf['manuscript']),load(conf['reference_map']);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and not doc['formatting_review_pending'],'five-gate editorial manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(mapping['format']=='dk4-maria-B97-source-relocation-map-v1' and mapping['file_path']==PATH and mapping['block']==97 and mapping['entry_point_offset']==8,'map scope differs')
    require(mapping['required_runtime_ARM9_sha256']==sha(arm) and mapping['source_SC3_sha256']==sha(source) and mapping['target_SC3_sha256']==conf['target_SC3_sha256'] and mapping['relative_skip_fixups']==[],'map runtime/relatives differ')
    for flag in FLAGS:require(mapping.get(flag) is True,'missing map gate:'+flag)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/maria_B97_layout_v2.py') and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/maria_B97_profile.py'),'unscoped layout')
    proofkeys=['native_font_proof','final_padding_proof','loader_proof','reference_census_proof','termination_decode_proof','relocated_control_proof','representative_proof','source_nameplate_consumer_proof','native_review_proof','actor_voice_contract','item_terminology_reconciliation','source_entry_proof']
    for key in proofkeys:require(sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],'proof binding differs:'+key)
    native,stored,loader,census,ends,controls,actual,names,review,voices,terms,entry=[load(doc[k]) for k in proofkeys]
    require(len(native['cases'])==32 and native['current_original_macro_alignment_calls']==256 and native['complete_one_page_progressive_planes']==30 and native['complete_FE_logical_and_physical_planes']==1,'native consumer coverage differs')
    require(len(native['negative_controls'])==24 and all(r['rejected'] for r in native['negative_controls']) and len(review['formatter_negatives'])==42 and all(r['rejected'] for r in review['formatter_negatives']),'native rejection checks incomplete')
    require(len(review['viewed_sheets'])==5 and all(r['viewed_in_full_current_turn'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in review['viewed_sheets']),'native sheet review differs')
    require(len(stored['final_stored_cases'])==32 and stored['stored_alignment_cases']==128 and stored['fresh_parity_alignment_cases']==72 and stored['exact_byte_reused_alignment_cases']==56 and stored['source72_actual_page_tail_guard_and_terminal_space_exact'],'stored targets incomplete')
    require(loader['all303_whole_blocks_and606_modes_each_pass'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'] and loader['original_EV3_actions_select_by_block_index_without_interior_byte_offset'],'original loaders/entry required')
    require(len(census['mapped_commands'])==40 and census['all40_complete_preambles_and8_exact_leaves_preserved'] and census['only_original24070_interpreter_call_and_no_literal_alias'],'entry census differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset'],r['logical_end']) for r in ends['cases']]==[('current',1898,1902),('research',2042,2046)],'guarded ends differ')
    require(len(controls['relocated_dispatch_cases'])==32 and len(controls['all8_source_current_target_exact_leaves'])==8 and len(controls['target_item_hide_pairs'])==2 and len(controls['target_setup_and_two_effect_structural_pairs'])==4,'relocated controls differ')
    require(controls['one_FE_null_actor_and31_original_progressive_consumers_preserved'] and controls['one_source_FO_default_Li_Clan_preserved'],'FE/FO scope differs')
    picture,hide=controls['target_item_hide_pairs'];pc=picture['target_case']['original_picture_boundary_calls'];hc=hide['target_case']['original_picture_boundary_calls'];oldhide=hide['original_current_case_reused']['original_picture_boundary_calls']
    require(len(pc)==len(hc)==len(oldhide)==1 and pc[0]['descriptor']==[0,176,1,5] and pc[0]['layout']==[2,0,0] and pc[0]['address']==0x02028A64,'original tablet descriptor differs')
    require(hide['old_offset']==1896 and hide['new_offset']==2040 and hc[0]['address']==0x02028A8C and hc[0]['args'][:3]==oldhide[0]['args'][:3] and oldhide[0]['args'][3]==0x02660000+1896 and hc[0]['args'][3]==0x02660000+2040,'original hide retained cursor relocation differs')
    require(names['progressive_nameplate_values']=={'3':'Maria Li','10':'Xien Yan','180':'Bandit'} and names['full_catalogue_values']=={'3':'Maria Huamei Li','10':'Xien Yan','180':'Bandit'} and names['actual_captain3_actor_object_selected_instead_of_static_copy'],'bound names/captain object differ')
    require({r['actor_ID']:r['original_voice_class'] for r in voices['catalog']['rows'] if r['actor_ID'] in [3,10,180]}=={3:3,10:5,180:0},'source voices differ')
    require(terms['approved_city']=='Sao Jorge' and terms['chosen_full_Proof_term']=='Proof of Conquest' and terms['source_FO_measured_default']=='Li Clan' and terms['source_tablet_generic_question_not_expanded_to_catalogue_title'],'source terms differ')
    require(entry['selected_B97_source_event']['event_ID']==97 and entry['selected_B97_source_event']['action_index']==98 and entry['original_source_EV3_and_action_table_exact'],'original source event binding differs')
    require(actual['complete_actual_panel_pages']==33 and not actual['failures'] and len(actual['paired_nontext_samples'])==327 and not actual['nontext_differences'],'actual coverage differs')
    require(len(actual['versions'])==2 and [len(v['command_pairs']) for v in actual['versions']]==[40,40] and [len(v['speech_intervals']) for v in actual['versions']]==[32,32] and [v['normal_end_frame'] for v in actual['versions']]==[23222,23822],'actual complete paths differ')
    page=actual['source72_page_boundary'];require(page['original_single_command_preserved'] and page['first_four_rows_match_font_matrix'] and page['original_A_event']==dict(start=15401,duration=8,buttons=['A']) and page['original_continuation_first_row_indent_px']==6 and page['full_wording_macro_controls_and_encoded_target_unchanged'],'two-page original A/guard contract differs')
    require(actual['B97_content_in_B33_entry_not_natural_event97_earned_recruitment_or_earned_tablet'] and not actual['final31000_whole_RGB_equal'] and actual['no_causal_PRNG_future_world_or_full_RAM_equivalence_claim'],'actual fixture/state disclosure differs')
    require([actual['final_state_observations'][k]['original_PRNG_word02168EB8'] for k in ['clean_Japanese','reviewed_English']]==[347786248,2289475870],'measured RNG inequality differs')
    actualapproval=load(conf['actual_approval']);require(actualapproval['manuscript']==doc['previous_manuscript'] and actualapproval['source72_current_original_A_continuation_complete_with_one_cell_indent'] and actualapproval['paired_nontext_differences']==0 and len(actualapproval['measured_timing_differences'])==34,'viewed actual approval differs')
    require(len(actualapproval['all_six_actual_sheets_viewed'])==6 and all(r['viewed_in_full_current_turn'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in actualapproval['all_six_actual_sheets_viewed']),'actual sheets not viewed')
    container=IlnkContainer.parse(source);oldblocks=list(container.blocks);block=oldblocks[97];jp=IlnkContainer.parse(clean).blocks[97]
    require(len(oldblocks)==303 and sha(block)==mapping['source_block_sha256'] and sha(jp)==mapping['clean_block_sha256'] and block[:4]==jp[:4]==b'CS\1\1','whole source block differs')
    rows=doc['records'];require([r['source_record_index'] for r in rows]==INDICES and len({r['id'] for r in rows})==32 and Counter(r['editorial_decision'] for r in rows)=={'revise':23,'retain-wording':9},'complete decisions differ')
    require(Counter(r['kind'] for r in rows)=={'progressive':31,'system-FE':1} and {r['source_selector'] for r in rows}=={3,10,180,254},'source consumer scope differs')
    fonts={r['id']:r for r in native['cases']};texts={r['id']:r for r in mapping['text_records']};dispatch={r['id']:r for r in controls['relocated_dispatch_cases']};finals={r['id']:r for r in stored['final_stored_cases']};require(set(fonts)==set(texts)==set(dispatch)==set(finals)=={r['id'] for r in rows},'reference proof keys differ')
    commands=mapping['mapped_native_commands'];require(len(commands)==40 and [c['word'] for c in commands if c['word']!=0x4000]==[0x6000,0x4620,0x633E,0xA000,0x4820,0xA000,0x4700,0],'all source commands required')
    byat={c['old_offset']:c for c in commands};patches=[];changes=[];macros=[]
    for r in rows:
        ident=r['id'];ref=texts[ident];raw,old=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex']);at=r['current_reference']['header_offset'];off=r['current_reference']['offset'];sa=r['source_reference']['offset'];cmd=byat[at];selector=r['source_selector'];paged=r['source_record_index']==72;fe=r['kind']=='system-FE'
        require(ref['new_command_offset']==cmd['new_offset'] and ref['new_text_offset']==ref['new_offset']==cmd['new_offset']+5 and ref['new_record_index']==ref['record_index']==r['current_record_index'],'exact relocated record reference differs:'+ident)
        require(r['current_reference']['bytes']==len(old) and r['source_reference']['bytes']==len(raw) and r['source_reference']['header_offset']+5==sa,'complete source/current reference extents differ:'+ident)
        require(r['file_path']==PATH and r['block']==97 and selector==raw[0]==old[0] and (selector==254)==fe and r['actual_B33_content_fixture_observed'],'individual source scope differs:'+ident)
        require(cmd['word']==0x4000 and off==at+5 and block[off:off+len(old)+1]==old+b'\0' and jp[sa:sa+len(raw)+1]==raw+b'\0','source/current references differ:'+ident)
        require(block[at:at+6]==jp[sa-5:sa+1]==bytes.fromhex(r['source_complete_preamble_hex']) and block[:off].count(b'\0')==r['record_index']==ref['record_index'],'complete preamble/index differs:'+ident)
        require(dispatch[ident]['resolved_actor_ID']==(None if fe else selector) and dispatch[ident]['registered_catalog_match'] is None,'target dispatch differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',r['english'])];require(sm==tm,'runtime substitution/order differs:'+ident);macros+=sm
        consumer='FE-paper' if fe else ('progressive-two-page' if paged else 'progressive');profile=profile_for(arm,block,consumer,raw);encoded=codec.encode_relocatable_dialogue(raw,r['english'],profile);case=fonts[ident]
        require(encoded.encoded.hex()==r['compiled_hex']==case['encoded_hex'],'compiled wording differs:'+ident)
        qa=codec.audit_relocatable_dialogue_record(raw,r['english'],profile)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and r.get('qa_waivers')==['line-break-count'] and r.get('qa_waiver_reason'))],'unapproved layout finding:'+ident)
        require(case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and_current_width_bounds_exact'] and case['pages_projected']==(2 if paged else 1),'complete native glyph/bounds/page proof differs:'+ident)
        require(sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'macro alignment proof differs:'+ident)
        if fe:require(all(c['null_source_actor'] for p in case['current_native_macro_pipelines'] for c in p['cases']),'FE actor differs')
        if paged:require(encoded.encoded.count(b'\n')==4 and encoded.encoded[1:].split(b'\n')[4]+(b' ' if ref['parity_space_added'] else b'')==bytes.fromhex(page['continuation_input_hex']),'exact continuation bytes differ')
        if r['editorial_decision']=='retain-wording':require(r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification'],'unjustified retention:'+ident)
        value=encoded.encoded;parity=len(value[1:])%2!=len(old[1:])%2;value+=b' ' if parity else b''
        require(value.hex()==ref['stored_text_hex'] and parity==ref['parity_space_added'] and ref['old_offset']==off and ref['old_length']==len(old) and ref['new_length']==len(value),'stored target/reference differs:'+ident)
        final=finals[ident];expected=value[1:].replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan');alignments=final['macro_alignment_cases']['cases']
        require(final['stored_text_hex']==value.hex() and final['compiled_text_hex']==encoded.encoded.hex() and final['parity_space_added']==parity and len(alignments)==4 and all(a['output_hex']==expected.hex() for a in alignments),'final stored native alignment differs:'+ident)
        command=block[at:at+5]+value+b'\0';command+=bytes(-len(command)%2);patches.append(dict(start=at,end=at+cmd['old_extent'],old=block[at:at+cmd['old_extent']],value=command))
        changes.append(dict(id=ident,block=97,old_offset=off,new_offset=ref['new_text_offset'],source_record_index=r['source_record_index'],source_selector=selector,decision=r['editorial_decision'],kind=r['kind'],stored_target_hex=value.hex()))
    require(macros==[b'FO'],'one source FO required');patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'overlapping owned spans')
    end=8+struct.unpack_from('<H',block,4)[0];require(end==1902 and len(block)==1904 and block[end:]==bytes(2),'source logical end/tail differs')
    def mapped(at):
        delta=0
        for p in patches:
            require(not p['start']<at<p['end'],'unclassified interior reference')
            if at>=p['end']:delta+=len(p['value'])-len(p['old'])
        return at+delta
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:end]);logical=bytearray(b''.join(pieces));require(len(logical)==mapped(end)==2046 and len(logical)<0x2400,'logical target size differs');struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(sha(target)==mapping['target_block_sha256'] and len(target)==2048,'complete reviewed target differs')
    for c in commands:
        a,b=c['old_offset'],c['new_offset'];require(mapped(a)==b and mapped(a+c['old_extent'])-b==c['new_extent'],'mapped command boundary differs')
        require(block[a:a+6]==target[b:b+6] if c['word']==0x4000 else block[a:a+c['old_extent']]==target[b:b+c['new_extent']],'original source preamble/control changed')
    restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    require(bytes(restored)+block[end:]==block,'inverse does not recover every predecessor byte/tail')
    container.blocks[97]=target;result=container.to_bytes();require(sha(result)==conf['target_SC3_sha256'] and [i for i,(a,b) in enumerate(zip(oldblocks,container.blocks,strict=True)) if a!=b]==[97],'unrelated script bytes changed')
    image.replace_file(PATH,result)
    return dict(source_SC3_sha256=sha(source),target_SC3_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),manuscript=conf['manuscript'],reference_map=conf['reference_map'],changed_records=changes,blocks=[dict(block=97,source_bytes=1904,target_bytes=2048,source_logical_end=1902,target_logical_end=2046,source_sha256=sha(block),target_sha256=sha(target),source_commands=40,speeches=32,nonspeech_leaves=8,inverse_restores_every_predecessor_byte_and_tail=True)],only_SC3_B97_changed=True,all302_other_SC3_blocks_and_original_B33_exact=True,one_FO_FE_and_two_page_A_guard_contract_preserved=True,source97_natural_activation_and_earned_inventory_not_claimed=True,postscene_RGB_actor_PRNG_inequality_disclosed=True,native_code_font_graphics_and123040_pool_unchanged=True)
