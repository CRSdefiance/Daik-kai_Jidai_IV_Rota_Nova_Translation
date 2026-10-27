"""Original direct escape consumers preserve correct wrapping after block21 moves."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts import probe_escape_direct_source_v1186 as previous
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_escape_regression_v1203')


def main():
    assert not ROOT.exists()
    plan=read('work/analysis/duel_bark_native_v1201/native_payload_plan.json')
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    rom=NdsImage.open('out/all_routes_combined_v1189_candidate.nds');source=rom.read_file('/__arm9__.bin')
    patches=[]
    for at,size in [*plan['metadata_fields'],*plan['owned_ARM9_fields']]:
        patches.append({'address':0x02000000+at,'source_hex':source[at:at+size].hex(),'target_hex':arm[at:at+size].hex()})
    staging=Path('work/analysis/duel_bark_native_v1201/direct_escape_regression_plan.json');assert not staging.exists()
    save(staging,{'research_ARM9':plan['target_ARM9'],'target_ARM9_sha256':sha(arm),'patches':patches})
    rom.replace_file('/COMMON/MESFILE.DK4',common);rom.rom.arm9=arm
    class ExactTarget:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v1166_candidate.nds';return rom
    code=inspect.getsource(previous.main)
    old="assert b'\\n' in bytes.fromhex(seen['formatted_hex'])"
    assert code.count(old)==1;code=code.replace(old,"if len(candidates[0]['lines'])>1: assert b'\\n' in bytes.fromhex(seen['formatted_hex'])")
    env={**previous.__dict__,'__file__':__file__,'ROOT':ROOT,'PLAN':staging,'NdsImage':ExactTarget,
        'RAW':Path('E:/Rota Nova translations/Generated/work/emulation_v193/escape_direct_v1190_1189/frame_006902_arm9_ram.bin'),
        'current_entries':lambda c,a:owned_entries(c,a,plan['directory_sha256'])}
    exec(compile(code,__file__,'exec'),env);env['main']()
    print('All13 original direct escape pipelines still match their corrected complete font outputs.',flush=True)


if __name__=='__main__':main()
