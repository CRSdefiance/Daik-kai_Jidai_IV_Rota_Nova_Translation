"""Reuse exact already-viewed body/name planes for actual capture auditing."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_models_v8741')
SOURCE=Path('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json')
STORED=Path('work/analysis/Hodram_B31_B53_stored_v8729/stored_pages_controls_andreferences.json')
VIEWED=Path('work/analysis/Hodram_B31_B53_pages_v8726/compiled_native_pages.json')
FIXTURES=Path('work/analysis/Hodram_B31_B53_fixtures_v8739/four_whole_scripts.json')
NAMES=Path('work/analysis/Hodram_B31_actor34_names_v8719/source_names_native_getters_andplanes.json')
if __name__=='__main__':
    assert not ROOT.exists();source,stored,viewed,fixtures,bindings=map(read,[SOURCE,STORED,VIEWED,FIXTURES,NAMES])
    assert source['source_macro_counts']==dict(FI=0,FA=0,FO=0) and source['source_FE_count']==0
    models={'clean_Japanese':[],'revised_English':[]}
    for row in source['records']:
        body=deepcopy(row['complete_native_source_display']);raw=bytes.fromhex(row['source_hex'])
        assert len(body['pages'])==1 and body['complete_consumed_bytes']==len(raw)-1
        models['clean_Japanese'].append({**body,'id':row['id'],'block':row['block'],'source_selector':row['source_selector'],'input_hex':raw.hex(),'expanded_native_hex':raw[1:].hex()})
    for row in stored['records']:
        body=deepcopy(row['complete_native_page']);raw=bytes.fromhex(row['stored_hex'])
        for page in body['pages']:
            if 'native_plane' not in page:page.update(native_plane=page['viewed_native_plane'],native_plane_sha256=page['viewed_native_plane_sha256'])
        assert len(body['pages'])==1 and body['complete_consumed_bytes']==len(raw)-1
        models['revised_English'].append({**body,'id':row['id'],'block':row['block'],'source_selector':row['source_selector'],'input_hex':raw.hex(),'expanded_native_hex':raw[1:].hex()})
    assert all(len(rows)==3 for rows in models.values())
    for rows in models.values():
        for row in rows:
            assert row['source_selector'] in [34,113]
            for page in row['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
    actor34=deepcopy(next(p for p in bindings['fresh_actor34_name_planes'] if p['text']=='Barbarossa Hayreddin'))
    actor34['original_pair_flush_width']=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in actor34['native_glyph_events'])
    names=[actor34,deepcopy(bindings['scoped_reused_actor113']['plane'])]
    assert {r['actor_ID'] for r in names}=={34,113}
    for row in names:assert sha(Path(row['native_plane']).read_bytes())==row['native_plane_sha256']
    for fixture in fixtures['fixtures']:
        image=NdsImage.open(fixture['research_ROM']);assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
        assert sha(image.read_file('/__arm9__.bin'))==source['ARM9_sha256']==viewed['ARM9_sha256']
        assert sha(image.read_file('/GRP/KANJI.FNT'))==source['font_sha256']==viewed['font_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'native_models.json',dict(native_models=models,name_planes=names,ARM9_sha256=source['ARM9_sha256'],font_sha256=source['font_sha256'],
        source_original3_andreviewed_stored3_planes_reused_by_exact_hash=True,two_current_progressive_nameplanes_reused_by_exact_inputs=True,
        no_native_reexecution=True,unvisited_conditional_rows_are_models_not_actual_coverage=True,
        actual_selected_body_header_path_transition_andnormal_return_binding_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,STORED,VIEWED,FIXTURES,NAMES,Path(__file__)]}))
    print('Exact3Japanese/3stored body models and2current progressive nameplanes bound foractual audit;no native replay oractual coverage credited.',flush=True)
