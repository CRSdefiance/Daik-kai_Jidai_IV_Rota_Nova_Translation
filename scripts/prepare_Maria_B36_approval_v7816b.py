"""Preserve the code-generation quote failure; freeze review/seal successors safely."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_B36_approval_repair_tools_v7816b');assert not root.exists()
    a=derive('scripts/Maria_B36_final_paths_v7816.py','scripts/Maria_B36_final_paths_v7816b.py',{
        'maria_B36_native_approval_v7816':'maria_B36_native_approval_v7816b',
        'maria_B36_reference_approval_v7817':'maria_B36_reference_approval_v7817b',
    })
    b=derive('scripts/prepare_Maria_B36_approval_v7816.py','scripts/prepare_Maria_B36_approval_fixed_v7816b.py',{
        "keeps He's a great merchant! together":"keeps the short closing praise together",
        "        'actual65_eachlanguage_no_unplayed_speeches':'actual16_eachlanguage_no_unplayed_speeches',\n":"",
        'maria_B36_approval_tools_v7816':'maria_B36_approval_tools_v7816b',
        'approve_Maria_B36_native_v7816.py':'approve_Maria_B36_native_v7816b.py',
        'seal_Maria_B36_references_v7817.py':'seal_Maria_B36_references_v7817b.py',
        "'Maria_B36_final_paths_v7816'":"'Maria_B36_final_paths_v7816b'",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=[a,b],
        original_code_generation_quote_failure_preserved_before_any_approval_orROM_ledger_write=True,
        metadata_quote_safe_wording_andabsent_derivation_key_corrected=True,
        all_original_native_high_constants_review_gates_source_prose_andinverse_guards_preserved=True,
        no_text_pixel_macro_orQA_output_change=True,new_credit=0,full_goal_complete=False))
