"""Reuse the observed original backing geometry with exact unchanged ARM9;prove new labels."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_choice_tools_v4133')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/prove_lil_B166_choices_v4080.py','scripts/prove_lil_B167_choices_v4133.py',{
        'lil_B166_choices_v4080':'lil_B167_choices_v4133',
        'lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice':'lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice',
        'lil_B166_choice_manuscript_v1':'lil_B167_choice_manuscript_v1','[(166,2152)]':'[(167,152)]',
        "    arm = image.read_file('/__arm9__.bin')":"    arm = image.read_file('/__arm9__.bin')\n    assert sha(arm)=='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa' # exact runtime of the observed B166 backing constructor",
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,earlier_B166_actual_backing_ownership_reused_by_exact_whole_ARM9=True,
        B167_menu_glyphs_pointers_geometry_and_return_indices_to_be_freshly_proven=True,
        no_new_actual_B167_scene_or_menu_selection_claim=True,no_ROM_registry_ledger_credit_change=True))
    print('B167 typed-menu proof created;observed backing reused by exact unchanged native code,new labels tested separately.')
