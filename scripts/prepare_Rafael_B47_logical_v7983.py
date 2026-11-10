"""Prepare four native literal/macro alignments for every B47 logical paragraph."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_logical_tools_v7983')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Rafael_B46_logical_v7931.py','scripts/prove_Rafael_B47_logical_v7983.py',{
        'Rafael_B46_logical_v7931':'Rafael_B47_logical_v7983',
        'rafael_B46_editorial_manuscript_v1':'rafael_B47_editorial_manuscript_v1',
        'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json':
            'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json',
        'prefix in [0,5,6,254]':'prefix in [0,4,5,6] and not is_FE',
        'len(rows)==24':'len(rows)==15',
        '24_logical_paragraphs96_original_native_alignments12_FE.json':'15_logical_paragraphs60_original_native_progressive_alignments.json',
        'fresh_native_alignment_cases=96,total_bound_alignment_cases=96,progressive_alignment_cases=48,FE_null_actor_alignment_cases=48':
            'fresh_native_alignment_cases=60,total_bound_alignment_cases=60,progressive_alignment_cases=60,FE_null_actor_alignment_cases=0',
        'FE_uses_original24310_null_actor_not_progressive_orfallback208':'B47_has_no_FE_orfallback208_all15_source_progressive',
        'Original four-alignment macro/literal checks for12 progressive and12 null-actor FE paragraphs.':
            'Original four-alignment macro/literal checks for all15 B47 progressive paragraphs.',
        '24 logical paragraphs/96 guarded native alignments pass:48 progressive and48 original null-actor FE. Fonts,layout,choices,actual and release pending.':
            '15 logical paragraphs/60 guarded native alignments pass;all progressive,zero source macros.Layout,fonts,actual andrelease pending.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B47 logical native checks without changing global guards.')
