"""Bounded coordinate-follow pilot; never inject dialogue, flags, or outcomes."""
import json
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import save


class CloseCommands:
    def __init__(self,journal,cap,root,case):
        self.stream=journal.open('r',encoding='utf-8')
        self.journal,self.cap,self.root,self.case=journal,cap,root,case
        self.arm=NdsImage.open('out/all_routes_combined_v1086_candidate.nds').read_file('/__arm9__.bin')
        self.owner=struct.unpack_from('<I',self.arm,0x552A0)[0]
        self.current=5410
        self.records=[]
        self.initial=False
        self.hold_done=False

    def readline(self,*args):
        line=self.stream.readline()
        if line:return line
        if self.hold_done:
            command={'stop':True}
        elif not self.initial:
            self.initial=True
            command={'until':5411,'duration':1,'battle_fixture':{'sighting_context':self.case}}
            self.current=5411
        else:
            raw=(self.cap/f'frame_{self.current:06d}_arm9_ram.bin').read_bytes()
            cpu,get=get_machine(self.arm,raw);root=get(0xCB1A8)
            own,enemy=root+4+132,root+4+28*132
            own_point=list(struct.unpack('<2i',cpu.mem_read(own+0x34,8)))
            target=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
            seen=bool(cpu.mem_read(enemy+0x50,1)[0]&4)
            template=cstring(raw,self.owner+0x2030)
            baseline=b' %s/%s\n  %s\n  Departed %s.'
            state=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))
            self.records.append({'frame':self.current,'own_point':own_point,'enemy_point':target,
                'first_sighting_seen':seen,'template_hex':template.hex(),'state':state,
                'groups_hex':bytes(cpu.mem_read(root+0x2080,16)).hex()})
            if seen or template!=baseline or self.current>=5531:
                command={'until':self.current+100,'duration':1}
                self.hold_done=True
                save(self.root/'bounded_follow_observations.json',{
                    'records':self.records,'stop_reason':'original-selection-or-seen' if seen or template!=baseline else 'bounded120-step-limit',
                    'no_dismissal_or_battle_outcome_input':True,'no_completion_claim':True})
            else:
                # Offset cycles explore only the existing close-bearing square.
                # Original motion/selection is allowed to run after every step.
                offsets=((0,0),(0,-2),(0,2),(-2,0),(2,0))
                dx,dy=offsets[(self.current-5411)%len(offsets)]
                point=[target[0]+dx,target[1]+dy]
                command={'until':self.current+1,'duration':1,
                    'battle_fixture':{'sighting_context':'followUnseen28','own_point':point}}
            self.current=command['until']
        with self.journal.open('a',encoding='utf-8') as out:out.write(json.dumps(command)+'\n')
        line=self.stream.readline()
        assert json.loads(line)==command
        return line

    def isatty(self):return False
    def close(self):self.stream.close()
