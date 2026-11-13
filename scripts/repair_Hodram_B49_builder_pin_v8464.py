"""Preserve failed registration;pin frozen builder inverse instead of accidental mutable whole-file digest."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import hodram_B49_editorial_v2 as owned
from dk4tool.patch.hodram_outcomes_builder_guard_v5 import BUILDER,validate_builder_bytes
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_builder_pin_fix_v8464')
REG=Path('work/analysis/Hodram_B49_registration_v8458')
OLD=Path('translations/hodram_B49_editorial_release_v2.json')
NEW=Path('translations/hodram_B49_editorial_release_v3.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists() and not (REG/'registration_receipt.json').exists()
    registry=read('translations/release_stack.json');assert registry==read(REG/'release_stack.planned.json') and BUILDER.read_bytes()==(REG/'planned_builder.bin').read_bytes()
    assert not Path('out/all_routes_combined_v8459_candidate.nds').exists()
    conf=read(OLD);prior=deepcopy(conf);key=str(BUILDER);old_digest=conf['dependencies'][key]
    frozen=read('translations/hodram_outcomes_native_contract_v1.json');digest=frozen['dependencies'][key];guard=read('work/analysis/Hodram_B49_builder_v8452/exact_builder_inverse_cases.json')
    assert old_digest==sha((REG/'build_integrated_release.py.before').read_bytes()) and old_digest!=digest==guard['full_original_source_inverse_sha256']
    assert validate_builder_bytes(BUILDER.read_bytes(),digest)['corrected_B49_stage_version']==2
    conf['dependencies'][key]=digest;conf['dependencies'][str(OLD.resolve())]=sha(OLD.read_bytes())
    assert all(conf[k]==prior[k] for k in prior if k!='dependencies') and all(conf['dependencies'][p]==h for p,h in prior['dependencies'].items() if p!=key)
    save(NEW,conf);owned.check_dependencies(conf);ROOT.mkdir(parents=True)
    save(REG/'failed_registration_terminal.json',dict(terminal=True,returncode=1,phase='postregistration-dependency-check-before-any-ROM-build',profile='all-routes-unified-v8459',builder_andregistry_match_preserved_planned_bytes=True,failed_profile_andall_backups_preserved=True,no_candidate_ROM_orcompletion_credit=True,cause='module-discovery copied a mutable builder digest into the new B49 production config;exact original417-source inverse digest is required',configuration=str(OLD),configuration_sha256=sha(OLD.read_bytes()),successor_configuration=str(NEW),successor_configuration_sha256=sha(NEW.read_bytes()),new_credit=0,full_goal_complete=False))
    result=derive('scripts/validate_Hodram_B49_atomic_v8456.py','scripts/validate_Hodram_B49_atomic_v8465.py',{
        "ROOT=Path('work/analysis/Hodram_B49_atomic_positive_v8456')":"CONFIG='translations/hodram_B49_editorial_release_v3.json'\nROOT=Path('work/analysis/Hodram_B49_atomic_positive_v8465')",
        'report=owned.apply_release(image,baseline)':'report=owned.apply_release(image,baseline,config=CONFIG)',
        'Path(owned.CONFIG)':'Path(CONFIG)',
    })
    save(ROOT/'pin_correction.json',dict(previous_configuration=str(OLD),previous_configuration_sha256=sha(OLD.read_bytes()),configuration=str(NEW),configuration_sha256=sha(NEW.read_bytes()),builder_dependency_path=key,preserved_accidental_mutable_digest=old_digest,guarded_original_builder_inverse_digest=digest,only_one_dependency_predicate_corrected_all_other_prior_entries_exact=True,no_frozen_native_orsemantic_guard_removed=True,all_source_prose_compiler_runtime_geometry_evidence_andsemantic_gates_unchanged=True,new_positive_derivation=result,failed_registration_preserved=str(REG/'failed_registration_terminal.json'),current_builder_andregistry_not_changed_by_this_repair=True,registered_successor_full_positive_andclean_patch_startup_completion_pending=True,new_credit=0,full_goal_complete=False))
    print('Preserved failed V8459 registration;configv3 binds exactoriginalbuilder inverse/allotherpins unchanged. Corrected whole-positive prepared;no ROM orcredit.')
