"""Prepare native approval with one exact complete-question wrap refinement."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_approval_tools_v5376')
if __name__=='__main__':
    assert not ROOT.exists()
    boundary="""        if row['source_record_index']==64:
            assert len(qa.get('reviewed_ordinary_boundaries',[]))==1 and qa['reviewed_ordinary_boundaries'][0]['after_word']=='be'
            row['reviewed_ordinary_boundaries']=qa['reviewed_ordinary_boundaries']
        else:assert not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries')
"""
    extra="""    proof=Path('work/analysis/lil_B191_wrap_comparison_v5375/all13_unchanged_words_and_exact_R64_boundary.json');wrap=read(proof)
    assert wrap['only_changed_record_IDs']==['DK4_MES_B191_R0064'] and wrap['all13_words_controls_and_prose_unchanged']
    assert wrap['twelve_other_compiled_targets_exact'] and wrap['twelve_other_native_planes_exact'] and len(wrap['exact_source_and_prose_mutation_controls'])==6
    doc['source_bound_wrap_refinement_proof'],doc['source_bound_wrap_refinement_proof_sha256']=str(proof),sha(proof.read_bytes())
"""
    row=derive('scripts/approve_lil_B191_native_v5371.py','scripts/approve_lil_B191_native_v5376.py',{
        'lil_B191_layout_v1':'lil_B191_layout_v3','native_approval_v5371':'native_approval_v5376','fonts_v5370':'fonts_v5374b',
        'editorial_manuscript_v2':'editorial_manuscript_v3','editorial_manuscript_v3':'editorial_manuscript_v4',
        "        assert not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries')\n":boundary,
        'no_record_specific_ordinary_boundary_exception_required=True':'no_record_specific_ordinary_boundary_exception_required=False,exact_source_prose_R64_after_be_boundary_reviewed=True',
        '    validate_natural_dialogue_batch(doc)':extra+'    validate_natural_dialogue_batch(doc)',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_wrap_native_approval.json',dict(derivation=row,
        only_R64_exact_source_and_prose_boundary_allowed=True,all_native_glyph_bounds_page_checks_retained=True,no_credit=True,full_goal_complete=False))
