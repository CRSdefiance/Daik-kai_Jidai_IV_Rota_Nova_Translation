"""Record original A-bit mapping and queue ordinary, bounded timed inputs."""
from pathlib import Path
import json
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/duel_bark_inputs_v1209')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206')
JOURNAL=Path('work/analysis/duel_bark_live_v1207/navigation.jsonl')


def main():
    assert not ROOT.exists()
    rom=NdsImage.open('out/all_routes_combined_v1206_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    path=CAP/'frame_005903_arm9_ram.bin';raw=path.read_bytes();cpu,get=get_machine(arm,raw)
    bits=[i for i in range(18) if get(0xCF534,0x023120B4,i,0)]
    assert bits==[5] and struct.unpack('<I',cpu.mem_read(0x023120B8,4))[0]==32
    assert struct.unpack('<I',cpu.mem_read(0x0231230C,4))[0]==32
    rows=[json.loads(s) for s in JOURNAL.read_text(encoding='utf8').splitlines() if s]
    assert rows[-1]=={'until':5903,'buttons':['A'],'duration':1}
    presses=set(range(5946,6913,43))
    points=sorted({*range(5913,6914,20),*presses,6913})
    current=5903;commands=[]
    for target in points:
        assert target>current
        command={'until':target,'duration':1}
        if current in presses:command.update(buttons=['A'],duration=2)
        commands.append(command);current=target
    ROOT.mkdir(parents=True)
    save(ROOT/'physical_A_timing_plan.json',{'ROM_sha256':sha(Path('out/all_routes_combined_v1206_candidate.nds').read_bytes()),
        'original_A_bit5_snapshot':str(path),'snapshot_sha256':sha(raw),'original_query_CF534_source_bit':5,
        'ordinary_A1_at5902_is_the_only_captured_input_and_sets_exactly_bit5':True,
        'input_object_word':0x023120B8,'shared_input_word':0x0231230C,'captured_mask':32,
        'read_only_original_query_all18_keys':bits,'press_start_frames':sorted(presses),'commands':commands,
        'journal_before_sha256':sha(JOURNAL.read_bytes()),'only_physical_A_and_frame_advances_no_RAM_or_outcome_changes':True,
        'commands_are_intentions_not_execution_receipts':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    with JOURNAL.open('a',encoding='utf8') as stream:
        for command in commands:stream.write(json.dumps(command)+'\n')
    print(len(commands),'ordinary timing commands queued through6913;actual reactions require separate visible proof.',flush=True)


if __name__=='__main__':main()
