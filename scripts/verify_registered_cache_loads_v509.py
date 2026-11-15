"""Load every existing registered PXL through the original cache and SDK bridge."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.research_online_loader_v190 import resource_call

ROM = Path('out/all_routes_combined_v508_candidate.nds')
OUT = Path('work/analysis/resource_registry_v509')
OPEN,READ,SEEK,CLOSE = 0x020DED50,0x020DEBDC,0x020DEB70,0x020DED08


def main():
    registry_path = OUT/'registry_proof.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    assert sha(ROM.read_bytes()) == registry['candidate_sha256']
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,original = rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    ranges = [(0x5310,0x5340),(0xD6524,0xD6C90),(0xD0398,0xD051C)]
    assert all(arm[lo:hi] == original[lo:hi]for lo,hi in ranges)
    u = machine(arm)
    trace = resource_call(u,0x5310,())
    constructors = list(struct.unpack_from('<41I',arm,0x12FB58))
    assert set(constructors) <= trace and struct.unpack_from('<I',arm,0x12FBFC)[0] == 0
    manager = struct.unpack_from('<I',arm,0x5D24)[0]
    call(u,0xD6C0C,(manager,))
    pool_start,pool_end = struct.unpack('<2I',u.mem_read(manager,8))
    by_path = {}
    for row in registry['constructed_owners']:
        if row.get('ROM_path'):
            by_path.setdefault(row['ROM_path'],row)
    assert len(by_path) == 356
    filenames = {row['owner']+12 for row in registry['constructed_owners']}
    filename_bytes = {field+i for field in filenames for i in range(4)}
    paths = {p.casefold():p for p in rom.path_map()}
    handles,events,name_writes = {},[],[]

    def bridge(cpu,address,size,unused):
        if address == 0x020E5650:
            raise ValueError('Original loader reached a fatal assertion')
        if address not in (OPEN,READ,SEEK,CLOSE):
            return
        obj = cpu.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R1),128)).split(b'\0')[0].decode('ascii')
            requested = '/'+name.replace('\\','/').lstrip('/')
            path = paths[requested.casefold()]
            raw = rom.read_file(path)
            assert obj not in handles
            handles[obj] = [path,raw,0]
            cpu.mem_write(obj+0x20,struct.pack('<2I',0,len(raw)))
            events.append({'operation':'open','path':path,'bytes':len(raw),'sha256':sha(raw)})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            position = cpu.reg_read(UC_ARM_REG_R1)
            assert cpu.reg_read(UC_ARM_REG_R2) == 0 and 0 <= position <= len(state[1])
            state[2] = position
            result = 1
        elif address == READ:
            state = handles[obj]
            destination,count = cpu.reg_read(UC_ARM_REG_R1),cpu.reg_read(UC_ARM_REG_R2)
            assert state[2]+count <= len(state[1])
            cpu.mem_write(destination,state[1][state[2]:state[2]+count])
            state[2] += count
            events.append({'operation':'read','path':state[0],'bytes':count})
            result = count
        else:
            events.append({'operation':'close','path':handles.pop(obj)[0]})
            result = 1
        cpu.reg_write(UC_ARM_REG_R0,result)
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))

    def watch_name(cpu,access,address,size,value,unused):
        if any(byte in filename_bytes for byte in range(address,address+size)):
            name_writes.append({'address':address,'bytes':size,'writer':cpu.reg_read(UC_ARM_REG_PC)})

    h1 = u.hook_add(UC_HOOK_CODE,bridge)
    h2 = u.hook_add(UC_HOOK_MEM_WRITE,watch_name)
    cases = []
    try:
        for index,(path,row) in enumerate(sorted(by_path.items())):
            owner = row['owner']
            raw = rom.read_file(path)
            name_pointer = bytes(u.mem_read(owner+12,4))
            assert list(struct.unpack('<5I',u.mem_read(owner,20))) == row['fields_after_registration']
            start = len(events)
            executed = resource_call(u,0xD6558,(owner,))
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert pool_start <= pointer < pointer+len(raw) <= pool_end,path
            assert bytes(u.mem_read(pointer,len(raw))) == raw,path
            assert bytes(u.mem_read(owner+12,4)) == name_pointer
            cold = events[start:]
            hot_start = len(events)
            resource_call(u,0xD6558,(owner,))
            assert u.reg_read(UC_ARM_REG_R0) == pointer
            assert len(events) == hot_start and bytes(u.mem_read(pointer,len(raw))) == raw
            assert not handles
            cases.append({'path':path,'owner':owner,'file_sha256':sha(raw),'file_bytes':len(raw),
                          'native_cache_pointer':pointer,'cold_io':cold,'hot_load_no_IO_same_pointer':True,
                          'complete_header_palette_pixel_bytes_exact':True,
                          'filename_field_unchanged':True,'distinct_native_instructions':len(executed)})
            if (index+1)%50 == 0:
                print(f'Checked {index+1}/356 registered cache files',flush=True)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    assert not name_writes
    item_owner = by_path['/_pxl/item.pxl']['owner']
    dynamic = []
    for caller,literal in [(0x02047888,0x478C8),(0x02047BA0,0x47C50)]:
        actual_owner = struct.unpack_from('<I',arm,literal)[0]
        assert actual_owner == item_owner
        dynamic.append({'call':caller,'original_literal_owner':actual_owner,
                        'registered_filename':'_pxl/item.pxl','filename_unchanged_in_all356_cold_warm_loads':True})
    proof = {'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
             'registry_proof_sha256':sha(registry_path.read_bytes()),'all41_original_constructors_reached':True,
             'original_code_ranges_exact':ranges,'native_cache_pool':[pool_start,pool_end],
             'all356_registered_file_loads':cases,'all712_cold_and_hot_native_returns_ABI_checked':True,
             'all_registered_filename_field_writes_during_loads':name_writes,
             'two_original_item_reader_literal_bindings':dynamic,
             'SDK_filesystem_only_bridged':True,
             'supplied_owner_calls_not_all_gameplay_callers_or_GPU_crops':True,
             'fifteen_unmatched_placeholder_owners_not_loaded_or_declared_globally_unused':True,
             'raw_legacy_archives_not_accessed_by_these_PXL_cache_cases':True,
             'production_ROM_modified':False,'full_goal_complete':False}
    (OUT/'cache_load_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('All356 registered PXL files load exactly; warm hits and all filename fields preserved.')


if __name__ == '__main__':
    main()
