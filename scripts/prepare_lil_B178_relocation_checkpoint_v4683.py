"""Derive the independent inverse/checkpoint and a separate full-history audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_relocation_checkpoint_tools_v4683');assert not ROOT.exists()
tools=[derive('scripts/checkpoint_lil_B177_relocation_v4627.py','scripts/checkpoint_lil_B178_relocation_v4683.py',{
    'lil_B177_relocation_checkpoint_text_v4627':'lil_B178_relocation_checkpoint_text_v4683',
    'lil_B177_relocation_checkpoint_v4627':'lil_B178_relocation_checkpoint_v4683',
    'editorial_handoff_verification_v4628':'editorial_handoff_verification_v4684',
    'lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
    'lil_B177_relocation_v4625':'lil_B178_relocation_v4681',
    'lil_B177_stored_v4626/all10_final_stored_targets40':'lil_B178_stored_v4682/all13_final_stored_targets52',
    'editorial_handoff_verification_v4624':'editorial_handoff_verification_v4680',
    '(40,24,16)':'(52,28,24)',"len(stored['final_target_parity_cases'])==10":"len(stored['final_target_parity_cases'])==13",
    "b['block']==177":"b['block']==178",'[177]':'[178]',
    '(488,472,486,470)':'(496,456,494,456)',
    "len(commands)==13 and len(speeches)==10 and len(b['command_map'])==13":
        "len(commands)==16 and len(speeches)==13 and len(b['command_map'])==16",
    '==[(482,466)]':'==[(490,452)]','all_routes_combined_v4595':'all_routes_combined_v4655',
    'lil_B177_reversible_relocation_v4627':'lil_B178_reversible_relocation_v4683',
    '## V4627: B177':'## V4683: B178','# Current editorial handoff - V4627':'# Current editorial handoff - V4683',
    "checkpoint='V4627'":"checkpoint='V4683'",
    'fresh_reread=5885,integrated=5875,pending=10':'fresh_reread=5898,integrated=5885,pending=13',
    'source_prose=5888,revised=3733,retained=2142':'source_prose=5901,revised=3738,retained=2147',
    'stored_alignment_cases=40,fresh_stored_cases=24,exact_reused_stored_cases=16':
        'stored_alignment_cases=52,fresh_stored_cases=28,exact_reused_stored_cases=24',
    'source_ends_mapped=[[482,466]]':'source_ends_mapped=[[490,452]]',
    'remaining_B178_B180_physical_speeches=38':'remaining_B179_B180_physical_speeches=25',
    'V4627 independently inverted/audited/applied:488 to472 bytes,13 commands,single end,40 stored cases. Counts and main V4541 unchanged.':
        'V4683 independently inverted/audited/applied:496 to456 bytes,16 commands,single end,52 stored cases. Counts and main V4595 unchanged.',
})]
tools.append(derive('scripts/verify_editorial_handoff_v4628b.py','scripts/verify_editorial_handoff_v4684.py',{
    'editorial_handoff_verification_v4628':'editorial_handoff_verification_v4684',
    'lil_B177_relocation_checkpoint_v4627':'lil_B178_relocation_checkpoint_v4683',
    'lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
    'lil_B177_relocation_v4625':'lil_B178_relocation_v4681',
    'lil_B177_stored_v4626/all10_final_stored_targets40':'lil_B178_stored_v4682/all13_final_stored_targets52',
    'lil_B177_reversible_relocation_v4627':'lil_B178_reversible_relocation_v4683',
    '(5875,5888,3733,2142)':'(5885,5901,3738,2147)','(5885,5875,10)':'(5898,5885,13)',
    "fresh['record_keys']})==5885":"fresh['record_keys']})==5898",
    "['/data/SC2.DK4']==4032":"['/data/SC2.DK4']==4045",
    'unfinished_editorial_scope_v4623':'unfinished_editorial_scope_v4679',
    "scope['remaining_B178_B180_physical_speeches']==38":"scope['remaining_B179_B180_physical_speeches']==25",
    "scope['incomplete_route_source_prose']==10":"scope['incomplete_route_source_prose']==13",
    "len(rows)==10 and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':5}":
        "len(rows)==13 and Counter(r['editorial_decision'] for r in rows)=={'revise':2,'retain-wording':11}",
    "len(font['cases'])==10 and font['current_original_macro_alignment_calls']==80":
        "len(font['cases'])==13 and font['current_original_macro_alignment_calls']==104",
    "(font['progressive_planes'],font['FE_planes'])==(9,1)":"(font['progressive_planes'],font['FE_planes'])==(12,1)",
    "source_macro_preservation_negatives'])==49":"source_macro_preservation_negatives'])==51",
    '(40,24,16)':'(52,28,24)',"b['block']==177":"b['block']==178",'[177]':'[178]',
    '(488,472,486,470)':'(496,456,494,456)',"len(b['command_map'])==13 and len(b['text_records'])==10":
        "len(b['command_map'])==16 and len(b['text_records'])==13",
    '[(0xA000,8,8),(0xC200,480,464),(0,482,466)]':'[(0xA000,8,8),(0xC200,488,450),(0,490,452)]',
    '00a0ffff01090fa1':'00a0ffff010002a1','source[480:486]==target[464:470]':'source[488:494]==target[450:456]',
    "struct.pack_into('<H',restored,4,478)":"struct.pack_into('<H',restored,4,486)",
    '==source[:486]':'==source[:494]',
    "main['profile']=='all-routes-unified-v4541'":"main['profile']=='all-routes-unified-v4595'",
    "ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4595'":"ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4655'",
    'all10_source_current_stored_references_and5_retentions_verified':'all13_source_current_stored_references_and11_retentions_verified',
    'all49_negatives80_logical_compiled_and40_stored_cases_bound':'all51_negatives104_logical_compiled_and52_stored_cases_bound',
    'current B177':'current B178',
    'V4627 independently verified:5885 reread/5875 completed/10 pending;all source/current/stored references,40 stored cases,inverse and full history exact. Main V4541 preserved.':
        'V4683 independently verified:5898 reread/5885 completed/13 pending;all source/current/stored references,52 stored cases,inverse and full history exact. Main V4595 preserved.',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source496_logical494_target456_logical456=True,
    C200488_target450_end490_target452=True,stored52_fresh28_reused24=True,
    console_only_macro_case_count_erratum40_authoritative_JSON52_retained=True,
    no_ROM_registry_ledger_orcredit_change_yet=True,full_goal_complete=False))
