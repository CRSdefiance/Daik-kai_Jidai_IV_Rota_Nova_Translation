"""Repack one optional no-argument notice;all native code stays exact."""
import inspect
from types import FunctionType
from pathlib import Path
from scripts import inspection_status_native_plan_v1573 as previous
from dk4tool.patch.hot_spring_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_notice_payload_v1632')
MANUSCRIPT=Path('translations/hot_spring_notice_editorial_manuscript_v1.json')
IDS=(310,)
PROFILE='hot-spring-experience-original-single-line-v1'
SOURCE_COMMON='3ac4a8a0309e02b601e633dab8e73491534c6d9498d9711756259fb2af166fd1'
SOURCE_ARM='0f7ba503189785238e6c27fee43b572c3288e25d9149846ceab8a66a1618bf5f'
compiled=FunctionType(previous.compiled.__code__,{**previous.__dict__,'IDS':IDS},argdefs=previous.compiled.__defaults__)
def plan(common,arm,doc):
    source=inspect.getsource(previous.plan).replace('all3666_unselected_texts_and_native_copy_spans_preserved','all3667_unselected_texts_and_native_copy_spans_preserved')
    env={**previous.__dict__,'SOURCE_COMMON':SOURCE_COMMON,'SOURCE_ARM':SOURCE_ARM,'IDS':IDS,'PROFILE':PROFILE,'current_entries':current_entries,'compiled':compiled}
    exec(compile(source,__file__,'exec'),env);return env['plan'](common,arm,doc)
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);rom=NdsImage.open(doc['current_ROM']);c,a,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp,ap=ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin';cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Notice310 repacked;3667 other text/copy spans,40 blocks,all native code/188 selector/172 gate/123040 staged bytes exact.')
