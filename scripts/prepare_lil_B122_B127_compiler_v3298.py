"""Create a guarded speech/two-choice successor; earlier stages stay exact."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('dk4tool/patch/lil_B111_B119_editorial.py')
NEW=Path('dk4tool/patch/lil_B122_B127_editorial.py')
ROOT=Path('work/analysis/lil_B122_B127_compiler_tools_v3298')
if __name__=='__main__':
    assert not NEW.exists() and not ROOT.exists();t=OLD.read_text(encoding='utf-8')
    for a,b in [('lil_B111_B119','lil_B122_B127'),('B111-B119','B122-B127'),('range(111,120)','range(122,128)'),('lil_B122_B127_profile import','lil_B122_B127_profile_v2 import'),("doc,voice=[load(config[k]) for k in ['manuscript','actor_styles']]","doc,menu=[load(config[k]) for k in ['manuscript','choices']]"),('for d in [doc,voice]:','for d in [doc,menu]:')]:assert a in t,a;t=t.replace(a,b)
    a=t.index('    for key in [\'all305_');z=t.index('    representative=load(',a)
    t=t[:a]+'''    for key in ['all312_physical_nested_command_boundaries_and64_relative_sites_verified',
        'all320_relocated_relative_skip_cases_preserve_original_targets',
        'all14_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM',
        'all155_active_speech_targets_preserved','two2100_objects_four_labels_and_source_indices_0_1_cancel_verified',
        'two_original2000_pause_words_and_mapped_resume_boundaries_verified',
        'trade_choice0_tutorial_choice1_already_know_branch_and_return0_both_VM_modes_verified',
        'no_dynamic_selector_or4100_objects','representative_shared_rules_approved']:
        _require(mapping.get(key) is True,'missing reference approval:'+key)
    _require(mapping['original_event_queries']==[],'unexpected event query')
'''+t[z:]
    t=t.replace("and representative.get('current4100_actual5_prefixes_all34_bodies_all48_aliases_and_all207_catalog_styles_bound') is True","and representative.get('two2100_menus_source_order_indices_geometry_complete_planes_and_selection_cancel_bound') is True\n        and representative.get('both_mapped_pause_resumption_boundaries_exact') is True\n        and representative.get('trade_tutorial_and_already_know_branch_native_paths_and_both_return_modes_bound') is True")
    a=t.index('    _require(len(FE[\'cases\'])');z=t.index('    context=load(',a)
    t=t[:a]+'''    _require(len(FE['cases'])==10 and FE['ARM9_sha256']==sha(arm)
        and FE['all10_one_native_page_consumes_complete_target']
        and FE['all10_complete_native_independent_planes_all_glyphs_and_canaries_equal']
        and len(FE['source_leading_vertical_staging_cases'])==7 and len(FE['source_FI_null_actor_cases'])==3,
        'complete distinct FE contract required')
    _require(controls['all14_predicate_current_relocated_results_and_source_operands_equal']
        and controls['all10_FE_preserve_original_null_actor_before_dynamic_fallback']
        and controls['all155_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text']
        and len(controls['relocated_predicate_pairs'])==14 and controls['original_event_queries']==[],
        'relocated predicate/FE/dispatch approval required')
    branch=load(doc['conditional_return_proof']);wait=load(doc['original2000_wait_proof'])
    _require(sha(Path(doc['conditional_return_proof']).read_bytes())==doc['conditional_return_proof_sha256']
        and branch['source_current_target_branch_endings_preserved']
        and branch['selection0_skips_already_know_return_and_reaches_tutorial']
        and branch['selection1_enters_already_know_branch_and_return0']
        and len(branch['conditional_native_paths'])==6 and len(branch['original_VM_return_cases'])==12,
        'original tutorial/already-know branch return proof required')
    _require(sha(Path(doc['original2000_wait_proof']).read_bytes())==doc['original2000_wait_proof_sha256']
        and wait['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence']
        and wait['all3_historical_pause_captures_viewed'],'source2000 actual-rule binding required')
    menu_native=load(doc['native_choice_proof']);menu_targets={}
    _require(menu_native['complete_current_and_reviewed_style_label_planes']==16
        and menu_native['native_selection_cancel_cases']==12,'complete two-menu native proof required')
    for m in menu_native['menus']:
        _require(sha(Path(m['proof']).read_bytes())==m['sha256'],'menu proof hash differs')
        detail=load(m['proof']);target=next(c for c in detail['current_and_reviewed_VM_and_font_cases'] if c['version']=='reviewed-research')
        menu_targets[(detail['block'],detail['original_command_offset'])]=target['object_hex']
    _require(len(menu_targets)==2,'two approved two-option objects required')
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    _require(len(doc['records'])==len(refs)==155 and {r['id'] for r in doc['records']}==set(refs),'155speech coverage differs')
    _require(len(fonts)==155 and set(fonts)==set(refs),'155complete native cases required')
    _require(len(menu['records'])==len({r['id'] for r in menu['records']})==4,'four choice labels required')
    _require(sorted(b['block'] for b in mapping['blocks'])==BLOCKS,'six exact blocks required')
'''+t[z:]
    t=t.replace('sum(expected_commands.values())==305','sum(expected_commands.values())==312').replace('used_styles=set()','used_choices=set()').replace('raw[0] in {2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220,254}','raw[0] in {2,6,9,20,26,92,95,151,254}')
    a=t.index("        for ref in spec['actor_style_commands']:");z=t.index('        patches.sort(',a)
    t=t[:a]+'''        _require(spec['actor_style_commands']==[],'unexpected actor-style object')
        for ref in spec['choice_commands']:
            at,length=ref['old_offset'],ref['old_length']
            _require(block[at:at+2]==original[at:at+2]==b'\\0\\x21','source two-option opcode differs')
            rows=sorted([r for r in menu['records'] if r['block']==n and r['command_offset']==at],key=lambda r:r['option_index'])
            _require([r['option_index'] for r in rows]==[0,1],'all2 ordered choices required')
            chunks=[];offsets=[];cursor=0
            for row in rows:
                ident=row['id'];i=row['option_index'];body_at,source_at,before,raw=bind_row(row)
                _require(ident not in used_choices and body_at==at+6+struct.unpack_from('<H',block,at+2+2*i)[0]
                    and source_at==at+6+struct.unpack_from('<H',original,at+2+2*i)[0],'choice source/index differs:'+ident)
                used_choices.add(ident);value=row['english'].encode('ascii')
                _require(value and value.strip()==value and all(32<=c<=126 for c in value) and b'{' not in value and b'}' not in value
                    and value.hex()==row['compiled_hex'],'choice must be reviewed plain ASCII:'+ident)
                offsets.append(cursor);chunk=value+b'\\0';chunk+=b'\\0'*(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
                r=ref['label_references'][i]
                _require(r['id']==ident and r['option_index']==i and r['new_length']==len(value),'choice target reference differs')
                changes.append(dict(id=ident,file_path=PATH,block=n,kind='choice',choice_command_offset=at,
                    option_index=i,old_offset=body_at,old_bytes=len(before),new_bytes=len(value),new_offset=r['new_offset']))
            value=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
            _require(value.hex()==ref['target_hex']==menu_targets[(n,at)] and len(value)==ref['new_length']
                and all(r['typed_target_object_hex']==value.hex() for r in rows),'approved two-option object differs')
            patches.append(dict(start=at,end=at+length,old=block[at:at+length],value=value))
'''+t[z:]
    t=t.replace('0x4100,0x2200','0x4100,0x2100')
    a=t.index('        if n==115:');z=t.index("        _require(sha(target)",a)
    t=t[:a]+'''        _require(len(spec['original2000_pause_and_resume_maps'])==(2 if n==122 else 0),'source pause census differs')
        for p in spec['original2000_pause_and_resume_maps']:
            a,z=p['old_offset'],p['new_offset'];resume=p['target_resume']
            _require(block[a:a+2]==original[a:a+2]==target[z:z+2]==b'\\0\\x20'
                and z==_mapped(patches,a) and p['source_resume']==a+2
                and resume==z+2==_mapped(patches,a+2) and resume in boundaries,'source2000 pause/resume differs')
        if n==126:
            for a in [336,954]:
                z=_mapped(patches,a)
                _require(block[a:a+4]==original[a:a+4]==target[z:z+4]==bytes(4),'conditional/final return0 differs')
'''+t[z:]
    a=t.index("            elif r['kind']=='actor-style':");z=t.index('        restored=bytearray(logical)',a)
    t=t[:a]+'''            elif r['kind']=='choice':
                a=_mapped(patches,r['choice_command_offset'])
                _require(r['new_offset']==a+6+struct.unpack_from('<H',target,a+2+2*r['option_index'])[0],'relocated choice pointer differs')
            else:raise ValueError('Unexpected ownership kind')
'''+t[z:]
    t=t.replace("actor_style_objects=len(spec['actor_style_commands']),three_option_menus=len(spec['choice_commands'])","two_option_menus=len(spec['choice_commands']),original2000_pauses=len(spec['original2000_pause_and_resume_maps'])")
    a=t.index('    _require(used_styles==');z=t.index('    result=container.to_bytes()',a)
    t=t[:a]+"    _require(used_choices=={r['id'] for r in menu['records']} and len(changes)==len({r['id'] for r in changes})==159,'incomplete editorial coverage')\n"+t[z:]
    a=t.index('        manuscript=config[\'manuscript\'],actor_styles=');t=t[:a]+'''        manuscript=config['manuscript'],choices=config['choices'],reference_map=config['reference_map'],
        changed_records=changes,blocks=reports,only_SC2_selected_six_blocks_changed=True,all330_other_SC2_blocks_unchanged=True,
        all155_speeches_four_choice_labels64_relative_operands_verified=True,
        both2000_pause_resume_boundaries_and_trade_return0_verified=True,
        both2100_menu_counts_indices01_cancel_and_native_planes_verified=True,
        native_code_and123040_staged_payload_unchanged=True)
'''
    t=t.replace('Source/runtime-locked speeches, aliased actor styles and three-option menus.','Source/runtime-locked155 speeches,two two-option menus andtwo source pauses.')
    compile(t,str(NEW),'exec');NEW.write_text(t,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'guarded_compiler_provenance.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),no_previous_release_stage_or_global_helper_modified=True,all155_speech_four_labels_both_source_pauses_conditional_returns_and64_spans_guarded=True,compiler_registration_negatives_and_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Guarded159-target compiler prepared;registration negatives and registered build pending.')
