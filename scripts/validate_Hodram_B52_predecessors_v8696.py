"""Reproduce the full registered V8609 prefix with every compatibility guard active."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_outcomes_editorial_v8 as outcomes
from dk4tool.patch import hodram_B49_editorial_v5 as B49
from dk4tool.patch import hodram_B50_editorial_v3 as B50
from dk4tool.patch import hodram_B51_editorial_v2 as B51
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prepare_Hodram_B52_builder_support_v8694b import SPECS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_predecessor_positive_v8696')
SUPPORT=Path('work/analysis/Hodram_B52_builder_support_v8694b/source_equivalence.json')

if __name__=='__main__':
    assert not ROOT.exists();support=read(SUPPORT)
    for spec,row in zip(SPECS,support['namespace_only_outcomes_derivations'],strict=True):
        a,b=Path(row['previous']),Path(row['successor'])
        assert sha(a.read_bytes())==row['previous_sha256'] and sha(b.read_bytes())==row['successor_sha256']
        assert checked_text(a.read_text(encoding='utf-8'),spec[-1])==b.read_text(encoding='utf-8')
    for row in support['B49_B50_B51_guard_import_only_derivations']:
        a,b=Path(row['previous']),Path(row['successor'])
        assert checked_text(a.read_text(encoding='utf-8'),{'hodram_outcomes_builder_guard_v7':'hodram_outcomes_builder_guard_v8'})==b.read_text(encoding='utf-8')
    for row in support['configurations']:
        old,new=read(row['old_configuration']),read(row['new_configuration'])
        assert all(new['dependencies'][p]==h for p,h in old['dependencies'].items())
        assert {k:v for k,v in old.items() if k!='dependencies'}=={k:v for k,v in new.items() if k!='dependencies'}
    for p,h in support['unchanged_frozen_native_contracts'].items():assert sha(Path(p).read_bytes())==h
    parent=NdsImage.open(outcomes.PARENT);image=NdsImage(outcomes.CANONICAL,deepcopy(parent.rom));baseline=NdsImage.open(outcomes.CANONICAL)
    stages=[];ROOT.mkdir(parents=True)
    for label,module,config,expected in [
        ('outcomes',outcomes,'translations/hodram_outcomes_editorial_release_v8.json',outcomes.ROM),
        ('B49',B49,'translations/hodram_B49_editorial_release_v6.json',B49.ROM),
        ('B50',B50,'translations/hodram_B50_editorial_release_v3.json',B50.ROM),
        ('B51',B51,'translations/hodram_B51_editorial_release_v2.json',B51.ROM)]:
        original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()};calls=[];commit=module.commit_image

        def trapped(target,planned):
            assert target is image and image.rom is original and bytes(original.save())==before and original.files==files and {p:v for p,v in image.iter_components()}==components
            assert planned is not original and bytes(planned.save())==expected.read_bytes();calls.append('one-complete-NDS');commit(target,planned)

        module.commit_image=trapped
        try:report=module.apply_release(image,baseline,config=config)
        finally:module.commit_image=commit
        assert calls==['one-complete-NDS'] and bytes(original.save())==before and bytes(image.rom.save())==expected.read_bytes()
        row=dict(stage=label,config=config,config_sha256=sha(Path(config).read_bytes()),before_sha256=sha(before),after_sha256=sha(bytes(image.rom.save())),changed_records=len(report['changed_records']),one_complete_NDS_commit=True,
             original_object_identity_files_components_andserialized_bytes_exact_until_commit=True)
        save(ROOT/(label+'.json'),row);stages.append(row);print('PASS compatible prefix',label,row['after_sha256'],flush=True)
    current=Path('out/all_routes_combined_v8609_candidate.nds')
    assert bytes(image.rom.save())==current.read_bytes() and [s['changed_records'] for s in stages]==[6,16,3,5]
    assert outcomes.resolve_config(outcomes.PRESERVED_CONFIG)==outcomes.CONFIG
    save(ROOT/'whole_V8609_byte_exact.json',dict(stages=stages,whole_registered_V8609_ROM_byte_exact=True,
         current_V8609_sha256=sha(current.read_bytes()),canonical_source_full_predecessor_memory=True,
         all_native_source_editorial_semantic_andproduction_guards_enabled=True,
         all_original_dependency_entries_andfrozen_native_contracts_preserved=True,
         original_outcomes_v3_alias_still_exact=True,no_disk_ROM_live_builder_registry_orcredit_change=True,
         full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [__file__,SUPPORT,outcomes.__file__,B49.__file__,B50.__file__,B51.__file__]}))
    print('Compatible full prefix reproduces registeredV8609 byte-for-byte with all production guards. No disk ROM/new gameplay/credit.')
