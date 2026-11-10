"""Prepare reversible twelve-object relocation with six conditional operand fixups."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_relocation_tools_v5157')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B182_relocation_v4893.py','scripts/research_lil_B186_relocation_v5157.py',{
        'B182':'B186','relocation_v4893':'relocation_v5157','editorial_manuscript_v3':'editorial_manuscript_v5','combined_v4867':'combined_v5122',
        'all8 B182 speeches;preserve ten relative sites,two500 RNG predicates':'all12 B186 speeches;preserve six relative sites,one700 RNG predicate',
        'len(source)==old_end==636':"len(source)==652 and old_end==650 and source[old_end:]==bytes(2)",
        "len(spec['all_current_native_commands'])==25":"len(spec['all_current_native_commands'])==24",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==8":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==12",
        "sum(c['word']==0x8000 for c in spec['all_current_native_commands'])==2":"sum(c['word']==0x8000 for c in spec['all_current_native_commands'])==1",
        'number==182':'number==186','==[632]':'==[646]',
        "sum(len(r['text_records']) for r in results)==8":"sum(len(r['text_records']) for r in results)==12",
        "sum(len(r['relative_skip_fixups']) for r in results)==10":"sum(len(r['relative_skip_fixups']) for r in results)==6",
        "sum(len(r['target_native_skip_cases']) for r in results)==50":"sum(len(r['target_native_skip_cases']) for r in results)==30",
        "sum(len(r['command_map']) for r in results)==25":"sum(len(r['command_map']) for r in results)==24",
        'not in [182]':'not in [186]',
        'all8speech_and7_nonrelative_leaves_preserved':'all12speech_and6_nonrelative_leaves_preserved',
        'all10_source_relative_sites_and50_native_skip_cases_preserved':'all6_source_relative_sites_and30_native_skip_cases_preserved',
        '25structural commands/8speech/1FE/ten relative sites/50 target cases,no pause,three alternative A000s/two500 RNG predicates/C200/end':
        '24structural commands/12speech/1FE/six relative sites/30 target cases,no pause,three alternative A000s/one700 RNG predicate/C200/end',
        "assert bytes(restored)==source[:old_end]":"assert bytes(restored)==source[:old_end]\n        assert bytes(restored)+source[old_end:]==source",
        'inverse_restoration_recovers_every_original_logical_byte=True':'inverse_restoration_recovers_every_original_logical_byte=True,inverse_plus_exact_original_two_tailzeros_recovers_entire_source=True',
    })]
    rows.append(derive('scripts/prove_lil_B182_stored_v4894.py','scripts/prove_lil_B186_stored_v5158.py',{
        'B182':'B186','stored_v4894':'stored_v5158','relocation_v4893':'relocation_v5157','voices_v4879':'voices_v5133',
        'editorial_manuscript_v3':'editorial_manuscript_v5','Verify all8':'Verify all12',
        '[166,167,254]':'[174,175,254]','len(cases)==8':'len(cases)==12','fresh+reused==32':'fresh+reused==48',
        'all8_final_stored_targets32_macro_cases':'all12_final_stored_targets48_macro_cases',
        'current_final_stored_macro_alignment_cases=32':'current_final_stored_macro_alignment_cases=48',
        'all8_final_targets':'all12_final_targets','stored_targets=8,progressive=7':'stored_targets=12,progressive=11','macro_cases=32':'macro_cases=48',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_reversible_conditional_relocation.json',dict(tools=rows,
        source_stored_bytes=652,source_logical_end=650,source_trailing_zeros=2,source_commands=24,speeches=12,progressive=11,FE=1,
        relative_sites=6,predicates=1,raw_threshold=700,alternative_A000=3,C200=1,single_end=646,stored_alignment_cases=48,
        exact_original_tailzeros_in_inverse=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared B186 conditional relocation and48 stored cases;preserve six fixups and two source tailzeros.')
