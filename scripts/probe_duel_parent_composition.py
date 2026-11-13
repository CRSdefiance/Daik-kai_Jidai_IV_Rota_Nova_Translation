"""Execute both native duel constructors and the primary bitmap draw dispatch.

GPU submission is captured at its native boundary. It is not a GPU emulator.
"""

import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.ordinary_name_fidelity_release import BASE
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized

PARENT, RENDERER = 0x02460000, 0x02461000
ASSET = 0x022BD83C
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
         UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)


def composition(source):
    machine = initialized(source)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.emu_start(BASE + 0x10DD0C, STOP, count=10000)
    header = list(struct.unpack('<5I', machine.mem_read(ASSET, 20)))
    if header != [4, 116, 96, 0xFFE681E4, 0x2594]:
        raise ValueError('Native source image metadata differs')
    width, height = header[1] * 4, header[2]
    bitmap_rows, requests, trace, contracts = [], [], set(), []

    def code(uc, address, size, data):
        trace.add(address)
        if address == BASE + 0xE368:
            owner = uc.reg_read(UC_ARM_REG_R0)
            index = uc.reg_read(UC_ARM_REG_R1)
            rect = list(struct.unpack('<4i', uc.mem_read(uc.reg_read(UC_ARM_REG_R2), 16)))
            bitmap_rows.append({'index': index, 'owner': owner, 'parent_rectangle': rect})
        elif address == BASE + 0xD351C:
            if uc.reg_read(UC_ARM_REG_R0) not in (PARENT + 0x3C + 0x74, PARENT + 0xE0 + 0x74):
                raise ValueError('Unexpected widget registration contract')
            contracts.append({'kind': 'widget_registration', 'owner': uc.reg_read(UC_ARM_REG_R0)})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0xD54C:
            # Full owner/actor/getter/formatter/raster sequence executes in the
            # separate 64 cases. Here it cannot change constructor geometry.
            contracts.append({'kind': 'stat_population', 'actor_index': uc.reg_read(UC_ARM_REG_R1)})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address in (BASE + 0xD13F8, BASE + 0xD0A40, BASE + 0xCFDE8):
            contracts.append({'kind': 'frame_border_or_secondary_picture', 'entry': address})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == 0x01FF92D8:
            sp = uc.reg_read(UC_ARM_REG_SP)
            sizep, destp = struct.unpack('<2I', uc.mem_read(sp, 8))
            requests.append({'image': uc.reg_read(UC_ARM_REG_R1),
                             'layer': uc.reg_read(UC_ARM_REG_R0),
                             'flags': uc.reg_read(UC_ARM_REG_R2),
                             'source_origin': list(struct.unpack('<2i', uc.mem_read(uc.reg_read(UC_ARM_REG_R3), 8))),
                             'size': list(struct.unpack('<2i', uc.mem_read(sizep, 8))),
                             'destination_origin': list(struct.unpack('<2i', uc.mem_read(destp, 8)))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    handle = machine.hook_add(UC_HOOK_CODE, code)
    for index in (0, 1):
        owner = PARENT + 0x3C + index * 0xA4
        machine.reg_write(UC_ARM_REG_R0, owner)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0xE4B0, STOP, count=10000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Native slot initializer fails to return')
    machine.reg_write(UC_ARM_REG_R10, PARENT)
    machine.reg_write(UC_ARM_REG_R9, 0)
    machine.emu_start(BASE + 0xD79C, BASE + 0xD840, count=10000)
    if len(bitmap_rows) != 2 or machine.reg_read(UC_ARM_REG_PC) != BASE + 0xD840:
        raise ValueError('Native two-actor constructor sequence differs')
    machine.mem_write(RENDERER, struct.pack('<I', 0x0215FA94))
    for index, row in enumerate(bitmap_rows):
        owner = row['owner']
        rect = row['parent_rectangle']
        if rect != ([152, 95, 256, 135] if index == 0 else [0, 95, 104, 135]):
            raise ValueError('Actual native parent rectangle differs')
        view = list(struct.unpack('<7I', machine.mem_read(owner + 0x14 + 0x10, 28)))
        if view != [ASSET, 5, 0, 0, 24 + index * 12, 0, 156]:
            raise ValueError('Native bitmap source view differs')
        if struct.unpack('<I', machine.mem_read(owner + 0x14 + 0x2C, 4))[0] != 12:
            raise ValueError('Native bitmap height differs')
        row['source_origin'] = [view[3], view[4]]
        row['source_size'] = [view[6], 12]
        machine.reg_write(UC_ARM_REG_R0, owner)
        machine.reg_write(UC_ARM_REG_R1, RENDERER)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        before = [machine.reg_read(r) for r in SAVED]
        start = len(requests)
        machine.emu_start(BASE + 0xE1B0, STOP, count=10000)
        if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
                or [machine.reg_read(r) for r in SAVED] != before):
            raise ValueError('Parent draw fails to preserve stack or saved registers')
        row['draw_requests'] = requests[start:]
        expected = [([0, 24 + index * 12], [60, 12], [rect[0] + 4, 103]),
                    ([60, 24 + index * 12], [60, 12], [rect[0] + 4, 115]),
                    ([120, 24 + index * 12], [36, 12], [rect[0] + 66, 119])]
        if len(row['draw_requests']) != 3:
            raise ValueError('Parent does not submit three complete text crops')
        for request, (src, dimensions, dest) in zip(row['draw_requests'], expected, strict=True):
            if (request != {'image': ASSET, 'layer': 0, 'flags': 0,
                           'source_origin': src, 'size': dimensions, 'destination_origin': dest}
                    or src[0] + dimensions[0] > width or src[1] + dimensions[1] > height
                    or not (rect[0] <= dest[0] and dest[0] + dimensions[0] <= rect[2]
                            and rect[1] <= dest[1] and dest[1] + dimensions[1] <= rect[3])):
                raise ValueError('Native primary crop clips text or exceeds image/parent bounds')
    machine.hook_del(handle)
    if not {BASE + o for o in (0xD3AFC, 0xD3E88, 0xD4A7C, 0xCB6C, 0xD470C, 0xCFC14, 0xD4170)} <= trace:
        raise ValueError('Actual constructor or parent composition dispatch was bypassed')
    return {'source_image_native_initializer': BASE + 0x10DD0C,
            'native_image_header': header, 'source_canvas': [width, height],
            'source_pixel_base': ASSET + header[4], 'source_palette_base': (ASSET + header[3]) & 0xFFFFFFFF,
            'actor_slots': bitmap_rows, 'native_primary_constructor_dispatch_and_crop_execute': True,
            'all_source_and_destination_bounds_pass': True, 'draw_stack_and_saved_registers_preserved': True,
            'contracts': contracts, 'gpu_submission_is_captured_contract': True}
