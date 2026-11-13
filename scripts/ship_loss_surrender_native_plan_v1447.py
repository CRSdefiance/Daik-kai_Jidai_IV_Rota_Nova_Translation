"""Repack all24 address-refined reports across the proven native22/23 boundary."""
import inspect
from pathlib import Path
from scripts import ship_loss_surrender_native_plan_v1444b as previous
from scripts.ship_loss_surrender_native_plan_v1444b import IDS,PROFILE,SOURCE_COMMON,SOURCE_ARM,compiled
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_loss_surrender_payload_v1447')
MANUSCRIPT = Path('translations/ship_loss_surrender_editorial_manuscript_v2.json')

def plan(common,arm,doc):
    source = inspect.getsource(previous.plan)
    anchor = "        ('=={22}','=={22,23}'),"
    assert source.count(anchor)==1
    source = source.replace(anchor,anchor+"\n        ('assert changed==[n for n in IDS if n!=2100]','assert changed==list(IDS)'),\n        ('all3645_unselected_or_retained_texts_and_native_copy_spans_preserved','all3644_unselected_texts_and_native_copy_spans_preserved'),")
    env = dict(previous.__dict__)
    exec(compile(source,__file__,'exec'),env)
    return env['plan'](common,arm,doc)

if __name__=='__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT);rom = NdsImage.open(doc['current_ROM'])
    c,a,proof = plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('24 revised loss/surrender templates repacked;3644 other texts/copies and all allocations preserved.',flush=True)
