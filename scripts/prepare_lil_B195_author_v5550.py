"""Record every contextual revision/retention while native layout remains pending."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    print(derive('scripts/author_lil_B193_v5456.py','scripts/author_lil_B195_v5550.py',{
        'B193':'B195','prose_v5455':'prose_v5549','author_v5456':'author_v5550','comparison_v5454/all15':'comparison_v5548/all20',
        "len(gloss['records'])==15":"len(gloss['records'])==20",'voices_v5448':'voices_v5542','dispatches_v5449/all15':'dispatches_v5543/all20',
        'controls_v5451':'controls_v5545','entry_v5450':'entry_v5544','names_v5452':'names_v5546',
        "{'revise':8,'retain-wording':7}":"{'revise':3,'retain-wording':17}",'revised=8,retained=7':'revised=3,retained=17',
        'source_three_Ladies_six_native_name_consumers_and_original_voice0_preserved':
        'source_Barkeep92_Patron103_PortWorker119_six_readonly_names_and_original_voice0_preserved',
        'source_cooking_price_concern_tentative_use_teaching_offer_and_explicit_friendship_preserved':
        'source_unnamed_cheese_specialty_skepticism_one_shared_order_coaxing_two_chewing_beats_praise_and_spreading_word_intention_preserved',
        'source_Chili29_and_both_Seoul_aliases_preserved':'source_Cheese8_and_both_Veracruz_aliases_preserved',
        'source18_linear_commands':'source23_linear_commands','all15':'all20','all7_retentions':'all17_retentions',
        'Record all15':'Record all20','B193:15 whole-exchange decisions,8 revisions/7 justified retentions.':
        'B195:20 whole-exchange decisions,3 revisions/17 justified retentions.',
    }))
