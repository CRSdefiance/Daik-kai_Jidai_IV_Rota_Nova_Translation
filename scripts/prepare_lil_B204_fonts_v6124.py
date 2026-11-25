"""Prepare complete current-native B204 planes and source-consumer negative controls."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_font_tools_v6124')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/verify_lil_B203_fonts_v6028.py','scripts/verify_lil_B204_fonts_v6124.py',{
        'B203':'B204','fonts_v6028':'fonts_v6124','lil_current_font_oracles_v5918':'lil_current_font_oracles_v6122',
        'scripts.current_build_native_context_v4774':'scripts.current_build_native_context_v6097',
        'work/analysis/lil_B203_voices_v6011/current_native_input.json':'work/analysis/lil_B204_current_v6118/current_native_input.json',
        'blocks[203]':'blocks[204]','blocks[202]':'blocks[203]',
        'len(cases)==len(qa_reports)==22 and macro_calls==176':'len(cases)==len(qa_reports)==20 and macro_calls==160',
        "sum(c['kind']=='system-FE' for c in cases)==1":"sum(c['kind']=='system-FE' for c in cases)==4",
        '[2,76,170,254]':'[2,11,124,130,145,254]','format(76 if selector==2 else 2':'format(11 if selector==2 else 2',"r['source_selector']==76":"r['source_selector']==11",'len(negatives)==22':'len(negatives)==24',
        'all22_progressive_FE_native_planes_and176_alignment_cases':'all20_progressive_FE_native_planes_and160_alignment_cases',
        'current_original_macro_alignment_calls=176':'current_original_macro_alignment_calls=160','progressive_alignment_calls=168':'progressive_alignment_calls=128','FE_null_actor_alignment_calls=8':'FE_null_actor_alignment_calls=32','complete_progressive_planes=21':'complete_progressive_planes=16','complete_FE_logical_and_physical_planes=1':'complete_FE_logical_and_physical_planes=4',
        'native_source_FI1_FA0_FO0_and_all_four_selectors_preserved':'native_source_FI0_FA0_FO0_and_all_six_selectors_preserved',
        'All22 current-font native planes,176 alignment cases and22 source-consumer negatives':'All20 current-font native planes,160 alignment cases and24 source-consumer negatives',
        'Complete B203 current-font progressive/FE planes and176 native alignment cases.':'Complete B204 current-font progressive/FE planes and160 native alignment cases.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(tool=tool,twenty_original_consumers_and_all_source_selectors_bound=True,native_addresses_and_glyph_geometry_unchanged=True,no_new_ROM_gameplay_or_review_credit=True,full_goal_complete=False));print('B20420-plane/160-alignment native verifier prepared with24 negative controls.')
