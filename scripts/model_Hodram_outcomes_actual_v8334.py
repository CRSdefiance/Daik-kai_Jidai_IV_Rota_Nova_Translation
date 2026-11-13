"""Normalize already checked exact source/stored native planes for actual mixed FE/progressive holds."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_actual_models_v8334')
SOURCE=Path('work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json')
STORED=Path('work/analysis/Hodram_outcome_stored_v8327/six_stored_bodies8_fresh16_reused_alignments_six_exact_native_pages.json')
FIXTURES=Path('work/analysis/Hodram_outcome_fixtures_v8332/four_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json')
if __name__=='__main__':
    assert not ROOT.exists();source,stored,fixtures=map(read,[SOURCE,STORED,FIXTURES]);assert source['ARM9_sha256']==stored['ARM9_sha256'] and source['font_sha256']==stored['font_sha256']
    models={'clean_Japanese':[],'revised_English':[]}
    for r in source['records']:
        body=deepcopy(r['complete_native_source_display']);is_FE=r['source_selector']==254
        if is_FE:
            assert body['pages']==1
            page=dict(page=1,start=0,end=len(bytes.fromhex(r['expanded_source_hex'])),events=body['events'],native_plane=body['native_logical_plane'],native_plane_sha256=body['native_logical_plane_sha256'],physical_plane=body['native_physical_plane'],physical_plane_sha256=body['native_physical_plane_sha256'])
            body['pages']=[page]
        assert len(body['pages'])==1
        for p in body['pages']:
            assert sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256']
            if is_FE:assert sha(Path(p['physical_plane']).read_bytes())==p['physical_plane_sha256'] and len(Path(p['physical_plane']).read_bytes())==228*64
        models['clean_Japanese'].append({**body,'id':r['id'],'block':r['block'],'source_selector':r['source_selector'],'input_hex':r['source_hex'],'expanded_native_hex':r['expanded_source_hex']})
    for r in stored['records']:
        body=deepcopy(r['complete_native_stored_proof']);assert len(body['pages'])==1
        for p in body['pages']:
            assert sha(Path(p['native_plane']).read_bytes())==p['native_plane_sha256']
            if r['source_selector']==254:assert sha(Path(p['physical_plane']).read_bytes())==p['physical_plane_sha256']
        models['revised_English'].append({**body,'id':r['id'],'block':r['block'],'source_selector':r['source_selector'],'input_hex':r['stored_hex'],'expanded_native_hex':r['expanded_stored_hex']})
    for fixture in fixtures['fixtures']:
        rom=NdsImage.open(fixture['research_ROM']);assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
        assert sha(rom.read_file('/__arm9__.bin'))==source['ARM9_sha256'] and sha(rom.read_file('/GRP/KANJI.FNT'))==source['font_sha256']
    assert len(fixtures['fixtures'])==4 and sum(len(f['all_original_exchange_commands']) for f in fixtures['fixtures'])==30
    name=source['reused_original_Lil_style11_plane'];assert sha(Path(name['native_plane']).read_bytes())==name['native_plane_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'six_clean_six_stored_native_bodies_one_Lil_header_distinct_FE.json',dict(native_models=models,name_planes=[name],ARM9_sha256=source['ARM9_sha256'],font_sha256=source['font_sha256'],
        all_existing_native_body_andname_planes_reused_without_reexecution=True,one_source_FI_expands_Hodram_andoriginal_note_remains_inclean_model=True,
        fixture_manifest_actual_counts=4,original_exchange_commands_both_versions=30,original_exchange_speeches_both_versions=12,
        prior_fixture_producer_console_line_six60_28_8_is_stale_only_manifest_andassertions_are_four30_12_zero=True,
        actual_hold_membership_FE_palette_geometry_transition_andreturn_not_yet_measured=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,STORED,FIXTURES,Path(__file__)]}))
    print('Actual models:6clean+6exactstored bodyplanes/oneLil header/distinctFE;no repeatednativeexecution.Fixturemanifest4runs/30originalcommands/12speeches;staleconsoleonly clarified.')
