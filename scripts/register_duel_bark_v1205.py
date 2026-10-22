"""Register complete V1189 ancestry plus16 reviewed timed-action reactions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import duel_bark_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_bark_native_plan_v1201 import plan
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_release_v1205')
PROFILE='all-routes-unified-v1206'


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript=Path('translations/duel_bark_editorial_manuscript_v2.json');doc=read(manuscript)
    rom=NdsImage.open('out/all_routes_combined_v1189_candidate.nds')
    c,a,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    registry_path=Path('translations/release_stack.json');registry=read(registry_path);raw=registry_path.read_bytes()
    builder=Path('scripts/build_integrated_release.py');before=builder.read_bytes()
    assert PROFILE not in registry['profiles'] and b"profile_config.get('duel_bark_editorial')" not in before
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    lo=before.index(b"    duel_editorial = profile_config.get('duel_editorial')")
    hi=before.index(b"    escape_direct_formatting = profile_config.get('escape_direct_formatting')")
    block=before[lo:hi].replace(b'duel_editorial',b'duel_bark_editorial').replace(b'DUEL_NATIVE_SELECTION_METADATA',b'DUEL_BARK_NATIVE_SELECTION_METADATA').replace(b'DUEL_OWNED_RENDERER_AND_ESCAPE_SCOPE',b'DUEL_BARK_FIVE_TABLE_FRONT_SAME_OWNED108')
    at=before.index(anchor);after=before[:at]+block+before[at:]
    assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    files=[str(Path(__file__)),str(manuscript),'dk4tool/patch/duel_bark_editorial.py',
        'scripts/duel_bark_native_plan_v1201.py','scripts/duel_bark_front_v1201.py','scripts/duel_bark_layout_v1200.py',
        'scripts/prepare_duel_bark_prose_v1200.py','scripts/research_duel_bark_context_v1199.py',
        'scripts/verify_duel_bark_native_v1202.py','scripts/verify_duel_bark_copies_v1203.py',
        'scripts/verify_duel_bark_escape_regression_v1203.py','scripts/approve_duel_bark_native_v1204.py',
        'translations/escape_direct_formatting_release_v1.json','translations/duel_bark_editorial_manuscript_v1.json',
        'work/analysis/duel_bark_native_v1201/native_payload_plan.json']
    files += [doc[key] for key in ('native_context_proof','native_font_proof','native_copy_proof','escape_regression_proof','visual_review')]
    files.append(read(doc['native_font_proof'])['review_sheet'])
    config={'format':'dk4-duel-bark-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(manuscript),'dependencies':{name:sha(Path(name).read_bytes()) for name in dict.fromkeys(files)}}
    ROOT.mkdir(parents=True);save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a);save(ROOT/'repack_plan.json',proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw);save(ROOT/'registry_before.json',registry)
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    builder.write_bytes(after)
    profile=deepcopy(registry['profiles']['all-routes-unified-v1189'])
    profile.update(duel_bark_editorial=owned.CONFIG,status='experimental',
        description='Full V1189 stack plus16 source-reviewed timed duel-action reactions and exact five-table108-byte front.',
        note='16 new+20 previous native fonts;65615 dispatch;92 complete copies18 cache sequences;13 escape regression pipelines; no allocation growth. Ordinary startup, exact patch and original timed-action gameplay pending. Canonical unchanged.')
    registry['profiles'][PROFILE]=profile;save(registry_path,registry)
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1189',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),'optional_stage_removal_restores_prior_builder_exact':True,
        'registry_before_sha256':sha(raw),'registry_after_sha256':sha(registry_path.read_bytes()),
        'all_prior_profiles_and_accepted_layers_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'build_actual_gameplay_and_completion_pending':True,'full_goal_complete':False})
    print('V1206 complete experimental profile registered;build and original timed-action gameplay pending.',flush=True)


if __name__=='__main__':main()
