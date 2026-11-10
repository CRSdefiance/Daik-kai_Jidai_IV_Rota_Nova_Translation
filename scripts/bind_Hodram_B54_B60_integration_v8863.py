"""Bind atomic/shared/prefix checks and extend the release closure without changing semantics."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B54_B60_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B54_B60_release_paths_v8853 import CONFIG,PARENT,ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_integration_binding_v8863')
FINAL=Path('translations/hodram_B54_B60_editorial_release_v2.json')
PROOFS=dict(atomic='work/analysis/Hodram_B54_B60_atomic_positive_v8857/atomic_positive.json',
    wrong='work/analysis/Hodram_B54_B60_wrong_memory_v8858/wrong_memory_rejections.json',
    semantic='work/analysis/Hodram_B54_B60_atomic_challenges_v8859/semantic_rejections.json',
    shared='work/analysis/Hodram_B54_B60_shared_extension_v8860/shared_extension_validation.json',
    builder='work/analysis/Hodram_B52_builder_validation_v8695/exact_builder_inverse_cases.json',
    support='work/analysis/Hodram_B52_builder_support_v8694b/source_equivalence.json',
    prefix='work/analysis/Hodram_B31_B53_release_v8779/registered_release_verification.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists();data={k:read(p) for k,p in PROOFS.items()}
    assert data['atomic']['positive_lifecycles']==2 and data['atomic']['one_complete_NDS_commit_percase'] and data['atomic']['all_native_semantic_production_guards_enabled']
    cases=data['atomic']['cases'];assert cases[0]['report']==cases[1]['report']
    assert data['wrong']['negative_count']==3 and data['wrong']['no_digest_orsemantic_bypass']
    assert data['semantic']['negative_count']==4 and data['semantic']['no_frozen_native_source_editorial_orsemantic_guard_bypassed']
    assert data['shared']['negative_count']==1 and data['shared']['positive_lifecycles']==1 and data['shared']['no_guard_digest_orsemantic_bypass']
    assert data['builder']['negative_count']==29 and len(data['builder']['positives'])==5
    assert data['prefix']['whole_ROM_equals_pinned_approved_reference'] and data['prefix']['candidate_sha256']==sha(PARENT.read_bytes()) and data['prefix']['manifest_batches']==647 and data['prefix']['accepted_layers']==114
    assert data['prefix']['all18_registered_release_checks_pass'] and data['prefix']['all110_release_dialogue_regressions_pass'] and data['prefix']['whole_clean_input_ROM_reconstruction_byte_exact']
    original=read(CONFIG);owned.check_dependencies(original);conf=deepcopy(original)
    previous=read('translations/hodram_B31_B53_editorial_release_v2.json')
    for p,h in previous['dependencies'].items():assert p not in conf['dependencies'] or conf['dependencies'][p]==h;conf['dependencies'][p]=h
    additional=[CONFIG,Path(__file__),Path('translations/hodram_B31_B53_editorial_release_v2.json'),Path('dk4tool/patch/hodram_b54_b60_extension_v1.py'),
        Path('scripts/validate_Hodram_B54_B60_atomic_v8857.py'),Path('scripts/validate_Hodram_B54_B60_wrong_memory_v8858.py'),
        Path('scripts/challenge_Hodram_B54_B60_atomic_v8859.py'),Path('scripts/validate_Hodram_B54_B60_shared_v8860.py'),
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
        all_original3562_entries_andentire_registered_V8778_dependencies_retained_exact=True,
        only_dependency_closure_extended_all_release_semantics_andsource_approvals_unchanged=True,
        lifecycle_reports_value_equal=True,both_lifecycles_one_whole_object_commit_exact_reference=True,
        genuine_wrong_memory_cases=3,semantic_zero_commit_cases=4,shared_zero_commit_cases=1,unchanged_builder_changed_input_cases_reused=29,
        entire_verified_registered_V8778_prefix_preserved=True,
        reference_ROM_sha256=sha(ROM.read_bytes()),
        no_live_builder_registry_ROM_orcompletion_credit_change=True,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [*PROOFS.values(),*additional]}))
    print('B54-B60 bound:equal lifecycle reports/3wrong-memory/4semantic/1late-target failures;unchanged builder tests andwhole verifiedV8778 prefix reused. Final dependencies',len(conf['dependencies']),';all3562 prior entries retained. No ROM/credit.')
