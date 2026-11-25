"""Prepare complete B170 relocation with no relative sites,one pause andtwo ends."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_relocation_tools_v4281')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B169_relocation_v4233.py','scripts/research_lil_B170_relocation_v4281.py',{
        'Relocate all36 B169 speeches; preserve twelve spans, five leaves and the single tail end.':'Relocate all33 B170 speeches;preserve twelve leaves,one pause,C200 and both consecutive ends.',
        'lil_B169_relocation_v4233':'lil_B170_relocation_v4281',
        'lil_B169_editorial_manuscript_v4':'lil_B170_editorial_manuscript_v5',
        'all_routes_combined_v4204':'all_routes_combined_v4251',
        'assert number==169 and len(end_maps)==1':'assert number==170 and len(end_maps)==2',
        "assert [e['source_offset'] for e in end_maps]==[2558] # single complete source tail end":"assert [e['source_offset'] for e in end_maps]==[1852,1856] # both consecutive source ends preserved",
        'for r in results)==36':'for r in results)==33',
        "sum(len(r['relative_skip_fixups']) for r in results)==12":"sum(len(r['relative_skip_fixups']) for r in results)==0",
        "sum(len(r['target_native_skip_cases']) for r in results)==60":"sum(len(r['target_native_skip_cases']) for r in results)==0",
        'for r in results)==53':'for r in results)==45',
        "sum(len(r['original2000_pause_and_resume_maps']) for r in results)==0":"sum(len(r['original2000_pause_and_resume_maps']) for r in results)==1",
        '[169]':'[170]',
        'all36speech_and12_relative_operands_preserved':'all33speech_and12_nonrelative_leaves_preserved',
        'all60_relocated_native_skip_cases_match_original_target_mapping':'no_source_relative_sites_or_native_skip_cases',
        'no_source2000_commands':'one_original2000_pause_and_resume_preserved',
        'single_declared_tail_endword_exact':'two_consecutive_declared_endwords_exact',
        '53commands/36speech/noFE/12spans/60targetskipcases,one tail end':'45commands/33speech/noFE/no_relative_sites,one pause andtwo consecutive ends',
    })]
    tools.append(derive('scripts/prove_lil_B169_stored_v4234.py','scripts/prove_lil_B170_stored_v4282.py',{
        'all36':'all33','lil_B169_stored_v4234':'lil_B170_stored_v4282',
        'lil_B169_editorial_manuscript_v4':'lil_B170_editorial_manuscript_v5',
        'lil_B169_relocation_v4233':'lil_B170_relocation_v4281',
        'lil_B169_voices_v4213':'lil_B170_voices_v4262',
        '[2,6,9,20,21,76]':'[2,25]','len(cases)==36':'len(cases)==33',
        'fresh+reused==144':'fresh+reused==132','stored_targets144':'stored_targets132',
        'current_final_stored_macro_alignment_cases=144':'current_final_stored_macro_alignment_cases=132',
        'stored_targets=36,progressive=36,FE=0':'stored_targets=33,progressive=33,FE=0',
        'macro_cases=144':'macro_cases=132',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=170,speeches=33,commands=45,
        nonrelative_leaves=12,relative_sites=0,predicates=0,pause_offset=36,pause_resume=38,
        source_end_offsets=[1852,1856],A000=1,A000_hex='00a0ffff19100120',C200=1,resources=2,
        final_stored_alignment_cases=132),no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('B170 relocation and132-case stored proof producers prepared;both ends,pause andC200 source-owned.')
