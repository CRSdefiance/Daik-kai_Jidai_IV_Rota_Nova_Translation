"""Keep the exact ARM946 alignment model, dispatching its hook only in range.

The original callback is a no-op outside CEC88..CECC0. Limiting registration
to that range avoids a Python callback for every unrelated instruction.
The historical file and all four load/store emulation cases remain unchanged.
"""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/probe_common_copy_arm946_alignment.py')
SOURCE_SHA = '5fb8c4b4d4cd1930abb9ba55815dfdbd8ea6300ab526bc9b459e80dafdd88024'
_factory = None


def machine(arm):
    global _factory
    if _factory is None:
        assert sha(SOURCE.read_bytes()) == SOURCE_SHA
        text = SOURCE.read_text(encoding='utf-8')
        before = 'machine.hook_add(UC_HOOK_CODE, cpu)'
        after = 'machine.hook_add(UC_HOOK_CODE, cpu, begin=BASE + 0xCEC88, end=BASE + 0xCECC0)'
        assert text.count(before) == 1
        context = {'__name__': '_scoped_ARM946_research', '__file__': str(SOURCE.resolve())}
        exec(compile(text.replace(before, after), str(SOURCE), 'exec'), context)
        _factory = context['arm946_machine']
    cpu = _factory(arm)
    cpu.mem_map(0x01FF0000, 0x10000)
    for section in MainCodeFile(arm, 0x02000000).sections:
        cpu.mem_write(section.ramAddress, bytes(section.data))
    return cpu
