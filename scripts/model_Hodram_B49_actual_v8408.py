"""Reuse the completed source/stored native planes for actual B49 frame comparison."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_models_v8408')
SOURCE=Path('work/analysis/Hodram_B49_source_display_v8386b/source_display.json')
STORED=Path('work/analysis/Hodram_B49_stored_v8399/stored_bodies.json')
FIXTURES=Path('work/analysis/Hodram_B49_fixtures_v8406/two_whole_scripts.json')

if __name__=='__main__':
    assert not ROOT.exists();source,stored,fixtures=map(read,[SOURCE,STORED,FIXTURES])
    models={'clean_Japanese':[],'revised_English':[]}
    for row in source['records']:
        body=deepcopy(row['complete_native_source_display']);FE=row['source_selector']==254
        if FE:
            assert body['pages']==1
            body['pages']=[dict(page=1,start=0,end=len(bytes.fromhex(row['expanded_source_hex'])),events=body['events'],native_plane=body['native_logical_plane'],native_plane_sha256=body['native_logical_plane_sha256'],physical_plane=body['native_physical_plane'],physical_plane_sha256=body['native_physical_plane_sha256'])]
        assert len(body['pages'])==1
        models['clean_Japanese'].append({**body,'id':row['id'],'block':49,'source_selector':row['source_selector'],'input_hex':row['source_hex'],'expanded_native_hex':row['expanded_source_hex']})
    viewed=read('work/analysis/Hodram_B49_pages_v8395/compiled_native_pages.json')
    for row in stored['records']:
        body=deepcopy(row['complete_native_stored_proof']);FE=row['source_selector']==254
        if 'pages' not in body:
            assert FE and 'full_logical_andphysical_planes_exact_to_viewed' in body
            body['pages']=[deepcopy(body['full_logical_andphysical_planes_exact_to_viewed'])]
        for p in body['pages']:
            if 'native_plane' not in p:p.update(native_plane=p['viewed_native_plane'],native_plane_sha256=p['viewed_native_plane_sha256'])
        assert len(body['pages'])==1
        models['revised_English'].append({**body,'id':row['id'],'block':49,'source_selector':row['source_selector'],'input_hex':row['stored_hex'],'expanded_native_hex':row['expanded_stored_hex']})
    assert all(len(v)==14 for v in models.values())
    for rows in models.values():
        for row in rows:
            for p in row['pages']:
                assert sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256']
                if row['source_selector']==254:assert sha(Path(p['physical_plane']).read_bytes())==p['physical_plane_sha256']
    names=deepcopy(source['reused_original_scoped_style11_planes'])
    assert {r['actor_ID'] for r in names}=={1,2}
    for n in names:assert sha(Path(n['native_plane']).read_bytes())==n['native_plane_sha256']
    for fixture in fixtures['fixtures']:
        image=NdsImage.open(fixture['research_ROM']);assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
        assert sha(image.read_file('/__arm9__.bin'))==source['ARM9_sha256']==viewed['ARM9_sha256']
        assert sha(image.read_file('/GRP/KANJI.FNT'))==source['font_sha256']==viewed['font_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'native_models.json',dict(native_models=models,name_planes=names,ARM9_sha256=source['ARM9_sha256'],font_sha256=source['font_sha256'],source_original14_andreviewed_stored14_planes_reused_by_exact_hash=True,two_current_nameplanes_reused_by_exact_code_font_actor_binding=True,no_native_reexecution=True,actual_selected_path_hold_membership_not_all14_conditional_speeches_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,STORED,FIXTURES,Path(__file__)]}))
    print('B49 actual models:14clean+14stored complete native body planes/two currentnameplanes reused exactly;no native reexecution orcredit.')
