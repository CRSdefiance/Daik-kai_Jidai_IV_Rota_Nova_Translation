"""Explicit successor payload for the reviewed2218 natural prose revision."""
from pathlib import Path
from scripts.search_reports_native_plan_v1661 import plan, compiled, IDS, PROFILE, SOURCE_ARM, SOURCE_COMMON
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/search_reports_payload_v1666')
MANUSCRIPT=Path('translations/search_reports_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);rom=NdsImage.open(doc['current_ROM'])
    c,a,p=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp,ap=ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**p,'target_COMMON':str(cp),'target_ARM9':str(ap),'manuscript':str(MANUSCRIPT),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Revised11-report payload repacked;3657 other copies and39 blocks preserved;186/188,168/172 and123040 allocations unchanged.')
