"""Pure source-bound integration of23 complete reviewed Help articles andtheir25 native pages."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.dialogue.reviewed_help_pages_v1 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load


def require(value,message):
    if not value:raise ValueError('Early Help23 release: '+message)


def plan_release(image,baseline,config_path):
    conf=load(config_path);require(conf['format']=='dk4-early-help23-release-v1','schema')
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'changed dependency: '+path)
    before,base_before=bytes(image.rom.save()),bytes(baseline.rom.save())
    require(sha(before)==conf['parent_ROM_sha256'],'complete ordered predecessor')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical input')
    require(sha(image.read_file('/__arm9__.bin'))==conf['pre_runtime_ARM9_sha256'],'pre-runtime ARM9')
    clean_path=Path(conf['clean_ROM']);require(sha(clean_path.read_bytes())==conf['clean_ROM_sha256'],'clean Japanese input')
    clean=NdsImage.open(clean_path);doc=load(conf['manuscript']);plan=load(conf['plan'])
    native,visual,actual,actual_visual=[load(conf[k]) for k in ['native','visual','actual','actual_visual']]
    require(len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count']==23,'unique complete membership')
    require([r['topic_id'] for r in doc['records']]==list(range(21))+[181,184],'exact reviewed article membership')
    require((doc['proposed_revisions'],doc['justified_retentions'])==(16,7),'individual revision/retention counts')
    require(doc['review_gates']==['source','context','localization','naturalness','formatting'],'all five gates')
    for row in doc['records']:
        require(all(row['review'].get(g) is True for g in REQUIRED_REVIEW_GATES),'individual review gates')
        require(all(str(row.get(k,'')).strip() for k in ['speaker','context','source_meaning','localization_note','finding']),'individual editorial context andfinding')
        require(row['decision'] in ['revision','retention'],'individual disposition')
        if row['decision']=='retention':require(bool(row['retention_reason']),'individual justified retention')
    require(native['native_pages']==25 and native['complete_articles']==23,'all native pages')
    require(native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
        and native['all_executed_current_instruction_bytes_exact'],'complete native pixels/controls/current code')
    require(native['current_ARM9_sha256']==conf['final_runtime_ARM9_sha256'],'same accepted final font/runtime')
    require(visual['all25_complete_pages_approved'] and visual['all_seven_readable_sheets_directly_viewed'],'every native page viewed')
    require(actual['all25_complete_actual_pages_andnative_child_targets_pass'] and actual['actual_pages']==25 and actual['actual_articles']==23,'all actual pages/targets')
    require(actual['actual_ordinary_controls_no_state_injection'] and not actual['full_story_playthrough'] and not actual['hardware'],'honest ordinary Help scope')
    require(len(actual['original_forward_back_andL_R_history_returns'])==3
        and all(r['complete_title_andbody_RGB_equal'] for r in actual['original_forward_back_andL_R_history_returns']),'both continuation returns andnative history')
    require(actual_visual['all25_complete_pages_approved'] and actual_visual['all_seven_readable_actual_sheets_directly_viewed'],'every actual page viewed')
    for proof_path,proof in [(conf['native'],native),(conf['actual'],actual)]:
        for path,digest in proof['evidence'].items():require(sha(Path(path).read_bytes())==digest,'changed proof dependency: '+path)
    require(actual_visual['actual_proof_sha256']==sha(Path(conf['actual']).read_bytes()),'actual review identity')
    path=doc['file_path'];require(path=='/COMMON/HELP.DK4','only owned Help resource')
    encoded,compiled=plan_articles(doc,clean.read_file(path),baseline.read_file(path),image.read_file(path))
    require(compiled['pages']==plan['pages'] and encoded==Path(conf['target_resource']).read_bytes(),'exact directly reviewed production bytes')
    require(sha(encoded)==conf['target_HELP_sha256'],'complete resource target')
    stored=IlnkContainer.parse(encoded).blocks;current=IlnkContainer.parse(image.read_file(path)).blocks
    actual_cases={r['topic_id']:r for r in actual['actual_HELP_cases']};native_cases={r['topic_id']:r for r in native['records']}
    changed=[]
    for row in doc['records']:
        pages=[p for p in compiled['pages'] if p['source_article_id']==row['topic_id']]
        require(len(pages)==len(row['planned_stored_pages']),'complete individual page membership')
        for page,ref in zip(pages,row['planned_stored_pages'],strict=True):
            t=page['topic_id'];raw=bytes.fromhex(page['encoded_hex'])
            require(ref['block']==t and ref['exact_stored_hex']==raw.hex()==native_cases[t]['encoded_hex'],'individual stored/native bytes')
            require(encoded[ref['archive_offset']:ref['archive_offset']+ref['bytes']]==raw==stored[t],'complete exact stored reference')
            require(ref['target_archive_sha256']==sha(encoded) and ref['actual_frame']==actual_cases[t]['frame'],'individual actual reference')
            require(actual_cases[t]['all_first_internal_final_glyphs_andblank_gaps_exact'],'all complete actual characters')
        changed.append(dict(id=row['id'],file_path=path,topic_id=row['topic_id'],source_reference=row['source_reference'],
            current_reference=row['current_reference'],planned_stored_pages=row['planned_stored_pages'],decision=row['decision']))
    require(compiled['compiler_generated_navigation_pairs']==[dict(article=7,page_ids=[7,202]),dict(article=9,page_ids=[9,211])],'scoped continuation ownership')
    planned=deepcopy(image);planned.replace_file(path,encoded)
    require([p for _,p,b in image.iter_files() if planned.read_file(p)!=b]==[path],'only Help changed')
    require(all(planned.read_file(p)==b for p,b in image.iter_components()),'all runtime/components exact')
    inverse=deepcopy(planned);inverse.replace_file(path,image.read_file(path));require(bytes(inverse.rom.save())==before,'complete serialized parent inverse')
    require(sha(bytes(planned.rom.save()))==conf['target_ROM_sha256'],'complete tested target')
    require(bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before,'pure planner preserves callers')
    proof=dict(format=conf['format'],one_complete_NDS_object_commit_after_all_gates=True,manuscripts=[conf['manuscript']],
        files=[dict(file_path=path,source_sha256=sha(image.read_file(path)),target_sha256=sha(encoded),changed_records=changed)],
        changed_records=changed,articles=23,pages=25,revisions=16,retentions=7,
        all_individual_source_current_final_refs_five_gates_native_pixels_visual_actual_widgets_andreturns_bound=True,
        complete_parent_inverse_andall_unowned_files_components_exact=True,HELP211_to212_with_existing202_preserved=True,
        actual_ordinary_Help_navigation=True,actual_story_playthrough=False,hardware=False,new_credit=0)
    return planned.rom,proof
