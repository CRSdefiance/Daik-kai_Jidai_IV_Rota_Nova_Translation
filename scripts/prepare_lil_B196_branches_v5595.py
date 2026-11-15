"""Prepare every original B196 relative site with whole-main-RAM guards."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_branch_tools_v5595')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/prove_lil_B142_B145_branches_v3578.py');text=source.read_text(encoding='utf-8')
    row=derive(source,'scripts/prove_lil_B196_branches_v5595.py',{
        'lil_B142_B145_branches_v3578':'lil_B196_branches_v5595',
        'work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json':
        'work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json',
        '                for last in (0,1,2,3,0xFFFFFFFF):':
        '                main_before=bytes(cpu.mem_read(0x02000000,0x400000))\n                for last in (0,1,2,3,0xFFFFFFFF):',
        '                    assert bytes(cpu.mem_read(STREAM,len(block)))==block':
        '                    assert bytes(cpu.mem_read(0x02000000,0x400000))==main_before\n                    assert bytes(cpu.mem_read(STREAM,len(block)))==block',
        '    assert len(cases)==10*len(edges)':'    assert len(edges)==52 and len(cases)==520 and len(cases)==10*len(edges)'})
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert not old-new and new-old==Counter({0x02000000:2,0x400000:2})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_whole_RAM_guarded_relative_checks.json',dict(derivation=row,
        all_original_native_integer_constants_preserved=True,only_added_native_constants_are_two_full4MiB_main_RAM_guard_reads=True,
        source_relative_sites=52,expected_native_clean_current_cases=520,no_event_or_choice_result_forced_in_gameplay=True,
        no_ROM_registry_ledger_or_credit_change=True,full_goal_complete=False))
