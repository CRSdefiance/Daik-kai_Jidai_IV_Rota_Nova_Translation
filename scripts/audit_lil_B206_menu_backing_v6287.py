"""Compare the actual complete caption backing to independent original-font glyphs after selection."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_menu_actual_v6287');OWNER=Path('work/analysis/lil_B206_menu_owner_v6284/actual_caption_context_view_and_backing.json');MENU=Path('work/analysis/lil_B206_choices_v6286/all2_typed_menus_native_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();owner=read(OWNER);menu=read(MENU);terminal=read('work/analysis/lil_B206_menu_owner_v6284/terminal.json');plan=read('work/analysis/lil_B206_menu_owner_v6284/plan.json');rp=Path(terminal['report']);report=read(rp)
    assert terminal['terminal'] and terminal['all_host_slots_restored'] and not owner['errors'] and not owner['mismatches'] and report['frames']==3501 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(rp.read_bytes())==terminal['report_sha256'] and report['ROM_sha256']==terminal['ROM_sha256']==sha(Path(plan['ROM']).read_bytes())
    assert menu['native_selection_cancel_cases']==12 and menu['complete_current_and_reviewed_style_label_planes']==24 and menu['all4_labels_source_order_pointers_counts_and_original_selection_results_preserved']
    rawspec=report['read_only_RAM_snapshot'];raw=Path(rawspec['path']).read_bytes();assert len(raw)==4194304 and sha(raw)==rawspec['sha256'] and rawspec['read_only_export'];arm=NdsImage.open(plan['ROM']).read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm)
    assert len({r['backing_pointer'] for r in owner['rows']})==1;pointer=owner['rows'][0]['backing_pointer'];packed=raw[pointer-0x02000000:pointer-0x02000000+4608];pixels=bytes(v for b in packed for v in [b&15,b>>4]);expected=bytearray(256*36);labels=[]
    for index,label in enumerate(["I'll take them!","That's expensive..."]):
        x=(114-len(label)*6)//2;y=index*12;ink=set()
        for i,c in enumerate(label):
            glyph=font.decode(c)
            for yy in range(11):
                for xx in range(6):
                    if glyph.getpixel((xx,yy)):expected[(y+yy+1)*256+x+i*6+xx]=8;ink.add((x+i*6+xx,y+yy+1))
        assert ink and all(any(x+i*6<=px<x+(i+1)*6 for px,py in ink) for i in [0,len(label)-1])
        labels.append(dict(option_index=index,text=label,visible_cell_origin=[x,y],all_first_final_internal_glyphs_and_blank_physical_guards_exact=True))
    assert pixels==bytes(expected),'Actual complete physical backing differs from independent glyph plane'
    sheets=[]
    for r in menu['menus']:
        assert sha(Path(r['review_sheet']).read_bytes())==r['review_sheet_sha256'];sheets.append(dict(path=r['review_sheet'],sha256=r['review_sheet_sha256'],viewed_after_image_return=True))
    photo=next(r for r in report['frames_captured'] if r['frame']==3500);assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'actual_full114px_two_labels256x36_backing_equals_independent_native_font.json',dict(complete_actual_backing_plane_sha256=sha(pixels),complete_independent_plane_sha256=sha(bytes(expected)),all4608_actual_packed_backing_bytes_and9216_pixels_equal=True,actual_logical_caption_size=[114,12],actual_physical_backing_size=[256,36],actual_caption_style=8,actual_second_menu_labels=labels,complete_first_T_stem_all_trailing_periods_and_odd_pair_blank_flush_preserved=True,no_actual_glyph_loss_from_failed_tight_bitmap_model=True,all_four_choice_labels24_native_style_planes12_original_selection_cancel_cases_and2_viewed_sheets_pass=True,viewed_sheets=sheets,actual_second_selected_label_capture=dict(**photo,viewed_after_image_return=True),actual_original_constructor_cold_boot_frames=3501,actual_second_menu_order_and_DOWN_selection_observed=True,original_input_loop_bridged_only_in_offline_VM_proof_actual_run_ordinary_inputs=True,actual_menu_acceptance_refusal_branch_association_not_exercised_in_focused_fixture=True,no_B206_story_natural_event_payment_effect_route_or_hardware_coverage=True,English_progressive_native_layout_full_scene_relocation_and_release_still_pending=True,no_ROM_wording_padding_font_viewport_guard_or_metrics_change=True,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OWNER,MENU,rp,Path(rawspec['path']),Path(plan['ROM']),Path('work/analysis/lil_B206_menu_owner_v6284/terminal.json'),Path('work/analysis/lil_B206_menu_owner_v6284/plan.json'),Path('work/analysis/lil_B206_menu_model_v6285/actual_native_backing_corrected_model_and_preserved_failures.json'),Path(__file__)]}));print('Actual whole256x36 caption backing equals independent font pixels:full T stem/all periods/two complete labels. Four labels/24 style planes/12 selection-cancel cases pass;English full-scene/relocation/release pending.')
