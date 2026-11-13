"""Exhaustive nested native speech/choice source packet for SC2 B120 and B23."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.research_wedding_command_v676 import walk
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lessons_source_v1717')
ROM = Path('out/all_routes_combined_v1711_candidate.nds')
SNAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY/final_arm9_ram.bin')
INPUT, OUTPUT = 0x02660000, 0x02662000
SPEAKERS = {2:'Lil Argot',9:'Camille',14:'Emilio',20:'Fernando',254:'System tutorial panel'}


def inventory(arm, block):
    commands = []
    def visit(start,end,ancestors):
        body = block[start:end]
        synthetic = b'CS\0\1'+struct.pack('<H',len(body))+b'\0\0'+body
        native = walk(arm,synthetic)
        assert native['error'] is None and native['stopped_offset']==native['logical_end']==len(body)+8
        for command in native['rows']:
            at = start+command['offset']-8; extent = command['native_extent']
            row = {'offset':at,'word':command['word'],'native_extent':extent,
                'ancestor_0100_offsets':ancestors,'whole_command_hex':block[at:at+extent].hex(),
                'native_result_hex':command['result']}
            commands.append(row)
            if command['word']==0x0100:
                assert extent==4+struct.unpack_from('<H',block,at+2)[0]
                visit(at+4,at+extent,[*ancestors,at])
    logical = 8+struct.unpack_from('<H',block,4)[0]
    assert logical<=len(block) and not any(block[logical:])
    visit(8,logical,[])
    rows = sorted((r for r in commands if r['word']==0x4000),key=lambda r:r['offset'])
    raw_headers = [i for i in range(len(block)-4) if block[i:i+5]==b'\0\x40\xff\xff\0']
    assert raw_headers==[r['offset'] for r in rows]
    return commands,rows


if __name__ == '__main__':
    assert not ROOT.exists()
    clean, current = NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    arm = current.read_file('/__arm9__.bin'); raw = SNAP.read_bytes()
    cpu,get = get_machine(arm,raw)
    assert get(0x7F244)==2 and struct.unpack_from('<I',raw,0x2796B0)[0]==2
    actors=get(0xCB184); captain=actors+0x19E4
    hook=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    files=[im.read_file('/data/SC2.DK4') for im in (clean,current)]
    source_blocks,current_blocks=[IlnkContainer.parse(f).blocks for f in files]
    packets=[]
    try:
        for number in (120,23):
            source,target=source_blocks[number],current_blocks[number]
            commands,speeches=inventory(clean.read_file('/__arm9__.bin'),source)
            now,now_speeches=inventory(arm,target)
            assert [(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in commands]==[
                (r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in now]
            parts=source.split(b'\0'); offsets={sum(len(p)+1 for p in parts[:i]):i for i in range(len(parts))}
            rows=[]
            for command in speeches:
                offset=command['offset']+5
                original=source[offset:source.index(b'\0',offset)]
                before=target[offset:target.index(b'\0',offset)]
                assert original[:1]==before[:1] and original[0] in SPEAKERS
                actor_ID=None if original[0]==254 else get(0x2434C,original[0])
                actor=captain if actor_ID in (None,2) else actors+4+actor_ID*32
                cpu.mem_write(INPUT-16,b'\xA5'*2080);cpu.mem_write(INPUT,before[1:]+b'\0')
                input_guard=bytes(cpu.mem_read(INPUT-16,2080))
                cpu.mem_write(OUTPUT-16,b'\xA5'*4128)
                call(cpu,0x242C8,(OUTPUT,INPUT,actor),instruction_limit=400000)
                runtime=bytes(cpu.mem_read(OUTPUT,4096)).split(b'\0')[0]
                assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
                assert bytes(cpu.mem_read(INPUT-16,2080))==input_guard
                assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xA5'*16
                assert bytes(cpu.mem_read(OUTPUT+len(runtime)+1,4096-len(runtime)-1))==b'\xA5'*(4096-len(runtime)-1)
                ident=f'DK4_MES_B{number:02d}_R{offsets[offset]:04d}'
                rows.append({'id':ident,'file_path':'/data/SC2.DK4','block':number,'record_index':offsets[offset],
                    'source_reference':{'offset':offset,'bytes':len(original),'header_offset':offset-5},
                    'current_reference':{'offset':offset,'bytes':len(before),'header_offset':offset-5},
                    'source_hex':original.hex(),'source_Japanese':original[1:].decode('cp932'),
                    'source_presentation_prefix_hex':original[:1].hex(),'speaker':SPEAKERS[original[0]],
                    'current_text_hex':before.hex(),'current_stored_English':before[1:].decode('cp932'),
                    'current_native_macro_output_hex':runtime.hex(),'current_native_macro_English':runtime.decode('cp932'),
                    'current_native_macro_entire4MiB_ABI_input_output_guards_exact':True,
                    'macro_probe_actor_ID':actor_ID,'system_FE_probe_uses_captain_without_claiming_FE_display_consumer':original[0]==254,
                    'ancestor_0100_offsets':command['ancestor_0100_offsets'],
                    'full_native_display_portrait_bounds_pages_and_runtime_branch_reachability_unverified':True})
            choices=[]
            for command in commands:
                if command['word']!=0x2100:continue
                at=command['offset'];extent=command['native_extent']
                choices.append({**command,'source_hex':source[at:at+extent].hex(),
                    'current_hex':target[at:at+extent].hex(),
                    'source_first_label':source[at+6:source.index(b'\0',at+6)].decode('cp932'),
                    'current_first_label':target[at+6:target.index(b'\0',at+6)].decode('cp932'),
                    'label_lengths_offsets_original_consumer_and_alternate_option_still_require_typed_review':True})
            packets.append({'block':number,'source_block_sha256':sha(source),'current_block_sha256':sha(target),
                'source_bytes':len(source),'current_bytes':len(target),'all_nested_native_commands':commands,
                'all_speech_headers_equal_independent_raw_header_inventory':True,
                'original_current_all_nested_offsets_extents_and_0100_ancestors_equal':True,
                'native_walks_map_structure_not_branch_reachability':True,'records':rows,'choices':choices})
    finally:
        cpu.hook_del(hook)
    ROOT.mkdir(parents=True)
    save(ROOT/'complete_lesson_source_context.json',{'format':'dk4-editorial-source-context-packet-v1',
        'file_path':'/data/SC2.DK4','source_ROM':'work/clean.nds','source_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'source_file_sha256':sha(files[0]),'current_file_sha256':sha(files[1]),'ARM9_sha256':sha(arm),
        'actual_snapshot':str(SNAP),'actual_snapshot_sha256':sha(raw),'blocks':packets,
        'scope':'Complete B120 steering/sail lesson and B23 crew lesson,including nested0100 branches and FE system panels;choices retained as typed unresolved structures.',
        'native_macro_probe_is_not_a_display_or_whole_scene_gameplay_claim':True,
        'no_ROM_registry_or_editorial_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    for packet in packets:
        print('B',packet['block'],'speech',len(packet['records']),'nested commands',len(packet['all_nested_native_commands']),'choices',len(packet['choices']),flush=True)
