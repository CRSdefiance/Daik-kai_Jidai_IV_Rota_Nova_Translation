"""Derive an independent inverse and preservation audit before checkpoint writes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B176_relocation_checkpoint_tools_v4577')
assert not root.exists()
source=Path('scripts/checkpoint_lil_B175_relocation_v4523.py')
text=source.read_text(encoding='utf-8')
start=text.index('    next_text=(')
end=text.index('    stable=',start)
old_narrative=text[start:end]
tool=derive(source,'scripts/checkpoint_lil_B176_relocation_v4577.py',{
    'Independently invert B175 relocation and checkpoint the next unresolved gates.':'Independently invert B176 relocation and checkpoint the next unresolved gates.',
    'from scripts.lil_B175_checkpoint_text_v4519 import NEXT as PREVIOUS_NEXT':
        'from scripts.lil_B176_relocation_checkpoint_text_v4577 import NEXT,SUMMARY',
    'lil_B175_relocation_checkpoint_v4523':'lil_B176_relocation_checkpoint_v4577',
    'editorial_handoff_verification_v4524':'editorial_handoff_verification_v4578',
    'lil_B175_editorial_manuscript_v3':'lil_B176_editorial_manuscript_v3',
    'lil_B175_relocation_v4521':'lil_B176_relocation_v4575',
    'lil_B175_stored_v4522':'lil_B176_stored_v4576',
    'all32_final_stored_targets128_macro_cases_and_complete_planes':'all10_final_stored_targets40_macro_cases_and_complete_planes',
    'editorial_handoff_verification_v4520':'editorial_handoff_verification_v4574c',
    '==(128,68,60)':'==(40,16,24)',
    "len(stored['final_target_parity_cases'])==32":"len(stored['final_target_parity_cases'])==10",
    "b['block']==175":"b['block']==176",'.blocks[175]':'.blocks[176]',
    'container.blocks[175]':'container.blocks[176]',
    '==(1712,1700,1710,1698)':'==(392,404,390,404)',
    "len(commands)==39 and len(speeches)==32 and len(b['command_map'])==39":"len(commands)==13 and len(speeches)==10 and len(b['command_map'])==13",
    '==[(1702,1690),(1706,1694)]':'==[(386,400)]',
    '==[0x6000,0x6344,0x4696,0x4635,0xC200,0,0]':'==[0xA000,0xC200,0]',
    '==[175]':'==[176]','target_blocks[175]':'target_blocks[176]',
    old_narrative:'    next_text,summary=NEXT,SUMMARY\n',
    'all_routes_combined_v4496':'all_routes_combined_v4541',
    'lil_B175_reversible_relocation_v4523':'lil_B176_reversible_relocation_v4577',
    '## V4523: B175 reversible relocation and stored native tests complete':'## V4577: B176 reversible relocation and stored native tests complete',
    '# Current editorial handoff - V4523':'# Current editorial handoff - V4577',
    "checkpoint='V4523'":"checkpoint='V4577'",
    'fresh_reread=5865,integrated=5833,pending=32':'fresh_reread=5875,integrated=5865,pending=10',
    'source_prose=5868,revised=3709,retained=2124,stored_alignment_cases=128,fresh_stored_cases=68,exact_reused_stored_cases=60':
        'source_prose=5878,revised=3728,retained=2137,stored_alignment_cases=40,fresh_stored_cases=16,exact_reused_stored_cases=24',
    'source_ends_mapped=[[1702,1690],[1706,1694]]':'source_ends_mapped=[[386,400]]',
    'remaining_B176_B180_physical_speeches=58':'remaining_B177_B180_physical_speeches=48',
    "print('V4523 independently inverted/audited/applied:1712 to1700 bytes,39 commands,both ends,128 stored cases. Counts and main V4496 unchanged.')":
        "print('V4577 independently inverted/audited/applied:392 to404 bytes,13 commands,single end,40 stored cases. Counts and main V4541 unchanged.')",
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,no_new_review_orcompletion_credit=True,full_goal_complete=False))
