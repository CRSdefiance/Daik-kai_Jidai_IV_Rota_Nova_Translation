"""Declared survival fixture for two live vessels; native critical RNG/result untouched."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ranged_staffing_v1050b import apply_fixture as prior
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
REFERENCE=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1051_1034_regional/frame_006130_arm9_ram.bin')


def apply_fixture(arm,raw,request):
    if request!={'reinforcement_context':'trainRangedAlive'}:return prior(arm,raw,request)
    assert sha(arm)==read('translations/reinforcement_sniping_editorial_release_v1.json')['target_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x519D4,0x51A28),(0xD9824,0xD9868),(0x73B18,0x73C10),
                  (0x81B78,0x81BD0),(0x17FE8,0x18034),(0x31990,0x319C0)):
        assert arm[lo:hi]==clean[lo:hi]
    reference=REFERENCE.read_bytes();assert len(reference)==0x400000
    source_report=read(REFERENCE.parent/'capture_report.json')
    record=next(r for r in source_report['read_only_pause_RAM_snapshots'] if r['frame']==6130)
    assert sha(reference)==record['sha256'] and source_report['frames']==8600
    baseline,get0=get_machine(arm,reference);r0=get0(0xCB1A8)
    enemy0=get0(0x36C70,r0+4+8*132+12);own0=get0(0x36C70,r0+4+132+12)
    model0=get0(0xAB158,own0)
    enemy_bounds=[get0(0x5543C,enemy0),get0(0x55444,enemy0)]
    provisions=list(struct.unpack('<2H',baseline.mem_read(model0+0x3E,4)))
    assert enemy_bounds==[60,163] and provisions==[144,142]
    after,receipt=prior(arm,raw,{'reinforcement_context':'recoverRangedOwn'})
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
    enemy=get(0x36C70,root+4+8*132+12);own=get(0x36C70,root+4+132+12);model=get(0xAB158,own)
    assert enemy and get(0x564C8,enemy)
    enemy_before=[get(0x5543C,enemy),get(0x55444,enemy)]
    assert all(0<v<=bound for v,bound in zip(enemy_before,enemy_bounds,strict=True))
    assert bytes(cpu.mem_read(model+8,24)).split(b'\0')[0]==b'Vestaros'
    fields={enemy+24:struct.pack('<2H',*enemy_bounds),model+0x3E:struct.pack('<2H',*provisions)}
    result=bytearray(after);owned=set(receipt['owned_bytes'])
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result);assert len(owned)==28
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    seed,flag=[struct.unpack_from('<I',arm,n)[0] for n in (0xD9858,0x51A20)]
    for at in (seed,flag):
        assert BASE<=at<BASE+len(raw)-4
        assert not set(range(at,at+4))&owned
        assert raw[at-BASE:at-BASE+4]==result[at-BASE:at-BASE+4]
    # The original successful-shot branch writes enemy+0Dh only after its
    # announcement returns. This result field is never owned by the fixture.
    assert enemy+13 not in owned and raw[enemy-BASE+13]==result[enemy-BASE+13]
    receipt.update(context='trainRangedAlive',owned_bytes=sorted(owned),changes=changes,
        training_enemy_live_Hull_Crew_before=enemy_before,training_enemy_observed_starting_bounds=enemy_bounds,
        training_own_provision_fields={str(model+0x3E):provisions},
        extra_declared_fields={str(k):v.hex() for k,v in fields.items()},
        enemy_and_other_fleet_stats_entirely_unchanged=False,
        only_enemy_live_Hull_Crew_restored_other_enemy_bytes_exact=True,
        enemy_result_byte0D_untouched=True,
        observed_reference=str(REFERENCE),observed_reference_sha256=sha(reference),
        RNG_seed_address=seed,RNG_initialization_flag_address=flag,
        entire_RNG_seed_and_initialization_flag_bytes_unchanged=True,
        no_disabled_or_dead_vessel_revived=True,
        no_numeric_message_RNG_or_battle_result_override=True,
        training_survival_fixture_not_earned_normal_battle_or_supplies=True,
        all_other4MiB_RAM_exact=True,fixture_sha256=sha(Path(__file__).read_bytes()),after_RAM_sha256=sha(result))
    return result,receipt
