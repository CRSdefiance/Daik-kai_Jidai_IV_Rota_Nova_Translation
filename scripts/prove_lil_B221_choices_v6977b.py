"""Execute original two-choice parsing, modal-return cases and complete label planes.

The modal input loop alone is bridged for isolated 0/1/cancel cases. These
counterfactual native tests do not establish an actual gameplay selection.
"""
import inspect
import struct
from pathlib import Path
from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts import native_B221_menu_backing_v6976 as backing
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B221_choices_v6977')
PACKET=Path('work/analysis/lil_B221_source_v6967/sixteen_clean_current_Crusades_Saladin_context_four_relative_sites_one_choice.json')
MANUSCRIPT=Path('translations/lil_B221_choice_manuscript_v1.json')
OBJECT,STREAM=0x02660000,0x02662000

if __name__=='__main__':
    assert not ROOT.exists()
    packet,doc=map(read,[PACKET,MANUSCRIPT])
    block=packet['blocks'][0]
    source=next(r for r in block['all_clean_native_commands'] if r['word']==0x2100)
    current=next(r for r in block['all_current_native_commands'] if r['word']==0x2100)
    assert source['offset']==current['offset']==150
    values=[r['english'].encode('ascii') for r in sorted(doc['records'],key=lambda r:r['option_index'])]
    assert values==[b'Yes',b'No']
    chunks=[];offsets=[];cursor=0
    for value in values:
        offsets.append(cursor);chunk=value+b'\0';chunk+=bytes(-len(chunk)%2)
        chunks.append(chunk);cursor+=len(chunk)
    target=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
    assert len(target)==14 and offsets==[0,4]
    objects=[('clean',bytes.fromhex(source['whole_command_hex'])),
        ('current',bytes.fromhex(current['whole_command_hex'])),('reviewed-research',target)]
    image=NdsImage.open(packet['current_ROM']);arm=image.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm)==packet['current_ARM9_sha256']=='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
    spans=[(0x2A30C,0x2A414),(0x2A1D8,0x2A30C),(0x51FC0,0x52030),(0x52E40,0x52F50)]
    assert all(arm[a:b]==clean[a:b] for a,b in spans)
    decoded=[]
    for version,value in objects:
        cpu=machine(arm);cpu.mem_write(STREAM-16,b'\xa5'*(len(value)+32));cpu.mem_write(STREAM,value)
        cpu.mem_write(OBJECT-16,b'\xa5'*64);cpu.mem_write(OBJECT,struct.pack('<3I',0,0,STREAM))
        before=bytes(cpu.mem_read(OBJECT-16,64));call(cpu,0x2A3B8,(OBJECT,))
        assert cpu.reg_read(UC_ARM_REG_R0)==2
        labels=[]
        for index in range(2):
            expected=6+struct.unpack_from('<H',value,2+index*2)[0]
            call(cpu,0x2A30C,(OBJECT,index));pointer=cpu.reg_read(UC_ARM_REG_R0)
            assert pointer==STREAM+expected
            text=bytes(cpu.mem_read(pointer,len(value)-expected)).split(b'\0')[0]
            labels.append(dict(stored_index=index,relative_offset=expected,text=text.decode('cp932'),hex=text.hex()))
        assert bytes(cpu.mem_read(OBJECT-16,64))==before
        assert bytes(cpu.mem_read(STREAM,len(value)))==value
        assert bytes(cpu.mem_read(STREAM-16,16))==bytes(cpu.mem_read(STREAM+len(value),16))==b'\xa5'*16
        decoded.append(dict(version=version,native_count=2,labels=labels,original_getters_ABI_input_and_guards_exact=True))
    vm_adapter=checked_text(inspect.getsource(original.choice_vm),{
        'pointer, 32':'pointer, len(object_bytes) - (pointer - text)',
        '96':'VM_GUARD_BYTES',
        'p.decode()':'p.decode("cp932")'})
    env={**original.__dict__,'VM_GUARD_BYTES':max(256,*[len(v)+32 for _,v in objects])}
    exec(compile(vm_adapter,__file__+'::source-owned-choice-VM','exec'),env)
    cases=[];pictures=[]
    for version,value in objects:
        vm=env['choice_vm'](arm,value)
        assert vm['labels']==[r['text'] for r in next(r for r in decoded if r['version']==version)['labels']]
        width=vm['minimum_width_units']*6
        assert 0<width<=228 and len(vm['VM_cases'])==3
        planes=[]
        if version!='clean':
            for index,label in enumerate(vm['labels']):
                for style in [1,8,15]:
                    pixels,proof=backing.paint(arm,label.encode('ascii'),style,width,(0,index*12))
                    assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank']
                    if version=='reviewed-research':assert proof['visible_cell_center_twice']==width
                    assert proof['style']==style
                    planes.append(dict(**proof,index=index,whole_native_plane_sha256=sha(pixels)))
                    if style==1:
                        picture=Image.new('RGB',(width,12));bg=(0,168,176) if index==0 else (204,198,180)
                        picture.putdata([(8,8,8) if p else bg for p in pixels])
                        pictures.append((version+' option'+str(index),picture))
        cases.append(dict(version=version,object_hex=value.hex(),native_VM_getters_geometry_and_selection=vm,
            source_derived_text_canvas_width=width,observed_backing_width=256,observed_backing_height=36,
            logical_caption_height=12,all_six_style_label_planes=planes,
            Japanese_font_plane_not_claimed=version=='clean'))
    assert sum(len(r['all_six_style_label_planes']) for r in cases)==12
    ROOT.mkdir(parents=True)
    path=ROOT/'current_and_reviewed_native_menu_labels.png'
    sheet=Image.new('RGB',(640,190),'#263238');draw=ImageDraw.Draw(sheet)
    for index,(title,picture) in enumerate(pictures):
        x,y=10+(index%2)*320,8+(index//2)*90
        draw.text((x,y),title,fill='white')
        sheet.paste(picture.resize((picture.width*3,36),Image.Resampling.NEAREST),(x,y+22))
    sheet.save(path)
    target_path=ROOT/'typed_two_choice_RESEARCH_ONLY.bin';target_path.write_bytes(target)
    save(ROOT/'three_original_choice_decoders_nine_modal_cases_twelve_complete_label_planes.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(PACKET),source_context_sha256=sha(PACKET.read_bytes()),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        original_command_offset=150,clean_current_reviewed_decoder_cases=decoded,native_cases=cases,
        typed_target_object_hex=target.hex(),target_object=str(target_path),target_object_sha256=sha(target),
        original_code_spans=[dict(start=a,end=b,sha256=sha(arm[a:b]),exact_clean_bytes=True) for a,b in spans],
        source_owned_VM_adapter=vm_adapter,source_owned_painter=Path(backing.__file__).read_text('utf-8'),
        native_selection_cancel_cases=9,complete_current_and_reviewed_style_label_planes=12,
        source_indices0_1_and_original_return_states2_2_0_preserved=True,
        clean_Japanese_decoder_width_rectangle_and_VM_proven_font_plane_unclaimed=True,
        original_modal_input_loop_02051FC0_bridged_counterfactual_offline_not_gameplay=True,
        complete_first_internal_final_ASCII_glyphs_pair_flush_bounds_and_centering=True,
        source_backing_evidence='work/analysis/lil_B206_menu_owner_v6284/actual_caption_context_view_and_backing.json',
        source_backing_evidence_sha256=sha(Path('work/analysis/lil_B206_menu_owner_v6284/actual_caption_context_view_and_backing.json').read_bytes()),
        actual_visible_choice_association_relocation_and_branch_tests_pending=True,
        visual_review_sheet=str(path),visual_review_sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,
        no_ROM_registry_ledger_or_completion_credit=True,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PACKET,MANUSCRIPT,Path(original.__file__),Path(backing.__file__),Path(__file__)]},
        full_goal_complete=False))
    print(dict(decoder_objects=3,native_modal_cases=9,native_ASCII_label_planes=12,
        source_bytes=28,target_bytes=14,actual_selection_pending=True,new_credit=0))
