"""Disclosed live-health/contact fixture; original shot RNG and outcome stay native."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ranged_staffing_v1050b import apply_fixture as staff, water, install, delta, guarded
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def apply_fixture(arm,raw,request):
    initial=request=={'reinforcement_context':'staffHealthyContact'}
    training=request=={'reinforcement_context':'trainHealthyContact'}
    if not (initial or training):return staff(arm,raw,request)
    guarded(arm,raw)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x7E154,0x7E1A4),(0x737C8,0x74010),(0x36A24,0x36A68),(0xD9824,0xD9868)):
        assert arm[lo:hi]==clean[lo:hi]
    if initial:after,parent=staff(arm,raw,{'reinforcement_context':'staffForRangedBattle'})
    else:after,parent=raw,None
    cpu,get=get_machine(arm,after);root=get(0xCB1A8)
    own,enemy=[root+4+n*132 for n in (1,8)]
    assert get(0x7F244)==get(0x2E58C)==1 and get(0x35320,own)==2 and get(0x35320,enemy)==8
    own_mobile,enemy_mobile=[get(0x36C70,f+12) for f in (own,enemy)]
    assert own_mobile and enemy_mobile and get(0x564C8,own_mobile) and get(0x564C8,enemy_mobile)
    captain,opponent=get(0x65EEC),get(0x3697C,enemy)
    assert captain==get(0xCB184)+0x19E4 and opponent==get(0xCB184)+4+32*32
    hp=[get(0x7E19C,a) for a in (captain,opponent)]
    assert all(v>0 for v in hp),'Never revive a dead captain'
    # Both values are positive source-native health preconditions, not result flags.
    get(0x7E154,captain,144);get(0x7E154,opponent,10)
    fields={captain+0x18:struct.pack('<H',144),opponent+0x18:struct.pack('<H',10)}
    contact=None;live=None
    if training:
        assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,1,8]
        live=[[get(0x5543C,m),get(0x55444,m)] for m in (own_mobile,enemy_mobile)]
        assert all(0<v<=bound for row,bounds in zip(live,((60,124),(60,163)),strict=True) for v,bound in zip(row,bounds,strict=True))
        model=get(0xAB158,own_mobile)
        assert (get(0x183A0,model),get(0x181BC,model))==(60,124)
        vtable=struct.unpack('<I',cpu.mem_read(enemy_mobile,4))[0]
        getter=struct.unpack('<I',cpu.mem_read(vtable+0x5C,4))[0]
        assert getter==BASE+0x36A24
        scratch=0x02470000;get(getter-BASE,scratch,enemy_mobile)
        point=list(struct.unpack('<2i',cpu.mem_read(scratch,8)))
        terrain=water(arm,[point]);assert terrain['queries'][0]['collision_free']
        # Copy the exact live fixed point, avoiding cached-coordinate drift/rounding.
        fixed=bytes(cpu.mem_read(enemy_mobile+16,8))
        fields.update({own+0x34:struct.pack('<2i',*point),own_mobile+16:fixed,
            own_mobile+24:struct.pack('<2H',60,124),enemy_mobile+24:struct.pack('<2H',60,163),
            model+0x3E:struct.pack('<2H',144,142)})
        contact={'native_live_point_getter':getter,'live_point':point,'exact_live_fixed_point_hex':fixed.hex(),
            'cached_enemy_point':list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8))),'terrain':terrain}
    result,extra=install(after,fields);owned=extra|set(parent['owned_bytes'] if parent else ())
    assert len(owned)==(53 if initial else 32)
    changes=delta(raw,result,owned)
    seed,flag=[struct.unpack_from('<I',arm,n)[0] for n in (0xD9858,0x51A20)]
    for at in (seed,flag):
        assert not set(range(at,at+4))&owned and raw[at-BASE:at-BASE+4]==result[at-BASE:at-BASE+4]
    assert enemy_mobile+13 not in owned and raw[enemy_mobile-BASE+13]==result[enemy_mobile-BASE+13]
    verify_cpu,verify=get_machine(arm,result)
    assert verify(0x7E19C,captain)==144 and verify(0x7E19C,opponent)==10
    assert verify(0x82478,root+0x2090,7)==16 and verify(0x8235C,root+0x2090,7,6,0)>150
    return result,{'context':request['reinforcement_context'],'owned_bytes':sorted(owned),'changes':changes,
        'parent_staffing_receipt':parent,'declared_fields':{str(k):v.hex() for k,v in fields.items()},
        'own_and_enemy_captain_HP_before':hp,'own_and_enemy_captain_HP_after':[144,10],
        'original_positive_HP_setter':BASE+0x7E154,'original_enemy_HP_greater_than30_duel_predicate_false':True,
        'contact_geometry':contact,'prior_live_Hull_Crew':live,
        'live_health_and_provisions_restored_to_observed_starting_bounds':training,
        'actor_IDs_ownership_and_names_unchanged':True,'all_other4MiB_RAM_exact':True,
        'no_dead_captain_or_disabled_vessel_revived':True,'enemy_result_byte0D_unchanged':True,
        'RNG_seed_and_initialization_flag_unchanged':True,
        'no_numeric_message_branch_patch_RNG_seed_or_outcome_injection':True,
        'synthetic_health_location_staffing_fixture_not_earned_gameplay':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}
