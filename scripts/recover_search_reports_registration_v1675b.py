"""Finish the verified1675 registration after Windows rejected opening the registry."""
from copy import deepcopy
from pathlib import Path
import json
import os
from dk4tool.patch import search_reports_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/search_reports_release_v1675')
PROFILE='all-routes-unified-v1676'
if __name__=='__main__':
    receipt=ROOT/'registration_provenance.json';assert not receipt.exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw=(ROOT/'registry_before_raw.json').read_bytes();before=(ROOT/'builder_before.py').read_bytes();block=(ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert rp.read_bytes()==raw and builder.read_bytes().replace(block,b'',1)==before
    registry=read(rp);assert PROFILE not in registry['profiles']
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    config=read(owned.CONFIG)
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    profile=deepcopy(registry['profiles']['all-routes-unified-v1637'])
    profile.update(search_reports_editorial=owned.CONFIG,status='experimental',
        description='Complete V1637 stack plus eleven source/native-reviewed Search reports.',
        note='COMMON4/23 and exact original metadata;186/188-byte selector with191 delta/run64 encoding and168/172 gate. Every prior membership preserved.3657 unselected copies,39 blocks,123040 staged bytes and all prior route/UI/graphics/centering layers exact.294 full-font cases,414 actor choices,17 compiler negatives,7336 copies180 cache,13 prior pipelines and529507 native dispatch/ABI tests pass. Registered patch/startup/revised original gameplay pending;V1492 remains promoted.')
    registry['profiles'][PROFILE]=profile
    root=Path.cwd().absolute();target=rp.absolute();temporary=(rp.parent/'release_stack_v1675b_pending.json').absolute()
    target.relative_to(root);temporary.relative_to(root)
    assert target.parent==temporary.parent and not temporary.exists()
    temporary.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert read(temporary)==registry and rp.read_bytes()==raw
    os.replace(temporary,target)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')
    save(receipt,{'profile':PROFILE,'source_profile':'all-routes-unified-v1637','builder_before_sha256':sha(before),'builder_after_sha256':sha(builder.read_bytes()),
        'optional_stage_removal_restores_prior_builder_exact':True,'registry_before_sha256':sha(raw),'registry_after_sha256':sha(rp.read_bytes()),
        'all_prior_profiles_accepted_layers_batches_centering_hot_spring14_and_promotion_preserved':True,
        'original_write_error':'OSError22 opening existing registry;original registry remained byte-exact;builder optional stage was already written',
        'recovery_validated_original_registry_and_complete_optional_builder_block_before_atomic_replacement':True,
        'original_registration_script_sha256':sha(Path('scripts/register_search_reports_v1675.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1676 registration recovered atomically;all prior registry profiles,114 accepted layers andV1492 promotion preserved. Build/startup/actual scenes pending.')
