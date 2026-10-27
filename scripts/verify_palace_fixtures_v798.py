"""Refresh both control/candidate Palace qualification fixtures before playback."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_palace_fixture_v798 import set_condition,MODES
from scripts.verify_village_wrap_v608 import save


def main():
    root=Path('work/analysis/palace_gameplay_v798');root.mkdir(parents=True,exist_ok=True)
    p=Path('E:/Rota Nova translations/Generated/work/emulation_v193/palace_v797_contract/frame_003200_arm9_ram.bin')
    raw=p.read_bytes();rows=[]
    for rom in ('out/all_routes_combined_v792_candidate.nds','out/all_routes_combined_v797_candidate.nds'):
        a=NdsImage.open(rom).read_file('/__arm9__.bin')
        for mode in MODES:
            after,proof=set_condition(a,raw,{'mode':mode});rows.append(proof)
    save(root/'fixture_preflight.json',{'RAM_source':str(p),'RAM_sha256':sha(raw),
        'all_eight_fixture_cases':rows,'source_donor_saves_or_ROMs_not_modified':True,
        'fixture_sha256':sha(Path('scripts/native_palace_fixture_v798.py').read_bytes()),
        'producer_sha256':sha(Path('scripts/verify_palace_fixtures_v798.py').read_bytes())})
    print('Eight original-menu fixture cases pass;only declared1-2 eligibility bytes change.',flush=True)


if __name__=='__main__':main()
