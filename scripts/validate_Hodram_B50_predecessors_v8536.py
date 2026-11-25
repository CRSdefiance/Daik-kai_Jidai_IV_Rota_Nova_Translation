"""Reproduce the complete V8475 ROM through both source-equivalent predecessor stages in memory."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_outcomes_editorial_v6 as outcomes
from dk4tool.patch import hodram_B49_editorial_v3 as B49
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prepare_Hodram_B50_builder_support_v8534 import SPECS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_predecessor_positive_v8536')
if __name__=='__main__':
    assert not ROOT.exists();derivation=read('work/analysis/Hodram_B50_builder_support_v8534/source_equivalence.json')
    for spec,d in zip(SPECS,derivation['namespace_only_outcomes_derivations'],strict=True):
        a,b=Path(d['previous']),Path(d['successor']);assert sha(a.read_bytes())==d['previous_sha256'] and sha(b.read_bytes())==d['successor_sha256']
        assert checked_text(a.read_text(encoding='utf-8'),spec[-1])==b.read_text(encoding='utf-8')
    d=derivation['B49_guard_import_only_derivation'];a,b=Path(d['previous']),Path(d['successor'])
    assert checked_text(a.read_text(encoding='utf-8'),{'hodram_outcomes_builder_guard_v5':'hodram_outcomes_builder_guard_v6'})==b.read_text(encoding='utf-8')
    parent=NdsImage.open(outcomes.PARENT);image=NdsImage(outcomes.CANONICAL,deepcopy(parent.rom));baseline=NdsImage.open(outcomes.CANONICAL)
    results=[]
    for label,module,config,expected in [('outcomes',outcomes,'translations/hodram_outcomes_editorial_release_v6.json',outcomes.ROM),('B49',B49,'translations/hodram_B49_editorial_release_v4.json',B49.ROM)]:
        original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()};calls=[];commit=module.commit_image
        def trapped(target,planned):
            assert target is image and target.rom is original and bytes(original.save())==before and original.files==files and {p:v for p,v in target.iter_components()}==components
            assert planned is not original and bytes(planned.save())==expected.read_bytes();calls.append('one-complete-NDS');commit(target,planned)
        module.commit_image=trapped
        try:report=module.apply_release(image,baseline,config=config)
        finally:module.commit_image=commit
        assert calls==['one-complete-NDS'] and bytes(original.save())==before and bytes(image.rom.save())==expected.read_bytes()
        results.append(dict(stage=label,config=config,config_sha256=sha(Path(config).read_bytes()),before_sha256=sha(before),after_sha256=sha(bytes(image.rom.save())),changed_records=len(report['changed_records']),one_complete_NDS_commit=True,original_object_files_components_serialized_bytes_exact_until_commit=True,original_object_still_exact_after_commit=True))
        print('PASS compatible predecessor',label,results[-1]['after_sha256'],flush=True)
    current=Path('out/all_routes_combined_v8475_candidate.nds');assert bytes(image.rom.save())==current.read_bytes()
    assert [r['changed_records'] for r in results]==[6,16]
    assert outcomes.resolve_config(outcomes.PRESERVED_CONFIG)==outcomes.CONFIG
    ROOT.mkdir(parents=True);save(ROOT/'whole_V8475_byte_exact.json',dict(stages=results,whole_registered_V8475_ROM_byte_exact=True,current_V8475_path=str(current),current_V8475_sha256=sha(current.read_bytes()),canonical_source_withfull_predecessor_memory=True,all_native_semantic_production_gates_enabled=True,all_original524_outcomes_and663_B49_dependency_entries_preserved=True,registered_old_v3_outcomes_alias_still_exact=True,no_builder_registry_disk_ROM_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path(outcomes.__file__),Path(B49.__file__),Path('work/analysis/Hodram_B50_builder_support_v8534/source_equivalence.json')]}))
    print('Compatible outcomesv6 plusB49v3 reproduce full registeredV8475 byte-for-byte,with all guards active andtwo whole-object commits;no disk ROM/replay/credit.')
