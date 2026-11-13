"""Source-bounded late condition tag after the original Deck UI has stopped world updates."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_physical_fatigue_fixture_v963 as initial
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
CASES=initial.CASES


def assign(arm,raw,request):
    if isinstance(request,str):return initial.assign(arm,raw,request)
    assert set(request)=={'case','late_condition_only'} and request['late_condition_only'] is True
    label=request['case'];assert label in CASES and len(raw)==0x400000
    assert sha(arm)==read('translations/physical_fatigue_editorial_release_v1.json')['target_arm9_sha256']
    assert arm[0x7E100:0x7E108]==bytes.fromhex('0600d0e51eff2fe1')
    cpu,get=get_machine(arm,raw);actor,role=CASES[label];hero=get(0x7F244);assert hero==1
    controller=get(0xCB1A8)+0x2090;assert get(0x82BC4,controller,12)==actor and get(0x81F54,controller,actor)==role==2
    matches=[];at=raw.find(struct.pack('<I',0x021314E8))
    while at>=0:
        parent=at-0x2194
        if parent>=0 and struct.unpack_from('<I',raw,parent)[0]==0x02130EF0:matches.append((at,parent))
        at=raw.find(struct.pack('<I',0x021314E8),at+4)
    assert len(matches)==1 and rtti(raw,0x02130EF0)=='18CDeckPersonnelView'
    actors=get(0xCB184);obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor==hero else actors+4+actor*32
    condition=get(0x7E100,obj);assert condition in (0,1)
    before=raw[obj-BASE:obj-BASE+32];after=bytearray(raw);after[obj-BASE+6]=1
    changes=[{'address':obj+6,'before':condition,'after':1}] if condition!=1 else []
    assert sum(a!=b for a,b in zip(raw,after,strict=True))==len(changes)
    assert bytes(after[obj-BASE:obj-BASE+32])==before[:6]+b'\x01'+before[7:]
    check,verify=get_machine(arm,bytes(after));assert verify(0x7E100,obj)==1
    return bytes(after),{'synthetic_physical_fatigue_late_condition_fixture':True,'case':label,'actor_ID':actor,
        'source_condition':condition,'fixture_condition':1,'condition_address':obj+6,'changes':changes,
        'original_Deck_parent':BASE+matches[0][1],'original_Cabin_child':BASE+matches[0][0],
        'room_assignment_already_present_not_reapplied':True,'only_condition_byte6_changes_all_other4MiB_exact':True,
        'other31_actor_bytes_and_actor_captain_identity_exact':True,'native_code_and_dialogue_not_changed':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(bytes(after)),'fixture_sha256':sha(Path(__file__).read_bytes()),
        'no_earned_fatigue_or_recovery_claim':True}
