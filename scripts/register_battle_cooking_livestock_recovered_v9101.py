"""Resume rejected registration without replacing any partial proof/config."""

from copy import deepcopy
from pathlib import Path
from dk4tool.patch import battle_cooking_livestock_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_cooking_livestock_v910')


def main():
    previous=Path('translations/battle_cooking_livestock_editorial_release_v1.json')
    old=read(previous);config=deepcopy(old)
    assert old['format']=='dk4-battle-repair-medical-editorial-v1'
    assert not Path(owned.CONFIG).exists()
    repair=read(ROOT/'unregistered_config_label_repair_provenance.json')
    module=Path('dk4tool/patch/battle_cooking_livestock_editorial.py')
    assert sha(module.read_bytes())==repair['module_after_sha256']
    assert old['dependencies'][str(module)]==repair['module_before_sha256']
    config['format']='dk4-battle-cooking-livestock-editorial-v1'
    config['dependencies'][str(module)]=sha(module.read_bytes())
    config['dependencies'][str(Path(__file__).absolute().relative_to(Path.cwd()))]=sha(Path(__file__).read_bytes())
    config['dependencies'][str(ROOT/'unregistered_config_label_repair_provenance.json')]=sha((ROOT/'unregistered_config_label_repair_provenance.json').read_bytes())
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    assert old==read(previous)
    save(owned.CONFIG,config)
    rom=NdsImage.open('out/all_routes_combined_v904_candidate.nds')
    c,a,proof=owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)
    assert c==(ROOT/'target_COMMON.bin').read_bytes() and a==(ROOT/'target_ARM9.bin').read_bytes()
    path=Path('translations/release_stack.json');registry=read(path)
    assert registry==read(ROOT/'registry_before.json') and 'all-routes-unified-v910' not in registry['profiles']
    profile=deepcopy(registry['profiles']['all-routes-unified-v904'])
    profile.update(battle_cooking_livestock_editorial=owned.CONFIG,status='experimental',
        description='Complete V904 stack plus25 reviewed battle Galley15/Livestock17 comments1620-1644.',
        note='150 source/control selections including Sera24 override,all25 fonts,7336 full native copies and178 sequences pass. Existing single8KiB cache,216x36 crop and all allocations preserved. Actual scenes/startup/exact patch pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v910']=profile;save(path,registry)
    save(ROOT/'config_label_recovery_complete.json',{'previous_partial_config':str(previous),'previous_partial_config_sha256':sha(previous.read_bytes()),
        'registered_config':owned.CONFIG,'registered_config_sha256':sha(Path(owned.CONFIG).read_bytes()),
        'registry_sha256':sha(path.read_bytes()),'native_outputs_unchanged':True,'strict_apply_replays_exact_target':True,
        'repack_proof':proof,'all150_controls25_fonts7336_copies178_sequences_pass':True,
        'actual_gameplay_and_registered_ROM_build_pending':True,'full_goal_complete':False})
    print('V910 registered with corrected v2 config. Partial v1/proofs retained;full target replay passes.',flush=True)


if __name__=='__main__':main()
