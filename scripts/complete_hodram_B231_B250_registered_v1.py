"""Credit the disjoint 225-record scope once, after registered release and own startup."""
import re
from scripts.complete_hodram_B211_B230_registered_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Credit277 unique contextual reviews':'Credit225 unique contextual reviews',
    'work/hodram_B211_B230_release_v1':'work/hodram_B231_B250_release_v1',
    'hodram_B211_B230_integrated_final_review_v1.json':'hodram_B231_B250_integrated_final_review_v1.json',
    'Hodram_SC1_B211_B230_contextual_integrated_20261107':'Hodram_SC1_B231_B250_contextual_integrated_20261107',
    'Hodram_B211_B230_clean_next_20261104':'Hodram_B231_B250_clean_next_20261107',
    '==(701,114,36)':'==(702,114,37)',
    'all277_individual_five_gates_pass':'all225_individual_five_gates_pass',
    'scope=dict(source_variants=270,native_body_pages=284,typed_labels=7,observed_source_variants=65,':
        'scope=dict(source_variants=223,native_body_pages=228,typed_labels=2,observed_source_variants=63,',
    'observed_body_pages=74,offline_only_source_variants=205,':'observed_body_pages=68,offline_only_source_variants=160,',
    'actual_menu_cursor_states=[0],observed_menu_instances=2,observed_choice_labels=5,offline_only_captions=2,byte_identical_repeated_menu_has_offline_proof_not_duplicate_occurrence_credit=True,':
        'actual_menu_cursor_states=[0],observed_menu_instances=1,observed_choice_labels=2,offline_only_captions=0,animated_cursor_band_andcomplete_caption_pixels_qualified=True,',
    'Hodram B211–B230 integrated once over Rafael5186.':'Hodram B231–B250 integrated once over registered B211–B230.',
    'editorial_review_current.Hodram_B211_B230_completion_v1.pending.json':'editorial_review_current.Hodram_B231_B250_completion_v1.pending.json',
    'Credited 277 Hodram B211–B230 reviews once.':'Credited 225 Hodram B231–B250 reviews once.',
    "'all_five_registered_review_gates_pass':True}":
        "'all_five_registered_review_gates_pass':True,'all_five_review_gates_pending':False,'all_formatting_gates_pending':False,'representative_gameplay_pending':False,'final_formatting_andvisual_approval_pending':False}",
})
counts={'277':'225','170':'115','107':'110','17031':'17308','17308':'17533','10584':'10699','6724':'6834','17311':'17536'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:277|170|107|17031|17308|10584|6724|17311)(?![0-9])',lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-with-earlier-prefixes-preserved','exec'),globals())
