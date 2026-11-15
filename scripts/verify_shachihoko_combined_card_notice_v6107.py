"""Complete actual card and generated-notice glyphs on the coordinated-data fixture."""
import inspect,struct
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.lil_current_font_oracles_v5918 import _expected
from scripts.prove_shachihoko_actual_name_glyphs_v6086 import tracked_model
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_combined_name_glyphs_v6107')
RUN=Path('work/analysis/shachihoko_item_menu_run_v6104')
if __name__=='__main__':
    assert not ROOT.exists();terminal,plan=map(read,[RUN/'terminal.json',RUN/'run_plan.json']);assert terminal['terminal'];cap=Path(plan['capture_folder']);report=read(cap/'capture_report.json');image=NdsImage.open(plan['research_ROM']);arm=image.read_file('/__arm9__.bin')
    assert report['ROM_sha256']==plan['research_ROM_sha256']==sha(Path(plan['research_ROM']).read_bytes())
    adapted=checked_text(inspect.getsource(raster),{'    events = []':'    cpu.mem_write(ctx+0x1C, struct.pack("<I", TRACKING_WORD))\n    events = []'})
    env={**raster.__globals__,'TRACKING_WORD':0xFFFFFFFF};exec(compile(adapted,__file__+'::original-item-title-tracking','exec'),env);cases=[]
    for kind,frame,text,origin,width,color in [('card_title',4750,b'Shachihoko',(88,236),88,(230,230,230)),('generated_acquisition_notice',5530,b'Shachihoko acquired!',(16,296),216,(0,8,0))]:
        pixels,events,font=(env['raster'] if kind=='card_title' else raster)(arm,text);expected=tracked_model(arm,events) if kind=='card_title' else _expected(arm,font,events)
        assert pixels==expected and [e['code'] for e in events]==list(text)
        model={(i%216,i//216) for i,v in enumerate(pixels) if v};photo=next(r for r in report['frames_captured'] if r['frame']==frame);p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB')
        observed={(x,y) for y in range(12) for x in range(width) if im.getpixel((origin[0]+x,origin[1]+y))==color};assert observed==model
        cases.append(dict(kind=kind,frame=frame,text_hex=text.hex(),native_events=events,complete_native_plane_sha256=sha(pixels),actual_foreground_color=list(color),original_source_bound_origin=list(origin),native_parent_width=width,PNG=str(p),PNG_sha256=photo['PNG_sha256'],all_first_interior_final_glyphs_and_blank_guards_exact=True))
    ROOT.mkdir(parents=True);save(ROOT/'actual_coordinated_card_and_generated_notice_complete_glyphs.json',dict(cases=cases,
        all_two_current_native_independent_and_actual_field_masks_exact=True,no_glyph_or_source_substitution_loss=True,
        actual_expanded_runtime_coordinated_name_and_description_fixture=True,generated_notice_not_a_new_stored_story_object_or_generic_prose_approval=True,
        no_natural_event_activation_earned_route_progress_full_effects_or_hardware_claim=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RUN/'terminal.json',RUN/'run_plan.json',cap/'capture_report.json',Path(__file__),Path('scripts/lil_current_font_oracles_v5918.py'),Path('scripts/prove_shachihoko_actual_name_glyphs_v6086.py')]}))
    print('Coordinated target actual card title and generated acquisition notice match complete native+independent glyph masks. No new generic prose or dialogue credit.')
