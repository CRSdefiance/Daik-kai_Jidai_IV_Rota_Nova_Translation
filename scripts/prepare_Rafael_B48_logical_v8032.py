"""Prepare source-locked logical native checks for87 progressive andfour FE B48 paragraphs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B48_logical_tools_v8032')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Rafael_B47_logical_v7983.py','scripts/prove_Rafael_B48_logical_v8032.py',{
        'Rafael_B47_logical_v7983':'Rafael_B48_logical_v8032',
        'rafael_B47_editorial_manuscript_v1.json':'rafael_B48_editorial_manuscript_v2.json',
        'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json':
            'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json',
        "body=row['english'].encode('cp932')":"body=row['english'].replace('{MACRO:FI}','FI').encode('cp932')",
        'prefix in [0,4,5,6] and not is_FE':'prefix in [0,4,5,6,7,8,13,75,113,254]',
        'assert len(rows)==15':'assert len(rows)==91',
        '15_logical_paragraphs60_original_native_progressive_alignments.json':'91_logical_paragraphs364_original_native_alignments4_FE.json',
        'fresh_native_alignment_cases=60,total_bound_alignment_cases=60,progressive_alignment_cases=60,FE_null_actor_alignment_cases=0':
            'fresh_native_alignment_cases=364,total_bound_alignment_cases=364,progressive_alignment_cases=348,FE_null_actor_alignment_cases=16',
        'source_macro_totals=dict(FI=0,FA=0,FO=0)':'source_macro_totals=dict(FI=1,FA=0,FO=0)',
        'B47_has_no_FE_orfallback208_all15_source_progressive':'B48_has87_progressive_four_FE_no_fallback208_andprintable4B71_source_state_only',
        '15 logical paragraphs/60 guarded native alignments pass;all progressive,zero source macros.Layout,fonts,actual andrelease pending.':
            '91 logical paragraphs/364guarded native alignments pass;87progressive/fourFE,one sourceFI.Layout,fonts,actual andrelease pending.',
        'Original four-alignment macro/literal checks for all15 B47 progressive paragraphs.':
            'Original four-alignment macro/literal checks for91 B48 paragraphs;four FE consumers stay distinct.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('B48 logical364-alignment probe prepared;formatting/native font pages/actual/release pending.')
