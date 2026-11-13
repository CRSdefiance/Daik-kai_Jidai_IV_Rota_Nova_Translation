"""Atomic one-message formatting revisit after the complete V4966 stack."""
import json
from pathlib import Path
from dk4tool.dialogue.earlier_market_letters_reflow_v2 import compile_letter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries

PATH='/COMMON/MESFILE.DK4'
CONFIG='translations/earlier775_reflow_release_v1.json'

def load(p):return json.loads(Path(p).read_bytes())
def require(value,message):
    if not value:raise ValueError('Earlier COMMON775 reflow: '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']=='dk4-earlier775-reflow-release-v1','wrong release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    arm,common=image.read_file('/__arm9__.bin'),image.read_file(PATH)
    require(sha(arm)==conf['source_ARM9_sha256'] and sha(common)==conf['source_COMMON_sha256'],'exact current source required')
    require(sha(baseline.read_file(PATH))==conf['canonical_COMMON_sha256'],'canonical base changed')
    require(sha(Path('work/clean.nds').read_bytes())==conf['clean_ROM_sha256'],'clean Japanese changed')
    doc=load(conf['manuscript']);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-fixed-v1','reviewed policy required')
    rows=doc['records'];require([r['message_id'] for r in rows]==[682,764,774,775] and all(all(r['review'].values()) for r in rows),'four individually reviewed retentions required')
    require(doc['retained_exact_layout_IDs']==[682,764,774] and doc['reflow_IDs']==[775] and doc['source_prose_or_completion_credit_added']==0,'one reflow and no duplicate credit required')
    native,approval,copies,actual=[load(conf[k]) for k in ['native_proof','native_approval','copy_proof','actual_approval']]
    require(native['retained_exact_layout_IDs']==[682,764,774] and native['proposed_reflow_IDs']==[775] and not native['changed_prose_IDs'],'contextual layout decisions changed')
    require([r['message_id'] for r in native['records']]==[682,764,774,775]
        and len(native['original_clean_current_selector_cases'])==13 and len(native['original_clean_current_funds_cases'])==11
        and len(native['original_clean_current_stock_letter_cases'])==36,'complete source/native scope required')
    for row in native['records']:
        require([r['label'] for r in row['native_cases']]==['current','reviewed'],'paired current native cases required')
        for c in row['native_cases']:
            require(c['full_independent_228x64_plane_equal'] and c['complete_leading_internal_final_glyphs_and_bounds']
                and c['all_source_bytes_consumed_one_native_page'] and c['original_expansion_then_existing_wrapper_without_new_dispatch'],'complete native plane required')
            require(c['compiled_hex']==c['native_formatted_hex']==row['current_hex' if c['label']=='current' else 'target_hex']
                and sha(Path(c['preview']).read_bytes())==c['preview_sha256'],'native target or preview changed')
    require(approval['all8_current_and_reviewed_complete_native_planes_viewed'] and approval['all14_unsafe_or_unowned_inputs_rejected']
        and len(approval['negative_controls'])==14 and all(r['rejected'] for r in approval['negative_controls']),'complete native approval required')
    require(approval['intro774_exhaustive_complete_word_partitions_at1_2_3_rows']=={'1':[],'2':[],'3':[]} and approval['intro774_four_rows_possible'],'774 retention proof required')
    require(copies['complete_native_copy_cases']==len(copies['cases'])==7336 and len(copies['sequenced_cache_cases'])==10,'complete native copies required')
    require(actual['ten_full_screens_viewed'] and not actual['visual_review_pending'] and actual['no_open_translation_specific_display_or_transition_finding'],'viewed actual transition required')
    require(actual['actual_original_reward_sequence']==[775,780,766] and actual['actual_panel_observations']==6 and actual['all_jobs_terminal'],'actual original reward sequence required')
    require(actual['nontext_equal_samples']==len(actual['captured_comparisons'])==74 and not actual['nontext_differences'],'paired nontext regions changed')
    require(actual['versions'][0]['all_font_rows']==actual['versions'][1]['all_font_rows'] and all(r['whole_RGB_equal'] for r in actual['sampled_after_original_farewell'])
        and actual['whole_final_RGB_equal'],'measured original timing and return scope changed')
    require(actual['native_final_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and actual['whole_actor_and_actual_captain_equal'] and actual['actual_donor_captain_IDs']==[1,1]
        and actual['PRNG_equal'] and actual['PRNG_seeds']==[260148687,260148687],'measured final state scope changed')
    require(actual['input_fixtures_are_counterfactual_not_earned_large_sale_share_inventory_qualification_or_letter']
        and actual['no_PC_or_emulator_code_or_RNG_fixture'] and actual['source_code_portraits_and_original_effect_bodies_unchanged'],'fixture scope must stay explicit')
    for version in actual['versions']:
        require([r['message_ID'] for r in version['holds']]==[775,780,766] and all(r['matching_holds'] for r in version['holds']),'actual held planes missing')
        require(all(r['complete_first_internal_final_glyphs_bounds_and_one_page'] and r['complete_ink_and_blank_paper_match'] for r in version['holds']),'actual complete planes required')
        fixture=version['qualification_input_fixture']
        require(fixture['PC']==0x020BBCA4 and fixture['original_sale_hold_total']==2 and fixture['supplied_reward_quantity_input']==16
            and fixture['supplied_qualification_result']==2 and fixture['supplied_bonus_flag']==1
            and fixture['all_other_CPU_WRAM_DTCM_ITCM_bytes_exact'] and fixture['no_PC_code_RNG_cash_or_cargo_quantity_write'],'bounded input fixture changed')
    before=owned_entries(common,arm,conf['directory_sha256']);clean=NdsImage.open('work/clean.nds')
    jp=common_message_entries(clean.read_file(PATH),clean.read_file('/__arm9__.bin'))
    for row in rows:
        n=row['message_id'];entry,source=before[n],jp[n]
        require(row['current_hex']==entry.text.hex() and row['source_hex']==source.text.hex(),'source/current bytes changed')
        for key,e in [('current_reference',entry),('source_reference',source)]:
            expected=dict(message_ID=n,block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text),record_index=e.record_index,table_offset=e.table_offset,start_in_record=e.start)
            require(row[key]==expected,'exact reference changed')
        require(row['fresh_retained_wording_justification'] and row['layout_review_reason'] and row['source_meaning'] and row['localization_note'],'individual reasons required')
        require(row['english'].removesuffix('{PAD}').encode()==b' '.join(entry.text.split()),'prose word changed')
        if n!=775:require(row['target_hex']==row['current_hex'] and row['editorial_decision']=='retain-wording-and-layout','retained layout changed')
        else:require(row['editorial_decision']=='retain-wording-reflow' and row['actual_recommendation_branch_observed'],'reflow needs actual scope')
    row=rows[-1];old=before[775];target,layout=compile_letter(775,row['english'],len(old.text))
    require(target.hex()==row['target_hex']==conf['target_text_hex'] and old.text.hex()==conf['source_text_hex'],'native-reviewed target changed')
    require(layout['lines']==["And I'll write you a letter",'of recommendation to thank you for','selling us so many popular goods.']
        and layout['generated_terminal_spaces']==2 and layout['generated_even_pre_LF_allocation_spaces']==[0,0],'reviewed allocation changed')
    source=IlnkContainer.parse(common);blocks=list(source.blocks);body=bytearray(blocks[old.block])
    require(old.block==10 and len(old.text)==len(target)==105 and body[old.block_offset:old.block_offset+106]==old.text+b'\0','owned NUL changed')
    body[old.block_offset:old.block_offset+105]=target;blocks[old.block]=bytes(body);result=IlnkContainer(blocks).to_bytes()
    require(len(result)==len(common) and sha(result)==conf['target_COMMON_sha256'],'whole target COMMON changed')
    after=owned_entries(result,arm,conf['directory_sha256'])
    for a,b in zip(before,after,strict=True):
        require((a.message_id,a.block,a.block_offset,a.copy_end,a.record_index,a.start,a.end)==(b.message_id,b.block,b.block_offset,b.copy_end,b.record_index,b.start,b.end),'native message boundary moved')
        require(b.text==(target if a.message_id==775 else a.text),'unselected message changed')
    restored=list(blocks);inverse=bytearray(restored[10]);inverse[old.block_offset:old.block_offset+105]=old.text;restored[10]=bytes(inverse)
    require(IlnkContainer(restored).to_bytes()==common,'inverse failed')
    # The only mutation follows every source,prose,native,actual and target check.
    image.replace_file(PATH,result)
    return dict(manuscript=conf['manuscript'],changed_records=[dict(id='COMMON_MESSAGE_775',message_ID=775)],
        source_COMMON_sha256=sha(common),target_COMMON_sha256=sha(result),lines=layout['lines'],generated_terminal_spaces=2,
        all3668_boundaries_and_unselected_payloads_exact=True,all_other_files_code_fonts_graphics_and_storylines_unmodified=True,
        retentions=[682,764,774],actual_original_sequence=[775,780,766],actual_reward_inputs_disclosed_not_earned=True,new_editorial_credit=0)
