"""Keep the prior receipt distinct from the current loop's compiled-page variable."""
from scripts import check_rafael557_punctuation_stored_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

CHANGED=previous.CHANGED
check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
compound_storage=previous.compound_storage
source=checked_text(previous.source,{
    'old=load(args.previous_stored)':'prior_stored=load(args.previous_stored)',
    **{f"old['{key}']":f"prior_stored['{key}']" for key in ['reconstruction','reconstruction_sha256','runtime','native','native_sha256',
        'all_stored_planes_equal_directly_viewed_compiled_planes','every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass','records','relative_cases']},
})
if __name__=='__main__':exec(compile(source,__file__+'::same-proof-guards-distinct-prior-receipt-variable','exec'),globals())
