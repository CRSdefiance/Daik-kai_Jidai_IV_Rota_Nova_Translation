"""Execute real item canvas construction/clear and its shared primary dispatch.

Upstream parent artwork/input/clipping and real text providers remain unverified.
"""

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
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized

OWNER, RENDERER = 0x02460000, 0x02468000


def source_canvas(source, *, include_machine=False):
    machine = initialized(source)
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    overlay = overlays[0]
    if list(overlays) != [0] or overlay.ramAddress != 0x01FFA000:
        raise ValueError('Native item clear overlay mapping differs')
    machine.mem_write(overlay.ramAddress, bytes(overlay.data))
    machine.mem_write(OWNER, source[0x4D9F8:0x4D9FC])
    machine.mem_write(OWNER + 0x70, b'\xA5' * 0x2D00)
    machine.mem_write(OWNER - 32, b'\xA5' * 32)
    machine.mem_write(OWNER + 0x2E00, b'\xA5' * 32)
    requests, contracts, trace = [], [], set()

    def hook(uc, address, size, data):
        trace.add(address)
        if address == 0x020AE220:
            if uc.reg_read(UC_ARM_REG_R0) != OWNER:
                raise ValueError('Item constructor registers a different widget')
            contracts.append('widget_registration_success')
            uc.reg_write(UC_ARM_REG_R0, 1)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == 0x01FF92D8:
            sp = uc.reg_read(UC_ARM_REG_SP)
            sizep, destp = struct.unpack('<2I', uc.mem_read(sp, 8))
            requests.append({'image': uc.reg_read(UC_ARM_REG_R1), 'layer': uc.reg_read(UC_ARM_REG_R0),
                             'flags': uc.reg_read(UC_ARM_REG_R2),
                             'source_origin': list(struct.unpack('<2i', uc.mem_read(uc.reg_read(UC_ARM_REG_R3), 8))),
                             'size': list(struct.unpack('<2i', uc.mem_read(sizep, 8))),
                             'destination_origin': list(struct.unpack('<2i', uc.mem_read(destp, 8)))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    handle = machine.hook_add(UC_HOOK_CODE, hook)

    def call(start, owner, secondary):
        machine.reg_write(UC_ARM_REG_R0, owner)
        machine.reg_write(UC_ARM_REG_R1, secondary)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(start, STOP, count=100000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Item native canvas method fails to return with intact stack')

    call(0x020D3D80, OWNER + 0x40, 0)
    call(0x0204D8A0, OWNER, 1)
    header = list(struct.unpack('<5I', machine.mem_read(OWNER + 0x2D70, 20)))
    view = list(struct.unpack('<8I', machine.mem_read(OWNER + 0x50, 32)))
    if (header[:3] != [4, 60, 96]
            or (OWNER + 0x2D70 + header[4]) & 0xFFFFFFFF != OWNER + 0x70
            or view != [OWNER + 0x2D70, 5, 0, 0, 0, 0, 240, 96]):
        raise ValueError('Item native canvas allocation/view differs')
    call(0x020D393C, OWNER + 0x40, 0)
    if (bytes(machine.mem_read(OWNER + 0x70, 0x2D00)) != bytes(0x2D00)
            or 0x01FFB2DC not in trace):
        raise ValueError('Item actual native overlay clear fails')
    machine.mem_write(RENDERER, struct.pack('<I', 0x0215FA94))
    machine.mem_write(RENDERER + 0x100, bytes(8))
    machine.reg_write(UC_ARM_REG_R2, 1)
    machine.reg_write(UC_ARM_REG_R3, RENDERER + 0x100)
    call(0x020CFDE8, RENDERER, OWNER + 0x40)
    if (requests != [{'image': OWNER + 0x2D70, 'layer': 1, 'flags': 0,
                      'source_origin': [0, 0], 'size': [240, 96], 'destination_origin': [0, 0]}]
            or not {0x020D3AFC, 0x020D393C, 0x020CFDE8, 0x020D4170} <= trace
            or bytes(machine.mem_read(OWNER - 32, 32)) != b'\xA5' * 32
            or bytes(machine.mem_read(OWNER + 0x2E00, 32)) != b'\xA5' * 32):
        raise ValueError(f'Item native source view/dispatch or canaries differ: {requests}, '
                         f'missing trace {sorted({0x020D3AFC, 0x020D393C, 0x020CFDE8, 0x020D4170} - trace)}, '
                         f'canaries {bytes(machine.mem_read(OWNER - 32, 32)).hex()} / '
                         f'{bytes(machine.mem_read(OWNER + 0x2E00, 32)).hex()}')
    machine.hook_del(handle)
    result = {'geometry': [240, 96], 'native_header': header, 'native_view': view,
            'pixel_span': [OWNER + 0x70, OWNER + 0x2D70], 'draw_requests': requests,
            'actual_constructor_and_seeded_overlay_clear_execute': True,
            'shared_primary_dispatch_executes': True, 'object_canaries_preserved': True,
            'overlay_sha256': sha(bytes(overlay.data)), 'contracts': contracts,
            'direct_shared_draw_layer_and_destination_are_fixtures': True,
            'upstream_parent_draw_artwork_clipping_input_and_gpu_output_verified': False}
    return (result, machine) if include_machine else result
