"""Reuse every completed source/stored body and scoped progressive-name plane."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_models_v8817')
SOURCE=Path('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json')
STORED=Path('work/analysis/Hodram_B54_B60_stored_v8811/stored_pages_controls_andreferences.json')
VIEWED=Path('work/analysis/Hodram_B54_B60_pages_v8804/compiled_native_pages.json')
FIXTURES=Path('work/analysis/Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json')
NAMES=Path('work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json')

def normalize(body,expanded,FE):
    body=deepcopy(body)
    if FE:
        assert body['pages']==1
        body['pages']=[dict(page=1,start=0,end=len(bytes.fromhex(expanded)),events=body['events'],native_plane=body['native_logical_plane'],native_plane_sha256=body['native_logical_plane_sha256'],physical_plane=body['native_physical_plane'],physical_plane_sha256=body['native_physical_plane_sha256'])]
        body['complete_consumed_bytes']=len(bytes.fromhex(expanded))
    for p in body['pages']:
        if 'native_plane' not in p:p.update(native_plane=p['viewed_native_plane'],native_plane_sha256=p['viewed_native_plane_sha256'])
        assert sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256']
        if FE:assert sha(Path(p['physical_plane']).read_bytes())==p['physical_plane_sha256']
    assert body['complete_consumed_bytes']==len(bytes.fromhex(expanded))
    return body

if __name__=='__main__':
    assert not ROOT.exists();source,stored,viewed,fixtures,bindings=map(read,[SOURCE,STORED,VIEWED,FIXTURES,NAMES]);models={'clean_Japanese':[],'revised_English':[]}
    for row in source['records']:
        body=normalize(row['complete_native_source_display'],row['expanded_source_hex'],row['source_selector']==254)
        models['clean_Japanese'].append({**body,'id':row['id'],'block':row['block'],'source_selector':row['source_selector'],'input_hex':row['source_hex'],'expanded_native_hex':row['expanded_source_hex']})
    for row in stored['records']:
        proof=row['complete_native_stored_proof']
        if 'exact_reused_compiled_native_record' in proof:body=proof['exact_reused_compiled_native_record']['complete_native_English_display']
        else:
            assert row['source_selector']!=254;body=proof
        body=normalize(body,row['expanded_stored_hex'],row['source_selector']==254)
        models['revised_English'].append({**body,'id':row['id'],'block':row['block'],'source_selector':row['source_selector'],'input_hex':row['stored_hex'],'expanded_native_hex':row['expanded_stored_hex']})
    assert all(len(v)==82 for v in models.values());names=[]
    for binding in bindings['fresh_twenty_progressive_andfull_current_getters']['rows']:
        if binding['consumer']!='progressive-nameplate':continue
        plane=deepcopy(next(p for p in bindings['native_name_planes'] if p['text']==binding['text']))
        plane.update(actor_ID=binding['actor_ID'],original_pair_flush_width=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in plane['native_glyph_events']))
        assert sha(Path(plane['native_plane']).read_bytes())==plane['native_plane_sha256'];names.append(plane)
    assert len(names)==10 and {r['actor_ID'] for r in names}=={1,20,23,24,36,84,113,114,119,141}
    for fixture in fixtures['fixtures']:
        image=NdsImage.open(fixture['research_ROM']);assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
        assert sha(image.read_file('/__arm9__.bin'))==source['ARM9_sha256']==viewed['ARM9_sha256']
        assert sha(image.read_file('/GRP/KANJI.FNT'))==source['font_sha256']==viewed['font_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'native_models.json',dict(native_models=models,name_planes=names,ARM9_sha256=source['ARM9_sha256'],font_sha256=source['font_sha256'],
        source82_andstored82_complete_planes_reused_by_exact_hash=True,ten_current_progressive_nameplanes_reused_by_exact_inputs=True,
        includes_distinct_FE_null_actor_andthree_English_two_page_records=True,no_native_reexecution=True,
        unvisited_conditional_rows_are_models_not_actual_coverage=True,actual_selected_body_header_path_FE_transition_andnormal_return_binding_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,STORED,VIEWED,FIXTURES,NAMES,Path(__file__)]}))
    print('82clean/82stored complete body models and10progressive nameplanes bound,includingFE/multipage;no rerender oractual credit.',flush=True)
