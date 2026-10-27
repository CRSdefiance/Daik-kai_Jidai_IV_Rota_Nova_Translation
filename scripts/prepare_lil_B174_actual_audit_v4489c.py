"""Compare actual English skips with relocated operands, preserving the failed audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_actual_tools_v4489c')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/audit_lil_B174_actual_v4489b.py','scripts/audit_lil_B174_actual_v4489c.py',{
        'lil_B174_actual_v4489b':'lil_B174_actual_v4489c',
        "FONT = Path(":"RELOCATION=Path('work/analysis/lil_B174_relocation_v4477/nested_source_relocation_research.json')\nFONT = Path(",
        "    control,branch=read(CONTROL),read(BRANCH)":
            "    control,branch=read(CONTROL),read(BRANCH)\n    relocation=read(RELOCATION);target_spec=relocation['blocks'][0]\n    assert plan['relocation_plan_sha256']==sha(RELOCATION.read_bytes()) and target_spec['block']==174",
        '[PLAN, FONT, CONTROL, BRANCH, Path(__file__)]':'[PLAN, FONT, CONTROL, BRANCH, RELOCATION, Path(__file__)]',
        "            cases=[c for c in branch['cases'] if c['version']=='current' and c['offset']==row['original_source_offset'] and c['last_choice_or_result']==result]\n            assert len(cases)==1 and row['extent']==cases[0]['native_decoded_extent']":
            """            if case=='reviewed_English':
                mapped=next(c['new_offset'] for c in target_spec['command_map'] if c['old_offset']==row['original_source_offset'])
                cases=[c for c in target_spec['target_native_skip_cases'] if c['new_offset']==mapped and c['last_result']==result]
                assert len(cases)==1;expected_extent=cases[0]['native_extent']
                row['expected_extent_scope']='Relocated English operand, independently native-tested at its mapped cursor.'
            else:
                cases=[c for c in branch['cases'] if c['version']=='clean' and c['offset']==row['original_source_offset'] and c['last_choice_or_result']==result]
                assert len(cases)==1;expected_extent=cases[0]['native_decoded_extent']
                row['expected_extent_scope']='Exact clean Japanese operand, independently native-tested.'
            assert row['extent']==expected_extent
            row['independently_verified_native_extent']=expected_extent""",
        'actual_last_result_model_reused_from_source_bound_VM_contract=True':
            'actual_last_result_model_reused_from_source_bound_VM_contract=True,source_and_relocated_relative_operand_extents_distinguished=True,failed_original_extent_only_audit_preserved=True',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        finding='Source0100 at890 skips52 bytes; relocated English counterpart skips62 bytes because complete optional Emilio speech grew. Compare each version to its own native operand proof.',
        no_ROM_prose_input_observer_orcapture_change=True,no_boot_restarted=True,full_goal_complete=False))
    print('Prepared version-specific actual relative-extent audit; original failed comparison and all captures preserved.')
