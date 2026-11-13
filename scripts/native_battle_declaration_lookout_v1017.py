"""Use a qualified Lookout for original identified-faction/readiness branches."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_battle_declaration_visible_v1012 import dispatch_fixture as prior
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000


def dispatch_fixture(arm,raw,request):
    after,receipt=prior(arm,raw,request)
    if not isinstance(request,dict) or request.get('declaration_context') not in ('KnownJanus','ReadyEmilio'):
        return after,receipt
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x705F8,0x706A4),(0x8205C,0x820D8),(0x82B30,0x82B38)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,after)
    controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller)
    assert get(0x7B60,7)==1 and get(0x15DE4,23,1)==1
    assert get(0x82B30,controller)!=7
    slots=[i for i in range(31) if get(0x132C0,model,i)==1]
    assert len(slots)==1
    fields={}
    for i in range(31):
        if get(0x82BC4,controller,i)==23:fields[controller+6+i]=b'\xD0'
    fields[controller+6+slots[0]]=bytes([23])
    result=bytearray(after);owned=set(receipt['owned_bytes'])
    for at,data in fields.items():
        result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result)
    verify_cpu,verify=get_machine(arm,result)
    assert verify(0x8205C,controller,1)==32 and verify(0x82478,controller,7)==23
    assert verify(0x82478,controller,1)==(4 if request['declaration_context']=='KnownJanus' else 14)
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    actors=get(0xCB184)
    for at in (actors+4+23*32,actors+0x19E4):assert raw[at-BASE:at-BASE+32]==result[at-BASE:at-BASE+32]
    receipt.update(owned_bytes=sorted(owned),changes=changes,after_RAM_sha256=sha(result),
        qualified_original_Lookout_actor_ID=23,Lookout_room_type=1,Lookout_room_slot=slots[0],
        original_8205C_no_empty_Lookout_result=32,original_role7_selector_actor=23,
        original_705F8_derives_identified_widget_flag_no_widget_injection=True,
        extra_Lookout_owned_fields={str(k):v.hex() for k,v in fields.items()},
        original_Lookout_actor_and_captain_identity_records_unchanged=True,
        Lookout_fixture_successor_sha256=sha(Path(__file__).read_bytes()))
    return result,receipt
