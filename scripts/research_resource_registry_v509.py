"""Execute original resource registration and record every constructed owner."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.research_online_loader_v190 import resource_call

ROM = Path('out/all_routes_combined_v508_candidate.nds')
OUT = Path('work/analysis/resource_registry_v509')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,original = rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    ranges = [(0x5310,0x5340),(0x12FB58,0x12FC00),
              (0x10E190,0x11182C),(0x111A90,0x1123D0),(0xD6C74,0xD6C90)]
    assert all(arm[lo:hi] == original[lo:hi]for lo,hi in ranges)
    u = machine(arm)
    owners = []
    opened = []
    class_writes = []

    def observe(cpu,address,size,unused):
        if address == 0x020D6C74:
            owners.append({'owner':cpu.reg_read(UC_ARM_REG_R0),'constructor_return':cpu.reg_read(UC_ARM_REG_LR)})
        elif address == 0x020DED50:
            opened.append(address)

    handle = u.hook_add(UC_HOOK_CODE,observe)
    def class_write(cpu,access,address,size,value,unused):
        if size == 4 and value == 0x02160538:
            class_writes.append({'owner':address,'writer':cpu.reg_read(UC_ARM_REG_PC)})
    write_handle = u.hook_add(UC_HOOK_MEM_WRITE,class_write)
    traces = []
    try:
        for offset in (0x5310,):
            traces.append({'initializer':offset+0x02000000,'distinct_executed_instructions':len(resource_call(u,offset,()))})
    finally:
        u.hook_del(handle)
        u.hook_del(write_handle)
    assert not opened
    by_owner = {r['owner']:r for r in owners}
    for event in class_writes:
        by_owner.setdefault(event['owner'],{'owner':event['owner'],'constructor_return':None})
    memory = bytes(u.mem_read(0x02000000,0x400000))
    for at in range(0,len(memory)-20,4):
        address = 0x02000000+at
        fields = struct.unpack_from('<5I',memory,at)
        if fields[:3] == (0x02160538,address+4,address+4) and fields[4] == 0xFFFFFFFF:
            by_owner.setdefault(address,{'owner':address,'constructor_return':None})
    owners = list(by_owner.values())
    names = []
    for row in owners:
        fields = struct.unpack('<5I',u.mem_read(row['owner'],20))
        assert fields[:3] == (0x02160538,row['owner']+4,row['owner']+4) and fields[4] == 0xFFFFFFFF
        row['fields_after_registration'] = list(fields)
        pointer = fields[3]
        if not 0x02000000 <= pointer < 0x02400000-128:
            row['filename'] = None
            continue
        raw = bytes(u.mem_read(pointer,128)).split(b'\0')[0]
        try:
            name = raw.decode('ascii')
        except UnicodeDecodeError:
            row['filename'] = None
            row['unparsed_filename_hex'] = raw.hex()
            continue
        path = '/'+name.replace('\\','/').lstrip('/')
        row['filename'] = name
        paths = {p.casefold():p for p in rom.path_map()}
        if path.casefold() in paths:
            resolved = paths[path.casefold()]
            row['ROM_path'] = resolved
            row['file_sha256'] = sha(rom.read_file(resolved))
            names.append(resolved)
        else:
            row['ROM_path'] = None
    proof = {'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
             'original_code_ranges_exact':ranges,'native_initializers':traces,
             'constructed_owners':owners,'unique_registered_ROM_paths':sorted(set(names)),
             'all_named_owner_vtable_writes_in_both_initializers':class_writes,
             'filesystem_opens_during_registration':opened,
             'registration_does_not_prove_loading_crops_GPU_or_global_nonuse':True,
             'production_ROM_modified':False,'full_goal_complete':False}
    (OUT/'registry_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'owners':len(owners),'unique_paths':len(set(names)),
                      'unresolved_names':sum(not r.get('ROM_path')for r in owners),
                      'suffixes':sorted({Path(p).suffix for p in names})},indent=2))


if __name__ == '__main__':
    main()
