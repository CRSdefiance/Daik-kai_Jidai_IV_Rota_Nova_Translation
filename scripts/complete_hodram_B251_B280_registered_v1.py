"""Credit the disjoint 216-record scope once after registered release and own startup."""
import re
from scripts.complete_hodram_B231_B250_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Credit225 unique contextual reviews':'Credit216 unique contextual reviews',
    'work/hodram_B231_B250_release_v1':'work/hodram_B251_B280_release_v1',
    'hodram_B231_B250_integrated_final_review_v1.json':'hodram_B251_B280_integrated_final_review_v1.json',
    'Hodram_SC1_B231_B250_contextual_integrated_20261107':'Hodram_SC1_B251_B280_contextual_integrated_20261107',
    'Hodram_B231_B250_clean_next_20261107':'Hodram_B251_B280_clean_next_20261107',
    '==(702,114,37)':'==(703,114,38)',
    'all225_individual_five_gates_pass':'all216_individual_five_gates_pass',
    'scope=dict(source_variants=223,native_body_pages=228,typed_labels=2,observed_source_variants=63,':
        'scope=dict(source_variants=209,native_body_pages=212,typed_labels=7,observed_source_variants=86,',
    'observed_body_pages=68,offline_only_source_variants=160,':'observed_body_pages=88,offline_only_source_variants=123,',
    'observed_menu_instances=1,observed_choice_labels=2':'observed_menu_instances=3,observed_choice_labels=7',
    'Hodram B231–B250 integrated once over registered B211–B230.':'Hodram B251–B280 integrated once over registered B231–B250.',
    'editorial_review_current.Hodram_B231_B250_completion_v1.pending.json':'editorial_review_current.Hodram_B251_B280_completion_v1.pending.json',
    'Credited 225 Hodram B231–B250 reviews once.':'Credited 216 Hodram B251–B280 reviews once.',
    "'all_five_registered_review_gates_pass':True,":"'current_story_gameplay_utterances':86,'current_story_gameplay_pages':88,'all_five_registered_review_gates_pass':True,",
})
counts={'225':'216','115':'129','110':'87','17308':'17533','17533':'17749','10699':'10828','6834':'6921','17536':'17752'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:225|115|110|17308|17533|10699|6834|17536)(?![0-9])',lambda m:counts[m[0]],source)
if __name__=='__main__':
    exec(compile(source,__file__+'::same-once-only-credit-all-earlier-prefixes-preserved','exec'),globals())
