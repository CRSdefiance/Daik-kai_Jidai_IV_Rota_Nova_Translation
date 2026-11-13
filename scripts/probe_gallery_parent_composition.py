"""Execute the actual Gallery primary canvas constructor and draw dispatch."""

import struct

from ndspy.code import loadOverlayTable
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
from dk4tool.patch.ordinary_name_fidelity_release import BASE
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized

OWNER, RENDERER = 0x02460000, 0x02468000


def composition(source):
    machine = initialized(source)
    # The complete bitmap clear lives in the separately loaded overlay.
    image = NdsImage.open('out/all_routes_combined_v157_candidate.nds')
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    if list(overlays) != [0] or overlays[0].ramAddress != 0x01FFA000:
        raise ValueError('Native Gallery clear overlay mapping differs')
    overlay = overlays[0]
    machine.mem_write(overlay.ramAddress, bytes(overlay.data))
    machine.mem_write(OWNER + 0x14, b'\xA5' * 24576)
    machine.mem_write(OWNER - 32, b'\xA5' * 32)
    machine.mem_write(OWNER + 0x6200, b'\xA5' * 32)
    requests, contracts, trace = [], [], set()

    def code(uc, address, size, data):
        trace.add(address)
        if address == BASE + 0xAE220:
            if uc.reg_read(UC_ARM_REG_R0) != OWNER:
                raise ValueError('Gallery registers a different primary widget')
            contracts.append({'kind': 'primary_widget_registration', 'entry': address})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == 0x01FF92D8:
            sp = uc.reg_read(UC_ARM_REG_SP)
            sizep, destp = struct.unpack('<2I', uc.mem_read(sp, 8))
            requests.append({'image': uc.reg_read(UC_ARM_REG_R1),
                             'layer': uc.reg_read(UC_ARM_REG_R0), 'flags': uc.reg_read(UC_ARM_REG_R2),
                             'source_origin': list(struct.unpack('<2i', uc.mem_read(uc.reg_read(UC_ARM_REG_R3), 8))),
                             'size': list(struct.unpack('<2i', uc.mem_read(sizep, 8))),
                             'destination_origin': list(struct.unpack('<2i', uc.mem_read(destp, 8)))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    machine.hook_add(UC_HOOK_CODE, code)
    for start, object_pointer in ((0xD3D80, OWNER + 0x6028), (0x45C84, OWNER)):
        machine.reg_write(UC_ARM_REG_R0, object_pointer)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + start, STOP, count=100000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Gallery native constructor fails to return')
    header = list(struct.unpack('<5I', machine.mem_read(OWNER + 0x6014, 20)))
    if (header[:3] != [4, 64, 192]
            or (OWNER + 0x6014 + header[4]) & 0xFFFFFFFF != OWNER + 0x14
            or bytes(machine.mem_read(OWNER + 0x14, 24576)) != bytes(24576)):
        raise ValueError('Gallery source canvas or actual whole clear differs')
    view = list(struct.unpack('<8I', machine.mem_read(OWNER + 0x6028 + 0x10, 32)))
    if view != [OWNER + 0x6014, 5, 0, 0, 0, 0, 256, 192]:
        raise ValueError('Gallery primary source view differs')
    machine.mem_write(RENDERER, struct.pack('<I', 0x0215FA94))
    machine.reg_write(UC_ARM_REG_R0, OWNER)
    machine.reg_write(UC_ARM_REG_R1, RENDERER)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.emu_start(BASE + 0x45710, STOP, count=100000)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or requests != [{'image': OWNER + 0x6014, 'layer': 1, 'flags': 0,
                             'source_origin': [0, 0], 'size': [256, 192], 'destination_origin': [0, 0]}]
            or not {BASE + o for o in (0xD3AFC, 0xD393C, 0x45710, 0xCFDE8, 0xD4170)} <= trace
            or 0x01FFB2DC not in trace
            or bytes(machine.mem_read(OWNER - 32, 32)) != b'\xA5' * 32
            or bytes(machine.mem_read(OWNER + 0x6200, 32)) != b'\xA5' * 32):
        raise ValueError('Gallery primary native composition clips or relocates the canvas')
    return {'native_geometry': [256, 192], 'native_header': header,
            'native_backing_pixels': [OWNER + 0x14, OWNER + 0x6014],
            'bitmap_offset': 0x6028, 'native_primary_view': view, 'draw_requests': requests,
            'native_constructor_clear_and_primary_composition_execute': True,
            'nonzero_canvas_seed_cleared_and_object_canaries_preserved': True,
            'native_overlay': {'base': overlay.ramAddress, 'sha256': sha(bytes(overlay.data))},
            'all_source_and_screen_bounds_pass': True,
            'contracts': contracts, 'gpu_submission_is_captured_contract': True,
            'surrounding_art_and_input_not_verified': True}
