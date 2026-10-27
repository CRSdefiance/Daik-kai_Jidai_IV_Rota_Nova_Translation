"""Closer original-terrain approach after the233-unit pilot never engaged."""
import inspect
from pathlib import Path
from scripts import native_combat_approach_fixture_v1463 as previous
from scripts.native_combat_approach_fixture_v1463 import ROM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/close_approach_fixture_v1467')

def apply_fixture(arm,raw,request):
    source = inspect.getsource(previous.apply_fixture)
    for old,new in [('[-200,120]','[-80,80]'),('[20976,3536]','[21096,3496]')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__}
    exec(compile(source,__file__,'exec'),env)
    result,receipt = env['apply_fixture'](arm,raw,request)
    receipt['context'] = 'five_ship_closer_southwest_approach_original_Carronade_escort_NoGun'
    receipt['earlier233_unit_approach_did_not_start_an_encounter'] = True
    receipt['point_adjustment_uses_fresh_prebattle_fixture_not_midrun_relocation'] = True
    return result,receipt

if __name__=='__main__':
    assert not ROOT.exists()
    cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/loss_surrender_control_v1461b_1456')
    report = read(cap/'capture_report.json');assert report['ROM_sha256']==sha(ROM.read_bytes())
    snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==4800)
    raw = Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    after,receipt = apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,{'ship_sinking_context':'five_ship_approach'})
    ROOT.mkdir(parents=True);save(ROOT/'prebattle_fixture_preflight.json',receipt)
    print('Closer water point [21096,3496],45 owned position/cannon bytes;all health,crew,enemy,RNG and result bytes unchanged.',flush=True)
