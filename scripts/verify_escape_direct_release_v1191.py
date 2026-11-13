"""Exact combined ancestry, unchanged COMMON and clean-input reconstructable patch."""
from pathlib import Path
from dk4tool.patch import escape_direct_formatting as owned
from dk4tool.patch import duel_editorial as previous
from dk4tool.patch.escape_direct_entries import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_direct_release_v1188')
ROM=Path('out/all_routes_combined_v1189_candidate.nds')
OLD=Path('out/all_routes_combined_v1166_candidate.nds')


def main():
    proof=ROOT/'registered_release_verification.json';assert not proof.exists()
    manifest,prior=map(lambda p:read(p.with_suffix('.manifest.json')),(ROM,OLD))
    assert manifest['profile']=='all-routes-unified-v1189'
    assert manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    registry=read('translations/release_stack.json')
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored={**registry,'profiles':{k:v for k,v in registry['profiles'].items() if k!='all-routes-unified-v1189'}}
    assert restored==read(ROOT/'registry_before.json')
    assert manifest['batches']==prior['batches'] and len(manifest['batches'])==471
    assert len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    old,new=map(NdsImage.open,(OLD,ROM))
    assert all(new.read_file(path)==raw for _,path,raw in old.iter_files())
    assert dict(old.iter_components()).keys()==dict(new.iter_components()).keys()
    for path,raw in old.iter_components():
        if path!='/__arm9__.bin':assert new.read_file(path)==raw,path
    before,after=old.read_file('/__arm9__.bin'),new.read_file('/__arm9__.bin')
    assert owned.apply_release(before,owned.CONFIG)[0]==after==(ROOT/'target_ARM9.bin').read_bytes()
    common=new.read_file('/COMMON/MESFILE.DK4')
    a,b=previous.current_entries(common,before),current_entries(common,after)
    assert len(a)==len(b)==3668 and a==b
    assert after[:0x800]==before[:0x800]
    builder=Path('scripts/build_integrated_release.py').read_bytes();block=(ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.replace(block,b'',1)==(ROOT/'builder_before.py').read_bytes()
    patch,rebuild,clean=ROM.with_suffix('.xdelta'),ROOT/'patch_reconstruction_RESEARCH_ONLY.nds',Path('work/clean.nds')
    assert not patch.exists() and not rebuild.exists()
    clean_sha=sha(clean.read_bytes());assert clean_sha=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,rebuild)
    assert rebuild.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    save(proof,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'profile':manifest['profile'],
        'canonical_base':manifest['base_rom'],'canonical_sha256':manifest['base_sha256'],
        'manifest_sha256':sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'COMMON_sha256':sha(common),'ARM9_sha256':sha(after),'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),
        'clean_input_sha256':clean_sha,'reconstruction':str(rebuild),'complete_reconstruction_byte_exact':True,
        'all471_batches114_accepted_layers_and_prior_profiles_exact':True,
        'all3668_COMMON_entries_routes_graphics_fonts_other_files_and_components_exact':True,
        'only_source_locked_existing_ARM9_gate_bank_status_load_and_literal_changed':True,
        'section_BSS_cache_arena_ITCM_and_staged123040_unchanged':True,
        'prior_builder_restores_by_removing_exact_optional_stage':True,
        'actual_gameplay_startup_and_new_completion_credit_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1189 combined ROM and clean-input patch reconstruct exactly.',flush=True)
    print('ROM SHA256',sha(ROM.read_bytes()));print('Patch SHA256',sha(patch.read_bytes()))


if __name__=='__main__':main()
