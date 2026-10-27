"""Current-runtime qualified Lookout/contact fixtures; preserve native shot chances."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_two_stage_sighting_v1786b import apply_fixture as approach, ROM
from scripts.native_close_follow_v1781 import water, BASE
from scripts.native_ranged_staffing_v1050b import install, delta
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lookout_contact_preflight_v1798b')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/two_stage_sighting_v1787_1775_twoStageReady8/frame_005503_arm9_ram.bin')


def apply_fixture(arm,raw,request):
    if 'sighting_context' in request:return approach(arm,raw,request)
    assert request in ({'lookout_contact':'qualify'}, {'lookout_contact':'maintain'})
    initial=request['lookout_contact']=='qualify'
    assert len(raw)==0x400000
    assert sha(arm)==read('translations/lil_lessons_editorial_release_v1.json')['required_runtime_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x732FC,0x74010),(0x7DCC8,0x7DE20),(0x7E154,0x7E1A4),
                  (0x7E750,0x7E7B4),(0x8235C,0x825E4),(0xAAF38,0xAAFB0),(0xAB158,0xAB1F0)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8);con=root+0x2090;actors=get(0xCB184)
    assert get(0x7F244)==get(0x2E58C)==1
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,1,8]
    own,enemy=[root+4+n*132 for n in (1,8)]
    assert get(0x35320,own)==2 and get(0x35320,enemy)==8
    mobiles=[get(0x36C70,f+12)for f in (own,enemy)]
    assert all(m and get(0x564C8,m)for m in mobiles),'Never revive disabled vessels'
    own_mobile,enemy_mobile=mobiles
    live=[[get(0x5543C,m),get(0x55444,m)]for m in mobiles]
    assert all(0<v<=bound for row,bounds in zip(live,((60,124),(60,163)),strict=True)for v,bound in zip(row,bounds,strict=True))
    captains=[get(0x65EEC),get(0x3697C,enemy)]
    assert captains==[actors+0x19E4,actors+4+32*32]
    hp=[get(0x7E19C,a)for a in captains];assert all(v>0 for v in hp),'Never revive dead captains'
    fields={}
    for a,value in zip(captains,(144,10),strict=True):
        get(0x7E154,a,value);fields[a+0x18]=bytes(cpu.mem_read(a+0x18,2))
    actor=actors+4+16*32
    assert get(0x7E958,actor)==2 and get(0x15DE4,16,1)==1 and get(0x7B60,7)==1
    level=get(0x7E728,actor);assert level==37
    if initial:
        assert get(0x82BC4,con,21)==16 and get(0x82BC4,con,3)==208
        assert (get(0x7DCC8,actor,6),cpu.mem_read(actor+13,1)[0])==(133,64)
        get(0x7E750,actor,5,36)
        assert get(0x7DCC8,actor,6)==166 and get(0x7E728,actor)==level
        fields.update({con+6+21:b'\xD0',con+6+3:bytes([16]),actor+13:bytes(cpu.mem_read(actor+13,1))})
    else:
        assert get(0x82BC4,con,3)==16 and get(0x82BC4,con,21)==208
        assert get(0x8235C,con,7,6,0)==166
    model=get(0xAB158,own_mobile)
    assert get(0x183A0,model)==60 and get(0xAB18C,model)==124
    if initial:
        assert get(0x181BC,model)==39
        get(0xAAF38,model,124);assert get(0x181BC,model)==124
        fields[model+0x44]=bytes(cpu.mem_read(model+0x44,2))
    else:assert get(0x181BC,model)==124
    vtable=struct.unpack('<I',cpu.mem_read(enemy_mobile,4))[0]
    getter=struct.unpack('<I',cpu.mem_read(vtable+0x5C,4))[0];assert getter==BASE+0x36A24
    scratch=0x02660100;get(getter-BASE,scratch,enemy_mobile)
    point=list(struct.unpack('<2i',cpu.mem_read(scratch,8)))
    terrain=water(arm,[point]);assert terrain['queries'][0]['collision_free']
    fixed=bytes(cpu.mem_read(enemy_mobile+16,8))
    fields.update({own+0x34:struct.pack('<2i',*point),own_mobile+16:fixed,
        own_mobile+24:struct.pack('<2H',60,124),enemy_mobile+24:struct.pack('<2H',60,163),
        model+0x3E:struct.pack('<2H',144,142)})
    result,owned=install(raw,fields);assert len(owned)==(37 if initial else 32)
    changes=delta(raw,result,owned)
    for at in [struct.unpack_from('<I',arm,n)[0]for n in (0xD9858,0x51A20)]+[enemy_mobile+13]:
        assert not set(range(at,at+(1 if at==enemy_mobile+13 else 4)))&owned
    verify_cpu,verify=get_machine(arm,result)
    assert verify(0x82478,con,7)==16 and verify(0x8235C,con,7,6,0)==166
    assert verify(0x7E728,actor)==37 and verify(0x78C60,1)==115
    assert [verify(0x7E19C,a)for a in captains]==[144,10]
    return result,{'context':request['lookout_contact'],'owned_bytes':sorted(owned),'changes':changes,
        'declared_fields':{str(k):v.hex()for k,v in fields.items()},'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),
        'original_positive_HP_before':hp,'original_live_Hull_Crew_before':live,
        'Lookout_actor_ID':16,'native_Aim_after':166,'unchanged_level':37,'native_Luck_method':BASE+0x7E750 if initial else None,
        'native_clamped_crew_method':BASE+0xAAF38 if initial else None,'native_live_position_getter':getter,
        'enemy_original_fixed_point_hex':fixed.hex(),'source_water_point':point,'terrain':terrain,
        'all_other4MiB_bytes_exact':True,'RNG_seed_initialization_cursor_and_enemy_result_byte_unchanged':True,
        'no_dead_captain_or_disabled_vessel_revived':True,'no_numeric_message_chance_branch_or_outcome_override':True,
        'synthetic_location_assignment_and_survival_fixture_not_earned_gameplay':True,
        'fixture_sha256':sha(Path(__file__).read_bytes())}


if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');raw=SNAP.read_bytes()
    assert sha(raw)==next(r['sha256']for r in read(SNAP.parent/'capture_report.json')['read_only_pause_RAM_snapshots']if r['frame']==5503)
    after,receipt=apply_fixture(arm,raw,{'lookout_contact':'qualify'})
    cpu,get=get_machine(arm,after);cursor=get(0xCB1B4)+8;actual=struct.unpack('<I',cpu.mem_read(cursor,4))[0]
    a,b=0x02660000,0x02660020;cases=[]
    for value in range(120):
        cpu.mem_write(cursor,struct.pack('<I',value));cpu.mem_write(a,bytes(16));cpu.mem_write(b,bytes(16))
        before=bytes(cpu.mem_read(BASE,0x400000));found=get(0x73694,a,b)
        own=list(struct.unpack('<4I',cpu.mem_read(a,16)));other=list(struct.unpack('<4I',cpu.mem_read(b,16)))
        assert bytes(cpu.mem_read(BASE,0x400000))==before
        cases.append({'offline_cursor':value,'native_contact_return':found,'own_contact':own,'other_contact':other,
            'original_flagship_pair':bool(found and own[2:]==[0,0]and other[2:]==[2,0]),'all4MiB_unchanged_by_original_query':True})
    assert sum(r['native_contact_return']!=0 for r in cases)==24
    assert sum(r['original_flagship_pair']for r in cases)==12
    save(ROOT/'current_contact_and_qualification_preflight.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_snapshot':str(SNAP),'source_snapshot_sha256':sha(raw),'actual_cursor_before_offline_cases':actual,
        'qualification_fixture':receipt,'all120_original_contact_cursor_cases':cases,
        'cursor_varied_only_in_disposable_offline_CPU_not_live_emulator':True,
        'no_shot_RNG_or_gameplay_execution_claim':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Current37-byte qualification and120 copied-state native contact cases pass;12 flagship pairs,24 contacts.',flush=True)
