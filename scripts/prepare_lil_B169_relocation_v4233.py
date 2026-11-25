"""Derive source-bound relocation/stored proofs for36 progressive B169 speeches."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_relocation_tools_v4233')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/research_lil_B168_relocation_v4190.py','scripts/research_lil_B169_relocation_v4233.py',{
        'Relocate all54 B168 speeches; preserve twelve spans, all effects and both consecutive ends.':'Relocate all36 B169 speeches; preserve twelve spans, five leaves and the single tail end.',
        'lil_B168_relocation_v4190':'lil_B169_relocation_v4233',
        'lil_B168_editorial_manuscript_v7':'lil_B169_editorial_manuscript_v4',
        'all_routes_combined_v4160':'all_routes_combined_v4204',
        'assert number==168 and len(end_maps)==2':'assert number==169 and len(end_maps)==1',
        "assert [e['source_offset'] for e in end_maps]==[2906,2910] # both predecessor end words remain consecutive":"assert [e['source_offset'] for e in end_maps]==[2558] # single complete source tail end",
        'for r in results)==54':'for r in results)==36',
        'for r in results)==82':'for r in results)==53',
        '[168]':'[169]',
        'all54speech_and12_relative_operands':'all36speech_and12_relative_operands',
        'source_FE_system_objects=3':'source_FE_system_objects=0',
        'two_consecutive_declared_endwords_exact':'single_declared_tail_endword_exact',
        '82commands/54speech/threeFE/12spans/60targetskipcases,two consecutive ends':'53commands/36speech/noFE/12spans/60targetskipcases,one tail end',
    })]
    tools.append(derive('scripts/prove_lil_B168_stored_v4191.py','scripts/prove_lil_B169_stored_v4234.py',{
        'all54':'all36','lil_B168_stored_v4191':'lil_B169_stored_v4234',
        'lil_B168_editorial_manuscript_v7':'lil_B169_editorial_manuscript_v4',
        'lil_B168_relocation_v4190':'lil_B169_relocation_v4233',
        'lil_B168_voices_v4170':'lil_B169_voices_v4213',
        '[2,6,9,20,76,87,165,166,254]':'[2,6,9,20,21,76]',
        'len(cases)==54':'len(cases)==36','fresh+reused==216':'fresh+reused==144',
        'stored_targets216':'stored_targets144',
        'current_final_stored_macro_alignment_cases=216':'current_final_stored_macro_alignment_cases=144',
        'stored_targets=54,progressive=51,FE=3':'stored_targets=36,progressive=36,FE=0',
        'macro_cases=216':'macro_cases=144',
        'all_resource_bodies_and_actual_selected_scenes_unexecuted':'actual_selected_scenes_and_later_A000_body_unexecuted',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,no_ROM_registry_ledger_orcredit_change=True,
        source_scope=dict(block=169,speeches=36,progressive=36,FE=0,commands=53,relative_sites=12,
                          target_skip_cases=60,stored_macro_cases=144,clean_and_current_end_offsets=[2558],
                          predicates=3,A000=1,numeric_A000_operands=[29,1],resources=0,presentations=0,FI=5,FA=0,FO=2)))
    print('B169 complete-object relocation and144 stored target alignment cases prepared; no release approval.')
