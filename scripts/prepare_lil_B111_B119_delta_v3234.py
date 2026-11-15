"""Bind unchanged native cases; rerender only the concrete phrase-flow change."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B111_B119_delta_tools_v3234')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/verify_lil_B111_B119_fonts_v3230b.py')
    new=Path('scripts/verify_lil_B111_B119_fonts_v3234b.py')
    assert not new.exists()
    text=old.read_text(encoding='utf-8')
    for a,b in [('lil_B111_B119_fonts_v3230b','lil_B111_B119_fonts_v3234b'),('lil_B111_B119_editorial_manuscript_v3.json','lil_B111_B119_editorial_manuscript_v4.json'),('lil_B111_B119_actor_style_manuscript_v2.json','lil_B111_B119_actor_style_manuscript_v3.json'),('lil_B111_B119_layout_v1','lil_B111_B119_layout_v2')]:
        assert a in text;text=text.replace(a,b)
    anchor='    cases=[];qa_reports=[];pictures=[];macro_calls=0'
    assert text.count(anchor)==1
    text=text.replace(anchor,"""    priorpath=Path('work/analysis/lil_B111_B119_fonts_v3230b/current_macro_QA_and_progressive_font_proof.json')
    prior=read(priorpath)
    assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['ARM9_sha256']==sha(arm) and prior['COMMON_sha256']==sha(common)
    for key,hashkey in [('manuscript','manuscript_sha256'),('actor_style_manuscript','actor_style_manuscript_sha256'),('scoped_profile','scoped_profile_sha256'),('native_formatter_module','native_formatter_module_sha256')]:
        assert sha(Path(prior[key]).read_bytes())==prior[hashkey]
    assert prior['scoped_profile']==doc['scoped_profile_module'] and prior['scoped_profile_sha256']==doc['scoped_profile_module_sha256']
    prior_rows={r['id']:r for p in [prior['manuscript'],prior['actor_style_manuscript']] for r in read(p)['records']}
    prior_cases={r['id']:r for r in prior['cases']}
    reused=0;changed=[]
"""+anchor)
    anchor="        if row['kind']=='system-FE':continue"
    assert text.count(anchor)==1
    text=text.replace(anchor,anchor+"""
        oldrow,oldcase=prior_rows[row['id']],prior_cases[row['id']]
        for key in ['block','current_hex','source_reference','current_reference','kind','english']:
            assert row[key]==oldrow[key],(row['id'],key)
        original_source=row.get('source_stored_alternative_hex',row['source_hex'])
        assert original_source==oldrow['source_hex']
        if row['kind']=='typed-4100-actor-style-alternative':
            assert row['virtual_formatter_prefix_hex']==oldrow['virtual_formatter_prefix_hex']
            assert row['style_indices']==oldrow['style_indices']
        caption=('selector'+row['source_presentation_prefix_hex']+' styles'+str(row['style_indices'])) if row['kind']=='typed-4100-actor-style-alternative' else 'selector'+row['source_presentation_prefix_hex']
        if result.encoded.hex()==oldcase['encoded_hex']:
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            cases.append({**oldcase,'reused_current_native_case':True,'reused_proof':str(priorpath),'reused_proof_sha256':sha(priorpath.read_bytes())})
            pictures.append((row['id'],caption,Image.open(oldcase['preview']).convert('RGB')))
            macro_calls+=8;reused+=1;continue
        changed.append(row['id'])
""")
    anchor='    negatives=[]'
    assert text.count(anchor)==1
    text=text.replace(anchor,"    assert changed==['DK4_MES_B111_R0112'] and reused==148,(changed,reused)\n"+anchor)
    anchor='        current_original_macro_alignment_calls=1192,'
    assert text.count(anchor)==1
    text=text.replace(anchor,"""        newly_executed_font_cases=149-reused,reused_unchanged_font_cases=reused,
        newly_executed_current_macro_alignment_cases=(149-reused)*8,reused_current_macro_alignment_cases=reused*8,
        reused_proof=str(priorpath),reused_proof_sha256=sha(priorpath.read_bytes()),changed_IDs=changed,
"""+anchor)
    new.write_text(text,encoding='utf-8')
    oldfe=Path('scripts/reconcile_lil_shrines_FE_v3184.py')
    newfe=Path('scripts/reconcile_lil_B111_B119_FE_v3235.py')
    assert not newfe.exists()
    t=oldfe.read_text(encoding='utf-8')
    swaps={'lil_Shrines_Temples_FE_v3184':'lil_B111_B119_FE_v3235',
        'lil_Shrines_Temples_FE_v3180':'lil_B111_B119_FE_v3231',
        'lil_shrines_temples_editorial_manuscript_v5.json':'lil_B111_B119_editorial_manuscript_v4.json',
        'lil_shrines_temples_profile':'lil_B111_B119_profile',
        'lil_shrines_temples_layout_v2':'lil_B111_B119_layout_v2',
        'assert len(cases)==30':'assert len(cases)==1',
        'all30_':'all1_',
        "'reused_unchanged_font_cases':30":"'reused_unchanged_font_cases':1",
        "'reused_current_macro_alignment_cases':240":"'reused_current_macro_alignment_cases':8",
        'all4_FE_sheets_viewed_and_hash_unchanged':'all1_FE_sheets_viewed_and_hash_unchanged',
        'Thirty complete FE planes/240macro cases':'One complete FE plane/8macro cases',
        'four viewed sheets hash-exact':'one viewed sheet hash-exact'}
    for a,b in swaps.items():assert a in t,a;t=t.replace(a,b)
    newfe.write_text(t,encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT/'bound_delta_tools_provenance.json',dict(previous={str(p):sha(p.read_bytes()) for p in [old,oldfe]},successors={str(p):sha(p.read_bytes()) for p in [new,newfe]},source_current_runtime_prose_prefix_alias_and_encoded_hash_binding=True,no_executed_producer_or_global_helper_modified=True,no_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Bound one-plane delta verifier and unchanged FE rebind prepared.')
