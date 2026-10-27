"""Execute real main item parent and all seven native detail GPU requests.

Border/background/artwork and UI-origin state are explicit runtime contracts.
"""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_item_source_canvas import OWNER, RENDERER, source_canvas

BASE, STACK, STOP = 0x02000000, 0x027F0000, 0x027FFF00


def verify(source):
    canvas, machine = source_canvas(source, include_machine=True)
    ancestor = OWNER + struct.unpack_from('<I', source, 0x13C98C)[0]
    machine.mem_write(ancestor + 0x18, struct.pack('<I', 1))
    machine.mem_write(ancestor + 0x20, bytes(8))
    requests, contracts, executed = [], [], set()

    def hook(uc, address, size, _):
        executed.add(address)
        if address in (BASE + 0xD0AA4, BASE + 0xD0A64):
            if uc.reg_read(UC_ARM_REG_R0) != ancestor:
                raise ValueError('Item parent border/background select a different ancestor')
            contracts.append('native_border_selection' if address == BASE + 0xD0AA4 else 'native_background_selection')
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0xCFDE8 and uc.reg_read(UC_ARM_REG_R1) == OWNER + 0x10:
            contracts.append('native_artwork_selection_not_rendered')
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0x48128:
            if uc.reg_read(UC_ARM_REG_R0) != 0:
                raise ValueError('Item parent selects an unexpected state operation')
            contracts.append('parent_state_update')
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == 0x01FF92D8:
            sp = uc.reg_read(UC_ARM_REG_SP)
            sizep, destination = struct.unpack('<2I', uc.mem_read(sp, 8))
            requests.append({'image': uc.reg_read(UC_ARM_REG_R1), 'layer': uc.reg_read(UC_ARM_REG_R0),
                             'flags': uc.reg_read(UC_ARM_REG_R2),
                             'source_origin': list(struct.unpack('<2i', uc.mem_read(uc.reg_read(UC_ARM_REG_R3), 8))),
                             'size': list(struct.unpack('<2i', uc.mem_read(sizep, 8))),
                             'destination_origin': list(struct.unpack('<2i', uc.mem_read(destination, 8)))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif not (BASE <= address < BASE + len(source)):
            raise ValueError(f'Item parent crop renderer escaped mapped source: {address:08X}')

    handle = machine.hook_add(UC_HOOK_CODE, hook)
    try:
        machine.reg_write(UC_ARM_REG_R0, OWNER)
        machine.reg_write(UC_ARM_REG_R1, RENDERER)
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0x4D490, STOP, count=100000)
    finally:
        machine.hook_del(handle)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or len(requests) != 7 or not {BASE + 0x4D490, BASE + 0xCFC14, BASE + 0xD4170} <= executed
            or any(r['image'] != OWNER + 0x2D70 or r['layer'] != 1 for r in requests)):
        raise ValueError(f'Actual item parent seven-crop dispatch/return differs: {requests}')
    return {'target_arm9_sha256': sha(source), 'canvas': canvas, 'requests': requests,
            'native_parent_and_seven_detail_crop_dispatches_execute': True,
            'destination_256x192_fit_at_native_zero_origin': all(
                0 <= r['destination_origin'][0] <= r['destination_origin'][0] + r['size'][0] <= 256
                and 0 <= r['destination_origin'][1] <= r['destination_origin'][1] + r['size'][1] <= 192 for r in requests),
            'contracts': contracts, 'ancestor_position_and_layer_are_inputs': True,
            'physical_GPU_artwork_border_background_and_controller_input_verified': False}


def main():
    source = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    result = verify(source)
    Path('work/analysis/item_parent_crops_research_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['requests'], indent=2))


if __name__ == '__main__':
    main()
