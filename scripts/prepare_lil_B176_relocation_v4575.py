"""Derive B176 relocation and final native stored-target checks without source-shape assumptions."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B176_relocation_tools_v4575')
assert not root.exists()
relocation=derive('scripts/research_lil_B175_relocation_v4521b.py','scripts/research_lil_B176_relocation_v4575.py',{
    'Relocate all32 B175 speeches;preserve23 progressive,nine FE,seven leaves,C200 and both ends.':
        'Relocate all10 B176 speeches;preserve9 progressive,one impersonal FE,leading A000,C200 and single end.',
    'lil_B175_relocation_v4521':'lil_B176_relocation_v4575',
    'lil_B175_editorial_manuscript_v3':'lil_B176_editorial_manuscript_v3',
    'all_routes_combined_v4496':'all_routes_combined_v4541',
    'number==175 and len(end_maps)==2':'number==176 and len(end_maps)==1',
    '[1702,1706] # both complete source endwords preserved':'[386] # the complete source tail endword is preserved',
    "for r in results)==32":"for r in results)==10",
    "sum(len(r['command_map']) for r in results)==39":"sum(len(r['command_map']) for r in results)==13",
    '[175]':'[176]',
    'all32speech_and7_nonrelative_leaves_preserved':'all10speech_and3_nonrelative_leaves_preserved',
    'source_FE_system_objects=9':'source_FE_system_objects=1',
    'both_declared_endwords_exact':'single_declared_tail_endword_exact',
    '39structural commands/32speech/23progressive/9FE,no relative sites,pause,A000 orpredicate,C200/two endwords':
        '13structural commands/10speech/9progressive/1impersonalFE,no relative sites,pause orpredicate,one opaque A000/C200/single endword',
})
stored=derive('scripts/prove_lil_B175_stored_v4522.py','scripts/prove_lil_B176_stored_v4576.py',{
    'Verify all32 final parity-preserving stored targets through their native consumers.':'Verify all10 final parity-preserving stored targets through their native consumers.',
    'lil_B175_stored_v4522':'lil_B176_stored_v4576',
    'lil_B175_editorial_manuscript_v3':'lil_B176_editorial_manuscript_v3',
    'lil_B175_relocation_v4521':'lil_B176_relocation_v4575',
    'lil_B175_fonts_v4517':'lil_B176_fonts_v4570',
    'stored[0] in [2,9,183,184,185,254]':'stored[0] in [174,175,254]',
    "expanded=stored[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')":"expanded=stored[1:]\n                assert not any(m in expanded for m in [b'FI',b'FA',b'FO'])",
    'len(cases)==32':'len(cases)==10','fresh+reused==128':'fresh+reused==40',
    "sum(c['consumer']=='FE-paper' for c in cases)==9":"sum(c['consumer']=='FE-paper' for c in cases)==1",
    'all32_final_stored_targets128_macro_cases_and_complete_planes':'all10_final_stored_targets40_macro_cases_and_complete_planes',
    'current_final_stored_macro_alignment_cases=128':'current_final_stored_macro_alignment_cases=40',
    'all32_final_targets_complete_native_planes_equal_reviewed_planes':'all10_final_targets_complete_native_planes_equal_reviewed_planes',
    'actual_selected_B175_scenes_presentations_resource_C200_bodies_and_two_end_reachability_unexecuted':
        'actual_selected_B176_scene_A000_C200_bodies_and_single_end_reachability_unexecuted',
    'stored_targets=32,progressive=23,FE=9,macro_cases=128':'stored_targets=10,progressive=9,FE=1,macro_cases=40',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(relocation=relocation,stored=stored,
    source_scope=dict(block=176,speeches=10,progressive=9,FE=1,commands=13,nonrelative_leaves=3,
        relative_sites=0,predicates=0,A000=1,C200=1,source_end_offsets=[386]),
    opaque_A000_packed_operand_semantics_not_inferred=True,no_ROM_registry_ledger_orcredit_change=True,
    full_goal_complete=False))
