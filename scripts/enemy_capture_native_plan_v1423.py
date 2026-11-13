"""Rebuild all eight refined capture clauses with exact scoped name protection."""
import inspect
from pathlib import Path
from types import FunctionType,SimpleNamespace
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import enemy_capture_native_plan_v1415 as prose
from scripts import enemy_capture_native_plan_v1419 as previous
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_payload_v1423')
MANUSCRIPT = Path('translations/enemy_capture_editorial_manuscript_v2.json')
IDS,PROFILE,SOURCE_COMMON,SOURCE_ARM = prose.IDS,prose.PROFILE,prose.SOURCE_COMMON,prose.SOURCE_ARM
compiled = prose.compiled

def prose_plan(common,arm,doc):
    source = inspect.getsource(prose.plan)
    for old,new in [
        ("('[2136,2137]','[2083,2086,2088]')","('[2136,2137]','list(IDS)')"),
        ('all3665_unselected_or_retained_texts_and_native_copy_spans_preserved','all3660_unselected_texts_and_native_copy_spans_preserved')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**prose.__dict__,'compiled':compiled}
    exec(compile(source,__file__,'exec'),env)
    return env['plan'](common,arm,doc)

def plan(common,arm,doc):
    bound = FunctionType(previous.plan.__code__,{**previous.__dict__,'prose':SimpleNamespace(plan=prose_plan)},argdefs=previous.plan.__defaults__)
    return bound(common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    c,a,proof = plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Eight refined capture messages rebuilt;all3660 other texts/copies and owned188/172/123040 byte allocations preserved.',flush=True)
