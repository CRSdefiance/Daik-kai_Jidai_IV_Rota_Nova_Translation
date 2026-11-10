"""Prepare source-bound B179 inverse checkpoint and independent handoff audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_relocation_checkpoint_tools_v4731')
assert not ROOT.exists()
shared={
    'lil_B178_relocation_checkpoint_text_v4683':'lil_B179_relocation_checkpoint_text_v4731',
    'lil_B178_relocation_checkpoint_v4683':'lil_B179_relocation_checkpoint_v4731',
    'editorial_handoff_verification_v4684':'editorial_handoff_verification_v4732',
    'lil_B178_editorial_manuscript_v3':'lil_B179_editorial_manuscript_v3',
    'lil_B178_relocation_v4681':'lil_B179_relocation_v4729',
    'lil_B178_stored_v4682/all13_final_stored_targets52_macro_cases':'lil_B179_stored_v4730/all14_final_stored_targets56_macro_cases',
    'lil_B178_reversible_relocation_v4683':'lil_B179_reversible_relocation_v4731',
    "b['block']==178":"b['block']==179",'blocks[178]':'blocks[179]',
    '==[178]':'==[179]',
    '==(52,28,24)':'==(56,20,36)',
    '==(496,456,494,456)':'==(512,496,512,496)',
    'len(speeches)==13':'len(speeches)==14',
    "len(stored['final_target_parity_cases'])==13":"len(stored['final_target_parity_cases'])==14",
    'fresh_reread=5898,integrated=5885,pending=13':'fresh_reread=5912,integrated=5898,pending=14',
    'source_prose=5901,revised=3738,retained=2147':'source_prose=5915,revised=3740,retained=2158',
    'all13':'all14',
    'V4683':'V4731',
}
tools=[derive('scripts/checkpoint_lil_B178_relocation_v4683.py','scripts/checkpoint_lil_B179_relocation_v4731.py',{
    **shared,
    'editorial_handoff_verification_v4680':'editorial_handoff_verification_v4728',
    'all_routes_combined_v4655':'all_routes_combined_v4701',
    '==(52,28,24)':'==(56,20,36)',
    '[(490,452)]':'[(508,492)]',
    '[0xA000,0xC200,0]':'[0xA000,0]',
    'stored_alignment_cases=52,fresh_stored_cases=28,exact_reused_stored_cases=24':
        'stored_alignment_cases=56,fresh_stored_cases=20,exact_reused_stored_cases=36',
    'source_ends_mapped=[[490,452]]':'source_ends_mapped=[[508,492]]',
    'remaining_B179_B180_physical_speeches=25':'remaining_B180_physical_speeches=11',
    'Independently invert B177 relocation':'Independently invert B179 relocation',
    'B178 reversible relocation':'B179 reversible relocation',
    '496 to456 bytes,16 commands,single end,52 stored cases. Counts and main V4595 unchanged.':
        '512 to496 bytes,16 commands,single end,no C200,56 stored cases. Counts and main V4701 unchanged.',
})]
tools.append(derive('scripts/verify_editorial_handoff_v4684.py','scripts/verify_editorial_handoff_v4732.py',{
    **{k:v for k,v in shared.items() if k not in ['lil_B178_relocation_checkpoint_text_v4683','len(speeches)==13',
        "len(stored['final_target_parity_cases'])==13",'fresh_reread=5898,integrated=5885,pending=13',
        'source_prose=5901,revised=3738,retained=2147']},
    '==(5885,5901,3738,2147)':'==(5898,5915,3740,2158)',
    '==(5898,5885,13)':'==(5912,5898,14)',
    "len(font['cases'])==13 and font['current_original_macro_alignment_calls']==104":
        "len(font['cases'])==14 and font['current_original_macro_alignment_calls']==112",
    "(font['progressive_planes'],font['FE_planes'])==(12,1)":"(font['progressive_planes'],font['FE_planes'])==(13,1)",
    "len(b['text_records'])==13":"len(b['text_records'])==14",
    '[(0xA000,8,8),(0xC200,488,450),(0,490,452)]':'[(0xA000,8,8),(0,508,492)]',
    '00a0ffff010002a1':'00a0ffff01221da1',
    "source[488:494]==target[450:456]==bytes.fromhex('00c200000000')":
        "source[508:512]==target[492:496]==bytes(4)",
    "struct.pack_into('<H',restored,4,486)":"struct.pack_into('<H',restored,4,504)",
    'source[:494]':'source[:512]',
    'all-routes-unified-v4595':'all-routes-unified-v4701',
    'all-routes-unified-v4655':'all-routes-unified-v4701',
    'and11_retentions_verified':'and6_retentions_verified',
    'all51_negatives104_logical_compiled_and52_stored_cases_bound':'all51_negatives112_logical_compiled_and56_stored_cases_bound',
    'source_A000_C200_single_end_byte_exact_and_uninterpreted':'source_A000_single_end_no_C200_byte_exact_and_uninterpreted',
    'current B178':'current B179',
    '5898 reread/5885 completed/13 pending':'5912 reread/5898 completed/14 pending',
    '52 stored cases,inverse and full history exact. Main V4595 preserved.':'56 stored cases,inverse and full history exact. Main V4701 preserved.',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_A0008_and_end508_target492_no_C200=True,
    stored_cases56_fresh20_reused36=True,complete_prior_ledger_and_all_counts_preserved=True,full_goal_complete=False))
