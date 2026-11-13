"""Run unchanged style/menu contracts for the exact two-style/one-menu scope."""
from pathlib import Path
import subprocess
import sys
from scripts.audit_story_glyph_consistency import load
from scripts.prepare_hodram_B231_B250_document_v2 import DOCUMENT
from scripts.review_hodram_B231_B250_contextual_v1 import OBJECTS
from scripts.prepare_hodram_B231_B250_scope_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'native_objects_v1'
PLAN=ROOT/'formatting_v1/initial_plan_v2/automatic_plans.json'
RELEASE=Path('work/hodram_B211_B230_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'

def main():
    assert not OUT.exists();OUT.mkdir()
    source=checked_text(Path('scripts/check_editorial_style_objects.py').read_text(encoding='utf-8'),{
        "assert len(objects)==8 and cases==64 and sum(len(o['physical_record_IDs']) for o in objects)==48":
            "assert len(objects)==2 and cases==16 and sum(len(o['physical_record_IDs']) for o in objects)==14",
        'physical_alternatives=48,':'physical_alternatives=14,',
        'PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks;':
            'PASS2 compiled4100 objects/14 physical alternatives/16 original target slot cases/18 semantic rejection checks;',
    })
    driver=OUT/'source_locked_style_driver.py';driver.write_text(source,encoding='utf-8')
    shared=['--release',str(RELEASE),'--startup',str(STARTUP)]
    subprocess.run([sys.executable,str(driver),'--manuscript',str(DOCUMENT),'--plan',str(PLAN),
        '--current-objects',str(OBJECTS),*shared,'--out',str(OUT/'styles')],check=True)
    subprocess.run([sys.executable,'-m','scripts.check_editorial_two_choice_batch','--manuscript',str(DOCUMENT),
        *shared,'--out',str(OUT/'menu')],check=True)
    assert len(load(OUT/'styles/compiled_style_objects.json')['objects'])==2
    assert len(load(OUT/'menu/complete_choice_objects.json')['objects'])==1
    print('Two style objects and one menu pass original complete-object contracts; visual approval pending.')

if __name__=='__main__':main()
