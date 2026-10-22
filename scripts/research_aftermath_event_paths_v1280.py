"""Original event caller census and existing town/defender prerequisite survey.

Queries a disposable CPU copy of an actual snapshot. No emulator fixture,
RNG result,event flag,actor ID or translation completion is supplied here.
"""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/aftermath_event_paths_v1280')
ROM = Path('out/all_routes_combined_v1266_candidate.nds')
RAW = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_navigation_v1281_1266/frame_003400_arm9_ram.bin')
BASE = 0x02000000


def main():
    assert not ROOT.exists()
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,original = rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == 'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'
    spans = ((0x717F8,0x71968),(0x71968,0x71A40),(0x72368,0x72BDC),(0x6ED34,0x6EE90),
        (0x513D0,0x514C0),(0xB3FD4,0xB4010),(0xB4AA8,0xB4AC0),(0xCD6B8,0xCD6CC))
    assert all(arm[lo:hi] == original[lo:hi] for lo,hi in spans)
    entries = (0x020717F8,0x02071968,0x02072368,0x0206ED34)
    callers = {str(t):[] for t in entries}
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for off in range(0,0x130000,4):
        word = struct.unpack_from('<I',original,off)[0]
        if word & 0x0F000000 != 0x0B000000:
            continue
        delta = word & 0xFFFFFF
        if delta & 0x800000:
            delta -= 0x1000000
        target = BASE+off+8+4*delta
        if target in entries:
            assert arm[off-28:off+8] == original[off-28:off+8]
            callers[str(target)].append({'source_call':BASE+off,
                'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                    for i in md.disasm(original[off-28:off+8],BASE+off-28)]})
    raw = RAW.read_bytes()
    assert len(raw) == 0x400000
    cpu,get = get_machine(arm,raw)
    actors,fleets,towns = get(0xCB184),get(0xCB1A8),get(0xCB178)
    assert get(0x7F244) == get(0x2E58C) == 1
    town_rows = []
    for index in range(114):
        town = towns+4+index*108
        vt = struct.unpack('<I',cpu.mem_read(town,4))[0]
        assert rtti(raw,vt) == '5CTown'
        name_ptr = get(struct.unpack('<I',cpu.mem_read(vt+8,4))[0]-BASE,town)
        name = bytes(cpu.mem_read(name_ptr,80)).split(b'\0')[0]
        port = get(0xCD6B8,index)
        point = list(struct.unpack('<2i',cpu.mem_read(port+12,8)))
        value = get(0xB3FD4,town,1)
        shares = [get(0xB4AA8,town,i) for i in range(20)]
        town_rows.append({'town_ID':index,'town_object':town,'native_name':name.decode('cp932'),
            'native_name_hex':name.hex(),'native_port_map_point':point,
            'source_B3FD4_parameter1_value':value,'all20_source_company_market_shares':shares})
    defenders = []
    for index in range(63):
        fleet = fleets+4+index*132
        vt = struct.unpack('<I',cpu.mem_read(fleet,4))[0]
        assert rtti(raw,vt) == '6CFleet'
        alive = get(struct.unpack('<I',cpu.mem_read(vt+0x10,4))[0]-BASE,fleet)
        if not alive:
            continue
        town_id = get(0x34674,fleet)
        company = get(0x35320,fleet)
        if not 0 <= town_id < 114 or company == 21:
            continue
        captain = get(0x3697C,fleet)
        share = get(0xB4AA8,towns+4+town_id*108,company)
        name_ptr = get(struct.unpack('<I',cpu.mem_read(vt+8,4))[0]-BASE,fleet)
        name = bytes(cpu.mem_read(name_ptr,96)).split(b'\0')[0].decode('cp932')
        defenders.append({'fleet_ID':index,'fleet_object':fleet,'original_fleet_name':name,
            'town_ID':town_id,'town_name':town_rows[town_id]['native_name'],
            'company_ID':company,'original_captain_actor_ID':get(0x7EE08,captain),
            'source_alive_virtual_query':alive,'source_market_share':share,
            'passes_city_defense_presence_and_positive_share_before_unforced_RNG':share > 0})
    ROOT.mkdir(parents=True)
    output = ROOT/'source_event_and_existing_prerequisites.json'
    save(output,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),
        'snapshot':str(RAW),'snapshot_sha256':sha(raw),'source_code_spans_exact_to_clean':spans,
        'original_direct_BL_callers':callers,'towns':town_rows,'existing_docked_alive_fleets':defenders,
        'zero_source_B3FD4_parameter1_towns':[r['town_ID'] for r in town_rows if r['source_B3FD4_parameter1_value'] == 0],
        'original_city_defender_RNG_requirement':'Original519D4(3)==0 after alive/presence/company/share checks;not evaluated or forced in this survey.',
        'original_ship_surrender_RNG_requirement':'72484 requires live Hull below half AB8F0 reference and live Crew below AB1C4 reference;original519D4(100) must not exceed50*(referenceCrew-liveCrew)/referenceCrew. No RNG call or flags supplied by this survey.',
        'withdrawal_coordinate_contract':'Original513D0 compares wrapped absolute x/y deltas against160 and320. Argument3 is optional distance-output pointer,not radius. Original7251C uses source town center for city battles and selected live flagship point for sea battles. Do not infer own sea withdrawal from distance to the enemy alone.',
        'CPU_query_copy_only_no_emulator_state_or_saved_file_mutation':True,
        'CPU_getters_left_all_input4MiB_bytes_exact':bytes(cpu.mem_read(BASE,0x400000)) == raw,
        'no_RNG_initialization_eligibility_result_or_actor_ID_edit':True,
        'source_and_formatting_completion_counts_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('114 source towns and'+str(len(defenders))+' existing docked fleet candidates surveyed;'+
        str(sum(r['source_B3FD4_parameter1_value'] == 0 for r in town_rows))+' zero-defense leads. No RNG/event or completion injection.',flush=True)


if __name__ == '__main__':
    main()
