"""Execute native result centering, setter, frame geometry and glyph requests."""

import struct

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_MODE_ARM, Uc
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

BASE, STACK, STOP = 0x02000000, 0x027F0000, 0x027FFF00
WIDGET, SCREEN, VTABLE, COORDS, TEXT = 0x02400000, 0x02401000, 0x02402000, 0x02403000, 0x02404000
BITMAP, RESOURCE, GETTER = 0x02405000, 0x02406000, 0x01FFF000


def execute(source, text, row, selected=False):
    source = bytes(source)
    if row not in range(4) or not text or len(text) > 29 or b'\0' in text:
        raise ValueError('Valid complete native row required')
    text.decode('cp932')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x800000)
    machine.mem_map(0x01FF0000, 0x10000)
    machine.mem_write(BASE, source)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.mem_write(STACK + 12, struct.pack('<I', row))
    machine.emu_start(BASE + 0xF7C0C, BASE + 0xF7C54, count=100)
    width, x, height = struct.unpack('<3I', machine.mem_read(STACK + 0x14, 12))
    machine.emu_start(BASE + 0xF7D34, BASE + 0xF7D44, count=20)
    y = machine.reg_read(UC_ARM_REG_R0 + 11)
    if (width, x, height, y) != (180, 38, 12, 32 + 28 * row):
        raise ValueError('Native result centering or row coordinates differ')
    machine.mem_write(WIDGET, struct.pack('<I', BASE + 0x16BAA0))
    machine.mem_write(WIDGET + 0x1C, struct.pack('<4I', int(selected), 1, width, height))
    machine.mem_write(COORDS, struct.pack('<2I', x, y))
    machine.mem_write(TEXT, text + b'\0')
    for index, value in enumerate((WIDGET, COORDS, TEXT, 1)):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.emu_start(BASE + 0xFB004, STOP, count=100)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native frame setter did not return intact')
    if tuple(struct.unpack('<4I', machine.mem_read(WIDGET + 12, 16))) != (x, y, TEXT, 1):
        raise ValueError('Native setter lost geometry, complete text pointer or style')
    machine.mem_write(SCREEN, struct.pack('<I', VTABLE))
    machine.mem_write(VTABLE + 4, struct.pack('<I', GETTER))
    draws, glyphs, calls = [], [], []
    instructions = 0

    def reg(index):
        return machine.reg_read(UC_ARM_REG_R0 + index)

    def pair(address):
        return list(struct.unpack('<2I', machine.mem_read(address, 8)))

    def finish_call(uc, value=0):
        for index in (0, 1, 2, 3, 12):
            uc.reg_write(UC_ARM_REG_R0 + index, 0xDEAD0000 + index)
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def hook(uc, address, size, _):
        nonlocal instructions
        instructions += 1
        if address == GETTER:
            if reg(0) != SCREEN:
                raise ValueError('Native screen getter lost its object')
            calls.append('screen-image-contract')
            finish_call(uc, BITMAP)
        elif address == BASE + 0xD6558:
            calls.append('artwork-resource-contract')
            finish_call(uc, RESOURCE)
        elif address in (0x01FFAC18, 0x01FF92D8, 0x01FF8E4C):
            if reg(0) != BITMAP:
                raise ValueError('Native frame draw targets a different bitmap')
            sp = uc.reg_read(UC_ARM_REG_SP)
            if address == 0x01FFAC18:
                draws.append({'kind': 'background', 'position': pair(reg(2)), 'size': pair(reg(3))})
            else:
                geometry, position = struct.unpack('<2I', uc.mem_read(sp, 8))
                draws.append({'kind': 'artwork-edge-contract', 'position': pair(position),
                              'descriptor': geometry, 'descriptor_words': pair(geometry), 'source': reg(3)})
                if address == 0x01FF8E4C:
                    draws[-1]['strip_end'] = pair(position + 8)
            finish_call(uc)
        elif address in (BASE + 0xD16B4, 0x01FF83AC):
            sp = uc.reg_read(UC_ARM_REG_SP)
            code, style = struct.unpack('<2I', uc.mem_read(sp, 8))
            glyphs.append({'code': code, 'x': reg(2), 'y': reg(3), 'style': style,
                           'advance': 6 if address == BASE + 0xD16B4 else 12})
            finish_call(uc)
        elif not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Frame executes outside source or explicit external contracts')

    machine.hook_add(UC_HOOK_CODE, hook)
    for index, value in enumerate((WIDGET, SCREEN)):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    preserved = {UC_ARM_REG_R0 + index: 0x12340000 + index for index in range(4, 12)}
    for register, value in preserved.items():
        machine.reg_write(register, value)
    flag_address = struct.unpack_from('<I', source, 0xFB4B8)[0] + 12
    initial_flag = bytes(machine.mem_read(flag_address, 4))
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.emu_start(BASE + 0xFB324, STOP, timeout=10000000, count=100000)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK
            or any(machine.reg_read(register) != value for register, value in preserved.items())
            or bytes(machine.mem_read(flag_address, 4)) != initial_flag):
        raise ValueError('Native frame failed to restore caller or renderer state')
    expected_codes = []
    index = 0
    while index < len(text):
        lead = text[index]
        if 0x81 <= lead <= 0xFC:
            if index + 1 >= len(text):
                raise ValueError('Incomplete CP932 character')
            expected_codes.append((lead << 8) | text[index + 1])
            index += 2
        else:
            expected_codes.append(lead)
            index += 1
    if [glyph['code'] for glyph in glyphs] != expected_codes:
        raise ValueError('Native frame renderer dropped complete text characters')
    end = x
    for glyph in glyphs:
        if (glyph['x'], glyph['y'], glyph['style']) != (end, y, 1):
            raise ValueError('Native frame text position or style differs')
        end += glyph['advance']
    if end > x + width or draws[0] != {'kind': 'background', 'position': [x - 12, y - 2], 'size': [width + 24, height + 4]}:
        raise ValueError('Complete text exceeds native frame bounds')
    if len(draws) != 4:
        raise ValueError('Native frame edge draw count differs')
    left, strip, right = draws[1:]
    if (left['position'] != [x - 16, y - 4] or right['position'] != [x + width + 8, y - 4]
            or left['descriptor_words'] != [8, 20] or right['descriptor_words'] != [8, 20]
            or strip.get('strip_end') != [x + width + 8, y + 16]
            or strip['position'] != [x - 8, y - 4]):
        raise ValueError('Native artwork frame border/strip geometry differs')
    if not (0 <= x - 16 < x + width + 16 <= 256 and 0 <= y - 4 < y + 16 <= 192):
        raise ValueError('Native complete frame leaves the screen')
    return {'row': row, 'selected': selected, 'width': width, 'x': x, 'y': y, 'text_end_x': end,
            'draw_calls': draws, 'glyph_requests': glyphs, 'instructions': instructions,
            'stack_and_callee_registers_preserved': True, 'renderer_flag_restored': True,
            'scope': 'Actual centering, setter, FB324 geometry and D1604 ASCII/CP932 dispatch; image/resource, artwork edges and glyph pixel painters are explicit external contracts.'}
