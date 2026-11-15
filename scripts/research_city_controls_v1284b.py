"""Correct the pilot position query to the proven output-buffer ABI.

The predecessor passed the mobile object as an output pointer in a disposable
CPU copy. Its disassembly is valid; its position fields are invalid and receive
no geometry or gameplay credit. No predecessor query mutated the emulator.
"""
import inspect
from pathlib import Path
from scripts import research_city_controls_v1284 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = "row['position'] = list(struct.unpack('<2i', cpu.mem_read(get(struct.unpack('<I', cpu.mem_read(vt+0x5C, 4))[0]-0x02000000, mobile), 8)))"
    new = "getter = struct.unpack('<I', cpu.mem_read(vt+0x5C, 4))[0]\n            assert getter == 0x02036A24\n            get(getter-0x02000000, 0x02470000, mobile)\n            row['position'] = list(struct.unpack('<2i', cpu.mem_read(0x02470000, 8)))"
    assert source.count(old) == 1
    source = source.replace(old, new)
    source = source.replace("spans = [(0x6ED34,", "spans = [(0x6F0C8, 0x6F4D4), (0x6ED34,")
    env = {**previous.__dict__, '__file__': __file__, 'ROOT': Path('work/analysis/city_controls_v1284b'),
           'RAW': Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_city_v1283b_1266/frame_006010_arm9_ram.bin')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
