"""One prebattle approach to the actual loaded Speyer position from V1350.

The first pilot proved that its offscreen cached point differs from its
ordinary loaded point. Retain all source guards and the forty own-position
bytes;derive this location from the existing ship in a hashed actual capture.
"""
import inspect
import struct
from pathlib import Path
from scripts import native_ship_sinking_fixture_v1351 as previous
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_fixture_v1352')
REFERENCE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1350_1344/frame_005100_arm9_ram.bin')


def apply_fixture(arm,raw,request):
    source = inspect.getsource(previous.apply_fixture)
    old = "    point = list(struct.unpack('<2i',cpu.mem_read(0x02460000,8)))"
    new = old+"""
    cached_point = point
    report_path = REFERENCE.parent/'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256']=='9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b'
    assert report['frames']==5400 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    capture = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==5100)
    loaded_raw = REFERENCE.read_bytes()
    assert previous.sha(loaded_raw)==capture['sha256']
    loaded_cpu,loaded_get = get_machine(arm,loaded_raw)
    loaded_fleet = loaded_get(0xCB1A8)+4+5*132
    assert loaded_get(0x35320,loaded_fleet)==5 and loaded_get(0x7EE08,loaded_get(0x3697C,loaded_fleet))==29
    loaded_mobile = loaded_get(0x36C70,loaded_fleet+12)
    assert loaded_mobile and loaded_get(0x564C8,loaded_mobile)
    fixed_point = struct.unpack('<2i',loaded_cpu.mem_read(loaded_mobile+16,8))
    point = [v//128 for v in fixed_point]
    assert point==[21176,3416]
"""
    assert source.count(old)==1
    source = source.replace(old,new)
    old = "'original_enemy_cached_map_point':point"
    new = "'current_offscreen_enemy_cached_map_point':cached_point,'prior_actual_loaded_enemy_map_point':point,'actual_position_reference':str(REFERENCE),'actual_position_reference_sha256':previous.sha(loaded_raw)"
    assert source.count(old)==1
    source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'REFERENCE':REFERENCE,'previous':previous}
    exec(compile(source,__file__,'exec'),env)
    return env['apply_fixture'](arm,raw,request)


if __name__=='__main__':
    assert not ROOT.exists()
    arm = previous.NdsImage.open(previous.ROM).read_file('/__arm9__.bin')
    raw = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1350_1344/frame_004800_arm9_ram.bin').read_bytes()
    after,receipt = apply_fixture(arm,raw,{'ship_sinking_context':'five_ship_approach'})
    ROOT.mkdir(parents=True)
    save(ROOT/'prebattle_fixture_preflight.json',receipt)
    print('Actual loaded target position source-bound;only40 own position bytes owned;all health/crew/roles/enemy/RNG/results exact.',flush=True)
