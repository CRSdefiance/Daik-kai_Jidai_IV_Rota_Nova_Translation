"""Full registered37-article release/clean-input verifier;17 observed pages and21 offline-only areexplicit."""
from pathlib import Path
from scripts import verify_town_HELP23_registered_release as previous
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.dialogue.reviewed_help_pages_v5 import plan_articles

source=checked_text(previous.source,{
 "len(manifest['batches'])==672":"len(manifest['batches'])==673",
 "len(qualification['changed_partial_coverage_rejections'])==4":"len(qualification['changed_partial_coverage_rejections'])==6",
 "len(compiled['pages'])==28":"len(compiled['pages'])==38",
 'len(blocks)==216':'len(blocks)==217',
 "visual['all15_observed_pages_approved']":"visual['all17_observed_pages_approved']",
 "actual['actual_pages']==15 and actual['actual_articles']==10 and actual['offline_only_pages']==13":
 "actual['actual_pages']==17 and actual['actual_articles']==16 and actual['offline_only_pages']==21",
 "len(actual['offline_only_article_IDs'])==13 and len(actual['original_forward_back_andL_R_history_returns'])==6":
 "len(actual['offline_only_article_IDs'])==21 and len(actual['original_forward_back_andL_R_history_returns'])==7",
 "native['native_pages']==28 and len(native['records'])==28":"native['native_pages']==38 and len(native['records'])==38",
 "native_visual['all28_complete_pages_approved'] and native_visual['all_seven_refined_sheets_directly_viewed']":
 "native_visual['all38_complete_pages_approved'] and native_visual['all_ten_sheets_directly_viewed']",
 "len(doc['records'])==23":"len(doc['records'])==37",
 '(19,4)':'(27,10)',
 'all23_exact_source_current_target_pages_andindividual_five_gates_bound':'all37_exact_source_current_target_pages_andindividual_five_gates_bound',
 'complete_stack_entries=672':'complete_stack_entries=673',
 'new_contextual_records=23,prose_revisions=19,justified_retentions=4':'new_contextual_records=37,prose_revisions=27,justified_retentions=10',
 'native_andvisually_reviewed_pages=28,observed_actual_pages=15,observed_actual_articles=10,offline_only_pages=13,offline_only_articles=13,actual_ordinary_Help_frames=31641':
 'native_andvisually_reviewed_pages=38,observed_actual_pages=17,observed_actual_articles=16,offline_only_pages=21,offline_only_articles=21,actual_ordinary_Help_frames=30681',
 'all23_exact_integrated_references_bound':'all37_exact_integrated_references_bound',
 "Path('work/t23')":"Path('work/s37')",
 'rom_retention_pins.TownHELP23_verified.pending.json':'rom_retention_pins.ShipyardHELP37_verified.pending.json',
 '672 entries/114 accepted layers/eight stages/23 exact articles andclean-input patch pass;28 native,15 observed,13 offline-only pages;own startup binding pending.':
 '673 entries/114 accepted layers/eight stages/37 exact articles andclean-input patch pass;38 native,17 observed,21 offline-only pages;own startup binding pending.',
})
env={**previous.main.__globals__,'__file__':__file__,'plan_articles':plan_articles,
 'PARENT_PROOF':Path('work/analysis/Town_HELP23_release_verified_20261104/registered_release_verification.json'),
 'QUAL':Path('work/analysis/Shipyard_HELP37_release_qualification_v2_20261104/qualification.json')}
exec(compile(source,__file__+'::same-complete-accepted-stack-inverses-individual-page-bindings-andclean-patch-for37-articles','exec'),env)
main=env['main']
if __name__=='__main__':main()
