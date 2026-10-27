"""Retain failed no-wrap reference;derive masks from observed native glyph writes."""
from pathlib import Path


def main():
    target=Path('scripts/probe_duel_text_surface_v1113.py');assert not target.exists()
    body=Path('scripts/probe_duel_text_surface_v1112.py').read_text(encoding='utf-8')
    body=body.replace('duel_text_surface_v1112','duel_text_surface_v1113')
    body=body.replace('from scripts.verify_personal_gameplay_v841 import get_machine',
        'from scripts.verify_personal_gameplay_v841 import get_machine\nfrom scripts.probe_button_prompt_native import STACK')
    body=body.replace('clears=[];draw={}','clears=[];draw={};events=[]')
    before="    hooks=[cpu.hook_add(UC_HOOK_CODE,clear,begin=0x01FFB2DC,end=0x01FFB2DC),"
    assert body.count(before)==1
    body=body.replace(before,"""    def glyph_event(u,pc,size,data):
        code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
        events.append({'code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3)})
    hooks=[cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=BASE+0xD16B4,end=BASE+0xD16B4),
        cpu.hook_add(UC_HOOK_CODE,clear,begin=0x01FFB2DC,end=0x01FFB2DC),""")
    lo=body.index('    expected=bytearray(208*36);full_ink=visible_ink=0')
    hi=body.index('    return {',lo)
    body=body[:lo]+"""    assert bytes(e['code'] for e in events)==text
    expected=bytearray(208*36);full_ink=0
    for event in events:
        assert event['style']==15
        glyph=font.decode(chr(event['code']))
        # Match the original software glyph writer's flat destination stride,
        # including its observed out-of-row writes. This proves the diagnosis,
        # not correct layout:off-row/off-crop coordinates are errors below.
        for y in range(12):
            for x in range(6):
                value=int(y<11 and bool(glyph.getpixel((x,y))))
                full_ink+=value
                at=(event['y']+y)*208+event['x']+x
                if 0<=at<len(expected):expected[at]=value
    assert native==bytes(expected),'Observed native glyph stores differ from independent font replay'
    source_ink=sum(native);visible=bytes(native[y*208+x] for y in range(36) for x in range(144))
    outside_source=[e for e in events if e['x']+6>208 or e['y']+12>36]
    outside_crop=[e for e in events if e['x']+6>144 or e['y']+12>36]
    first=font.decode(chr(text[0]));first_damaged=any(
        native[(12+y)*208+x]!=int(y<11 and bool(first.getpixel((x,y)))) for y in range(12) for x in range(6))
    requests=[]
    def gpu(u,pc,size,data):
        size_pointer,destination_pointer=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
        requests.append({'image':u.reg_read(UC_ARM_REG_R1),
            'source':list(struct.unpack('<2i',u.mem_read(u.reg_read(UC_ARM_REG_R3),8))),
            'size':list(struct.unpack('<2i',u.mem_read(size_pointer,8))),
            'destination':list(struct.unpack('<2i',u.mem_read(destination_pointer,8)))})
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    point=0x02469000;renderer=0x02469100
    cpu.mem_write(point,struct.pack('<2i',52,16));cpu.mem_write(renderer,struct.pack('<I',0x0215FA94))
    cpu.mem_write(STACK,struct.pack('<3I',0,point,0))
    hook=cpu.hook_add(UC_HOOK_CODE,gpu,begin=0x01FF92D8,end=0x01FF92D8)
    try:get(0xCFC14,renderer,view,0x0211460C,3)
    finally:cpu.hook_del(hook)
    assert requests==[{'image':header,'source':[0,i*12],'size':[144,12],'destination':[56,20+i*20]} for i in range(3)]
"""+body[hi:]
    body=body.replace("'only_widget_registration_and_SDK_clear_boundaries_bridged':True,",
        "'widget_registration_and_SDK_clear_bridged_GPU_submission_captured_not_rendered':True,")
    body=body.replace("'source_bitmap_matches_independent_full_glyphs_clipped_to_backing_canvas':True,",
        "'source_bitmap_exact_to_independent_font_replay_at_observed_native_positions':True,\n        'observed_native_glyphs':events,'glyphs_crossing_source_rows':outside_source,\n        'glyphs_outside_final_visible_crop':outside_crop,'first_glyph_damaged_by_later_stride_spill':first_damaged,\n        'original_renderer_three_final_crop_submissions':requests,'correct_visible_layout_approved':False,")
    body=body.replace("'ink_outside_final_crop':full_ink-visible_ink", "'glyph_ink_absent_from_final_crop':full_ink-sum(visible)")
    body=body.replace("canvas=Image.new('RGB',(852,190),'#263238')", "canvas=Image.new('RGB',(852,370),'#263238')")
    body=body.replace("draw.text((4,168),'Visible native crop:144 pixels /24 ASCII cells per row;3 rows',fill='white')",
        "draw.text((4,180),'Final crop144x36:24 cells /3 rows;research diagnostic,not approved',fill='white')\n        crop=Image.frombytes('L',(144,36),bytes(0 if v else 255 for v in visible))\n        canvas.paste(crop.resize((576,144),Image.Resampling.NEAREST),(4,202))")
    body=body.replace("results[0]['ink_outside_final_crop']", "results[0]['glyph_ink_absent_from_final_crop']").replace(
        "r['ink_outside_final_crop']", "r['glyph_ink_absent_from_final_crop']")
    body=body.replace("'native_macro_measurement_constructor_and_glyph_path_execute':True,",
        "'native_macro_measurement_constructor_glyph_and_final_crop_paths_execute':True,\n        'failed_predecessor':'scripts/probe_duel_text_surface_v1112.py',\n        'failed_reference_assumed_no_automatic_row_advance_and_was_rejected':True,\n        'current_default_renderer_advances_after_an_already_out_of_row_glyph':True,\n        'source_stride_spill_can_corrupt_first_glyph_even_when_input_is_fully_consumed':True,")
    body=body.replace("native_duel_visible_columns=24,native_duel_visible_rows=3,",
        "native_duel_visible_columns=24,native_duel_visible_rows=3,\n        original_automatic_glyph_wrap_can_spill_into_next_pixel_row_and_corrupt_initial_letter=True,")
    target.write_text(body,encoding='utf-8')
    print('Created observed-position/native-store diagnostic successor;failed reference retained and no layout approval added.')


if __name__=='__main__':main()
