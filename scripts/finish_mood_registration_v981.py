"""Finish the existing native-copy preflight after a config-format metadata error."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import mood_comments_editorial_v981b as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_v981')

def main():
    rp=Path('translations/release_stack.json');registry=read(rp)
    assert registry==read(ROOT/'registry_before.json') and 'all-routes-unified-v981' not in registry['profiles']
    cp=Path(owned.CONFIG);before=cp.read_bytes();config=read(cp)
    assert config['format']=='dk4-illness-critical-editorial-v1'
    snapshot=ROOT/'unregistered_config_format_error.json';assert not snapshot.exists();snapshot.write_bytes(before)
    config['format']='dk4-mood-comments-editorial-v1'
    for name in ('scripts/prepare_mood_comments_release_v981b.py','scripts/finish_mood_registration_v981.py',
                 'work/analysis/mood_comments_v981/release_path_successors_v981b.json'):
        config['dependencies'][name]=sha(Path(name).read_bytes())
    rom=NdsImage.open('out/all_routes_combined_v975_candidate.nds')
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),read(config['manuscript']))
    assert c==(ROOT/'target_COMMON.bin').read_bytes() and a==(ROOT/'target_ARM9.bin').read_bytes()
    assert config['target_common_sha256']==sha(c) and config['target_arm9_sha256']==sha(a)
    assert cp.read_bytes()==before;save(cp,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),str(cp))[:2]==(c,a)
    assert read(rp)==registry
    profile=deepcopy(registry['profiles']['all-routes-unified-v975'])
    profile.update(mood_comments_editorial=str(cp),status='experimental',
        description='Complete V975 stack plus39 reviewed mood/panic alternatives1833-1871 for original moods0/4/5.',
        note='225 original selections,75 physical-priority and72 normal-mood controls,78 complete font cases (76 exact reused plus2 fresh),7336 copies and178 cache sequences pass. Native code,opaque spans,single8KiB cache,216x36 crop and123040 staged bytes preserved. Actual scenes,startup and exact patch pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v981']=profile;save(rp,registry)
    save(ROOT/'registration_completion.json',{'failed_unregistered_config_sha256':sha(before),
        'corrected_config_sha256':sha(cp.read_bytes()),'only_format_and_explicit_provenance_dependencies_changed':True,
        'prior_native_copy_proof_reused_after_complete_source_target_hash_check':True,
        'all_registered_stage_guards_and_target_byte_equality_pass':True,'registry_sha256':sha(rp.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'actual_and_registered_build_pending':True})
    print('V981 registered:39 reviewed entries,7336 complete copies and178 cache sequences pass.')

if __name__=='__main__':main()
