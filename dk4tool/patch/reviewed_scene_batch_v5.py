"""Pure registered integration of complete source-bound speech/menu/personality scenes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES,validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from scripts.audit_story_glyph_consistency import load
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

def require(value,message):
    if not value:raise ValueError('Reviewed mixed scene integration: '+message)

def compound_objects(group,approved,plans,menu,styles):
    objects=[]
    for obj in group['native_objects']:
        oldrows=obj['records'];rows=[approved[r['id']] for r in oldrows]
        for row,old in zip(rows,oldrows,strict=True):
            keys=['id','english','source_hex','current_hex','current_reference','source_command_offset']
            keys+=['source_style_indices','source_reference','source_header_hex'] if obj['word']==0x4100 else ['source_index','source_byte_offset']
            require(all(row[k]==old[k] for k in keys),'exact original compound source/current/prose membership')
        source,current=map(bytes.fromhex,[obj['source_hex'],obj['current_hex']])
        if obj['word']==0x4100:
            value=compile_styles(source,current,rows,plans)
            proof=next(r for r in styles['objects'] if r['block']==group['block'] and r['source_command_offset']==obj['old_offset'])
        else:
            require(obj['word'] in (0x2100,0x2200),'mapped native menu consumer')
            value=compile_choices(source,current,rows)
            proof=next(r for r in menu['menus'] if r['block']==group['block'] and r['source_command_offset']==obj['old_offset'])
        require(value.hex()==obj['compiled_hex']==proof['target_object_hex'],'fresh reviewed native object equals tested object')
        # Preserve the immutable relocation proof's historical record metadata.
        objects.append(dict(id=obj['id'],word=obj['word'],offset=obj['old_offset'],current_hex=current.hex(),source_hex=source.hex(),compiled_hex=value.hex(),records=oldrows))
    return objects

def plan_release(image,baseline,config_path):
    conf=load(config_path);require(conf['format']=='dk4-reviewed-scene-release-v5','release schema')
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'changed dependency: '+path)
    before,base_before=bytes(image.rom.save()),bytes(baseline.rom.save())
    require(sha(before)==conf['parent_ROM_sha256'],'complete ordered predecessor')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    arm=image.read_file('/__arm9__.bin');require(sha(arm)==conf['pre_runtime_ARM9_sha256'],'unchanged pre-runtime ARM9')
    clean_path=Path(conf['clean_ROM']);require(sha(clean_path.read_bytes())==conf['clean_ROM_sha256'],'clean Japanese input')
    clean=NdsImage.open(clean_path)
    doc,layout,reconstruction,stored,loaders,actual,visual,menu,styles,pixels,FE=[load(conf[k]) for k in
        ['manuscript','plan','reconstruction','stored_native','loaders','actual','visual_review','typed_menu','native_styles','focused_pixels','FE_layout']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','individual American English review')
    require(len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count'],'unique complete record membership')
    require(all(all(r['review'][g] is True for g in REQUIRED_REVIEW_GATES) for r in doc['records']),'all five individual gates')
    require(all(not any(t in r['english'] for t in ['{LB','{ALIGN','{PAD}','\n']) for r in doc['records']),'logical prose only')
    speech=[r for r in doc['records'] if r['kind'] in ('progressive','system-FE')]
    ordinary=[r for r in speech if r.get('native_object_kind')!='4100-style-alternative']
    variants=[r for r in speech if r.get('native_object_kind')=='4100-style-alternative']
    choices=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    require((len(speech),len(ordinary),len(variants),len(choices))==tuple(conf[k] for k in ['speech_count','ordinary_count','style_count','typed_choice_count']),'complete consumer membership')
    plans={r['id']:r for r in layout['records']};approved={r['id']:r for r in doc['records']}
    require(len(plans)==len(speech) and not layout['failures'],'complete unique plans')
    for row in speech:
        plan=plans[row['id']]
        require(row['english']==plan['logical_English'] and row['planned_English_markup']==plan['English'],'prose and formatted plan binding')
        require(bytes.fromhex(plan['encoded_hex'])[0]==row['source_selector'],'source speaker selector')
        require(not any(i['severity'] in ('warning','error') for i in plan['base_QA']['issues']),'resolved fresh formatting diagnostics')
    require(set(doc['blocks'])==set(conf['reviewed_blocks'])=={g['block'] for g in reconstruction['groups']},'complete inventoried scope')
    require(set(conf['blocks'])==set(reconstruction['changed_blocks']) and set(conf['reviewed_blocks'])-set(conf['blocks'])==set(reconstruction['unchanged_control_only_blocks']),'changed versus control-only scope')
    require(stored['complete_stored_pages']==visual['pages']==conf['native_pages'] and stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'],'complete stored native pages')
    require(stored['fresh_relocated_native_relative_cases']==conf['relative_cases'] and stored['all_stored_planes_equal_directly_viewed_compiled_planes'],'native branches and inherited pixels')
    require(visual['all_final_pages_directly_viewed_or_exact_plane_reuse'],'all final pages visually reviewed')
    require(FE['unexpected_blank_rows_orwraps_absent'] and not FE['findings'] and FE['FE_records']==conf['FE_count'],'exact FE row placement')
    require(loaders['fresh_whole_archive_loads_andcache_hits']==325 and loaders['fresh_parent_cases']==2*len(conf['blocks']) and loaders['exact_reused_parent_cases']==650-2*len(conf['blocks']) and loaders['prior_executed_parent_instructions_match_current_runtime'],'native archive and parent handoffs')
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'],'complete native menus')
    require(menu['native_provider_alignments']==conf['menu_alignments'] and menu['bridged_modal_returns']==conf['menu_returns'] and menu['complete_English_caption_style_planes']==conf['menu_planes'],'native menu selection/cancel and style coverage')
    require(styles['native_target_slot_cases']==conf['style_slots'] and styles['source_alias_equivalence_exact'],'all source personality slots/aliases')
    require(stored['typed_labels_checked']==len(choices) and len(stored['style_records'])==len(variants),'complete stored compound membership')
    require(actual['total_frames']==conf['actual_frames'] and len(actual['runs'])==conf['actual_runs'] and len(actual['all_review_sheets_directly_viewed'])==conf['actual_sheets'],'completed representative English runs')
    require(actual['representative_progressive_FE_actor0_style_three_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andnormal_F_headers_complete'] and actual['no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim'],'observed distinct behavior and honest scope')
    require({k:len(pixels[k]) for k in conf['focused_pixel_counts']}==conf['focused_pixel_counts'],'actual pixel membership')
    require(all(p['complete_native_glyph_plane_andblank_guards_equal'] for p in pixels['body_pages']),'complete actual body pixels')
    require({p['selected_option'] for p in pixels['menu_samples']}=={0,1,2} and all(p['all_three_complete_caption_glyphs_andblank_guards_exact'] and p['all_highlight_background_RGB_exact'] for p in pixels['menu_samples']),'three complete controller highlights')
    path=doc['file_path'];require(path=='/data/SC1.DK4','owned route archive')
    archive=image.read_file(path);require(sha(archive)==reconstruction['source_archive_sha256'],'complete source archive')
    container=IlnkContainer.parse(archive);clean_blocks=IlnkContainer.parse(clean.read_file(path)).blocks
    require(len(container.blocks)==len(clean_blocks)==325,'whole route block count')
    inventory,_,_=scoped_inventory();blocks=list(container.blocks);changes=[]
    for group in reconstruction['groups']:
        number=group['block'];require(sha(blocks[number])==group['current_sha256'] and sha(clean_blocks[number])==group['clean_sha256'],'source/current block identities')
        objects=compound_objects(group,approved,plans,menu,styles)
        rows=[r for r in ordinary if r['block']==number]
        target,proof=rebuild_block(arm,clean_blocks[number],blocks[number],rows,plans,inventory,objects)
        require(sha(target)==group['target_sha256'] and target==Path(group['target_block']).read_bytes(),'fresh tested complete block')
        require(all(value==group[key] for key,value in proof.items()),'exact complete reconstruction map')
        blocks[number]=target
        for row in (r for r in doc['records'] if r['block']==number):
            ref=row['planned_integrated_reference'];at=ref['offset'];raw=bytes.fromhex(ref['exact_stored_hex'])
            require(target[at:at+len(raw)+1]==raw+b'\0' and ref['target_archive_sha256']==reconstruction['target_archive_sha256'],'individual final stored reference')
            changes.append(dict(id=row['id'],file_path=path,block=number,new_offset=at,kind=row.get('native_object_kind',row['kind']),stored_sha256=sha(raw)))
    result=IlnkContainer(blocks).to_bytes()
    require(sha(result)==reconstruction['target_archive_sha256'] and result==Path(reconstruction['target_archive']).read_bytes(),'whole tested archive')
    require({i for i,(a,b) in enumerate(zip(container.blocks,blocks,strict=True)) if a!=b}==set(conf['blocks']),'only reviewed changed blocks')
    inverse=list(blocks)
    for number in conf['blocks']:inverse[number]=container.blocks[number]
    require(IlnkContainer(inverse).to_bytes()==archive,'whole archive inverse')
    planned=deepcopy(image);planned.replace_file(path,result)
    require(sha(bytes(planned.rom.save()))==conf['target_ROM_sha256'],'whole tested pre-runtime target')
    require([p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[path] and all(planned.read_file(p)==v for p,v in image.iter_components()),'all unowned bytes/components')
    require(bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before,'pure caller and baseline preservation')
    return planned.rom,dict(manuscripts=[conf['manuscript']],changed_records=changes,
        files=[dict(file_path=path,source_sha256=sha(archive),target_sha256=sha(result),changed_records=changes)],
        one_complete_NDS_object_commit_after_all_gates=True,all_source_controls_commands_relatives_andunowned_bytes_preserved=True,
        native_pages=conf['native_pages'],fresh_relative_cases=conf['relative_cases'],native_loads=325,style_slots=conf['style_slots'],typed_labels=len(choices),
        actual_frames=conf['actual_frames'],representative_initialized_gameplay_not_natural_event_activation=True,
        canonical_stage_requires_registered_right_bound_runtime_layer=conf['right_bound_configuration'],no_completion_credit_orpromotion_granted=True,full_goal_complete=False)
