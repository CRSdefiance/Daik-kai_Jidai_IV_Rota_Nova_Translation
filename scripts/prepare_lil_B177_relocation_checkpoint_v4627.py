"""Derive independent B177 inverse/history checks and the next unresolved gates."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B177_relocation_checkpoint_tools_v4627')
assert not root.exists()
tool=derive('scripts/checkpoint_lil_B176_relocation_v4577.py','scripts/checkpoint_lil_B177_relocation_v4627.py',{
    'B176':'B177','lil_B176':'lil_B177',
    'relocation_checkpoint_text_v4577':'relocation_checkpoint_text_v4627',
    'relocation_checkpoint_v4577':'relocation_checkpoint_v4627',
    'editorial_handoff_verification_v4578':'editorial_handoff_verification_v4628',
    'editorial_manuscript_v3':'editorial_manuscript_v5','relocation_v4575':'relocation_v4625',
    'stored_v4576':'stored_v4626','editorial_handoff_verification_v4574c':'editorial_handoff_verification_v4624',
    '==(40,16,24)':'==(40,24,16)',"b['block']==176":"b['block']==177",'blocks[176]':'blocks[177]',
    '==(392,404,390,404)':'==(488,472,486,470)','==[(386,400)]':'==[(482,466)]',
    '==[176]':'==[177]','all_routes_combined_v4541':'all_routes_combined_v4595',
    'lil_B176_reversible_relocation_v4577':'lil_B177_reversible_relocation_v4627',
    '## V4577: B176':'## V4627: B177','# Current editorial handoff - V4577':'# Current editorial handoff - V4627',
    "checkpoint='V4577'":"checkpoint='V4627'",'fresh_reread=5875,integrated=5865,pending=10':'fresh_reread=5885,integrated=5875,pending=10',
    'source_prose=5878,revised=3728,retained=2137,stored_alignment_cases=40,fresh_stored_cases=16,exact_reused_stored_cases=24':
        'source_prose=5888,revised=3733,retained=2142,stored_alignment_cases=40,fresh_stored_cases=24,exact_reused_stored_cases=16',
    'source_ends_mapped=[[386,400]]':'source_ends_mapped=[[482,466]]',
    'remaining_B177_B180_physical_speeches=48':'remaining_B178_B180_physical_speeches=38',
    'V4577 independently inverted/audited/applied:392 to404 bytes':'V4627 independently inverted/audited/applied:488 to472 bytes',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,no_new_review_orcompletion_credit=True,full_goal_complete=False))
