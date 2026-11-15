"""Prepare reversible twenty-record relocation and final stored native proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B195_relocation_tools_v5561')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B193_relocation_v5461.py','scripts/research_lil_B195_relocation_v5561.py',{
        'B193':'B195','relocation_v5461':'relocation_v5561','combined_v5437':'combined_v5531',
        'len(source)==668 and old_end==666':'len(source)==712 and old_end==710',
        "len(spec['all_current_native_commands'])==18":"len(spec['all_current_native_commands'])==23",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==15":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==20",
        'number==193':'number==195','==[662]':'==[706]',"sum(len(r['text_records']) for r in results)==15":"sum(len(r['text_records']) for r in results)==20",
        "sum(len(r['command_map']) for r in results)==18":"sum(len(r['command_map']) for r in results)==23",'[193]':'[195]',
        'all15':'all20','Relocate all15':'Relocate all20','preserve14 progressive':'preserve19 progressive',
        '18structural commands/15speech/14progressive':'23structural commands/20speech/19progressive',
    })]
    rows.append(derive('scripts/prove_lil_B193_stored_v5462.py','scripts/prove_lil_B195_stored_v5562.py',{
        'B193':'B195','stored_v5462':'stored_v5562','relocation_v5461':'relocation_v5561','voices_v5448':'voices_v5542',
        'in [166,167,168,254]':'in [92,103,119,254]','len(cases)==15':'len(cases)==20','fresh+reused==60':'fresh+reused==80',
        'all15':'all20','targets60':'targets80','current_final_stored_macro_alignment_cases=60':'current_final_stored_macro_alignment_cases=80',
        'stored_targets=15,progressive=14':'stored_targets=20,progressive=19','macro_cases=60':'macro_cases=80',
        'Verify all15':'Verify all20',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,source_commands=23,speeches=20,
        source_stored_logical=[712,710],source_tailzeros=2,source_relative_sites=0,source_macros=0,
        approved_v1_formatter_and_three_row_R17_unchanged=True,target_sizes_and_parity_to_be_measured=True,
        no_ROM_registry_ledger_or_credit_change=True,full_goal_complete=False))
