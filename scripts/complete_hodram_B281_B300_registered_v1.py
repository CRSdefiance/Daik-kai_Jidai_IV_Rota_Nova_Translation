"""Credit the 384 disjoint reviews once, only after release, clean patch and own startup pass."""
import re
from scripts.complete_hodram_B251_B280_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Credit216 unique contextual reviews':'Credit384 unique contextual reviews',
    'work/hodram_B251_B280_release_v1':'work/hodram_B281_B300_release_v1',
    'hodram_B251_B280_integrated_final_review_v1.json':'hodram_B281_B300_integrated_final_review_v1.json',
    'Hodram_SC1_B251_B280_contextual_integrated_20261107':'Hodram_SC1_B281_B300_contextual_integrated_20261107',
    'Hodram_B251_B280_clean_next_20261107':'Hodram_B281_B300_clean_next_20261107',
    '==(703,114,38)':'==(704,114,39)',
    'all216_individual_five_gates_pass':'all384_individual_five_gates_pass',
    'scope=dict(source_variants=209,native_body_pages=212,typed_labels=7,observed_source_variants=86,':
        'scope=dict(source_variants=373,native_body_pages=374,typed_labels=11,observed_source_variants=134,',
    'observed_body_pages=88,offline_only_source_variants=123,':'observed_body_pages=135,offline_only_source_variants=239,',
    'observed_menu_instances=3,observed_choice_labels=7':'observed_menu_instances=5,observed_choice_labels=11',
    "'current_story_gameplay_utterances':86,'current_story_gameplay_pages':88":
        "'current_story_gameplay_utterances':134,'current_story_gameplay_pages':135",
    'Hodram B251–B280 integrated once over registered B231–B250.':'Hodram B281–B300 integrated once over registered B251–B280.',
    'editorial_review_current.Hodram_B251_B280_completion_v1.pending.json':'editorial_review_current.Hodram_B281_B300_completion_v1.pending.json',
    'Credited 216 Hodram B251–B280 reviews once.':'Credited 384 Hodram B281–B300 reviews once.',
})
counts={'216':'384','129':'181','87':'203','17533':'17749','17749':'18133','10828':'11009','6921':'7124','17752':'18136'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:216|129|87|17533|17749|10828|6921|17752)(?![0-9])',lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-all-prefixes-and-families-preserved','exec'),globals())
