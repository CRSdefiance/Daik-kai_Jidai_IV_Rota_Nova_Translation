"""Register one notice-only stage after the complete V1622 combined stack."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hot_spring_notice_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_notice_release_v1636')
PROFILE='all-routes-unified-v1637'
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript=Path('translations/hot_spring_notice_editorial_manuscript_v2.json');doc=read(manuscript);parent=Path('out/all_routes_combined_v1622_candidate.nds')
    assert sha(parent.read_bytes())=='cb049635c45b6bc75add4ada18db69ae2ece4aa05b9270a3553ed9ed74a228e4'
    rom=NdsImage.open(parent);c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and b"profile_config.get('hot_spring_notice_editorial')" not in before
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1;hi=before.index(anchor)
    lo=before.index(b"    hot_spring_editorial = profile_config.get('hot_spring_editorial')")
    block=before[lo:hi].replace(b'hot_spring_editorial',b'hot_spring_notice_editorial').replace(b'HOT_SPRING_NATIVE_METADATA_AND_SELECTOR_KEYS',b'HOT_SPRING_NOTICE_NATIVE_METADATA').replace(b'HOT_SPRING_ROLE1_SOURCE_DIALOGUE',b'HOT_SPRING_OPTIONAL_EXPERIENCE_MODAL_TEXT')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    files=set(read('translations/hot_spring_editorial_release_v1.json')['dependencies'])
    files.update([str(manuscript),__file__,'translations/hot_spring_editorial_release_v1.json','translations/hot_spring_notice_editorial_manuscript_v1.json',
        'dk4tool/patch/hot_spring_notice_editorial.py','scripts/author_hot_spring_notice_v1631.py','scripts/hot_spring_notice_plan_v1632.py',
        'scripts/probe_hot_spring_notice_fonts_v1633.py','scripts/verify_hot_spring_notice_copies_v1634.py','scripts/approve_hot_spring_notice_v1635.py',
        'work/analysis/hot_spring_notice_payload_v1632/native_payload_plan.json','work/analysis/hot_spring_notice_native_review_v1635/native_approval_receipt.json',doc['source_context']])
    for k in ['native_font_proof','native_copy_proof','visual_review']:files.add(doc[k])
    fonts=read(doc['native_font_proof']);files.add(fonts['review_sheet']);files.update(c['preview'] for c in fonts['cases'])
    config={'format':'dk4-hot-spring-notice-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],'manuscript':str(manuscript),
        'dependencies':{p:sha(Path(p).read_bytes()) for p in sorted(files)}}
    ROOT.mkdir(parents=True);save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a);save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    profile=deepcopy(registry['profiles']['all-routes-unified-v1622']);profile.update(hot_spring_notice_editorial=owned.CONFIG,status='experimental',
        description='Complete V1622 stack plus source/native-approved optional Experience notice310.',
        note='One natural no-argument status replaces legacy indent/LF;COMMON4 and original metadata only.3667 other text/copy spans,40 blocks,all native code/188 selector/172 gate/123040 staged bytes preserved. Full native font and7336 copies180 cache pass;patch/startup/optional relaxation-notice gameplay pending. V1492 remains promoted.')
    registry['profiles'][PROFILE]=profile;builder.write_bytes(after);save(rp,registry)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1622','builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),'registry_after_sha256':sha(rp.read_bytes()),
        'all_prior_profiles_accepted_layers_batches_centering_hot_spring13_and_promotion_preserved':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Experimental V1637 registered after all V1622 changes;patch/startup/optional relaxation and notice gameplay remain pending.')
