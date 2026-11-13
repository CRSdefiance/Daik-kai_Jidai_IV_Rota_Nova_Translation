"""Atomic, uniquely owned actor17 additional-name typography; no global normalization."""
import json,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
PATH='/__arm9__.bin';CONFIG='translations/Al_Ferid_name_release_v1.json'
SOURCE='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
TARGET='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
BASE,POOL,TABLE=0x02000000,0x02387A20,0x120B80
def load(p):return json.loads(Path(p).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('Al Ferid name '+message)
def cstring(data,at):
    require(0<=at<len(data),'string address');end=data.find(b'\0',at);require(end>=at,'complete string');return data[at:end+1]
def transform(arm,clean,row):
    require(sha(arm)==SOURCE,'source ARM9')
    require(row['id']=='ACTOR_017_ADDITIONAL_NAME_TYPOGRAPHY' and row['actor_ID']==17 and row['field_column']==8,'exact identity/field')
    require((row['source_Japanese'],row['current_English'],row['english'],row['editorial_decision'],row['target_locale'])==('フェリド','Ｆerid','Ferid','revise','en-US'),'source/current/target wording')
    require(row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=True),'five gates')
    require(all(row[k] for k in ['source_meaning','speaker','context','localization_note','formatting_reason']),'context notes')
    require(row['new_name_completion_credit']==row['new_dialogue_completion_credit']==0,'no duplicate credit')
    code=MainCodeFile(arm,BASE);require(len(code.sections)==5 and code.sections[3].ramAddress==0x023A7200,'section layout')
    payload=bytes(code.sections[3].data[:-48]);require(len(payload)==123264 and arm.count(payload)==1,'unique complete payload')
    raw_at=arm.index(payload);field=TABLE+17*32+8;pointer=struct.unpack_from('<I',arm,field)[0];offset=pointer-POOL;at=raw_at+offset
    old,new=bytes.fromhex('82656572696400'),b'Ferid\0\0'
    require((field,pointer,offset,at)==(1183144,37256524,812,1518776) and arm[at:at+7]==old and arm.count(old)==1,'exact seven-byte slot')
    source=row['source_reference'];sp=struct.unpack_from('<I',clean,field)[0]
    require(source==dict(source_file=PATH,pointer_field=field,pointer=sp,storage_offset=sp-BASE,terminated_hex=cstring(clean,sp-BASE).hex()) and source['terminated_hex']=='83748346838a836800','exact clean reference')
    require(row['current_reference']==dict(source_file=PATH,pointer_field=field,runtime_pointer=pointer,staged_payload_offset=offset,file_offset=at,terminated_hex=old.hex()),'exact current reference')
    parts=row['all_three_source_current_name_fields'];require(len(parts)==3,'three name fields')
    for delta,part,jp,en in zip([0,4,8],parts,['アル','シン','フェリド'],['Al','Shin','Ｆerid'],strict=True):
        f=TABLE+17*32+delta;cp=struct.unpack_from('<I',arm,f)[0];sp=struct.unpack_from('<I',clean,f)[0];storage=raw_at+cp-POOL if POOL<=cp<POOL+len(payload) else cp-BASE
        require(part['column']==delta and part['pointer_field']==f and part['source_pointer']==sp and part['source_storage_offset']==sp-BASE and part['source_terminated_hex']==cstring(clean,sp-BASE).hex() and part['Japanese']==jp,'clean field ownership')
        require(part['current_pointer']==cp and part['current_storage_offset']==storage and part['current_terminated_hex']==cstring(arm,storage).hex() and part['current_English']==en,'current field ownership')
    hits=[i for i in range(len(arm)-3) if arm[i:i+4]==struct.pack('<I',pointer)];require(hits==[field],'raw pointer byte census')
    fields=[struct.unpack_from('<3I',arm,TABLE+i*32) for i in range(207)];aliases=[(i,d) for i,ps in enumerate(fields) for d,p in zip([0,4,8],ps,strict=True) if pointer<=p<pointer+7];require(aliases==[(17,8)],'all621 fields/no interior aliases')
    target=arm[:at]+new+arm[at+7:];parsed=MainCodeFile(target,BASE)
    require(sha(target)==TARGET and len(target)==len(arm),'exact approved target')
    require([(s.ramAddress,s.bssSize,len(s.data)) for s in code.sections]==[(s.ramAddress,s.bssSize,len(s.data)) for s in parsed.sections],'section extents/BSS')
    require([i for i,(a,b) in enumerate(zip(code.sections,parsed.sections,strict=True)) if bytes(a.data)!=bytes(b.data)]==[3],'unowned code/font sections')
    require(bytes(code.sections[3].data[-48:])==bytes(parsed.sections[3].data[-48:]) and cache_plan(arm)==cache_plan(target),'copy/cache wrapper')
    require([struct.unpack_from('<3I',target,TABLE+i*32) for i in range(207)]==fields,'all621 pointers')
    require(target[:at]+old+target[at+7:]==arm and cstring(target,at)==b'Ferid\0' and target[at+6]==arm[at+6]==0,'inverse/tail')
    return target,dict(actor_ID=17,field_column=8,pointer_field=field,runtime_pointer=pointer,staged_payload_offset=offset,file_offset=at,old_complete_slot_hex=old.hex(),target_complete_slot_hex=new.hex(),changed_byte_offsets=[i for i,(a,b) in enumerate(zip(arm,target,strict=True)) if a!=b],raw_pointer_occurrences=hits,all621_fields_exact=True,all_unowned_bytes_code_fonts_sections_BSS_cache_copy_and123264_extent_exact=True,full_inverse=True)
def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']=='dk4-Al-Ferid-name-release-v1','config format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency:'+p)
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['source_files'] and {p:sha(v) for p,v in image.iter_components()}==conf['source_components'],'complete cumulative input')
    require(sha(baseline.read_file(PATH))==conf['canonical_ARM9_sha256'],'canonical ARM9')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','clean ROM');clean=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(clean)==conf['clean_ARM9_sha256'],'clean ARM9')
    doc,seal,proof=[load(conf[k]) for k in ['manuscript','approval','native_proof']]
    require(doc['format']=='dk4-source-bound-additional-name-typography-manuscript-v1' and doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','manuscript policy')
    for k in ['all_five_individual_name_review_gates_true','all621_name_table_pointers_and_cache_plan_unchanged','full_catalogue_UI_unvisited','all207_name_role_alias_and_earlier_consumer_review_open']:require(doc[k] is True,'manuscript scope:'+k)
    require(len(doc['records'])==1 and not doc['full_goal_complete'] and doc['exact_name_pointer_occurrences']==[1183144],'one name/no goal closure')
    require(seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['native_target_proof_sha256']==sha(Path(conf['native_proof']).read_bytes())==doc['native_target_proof_sha256'],'sealed assets')
    for k in ['one_additional_name_field_typography_approved_without_new_spelling','all5_review_gates_true','original_full_catalogue_getter_corrected_not_actual_full_catalogue_UI','progressive_Al_Shin_and_all_other_fields_pointers_cache_code_fonts_unchanged','no_global_name_normalization_or_207_queue_closure']:require(seal[k] is True,'approval:'+k)
    require(not seal['visual_review_pending'] and seal['new_review_credit']==0 and seal['exact_raw_pointer_hits']==[1183144],'visual/credit/pointer scope')
    require(proof['source_ARM9_sha256']==doc['current_ARM9_sha256']==SOURCE and proof['target_ARM9_sha256']==doc['target_ARM9_sha256']==TARGET,'native runtime hashes')
    for k in ['all9_whole_RGB_frames_match_V6488','actual_target_staged123264_payload_and_each_executed_instruction_bound','all_pointer_actor_rows_code_font_other_files_and_components_exact_except_five_name_data_bytes','full_catalogue_getter_returns_corrected_Al_Ferid_Shin','progressive_Al_Shin_and_both_Lil_Argot_consumers_unchanged','only_ASCII_typography_correction_no_new_spelling_rank_relationship_or_biography','full_catalogue_UI_unvisited_not_claimed_as_actual_full_name_display','source_name_queue207_and_all_other_alias_consumers_open']:require(proof[k] is True,'native scope:'+k)
    require(proof['name_literal_alignment_cases']==32 and len(proof['actual_target_opening_framebuffer_pairs'])==9 and len(proof['target_native_name_planes'])==3,'native counts')
    require(all(r['complete_leading_internal_final_ASCII_glyphs_in_bounds_one_row'] and r['same_pixels_as_previously_reviewed_literal'] for r in proof['target_native_name_planes']),'complete native planes')
    getters=proof['native_four_name_getters'];require(getters['all_four_original_consumers_and_owned_or_readonly_memory_paths_exact'] and [(r['actor_ID'],r['consumer'],r['text']) for r in getters['rows']]==[(2,'progressive-nameplate','Lil Argot'),(2,'full-catalogue','Lil Argot'),(17,'progressive-nameplate','Al Shin'),(17,'full-catalogue','Al Ferid Shin')],'four source getters')
    compatibility=load(conf['B210_compatibility']);require(compatibility['all10_entire_dispatch_results_identical'] and compatibility['all467_catalogue_rows_and_native_calls_bound'] and compatibility['only_adapter_hash_guard_updated_no_address_or_instruction_change'] and compatibility['exact_corrected_name_ARM9_sha256']==TARGET and len(compatibility['cases'])==10,'post-name B210 dispatch compatibility')
    arm=image.read_file(PATH);target,plan=transform(arm,clean,doc['records'][0]);require(target==NdsImage.open(doc['approved_target_research_ROM']).read_file(PATH) and sha(Path(doc['approved_target_research_ROM']).read_bytes())==doc['approved_target_research_ROM_sha256'],'approved isolated target')
    report=dict(manuscript=conf['manuscript'],source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),changed_records=[dict(id=doc['records'][0]['id'],actor_ID=17,before='Ｆerid',after='Ferid')],data_plan=plan,no_duplicate_dialogue_or_name_completion_credit=True,full_catalogue_UI_unvisited=True,all207_name_role_alias_consumers_and_full_editorial_goal_open=True,full_goal_complete=False)
    image.replace_file(PATH,target);return report
