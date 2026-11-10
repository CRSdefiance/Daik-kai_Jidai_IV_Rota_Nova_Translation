"""Atomic registered layer for ten context-reviewed occupational speaker labels."""
import json
from pathlib import Path
from dk4tool.patch.square_shopkeeper_label_data_v1 import transform,SOURCE,require
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
PATH='/__arm9__.bin'
CONFIG='translations/square_shopkeeper_label_release_v2.json'
FORMAT='dk4-ten-square-shopkeeper-label-release-v2'

def load(path):return json.loads(Path(path).read_bytes())

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path);require(conf['format']==FORMAT,'registered format')
    critical=[conf[k] for k in ['manuscript','approval','names','actual','view']]+[__file__,
        'dk4tool/patch/square_shopkeeper_label_data_v1.py','scripts/square_shopkeeper_exact_native_context_v7020.py',
        'scripts/square_shopkeeper_name_style_v7020.py','scripts/square_shopkeeper_font_oracles_v7020.py',
        'work/analysis/square_shopkeeper_origin_v7024b/exact_native_origin_and_source_locked_successor.json']
    require({Path(p).resolve() for p in critical}<={Path(p).resolve() for p in conf['dependencies']},'complete critical dependency closure')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency:'+p)
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['source_files'],'complete cumulative files')
    require({p:sha(v) for p,v in image.iter_components()}==conf['source_components'],'complete cumulative components')
    arm=image.read_file(PATH);require(sha(arm)==SOURCE==conf['source_ARM9_sha256'],'current runtime hash')
    require(sha(baseline.read_file(PATH))==conf['canonical_ARM9_sha256'],'canonical runtime')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','clean ROM')
    clean=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(clean)==conf['clean_ARM9_sha256'],'clean runtime')
    doc,seal,names,actual,view=[load(conf[k]) for k in ['manuscript','approval','names','actual','view']]
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','v2 en-US policy')
    require(doc['all_five_per_name_review_gates_approved_registered_release_pending'] and doc['all207_name_review_scope_remains_open'],'approval/full207 scope')
    require(doc['full_catalogue_UI_unvisited'] and doc['no_duplicate_dialogue_or_name_completion_credit'] and not doc['full_goal_complete'],'coverage scope')
    require(doc['all_measured_later_differences_preserved_for_older_record_technical_reaudit'],'later differences retained')
    require(len(doc['records'])==10 and [r['actor_ID'] for r in doc['records']]==list(range(82,92)),'ten source identities')
    for row in doc['records']:
        require(row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=True),'five per-name gates')
        require(not row['formatting_and_shared_consumer_validation_pending'] and row['formatting_reason'],'native name approval')
        require(row['new_name_completion_credit']==row['new_dialogue_completion_credit']==0,'no duplicate credit')
        expected={**row['current_reference'],'terminated_hex':b'Shopkeeper\0'.hex()}
        require(row['target_reference']==expected,'target complete terminator/pointer reference')
    require(seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'sealed manuscript')
    for flag in ['all_ten_source_context_localization_naturalness_and_formatting_gates_true',
        'all414_name621_field207_voice_consumers176_macro_alignments_and_complete_native_label_pass',
        'two_storage_behaviors_actual_nine_changed_headers_and32_native_pages_viewed',
        'all621_pointers_all_other197_names_voices_dynamic_roles_and_unread_old_tails_preserved',
        'full_catalogue_UI_every_conditional_nameplate_and_full207_editorial_approval_not_claimed',
        'B189_retrospective_line_breaks_and_all_measured_later_differences_remain_separate_open_leads',
        'all_earlier_ROMs_translations_failures_proofs_and_history_preserved']:require(seal[flag] is True,'approval flag:'+flag)
    require(not seal['visual_review_pending'] and seal['new_name_or_dialogue_completion_credit']==0,'visual/credit approval')
    require(names['source_ARM9_sha256']==SOURCE and names['target_ARM9_sha256']==conf['target_ARM9_sha256'],'native source/target')
    require(names['all414_parent_and414_target_getters_pass'] and names['all621_parent_and621_target_field_consumers_pass'],'all native names/fields')
    require(names['all_other197_actors_all207_voices_and_dynamic_CF_D0_assignments_preserved'] and names['original_actual_captain2_uses_special_object'],'voices/actual captain')
    require(names['all_original_scratch_or_readonly_paths_restore_all4MiB'] and names['own_target_payload_and_each_executed_instruction_exact_no_RAM_overlay_or_forced_roles'],'native ownership/instructions')
    require(names['full_catalogue_UI_and_all_conditional_shared_nameplate_visits_not_claimed'],'native coverage scope')
    require([v['case'] for v in names['versions']]==['parent','target'],'native versions')
    for key,textkey,count,changed_count in [('name_getters','text',414,20),('catalogue_voices','current_catalog_name',207,10),('field_getters','text_hex',621,10)]:
        left,right=[v[key]['rows'] for v in names['versions']];require(len(left)==len(right)==count,'native row count:'+key);changes=[]
        for a,b in zip(left,right,strict=True):
            different={k for k in a if a[k]!=b.get(k)};require(a.keys()==b.keys(),'native row shape')
            if not different:continue
            require(82<=a['actor_ID']<=91 and a['actor_ID']==b['actor_ID'],'only ten actor outputs')
            require(different=={textkey} or key=='name_getters' and different=={'text','text_hex'},'only text values change')
            if key=='field_getters':require(a['column']==b['column']==0 and a[textkey]==b'Square Shopkeeper'.hex() and b[textkey]==b'Shopkeeper'.hex(),'only primary fields')
            else:require(a[textkey]=='Square Shopkeeper' and b[textkey]=='Shopkeeper','exact returned labels')
            changes.append(a['actor_ID'])
        require(len(changes)==changed_count and set(changes)==set(range(82,92)),'complete changed native actors')
    require(names['versions'][0]['dynamic_roles']['rows']==names['versions'][1]['dynamic_roles']['rows'],'unforced dynamic roles')
    require(names['macro_alignment_cases']==176 and [v['case'] for v in names['macro_versions']]==['parent','target'],'macro versions/count')
    for version in names['macro_versions']:
        require(len(version['cases'])==22,'macro input cases')
        for row in version['cases']:
            body=bytes.fromhex(row['input_hex']);require(body in [b'FI FA FO FU',b'Shopkeeper'] and row['actor_ID'] in [2,*range(82,92)],'original macro identities')
            expected=b'Lil Argot Argot Co. Lil Argot' if body==b'FI FA FO FU' else body
            require(len(row['native']['cases'])==4 and [c['input_alignment'] for c in row['native']['cases']]==list(range(4)),'four literal/macro alignments')
            require(all(bytes.fromhex(c['output_hex'])==expected and c['source_owned_name_ring_restoration_recovers_complete4MiB'] for c in row['native']['cases']),'macro bytes/owned memory')
    plane=names['native_name_plane'];require(plane['text']=='Shopkeeper' and plane['native_width']==60 and plane['all_leading_internal_final_glyphs_complete_in_one_original_style11_row'],'complete native label')
    require([e['code'] for e in plane['events']]==list(b'Shopkeeper') and not plane['zero_ink_flushes'],'complete glyph sequence')
    require(actual['target_changed_nameplate_observations']==9 and actual['target_complete_page_observations']==32 and actual['target_speech_observations']==30,'actual scene counts')
    for flag in ['all_complete_source_owned_commands_retained_and_both_normal_returns_observed',
        'all_native_body_glyphs_black_gray_and_nameplate_first_internal_final_glyphs_and_blank_guards_pass',
        'no_stale_old_label_ink_wrap_or_nameplate_pagination','all_jobs_terminal_and_reaped',
        'original_schedules_no_RAM_roles_roster_funds_RNG_conditions_or_results_forced','all_measured_timing_RNG_UI_and_RGB_differences_retained',
        'initialized_scenes_not_natural_activation_original_location_earned_progress_full_effects_full_route_or_hardware',
        'full_catalogue_UI_and_every_conditional_nameplate_not_visited','no_new_prose_approval_or_duplicate_credit',
        'B189_early_line_breaks_separate_retrospective_editorial_lead']:require(actual[flag] is True,'actual requirement:'+flag)
    require([v['case'] for v in actual['versions']]==['static_parent','static_target','staged_parent','staged_target'],'four actual versions')
    require([v['actual_complete_body_holds'] for v in actual['versions']]==[67,67,59,59] and [v['actual_complete_name_holds'] for v in actual['versions']]==[63,63,59,59],'complete actual glyph holds')
    fixtures=load(actual['fixtures']);bycase={f['case']:f for f in fixtures['fixtures']};target_last_pages=[]
    for version in actual['versions']:
        fixture=bycase[version['case']];records={r['id']:r for r in fixture['original_text_records']}
        expected_names={r['actor_ID']:r['text'] for v in names['versions'] if v['case']==version['version'] for r in v['name_getters']['rows'] if r['consumer']=='progressive-nameplate'}
        require(len(version['panels'])==(17 if version['scene']=='static' else 13),'complete individual speeches')
        require(len({p['id'] for p in version['panels']})==len(version['panels']),'unique actual speech references')
        for panel in version['panels']:
            record=records[panel['id']];require(panel['actor_ID']==record['source_selector'],'actual source selector')
            pair=next(p for p in version['command_pairs'] if p['offset']==record['fixture_command_offset'])
            require(pair['word']==0x4000 and (pair['start'],pair['returned'])==(panel['start'],panel['returned']),'complete speech interval')
            require(len(panel['complete_page_holds'])==panel['native_pages'] and all(panel['complete_page_holds']),'every actual native page')
            require(panel['name']==(None if panel['actor_ID']==254 else expected_names[panel['actor_ID']]),'actual native name binding')
            require(bool(panel['complete_name_holds'])==(panel['name'] is not None),'every actual named header')
            if version['version']=='target':
                for number,holds in enumerate(panel['complete_page_holds'],1):target_last_pages.append((panel['id'],number,holds[-1]['capture'],holds[-1]['sha256']))
        require(sum(p['native_pages'] for p in version['panels'])==version['actual_complete_page_observations']==(17 if version['scene']=='static' else 15),'actual page count')
        require(sum(sum(map(len,p['complete_page_holds'])) for p in version['panels'])==version['actual_complete_body_holds'],'individual body holds')
        require(sum(len(p['complete_name_holds']) for p in version['panels'])==version['actual_complete_name_holds'],'individual name holds')
    require(sum(p['actor_ID'] in [82,85] for v in actual['versions'] if v['version']=='target' for p in v['panels'])==9,'nine changed nameplate observations')
    require(len(view['all32_whole_frame_panes_pixel_equal'])==32 and all(p['whole_pane_pixel_equal'] for p in view['all32_whole_frame_panes_pixel_equal']),'complete viewed panes')
    require(sorted(target_last_pages)==sorted((p['id'],p['page'],p['capture'],p['sha256']) for p in view['all32_whole_frame_panes_pixel_equal']),'viewed exact actual pages')
    for scene in ['static','staged']:
        a,b=[next(v for v in actual['versions'] if v['case']==scene+'_'+label) for label in ['parent','target']]
        require(len(a['command_pairs'])==len(b['command_pairs']),'paired command count')
        for x,y in zip(a['command_pairs'],b['command_pairs'],strict=True):
            require(all(x[k]==y[k] for k in ['offset','word','result','UI_after','decoded_length']),'original command result/UI/extent')
        require(a['command_pairs'][-1]['result']==b['command_pairs'][-1]['result']==[0,0],'original normal returns')
        measured=next(c for c in actual['comparisons'] if c['scene']==scene);computed=[]
        for x,y in zip(a['command_pairs'],b['command_pairs'],strict=True):
            fields=[k for k in x if x[k]!=y[k]]
            if fields:computed.append(dict(offset=x['offset'],word=x['word'],different_fields=fields,before=x,after=y))
        require(measured['command_differences']==computed and measured['normal_exit_frames']==[a['exit_frame'],b['exit_frame']],'all measured command/RNG/timing differences retained')
        require(measured['no_full_RAM_final_components_future_or_complete_causal_equivalence_claim'],'later-world scope')
    require([sum(not d['all_differences_within_nameplate_strip'] for d in c['RGB_differences']) for c in actual['comparisons']]==[82,0],'all outside-nameplate RGB differences retained')
    require([c['normal_exit_frames'] for c in actual['comparisons']]==[[6937,6936],[6693,6693]],'measured exit differences')
    require([len(c['command_differences']) for c in actual['comparisons']]==[18,0] and [len(c['RGB_differences']) for c in actual['comparisons']]==[98,19],'later measured differences')
    require(not view['visual_review_pending'] and view['all_six_target_exchange_sheets_individually_returned_and_viewed'] and len(view['all32_whole_frame_panes_pixel_equal'])==32,'whole exchange views')
    require(view['both_static82_and_staged85_actual_complete_nameplates_viewed'] and view['all_measured_timing_RNG_UI_RGB_differences_preserved'],'views and limits')
    for p in view['viewed_images']:require(sha(Path(p['path']).read_bytes())==p['sha256'],'viewed image:'+p['path'])
    target,plan=transform(arm,clean,doc['records'])
    require(plan==doc['data_plan']==seal['source_owned_data_plan'] and sha(target)==conf['target_ARM9_sha256']==seal['target_ARM9_sha256'],'exact owned target')
    require(target==Path(doc['target_ARM9']).read_bytes() and sha(Path(doc['target_research_ROM']).read_bytes())==doc['target_research_ROM_sha256']==conf['reference_ROM_sha256'],'approved research target')
    require(NdsImage.open(doc['target_research_ROM']).read_file(PATH)==target,'research ARM9 equality')
    report=dict(manuscript=conf['manuscript'],manuscript_sha256=sha(Path(conf['manuscript']).read_bytes()),source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),
        changed_records=[dict(id=r['id'],actor_ID=r['actor_ID'],before='Square Shopkeeper',after='Shopkeeper') for r in doc['records']],data_plan=plan,
        all_ten_contextual_five_gates_and_native_representative_nameplates_pass=True,all_other_files_fonts_code_pointers_voices_and197_names_preserved=True,
        actual_changed_headers=9,actual_target_body_page_observations=32,full_catalogue_UI_and_all_conditional_visits_unclaimed=True,
        measured_static_one_frame18_timing_two_RNG_word_and98_RGB_differences_preserved=True,no_duplicate_name_or_dialogue_completion_credit=True,full_goal_complete=False)
    # No ROM mutation until every input,meaning,ownership,native,display and scope guard passes.
    image.replace_file(PATH,target)
    return report
