"""Prepare final-stored parity-tail checks without redoing exact compiled inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_stored_tools_v6995')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/prove_lil_B220_stored_v6941.py','scripts/prove_lil_B221_stored_v6995.py',{
        'B220':'B221','stored_v6941':'stored_v6995',
        'relocation_v6940/all17_objects20_commands_full1280_inverse_RESEARCH':
        'relocation_v6994/all16_objects21_commands_four_relatives_full1208_inverse_RESEARCH',
        'native_pages_v6928b/all17_paragraphs17_complete_native_pages136_alignments':
        'native_pages_v6980c/all14_paragraphs16_complete_native_pages112_alignments',
        'current_V6910_native_v6920':'current_V6956_native_v6966',
        "assert len(rendered['pages'])==1":"assert len(rendered['pages'])==len(base['pages'])",
        "path=ROOT/(ref['id']+'_stored_page.bin')":"path=ROOT/(ref['id']+f'_stored_page{page[\"page\"]}.bin')",
        'len(records)==17 and fresh+reused==68':'len(records)==14 and fresh+reused==56',
        'all17_final_stored_targets68_alignments17_complete_pages':'all14_final_stored_targets56_alignments16_complete_pages',
        'stored_alignment_cases=68':'stored_alignment_cases=56','complete_native_pages=17':'complete_native_pages=16',
        'final_stored_targets=17,alignments=68':'final_stored_targets=14,alignments=56',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_stored_native_successor.json',dict(derivation=row,
        all_fourteen_exact_paragraphs_and_two_scoped_native_continuations_preserved=True,
        page_specific_plane_paths_prevent_overwriting_two_page_evidence=True,
        only_changed_parity_tail_inputs_require_fresh_native_execution=True,
        no_new_ROM_or_credit=True,full_goal_complete=False))
