"""Source-lock fourteen clean utterances, both approved speakers and the distinct original FE consumer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_source_display_tools_v8386');assert not root.exists();s=Path('scripts/prove_Hodram_B47_B48_source_display_v8316b.py').read_text('utf8');a=s.index('    identity=next(');b=s.index('    progressive=',a);c=s.index('        clean_current_Lil_fields=');d=s.index('        no_FE_actor254',c)
    identities='''    identities=[next(r for r in oldnames['complete_clean_andcurrent_name_fields'] if r['actor_ID']==actor) for actor in [1,2]]
    for identity in identities:
        for version,im in [('clean_fields',clean),('current_fields',image)]:
            code=im.read_file('/__arm9__.bin')
            for f in identity[version]:
                at=f['table_field'];assert code[at:at+4].hex()==f['table_field_hex']
                if f['pointer']:
                    off=f['offset'];raw=bytes.fromhex(f['hex']);assert code[off:off+len(raw)+1]==raw+b'\\0'
    assert [f.get('text') for f in identities[1]['clean_fields']]==['リル','アーゴット',None]
    assert [[f.get('text') for f in r['current_fields']] for r in identities]==[['Hodram','Bergstrom',None],['Lil','Argot',None]]
    getters=[r for r in names['native_twelve_progressive_andfull_getters']['rows'] if r['actor_ID'] in [1,2]]
    assert len(getters)==4 and all(r['text']=={1:'Hodram Bergstrom',2:'Lil Argot'}[r['actor_ID']] for r in getters)
    nameplanes=[r for r in names['name_planes'] if r['actor_ID'] in [1,2]];assert len(nameplanes)==2
    for name in nameplanes:assert sha(Path(name['native_plane']).read_bytes())==name['native_plane_sha256']
'''
    result=derive('scripts/prove_Hodram_B47_B48_source_display_v8316b.py','scripts/prove_Hodram_B49_source_display_v8386.py',{
        'Hodram_B47_B48_source_display_v8316b':'Hodram_B49_source_display_v8386',
        'work/analysis/Hodram_B47_B48_clean_gloss_v8312/six_first_clean_glosses_both_race_outcomes_FE_FI_andAmsterdam_wait_direction.json':'work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json',
        "gloss['all_six_clean_utterances_glossed_before_current_English']":"gloss['all14_clean_utterances_andtwo_choices_glossed_before_current_English']",
        "gloss['no_current_English_translation_comparison_rewrite_formatting_orname_approval']":"gloss['no_current_English_comparison_localized_revision_name_item_approval_orcompletion_credit']",
        s[a:b]:identities,s[c:d]:"        clean_current_scoped_fields=identities,reused_original_scoped_getters=getters,reused_original_scoped_style11_planes=nameplanes,source_qualified_scoped_name_scope='Approved Hodram andestablished Lil Argot fields/getters/nameplanes reused through exact complete current code/shared/font/actualactors;no new207-name approval orasset.',\n",
        'assert prefix in [2,254]':'assert prefix in [1,2,254]',
        "result['resolved_actor_ID']==(None if is_FE else 2) and result['source_voice_class']==(None if is_FE else 3)":"result['resolved_actor_ID']==(None if is_FE else prefix) and result['source_voice_class']==(None if is_FE else {1:1,2:3}[prefix])",
        'assert len(rows)==6':'assert len(rows)==14','for r in rows)==24':'for r in rows)==56',"if r['source_selector']!=254)==5":"if r['source_selector']!=254)==13",
        '(912,480)':'(912,1120)','six_complete_clean_source_pages.png':'fourteen_clean_source_pages.png','six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json':'source_display.json',
        'source_macro_counts=dict(FI=1,FA=0,FO=0),source_note_count=1':'source_macro_counts=dict(FI=0,FA=0,FO=0),source_note_count=0',
        'Source6:6dispatches/24guarded alignments/5progressivepages/1distinct FEpage/one FI andnote;Lil identity/name/getter reuse bound.':'Source14:14dispatches/56guarded alignments/13progressivepages/1original FEpage/no FI ornote;Hodram andLil scoped identity/getter/nameplane reuse bound.',
    })
    root.mkdir(parents=True);save(root/'source_display_derivation.json',dict(derivation=result,all_native_high_constants_andmultiplicity_preserved=True,original_8300_own_captain1_context_used_until_new_registered_capture_available=True,no_current_B49_English_exposed_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
