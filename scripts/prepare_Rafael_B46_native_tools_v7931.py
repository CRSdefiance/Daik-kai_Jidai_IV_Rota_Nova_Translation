"""Derive same-runtime logical and complete-page checks for all24 B46 speeches."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_native_tools_v7931');assert not root.exists();rows=[]
    rows.append(derive('scripts/prove_Rafael_B45_logical_v7874.py','scripts/prove_Rafael_B46_logical_v7931.py',{
        'Original four-alignment macro/literal checks for eleven progressive and one null-actor FE paragraphs.':'Original four-alignment macro/literal checks for12 progressive and12 null-actor FE paragraphs.',
        'Rafael_B45_logical_v7874':'Rafael_B46_logical_v7931',
        'rafael_B45_editorial_manuscript_v1':'rafael_B46_editorial_manuscript_v1',
        'Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json':'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json',
        'prefix in [0,6,254]':'prefix in [0,5,6,254]',
        'len(rows)==12':'len(rows)==24',
        '12_logical_paragraphs48_original_native_alignments_distinct_FE.json':'24_logical_paragraphs96_original_native_alignments12_FE.json',
        'fresh_native_alignment_cases=48,progressive_alignment_cases=44,FE_null_actor_alignment_cases=4':'fresh_native_alignment_cases=96,total_bound_alignment_cases=96,progressive_alignment_cases=48,FE_null_actor_alignment_cases=48',
        'source_macro_totals=dict(FI=0,FA=0,FO=1)':'source_macro_totals=dict(FI=0,FA=0,FO=0)',
        '12 logical paragraphs/48 guarded native alignments pass:44 progressive and4 original null-actor FE. Font,layout,actual andrelease pending.':'24 logical paragraphs/96 guarded native alignments pass:48 progressive and48 original null-actor FE. Fonts,layout,choices,actual and release pending.',
    }))
    rows.append(derive('scripts/prove_Rafael_B45_pages_v7882.py','scripts/prove_Rafael_B46_pages_v7933.py',{
        'Rafael_B45_pages_v7882':'Rafael_B46_pages_v7933',
        'Rafael_B45_layout_v7881/12_automatic_plans_full_native_width_zero_preamble_separate_body.json':'Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json',
        'Rafael_B45_logical_refined_v7876b/12_refined_logical_bindings44_reused4_fresh_alignments.json':'Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json',
        'rafael_B45_editorial_manuscript_v2':'rafael_B46_editorial_manuscript_v1',
        'Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json':'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json',
        "assert b'Castor Co.' in expected and b'20 percent' in expected":"assert all(token not in expected for token in [b'FI',b'FA',b'FO',b'%'])",
        "len(rows)==12 and not ctx.machines and sum(len(r['pages']) for r in rows)==12":"len(rows)==24 and not ctx.machines and sum(len(r['pages']) for r in rows)==24",
        'Rafael_B45_native_pages_sheet':'Rafael_B46_native_pages_sheet',
        '12_complete_native_pages48_compiled_alignments_distinct_FE.json':'24_complete_native_pages96_compiled_alignments12_FE.json',
        'fresh_compiled_alignment_cases=48,progressive_alignment_cases=44,FE_null_actor_alignment_cases=4':'fresh_compiled_alignment_cases=96,progressive_alignment_cases=48,FE_null_actor_alignment_cases=48',
        'complete_progressive_pages=11,complete_FE_logical_andphysical_pages=1':'complete_progressive_pages=12,complete_FE_logical_andphysical_pages=12',
        'FE_source_FO_and20_percent_preserved_without_printf_conversion':'FE_source_zero_macros_buttons_mode_orders_andno_printf_conversion_preserved',
        'all12_formatting_gates_false':'all26_formatting_gates_false',
        '12 complete native pages/48 fresh compiled alignments pass. Two sheets need viewing;actual scenes,relocation andregistered release pending.':'24 complete native pages/96 fresh compiled alignments pass. Four sheets need viewing;choice fonts,actual scenes,relocation andregistered release pending.',
    }))
    root.mkdir(parents=True);save(root/'source_locked_derivations.json',rows)
