"""Source-bounded late mood tag after the original Deck UI has stopped world updates."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_mood_comments_room_v982 as initial
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
CASES=initial.CASES
MOODS={'CamillePositive': 0, 'SeraPositive': 0, 'CarloDejected': 4, 'CaptainSilent': 4, 'CaptainPanic': 5, 'SeraPanic': 5}


def assign(arm,raw,request):
    if isinstance(request,str):return initial.assign(arm,raw,request)
    assert set(request)=={'case','late_mood_only'} and request['late_mood_only'] is True
    label=request['case'];assert label in CASES and len(raw)==0x400000;status=MOODS[label]
    assert sha(arm)==read('translations/mood_comments_editorial_release_v1.json')['target_arm9_sha256']
    assert arm[0x7E100:0x7E108]==bytes.fromhex('0600d0e51eff2fe1')
    assert arm[0x7E0B4:0x7E0BC]==bytes.fromhex('0700d0e51eff2fe1')
    cpu,get=get_machine(arm,raw);actor,role=CASES[label];hero=get(0x7F244);assert hero==1
    controller=get(0xCB1A8)+0x2090;assert get(0x82BC4,controller,12)==actor and get(0x81F54,controller,actor)==role==2
    matches=[];at=raw.find(struct.pack('<I',0x021314E8))
    while at>=0:
        parent=at-0x2194
        if parent>=0 and struct.unpack_from('<I',raw,parent)[0]==0x02130EF0:matches.append((at,parent))
        at=raw.find(struct.pack('<I',0x021314E8),at+4)
    assert len(matches)==1 and rtti(raw,0x02130EF0)=='18CDeckPersonnelView'
    actors=get(0xCB184);obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor==hero else actors+4+actor*32
    physical=get(0x7E100,obj);mood=get(0x7E0B4,obj);assert physical==0 and mood in (1,2,3)
    before=raw[obj-BASE:obj-BASE+32];after=bytearray(raw);after[obj-BASE+7]=status
    changes=[{'address':obj+7,'before':mood,'after':status}]
    assert sum(a!=b for a,b in zip(raw,after,strict=True))==len(changes)
    assert bytes(after[obj-BASE:obj-BASE+32])==before[:7]+bytes([status])+before[8:]
    check,verify=get_machine(arm,bytes(after));assert verify(0x7E0B4,obj)==status and verify(0x7E100,obj)==0
    return bytes(after),{'synthetic_mood_comments_late_mood_fixture':True,'case':label,'actor_ID':actor,
        'source_mood':mood,'fixture_mood':status,'mood_address':obj+7,'changes':changes,
        'original_Deck_parent':BASE+matches[0][1],'original_Cabin_child':BASE+matches[0][0],
        'room_assignment_already_present_not_reapplied':True,'only_mood_byte7_changes_all_other4MiB_including_physical_condition_exact':True,
        'other31_actor_bytes_and_actor_captain_identity_exact':True,'native_code_and_dialogue_not_changed':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(bytes(after)),'fixture_sha256':sha(Path(__file__).read_bytes()),
        'no_earned_mood_or_recovery_claim':True}
