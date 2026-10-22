"""Read-only cannon census and clean source damage mapping for the next pilot."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_cannon_setup_v1377')
ROM = Path('out/all_routes_combined_v1364_candidate.nds')
SNAPSHOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_gunnery_v1373_1364/frame_004800_arm9_ram.bin')
BASE = 0x02000000


def main():
    assert not ROOT.exists()
    release = read('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    raw = SNAPSHOT.read_bytes()
    spans = [(0x48180,0x481B4),(0x1856C,0x18574),(0x74538,0x74750),
        (0xA3A04,0xA3B1C),(0x750FC,0x751E0),(0x751E0,0x756FC),(0xAB71C,0xAB7AC)]
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.skipdata = True
    source = []
    for lo,hi in spans:
        assert arm[lo:hi]==clean[lo:hi]
        source.append({'span':[BASE+lo,BASE+hi],'sha256':sha(clean[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                for i in md.disasm(clean[lo:hi],BASE+lo)]})
    cpu,get = get_machine(arm,raw)
    root = get(0xCB1A8)
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,0,0]
    catalogue = []
    for identity in range(6):
        pointer = get(0x48180,identity)
        body = bytes(cpu.mem_read(pointer,19))
        assert body[17:]==clean[pointer-BASE+17:pointer-BASE+19]
        assert get(0xAB784,identity)==body[17]
        catalogue.append({'native_cannon_type':identity,'pointer':pointer,
            'current_label':body[:17].split(b'\0')[0].decode('cp932').rstrip(),
            'whole_current_catalogue_hex':body.hex(),'original_stats_exact':True,
            'native_strength':get(0xAB784,identity)})
    assert get(0xAB784,7)==0
    ships = []
    for slot in range(5):
        mobile = get(0x36C70,root+4+132+12+slot*8)
        model = get(0x36C94,root+4+132+12+slot*8)
        vt = struct.unpack('<I',cpu.mem_read(mobile,4))[0]
        getter = struct.unpack('<I',cpu.mem_read(vt+0x1C,4))[0]
        kind = get(getter-BASE,mobile)
        model_vt = struct.unpack('<I',cpu.mem_read(model,4))[0]
        assert struct.unpack('<I',cpu.mem_read(model_vt+0x1C,4))[0]==BASE+0x1856C
        assert get(0x1856C,model)==kind==raw[model+0x4A-BASE]
        multiplier = get(0xAB71C,mobile)
        strength = get(0xAB784,kind)
        shots = [(strength*multiplier+random_draw)//2//2 for random_draw in range(3)]
        ships.append({'slot':slot,'mobile':mobile,'model':model,'current_cannon_type':kind,
            'native_strength':strength,'native_battery_multiplier':multiplier,
            'native_type_field':model+0x4A,'native_mobile_getter':getter,
            'broadside_base_projectile_Hull_damage_for_all3_unforced_draw_values':shots,
            'actual_Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)]})
    assert [s['current_cannon_type'] for s in ships]==[1,0,0,0,0]
    assert [s['native_battery_multiplier'] for s in ships]==[4,1,1,1,1]
    assert catalogue[4]['current_label']=='Heavy Cannon' and catalogue[4]['native_strength']==5
    ROOT.mkdir(parents=True)
    save(ROOT/'source_cannon_setup.json',{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'snapshot':str(SNAPSHOT),'snapshot_sha256':sha(raw),'entire_original_code_spans':source,
        'source_native_catalogue':catalogue,'actual_prebattle_five_ship_cannons':ships,
        'native_NoGun_type7_strength_zero':True,
        'source_damage_contract':'Original74538 computes strength times battery multiplier for broadside,adds original RNG(3),halves,then original A3A04 halves again into projectile+24. Original750FC may add50percent critical damage through original RNG. Crew casualties use separate unforced RNG(6) at75588.',
        'next_prebattle_loadout':'Flagship original Heavy Cannon type4;four escorts original NoGun type7,so weak escort fire does not exhaust enemy crews before flagship hull damage. Only original gun-type model bytes plus the established prebattle location are proposed.',
        'theoretical_flagship_HeavyCannon_base_Hull_damage_per_shot':[5,5,5],
        'theory_not_a_gameplay_outcome_or_RNG_override':True,
        'all_reads_only_no_live_game_fixture_or_completion_credit':True,
        'no_enemy_health_crew_actor_identity_RNG_or_result_changes':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Source cannon census:flagship Culverin base2Hull,escorts Saker base0Hull;Heavy Cannon theory5Hull. No live changes or completion credit.',flush=True)


if __name__=='__main__':
    main()
