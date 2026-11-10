"""Resolve one stale intake-status field using the completed registered review evidence."""
from scripts.complete_hodram_B281_B300_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    '    rows=[]':
        """    scoped=load(conf['scoped_names'])
    assert scoped['all_five_gates_pass_in_scoped_context'] and len(scoped['records'])==18
    assert all(len(r['review'])==5 and all(r['review'].values()) for r in scoped['records'])
    assert doc['all_individual_five_gates_pass'] and release['exact_all_integrated_references_bound']
    assert sum(r.get('clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending') is True for r in doc['records'])==242
    save(ROOT/'completion_flag_binding_v2.json',dict(
        preserved_first_attempt='v1 stopped at the stale-status assertion before writing an integrated review or changing the ledger.',
        resolved_field='clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending',
        original_intake_status_retained_in_research_manuscript=True,
        qualification=str(release['preparation']),qualification_sha256=release['preparation_sha256'],
        scoped_names=conf['scoped_names'],scoped_names_sha256=sha(Path(conf['scoped_names']).read_bytes()),
        all_source_current_draft_andfive_gate_proofs_required=True,
        no_new_original_event_activation_orparty_membership_claim=True,new_credit=0))
    rows=[]""",
    "'native_style_dispatch_andall_five_review_gates_pending','all_five_review_gates_pending')":
        "'native_style_dispatch_andall_five_review_gates_pending','all_five_review_gates_pending','clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending')",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-one-qualified-stale-intake-status','exec'),globals())
