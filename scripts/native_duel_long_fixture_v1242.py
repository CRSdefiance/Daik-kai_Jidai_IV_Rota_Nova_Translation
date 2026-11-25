"""Longer disposable duel using source-valid health/luck attribute limits.

Pre-duel only: stamina/agility1, spirit/luck100 through native delta setter;
native HP limit and positive-health setter; shield49 retained in inventory.
Luck100 raises the original random chance to10 percent; it does not force it.
No actor ID,RNG word,eligibility flag,numeric message or result is injected.
"""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_duel_long_fixture_v1239 import apply_fixture as prior,ROM
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000


def apply_fixture(arm,raw,request):
    if request=={'sighting_context':'compassAttack8'}:
        return prior(arm,raw,request)
    after,parent=prior(arm,raw,request)
    cpu,get=get_machine(arm,after)
    root=get(0xCB184);actors=[root+0x19E4,root+4+32*32]
    assert [get(0x7EE08,a) for a in actors]==[1,32]
    owned=set(parent['owned_bytes']);fields=[]
    for actor in actors:
        assert get(0x7E19C,actor)>0
        before=[get(0x7E944,actor,i) for i in range(6)]
        for index,target in ((0,1),(1,1),(4,100),(5,100)):
            get(0x7E750,actor,index,target-before[index])
            assert get(0x7E944,actor,index)==target
            owned.add(actor+8+index)
        maximum=get(0x7DF58,actor,0,0)
        assert 0<maximum<=500
        get(0x7E154,actor,maximum)
        assert get(0x7E19C,actor)==maximum
        fields.append({'actor_ID':get(0x7EE08,actor),'attributes_before':before,
            'attributes_after':[get(0x7E944,actor,i) for i in range(6)],
            'positive_HP_and_native_maximum':[maximum,maximum],'fencing':get(0x7DCC8,actor,5)})
    native=bytes(cpu.mem_read(BASE,0x400000))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,native,strict=True)) if a!=b]
    assert all(r['address'] in owned for r in changes)
    for off in (0xD9858,0x51A20):
        at=struct.unpack_from('<I',arm,off)[0]
        assert not owned.intersection(range(at,at+4)) and raw[at-BASE:at-BASE+4]==native[at-BASE:at-BASE+4]
    return native,{'context':'longHealthLuckContact','owned_bytes':sorted(owned),'changes':changes,
        'parent_low_fencing_equipment_contact_receipt':parent,'native_pre_duel_attribute_changes':fields,
        'original_attribute_delta_setter':BASE+0x7E750,'original_positive_HP_setter':BASE+0x7E154,
        'original_unforced_special_random_chance_percent':10,
        'no_actor_ID_RNG_word_eligibility_flag_numeric_message_or_result_override':True,
        'no_healing_revival_relocation_or_ability_changes_during_or_after_duel':True,
        'only_disposable_prerequisites_not_earned_progression':True,
        'all_other4MiB_RAM_exact':True,'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(native),
        'fixture_sha256':sha(Path(__file__).read_bytes())}
