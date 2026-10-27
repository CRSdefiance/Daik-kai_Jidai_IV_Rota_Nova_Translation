"""Bounded current-run one-frame placement; original game selects any dialogue."""
import json
import struct
import time
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_close_sighting_v1689 import ROM, apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import save

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/close_sighting_v1690_1676_closeReady8')
ROOT=Path('work/analysis/close_sighting_follow_v1692')
JOURNAL=Path('work/analysis/close_sighting_v1690_closeReady8/navigation.jsonl')


if __name__=='__main__':
    assert not ROOT.exists()
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    frame=5310
    assert json.loads(JOURNAL.read_text(encoding='utf-8').splitlines()[-1])['until']==frame
    ROOT.mkdir(parents=True)
    owner=struct.unpack_from('<I',arm,0x552A0)[0]
    observations=[]
    for step in range(33):
        path=CAP/f'frame_{frame:06d}_arm9_ram.bin'
        deadline=time.monotonic()+45
        while not path.exists() or path.stat().st_size!=0x400000:
            assert time.monotonic()<deadline,('capture observation timeout;emulator state not inferred terminal',frame)
            time.sleep(.1)
        raw=path.read_bytes();cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
        own,enemy=root+4+132,root+4+8*132
        template=cstring(raw,owner+0x2030)
        seen=bool(cpu.mem_read(enemy+0x50,1)[0]&4)
        row={'frame':frame,'RAM_sha256':sha(raw),'own_point':list(struct.unpack('<2i',cpu.mem_read(own+0x34,8))),
             'enemy_point':list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8))),'seen_flag':seen,
             'loaded_groups':list(cpu.mem_read(root+0x2080,16)),'template_hex':template.hex()}
        observations.append(row)
        stop=seen or template!=b' %s/%s\n  %s\n  Departed %s.' or step==32
        if stop:
            reason='original_sighting_or_changed_selection' if step<32 else 'bounded32-step-limit'
            command={'until':frame+100,'duration':1}
        else:
            after,proof=apply_fixture(arm,raw,{'sighting_context':'closeReady8'})
            assert len(proof['owned_bytes'])==17
            row['replayed_fixture']=proof
            command={'until':frame+1,'duration':1,'battle_fixture':{'sighting_context':'closeReady8'}}
        with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')
        save(ROOT/'observations.json',{'observations':observations,'no_completion_credit':True,
             'no_enemy_seen_flag_actor_RNG_or_outcome_injection':True,'producer_sha256':sha(Path(__file__).read_bytes())})
        print({'frame':frame,'seen':seen,'groups':row['loaded_groups'],'template':template.decode('cp932')},flush=True)
        frame=command['until']
        if stop:
            save(ROOT/'stop_reason.json',{'reason':reason,'observed_frame':row['frame'],'requested_hold':frame,
                                       'no_target_UI_claim_without_separate_verification':True})
            break
