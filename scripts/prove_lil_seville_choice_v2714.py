"""Original two-choice decoder/VM/geometry and complete native label planes."""
import inspect
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Seville_choice_v2714')
PACKET = Path('work/analysis/lil_Seville_source_v2704b/complete20_clean_current_native_context.json')
CHOICES = Path('translations/lil_seville_choices_editorial_draft_v1.json')
OBJECT,STREAM = 0x02660000,0x02662000

if __name__ == '__main__':
    assert not ROOT.exists()
    packet,doc = map(read,(PACKET,CHOICES))
    spec = next(r for r in packet['blocks'] if r['block']==28)
    source_command = next(r for r in spec['all_clean_native_commands'] if r['word']==0x2100)
    current_command = next(r for r in spec['all_current_native_commands'] if r['word']==0x2100)
    assert source_command['offset'] == current_command['offset'] == 694
    values = [r['english'].encode('ascii') for r in sorted(doc['records'],key=lambda r:r['option_index'])]
    first = values[0]+b'\0'
    first += b'\0'*(-len(first)%2)
    second = values[1]+b'\0'
    second += b'\0'*(-len(second)%2)
    target = b'\0\x21\0\0'+struct.pack('<H',len(first))+first+second
    objects = [('clean',bytes.fromhex(source_command['whole_command_hex'])),
        ('current',bytes.fromhex(current_command['whole_command_hex'])),('reviewed-research',target)]
    image,clean = NdsImage.open(packet['current_ROM']),NdsImage.open('work/clean.nds')
    arm = image.read_file('/__arm9__.bin')
    spans = [(0x2A30C,0x2A414),(0x2A1D8,0x2A30C),(0x51FC0,0x52030),(0x52E40,0x52F50)]
    assert all(arm[a:b] == clean.read_file('/__arm9__.bin')[a:b] for a,b in spans)
    decode = []
    for version,value in objects:
        cpu = machine(arm)
        cpu.mem_write(STREAM-16,b'\xa5'*(len(value)+32))
        cpu.mem_write(STREAM,value)
        cpu.mem_write(OBJECT-16,b'\xa5'*64)
        cpu.mem_write(OBJECT,struct.pack('<3I',0,0,STREAM))
        before = bytes(cpu.mem_read(OBJECT-16,64))
        call(cpu,0x2A3B8,(OBJECT,))
        assert cpu.reg_read(UC_ARM_REG_R0) == 2
        labels = []
        for index in (0,1):
            expected = 6+struct.unpack_from('<H',value,2+index*2)[0]
            call(cpu,0x2A30C,(OBJECT,index))
            pointer = cpu.reg_read(UC_ARM_REG_R0)
            assert pointer == STREAM+expected
            text = bytes(cpu.mem_read(pointer,len(value)-expected)).split(b'\0')[0]
            labels.append(dict(stored_index=index,relative_offset=expected,text=text.decode('cp932'),hex=text.hex()))
        assert bytes(cpu.mem_read(OBJECT-16,64)) == before
        assert bytes(cpu.mem_read(STREAM,len(value))) == value
        assert bytes(cpu.mem_read(STREAM-16,16)) == bytes(cpu.mem_read(STREAM+len(value),16)) == b'\xa5'*16
        decode.append(dict(version=version,native_count=2,labels=labels,original_getters_ABI_input_and_guards_exact=True))
    painter = inspect.getsource(prior.paint)
    anchor = '    width, height = 48, 20'
    assert painter.count(anchor) == 1
    painter = painter.replace(anchor,'    width, height = LABEL_WIDTH, 20')
    cases,pictures = [],[]
    for version,value in objects[1:]:
        vm = prior.choice_vm(arm,value)
        assert vm['labels'] == [r['text'] for r in next(r for r in decode if r['version']==version)['labels']]
        width = vm['minimum_width_units']*6
        assert 0 < width <= 228
        env = {**prior.__dict__,'LABEL_WIDTH':width}
        exec(compile(painter,'source_derived_Seville_choice_painter_v2714','exec'),env)
        planes = []
        for index,label in enumerate(vm['labels']):
            for style in (1,15):
                pixels,proof = env['paint'](arm,label.encode('ascii'),style)
                assert proof['native_origin'][0] >= 0 and proof['independent_complete_native_pixels_match']
                if version=='reviewed-research':assert proof['visible_cell_center_twice'] == width
                planes.append(dict(**proof,index=index,whole_native_plane_sha256=sha(pixels)))
                if style==1:
                    im = Image.new('RGB',(width,20))
                    bg = (0,168,176) if index==0 else (204,198,180)
                    im.putdata([(8,8,8) if p else bg for p in pixels])
                    pictures.append((f'{version} stored option{index}',im))
        cases.append(dict(version=version,object_hex=value.hex(),native_VM_getters_geometry_and_selection=vm,
            source_derived_text_canvas_width=width,all_four_style_label_planes=planes,
            complete_first_last_internal_glyphs_and_bounds_verified=True))
    ROOT.mkdir(parents=True)
    sheet = Image.new('RGB',(1000,300),(28,36,40))
    draw = ImageDraw.Draw(sheet)
    for index,(title,im) in enumerate(pictures):
        x,y = 12+496*(index%2),10+140*(index//2)
        draw.text((x,y),title,fill='white')
        sheet.paste(im.resize((im.width*2,40),Image.Resampling.NEAREST),(x,y+24))
    path = ROOT/'current_and_reviewed_native_menu_labels.png'
    sheet.save(path)
    (ROOT/'typed_two_choice_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'original_choice_decoder_VM_geometry_and_native_pixels.json',dict(candidate=packet['current_ROM'],
        candidate_sha256=packet['current_ROM_sha256'],source_context=str(PACKET),source_context_sha256=sha(PACKET.read_bytes()),
        manuscript=str(CHOICES),manuscript_sha256=sha(CHOICES.read_bytes()),block=28,original_command_offset=694,
        clean_current_reviewed_native_decoder_cases=decode,current_and_reviewed_VM_and_font_cases=cases,
        typed_target_object_hex=target.hex(),source_derived_painter_adapter=painter,
        six_original_VM_selection_and_cancel_cases_pass=True,eight_complete_native_style_label_planes_pass=True,
        stored_option_indices_and_original_selection_return_values_preserved=True,
        input_loop_is_bridged_not_actual_selected_branch_gameplay=True,
        actual_visible_selection_association_and_relocated_scene_still_pending=True,
        visual_review_sheet=str(path),visual_review_sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,
        no_ROM_registry_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_decodes=len(decode),native_VM_selection_cancel_cases=6,native_label_planes=8,
        source_bytes=len(objects[1][1]),reviewed_bytes=len(target),actual_selection_still_pending=True))
