"""Pin six source-dispatched history inputs and ordinary capture commands."""

from pathlib import Path
import json

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_inn_history_fixture_v804 import set_condition
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/inn_history_v804')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=Path('out/all_routes_combined_v803_candidate.nds');arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    p=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inn_v803_stays/frame_003200_arm9_ram.bin');raw=p.read_bytes()
    cases=[]
    for event,won,months in (('fleet',True,10),('fleet',False,1),('raid',True,0),('raid',False,11),('town-defense',True,2),('town-defense',False,3)):
        request=dict(mode='Inn-history',event=event,won=won,months_ago=months)
        out,proof=set_condition(arm,raw,request)
        label=f'{event}_{"won" if won else "lost"}_{months}m'
        commands=[dict(until=3600,condition_fixture=request,touch=[20,80],duration=8)]
        commands += [dict(until=f,buttons=['A'],duration=8) for f in (4000,4400,4800,5200,5600,6000)]
        commands += [dict(until=6400,buttons=['B'],duration=8),dict(stop=True)]
        path=ROOT/(label+'_commands.jsonl')
        path.write_text(''.join(json.dumps(c)+'\n' for c in commands),encoding='utf-8')
        cases.append(dict(label=label,request=request,proof=proof,commands=str(path),commands_sha256=sha(path.read_bytes())))
    save(ROOT/'input_preflight.json',dict(candidate=str(rom),candidate_sha256=sha(rom.read_bytes()),
        source_RAM=str(p),source_RAM_sha256=sha(raw),cases=cases,
        producer_sha256=sha(Path(__file__).read_bytes()),fixture_sha256=sha(Path('scripts/native_inn_history_fixture_v804.py').read_bytes()),
        ROM_unchanged=True,actual_emulator_samples_pending=True,full_goal_complete=False))
    print('Six source-dispatched history inputs and capture schedules pinned;V803 unchanged.',flush=True)


if __name__=='__main__':main()
