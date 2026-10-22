"""Pre-duel low-fencing fixture via original attribute and equipment routines.

Only disposable testing state: set both living duelists' stamina/agility to6,
clamp HP through the original maximum, and move shield49 into inventory.
Actor IDs, luck, special eligibility, RNG and result handling remain unchanged.
Never called during or after a duel; the parent enforces pre-duel contact.
"""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_duel_special_fixture_v1232 import apply_fixture as prior,ROM
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000


def apply_fixture(arm,raw,request):
    if request=={'sighting_context':'compassAttack8'}:
        return prior(arm,raw,request)
    assert request=={'duel_context':'healthyContact'}
    after,parent=prior(arm,raw,request)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x7DF58,0x7E1A4),(0x7E750,0x7E788),(0x7E944,0x7E950),
        (0x49DE8,0x49F30),(0x49F30,0x4A0F8),(0x4A5F4,0x4A628),(0x7DCC8,0x7DE20))
    for lo,hi in spans:assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,after)
    actors_root,fleets=get(0xCB184),get(0xCB1A8)
    actors=[actors_root+0x19E4,get(0x3697C,fleets+4+8*132)]
    assert [get(0x7EE08,a) for a in actors]==[1,32]
    owned=set(parent['owned_bytes']);attributes=[]
    for actor in actors:
        old=[get(0x7E944,actor,i) for i in range(6)]
        assert get(0x7E19C,actor)>0
        for index in (0,1):
            get(0x7E750,actor,index,6-old[index])
            assert get(0x7E944,actor,index)==6
            owned.add(actor+8+index)
        get(0x7E108,actor,0)
        assert get(0x7E19C,actor)==get(0x7DF58,actor,0,0)>0
        new=[get(0x7E944,actor,i) for i in range(6)]
        assert old[2:]==new[2:]
        attributes.append({'actor_ID':get(0x7EE08,actor),'before':old,'after':new,
            'HP_and_native_maximum':[get(0x7E19C,actor),get(0x7DF58,actor,0,0)]})
    slots=list(cpu.mem_read(actors[0]+0x1B,5))
    assert slots in ([219,49,219,219,219],[219]*5)
    transfer=None
    if slots[1]!=219:
        item=get(0xCB190)+4+49*20;scratch=0x02470020
        get(0x49DE8,scratch,item)
        assert struct.unpack('<2I',cpu.mem_read(scratch+4,8))==(2,1)
        get(0x4A610,scratch,0)
        assert get(0x49F30,item,scratch,6,0)==1
        get(0x49DE8,scratch,item)
        assert struct.unpack('<I',cpu.mem_read(scratch+4,4))[0]==0
        assert list(cpu.mem_read(actors[0]+0x1B,5))==[219]*5
        history=struct.unpack_from('<I',arm,0x4A0EC)[0]
        owned.update(range(actors[0]+0x1B,actors[0]+0x20))
        owned.update(range(item,item+20));owned.update(range(history,history+28))
        transfer={'item_ID':49,'owner_kind_before':2,'owner_actor_before':1,'owner_kind_after_inventory':0,
            'original_transfer':BASE+0x49F30,'item_not_deleted':True}
    fencing=[get(0x7DCC8,a,5) for a in actors]
    assert all(0<v<30 for v in fencing)
    native=bytes(cpu.mem_read(BASE,0x400000))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,native,strict=True)) if a!=b]
    assert all(r['address'] in owned for r in changes)
    for off in (0xD9858,0x51A20):
        at=struct.unpack_from('<I',arm,off)[0]
        assert not owned.intersection(range(at,at+4)) and raw[at-BASE:at-BASE+4]==native[at-BASE:at-BASE+4]
    return native,{'context':'lowFencingContact','owned_bytes':sorted(owned),'changes':changes,
        'parent_positive_health_and_contact_receipt':parent,'original_attribute_delta_setter':BASE+0x7E750,
        'original_HP_delta_clamp':BASE+0x7E108,'native_attribute_changes':attributes,
        'original_fencing_values_after_fixture':fencing,'native_shield_transfer':transfer,
        'only_disposable_pre_duel_ability_health_equipment_contact_state_not_earned_progression':True,
        'no_actor_ID_luck_RNG_eligibility_or_result_changes':True,
        'no_healing_revival_or_relocation_during_or_after_duel':True,
        'all_other4MiB_RAM_exact':True,'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(native),
        'fixture_sha256':sha(Path(__file__).read_bytes())}
