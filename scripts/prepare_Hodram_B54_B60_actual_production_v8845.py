"""Extend independent saved-capture reading to every main/focused page without recapturing scenes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_actual_production_tools_v8845');assert not root.exists()
    hydrated=derive('scripts/Hodram_B31_B53_verified_inputs_v8763.py','scripts/Hodram_B54_B60_verified_inputs_v8846.py',{
        'hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_names_v1':'hodram_B54_B60_names_v1',
        'review_Hodram_B31_B53_actual_v8744':'review_Hodram_B54_B60_actual_v8825',
        'translations/hodram_B31_B53_editorial_manuscript_v5.json':'translations/hodram_B54_B60_editorial_manuscript_v4.json',
        'translations/hodram_B31_B53_speaker_name_review_v3.json':'translations/hodram_B54_B60_speaker_name_review_v2.json',
        'Hodram_B31_B53_native_validation_v8754':'Hodram_B54_B60_native_validation_v8838',
        'Hodram_B31_B53_reference_validation_v8756':'Hodram_B54_B60_reference_validation_v8836',
        'Hodram_B31_B53_actual_review_v8744':'Hodram_B54_B60_actual_review_v8825',
        'six_complete_source_andstored_native_pages_two_current_progressive_names_andall_independent_pixels_exact':'all167_complete_source_andstored_native_pages_ten_current_progressive_names_andall_independent_pixels_exact',
        'positive_entire_archive_whole_reference_ROM_all323_unownedblocks_files_components_andallinverses':'positive_entire_archive_whole_reference_ROM_all318_unownedblocks_files_components_andallinverses',
        "m['expanded_native_hex']==m['input_hex'][2:]":"m['expanded_native_hex']==bytes.fromhex(m['input_hex'])[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet').hex()",
        "sha(plane)==p['native_plane_sha256'] and len(plane)==216*64":"sha(plane)==p['native_plane_sha256'] and len(plane)==(228*48 if m['source_selector']==254 else 216*64)",
        "pages.append(dict(deepcopy(p),native_plane_bytes=plane))":"page=dict(deepcopy(p),native_plane_bytes=plane)\n                if m['source_selector']==254:\n                    physical=Path(p['physical_plane']).read_bytes();assert len(physical)==228*64 and sha(physical)==p['physical_plane_sha256'];page['physical_plane_bytes']=physical\n                pages.append(page)",
        "set(native['names'])=={34,113}":"set(native['names'])=={1,20,23,24,36,84,113,114,119,141}",
    })
    old=Path('dk4tool/patch/hodram_B31_B53_actual_evidence_v1.py').read_text(encoding='utf-8')
    start=old.index("                model=native['bodies'][version][ident];page=model['pages'][0]")
    end=old.index('\n            require(not unknown',start)
    single=old[start:end]
    multi="""                model=native['bodies'][version][ident];require(model['source_selector']==actor,'actual glyph model source consumer')
                allholds=[];allpartial=[];allnameholds=[];page_selections=[]
                for page in model['pages']:
                    plane=page['native_plane_bytes']
                    if FE:
                        physical=page['physical_plane_bytes'];black={(i%228,i//228) for i,v in enumerate(physical) if v==15};gray=set();cpgray={(i%228,i//228) for i,v in enumerate(physical) if v==14};name=None
                    else:
                        black={(i%216,i//216) for i,v in enumerate(plane) if v==1};allgray={(i%216,i//216) for i,v in enumerate(plane) if v==15}
                        cp=oracle(arm,font,[e for e in page['events'] if e['kind']=='cp932']);cpgray={(i%216,i//216) for i,v in enumerate(cp) if v==15}&allgray;gray=allgray-cpgray;name=names[actor]
                    wanted=dict(zip(COLORS,[black,gray,cpgray],strict=True));holds=[];nameholds=[];partial=[]
                    for frame,photo in photos.items():
                        if not entry['frame']+20<frame<row['frame']-4:continue
                        pic=photo['image'];found={(x-16,y-276) for y in range(276,289) for x in range(14,244 if FE else 18+name['width']) if pic.getpixel((x,y))==COLORS[1]}
                        nameok=not found if FE else found==nameinks[actor]
                        if nameok:nameholds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],FE_absent_nameplate=FE))
                        diffs={str(color):len(photo['masks228' if FE else 'masks216'][color]^wanted[color]) for color in COLORS}
                        if any(diffs.values()) or not nameok:
                            sample=dict(frame=frame,body_differences=diffs,name_pixels=len(found),not_counted_as_complete=True)
                            if number!=56:sample['native_page']=page['page']
                            partial.append(sample);continue
                        holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=page['page'],complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal=True,complete_name_mask_equal=not FE,original_FE_absent_nameplate_preserved=FE,actual_name=None if FE else name['text'],native_geometry=[228 if FE else 216,64]))
                    require(holds,'complete actual body/name-orabsent-FE-header hold:'+ident+':page'+str(page['page']))
                    allholds.extend(holds);allpartial.extend(partial);allnameholds.extend(nameholds)
                    page_selections.append(dict(native_page=page['page'],complete_holds=holds,selected_capture=holds[-1]))
                nameholds=list({h['frame']:h for h in allnameholds}.values())
                speech=dict(id=ident,source_selector=actor,name=None if FE else name['text'],start=entry['frame'],returned=row['frame'],pages=len(model['pages']),complete_holds=allholds,nameholds=nameholds,partial_ortransition_samples=allpartial,selected_capture=allholds[-1],kind='system-FE' if FE else 'progressive')
                if number!=56:speech['page_selections']=page_selections
                speechrows.append(speech);totalholds+=len(allholds);page_occurrences+=len(model['pages'])
                observations[ident].append(dict(version=version,source_selector=actor,name=None if FE else name['text'],selected_capture=allholds[-1],complete_holds=len(allholds)))"""
    old_path="""            ids=['DK4_MES_B31_R0018'] if number==31 else ['DK4_MES_B53_R0007'];require(len(pairs)==(15 if number==31 else 17) and not any(p['word']==0x2100 for p in pairs),'whole block selected commands/one observed speech/no menu')
            path=[8,10,18,22,90,188,192] if number==31 else [8,10,12,98,106,114,122,130,132]"""
    paths={54:[8,10,38,54,118,128,136],56:[8,10,14,16,68,92,188],57:[8,10,12,26,44,66,98,126,158,184,214],58:[8,10,12,48,50,72,74,102,148,202,224,226,260,262,306,328,436,520,616,624,632,676,738,764,766,774,782,846,854,862,1260,1320,1348,1408,1436,1438,1448,1456,1464,1706,1718,1816,1826,1884,1958,2062,2166,2188,2234,2254,2320,2346,2354,2362,2432,2440,2448,2452,2460,2468,2472,2480,2488],59:[8,10,44,48,104,106,154,158,166,182,320,458,460,518],60:[8,10,72,82,204,294,420,434,562,650,696,720]}
    specs="[(54,'B54_actual'),(56,'B56_actual'),(57,'B57_actual'),(58,'B58_actual'),(59,'B59_actual'),(60,'B60_actual'),(60,'focus_actual')]"
    module=derive('dk4tool/patch/hodram_B31_B53_actual_evidence_v1.py','dk4tool/patch/hodram_B54_B60_actual_evidence_v1.py',{
        'B31/B53':'B54-B60',
        "len(source_commands)==9,'all9 original block commands'":"len(source_commands)=={54:7,56:7,57:11,58:98,59:14,60:12}[number],'all original block commands'",
        "len(selected_commands)==9":"len(selected_commands)==len(source_commands)",
        '(4 if number==31 else 0)':'(24 if number==58 else 0)',
        'len(objects)==9':'len(objects)==len(source_commands)',
        "[(31,'B31_actual'),(53,'B53_actual')]":specs,
        "scope='whole';canonical.update(check_fixtures(data,rows,parent,clean,rebuilt,require,number))":"scope='whole'\n        if (number,scope,'clean_Japanese') not in canonical:canonical.update(check_fixtures(data,rows,parent,clean,rebuilt,require,number))\n        expected_frames=7001 if key=='focus_actual' else {54:6001,56:7001,57:9001,58:16001,59:10001,60:10001}[number]",
        "group['actual_frames']==6001":"group['actual_frames']==expected_frames",
        "root=Path('work/analysis/Hodram_B31_B53_scene_runs_v8740')/f'route1_B{number}_{version}'":"root=Path('work/analysis/Hodram_B60_boundary_focus_runs_v8822' if key=='focus_actual' else 'work/analysis/Hodram_B54_B60_scene_runs_v8816')/f'route1_B{number}_{version}'",
        "report['frames']==6001":"report['frames']==expected_frames",
        'range(4000,5521,240)':"range(4000,6481 if key=='focus_actual' else {54:5521,56:6481,57:8401,58:15601,59:9601,60:9601}[number],240)",
        'if number==53:normal.update':'if number!=56:normal.update',
        single:multi,
        old_path:"            path="+repr(paths)+"[number]\n            ids=[r['id'] for r in f['declared']['original_text_records'] if r['source_reference']['header_offset'] in path]\n            require(len(pairs)==len(path)+8 and not any(p['word']==0x2100 for p in pairs),'whole block complete unforced selected commands/no typed menu')",
        "actual_pages=len(speechrows)":"actual_pages=sum(s['pages'] for s in speechrows),actual_frames=expected_frames,case='focus' if key=='focus_actual' else 'main'",
        "row['actual_observation_status']=='paired-whole-script-body-name-andportrait-observed'":"row['actual_observation_status']=='paired-initialized-whole-script-every-page-observed'",
        "data['actual_review']['offline_only_text_IDs']==['DK4_MES_B31_R0013']":"data['actual_review']['offline_only_text_IDs']==sorted(k for k,v in observations.items() if not v)",
        'two observed utterances andone explicitly unvisited short variant':'63 observed utterances and19 explicitly offline-only utterances',
        'len(results)==4 and page_occurrences==4 and totalholds==76':'len(results)==14 and page_occurrences==150 and totalholds==676',
        'four actual groups/four page occurrences/76 complete body-name holds':'14 actual groups/150 page occurrences/676 complete body-name-orFE holds',
        'whole_actual_frames=24004,complete_actual_page_occurrences=4,complete_actual_holds=76,unique_speech_IDs=2':'whole_actual_frames=130014,complete_actual_page_occurrences=150,complete_actual_holds=676,unique_speech_IDs=63',
        'all18_original_commands_retained_unforced_selected_paths_andnormal_resultword_channels_verified':'all152_original_commands_retained_infixtures_unforced_selected_paths_andnormal_resultword_channels_verified',
    })
    validation=derive('scripts/validate_Hodram_B31_B53_actual_v8764.py','scripts/validate_Hodram_B54_B60_actual_v8847.py',{
        'hodram_B31_B53_actual_evidence_v1':'hodram_B54_B60_actual_evidence_v1',
        'Hodram_B31_B53_verified_inputs_v8763':'Hodram_B54_B60_verified_inputs_v8846',
        'Hodram_B31_B53_actual_validation_v8764':'Hodram_B54_B60_actual_validation_v8847',
        'B31/B53 actual production:':'B54-B60 actual production:','Frozen Hodram-B31-B53 contract changed':'Frozen Hodram-B54-B60 contract changed',
        '==[24004,4,76,2]':'==[130014,150,676,63]',
        "len(result['canonical_fixtures'])==4":"len(result['canonical_fixtures'])==12",
        'rebuilt,require,31)':'rebuilt,require,54)',
        "['B31_actual']":"['B54_actual']","['B53_actual']":"['B60_actual']",
        "__setitem__(1,0)":"__setitem__(1,1)",
        "d['B31_actual']['groups'][0].__setitem__('unvisited_conditional_text_IDs',[])":"d['B58_actual']['groups'][0].__setitem__('unvisited_conditional_text_IDs',[])",
        "n['names'][34]":"n['names'][1]",
        "r[0].__setitem__('actual_observation_status','paired-whole-script-body-name-andportrait-observed')":"r[4].__setitem__('actual_observation_status','paired-initialized-whole-script-every-page-observed')",
        '    assert len(cases)==13 and':"    reject('wrong-focused-run-length',lambda d,n,r:d['focus_actual']['groups'][0].__setitem__('actual_frames',7000))\n    reject('missing-English-continuation-page-selection',lambda d,n,r:next(s for s in d['B59_actual']['groups'][1]['speeches'] if s['pages']==2)['page_selections'].pop())\n    reject('invented-FE-speaker-header',lambda d,n,r:next(s for s in d['B56_actual']['groups'][0]['speeches'] if s['source_selector']==254).__setitem__('name','Girl'))\n    assert len(cases)==16 and",
        'all_four_whole_fixture_inverses_all_saved_trace_fields_body_name_holds_andnormal_returns_independently_checked':'all_twelve_whole_fixture_inverses_fourteen_saved_runs_all_pages_FE_body_name_holds_andnormal_returns_independently_checked',
        'short_B31_R0013_still_offline_only_no_predicates_orflags_forced':'B55_and18_B58_conditionals_still_offline_only_no_predicates_orflags_forced',
        'Actual production:4whole fixture inverses/24004saved frames/76complete holds/4pages/2utterances pass;13semantic defects reject. ShortB31 offline only;no captures,ROMcommit orcredit.':'Actual production:12whole fixture inverses/14saved runs130014frames/676complete holds/150pages/63utterances pass;16semantic defects reject.19offline only;no captures,ROMcommit orcredit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_actual_production.json',dict(hydration=hydrated,module=module,validation=validation,all_original_native_CPU_resident_payload_readonly_observer_input_schedule_wholefixture_andinverse_guards_preserved=True,each_continuation_page_requires_independent_complete_glyph_andname_hold=True,FE_original_absentheader_andlogical_physical_masks_preserved=True,all_original_source_selected_paths_explicitly_pinned_without_invented_query_effect_semantics=True,no_new_capture_producer_replay_orcredit=True,new_credit=0,full_goal_complete=False))
