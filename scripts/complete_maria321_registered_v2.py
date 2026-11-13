"""Clear the inherited draft-only provisional label after all registered gates pass."""
from scripts.complete_maria321_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "        row.update(no_proposal_may_ship_orreceive_completion_credit_yet=False,planned_integrated_reference=bound['registered_reference'],registered_integration_pending=False,":
        """        if row.get('names_andUI_terms_provisional_until_consumer_binding'):
            assert row['approved_names_terms_titles_andruntime_substitutions_pending'] is False
            assert len(row['scoped_prose_name_term_references'])==3 and all(row['review'].values())
            row['names_andUI_terms_provisional_until_consumer_binding']=False
        row.update(no_proposal_may_ship_orreceive_completion_credit_yet=False,planned_integrated_reference=bound['registered_reference'],registered_integration_pending=False,""",
})

if __name__ == '__main__':
    exec(compile(source,__file__+'::same-once-only-credit-guards-clear-source-bound-draft-metadata','exec'),globals())
