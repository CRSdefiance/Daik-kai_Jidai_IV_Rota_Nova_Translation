"""Reach original contact/boarding with a live low-HP captain; never force a shot."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ranged_staffing_v1050b import apply_fixture as staff
from scripts.native_ranged_training_v1056 import apply_fixture as train
from scripts.native_ranged_staffing_v1050b import water
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000


def apply_fixture(arm,raw,request):
    if request=={'reinforcement_context':'staffForContactBattle'}:
        after,receipt=staff(arm,raw,{'reinforcement_context':'staffForRangedBattle'});expected=51
    elif request=={'reinforcement_context':'trainContactAlive'}:
        after,receipt=train(arm,raw,{'reinforcement_context':'trainRangedAlive'});expected=30
    else:return staff(arm,raw,request)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x7E154,0x7E1A4),(0x737C8,0x74010),(0x65EEC,0x65F08)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,after);captain=get(0x65EEC)
    assert get(0x7F244)==1 and captain==get(0xCB184)+0x19E4
    hp=get(0x7E19C,captain);assert 0<hp<=144
    get(0x7E154,captain,30);assert get(0x7E19C,captain)==30
    fields={captain+0x18:struct.pack('<H',30)}
    contact=None
    if request=={'reinforcement_context':'trainContactAlive'}:
        root=get(0xCB1A8);own=root+4+132;enemy=root+4+8*132;mobile=get(0x36C70,own+12)
        point=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
        points=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,20),(20,0),(-20,0),(0,-20),(16,16),(-16,16))]
        terrain=water(arm,points);near=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
        fields[own+0x34]=struct.pack('<2i',*near);fields[mobile+16]=struct.pack('<2i',*[v*128 for v in near])
        contact={'original_enemy_point':point,'native_water_point':near,'terrain':terrain}
    result=bytearray(after);owned=set(receipt['owned_bytes'])
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result);assert len(owned)==expected
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    seed,flag=[struct.unpack_from('<I',arm,n)[0] for n in (0xD9858,0x51A20)]
    for at in (seed,flag):
        assert not set(range(at,at+4))&owned
        assert raw[at-BASE:at-BASE+4]==result[at-BASE:at-BASE+4]
    verify_cpu,verify=get_machine(arm,result)
    assert verify(0x7E19C,captain)==30 and verify(0x7F244)==1
    assert verify(0x8235C,verify(0xCB1A8)+0x2090,7,6,0)==166
    receipt.update(context=request['reinforcement_context'],owned_bytes=sorted(owned),changes=changes,
        original_live_captain_HP_setter=0x0207E154,own_captain_HP_before_after=[hp,30],
        own_captain_ID_unchanged=1,positive_HP_only_no_death_or_revival=True,
        original_duel_own_HP_greater_than30_predicate_false=True,
        original_contact_scan_and_shot_RNG2000_and_outcome_code_unchanged=True,
        contact_position=contact,extra_declared_captain_and_contact_fields={str(k):v.hex() for k,v in fields.items()},
        RNG_seed_and_initialization_flag_unchanged=True,
        fixture_sha256=sha(Path(__file__).read_bytes()),after_RAM_sha256=sha(result))
    # Parent receipts predate the explicit Luck/staffing/HP additions. Their
    # blanket noncoordinate-record claim is superseded by the full owned delta.
    for key in ('actor_identities_ownership_policies_and_all_noncoordinate_fields_unchanged',
                'regional_fleet_and_all_actor_identity_records_unchanged'):
        if key in receipt:receipt[key]=False
    receipt.update(actor_IDs_captain_ID_and_ownership_unchanged=True,
        declared_Luck_HP_staffing_and_supply_changes_supersede_parent_blanket_record_claims=True,
        all_bytes_outside_updated_owned_fields_exact=True)
    return result,receipt
