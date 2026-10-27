"""Prepare complete B178 relocation and native checks for all final stored targets."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_relocation_tools_v4681');assert not ROOT.exists()
tools=[derive('scripts/research_lil_B177_relocation_v4625.py','scripts/research_lil_B178_relocation_v4681.py',{
    'lil_B177_relocation_v4625':'lil_B178_relocation_v4681','lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
    'all_routes_combined_v4595':'all_routes_combined_v4655','number==177':'number==178','[177]':'[178]',
    '[482] # the complete source tail endword is preserved':'[490] # the complete source tail endword is preserved',
    "for r in results)==10":"for r in results)==13","for r in results)==13":"for r in results)==16",
    'all10speech_and3':'all13speech_and3','all10 B177 speeches;preserve9 progressive':'all13 B178 speeches;preserve12 progressive',
    '13structural commands/10speech/9progressive':'16structural commands/13speech/12progressive',
})]
tools.append(derive('scripts/prove_lil_B177_stored_v4626.py','scripts/prove_lil_B178_stored_v4682.py',{
    'lil_B177_stored_v4626':'lil_B178_stored_v4682','lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
    'lil_B177_relocation_v4625':'lil_B178_relocation_v4681','lil_B177_fonts_v4621':'lil_B178_fonts_v4677',
    'in [174,175,254]':'in [166,167,168,254]','len(cases)==10':'len(cases)==13','fresh+reused==40':'fresh+reused==52',
    'all10_final_stored_targets40_macro_cases':'all13_final_stored_targets52_macro_cases',
    'current_final_stored_macro_alignment_cases=40':'current_final_stored_macro_alignment_cases=52',
    'all10_final_targets':'all13_final_targets','actual_selected_B177':'actual_selected_B178',
    'stored_targets=10,progressive=9':'stored_targets=13,progressive=12','Verify all10':'Verify all13',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_block=178,speeches=13,progressive=12,FE=1,commands=16,
    opaque_A0008_C200488_single_end490=True,no_source_relative_predicate_or_typed_object=True,
    all_reviewed_English_unchanged=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
