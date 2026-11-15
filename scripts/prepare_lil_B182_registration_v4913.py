"""Prepare meaningful atomic negatives and cumulative B182 registration."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B182_registration_tools_v4913')
if __name__=='__main__':
    assert not ROOT.exists()
    p=Path('scripts/register_lil_B180_v4820d.py');old=p.read_text(encoding='utf-8')
    a=old.index("        description='Complete V4766");b=old.index("        note=",a)
    description="        description='Complete V4867 stack plus8 B182 whole-exchange reviews:6 revisions/2 justified retentions,seven progressive Lady166/167 and one prospective Gems/London notice. All25 source commands,two500 predicates,ten relative sites,three alternative A000s,C200/end preserved. Exact optional operand scratch/RNG ownership bound. Two9001-frame content cold boots show8 complete panels and normal return;13 timing differences,18 later A-indicator RGB differences and unequal final RNG remain disclosed.115 nontext samples,five state groups,whole actor and final RGB agree.',\n"
    tool=derive(str(p),'scripts/register_lil_B182_v4913.py',{
        old[a:b]:description,'B180':'B182','editorial_v4 as owned':'editorial_v1 as owned',
        'from dk4tool.patch.lil_B180_editorial_v4 import':'from dk4tool.patch.lil_B182_editorial_v1 import',
        'registration_v4820d':'registration_v4913','all-routes-unified-v4821':'all-routes-unified-v4914',
        'combined_v4766':'combined_v4867','all-routes-unified-v4766':'all-routes-unified-v4867','V4766':'V4867',
        'editorial_handoff_verification_v4818b':'editorial_handoff_verification_v4911',
        'reference_approval_v4816':'reference_approval_v4909','loader_v4802':'loader_v4899',
        "'postscene_native_state_proof','predicate_RNG_ownership_proof','current_C200_source_ownership_proof'":
        "'postscene_native_state_proof','current_C200_source_ownership_proof'",
        'native_approval_v4795/all11':'native_approval_v4892/all8','actual_v4811c/actual_all11':'actual_v4906/actual_all8',
        'deps.update([native_approval,actual_proof])':
        "operand='work/analysis/lil_B182_predicate500_v4896/all24_aligned_and_unaligned_original500_ownership_cases.json'\n    deps.update([native_approval,actual_proof,operand])",
        'native_approval=native_approval,actual_proof=actual_proof,dependencies=':
        'native_approval=native_approval,actual_proof=actual_proof,operand_ownership_proof=operand,dependencies=',
        "len(proof['changed_records'])==11":"len(proof['changed_records'])==8",
        'complete_matching_observations=10':'complete_matching_observations=7',
        "('concealed-town-difference',doc['postscene_native_state_proof'],lambda v:v['postscene9001_native_component_equality'].update(persistent_objects=True))":
        "('invented-town-difference',doc['postscene_native_state_proof'],lambda v:v['postscene9001_native_component_equality'].update(persistent_objects=False))",
        "    for label,path,edit in mutations:reject(label,path,edit)":
        "    mutations.extend([\n        ('missing-operand-case',operand,lambda v:v['cases'].pop()),\n        ('wrong-scratch-address',operand,lambda v:next(r for r in v['cases'] if r['operand_pointer_unaligned'])['all_original_native_writes'][0].update(address=0x02279604)),\n        ('wrong-scratch-value',operand,lambda v:next(r for r in v['cases'] if r['operand_pointer_unaligned'])['all_original_native_writes'][0].update(value=501)),\n        ('unowned-write-approved',operand,lambda v:v['cases'][0].update(full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch=False)),\n        ('emulator-seed-forcing',operand,lambda v:v.update(actual_emulator_seed_writes=1)),\n        ('missing-threshold-boundary',operand,lambda v:v['cases'][0].update(roll=0)),\n    ])\n    for label,path,edit in mutations:reject(label,path,edit)",
        'build_integrated_release_v4820d.tmp':'build_integrated_release_v4913.tmp',
        'expected_manifest_batches=562':'expected_manifest_batches=564',
        'positive_records=11':'positive_records=8','expected_batches=562':'expected_batches=564'
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_registration.json',dict(tool=tool,
        parent_profile='all-routes-unified-v4867',profile='all-routes-unified-v4914',
        no_registry_ROM_or_credit_change=True,full_goal_complete=False))
    print('Prepared B182 cumulative registration with distinct operand/scratch rejection controls.')
