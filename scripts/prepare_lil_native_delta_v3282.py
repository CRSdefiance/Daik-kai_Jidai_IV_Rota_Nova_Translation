"""Repaint changed native planes, bind exact unchanged source/current cases."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B122_B127_delta_tools_v3282');assert not root.exists()
    old=Path('scripts/verify_lil_B122_B127_fonts_v3277.py');new=Path('scripts/verify_lil_B122_B127_fonts_v3283.py');assert not new.exists()
    text=old.read_text(encoding='utf-8').replace('lil_B122_B127_fonts_v3277','lil_B122_B127_fonts_v3283').replace('lil_B122_B127_editorial_manuscript_v3.json','lil_B122_B127_editorial_manuscript_v4.json').replace('lil_B122_B127_layout_v1','lil_B122_B127_layout_v2')
    anchor='    cases=[];qa_reports=[];pictures=[];macro_calls=0';assert text.count(anchor)==1
    text=text.replace(anchor,'''    priorpath=Path('work/analysis/lil_B122_B127_fonts_v3277/current_macro_QA_and_progressive_font_proof.json')
    prior=read(priorpath);priorrows={r['id']:r for r in read(prior['manuscript'])['records']};priorcases={r['id']:r for r in prior['cases']}
    assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['ARM9_sha256']==sha(arm) and prior['COMMON_sha256']==sha(common)
    for key,hashkey in [('manuscript','manuscript_sha256'),('scoped_profile','scoped_profile_sha256'),('native_formatter_module','native_formatter_module_sha256')]:assert sha(Path(prior[key]).read_bytes())==prior[hashkey]
    assert Path(prior['scoped_profile'])==Path(doc['scoped_profile_module']) and prior['scoped_profile_sha256']==doc['scoped_profile_module_sha256']
    reused=0;changed=[]
'''+anchor)
    anchor="        if row['kind']=='system-FE':continue";assert text.count(anchor)==1
    text=text.replace(anchor,anchor+'''
        oldrow,oldcase=priorrows[row['id']],priorcases[row['id']]
        for key in ['block','current_hex','source_hex','source_reference','current_reference','kind','english','source_presentation_prefix_hex']:assert row[key]==oldrow[key],(row['id'],key)
        if result.encoded.hex()==oldcase['encoded_hex']:
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            cases.append({**oldcase,'reused_current_native_case':True,'reused_proof':str(priorpath),'reused_proof_sha256':sha(priorpath.read_bytes())})
            pictures.append((row['id'],'selector'+row['source_presentation_prefix_hex'],Image.open(oldcase['preview']).convert('RGB')))
            macro_calls+=8;reused+=1;continue
        changed.append(row['id'])
''')
    anchor='        current_original_macro_alignment_calls=1160,';assert text.count(anchor)==1
    text=text.replace(anchor,"        reused_proof=str(priorpath),reused_proof_sha256=sha(priorpath.read_bytes()),newly_executed_font_cases=145-reused,reused_unchanged_font_cases=reused,newly_executed_current_macro_alignment_cases=(145-reused)*8,reused_current_macro_alignment_cases=reused*8,changed_IDs=changed,\n"+anchor)
    text=text[:text.rindex('    print(')]+"    print(dict(complete_planes=145,newly_painted=145-reused,reused=reused,changed=changed,macro_cases=1160,credit=0))\n"
    compile(text,str(new),'exec');new.write_text(text,encoding='utf-8')
    fold=Path('scripts/verify_lil_B122_B127_FE_v3278.py');fnew=Path('scripts/verify_lil_B122_B127_FE_v3284.py');assert not fnew.exists()
    text=fold.read_text(encoding='utf-8').replace('lil_B122_B127_FE_v3278','lil_B122_B127_FE_v3284').replace('lil_B122_B127_editorial_manuscript_v3.json','lil_B122_B127_editorial_manuscript_v4.json').replace('lil_B122_B127_layout_v1','lil_B122_B127_layout_v2')
    compile(text,str(fnew),'exec');fnew.write_text(text,encoding='utf-8')
    root.mkdir(parents=True);save(root/'exact_native_delta_provenance.json',dict(previous={str(p):sha(p.read_bytes()) for p in [old,fold]},successors={str(p):sha(p.read_bytes()) for p in [new,fnew]},only_changed_progressive_planes_and_macro_cases_reexecuted=True,all_ten_FE_current_planes_reexecuted_for_final_formatter=True,choices_exact_labels_bound_separately_without_redundant_VM_run=True,no_ROM_registry_orcredit=True,producer_sha256=sha(Path(__file__).read_bytes())))
