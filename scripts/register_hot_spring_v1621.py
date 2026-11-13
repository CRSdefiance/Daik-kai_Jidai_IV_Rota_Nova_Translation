"""Register one optional hot-spring stage after the latest centered screenshot stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hot_spring_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_release_v1621')
PROFILE='all-routes-unified-v1622'
PARENT='screenshot-text-repairs-centered-20261022'
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript=Path('translations/hot_spring_editorial_manuscript_v2.json');doc=read(manuscript)
    source=Path(doc['current_ROM']);assert sha(source.read_bytes())==doc['current_ROM_sha256']
    rom=NdsImage.open(source);c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles'] and PARENT in registry['profiles']
    assert registry['profiles'][PARENT]['ship_advice_choice_centering']=='translations/ship_advice_choice_centering_20261022_release_v1.json'
    assert registry['latest_promoted_build']['rom_sha256']=='96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd'
    assert b"profile_config.get('hot_spring_editorial')" not in before
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1;hi=before.index(anchor)
    lo=before.index(b"    fatigue_status_editorial = profile_config.get('fatigue_status_editorial')")
    end=before.index(b"    screenshot_repairs = profile_config.get('screenshot_text_repairs')")
    block=before[lo:end].replace(b'fatigue_status_editorial',b'hot_spring_editorial').replace(b'FATIGUE_STATUS_NATIVE_METADATA',b'HOT_SPRING_NATIVE_METADATA_AND_SELECTOR_KEYS').replace(b'FATIGUE_STATUS_SOURCE_NUMERIC_SYSTEM_MODAL_TEXT',b'HOT_SPRING_ROLE1_SOURCE_DIALOGUE')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    files=set(read('translations/fatigue_status_editorial_release_v1.json')['dependencies'])
    for config in ['translations/fatigue_status_editorial_release_v1.json','translations/screenshot_text_repairs_20261022_release_v1.json','translations/ship_advice_choice_centering_20261022_release_v1.json']:
        files.add(config);files.update(read(config).get('dependencies',{}))
    files.update([str(manuscript),__file__,'dk4tool/patch/hot_spring_editorial.py','translations/hot_spring_editorial_manuscript_v1.json',
        'scripts/inventory_hot_spring_dialogue_v1610.py','scripts/author_hot_spring_dialogue_v1611.py','scripts/author_hot_spring_dialogue_v1611b.py',
        'scripts/hot_spring_runtime_v1614.py','scripts/hot_spring_native_plan_v1615.py','scripts/verify_hot_spring_runtime_v1616.py',
        'scripts/probe_hot_spring_fonts_v1617.py','scripts/verify_hot_spring_copies_v1618.py','scripts/verify_hot_spring_escape_v1619.py','scripts/approve_hot_spring_v1620.py',
        'work/analysis/hot_spring_payload_v1615/native_payload_plan.json','work/analysis/hot_spring_native_review_v1620/native_approval_receipt.json',doc['source_context']])
    for key in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']:files.add(doc[key])
    fonts=read(doc['native_font_proof']);files.update(c['preview'] for c in fonts['cases']);files.update(s['path'] for s in fonts['sheets_for_visual_review'])
    config={'format':'dk4-hot-spring-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
        'dependencies':{p:sha(Path(p).read_bytes()) for p in sorted(files)}}
    ROOT.mkdir(parents=True);save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a);save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    profile=deepcopy(registry['profiles'][PARENT]);profile.update(hot_spring_editorial=owned.CONFIG,status='experimental',
        description='Complete centered screenshot repair stack plus source/native-approved hot-spring13.',
        note='12 revisions1 retention;COMMON24/native metadata and two exact source role1 selector memberships only.188/172/123040 sizes fixed.529481 native dispatch cases,7336 copies180 cache,13 escapes,16 viewed native panels pass. Exact patch/startup/original hot-spring event pending;V1492 promoted.')
    registry['profiles'][PROFILE]=profile;builder.write_bytes(after);save(rp,registry)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':PARENT,'source_text_payload_reference':str(source),
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),'optional_stage_removal_restores_prior_builder_exact':True,
        'registry_before_sha256':sha(raw),'registry_after_sha256':sha(rp.read_bytes()),'all_prior_profiles_accepted_layers_batches_centering_and_promotion_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_patch_startup_original_event_and_completion_pending':True,'full_goal_complete':False})
    print('Experimental V1622 registered after full centered screenshot profile;all prior profiles and V1492 promotion preserved. Build/patch/startup/actual event pending.')
