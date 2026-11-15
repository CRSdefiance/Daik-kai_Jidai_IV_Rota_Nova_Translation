"""Use a natural count-neutral sailor-loss label;preserve one original amount."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save
from scripts.search_reports_native_plan_v1661 import plan
from dk4tool.rom.nds import NdsImage

ROOT=Path('work/analysis/search_reports_payload_v1670')
OUT=Path('translations/search_reports_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    source=Path('translations/search_reports_editorial_manuscript_v2.json');doc=deepcopy(read(source))
    row=next(r for r in doc['records'] if r['message_id']==312);assert row['english']=='Lost %s sailors.'
    row['english']='Sailors lost: %s.'
    row['localization_note']+=' Visual numeric review exposed the singular mismatch Lost1 sailors. A count-neutral status label is natural for both one and multiple losses and preserves the single original numeric value without inventing death or a cause.'
    doc.update(revised_from_manuscript=str(source),revised_from_sha256=sha(source.read_bytes()),
               status='source-prose-revised-after-numeric-grammar-review;native-recheck-pending')
    for r in doc['records']:
        if r['message_id']>=2229:
            r['source_quantity_contract']['nonzero_quantities_are_multiples_of_five']=True
            r['localization_note']+=' Original79F18/79F2C multiplies both quantities by5,so nonzero source counts are at least5;the plural barrels never receives a singular count in the original event.'
    save(OUT,doc);rom=NdsImage.open(doc['current_ROM']);c,a,p=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp,ap=ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin';cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**p,'target_COMMON':str(cp),'target_ARM9':str(ap),'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Sailor-loss wording is count-neutral;foraging source multiples-of-five documented. All11 repacked;native recheck pending,no completion credit.')
