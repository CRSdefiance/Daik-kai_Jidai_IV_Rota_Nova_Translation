"""Pure integration of the two already-reviewed ordered Help groups with exact page provenance."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.dialogue.reviewed_help_pages_v12 import plan_articles as deck_plan
from dk4tool.dialogue.reviewed_help_pages_v16 import plan_articles as remaining_plan
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load

def require(value,message):
    if not value:raise ValueError('Remaining Help release: '+message)

def plan_release(image,baseline,config_path):
    conf=load(config_path);require(conf['format']=='dk4-reviewed-remaining-help-release-v1','schema')
    kind=conf['kind'];require(kind in ['deck31','remaining67'],'exact qualified Help group')
    deck=kind=='deck31';count,pagecount,rev,ret=(31,31,11,20) if deck else (67,72,7,60)
    topics=({33}|set(range(103,133))) if deck else (set(range(133,202))-{181,184})
    before,base_before=bytes(image.rom.save()),bytes(baseline.rom.save())
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'changed dependency: '+path)
    require(sha(before)==conf['parent_ROM_sha256'],'complete ordered predecessor')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical input')
    require(sha(image.read_file('/__arm9__.bin'))==conf['pre_runtime_ARM9_sha256'],'pre-runtime ARM9')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean Japanese input')
    clean=NdsImage.open(conf['clean_ROM'])
    doc,plan,native,visual,actual,actual_visual=[load(conf[k]) for k in ['manuscript','plan','native','visual','actual','actual_visual']]
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US','American English contextual policy')
    require(len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count']==count,'complete unique source articles')
    require({r['topic_id'] for r in doc['records']}==topics,'exact reviewed article membership')
    require((sum(r['decision']=='revision' for r in doc['records']),sum(r['decision']=='retention' for r in doc['records']))==(rev,ret),'individual dispositions')
    for row in doc['records']:
        require(all(row['review'].get(g) is True for g in REQUIRED_REVIEW_GATES),'all five individual gates')
        require(all(str(row.get(k,'')).strip() for k in ['speaker','context','source_meaning','localization_note','finding']),'individual source/context/finding')
        require(row['decision'] in ['revision','retention'] and (row['decision']!='retention' or bool(row['retention_reason'])),'justified individual retention')
    require(native['native_pages']==pagecount and native['complete_articles']==count,'all native pages/articles')
    require(native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass'] and
        native['all_executed_current_instruction_bytes_exact'],'complete native glyphs,links,bounds andsource code')
    require(native['current_ARM9_sha256']==conf['final_runtime_ARM9_sha256'],'qualified final renderer')
    require((visual.get('all31_pages_approved') if deck else visual.get('all72_pages_approved')) is True,'all generated pages visually approved')
    require(actual['actual_ordinary_controls_no_state_injection'] and not actual['full_story_playthrough'] and not actual['hardware'],'honest ordinary Help coverage')
    if deck:
        require(visual['all31_pages_approved'] and actual_visual['all9_fresh_observed_pages_approved'] and
            actual_visual['all_three_fresh_actual_sheets_directly_viewed'] and actual_visual['exact_prior_actual_pages_reused']==22,'fresh andexact reused visual evidence')
        require(doc['all31_individual_five_gates_pass'] and doc['new_source_records']==30 and doc['previously_credited_amendments']==[33],'30 new articles pluszero-credit Coerce33')
        cases=actual_visual['cases'];require(len(cases)==31 and sum(c['exact_prior_observation_reused'] for c in cases)==22,'disjoint9 fresh/22 exact prior actual pages')
    else:
        require((actual['actual_pages'],actual['actual_articles'],actual['offline_only_pages'])==(25,20,47),'25 observed versus47 offline-only pages')
        require(len(actual['original_forward_back_andL_R_history_returns'])==15 and actual_visual['all25_observed_pages_approved'] and
            actual_visual['all_seven_actual_sheets_directly_viewed'],'five continuations andnative history returns')
        cases=actual['actual_HELP_cases'];require(len(cases)==25,'individual observed membership')
    for proof_path,proof in [(conf['native'],native),(conf['actual'],actual)]:
        for path,digest in proof['evidence'].items():require(sha(Path(path).read_bytes())==digest,'changed proof input: '+path)
    require(actual_visual['actual_proof_sha256']==sha(Path(conf['actual']).read_bytes()),'actual approval identity')
    path=doc['file_path'];require(path=='/COMMON/HELP.DK4','owned Help resource')
    resource,compiled=(deck_plan if deck else remaining_plan)(doc,clean.read_file(path),baseline.read_file(path),image.read_file(path))
    require(compiled['pages']==plan['pages'] and resource==Path(conf['target_resource']).read_bytes(),'fresh compiler equals every reviewed page')
    require(sha(resource)==conf['target_HELP_sha256'],'whole tested resource')
    target=IlnkContainer.parse(resource).blocks
    require(len(target)==217 and target[203]==b'\0','native topic/sentinel contract')
    expected_pairs=[] if deck else [dict(article=a,page_ids=[a,b]) for a,b in [(133,209),(139,210),(150,206),(151,207),(168,208)]]
    require(compiled['compiler_generated_navigation_pairs']==expected_pairs,'source-bound continuation ownership')
    native_byid={r['topic_id']:r for r in native['records']};actual_byid={r['topic_id']:r for r in cases}
    require(len(native_byid)==pagecount and set(native_byid)=={p['topic_id'] for p in compiled['pages']},'individual native membership')
    require(set(actual_byid)=={p['block'] for r in doc['records'] for p in r['planned_stored_pages'] if 'actual_frame' in p},'individual actual membership')
    # Group by original research ROM so each dependency image is opened only once.
    proof_roms={}
    for case in cases:
        rom=case['research_ROM'] if deck else actual['research_ROM'];digest=case['research_ROM_sha256'] if deck else actual['research_ROM_sha256']
        proof_roms.setdefault((rom,digest),[]).append(case)
    reference=NdsImage.open(conf['final_dependency_ROM'])
    require(sha(Path(conf['final_dependency_ROM']).read_bytes())==conf['final_dependency_ROM_sha256'],'verified renderer dependency ROM')
    for (rom,digest),members in proof_roms.items():
        require(sha(Path(rom).read_bytes())==digest,'actual research ROM identity')
        observed=NdsImage.open(rom)
        require(all(observed.read_file(p)==reference.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']),'actual renderer/UI/font dependencies exact')
        observed_pages=IlnkContainer.parse(observed.read_file(path)).blocks
        for case in members:
            require(observed_pages[case['topic_id']]==target[case['topic_id']],'actual page bytes equal current target')
            require(case['all_first_internal_final_glyphs_andblank_gaps_exact'],'complete actual glyphs/blank guards')
            require(sha(Path(case['capture']).read_bytes())==case['capture_sha256'] and
                sha(Path(case['RAM']['path']).read_bytes())==case['RAM']['sha256'],'actual image/RAM evidence')
    changes=[]
    for row in doc['records']:
        pages=[p for p in compiled['pages'] if p['source_article_id']==row['topic_id']]
        require(len(pages)==len(row['planned_stored_pages']),'complete individual page references')
        for page,ref in zip(pages,row['planned_stored_pages'],strict=True):
            topic=page['topic_id'];raw=bytes.fromhex(page['encoded_hex']);nr=native_byid[topic]
            require(ref['block']==topic and raw.hex()==ref['exact_stored_hex']==nr['encoded_hex'],'stored/native individual bytes')
            require(resource[ref['archive_offset']:ref['archive_offset']+ref['bytes']]==raw==target[topic] and
                ref['target_archive_sha256']==sha(resource),'exact complete archive reference')
            require(sha(Path(nr['preview']).read_bytes())==nr['preview_sha256'],'viewed native preview')
            if topic in actual_byid:require(ref['actual_frame']==actual_byid[topic]['frame'],'exact individual observed frame')
            else:require(row['offline_only'] and 'actual_frame' not in ref,'offline content hasno invented actual claim')
        changes.append(dict(id=row['id'],file_path=path,topic_id=row['topic_id'],source_reference=row['source_reference'],
            current_reference=row['current_reference'],planned_stored_pages=row['planned_stored_pages'],decision=row['decision']))
    planned=deepcopy(image);planned.replace_file(path,resource)
    require([(p,q) for (_,p,a),(_,q,b) in zip(image.iter_files(),planned.iter_files(),strict=True) if p!=q or a!=b]==[(path,path)]
        and all(planned.read_file(p)==v for p,v in image.iter_components()),'all other files/components exact')
    inverse=deepcopy(planned);inverse.replace_file(path,image.read_file(path))
    require(bytes(inverse.rom.save())==before,'complete serialized parent inverse')
    require(sha(bytes(planned.rom.save()))==conf['target_ROM_sha256'],'complete ordered target')
    require(bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before,'pure caller preservation')
    return planned.rom,dict(manuscripts=[conf['manuscript']],changed_records=changes,
        files=[dict(file_path=path,source_sha256=sha(image.read_file(path)),target_sha256=sha(resource),changed_records=changes)],
        articles=count,pages=pagecount,new_source_articles=30 if deck else 67,previously_credited_amendments=[33] if deck else [],
        actual_pages=31 if deck else 25,offline_only_pages=0 if deck else 47,
        composite_actual_provenance_not_one_full_final_ROM_playthrough=True,
        all_individual_source_current_final_refs_five_gates_native_visual_andactual_oroffline_bound=True,
        complete_parent_inverse_andall_unowned_files_components_exact=True,new_credit=0)
