"""Freeze one-block reference, exact-parent loader reuse and source caller census."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B223_reference_tools_v7102')
if __name__=='__main__':
    assert not ROOT.exists()
    checkpoint=read('work/analysis/editorial_handoff_verification_v7101/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==checkpoint['ledger_sha256']
    for k in ['candidate','patch']:assert sha(Path(checkpoint[k]).read_bytes())==checkpoint[k+'_sha256']
    jobs=[
      ('scripts/create_lil_B214_reference_v6718.py','scripts/create_lil_B223_reference_v7102.py',{
       'B214':'B223','reference_v6718':'reference_v7102',
       'relocation_v6716':'relocation_v7097',
       'stored_v6717/all17_stored_targets68_alignments_seventeen_complete_pages':'stored_v7098/all17_stored_targets68_alignments_nineteen_complete_pages',
       'v6686':'v7067','[214]':'[223]',
       'all17 letter/voice objects,reversible eight-relative-site/native single-page research':'all17 Timur-letter and voice objects,reversible four-relative-site research,nineteen complete native pages'}),
      ('scripts/verify_lil_B214_loader_v6719.py','scripts/verify_lil_B223_loader_v7103.py',{
       'B214':'B223','V6686':'V7067','reference_v6718':'reference_v7102','loader_v6719':'loader_v7103',
       'lil_B213_loader_v6674/whole_SC2_and_B213_initial_entry_proof':'lil_B222_loader_v7055/whole_SC2_and_B222_initial_entry_proof',
       'B2231304_bytes':'B2231384_bytes'}),
      ('scripts/verify_lil_B214_references_v6720.py','scripts/verify_lil_B223_references_v7104.py',{
       'B214':'B223','all27':'all22','All27':'All22',
       'reference_v6718':'reference_v7102','reference_census_v6720':'reference_census_v7104','loader_v6719':'loader_v7103',
       'lil_B213_reference_census_v6675/all27_commands4_relative_sites_original_predicate_staging_and_shipped_census':'lil_B222_reference_census_v7056/all18_commands_no_relative_or_typed_sites_and_shipped_census',
       '[214]':'[223]','block=214':'block=223','len(w)==27':'len(w)==22',
       "len(spec['relative_skip_fixups'])==8":"len(spec['relative_skip_fixups'])==4",
       "len(spec['target_native_skip_cases'])==40":"len(spec['target_native_skip_cases'])==20",
       'all22_commands8_relative_sites_typed_alias_predicates_staging_and_shipped_census':'all22_commands4_relative_sites_typed_alias_predicate_staging_and_shipped_census',
       'typed_relative_span_count=8,target_native_skip_cases=40':'typed_relative_span_count=4,target_native_skip_cases=20',
       'All22 commands/eight relative sites/typed aliases/two predicates':'All22 commands/four relative sites/typed aliases/one predicate'}),
    ]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs]
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tools.json',dict(tools=rows,prior_ledger_sha256=checkpoint['ledger_sha256'],no_native_address_change=True,exact_parent_proof_reused_only_by_whole_ROM_hash=True,new_credit=0,full_goal_complete=False))
