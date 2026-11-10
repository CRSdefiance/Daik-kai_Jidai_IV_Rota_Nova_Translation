"""Bind the sealed atomic module to both exact positives and all substantive semantic failures."""
from pathlib import Path
from dk4tool.patch import hodram_B51_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B51_release_paths_v8595 import CONFIG,ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B51_atomic_binding_v8606')
POSITIVE=Path('work/analysis/Hodram_B51_atomic_positive_v8604/atomic_positive.json')
NEGATIVE=Path('work/analysis/Hodram_B51_atomic_challenges_v8605b/semantic_rejections.json')
if __name__=='__main__':
    assert not ROOT.exists();positive,negative=map(read,[POSITIVE,NEGATIVE]);conf=read(CONFIG);owned.check_dependencies(conf)
    assert positive['positive_lifecycles']==2 and positive['all_native_semantic_production_guards_enabled'] and positive['whole_output_equals_tested_reference']
    assert [p['mode'] for p in positive['cases']]==['direct-current','canonical-source-full-current-memory']
    for p in positive['cases']:
        assert p['one_complete_NDS_commit'] and p['original_object_still_exact_after_commit'] and p['original_object_identity_files_components_andserialized_bytes_exact_until_commit']
        assert p['planned_output_sha256']==conf['reference_ROM_sha256']==sha(ROM.read_bytes()) and len(p['report']['changed_records'])==5
    assert negative['negative_count']==len(negative['cases'])==17 and negative['all_changed_inputs_distinct_andexpected_semantic_guards_match']
    assert negative['all_protected_files_ROMs_registry_ledger_pins_andmodules_hash_exact'] and negative['zero_commits_andwhole_input_unchanged_forall_failures']
    assert all(c['rejected'] and c['commit_calls']==0 and c['actual_changed_input'] and c['original_object_files_components_andserialized_bytes_unchanged'] for c in negative['cases'])
    assert negative['only_production_digest_layer_bypassed_to_reach_semantics'] and negative['no_frozen_native_orsemantic_guard_bypassed']
    assert positive['cases'][0]['report']==positive['cases'][1]['report']
    wrong_path=Path('work/analysis/Hodram_B51_wrong_memory_v8605/wrong_memory_rejections.json');wrong=read(wrong_path)
    assert wrong['negative_count']==3 and wrong['every_wrong_image_rejected_before_commit_withall_guards_active'] and wrong['no_digest_orsemantic_bypass']
    assert all(c['actual_wrong_inmemory_image'] and c['commit_calls']==0 and c['whole_original_input_object_files_components_andserialized_bytes_unchanged'] for c in wrong['cases'])
    for path,digest in wrong['evidence'].items():assert sha(Path(path).read_bytes())==digest
    for p,h in positive['evidence'].items():assert sha(Path(p).read_bytes())==h
    ROOT.mkdir(parents=True);save(ROOT/'semantic_binding.json',dict(positive=str(POSITIVE),positive_sha256=sha(POSITIVE.read_bytes()),negative=str(NEGATIVE),negative_sha256=sha(NEGATIVE.read_bytes()),configuration=str(CONFIG),configuration_sha256=sha(CONFIG.read_bytes()),atomic_module=str(Path(owned.__file__)),atomic_module_sha256=sha(Path(owned.__file__).read_bytes()),both_input_lifecycles_one_complete_commit_exact_reference=True, lifecycle_reports_value_equal=True, wrong_memory=str(wrong_path),wrong_memory_sha256=sha(wrong_path.read_bytes()),all3_genuine_wrong_memory_inputs_rejected_withall_guards_active=True,all17_actually_changed_semantic_precommit_cases_rejected_without_mutation=True,all_frozen_andsemantic_guards_remained_enabled=True,only_outer_production_digest_layer_bypassed_in_negative_tests=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Bound B51 sealedmodule:both complete-ROM positives/17actual-changing semantic failures;whole input exact on every failure;all frozen/semantic guards active.No credit.')
