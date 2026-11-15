"""Derive exact own-current source-name/voice/default probes for actors00,05,06."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_name_tools_v7921');assert not root.exists()
    row=derive('scripts/prove_Rafael_B45_names_v7869.py','scripts/prove_Rafael_B46_names_v7921.py',{
        'Rafael_B45_names_v7869':'Rafael_B46_names_v7921',
        'Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json':'Rafael_B46_clean_gloss_v7920b/24_speeches2_choices_fresh_clean_glosses_before_current_English.json',
        'current_V7857_Rafael_native_v7868':'current_V7911_Rafael_native_v7914',
        'Rafael_B45_context_binding_v7868':'Rafael_B45_context_binding_v7914',
        "source=read(gloss['source_packet'])":"source=read('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')",
        "gloss['all12_complete_clean_Japanese_speeches_read_before_current_English']":"gloss['complete_clean_exchange_andprerequisite_read_before_current_English']",
        'chosen==[0,6]':'chosen==[0,5,6]',
        "assert excluded==['DK4_MES_B45_R0052']":"assert len(excluded)==12 and all(r['source_selector']==254 for r in gloss['records'] if r['id'] in excluded)",
        "'all_four_original_consumers'":"'all_six_original_consumers'",
        '::two-source-static-speakers':'::three-source-static-speakers',
        "expected={0:'Rafael Castor',6:'Julio Erneco'}":"expected={0:'Rafael Castor',5:'Claudio Manaus',6:'Julio Erneco'}",
        "len(native['rows'])==4":"len(native['rows'])==6",
        "0:['ラファエル','カストール',None],6:":"0:['ラファエル','カストール',None],5:['クラウディオ','マナウス',None],6:",
        'two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json':'three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json',
        'native_four_progressive_andfull_getters':'native_six_progressive_andfull_getters',
        "dict(actor_ID=6,name='Julio Erneco'":"dict(actor_ID=5,name='Claudio Manaus',reason='Clean クラウディオ/マナウス and both original getters support Claudio Manaus. Retain the existing spelling without adding rank or kinship.'),\n            dict(actor_ID=6,name='Julio Erneco'",
        'macro_default_alignment_cases=8':'macro_default_alignment_cases=12',
        'original_source_macro_counts=dict(FI=0,FA=0,FO=1)':'original_source_macro_counts=dict(FI=0,FA=0,FO=0)',
        'actual_FE_source_FO_dispatch_expansion_andpercent_display_pending=True':'actual_12_FE_source_body_dispatch_button_labels_modes_andmenu_owner_display_pending=True',
        'current_English_B45_bodies_still_unread':'current_English_B46_bodies_andtwo_choices_still_unread',
        'no_actual_B45_header_orwhole_catalogue_UI_orcustom_player_name_coverage':'no_actual_B46_header_orwhole_catalogue_UI_orcustom_player_name_coverage',
        "'B45 names:'":"'B46 names:'",
        'Default macros FI6/FA6/FO10,eight guarded alignments.FE source dispatch andpercent consumer still pending;current English unread.':'Synthetic default macros FI6/FA6/FO10,twelve guarded alignments;none added to source. B46 FE/menu dispatch anddisplay pending;current English unread.',
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
