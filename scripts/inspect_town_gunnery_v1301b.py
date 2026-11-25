"""Read the original town surrender threshold alongside actual battle snapshots."""
import inspect
from pathlib import Path
from scripts import inspect_aftermath_town_v1292 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = "'native_town_defenses':get(0xB3FD4,town,1),"
    assert source.count(old) == 1
    source = source.replace(old,old+"\n            'native_surrender_check_threshold':struct.unpack('<I',cpu.mem_read(world+0x1364,4))[0],\n            'Gunnery_actor_ID':get(0x82478,fleets+0x2090,9),")
    env = {**previous.__dict__,'__file__':__file__,
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
