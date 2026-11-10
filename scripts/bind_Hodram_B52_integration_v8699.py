"""Bind atomic/shared/prefix checks and extend the release closure without changing semantics."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B52_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_release_paths_v8693 import CONFIG,PARENT,ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_integration_binding_v8699')
FINAL=Path('translations/hodram_B52_editorial_release_v3.json')
PROOFS=dict(atomic='work/analysis/Hodram_B52_atomic_positive_v8690b/atomic_positive.json',
    wrong='work/analysis/Hodram_B52_wrong_memory_v8691b/wrong_memory_rejections.json',
    semantic='work/analysis/Hodram_B52_atomic_challenges_v8692/semantic_rejections.json',
    shared='work/analysis/Hodram_B52_shared_extension_v8697/shared_extension_validation.json',
    builder='work/analysis/Hodram_B52_builder_validation_v8695/exact_builder_inverse_cases.json',
    support='work/analysis/Hodram_B52_builder_support_v8694b/source_equivalence.json',
    prefix='work/analysis/Hodram_B52_predecessor_positive_v8696/whole_V8609_byte_exact.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists();data={k:read(p) for k,p in PROOFS.items()}
    assert data['atomic']['positive_lifecycles']==2 and data['atomic']['one_complete_NDS_commit_percase'] and data['atomic']['all_native_semantic_production_guards_enabled']
    cases=data['atomic']['cases'];assert cases[0]['report']==cases[1]['report']
    assert data['wrong']['negative_count']==3 and data['wrong']['no_digest_orsemantic_bypass']
    assert data['semantic']['negative_count']==16 and data['semantic']['no_frozen_native_source_editorial_orsemantic_guard_bypassed']
    assert data['shared']['negative_count']==6 and data['shared']['positive_lifecycles']==1 and data['shared']['no_guard_digest_orsemantic_bypass']
    assert data['builder']['negative_count']==29 and len(data['builder']['positives'])==5
    assert data['prefix']['whole_registered_V8609_ROM_byte_exact'] and data['prefix']['current_V8609_sha256']==sha(PARENT.read_bytes())
    assert data['prefix']['all_native_source_editorial_semantic_andproduction_guards_enabled']
    original=read(CONFIG);owned.check_dependencies(original);conf=deepcopy(original)
    previous=read('translations/hodram_B51_editorial_release_v2.json')
    for p,h in previous['dependencies'].items():assert p not in conf['dependencies'] or conf['dependencies'][p]==h;conf['dependencies'][p]=h
    additional=[CONFIG,Path(__file__),Path('translations/hodram_B51_editorial_release_v2.json'),Path('dk4tool/patch/hodram_b52_extension_v2.py'),
        Path('scripts/validate_Hodram_B52_atomic_v8690b.py'),Path('scripts/validate_Hodram_B52_wrong_memory_v8691b.py'),
        Path('scripts/challenge_Hodram_B52_atomic_v8692.py'),Path('scripts/validate_Hodram_B52_shared_extension_v8697.py'),
        Path('scripts/validate_Hodram_B52_builder_v8695.py'),Path('scripts/validate_Hodram_B52_predecessors_v8696.py'),*map(Path,PROOFS.values())]
    for p in additional:
        key,h=str(p.resolve()),sha(p.read_bytes());assert key not in conf['dependencies'] or conf['dependencies'][key]==h;conf['dependencies'][key]=h
    assert all(conf['dependencies'][p]==h for p,h in original['dependencies'].items())
    assert {k:v for k,v in conf.items() if k!='dependencies'}=={k:v for k,v in original.items() if k!='dependencies'}
    save(FINAL,conf);owned.check_dependencies(conf)
    ROOT.mkdir(parents=True)
    save(ROOT/'integration_binding.json',dict(configuration=str(FINAL),configuration_sha256=sha(FINAL.read_bytes()),
        previous_configuration=str(CONFIG),previous_configuration_sha256=sha(CONFIG.read_bytes()),
        prior_dependencies=len(original['dependencies']),final_dependencies=len(conf['dependencies']),
        all_original998_entries_andall_compatible_prefix_dependencies_retained_exact=True,
        only_dependency_closure_extended_all_release_semantics_andsource_approvals_unchanged=True,
        lifecycle_reports_value_equal=True,both_lifecycles_one_whole_object_commit_exact_reference=True,
        genuine_wrong_memory_cases=3,semantic_zero_commit_cases=16,shared_zero_commit_cases=6,builder_changed_input_cases=29,
        whole_registered_V8609_prefix_reproduced_withall_guards=True,
        reference_ROM_sha256=sha(ROM.read_bytes()),
        no_live_builder_registry_ROM_orcompletion_credit_change=True,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [*PROOFS.values(),*additional]}))
    print('B52 integration bound:equal lifecycle reports/3wrong-memory/16semantic/6shared failures/29builder failures/fullV8609 prefix. Final dependencies',len(conf['dependencies']),';all998 prior entries retained. No ROM/credit.')
