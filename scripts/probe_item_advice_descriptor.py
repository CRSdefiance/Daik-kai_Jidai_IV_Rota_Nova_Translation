"""Execute actual conditional descriptor setup for both native item menus."""

import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

BASE, FRAME = 0x02000000, 0x02450000


def prepare(source, machine, menu, advice_enabled, select_enabled=True):
    if menu not in ('gallery', 'regular') or menu == 'gallery' and not select_enabled:
        raise ValueError('Unmapped native item menu configuration')
    gallery = menu == 'gallery'
    start, end = (0x4553C, 0x455A8) if gallery else (0x4D104, 0x4D180)
    field, table, displacement = (0x45664, 0x1156A8, 0x4048) if gallery else (0x4D254, 0x11627C, 0x4058)
    flag_owner = struct.unpack_from('<I', source, 0x45660 if gallery else 0x4D250)[0]
    machine.mem_write(flag_owner + 4, struct.pack('<I', 16 if advice_enabled else 0))
    descriptor = FRAME + displacement
    machine.mem_write(descriptor - 16, b'\xA5' * 56)
    context = machine.context_save()
    stack = machine.reg_read(UC_ARM_REG_SP)
    machine.mem_write(stack + 12, struct.pack('<I', int(select_enabled)))
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address < BASE + len(source):
            raise ValueError('Item descriptor setup escaped native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((descriptor <= address < address + size <= descriptor + 24)
                or (stack - 40 <= address < address + size <= stack)):
            raise ValueError('Item descriptor setup escaped descriptor/stack')

    handles = [machine.hook_add(UC_HOOK_CODE, code), machine.hook_add(UC_HOOK_MEM_WRITE, write)]
    try:
        machine.reg_write(UC_ARM_REG_R0, FRAME)
        machine.emu_start(BASE + start, BASE + end, count=1000)
        expected = list(struct.unpack_from('<6I', source, table))
        if advice_enabled:
            expected[2] = struct.unpack_from('<I', source, field)[0]
        if not gallery and not select_enabled:
            expected[5] = 0
        actual = list(struct.unpack('<6I', machine.mem_read(descriptor, 24)))
        if (machine.reg_read(UC_ARM_REG_PC) != BASE + end or 0x23C60 not in executed
                or actual != expected or machine.reg_read(UC_ARM_REG_SP) != stack - 40
                or bytes(machine.mem_read(descriptor - 16, 16)) != b'\xA5' * 16
                or bytes(machine.mem_read(descriptor + 24, 16)) != b'\xA5' * 16):
            raise ValueError('Native conditional item menu descriptor/guards differ')
    finally:
        for handle in handles:
            machine.hook_del(handle)
        machine.context_restore(context)
    return {'menu': menu, 'advice_enabled': advice_enabled, 'select_enabled': select_enabled,
            'pointer': descriptor, 'words': actual, 'source_table': BASE + table,
            'advice_pointer_field': BASE + field, 'native_setup_segment': [BASE + start, BASE + end],
            'native_option_bit_query_executes': True, 'guards_and_descriptor_pass': True,
            'paused_constructor_frame_bytes': 40,
            'flag_state_and_outer_widget_binding_are_contracts': True}
