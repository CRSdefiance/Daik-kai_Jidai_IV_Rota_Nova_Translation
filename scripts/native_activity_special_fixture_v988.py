"""Disposable display fixtures:room assignment and original personnel UI event/selection fields."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
SPECS={'EmilioAfter':(14,1873,2,None),'FernandoAfter':(20,1876,2,None),
    'YifaBattle':(25,1885,1,None),'JulianBattle':(26,1886,1,None),
    'AzizaBattle0':(27,1887,1,0),'AzizaBattle4':(27,1888,1,4),
    'AlChapel':(17,1878,None,None),'YifaChapel':(25,1879,None,None),'YukihisaChapel':(12,1880,None,None)}
CASES={k:(v[0],18 if v[2] is None else 2) for k,v in SPECS.items()}

def assign(arm,raw,request):
    label=request if isinstance(request,str) else request['case']
    assert label in SPECS and len(raw)==0x400000
    late=not isinstance(request,str)
    if late:assert set(request)=={'case','late_case_only'} and request['late_case_only'] is True
    assert sha(arm)==read('translations/activity_special_editorial_release_v1.json')['target_arm9_sha256']
    cpu,get=get_machine(arm,raw);actor,number,activity,flag=SPECS[label];hero=get(0x7F244);assert hero==1
    context=get(0x3F0F8);assert list(struct.unpack('<2I',cpu.mem_read(context+8,8)))==[0,1]
    controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller);actors=get(0xCB184);obj=actors+4+actor*32
    assert get(0x7E100,obj)==0 and get(0x7E0B4,obj) in (1,2,3)
    fields={};parent=None
    if not late and activity is not None:
        occupants=[get(0x82BC4,controller,n) for n in range(31)]
        assert occupants[12]==208 and get(0x132C0,model,12)==12
        fields[model+0x1E+12]=bytes([2])
        if actor in occupants:fields[controller+6+occupants.index(actor)]=bytes([208])
        fields[controller+6+12]=bytes([actor])
    elif late:
        parents=[i for i in range(0,len(raw)-0x2198,4) if raw[i:i+4]==struct.pack('<I',0x02130EF0) and raw[i+0x2194:i+0x2198]==struct.pack('<I',0x021314E8)]
        assert len(parents)==1;parent=BASE+parents[0]
        assert rtti(raw,0x02130EF0)=='18CDeckPersonnelView'
        if activity is None:
            assert get(0x82BC4,controller,12)==208 and get(0x132C0,model,12)==12
            assert get(0x15DE4,actor,18)==0
            fields[model+0x1E+12]=bytes([18]);fields[parent+0x40]=struct.pack('<2I',actor,32)
        else:
            assert get(0x82BC4,controller,12)==actor and get(0x81F54,controller,actor)==2
            fields[parent+0x3A0]=struct.pack('<I',activity)
            fields[parent+0x39C]=struct.pack('<I',1);fields[parent+0x384]=struct.pack('<I',actor)
            if flag is not None:
                root=get(0xCB190);at=root+0x1A5;old=raw[at-BASE]
                fields[at]=bytes([(old&~4)|flag])
    after=bytearray(raw);allowed=set()
    for at,data in fields.items():
        after[at-BASE:at-BASE+len(data)]=data;allowed.update(range(at,at+len(data)))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(r['address'] in allowed for r in changes)
    verify_cpu,verify=get_machine(arm,bytes(after));assert verify(0x7F244)==hero
    assert bytes(after[obj-BASE:obj-BASE+32])==raw[obj-BASE:obj-BASE+32]
    assert bytes(after[actors+0x19E4-BASE:actors+0x19E4-BASE+32])==raw[actors+0x19E4-BASE:actors+0x19E4-BASE+32]
    return bytes(after),{'synthetic_activity_special_personnel_display_fixture':True,'case':label,'phase':'late' if late else 'room',
        'actor_ID':actor,'expected_message_ID':number,'activity_state_fixture':activity,'shared_object_bit2_fixture':flag,
        'modal_Chapel_refusal':activity is None,'parent':parent,'changes':changes,
        'declared_owned_fields':{str(k):v.hex() for k,v in fields.items()},
        'all_other4MiB_RAM_including_health_mood_battle_mode_money_and_native_text_code_exact':True,
        'actor_and_genuine_captain32_byte_records_unchanged':True,'source_actual_battle_fields8_12':[0,1],
        'no_earned_event_unlock_recruitment_or_assignment_claim':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(bytes(after)),'fixture_sha256':sha(Path(__file__).read_bytes())}
