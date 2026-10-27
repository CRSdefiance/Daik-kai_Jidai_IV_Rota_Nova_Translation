"""Read actual ship/room prerequisites and source model getters; no live edits."""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_town_fixture_v1290 import ROM, apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/town_artillery_v1296')


def main():
    assert not ROOT.exists()
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    source = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_town_v1291_1266/frame_005000_arm9_ram.bin')
    raw = source.read_bytes()
    after, receipt = apply_fixture(arm,raw,{'town_context':'SaoTomeFirstMate'})
    cpu,get = get_machine(arm,after)
    root,actors = get(0xCB1A8),get(0xCB184)
    duty = root+0x2090
    model = get(0x82E04,duty)
    rows = [{'slot':i,'native_room_type':get(0x132C0,model,i),'native_occupant_ID':get(0x82BC4,duty,i)} for i in range(31)]
    crew = []
    for index in [4,16,18,19,20,23]:
        obj = actors+4+index*32
        crew.append({'actor_ID':index,'native_company':get(0x7E958,obj),'condition':get(0x7E100,obj),
            'mood':get(0x7E0B4,obj),'current_duty_type':get(0x81F54,duty,index),'Gunnery_qualified':get(0x15DE4,index,8)})
    ROOT.mkdir(parents=True)
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for lo,hi in [(0x18180,0x18440),(0xAB8A0,0xAB940),(0x70400,0x705F8)]:
        assert arm[lo:hi] == clean[lo:hi]
        (ROOT/f'original_{lo:X}_{hi:X}.txt').write_text('\n'.join(f'{i.address:08X} {i.mnemonic} {i.op_str}'
            for i in md.disasm(clean[lo:hi],0x02000000+lo))+'\n',encoding='utf-8')
    mobile = get(0x36C70,root+4+132+12)
    ship = get(0xAB158,mobile)
    save(ROOT/'ship_and_crew.json',{'snapshot':str(source),'snapshot_sha256':sha(raw),'fixture_receipt':receipt,
        'rooms':rows,'existing_actor_prerequisites':crew,'actual_ship_model':ship,
        'ship_model_first144_hex':bytes(cpu.mem_read(ship,144)).hex(),'native_Hull_Crew_capacity':[get(0x183A0,ship),get(0x181BC,ship),get(0xAB18C,ship)],
        'source_model_getters_and_AI_code_equal_clean':True,'CPU_research_only_no_emulator_mutation':True,
        'no_new_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print(rows)
    print(crew)


if __name__ == '__main__':
    main()
