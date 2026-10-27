"""Derive complete B167 relocation and stored-byte proofs; preserve both separated ends."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_relocation_tools_v4138')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B166_relocation_v4093.py','scripts/research_lil_B167_relocation_v4139.py',{
        'Relocate B166 complete speeches and advice labels; preserve eight spans and one tail end.':'Relocate B167 complete speeches and labels; preserve twelve spans and both separated ends.',
        'lil_B166_relocation_v4093':'lil_B167_relocation_v4139',
        'lil_B166_editorial_manuscript_v5':'lil_B167_editorial_manuscript_v12',
        'lil_B166_choice_manuscript_v2':'lil_B167_choice_manuscript_v2',
        'all_routes_combined_v4046':'all_routes_combined_v4110',
        'assert number==166 and len(end_maps)==1':'assert number==167 and len(end_maps)==2',
        "assert end_maps[0]['source_offset']==2948 # both advice paths rejoin before the sole A000/end":"assert [e['source_offset'] for e in end_maps]==[430,2172] # refusal and lecture have distinct ends",
        "for r in results)==42":"for r in results)==27", "for r in results)==8":"for r in results)==12",
        "for r in results)==40":"for r in results)==60", "for r in results)==62":"for r in results)==46",
        '[166]':'[167]',
        'one_original2100_object_two_source_ordered_advice_labels':'one_original2100_object_two_source_ordered_accept_refuse_labels',
        'all42speech_and8_relative_operands':'all27speech_and12_relative_operands',
        'all40_relocated_native_skip_cases':'all60_relocated_native_skip_cases',
        'one_declared_tail_end_after_advice_rejoin_exact':'two_separated_declared_refusal_and_lecture_endwords_exact',
        '62commands/42speech/one2100/8spans/40targetskipcases,one tail end':'46commands/27speech/one2100/12spans/60targetskipcases,two distinct ends'
    })]
    tools.append(derive('scripts/prove_lil_B166_stored_v4094.py','scripts/prove_lil_B167_stored_v4140.py',{
        'all42':'all27','lil_B166_stored_v4094':'lil_B167_stored_v4140',
        'lil_B166_editorial_manuscript_v5':'lil_B167_editorial_manuscript_v12',
        'lil_B166_relocation_v4093':'lil_B167_relocation_v4139',
        'lil_B166_voices_v4056':'lil_B167_voices_v4120','[2,9,20,23]':'[2,4,13,23,109]',
        'len(cases)==42':'len(cases)==27','fresh+reused==168':'fresh+reused==108',
        'final_stored_targets168':'final_stored_targets108',
        'current_final_stored_macro_alignment_cases=168':'current_final_stored_macro_alignment_cases=108',
        'stored_targets=42,progressive=42':'stored_targets=27,progressive=27','macro_cases=168':'macro_cases=108'
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=167,speeches=27,choice_labels=2,commands=46,relative_sites=12,target_skip_cases=60,stored_macro_cases=108,separated_end_offsets=[430,2172],membership_queries=2,resource_words=[0x6327,0x632B],A000=0,macros=0,static_actors=[2,4,13,23,109]),no_ROM_registry_ledger_orcredit_change=True))
    print('B167 complete relocation and stored proof successors created.')
