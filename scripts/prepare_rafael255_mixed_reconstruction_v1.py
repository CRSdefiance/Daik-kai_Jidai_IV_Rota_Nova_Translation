"""Join229 exact approved body checks with14 fresh style checks andfull text-object census."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v5.json')
PLAN=Path('work/analysis/Rafael255_layout_v1_20261105/automatic_plans.json')
BASE=Path('work/analysis/Rafael241_native_final_v6_20261105/compiled_native_pages.json')
FRESH=Path('work/analysis/Rafael14_native_v1_20261105/compiled_native_pages.json')
STYLE=Path('work/analysis/Rafael14_compiled_style_objects_v1_20261105/compiled_style_objects.json')
MENU=BASE.with_name('qualified_menu.json')
PACKET=Path('work/analysis/Rafael_B101_B120_current678_20261105/current_effective.json')
ROOT=Path('work/analysis/Rafael255_reconstruction_inputs_v1_20261105')

if __name__=='__main__':
    assert not ROOT.exists();doc,plan,base,fresh,style,menu,packet=map(load,[DOC,PLAN,BASE,FRESH,STYLE,MENU,PACKET])
    assert len(doc['records'])==255 and (doc['proposed_revisions'],doc['justified_retentions'])==(135,120)
    assert base['runtime']==fresh['runtime']==style['runtime']==menu['runtime']==packet['runtime']
    assert base['font_sha256']==fresh['font_sha256'] and len(base['records'])==229 and len(fresh['records'])==14
    assert plan['manuscript_sha256']==sha(DOC.read_bytes()) and not plan['failures']
    assert all(i['severity'] not in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    oldplan=load(base['plan']);old_by={r['id']:r for r in oldplan['records']}
    records={r['id']:deepcopy(r) for r in base['records']};records.update({r['id']:deepcopy(r) for r in fresh['records']})
    assert len(records)==243
    origins=deepcopy(base['origins'])
    for r in plan['records']:
        row=records[r['id']];assert row['compiled_hex']==r['encoded_hex'] and row['logical_English']==r['logical_English']
        if r['id'] in old_by:assert r['encoded_hex']==old_by[r['id']]['encoded_hex'] and r['lines']==old_by[r['id']]['lines']
        else:origins[r['id']]=dict(native_proof=str(FRESH),native_proof_sha256=sha(FRESH.read_bytes()),freshly_rendered_anddirectly_viewed=True)
        assert len(row['native_alignment']['cases'])==4 and all(c['output_hex']==row['expanded_native_hex'] for c in row['native_alignment']['cases'])
        rendered=row['complete_native_English_display'];pages=[rendered] if row['kind']=='system-FE' else rendered['pages']
        assert len(pages)==r['expected_native_pages']
        for page in pages:
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'] and sha(Path(page['preview']).read_bytes())==page['preview_sha256']
    assert len(fresh['review_sheets'])==2 and fresh['pages']==14
    for sheet in fresh['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    olddoc=load(base['manuscript']);assert doc['records'][:241]==olddoc['records']
    oldcaptions={r['id']:r for r in olddoc['records'] if r['kind']=='typed-choice-label'}
    assert all(r==oldcaptions[r['id']] for r in doc['records'] if r['kind']=='typed-choice-label')
    source_counts=Counter(c['word'] for g in packet['groups'] for c in g['all_source_commands'])
    current_counts=Counter(c['word'] for g in packet['groups'] for c in g['all_current_commands'])
    assert source_counts==current_counts and (source_counts[0x4000],source_counts[0x2100],source_counts[0x2200],source_counts[0x4100])==(229,0,4,2)
    assert style['manuscript_sha256']==sha(DOC.read_bytes()) and style['plan_sha256']==sha(PLAN.read_bytes())
    assert (len(style['objects']),style['physical_alternatives'],style['native_target_slot_cases'])==(2,14,16)
    assert sum(len(x['rejected']) for x in style['compiler_negatives'])==18
    ROOT.mkdir();approval=ROOT/'visual_andinventory_approval.json'
    save(approval,dict(base_visual=str(BASE.with_name('direct_visual_approval.json')),base_visual_sha256=sha(BASE.with_name('direct_visual_approval.json').read_bytes()),
        fresh_style_native=str(FRESH),fresh_style_native_sha256=sha(FRESH.read_bytes()),fresh_style_sheets=fresh['review_sheets'],
        all14_fresh_style_pages_directly_viewed=True,all_previous234_body_pages_andall12_captions_exact_review_reused=True,
        full_body_pages=248,source_speeches=229,style_physical_alternatives=14,style_alias_slots=16,choice_labels=12,
        command_kind_counts={f'{k:04x}':v for k,v in sorted(source_counts.items())},
        source_text_object_census_complete_for4000_2100_2200_4100=True,
        failed_plain_zero_style_preflight_preserved=True,no_fifth_gate_gameplay_orcompletion_credit=True,new_credit=0))
    native=deepcopy(base)
    native.update(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=[records[r['id']] for r in plan['records']],origins=origins,pages=248,fresh_compiled_alignments=972,
        alignment_count_is_composite_not_one_run=True,review_sheets=base['review_sheets']+fresh['review_sheets'],
        dynamic_role_bindings=fresh['dynamic_role_bindings'],all243_body_layouts_approved=True,all248_complete_pages_directly_viewed=True,
        full255_object_batch_offline_display_complete=True,source_owned_progressive_macro_adapter=fresh['source_owned_progressive_macro_adapter'],
        direct_visual_review_pending=False,formatting_gates_still_false=True,actual_gameplay=False,new_credit=0,
        previous229_exact_prose_andcompiled_byte_reuses=True,new_style_native=str(FRESH),new_style_native_sha256=sha(FRESH.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,BASE,FRESH,STYLE,MENU,PACKET,approval,Path(__file__)]})
    save(ROOT/'native.json',native)
    projected=deepcopy(menu);projected.update(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        offline_visual_approved=True,source_visual_approval=str(approval),source_visual_approval_sha256=sha(approval.read_bytes()),
        all12_complete_source_current_caption_objects_gates_andnative_dependencies_unchanged=True,no_new_menu_execution_claim=True)
    save(ROOT/'menu.json',projected)
    save(ROOT/'styles.json',style)
    print('Full source census:229 ordinary+14 style speeches+12 captions.248 native/viewed pages;16 style target slots/18 negatives;229 bodies/12 captions reused exactly.')
