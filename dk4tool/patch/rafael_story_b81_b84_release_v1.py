"""Pure registered330-object integration, including two source-owned FE continuations."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES,validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_scene_batch_v5 import compound_objects
from dk4tool.rom.nds import NdsImage
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from dk4tool.script.reviewed_FE_pagination_v1 import insert_FE_continuations
from scripts.audit_story_glyph_consistency import load
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

def require(value,message):
    if not value:raise ValueError('Rafael330 release: '+message)

def qualify_evidence(conf,doc,reconstruction,stored):
    native,visual,actual,names,lookup,loaders,menu=[load(conf[k]) for k in
        ['compiled_native','visual_review','actual','scoped_names','stored_lookup','loaders','typed_menu']]
    validate_natural_dialogue_batch(names)
    require(native['runtime']==stored['runtime'] and stored['runtime']['captain']==0,'own Rafael runtime')
    require(native['pages']==stored['complete_stored_pages']==visual['body_pages']==336,'all native/stored/viewed pages')
    require(visual['all336_final_pages_directly_viewed_or_exact_native_plane_reuse'] and
        visual['all20_caption_style_planes_andfive_labels_viewed'] and visual['all16_scoped_nameplanes_viewed'], 'complete visual coverage')
    require(stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
        stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['fresh_relocated_native_relative_cases']==140,'native text/branch guards')
    require(stored['native_sha256']==sha(Path(conf['compiled_native']).read_bytes()),'current native proof')
    require(stored['reconstruction_sha256']==sha(Path(conf['consumer_reconstruction']).read_bytes()),'current327 consumer proof')
    compiled={r['id']:r for r in native['records']};entries={r['id']:r for r in stored['records']}
    require(set(compiled)==set(entries) and len(entries)==len(lookup['records'])==327,'all327 physical native bodies')
    consumer=load(conf['consumer_reconstruction'])
    physical={t['id']:t for g in consumer['groups'] for t in g['text_records']}
    require(set(physical)==set(compiled),'exact physical consumer membership')
    for row in native['records']:
        require(row['compiled_hex']==physical[row['id']]['compiled_hex'],'compiled/stored command binding')
        display=row['complete_native_English_display'];pages=[display] if row['kind']=='system-FE' else display['pages']
        for page in pages:require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'],'complete viewed native plane')
    require(lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'],'original catalogue doesnot restoreold wording')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,2,684)
        and loaders['prior_executed_parent_instructions_match_current_runtime'],'whole archive loads andqualified parent modes')
    require(len(names['records'])==16 and {r['actor_ID'] for r in names['records']}==
        {0,4,5,6,7,14,15,16,79,82,95,104,113,147,162,167} and names['actual_headers_observed'],'16 source-bound actual headers')
    require((actual['source_speeches_observed'],actual['native_commands_observed'],actual['native_body_pages_observed'],
        actual['actual_choice_labels'],actual['offline_only_source_speeches'])==(75,77,86,5,250),'honest per-object actual/offline scope')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['qualifying_current_runs'],actual['qualifying_current_frames'])==
        (72406,6,5,65205),'current versus preserved earlier runs')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']),'no unvisited chronology/route/hardware claim')
    require(actual['all_native_menu_cursor_positions_andA_returns_observed'] and
        actual['four_FE_panels_andthree_FI_notice_texts_observed'] and actual['all_nine_two_page_cases_andseven_page_turn_fixes_observed'],'distinct native behavior observed')
    require(actual['actual_training_stat_effects_numeric_choice_returns_original_story_branches_andcancellation_unvisited'], 'explicit unvisited outcomes')
    require(menu['offline_visual_approved'] and len(menu['menus'])==2 and menu['typed_labels']==5,'both native menu objects')
    for obj in menu['menus']:
        proof=load(obj['source_native_receipt'])
        require(sha(Path(obj['source_native_receipt']).read_bytes())==obj['source_native_receipt_sha256'],'native menu proof identity')
        require(proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and proof['native_provider_alignments']==6,'native provider,caption andbounds')
    require(reconstruction['source_editorial_objects']==330 and reconstruction['source_speeches']==325 and
        reconstruction['native_speech_commands']==327 and reconstruction['complete_native_display_pages']==336,'source versus native page membership')

def plan_release(image,baseline,config_path):
    conf=load(config_path);require(conf['format']=='dk4-rafael-B81-B84-release-v1','schema')
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'changed dependency: '+path)
    before,base_before=bytes(image.rom.save()),bytes(baseline.rom.save())
    require(sha(before)==conf['parent_ROM_sha256'],'complete ordered predecessor')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    arm=image.read_file('/__arm9__.bin');require(sha(arm)==conf['pre_runtime_ARM9_sha256'],'pre-runtime ARM9')
    clean_path=Path(conf['clean_ROM']);require(sha(clean_path.read_bytes())==conf['clean_ROM_sha256'],'clean Japanese input')
    clean=NdsImage.open(clean_path)
    doc,layout,reconstruction,stored,menu=[load(conf[k]) for k in ['manuscript','plan','reconstruction','stored_native','typed_menu']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','individual American English review')
    require(len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count']==330,'unique complete source membership')
    require(all(all(r['review'][g] is True for g in REQUIRED_REVIEW_GATES) for r in doc['records']),'all five individual gates')
    require(all(not any(t in r['english'] for t in ['{LB','{ALIGN','{PAD}','\n']) for r in doc['records']),'unpositioned logical prose')
    speech=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    choices=[r for r in doc['records'] if r['kind']=='typed-choice-label'];plans={r['id']:r for r in layout['records']}
    require(len(speech)==len(plans)==325 and len(choices)==5 and not layout['failures'],'exact qualified consumers')
    for row in speech:
        plan=plans[row['id']]
        require(row['english']==plan['logical_English'] and row['planned_English_markup']==plan['formatted_markup'],'logical andformatted prose')
        require(bytes.fromhex(plan['encoded_hex'])[0]==row['source_selector'],'complete source speaker selector')
        require(not any(i['severity'] in ['warning','error'] for i in plan['base_QA']['issues']),'resolved fresh formatting diagnostics')
    require(doc['blocks']==conf['blocks']==reconstruction['changed_blocks']==[81,82,83,84],'four complete source exchanges')
    qualify_evidence(conf,doc,reconstruction,stored)
    path=doc['file_path'];require(path=='/data/SC0.DK4','owned route archive')
    archive=image.read_file(path);require(sha(archive)==reconstruction['source_archive_sha256'],'complete current archive')
    container=IlnkContainer.parse(archive);original=IlnkContainer.parse(clean.read_file(path)).blocks
    require(len(container.blocks)==len(original)==343,'complete route block membership')
    inventory,_,_=scoped_inventory();blocks=list(container.blocks);approved={r['id']:r for r in doc['records']};changes=[]
    require([g['block'] for g in reconstruction['groups']]==conf['blocks'],'complete ordered reconstruction')
    for group in reconstruction['groups']:
        number=group['block'];require(sha(blocks[number])==group['current_sha256'] and sha(original[number])==group['clean_sha256'],'source/current complete block identity')
        initial=group['first_page_reconstruction'];objects=compound_objects({**initial,'block':number},approved,plans,menu,{'objects':[]})
        rows=[r for r in speech if r['block']==number]
        target,proof=rebuild_block(arm,original[number],blocks[number],rows,plans,inventory,objects)
        require(proof==initial,'complete original command order/scopes/relative maps andinverse')
        if group['FE_pagination'] is not None:
            owners=[]
            for row in rows:
                if 'planned_integrated_native_pages' not in row:continue
                p=plans[row['id']];first=next(t for t in proof['text_records'] if t['id']==row['id'])
                pages=[dict(native_child_page=i+1,logical_English=c['logical_English'],encoded_hex=c['encoded_hex']) for i,c in enumerate(p['native_FE_child_pages'])]
                owners.append(dict(source_ID=row['id'],first_command_offset=first['new_offset']-5,
                    first_stored_hex=first['stored_hex'],complete_source_preamble_hex=row['source_complete_preamble_hex'],
                    continuation_encoded_hex=pages[1]['encoded_hex'],pages=pages,unchanged_logical_English=row['english']))
            require({o['source_ID'] for o in owners}=={'DK4_MES_B84_R0470','DK4_MES_B84_R0539'},'onlytwo qualified FE owners')
            target,pagination=insert_FE_continuations(arm,target,owners,inventory)
            require(pagination==group['FE_pagination'],'complete qualified repeated-control inverse andrelative rebinding')
        require(sha(target)==group['target_sha256'] and target==Path(group['target_block']).read_bytes(),'independent source-bound whole block reconstruction')
        blocks[number]=target
        for row in (r for r in doc['records'] if r['block']==number):
            refs=row.get('planned_integrated_native_pages',[row['planned_integrated_reference']])
            for ref in refs:
                at=ref['offset'];raw=bytes.fromhex(ref['exact_stored_hex'])
                require(target[at:at+len(raw)+1]==raw+b'\0','individual full stored text')
            ref=row['planned_integrated_reference']
            require(ref['target_archive_sha256']==reconstruction['target_archive_sha256'],'individual complete archive reference')
            changes.append(dict(id=row['id'],file_path=path,block=number,new_offset=ref['offset'],kind=row['kind'],
                stored_sha256=sha(bytes.fromhex(ref['exact_stored_hex']))))
    result=IlnkContainer(blocks).to_bytes()
    require(sha(result)==reconstruction['target_archive_sha256'] and result==Path(reconstruction['target_archive']).read_bytes(),'whole tested archive')
    require({i for i,(a,b) in enumerate(zip(container.blocks,blocks,strict=True)) if a!=b}==set(conf['blocks']),'onlyreviewed blocks changed')
    inverse=list(blocks)
    for number in conf['blocks']:inverse[number]=container.blocks[number]
    require(IlnkContainer(inverse).to_bytes()==archive,'whole archive inverse')
    planned=deepcopy(image);planned.replace_file(path,result)
    require(sha(bytes(planned.rom.save()))==conf['target_ROM_sha256'],'complete ordered target')
    require([(p,q) for (_,p,a),(_,q,b) in zip(image.iter_files(),planned.iter_files(),strict=True) if p!=q or a!=b]==[(path,path)]
        and all(planned.read_file(p)==v for p,v in image.iter_components()),'all other files/components exact')
    restored=deepcopy(planned);restored.replace_file(path,archive)
    require(bytes(restored.rom.save())==before and bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before,'serialized parent inverse andpure callers')
    return planned.rom,dict(manuscripts=[conf['manuscript']],changed_records=changes,
        files=[dict(file_path=path,source_sha256=sha(archive),target_sha256=sha(result),changed_records=changes)],
        all_source_controls_commands_relatives_andunowned_bytes_preserved=True,
        source_owned_FE_continuations_not_additional_source_records=True,native_pages=336,native_commands=327,typed_labels=5,
        source_editorial_objects=330,fresh_relative_cases=140,native_loads=343,actual_frames=72406,
        representative_initialized_gameplay_not_natural_event_activation=True,
        canonical_stage_requires_registered_right_bound_runtime_layer=conf['right_bound_configuration'],
        no_completion_credit_orpromotion_granted=True,full_goal_complete=False)
