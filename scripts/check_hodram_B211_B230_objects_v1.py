"""Run the existing complete style and menu contracts for this exact batch."""
from copy import deepcopy
from pathlib import Path
import subprocess
import sys
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_hodram_B211_B230_formatting_v1 import FORMATTING
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'native_objects_v1'
PLAN=ROOT/'formatting_v1/initial_plan/automatic_plans.json'
RELEASE=Path('work/rafael5186_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v3/own_route_context.json'

def main():
    assert not OUT.exists();OUT.mkdir()
    source=checked_text(Path('scripts/check_editorial_style_objects.py').read_text(encoding='utf-8'),{
        "assert len(objects)==8 and cases==64 and sum(len(o['physical_record_IDs']) for o in objects)==48":
            "assert len(objects)==4 and cases==32 and sum(len(o['physical_record_IDs']) for o in objects)==29",
        'physical_alternatives=48,':'physical_alternatives=29,',
        'PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks;':
            'PASS4 compiled4100 objects/29 physical alternatives/32 original target slot cases/36 semantic rejection checks;',
    })
    driver=OUT/'source_locked_style_driver.py';driver.write_text(source,encoding='utf-8')
    shared=['--release',str(RELEASE),'--startup',str(STARTUP)]
    subprocess.run([sys.executable,str(driver),'--manuscript',str(FORMATTING),'--plan',str(PLAN),
        '--current-objects',str(OBJECTS),*shared,'--out',str(OUT/'styles')],check=True)
    original=load(FORMATTING)
    for name,count in [('two',2),('three',3)]:
        doc=deepcopy(original)
        rows=[r for r in doc['records'] if r['kind']=='typed-choice-label']
        groups={}
        for r in rows:groups.setdefault((r['block'],r['source_command_offset']),[]).append(r)
        doc['records']=[r for group in groups.values() if len(group)==count for r in group]
        doc['typed_choice_objects']=len(doc['records'])
        doc['physical_speech_objects']=doc['ordinary_speech_objects']=doc['style_physical_speech_objects']=0
        assert len(doc['records'])==({'two':4,'three':3}[name])
        path=OUT/(name+'_choice_manuscript.json');save(path,doc)
        module='scripts.check_editorial_two_choice_batch' if count==2 else 'scripts.check_editorial_three_choice_single'
        subprocess.run([sys.executable,'-m',module,'--manuscript',str(path),*shared,'--out',str(OUT/name)],check=True)
    print('All four style objects and three menus passed their original contracts; visual review remains.')

if __name__=='__main__':main()
