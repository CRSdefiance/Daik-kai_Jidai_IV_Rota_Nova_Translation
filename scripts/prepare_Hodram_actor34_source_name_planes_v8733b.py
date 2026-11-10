"""Qualify the original 19-glyph full-name wrap, preserving the stopped one-row test."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_actor34_source_name_tools_v8733b');assert not root.exists()
    receipt=derive('scripts/prove_Hodram_actor34_source_name_planes_v8733.py','scripts/prove_Hodram_actor34_source_name_planes_v8733b.py',{
        'Hodram_actor34_source_name_planes_v8733':'Hodram_actor34_source_name_planes_v8733b',
        "emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw) and not flushes":"assert [e['code'] for e in events]==codes(raw)",
        "assert all(e['kind']=='cp932' and e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+12<=216 for e in events)":"assert all(e['kind']=='cp932' and e['style']==11 and (e['x'],e['y'])==((i%18)*12,(i//18)*16) and e['x']+12<=216 and e['y']+13<=64 for i,e in enumerate(events))",
        "assert len(events)==len(raw)//2 and max(e['x']+12 for e in events)==12*len(events)":"assert len(events)==len(raw)//2 and len(events)==(13 if r['consumer']=='progressive-nameplate' else 19)\n        assert max(e['x']+12 for e in events)==min(216,12*len(events))",
        "width_px=12*len(events),native_plane=str(path)":"width_px=min(216,12*len(events)),literal_advance_px=12*len(events),rows=1+(len(events)-1)//18,native_plane=str(path)",
        "full_getter_literal_native_plane_not_actual_catalogue_UI_orline_width_measurement=True":"full_getter_literal_native_plane_not_actual_catalogue_UI_orline_width_measurement=True,\n        source_full_literal_19th_character_wraps_to_row2_under_this216px_test_consumer=True,\n        preserved_stopped_one_row_assumption='scripts/prove_Hodram_actor34_source_name_planes_v8733.py',\n        original_metrics_font_guard_andcomplete_glyph_requirements_unchanged=True",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,source_fullname_has19_CP932_glyphs_on_original216px18glyph_row=True,
        exact_original_native_position_model_now_checks_all19_codes_including_final_row2_character=True,
        no_wider_geometry_font_guard_orproduction_QA_change=True,stopped_producer_andpartial_progressive_plane_preserved=True,new_credit=0,full_goal_complete=False))
    print('Prepared exact19glyph/2row source-literal check with unchanged216px geometry;stopped one-row test preserved.')
