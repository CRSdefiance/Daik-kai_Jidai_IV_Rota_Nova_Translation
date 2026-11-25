"""Keep ship and source fleet position fields consistent in a disposable fixture."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_battle_declaration_context_v1002 import assign as prior
from scripts.native_battle_declaration_standoff_v999 import apply_fixture as standoff
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000


def dispatch_fixture(arm,raw,request):
    if request=='approach':return standoff(arm,raw,request)
    assert isinstance(request,dict) and set(request)=={'declaration_context'}
    after,receipt=prior(arm,raw,request['declaration_context'])
    if request!={'declaration_context':'approachPasha'}:return after,receipt
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x2C1C4:0x2C1D8]==clean[0x2C1C4:0x2C1D8]
    cpu,get=get_machine(arm,raw)
    root=get(0xCB1A8);assert get(0x2E58C)==1
    fleet=root+4+0x84
    vt=struct.unpack('<I',cpu.mem_read(fleet,4))[0]
    fn=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
    assert fn==BASE+0x2C1C4
    get(fn-BASE,0x02460000,fleet)
    original=list(struct.unpack('<2i',cpu.mem_read(0x02460000,8)))
    water=receipt['source_verified_water_point']
    result=bytearray(after)
    result[fleet+0x34-BASE:fleet+0x3C-BASE]=struct.pack('<2i',*water)
    result=bytes(result)
    owned=set(receipt['owned_bytes'])|set(range(fleet+0x34,fleet+0x3C))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes) and len(owned)==16
    verify_cpu,verify=get_machine(arm,result)
    verify(fn-BASE,0x02460000,fleet)
    assert list(struct.unpack('<2i',verify_cpu.mem_read(0x02460000,8)))==water
    mobile=get(0x36C70,fleet+12)
    assert struct.unpack('<2i',verify_cpu.mem_read(mobile+16,8))==tuple(v*128 for v in water)
    assert verify(0x7F244)==1 and verify(0x2E58C)==1
    receipt.update(owned_bytes=sorted(owned),changes=changes,after_RAM_sha256=sha(result),
        original_cached_fleet_point=original,consistent_cached_fleet_point=water,
        cached_location_fields=[fleet+0x34,fleet+0x38],original_point_getter=fn,
        original_point_getter_exact_clean=True,
        all_other_RAM_bytes_exact=True,no_outcome_actor_identity_renderer_or_message_change=True,
        fixture_location_successor_sha256=sha(Path(__file__).read_bytes()))
    return result,receipt
