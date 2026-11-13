"""Bind all actual pages and the sole retained glyph's verified original shadow palette."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_English_audit_tools_v7157')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/audit_lil_B220_English_v6948.py';b='scripts/audit_lil_B224_English_v7157.py'
    c={'B220':'B224','English_actual_v6948':'English_actual_v7157','English_fixture_v6946':'English_fixture_v7154','English_run_v6947':'English_run_v7155',
      'source_actual_v6936/all17_source_speeches_complete_Japanese_name_masks29_commands_C200_and_normal_return':'source_actual_v7139/all15_source_speeches_complete_Japanese_name_masks27_commands_C200_and_normal_return',
      'stored_v6941/all17_final_stored_targets68_alignments17_complete_pages':'stored_v7149/all15_final_stored_targets60_alignments15_complete_pages',
      'name_planes_v6929/two_actors_four_getters_four_name_component_planes16_alignments':'name_planes_v7134/two_actors_four_getters_five_literal_planes20_alignments',
      'consumers_v6922/seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers':'consumers_v7131/fifteen_effective_bodies30_dispatches_two_actors_four_name_consumers',
      "if __name__=='__main__':":"PAL=Path('work/analysis/lil_B224_ellipsis_palette_v7156b/retained_R11_source_lighter_gray_palette_and_complete_masks.json')\nif __name__=='__main__':",
      'source,stored,names,consumer=map(read,[SOURCE,STORED,NAMES,CONSUMER])':"source,stored,names,consumer=map(read,[SOURCE,STORED,NAMES,CONSUMER]);pal=read(PAL);assert pal['actual_source_proof_sha256']==sha(SOURCE.read_bytes()) and pal['record_ID']=='DK4_MES_B224_R0011' and pal['complete_source_current_compiled_hex']=='1a8163' and pal['retained_CP932_shadow_RGB']==[197,198,197]",
      "not trace['unreturned_at_capture_end']":"all((trace['rows'][p['entry_row']]['source']['route'],trace['rows'][p['entry_row']]['source']['block'])!=(2,22) for p in trace['unreturned_at_capture_end'])",
      'all20_source_commands_retained':'all18_source_commands_retained','source_event220':'source_event224',
      "bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;commands=":"banks={i:IlnkContainer.parse(image.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)};bank=banks[2];commands=",
      "s['route']==2":"s['route'] in banks","sha(bank[s['block']])":"sha(banks[s['route']][s['block']])",
      "if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block']":"if (s['route'],s['block'])!=(2,22):following.append(dict(frame=row['frame'],route=s['route'],block=s['block']",
      'complete=[];nameholds=[];partial=[]':"complete=[];nameholds=[];partial=[];retained=record['id']==pal['record_ID'];gray_RGB=tuple(pal['retained_CP932_shadow_RGB']) if retained else (98,97,98)\n            if retained:assert ref['final_target_hex']==pal['complete_source_current_compiled_hex']=='1a8163' and len(black)==len(gray)==6",
      "actualgray={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(98,97,98)}":"actualgray={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==gray_RGB}",
      "                complete.append(dict(frame=frame":"                if retained:assert sha(im.crop((16,296,232,360)).tobytes())==pal['source_body_RGB_sha256']\n                complete.append(dict(frame=frame",
      'complete_independent_native_body_black_gray_all_glyphs_equal=True':'complete_independent_native_body_black_gray_all_glyphs_equal=True,body_shadow_RGB=list(gray_RGB),retained_R11_full_body_RGB_equals_original=retained',
      'native_stored_plane=page[\'native_plane\']':'body_shadow_RGB=list(gray_RGB),retained_original_R11_palette_scope=retained,native_stored_plane=page[\'native_plane\']',
      'len(pairs)==29':'len(pairs)==27','len(observations)==17':'len(observations)==15','range(0,17,6)':'range(0,15,6)',
      'all17_English_speeches_complete_native_masks29_commands_C200_source_comparison':'all15_English_speeches_complete_native_masks27_commands_C200_source_comparison',
      'actual_unique_speeches=17':'actual_unique_speeches=15','all29_commands_observed':'all27_commands_observed',
      'original_C200_source_offset1274_target1270_observed':'original_C200_source_offset952_target1034_observed',"p['source_offset']==1274":"p['source_offset']==952",'not_natural_event220':'not_natural_event224','speeches=17':'speeches=15',
      'visual_review_pending=True,new_credit=0':"visual_review_pending=True,retained_R11_complete_original_CP932_ink_lighter_gray_and_whole_body_RGB_verified=True,ellipsis_palette_proof=str(PAL),ellipsis_palette_proof_sha256=sha(PAL.read_bytes()),ASCII_dark_gray_masks_and_all_name_masks_unchanged=True,all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank=True,unreturned_following_dialogues_at_capture_end=trace['unreturned_at_capture_end'],later_scene_not_claimed_complete=True,new_credit=0",
      'SOURCE,STORED,NAMES,CONSUMER,rp,tp':'SOURCE,STORED,NAMES,CONSUMER,PAL,rp,tp',
    }
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_actual_English_audit.json',dict(tool=row,all15_body_and_header_glyph_masks_required=True,sole_unchanged_1a8163_glyph_has_source_measured_lighter_shadow_and_exact_original_RGB_requirement=True,no_font_glyph_runtime_guard_QA_or_capture_modified=True,cross_route_payloads_and_later_open_dialogues_explicit=True,new_credit=0,full_goal_complete=False))
