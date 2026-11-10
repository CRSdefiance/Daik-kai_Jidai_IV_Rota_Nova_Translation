"""Prepare source-bound four-actor identity/getter probes without B47 current speech."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_name_tools_v7976')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Rafael_B46_names_v7921.py','scripts/prove_Rafael_B47_names_v7976.py',{
        'Rafael_B46_names_v7921':'Rafael_B47_names_v7976',
        'Rafael_B46_clean_gloss_v7920b/24_speeches2_choices_fresh_clean_glosses_before_current_English.json':
            'Rafael_B47_clean_gloss_v7973/15_fresh_clean_glosses_complete_B37_context_before_current_English.json',
        'current_V7911_Rafael_native_v7914':'current_V7964_Rafael_native_v7967',
        'Rafael_B45_context_binding_v7914':'Rafael_B46_context_binding_v7967',
        'Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json':
            'Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json',
        "gloss['complete_clean_exchange_andprerequisite_read_before_current_English']":
            "gloss['all15_glosses_fresh_before_current_English_exposure']",
        'chosen==[0,5,6]':'chosen==[0,4,5,6]',
        "assert len(excluded)==12 and all(r['source_selector']==254 for r in gloss['records'] if r['id'] in excluded)":
            'assert excluded==[]',
        "'all_six_original_consumers'":"'all_eight_original_consumers'",
        '::three-source-static-speakers':'::four-source-static-speakers',
        "expected={0:'Rafael Castor',5:'Claudio Manaus',6:'Julio Erneco'}":
            "expected={0:'Rafael Castor',4:'Janus Pasar',5:'Claudio Manaus',6:'Julio Erneco'}",
        "len(native['rows'])==6":"len(native['rows'])==8",
        "0:['ラファエル','カストール',None],5:":
            "0:['ラファエル','カストール',None],4:['ジェナス','パサー',None],5:",
        'three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json':
            'four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json',
        'native_six_progressive_andfull_getters':'native_eight_progressive_andfull_getters',
        "dict(actor_ID=5,name='Claudio Manaus'":
            "dict(actor_ID=4,name='Janus Pasar',reason='Clean ジェナス/パサー and both native getters support retaining the established Janus Pasar identity. パサー is distinct from パシャ in the force references; do not rename him Pasha or infer an affiliation. Full catalogue UI andwider207 consumers remain unreviewed.'),\n            dict(actor_ID=5,name='Claudio Manaus'",
        'macro_default_alignment_cases=12':'macro_default_alignment_cases=16',
        'actual_12_FE_source_body_dispatch_button_labels_modes_andmenu_owner_display_pending':
            'all15_progressive_body_nameplate_source_predicates_andactual_display_pending',
        'current_English_B46_bodies_andtwo_choices_still_unread':'current_English_B47_bodies_still_unread',
        'no_actual_B46_header_orwhole_catalogue_UI_orcustom_player_name_coverage':
            'no_actual_B47_header_orwhole_catalogue_UI_orcustom_player_name_coverage',
        'full207_names_branches_controls_FE_fonts_actual_andrelease_still_pending':
            'full207_names_branches_controls_progressive_fonts_actual_andrelease_still_pending',
        "'B46 names:'":"'B47 names:'",
        'Synthetic default macros FI6/FA6/FO10,twelve guarded alignments;none added to source. B46 FE/menu dispatch anddisplay pending;current English unread.':
            'Synthetic default macros FI6/FA6/FO10,sixteen guarded alignments;none added to source.All15 B47 progressive displays andbranches pending;current English unread.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared four-actor B47 identity probes;current speech remains unread.')
