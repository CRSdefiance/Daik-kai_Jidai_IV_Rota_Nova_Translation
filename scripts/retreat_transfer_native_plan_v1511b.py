"""Exact186-byte selector successor for the seven retreat paragraphs."""
from pathlib import Path
from types import FunctionType
from scripts import retreat_transfer_native_plan_v1511 as previous
from scripts import retreat_transfer_runtime_v1509b as runtime
from scripts.retreat_transfer_native_plan_v1511 import MANUSCRIPT,IDS,PROFILE,SOURCE_COMMON,SOURCE_ARM,compiled
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/retreat_transfer_payload_v1511b')

def plan(common,arm,doc):
    bound=FunctionType(previous.plan.__code__,{**previous.__dict__,'runtime':runtime},argdefs=previous.plan.__defaults__)
    return bound(common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);rom=NdsImage.open(doc['current_ROM'])
    c,a,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp=ROOT/'COMMON_RESEARCH_ONLY.DK4';ap=ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Retreat7 payload passes;3 revisions,3665 other/retained texts and40 blocks exact;186/188 selector bytes,172-byte gate/staged memory unchanged.')
