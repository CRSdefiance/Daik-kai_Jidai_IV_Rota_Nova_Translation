"""Derive B175 inverse-checked relocation with both declared endwords intact."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B175_relocation_tools_v4521')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/research_lil_B174_relocation_v4477.py','scripts/research_lil_B175_relocation_v4521.py',{
        'Relocate all33 B174 speeches;preserve conditional Emilio,four relative sites,predicate,two A000s,C200,eight leaves and single end.':
            'Relocate all32 B175 speeches;preserve23 progressive,nine FE,seven leaves,C200 and both ends.',
        'lil_B174_relocation_v4477':'lil_B175_relocation_v4521',
        'lil_B174_editorial_manuscript_v5':'lil_B175_editorial_manuscript_v3',
        'all_routes_combined_v4445':'all_routes_combined_v4496',
        'number==174 and len(end_maps)==1':'number==175 and len(end_maps)==2',
        '[2086] # one complete source tail end preserved':'[1702,1706] # both complete source endwords preserved',
        "for r in results)==33":"for r in results)==32",
        "sum(len(r['relative_skip_fixups']) for r in results)==4":"sum(len(r['relative_skip_fixups']) for r in results)==0",
        "sum(len(r['target_native_skip_cases']) for r in results)==20":"sum(len(r['target_native_skip_cases']) for r in results)==0",
        "sum(len(r['command_map']) for r in results)==45":"sum(len(r['command_map']) for r in results)==39",
        '[174]':'[175]',
        'all33speech_and8_nonrelative_leaves_preserved':'all32speech_and7_nonrelative_leaves_preserved',
        'all4_source_relative_sites_and20_native_skip_cases_preserved':'source_has_no_relative_sites_or_native_skip_cases',
        'single_declared_tail_endword_exact':'both_declared_endwords_exact',
        '45structural commands/33speech/noFE/four relative sites/20 target cases,no pause,two A000s/one predicate/C200/one tail end':
            '39structural commands/32speech/23progressive/9FE,no relative sites,pause,A000 orpredicate,C200/two endwords',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        source_scope=dict(block=175,speeches=32,progressive=23,FE=9,commands=39,nonrelative_leaves=7,
            relative_sites=0,predicates=0,A000=0,C200=1,source_end_offsets=[1702,1706]),
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared reversible B175 relocation with both source ends and every command retained.')
