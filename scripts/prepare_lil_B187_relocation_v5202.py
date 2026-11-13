"""Prepare reversible B187 linear relocation and final stored-target native checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_relocation_tools_v5202')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B185_relocation_v5105.py','scripts/research_lil_B187_relocation_v5202.py',{
        'B185':'B187','relocation_v5105':'relocation_v5202','editorial_manuscript_v4':'editorial_manuscript_v3','combined_v5076':'combined_v5177',
        'Relocate all8':'Relocate all16','preserve7 progressive':'preserve15 progressive',
        'len(source)==old_end==388':'len(source)==680 and old_end==678 and source[old_end:]==bytes(2)',
        "len(spec['all_current_native_commands'])==11":"len(spec['all_current_native_commands'])==19",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==8":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==16",
        'number==185':'number==187','==[384]':'==[674]',
        'assert bytes(restored)==source[:old_end]':'assert bytes(restored)==source[:old_end]\n        assert bytes(restored)+source[old_end:]==source',
        'inverse_restoration_recovers_every_original_logical_byte=True':'inverse_restoration_recovers_every_original_logical_byte=True,inverse_plus_exact_original_two_tailzeros_recovers_entire_source=True',
        "sum(len(r['text_records']) for r in results)==8":"sum(len(r['text_records']) for r in results)==16",
        "sum(len(r['command_map']) for r in results)==11":"sum(len(r['command_map']) for r in results)==19",
        'not in [185]':'not in [187]','all8speech':'all16speech',
        '11structural commands/8speech/7progressive':'19structural commands/16speech/15progressive',
    })]
    rows.append(derive('scripts/prove_lil_B186_stored_v5158.py','scripts/prove_lil_B187_stored_v5203.py',{
        'B186':'B187','stored_v5158':'stored_v5203','relocation_v5157':'relocation_v5202','voices_v5133':'voices_v5189',
        'editorial_manuscript_v5':'editorial_manuscript_v3','Verify all12':'Verify all16',
        '[174,175,254]':'[87,155,254]','len(cases)==12':'len(cases)==16','fresh+reused==48':'fresh+reused==64',
        'all12_final_stored_targets48_macro_cases':'all16_final_stored_targets64_macro_cases',
        'current_final_stored_macro_alignment_cases=48':'current_final_stored_macro_alignment_cases=64',
        'all12_final_targets':'all16_final_targets','stored_targets=12,progressive=11':'stored_targets=16,progressive=15','macro_cases=48':'macro_cases=64',
        'actual_selected_B186_scene_predicates_three_effects_C200_and_end_reachability_unexecuted':
        'actual_selected_B187_scene_A000_C200_and_end_reachability_unexecuted',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_linear_relocation_and_stored_checks.json',dict(tools=rows,
        source_stored_bytes=680,source_logical_end=678,source_alignment_tailzeros=2,source_commands=19,speeches=16,progressive=15,FE=1,
        relative_sites=0,predicates=0,A000=1,C200=1,source_end=674,expected_stored_alignment_cases=64,
        target_lengths_to_be_measured=True,exact_inverse_includes_original_tailzeros=True,
        no_ROM_registry_ledger_or_review_credit_change=True,full_goal_complete=False))
    print('Prepared B187 linear relocation/inverse and64 final stored native cases;target lengths will be measured.')
