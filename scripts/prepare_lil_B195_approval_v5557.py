"""Seal the viewed original formatter with the independently measured R17 retention reason."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    extra="""    retention_path=Path('work/analysis/lil_B195_R17_guarded_rows_v5558/all11_two_row_splits_rejected_original_three_rows_retained.json')
    retention=read(retention_path)
    assert retention['all11_two_row_splits_fail_unchanged_native_lint'] and retention['no_ordinary_boundary_exception_adopted']
    assert retention['paragraph_ASCII_characters']==68 and retention['selected_formatter_unchanged']
    assert retention['all20_paragraphs_compiled_bytes_and_current_native_planes_unchanged'] and retention['all20_previews_viewed_on_three_returned_sheets']
    assert len(retention['all_complete_word_two_row_splits'])==11
    selected=next(r for r in doc['records'] if r['id']==retention['record_ID'])
    assert selected['compiled_hex']==retention['retained_compiled_hex'] and selected['english']==retention['exact_logical_prose']
    selected['native_layout_retention_reason']=retention['retention_reason']
    doc['source_bound_wrap_retention_proof'],doc['source_bound_wrap_retention_proof_sha256']=str(retention_path),sha(retention_path.read_bytes())
"""
    print(derive('scripts/approve_lil_B195_native_v5554.py','scripts/approve_lil_B195_native_v5557.py',{
        'native_approval_v5554':'native_approval_v5557',
        '    validate_natural_dialogue_batch(doc)':extra+'    validate_natural_dialogue_batch(doc)',
    }))
