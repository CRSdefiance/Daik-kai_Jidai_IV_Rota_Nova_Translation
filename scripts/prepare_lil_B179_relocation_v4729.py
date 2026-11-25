"""Prepare B179 relocation and all56 stored alignment cases without a C200 leaf."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_relocation_tools_v4729')
assert not ROOT.exists()
tools=[derive('scripts/research_lil_B178_relocation_v4681.py','scripts/research_lil_B179_relocation_v4729.py',{
    'lil_B178_relocation_v4681':'lil_B179_relocation_v4729',
    'lil_B178_editorial_manuscript_v3':'lil_B179_editorial_manuscript_v3',
    'all_routes_combined_v4655':'all_routes_combined_v4701',
    'number==178':'number==179','[178]':'[179]',
    '[490] # the complete source tail endword is preserved':'[508] # the complete source tail endword is preserved',
    "for r in results)==13":"for r in results)==14",
    'all13speech_and3_nonrelative_leaves_preserved':'all14speech_and2_nonrelative_leaves_preserved',
    'Relocate all13 B178 speeches;preserve12 progressive,one impersonal FE,leading A000,C200 and single end.':
        'Relocate all14 B179 speeches;preserve13 progressive,one impersonal FE,leading A000 and single end; no C200.',
    '16structural commands/13speech/12progressive/1impersonalFE,no relative sites,pause orpredicate,one opaque A000/C200/single endword,inversebytes and335otherblocks exact. Researchonly.':
        '16structural commands/14speech/13progressive/1impersonalFE,no relative sites,pause orpredicate,one opaque A000/single endword,no C200,inversebytes and335otherblocks exact. Researchonly.',
    "assert sha(source)==spec['current_block_sha256']":
        "assert sha(source)==spec['current_block_sha256']\n        assert len(source)==old_end==512\n        assert len(spec['all_current_native_commands'])==16\n        assert sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==14\n        assert [c['word'] for c in spec['all_current_native_commands'] if c['word']!=0x4000]==[0xA000,0]",
    'single_declared_tail_endword_exact=True,':'single_declared_tail_endword_exact=True,no_source_C200_commands=True,',
})]
tools.append(derive('scripts/prove_lil_B178_stored_v4682.py','scripts/prove_lil_B179_stored_v4730.py',{
    'lil_B178_stored_v4682':'lil_B179_stored_v4730',
    'lil_B178_editorial_manuscript_v3':'lil_B179_editorial_manuscript_v3',
    'lil_B178_relocation_v4681':'lil_B179_relocation_v4729',
    'lil_B178_fonts_v4677':'lil_B179_fonts_v4724',
    'in [166,167,168,254]':'in [92,96,152,254]',
    'len(cases)==13':'len(cases)==14','fresh+reused==52':'fresh+reused==56',
    'all13_final_stored_targets52_macro_cases':'all14_final_stored_targets56_macro_cases',
    'current_final_stored_macro_alignment_cases=52':'current_final_stored_macro_alignment_cases=56',
    'all13_final_targets':'all14_final_targets',
    'actual_selected_B178_scene_A000_C200_bodies_and_single_end_reachability_unexecuted':
        'actual_selected_B179_scene_A000_body_and_single_end_reachability_unexecuted',
    'stored_targets=13,progressive=12':'stored_targets=14,progressive=13',
    'macro_cases=40':'macro_cases=56','Verify all13':'Verify all14',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_block=179,speeches=14,progressive=13,FE=1,commands=16,
    opaque_A0008_single_end508=True,no_C200=True,no_source_relative_predicate_or_typed_object=True,
    all_reviewed_English_unchanged=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
