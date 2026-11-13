"""Register the reviewed11-report stage after every complete V1637 layer."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import search_reports_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/search_reports_release_v1675')
PROFILE='all-routes-unified-v1676'
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript=Path('translations/search_reports_editorial_manuscript_v4.json');doc=read(manuscript)
    parent=Path('out/all_routes_combined_v1637_candidate.nds')
    assert sha(parent.read_bytes())=='0d81ee2668d2ff535432e2a50a5df44b9c1a4b0f683fca407f5753348038e7b2'
    rom=NdsImage.open(parent);c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert b"profile_config.get('search_reports_editorial')" not in before
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1;hi=before.index(anchor)
    lo=before.index(b"    hot_spring_notice_editorial = profile_config.get('hot_spring_notice_editorial')")
    block=before[lo:hi].replace(b'hot_spring_notice_editorial',b'search_reports_editorial').replace(b'HOT_SPRING_NOTICE_NATIVE_METADATA',b'SEARCH_REPORTS_NATIVE_METADATA_AND_EXACT_TABLE_KEYS').replace(b'HOT_SPRING_OPTIONAL_EXPERIENCE_MODAL_TEXT',b'SEARCH_ROLE1_ROLE7_AND_LOSS_MODAL_SOURCE_TEXT')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    files=set(read('translations/hot_spring_notice_editorial_release_v1.json')['dependencies'])
    files.update([__file__,'translations/hot_spring_notice_editorial_release_v1.json','dk4tool/patch/search_reports_editorial.py',
                  'scripts/revise_search_loss_grammar_v1670.py',doc['source_context'],doc['source_quantity_bounds']])
    files.update(str(p) for p in Path('scripts').glob('*search_reports*.py'))
    files.update(str(p) for p in Path('translations').glob('search_reports_editorial_manuscript_v*.json'))
    for folder in ['search_reports_source_v1653','search_reports_revision_v1665','search_reports_payload_v1670','search_reports_runtime_v1660','search_reports_native_review_v1674']:
        files.update(str(p) for p in (Path('work/analysis')/folder).glob('*.json'))
    for key in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']:files.add(doc[key])
    fonts=read(doc['native_font_proof']);files.update(c['preview'] for c in fonts['cases']);files.update(s['path'] for s in fonts['sheets_for_visual_review'])
    config={'format':'dk4-search-reports-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
            'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
            'manuscript':str(manuscript),'dependencies':{p:sha(Path(p).read_bytes()) for p in sorted(files)}}
    ROOT.mkdir(parents=True);save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a);save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    profile=deepcopy(registry['profiles']['all-routes-unified-v1637'])
    profile.update(search_reports_editorial=owned.CONFIG,status='experimental',
        description='Complete V1637 stack plus eleven source/native-reviewed Search reports.',
        note='COMMON4/23 and exact original metadata;186/188-byte selector with191 delta/run64 encoding and168/172 gate. Every prior membership preserved.3657 unselected copies,39 blocks,123040 staged bytes and all prior route/UI/graphics/centering layers exact.294 full-font cases,414 actor choices,17 compiler negatives,7336 copies180 cache,13 prior pipelines and529507 native dispatch/ABI tests pass. Registered patch/startup/revised original gameplay pending;V1492 remains promoted.')
    registry['profiles'][PROFILE]=profile;builder.write_bytes(after);save(rp,registry)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1637',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),'optional_stage_removal_restores_prior_builder_exact':True,
        'registry_before_sha256':sha(raw),'registry_after_sha256':sha(rp.read_bytes()),
        'all_prior_profiles_accepted_layers_batches_centering_hot_spring14_and_promotion_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Experimental V1676 profile registered after the full V1637 stack;patch,startup and actual revised Search scenes pending.')
