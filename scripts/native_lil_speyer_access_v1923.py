"""Focused Hamburg access:16 coordinate bytes and4 declared synthetic funds bytes."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_lil_london_location_v1883 import apply_fixture as previous
from scripts.native_lil_london_location_v1883 import REQUEST as LONDON
from scripts.native_lil_Bruges_location_v1754 import REQUEST as BRUGES
from scripts.native_lil_Amsterdam_location_v1833c import REQUEST as AMSTERDAM
from scripts.native_lil_Bruges_location_v1752c import source_bound_terrain
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Speyer_access_v1923')
REQUEST = {'Lil_Speyer_Hamburg_access':'coherent_location_and_declared60000_funds'}
BASE = 0x02000000

def apply_fixture(arm,raw,request):
    if request in (BRUGES,AMSTERDAM,LONDON):return previous(arm,raw,request)
    if request != REQUEST or len(raw) != 0x400000:
        raise ValueError('Speyer access requires exact declared request and4MiB state')
    if sha(arm) != '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e':
        raise ValueError('Speyer access requires exact V1909 runtime')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x78C60,0x78E80),(0xB566C,0xB5688),(0xB521C,0xB5230),(0x69B5C,0x69E00),
        (0x3CC80,0x3CCD0),(0x397D8,0x397E0)]
    assert all(arm[a:b] == source[a:b] for a,b in spans)
    threshold = read('work/analysis/lil_Speyer_threshold_v1919/original_event128_fifty_thousand_cash_boundary.json')
    assert threshold['required_cash'] == 50000
    assert [(r['offline_funds'],r['full_original_predicate_result']) for r in threshold['cases']] == [(34882,0),(49999,0),(50000,1),(50001,1)]
    cpu,get = get_machine(arm,raw)
    assert get(0x2E58C) == get(0x7F244) == 2
    fleet = get(0xCB1A8)+4+2*132
    assert get(0x34674,fleet) == 115
    table = get(0xCB160)
    own = get(0x397D8,table)
    assert own == 1
    company = table+4+own*76
    funds = get(0x3CCC8,company)
    assert 0 < funds < 50000
    town = get(0xCB178)+4+5*108
    assert get(0xB5600,town) == 5 and get(0xB521C,town) == 1
    known = get(0xB50D8,town)
    get(0xB566C,0x02640000,town)
    top = list(struct.unpack('<2i',cpu.mem_read(0x02640000,8)))
    center = [v+24 for v in top]
    offsets = sorted([(dx,dy)for dx in range(-40,41,8)for dy in range(-40,41,8)if dx*dx+dy*dy<=40**2],
        key=lambda xy:(xy[0]**2+xy[1]**2,xy))
    terrain = source_bound_terrain(arm,[[center[0]+dx,center[1]+dy] for dx,dy in offsets])
    target = next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    # Apply the original funds method on a disposable copy. It must own only
    # CForce+0Ch; the live frontend receives the independently audited final delta.
    assert bytes(cpu.mem_read(BASE,0x400000)) == raw
    get(0x3CC80,company,60000-funds)
    funded = bytes(cpu.mem_read(BASE,0x400000))
    fund_changes = [dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,funded,strict=True)) if a!=b]
    assert get(0x3CCC8,company) == 60000
    assert all(r['address'] in range(company+12,company+16) for r in fund_changes)
    owned = {*range(fleet+0x34,fleet+0x3C),*range(company+12,company+16)}
    after = bytearray(funded)
    struct.pack_into('<2i',after,fleet+0x34-BASE,*target)
    mobiles = []
    for slot in range(5):
        mobile = get(0x36C70,fleet+12+slot*8)
        if not mobile:continue
        assert struct.unpack('<I',cpu.mem_read(mobile,4))[0] == 0x02143A80
        owned.update(range(mobile+16,mobile+24))
        prior = list(struct.unpack('<2i',cpu.mem_read(mobile+16,8)))
        struct.pack_into('<2i',after,mobile+16-BASE,*[v*128 for v in target])
        mobiles.append(dict(slot=slot,mobile=mobile,prior_fixed_point=prior,target_fixed_point=[v*128 for v in target]))
    assert len(mobiles) == 1 and len(owned) == 20
    after = bytes(after)
    changes = [dict(address=BASE+i,before=a,after=b)for i,(a,b)in enumerate(zip(raw,after,strict=True))if a!=b]
    assert all(r['address'] in owned for r in changes)
    check,query = get_machine(arm,after)
    assert query(0x34674,fleet) == 115 and query(0xB50D8,town) == known
    assert query(0x397D8,table) == 1 and query(0x3CCC8,company) == 60000
    assert bytes(check.mem_read(BASE,0x400000)) == after
    return after,dict(fixture='Lil_Speyer_Hamburg_coordinate_and_synthetic_funds_access',
        owned_bytes=sorted(owned),changes=changes,fleet=fleet,mobiles=mobiles,
        target_map_point=target,original_town_top_left=top,native_center=center,source_water_queries=terrain,
        original_Hamburg_known_flag_before=known,original_Hamburg_known_flag_after=known,
        original_town_sentinel115_unchanged=True,company_ID=own,company_pointer=company,
        before_funds=funds,synthetic_funds=60000,original_money_method=BASE+0x3CC80,funds_field=company+12,
        original_event128_funds_threshold=50000,ten_thousand_margin_for_normal_town_costs=True,
        threshold_proof='work/analysis/lil_Speyer_threshold_v1919/original_event128_fifty_thousand_cash_boundary.json',
        threshold_proof_sha256=sha(Path('work/analysis/lil_Speyer_threshold_v1919/original_event128_fifty_thousand_cash_boundary.json').read_bytes()),
        all_other4MiB_exact=True,only16_coordinates_and4_company_funds_bytes_owned=True,
        no_event_RNG_health_inventory_actor_message_branch_or_outcome_ownership=True,
        earned_travel_and_earned_wealth_not_claimed=True,normal_docking_town_action_and_original_event_activation_required=True,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(after),fixture_sha256=sha(Path(__file__).read_bytes()))

if __name__ == '__main__':
    assert not ROOT.exists()
    snap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_revised_run_v1903_RESEARCH_ONLY/frame_048810_arm9_ram.bin')
    arm = NdsImage.open('out/all_routes_combined_v1909_candidate.nds').read_file('/__arm9__.bin')
    raw = snap.read_bytes()
    after,proof = apply_fixture(arm,raw,REQUEST)
    negative = []
    for label,badarm,badraw,request in [('unknown-request',arm,raw,{}),('short-state',arm,raw[:-1],REQUEST),
        ('wrong-runtime',bytes([arm[0]^1])+arm[1:],raw,REQUEST)]:
        try:apply_fixture(badarm,badraw,request)
        except (ValueError,AssertionError) as error:negative.append(dict(case=label,error=str(error)))
        else:raise AssertionError('Invalid fixture input accepted')
    ROOT.mkdir(parents=True)
    save(ROOT/'twenty_byte_access_preflight.json',dict(**proof,snapshot=str(snap),snapshot_sha256=sha(raw),
        negative_controls=negative,no_live_fixture_applied_by_preflight=True))
    print(dict(owned_bytes=len(proof['owned_bytes']),target=proof['target_map_point'],before_funds=proof['before_funds'],
        synthetic_funds=60000,known_flag_preserved=proof['original_Hamburg_known_flag_before'],negative_controls=len(negative)))
