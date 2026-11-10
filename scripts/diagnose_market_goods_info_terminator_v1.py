"""Bind the reported build and execute the current native market printf without repairs."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import STACK

ROOT=Path('work/market_goods_info_terminator_20261109_v1')
USER=Path('out/all_routes_rafael2952_extended_checkpoint_v1_20261106_candidate.nds')
CURRENT=Path('work/maria301_release_v1/all_routes_maria301_candidate.nds')
SCREEN=Path('C:/Users/CHRISR~1.FRA/AppData/Local/Temp/codex-clipboard-399e6f42-28f3-431c-b209-36dc84ba8bc4.png')

def execute(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    output,name,category=0x02660020,0x02661020,0x02662020
    cpu.mem_write(name,b'Cheese\0');cpu.mem_write(category,b'Food\0')
    fmt=struct.unpack_from('<I',arm,0xC3EF8)[0]
    before=bytes(cpu.mem_read(0x02000000,0x400000))
    cpu.mem_write(output-16,b'\xa5'*544)
    cpu.mem_write(STACK,struct.pack('<I',101))
    call(cpu,0xD7720,(output,fmt,name,category),instruction_limit=1000000)
    value=bytes(cpu.mem_read(output,512)).split(b'\0')[0]
    assert len(value)<512
    assert bytes(cpu.mem_read(output-16,16))==bytes(cpu.mem_read(output+512,16))==b'\xa5'*16
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    assert value.startswith(b'Cheese\n  Food 101%') and value!=b'Cheese\n  Food 101%'
    return dict(output_hex=value.hex(),output_CP932=value.decode('cp932',errors='backslashreplace'),
        native_sprintf_andall_reached_helpers_executed_without_replacement=True,
        complete_return_andcallee_saved_ABI_output_canaries_andunowned4MiB_pass=True,
        format_pointer=fmt,extra_bytes_after_expected_percent=value[len(b'Cheese\n  Food 101%'):].hex())

def main():
    assert not ROOT.exists();ROOT.mkdir()
    screenshot=SCREEN.read_bytes();(ROOT/'user_screenshot.png').write_bytes(screenshot)
    rows=[]
    for role,path in [('user_reported_Rafael2952',USER),('current_registered_Maria301',CURRENT)]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');sections=MainCodeFile(arm,0x02000000).sections
        owner=next(s for s in sections if s.ramAddress==0x01FFC000)
        cases=[]
        for field in [0xC3EF8,0xC4074]:
            pointer=struct.unpack_from('<I',arm,field)[0];assert pointer==0x01FFC6A0
            data=bytes(owner.data);at=pointer-owner.ramAddress;end=data.index(0,at)
            fmt=data[at:end]
            assert fmt.startswith(b'%s\n  %s %d%%') and data[at+12]==0x0C
            assert fmt!=b'%s\n  %s %d%%'
            cases.append(dict(pointer_field=field,pointer=pointer,first_NUL_address=owner.ramAddress+end,
                actual_format_hex=fmt.hex(),expected_complete_terminated_format_hex=(b'%s\n  %s %d%%\0').hex(),
                required_NUL_address=0x01FFC6AC,actual_byte_at_required_NUL=data[0x6AC]))
        rows.append(dict(role=role,ROM=str(path),ROM_sha256=sha(path.read_bytes()),ARM9_sha256=sha(arm),cases=cases))
    assert rows[0]['cases']==rows[1]['cases']
    runtime=RegisteredRuntime('work/maria301_release_v1/registered_release_verification.json',
        'work/maria301_release_v1/own_registered_startup_verification.json',captain=3)
    native=runtime.execute(execute);runtime.calls.clear()
    save(ROOT/'diagnosis.json',dict(reported_screen='Market Trade / Goods Info / Cheese / Food101%',
        user_screenshot_sha256=sha(screenshot),source_user_ROM_name=USER.name,build_bindings=rows,
        native_reproduction=native,runtime=runtime.receipt(),
        source_collision=dict(market_template=0x01FFC6A0,required_terminator=0x01FFC6AC,
            later_town_stock_CAPTURE=0x01FFC6AC,town_stock_source='dk4tool/patch/town_stock_rows.py'),
        confirmed_missing_terminator_causes_native_read_into_machine_code=True,
        not_an_untranslated_Japanese_sentence=True,no_ROM_orrelease_registry_changes=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SCREEN,Path('dk4tool/patch/town_stock_rows.py'),
            Path('dk4tool/patch/commodity_ui_release.py'),Path('docs/commodity_integrated_v360_checkpoint.md'),Path(__file__)]}))
    print(native)
    print('Confirmedidentical missing-NUL/code overlap inuser Rafael2952 andcurrent registered Maria301;no ROM changes.')

if __name__=='__main__':main()
