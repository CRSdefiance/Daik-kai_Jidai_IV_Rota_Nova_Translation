"""Prepare complete native logical macro checks for all224 reviewed paragraphs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B61_B70_logical_preparation_v8891')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/prove_Hodram_B54_B60_logical_v8801.py','scripts/prove_Hodram_B61_B70_logical_v8891.py',{
        'scripts.Hodram_B31_B53_registered_route_context_v8781':'scripts.Hodram_B54_B60_registered_route_context_v8868',
        'work/analysis/Hodram_B54_B60_logical_v8801':'work/analysis/Hodram_B61_B70_logical_v8891',
        'translations/hodram_B54_B60_editorial_manuscript_v1.json':'translations/hodram_B61_B70_editorial_manuscript_v1.json',
        'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json':
            'work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json',
        'work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json':'work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json',
        "len(doc['records'])==82 and doc['source_macro_counts']==dict(FI=3,FA=4,FO=0)":"len(doc['records'])==224 and doc['source_macro_counts']==dict(FI=15,FA=3,FO=0)",
        'len(rows)==82':'len(rows)==224',
        'fresh_native_alignment_cases=328,progressive_alignment_cases=324,FE_null_actor_alignment_cases=4':
            'fresh_native_alignment_cases=896,progressive_alignment_cases=896,FE_null_actor_alignment_cases=0',
        'all82_formatting_gates_remain_false':'all224_formatting_gates_remain_false',
        '82 English logical paragraphs / 328 default-name native alignments pass':'224 English logical paragraphs / 896 default-name native alignments pass'
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=receipt,
        original_logical_literal_macro_alignments_complete_memory_ownership_ABI_andguards_preserved=True,
        all224_four_prose_gates_required_formatting_false=True,new_credit=0,full_goal_complete=False))
