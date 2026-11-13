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

MAINROOT = Path('work/analysis/lil_B131_B133_choices_diagnostic_v3321b')
PACKET = Path('work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json')
CHOICES = Path('translations/lil_B131_B133_choice_manuscript_v2.json')
OBJECT,STREAM = 0x02660000,0x02662000

def prove(block,offset):
    ROOT=MAINROOT/f'B{block}_C{offset}'
    assert not ROOT.exists()
    packet,doc = map(read,(PACKET,CHOICES))
    spec = next(r for r in packet['blocks'] if r['block']==block)
    source_command = next(r for r in spec['all_clean_native_commands'] if r['word']==0x2100 and r['offset']==offset)
    current_command = next(r for r in spec['all_current_native_commands'] if r['word']==0x2100 and r['offset']==offset)
    assert source_command['offset'] == current_command['offset'] == offset
    values = [r['english'].encode('ascii') for r in sorted([r for r in doc['records'] if r['block']==block and r['command_offset']==offset],key=lambda r:r['option_index'])]
    assert len(values)==2
    chunks=[];offsets=[];cursor=0
    for value in values:
        assert value and value.strip()==value and b'\n' not in value
        assert all(32<=v<127 for v in value)
        offsets.append(cursor)
        chunk=value+b'\0';chunk+=b'\0'*(-len(chunk)%2)
        chunks.append(chunk);cursor+=len(chunk)
    target=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
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
        for index in range(2):
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
    vm_source=inspect.getsource(prior.choice_vm)
    vm_changes={"pointer, 32":"pointer, len(object_bytes)","96":"VM_GUARD_BYTES"}
    for old,new in vm_changes.items():
        assert old in vm_source,old
        vm_source=vm_source.replace(old,new)
    vm_env={**prior.__dict__,'VM_GUARD_BYTES':max(256,len(target)+32,len(objects[1][1])+32)}
    exec(compile(vm_source,'source_derived_two_choice_VM_v3279','exec'),vm_env)
    choice_vm=vm_env['choice_vm']
    painter = inspect.getsource(prior.paint)
    anchor = '    width, height = 48, 20'
    assert painter.count(anchor) == 1
    painter = painter.replace(anchor,'    width, height = LABEL_WIDTH, 20')
    replacements={
        '    size = width * height // 2':'    stride=(width+3)//4*4;size = stride * height // 2',
        "struct.pack('<5I', 4, width // 4, height,":"struct.pack('<5I', 4, stride // 4, height,",
        '    expected = bytearray(width * height)':'    expected = bytearray(stride * height)',
        'expected[(y + yy) * width + x + index * 6 + xx]':'expected[(y + yy) * stride + x + index * 6 + xx]',
        '    return pixels, {':"    whole=pixels;pixels=bytes(whole[yy*stride+xx] for yy in range(height) for xx in range(width))\n    return pixels, {'storage_stride_px':stride,'logical_width_px':width,'complete_storage_plane_sha256':sha(whole),'storage_padding_all_blank':all(not whole[yy*stride+xx] for yy in range(height) for xx in range(width,stride)),"}
    for old,new in replacements.items():
        assert painter.count(old)==1,old
        painter=painter.replace(old,new)

    needle='    assert pixels == bytes(expected)'
    diagnostic="""    if pixels!=bytes(expected):
        diagnostic_root.mkdir(parents=True,exist_ok=True)
        differences=[dict(x=i%stride,y=i//stride,native=a,expected=b) for i,(a,b) in enumerate(zip(pixels,expected)) if a!=b]
        save(diagnostic_root/'native_complete_plane_difference.json',dict(label=text.decode('ascii'),logical_width=width,storage_stride=stride,expected_origin=[x,y],native_plane_sha256=sha(pixels),independent_plane_sha256=sha(bytes(expected)),differences=differences,native_view_words=list(struct.unpack('<20I',bytes(cpu.mem_read(view,80)))),native_context_words=list(struct.unpack('<12I',bytes(cpu.mem_read(context,48)))),input_and_header_and_canaries_preserved=bytes(cpu.mem_read(string-16,96))==original and bytes(cpu.mem_read(header,20))==raw_header))
        print(dict(label=text.decode('ascii'),logical_width=width,storage_stride=stride,differing_pixels=len(differences),difference_x_bounds=[min(d['x'] for d in differences),max(d['x'] for d in differences)]),flush=True)
    assert pixels == bytes(expected)"""
    assert painter.count(needle)==1
    painter=painter.replace(needle,diagnostic)
    cases,pictures = [],[]
    for version,value in objects[1:]:
        vm = choice_vm(arm,value)
        assert vm['labels'] == [r['text'] for r in next(r for r in decode if r['version']==version)['labels']]
        width = vm['minimum_width_units']*6
        assert 0 < width <= 228
        env = {**prior.__dict__,'LABEL_WIDTH':width,'sha':sha,'save':save,'diagnostic_root':MAINROOT}
        exec(compile(painter,'source_derived_B122_B127_choice_painter_v3279','exec'),env)
        planes = []
        for index,label in enumerate(vm['labels']):
            for style in (1,15):
                pixels,proof = env['paint'](arm,label.encode('ascii'),style)
                assert proof['native_origin'][0] >= 0 and proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank']
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
    sheet = Image.new('RGB',(1000,440),(28,36,40))
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
        manuscript=str(CHOICES),manuscript_sha256=sha(CHOICES.read_bytes()),block=block,original_command_offset=offset,
        clean_current_reviewed_native_decoder_cases=decode,current_and_reviewed_VM_and_font_cases=cases,
        typed_target_object_hex=target.hex(),source_derived_painter_adapter=painter,
        source_derived_two_option_VM_adapter=vm_source,source_count2_results0_1_and_cancel_explicit=True,
        six_original_VM_selection_and_cancel_cases_pass=True,eight_complete_native_style_label_planes_pass=True,
        stored_option_indices_and_original_selection_return_values_preserved=True,
        input_loop_is_bridged_not_actual_selected_branch_gameplay=True,
        actual_visible_selection_association_and_relocated_scene_still_pending=True,
        visual_review_sheet=str(path),visual_review_sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,
        no_ROM_registry_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_decodes=len(decode),native_VM_selection_cancel_cases=6,native_label_planes=8,
        source_bytes=len(objects[1][1]),reviewed_bytes=len(target),actual_selection_still_pending=True))

if __name__=='__main__':
    assert not MAINROOT.exists()
    for block,offset in [(133,1530)]:prove(block,offset)
    cases=[]
    for path in sorted(MAINROOT.glob('B*/original_choice_decoder_VM_geometry_and_native_pixels.json')):
        d=read(path);assert d['six_original_VM_selection_and_cancel_cases_pass'] and d['eight_complete_native_style_label_planes_pass']
        cases.append(dict(proof=str(path),sha256=sha(path.read_bytes()),block=d['block'],command_offset=d['original_command_offset'],review_sheet=d['visual_review_sheet'],review_sheet_sha256=d['visual_review_sheet_sha256']))
    assert len(cases)==1
    save(MAINROOT/'all1_typed_menu_native_proof.json',dict(menus=cases,native_selection_cancel_cases=6,complete_current_and_reviewed_style_label_planes=8,clean_current_reviewed_native_decoder_cases=3,all2_labels_source_order_pointers_counts_and_original_selection_results_preserved=True,input_loop_bridged_not_actual_branch_selection_gameplay=True,visual_review_pending=True,no_ROM_registry_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
