"""Read-only snapshot inspections for the anchored firing replay."""
import argparse
from pathlib import Path
from types import FunctionType
from scripts import inspect_ship_sinking_live_v1374 as previous
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_anchor_v1383_1364')
ROOT = Path('work/analysis/ship_anchor_inspection_v1384')
inspect = FunctionType(previous.inspect.__code__,{**previous.__dict__,'CAP':CAP})


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('frames',type=int,nargs='+')
    args = parser.parse_args()
    assert sha(previous.ROM.read_bytes())=='dbf86d020cb868f443f9c6a9f68706e8cda28e9268ce0318a63ef765f4f3281c'
    arm = NdsImage.open(previous.ROM).read_file('/__arm9__.bin')
    ROOT.mkdir(parents=True,exist_ok=True)
    for frame in args.frames:
        result = inspect(frame,arm)
        target = ROOT/f'frame_{frame:06d}.json'
        assert not target.exists()
        save(target,{**result,'read_only_snapshot_inspection':True,'producer_sha256':sha(Path(__file__).read_bytes())})
        print(result,flush=True)
