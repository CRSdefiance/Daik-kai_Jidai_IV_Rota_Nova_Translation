"""Bind unchanged planes;repaint only three concrete phrase-flow refinements."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B131_B133_delta_tools_v3324');assert not root.exists();old=Path('scripts/verify_lil_B131_B133_fonts_v3319.py');new=Path('scripts/verify_lil_B131_B133_fonts_v3324b.py');assert not new.exists()
    t=old.read_text(encoding='utf-8').replace('lil_B131_B133_fonts_v3319','lil_B131_B133_fonts_v3324b').replace('lil_B131_B133_editorial_manuscript_v2.json','lil_B131_B133_editorial_manuscript_v3.json').replace('lil_B131_B133_layout_v1','lil_B131_B133_layout_v2')
    a='    cases=[];qa_reports=[];pictures=[];macro_calls=0';assert t.count(a)==1
    t=t.replace(a,'''    priorpath=Path('work/analysis/lil_B131_B133_fonts_v3319/current_macro_QA_and_progressive_font_proof.json');prior=read(priorpath)
    assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['ARM9_sha256']==sha(arm) and prior['COMMON_sha256']==sha(common)
    for key,hashkey in [('manuscript','manuscript_sha256'),('scoped_profile','scoped_profile_sha256'),('native_formatter_module','native_formatter_module_sha256')]:assert sha(Path(prior[key]).read_bytes())==prior[hashkey]
    assert Path(prior['scoped_profile'])==Path(doc['scoped_profile_module']) and prior['scoped_profile_sha256']==doc['scoped_profile_module_sha256']
    priorrows={r['id']:r for r in read(prior['manuscript'])['records']};priorcases={r['id']:r for r in prior['cases']};reused=0;changed=[]
'''+a)
    a="        if row['kind']=='system-FE':continue";assert t.count(a)==1
    t=t.replace(a,a+'''
        oldrow,oldcase=priorrows[row['id']],priorcases[row['id']]
        for key in ['block','current_hex','source_hex','source_reference','current_reference','kind','english','source_presentation_prefix_hex']:assert row[key]==oldrow[key],(row['id'],key)
        if result.encoded.hex()==oldcase['encoded_hex']:
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            cases.append({**oldcase,'reused_current_native_case':True,'reused_proof':str(priorpath),'reused_proof_sha256':sha(priorpath.read_bytes())});pictures.append((row['id'],'selector'+row['source_presentation_prefix_hex'],Image.open(oldcase['preview']).convert('RGB')));macro_calls+=8;reused+=1;continue
        changed.append(row['id'])
''')
    a='        current_original_macro_alignment_calls=480,';assert t.count(a)==1
    t=t.replace(a,"        reused_proof=str(priorpath),reused_proof_sha256=sha(priorpath.read_bytes()),newly_executed_font_cases=60-reused,reused_unchanged_font_cases=reused,newly_executed_current_macro_alignment_cases=(60-reused)*8,reused_current_macro_alignment_cases=reused*8,changed_IDs=changed,\n"+a)
    t=t[:t.rindex('    print(')]+"    print(dict(complete_planes=60,newly_painted=60-reused,reused=reused,changed=changed,macro_cases=480,credit=0))\n";compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    fold=Path('scripts/verify_lil_B131_B133_FE_v3320.py');fnew=Path('scripts/verify_lil_B131_B133_FE_v3325.py');assert not fnew.exists();t=fold.read_text(encoding='utf-8').replace('lil_B131_B133_FE_v3320','lil_B131_B133_FE_v3325').replace('lil_B131_B133_editorial_manuscript_v2.json','lil_B131_B133_editorial_manuscript_v3.json').replace('lil_B131_B133_layout_v1','lil_B131_B133_layout_v2');compile(t,str(fnew),'exec');fnew.write_text(t,encoding='utf-8')
    root.mkdir(parents=True);save(root/'bound_native_delta_successors.json',dict(previous={str(p):sha(p.read_bytes()) for p in [old,fold]},successors={str(p):sha(p.read_bytes()) for p in [new,fnew]},unchanged_source_current_English_and_exact_encoded_planes_bound_without_repainting=True,all_earlier_producers_unchanged=True,no_ROM_orcredit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
