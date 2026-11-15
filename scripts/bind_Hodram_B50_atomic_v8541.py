"""Bind the sealed atomic module to both exact positives and all substantive semantic failures."""
from pathlib import Path
from dk4tool.patch import hodram_B50_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B50_release_paths_v8537 import CONFIG,ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_atomic_binding_v8541')
POSITIVE=Path('work/analysis/Hodram_B50_atomic_positive_v8539/atomic_positive.json')
NEGATIVE=Path('work/analysis/Hodram_B50_atomic_challenges_v8540/semantic_rejections.json')
if __name__=='__main__':
    assert not ROOT.exists();positive,negative=map(read,[POSITIVE,NEGATIVE]);conf=read(CONFIG);owned.check_dependencies(conf)
    assert positive['positive_lifecycles']==2 and positive['all_native_semantic_production_guards_enabled'] and positive['whole_output_equals_tested_reference']
    assert [p['mode'] for p in positive['cases']]==['direct-current','canonical-source-full-current-memory']
    for p in positive['cases']:
        assert p['one_complete_NDS_commit'] and p['original_object_still_exact_after_commit'] and p['original_object_identity_files_components_andserialized_bytes_exact_until_commit']
        assert p['planned_output_sha256']==conf['reference_ROM_sha256']==sha(ROM.read_bytes()) and len(p['report']['changed_records'])==3
    assert negative['negative_count']==len(negative['cases'])==16 and negative['all_changed_inputs_distinct_andexpected_semantic_guards_match']
    assert negative['all_protected_files_ROMs_registry_ledger_pins_andmodules_hash_exact'] and negative['zero_commits_andwhole_input_unchanged_forall_failures']
    assert all(c['rejected'] and c['commit_calls']==0 and c['actual_changed_input'] and c['original_object_files_components_andserialized_bytes_unchanged'] for c in negative['cases'])
    assert negative['only_production_digest_layer_bypassed_to_reach_semantics'] and negative['no_frozen_native_orsemantic_guard_bypassed']
    for p,h in positive['evidence'].items():assert sha(Path(p).read_bytes())==h
    ROOT.mkdir(parents=True);save(ROOT/'semantic_binding.json',dict(positive=str(POSITIVE),positive_sha256=sha(POSITIVE.read_bytes()),negative=str(NEGATIVE),negative_sha256=sha(NEGATIVE.read_bytes()),configuration=str(CONFIG),configuration_sha256=sha(CONFIG.read_bytes()),atomic_module=str(Path(owned.__file__)),atomic_module_sha256=sha(Path(owned.__file__).read_bytes()),both_input_lifecycles_one_complete_commit_exact_reference=True,all16_actually_changed_semantic_precommit_cases_rejected_without_mutation=True,all_frozen_andsemantic_guards_remained_enabled=True,only_outer_production_digest_layer_bypassed_in_negative_tests=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Bound B50 sealedmodule:both complete-ROM positives/16actual-changing semantic failures;whole input exact on every failure;all frozen/semantic guards active.No credit.')
