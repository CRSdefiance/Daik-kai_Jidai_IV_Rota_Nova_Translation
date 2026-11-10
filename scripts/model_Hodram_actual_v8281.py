"""Native clean-Japanese body models and exact reused revised/name planes for actual scenes."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_actual_models_v8281')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v3.json')
STORED=Path('work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json')
NAMES=Path('work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json')
FIXTURES=Path('work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,stored,names,fixtures=map(read,[DOC,STORED,NAMES,FIXTURES])
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT');digest=sha(arm)
    assert digest==stored['ARM9_sha256']==names['ARM9_sha256']=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
    for fixture in fixtures['fixtures']:
        own=NdsImage.open(fixture['research_ROM']);assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
        assert all(own.read_file(p)==v for p,v in image.iter_components()) and own.read_file('/GRP/KANJI.FNT')==font
    pixels=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':digest},argdefs=original_pixels.__defaults__)
    env={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes}
    adapter=stored['source_owned_target_page_adapter'];exec(compile(adapter,__file__+'::unchanged-exact-target-native-pages','exec'),env)
    ROOT.mkdir(parents=True);models={'clean_Japanese':[],'revised_English':[]}
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);assert raw[0]==row['source_selector'] and not any(v in raw[1:] for v in [b'FI',b'FA',b'FO',b'%'])
        proof=env['pages'](arm,font,raw[1:])
        for page in proof['pages']:
            plane=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/f'{row["id"]}_clean_page{page["page"]}.bin';path.write_bytes(plane)
            page.update(native_plane=str(path),native_plane_sha256=sha(plane))
        models['clean_Japanese'].append(dict(id=row['id'],block=row['block'],source_selector=row['source_selector'],input_hex=raw.hex(),**proof))
        prior=next(r for r in stored['records'] if r['id']==row['id']);reused=deepcopy(prior['complete_native_stored_proof'])
        for page in reused['pages']:
            if 'native_plane' not in page:
                page['native_plane']=page['viewed_native_plane'];page['native_plane_sha256']=page['viewed_native_plane_sha256']
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        models['revised_English'].append(dict(id=row['id'],block=row['block'],source_selector=row['source_selector'],input_hex=prior['stored_hex'],**reused))
    assert all(len(v)==28 for v in models.values())
    for name in names['name_planes']:assert sha(Path(name['native_plane']).read_bytes())==name['native_plane_sha256']
    save(ROOT/'28_clean_native_bodies28_exact_revised_reuses_six_current_headers.json',dict(native_models=models,name_planes=names['name_planes'],
        source_owned_exact_target_page_adapter=adapter,ARM9_sha256=digest,font_sha256=sha(font),
        clean_literal_source_bodies_zero_substitutions_not_relocalized_orreformatted=True,
        fresh_clean_native_paragraphs=28,fresh_clean_native_pages=sum(len(r['pages']) for r in models['clean_Japanese']),
        exact_revised_native_paragraph_reuses=28,exact_current_native_nameplane_reuses=6,
        complete_native_first_internal_final_glyphs_bounds_consumption_checked=True,
        models_only_actual_hold_membership_and4800_geometry_not_yet_measured=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,STORED,NAMES,FIXTURES,Path(__file__)]}))
    print('Actual-scene models:28fresh literal Japanese paragraphs,28exact revised body reuses,six exact current names. Scene observations still pending.')
