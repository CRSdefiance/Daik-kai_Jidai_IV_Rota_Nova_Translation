"""Prepare88 native alignment cases and11 current-font planes;no old pixel approval reused."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_font_tools_v4793')
if __name__=='__main__':
    assert not ROOT.exists()
    old_context="""    contextpath=ROOT/'historical_source_context.json'
    save(contextpath,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json'
    save(inputpath,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(contextpath)))"""
    tools=[derive('scripts/verify_lil_B179_fonts_v4724.py','scripts/verify_lil_B180_fonts_v4794.py',{
        'Complete B179 progressive/FE native planes and112 original alignment cases.':'Complete B180 current-font progressive/FE planes and88 native alignment cases.',
        'lil_B179_profile':'lil_B180_profile','lil_B179_layout_v1':'lil_B180_layout_v1',
        'lil_B179_fonts_v4724':'lil_B180_fonts_v4794','lil_B179_editorial':'lil_B180_editorial',
        'from scripts.current_common_native_context_v2677 import CurrentContext':'from scripts.current_build_native_context_v4774 import CurrentContext',
        'from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter':'from scripts.lil_current_font_oracles_v4792 import make_painter,expected_pixels',
        'from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels':'from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster',
        old_context:"    inputpath=Path('work/analysis/lil_B180_voices_v4775/current_native_input.json')",
        'len(cases)==len(qa_reports)==14 and macro_calls==112':'len(cases)==len(qa_reports)==11 and macro_calls==88',
        'blocks[179]':'blocks[180]','blocks[178]':'blocks[179]',
        'for selector in [92,96,152,254]':'for selector in [166,167,254]',
        'format(96 if selector==92 else 92':'format(167 if selector==166 else 166',
        "r['source_selector']==92 and":"r['source_selector']==166 and",
        'assert len(negatives)==20':'assert len(negatives)==18',
        'all14_progressive_FE_native_planes_and112_alignment_cases':'all11_progressive_FE_native_planes_and88_alignment_cases',
        'current_original_macro_alignment_calls=112,progressive_alignment_calls=104,FE_null_actor_alignment_calls=8':
            'current_original_macro_alignment_calls=88,progressive_alignment_calls=80,FE_null_actor_alignment_calls=8',
        'complete_progressive_planes=13,complete_FE_logical_and_physical_planes=1':'complete_progressive_planes=10,complete_FE_logical_and_physical_planes=1',
        'all_four_selectors_preserved':'all_three_selectors_preserved',
        'all_actor_models_and_original4MiB_context_preserved_under_bounded_overlays':'all_actor_models_and_current4MiB_context_preserved_without_overlay',
        'actual_selected_B179_IDs':'actual_selected_B180_IDs',
        'All14 complete native planes,112 alignment cases and20 source-consumer negatives pass;two sheets need visual review.':
            'All11 current-font native planes,88 alignment cases and18 source-consumer negatives pass;two sheets need visual review.'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,
        all_current_native_code_and_font_source_bound=True,no_old_font_pixel_approval_inherited=True,
        historical_FE_evidence_is_typed_geometry_only=True,current_B180_actual_FE_gameplay_still_pending=True,
        no_new_metric_guard_phrase_exception_ROM_or_credit=True,full_goal_complete=False))
    print('Prepared current-font11-plane/88-alignment proof;historical geometry and current native pixels remain distinct.')
