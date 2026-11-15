"""Bounded Bridge room fixture;all actors,battle mode and resources retained."""

import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
CASES={'CaptainBridge':(1,5),'CaptainHelm':(1,4),'ClaudioMate':(5,6),'ManuelHelm':(23,4),'Voice7Helm19':(19,4)}


def assign(arm,raw,request):
    assert request in CASES and len(raw)==0x400000
    config=read('translations/battle_bridge_editorial_release_v1.json')
    assert sha(arm)==config['target_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a,b in ((0x12104,0x12920),(0x81F54,0x81FA0),(0x82BA8,0x82BD0),(0x132C0,0x132CC),(0x3F0F8,0x3F100)):
        assert arm[a:b]==clean[a:b]
    cpu,get=get_machine(arm,raw);actor,role=CASES[request];hero=get(0x7F244);assert hero==1
    context=get(0x3F0F8);actual_mode=list(struct.unpack('<2I',cpu.mem_read(context+8,8)))
    if request not in ('ClaudioMate','Voice7Helm19'):assert actual_mode==[0,1],actual_mode
    actors=get(0xCB184);obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor==hero else actors+4+actor*32
    condition,mood=get(0x7E100,obj),get(0x7E0B4,obj);assert condition==0 and mood in (1,2,3)
    faction=get(0x7E958,obj);company=get(0x397D8,get(0xCB160))
    controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller)
    occupants=[get(0x82BC4,controller,n) for n in range(31)]
    assert occupants[12]==208 and get(0x132C0,model,12)==12
    fields=[(model+0x1E+12,role)];old_slot=occupants.index(actor) if actor in occupants else None
    if old_slot is not None:
        get(0x82BA8,controller,old_slot);fields.append((controller+6+old_slot,208))
    get(0x82BB8,controller,12,actor);fields.append((controller+6+12,actor))
    cpu.mem_write(model+0x1E+12,bytes([role]));assert get(0x81F54,controller,actor)==role
    after=bytearray(raw);changes=[]
    for at,value in fields:
        before=after[at-BASE];assert before!=value
        after[at-BASE]=value;changes.append({'address':at,'before':before,'after':value})
    assert sum(a!=b for a,b in zip(raw,after,strict=True))==len(fields)
    return bytes(after),{'synthetic_battle_bridge_assignment_fixture':True,'case':request,'actor_ID':actor,
        'actual_captain_ID_preserved':hero,'role_type':role,'room_slot':12,'old_assignment_slot':old_slot,
        'original_actor_faction':faction,'player_company':company,'actor_owned_in_source_save':faction==company,
        'source_condition':condition,'source_mood':mood,'changes':changes,'source_actual_battle_fields8_12':actual_mode,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(bytes(after)),
        'all_other4MiB_RAM_including_battle_mode_actor_captain_health_money_calendar_RNG_text_code_exact':True,
        'no_earned_refit_assignment_or_recruitment_claim':True,'fixture_sha256':sha(Path(__file__).read_bytes())}
