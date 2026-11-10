"""Reuse complete source masks and audit actual routes rather than assuming SC2 only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_source_audit_tools_v7139')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/audit_lil_B220_source_v6936.py';b='scripts/audit_lil_B224_source_v7139.py';s=Path(a).read_text('utf8')
    lo=s.index("pixels,events,font=raster(image.read_file('/__arm9__.bin'),body)");hi=s.index('\n        ink=',lo);old=s[lo:hi]
    assert 'expected_pixels' in old and 'codes(body)' in old and "e['x']+(6" in old
    new="native=font_rows[row['id']];assert native['source_body_hex']==body.hex() and len(native['pages'])==1;page=native['pages'][0];pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256'] and page['native_independent_plane_equal'] and native['all_visible_first_internal_final_characters_in_order'];events=page['events']"
    c={
      'B220':'B224','source_actual_v6936':'source_actual_v7139','source_fixture_v6930':'source_fixture_v7135','source_run_v6931':'source_run_v7136',
      'name_planes_v6929/two_actors_four_getters_four_name_component_planes16_alignments':'name_planes_v7134/two_actors_four_getters_five_literal_planes20_alignments',
      'consumers_v6922/seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers':'consumers_v7131/fifteen_effective_bodies30_dispatches_two_actors_four_name_consumers',
      'Al_Ferid_font_oracles_v6520':'square_shopkeeper_font_oracles_v7020',
      "if __name__=='__main__':":"FONT=Path('work/analysis/lil_B224_source_pages_v7137/all15_clean_objects_complete_native_CP932_pages_and_exact_consumption.json')\nif __name__=='__main__':",
      'consumer,naming=map(read,[CONSUMER,NAMES])':"consumer,naming=map(read,[CONSUMER,NAMES]);font_proof=read(FONT);assert font_proof['source_context_sha256']==sha(Path(fd['source_context']).read_bytes()) and font_proof['complete_objects']==font_proof['complete_native_pages']==15;font_rows={r['id']:r for r in font_proof['records']}",
      "not trace['unreturned_at_capture_end']":"all((trace['rows'][p['entry_row']]['source']['route'],trace['rows'][p['entry_row']]['source']['block'])!=(2,22) for p in trace['unreturned_at_capture_end'])",
      'all20_source_commands_retained':'all18_source_commands_retained','source_event220':'source_event224',
      "bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;commands=":"banks={i:IlnkContainer.parse(image.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)};bank=banks[2];commands=",
      "s['route']==2":"s['route'] in banks","sha(bank[s['block']])":"sha(banks[s['route']][s['block']])",
      "if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block']":"if (s['route'],s['block'])!=(2,22):following.append(dict(frame=row['frame'],route=s['route'],block=s['block']",
      'len(pairs)==29':'len(pairs)==27','len(observations)==17':'len(observations)==15','all34_source_current_dispatches':'all30_source_current_dispatches',
      old:new,'range(0,17,6)':'range(0,15,6)',
      'all17_source_speeches_complete_Japanese_name_masks29_commands_C200_and_normal_return':'all15_source_speeches_complete_Japanese_name_masks27_commands_C200_and_normal_return',
      'actual_source_unique_speeches=17':'actual_source_unique_speeches=15','all9_initializers_and20_original_commands_observed':'all9_initializers_and18_original_commands_observed','all29_stored_commands_executed':'all27_stored_commands_executed',
      'original_C200_at1274_observed_with_result3':'original_C200_at952_observed_with_result3',"p['source_offset']==1274":"p['source_offset']==952",'not_natural_event220':'not_natural_event224',
      'CONSUMER,NAMES,Path(__file__)]':'CONSUMER,NAMES,FONT,Path(__file__)]',
      'actual_Japanese_speeches=17':'actual_Japanese_speeches=15','commands=29,exit=':'commands=27,exit=',
      'visual_review_pending=True,Japanese_black_masks_only_English_body_unvisited=True':"visual_review_pending=True,source_font_planes_reused_by_exact_hash_without_repeat_render=True,all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank=True,unreturned_following_dialogues_at_capture_end=trace['unreturned_at_capture_end'],later_scene_not_claimed_complete=True,Japanese_black_masks_only_English_body_unvisited=True",
      'exit_frame=pairs[-1][\'returned\'];ROOT.mkdir(parents=True)':"exit_frame=pairs[-1]['returned'];c200=next(p for p in pairs if p['source_offset']==952);assert c200['word']==0xC200 and c200['native_result']==[3,0];ROOT.mkdir(parents=True)",
    }
    assert not Path(b).exists();checked_text(s,c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_actual_mask_audit.json',dict(tool=row,completed15_single_page_masks_reused_by_source_and_plane_hashes=True,cross_route_payloads_and_later_open_dialogues_explicit=True,all_native_addresses_glyph_masks_and_UI_origins_unchanged=True,new_credit=0,full_goal_complete=False))
