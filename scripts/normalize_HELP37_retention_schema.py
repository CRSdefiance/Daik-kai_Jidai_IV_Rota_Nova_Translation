"""Keep frozen failed preparation;normalize only the ten retention metadata tags to Help's schema."""
import os
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Shared_HELP_T44_T80_formatting_20261104');failed=Path('work/analysis/Shipyard_HELP37_release_20261104')
    old=Path('translations/help_shipyard37_contextual_final_review_v2.json');new=old.with_name('help_shipyard37_contextual_final_review_v3.json')
    assert not new.exists() and not (root/'production_plan_v3.json').exists()
    doc=load(old);before=deepcopy(doc);revised=0
    for row in doc['records']:
        if row['decision']=='retain-wording':assert row['retention_reason'];row['decision']='retention';revised+=1
    assert revised==10 and sum(r['decision']=='revision'for r in doc['records'])==27
    assert all({k:v for k,v in a.items()if k!='decision'}=={k:v for k,v in b.items()if k!='decision'}for a,b in zip(doc['records'],before['records'],strict=True))
    doc.update(previous_final_review=str(old),previous_final_review_sha256=sha(old.read_bytes()),retention_schema_normalization_only_no_new_editorial_credit=True)
    doc['evidence'][str(Path(__file__))]=sha(Path(__file__).read_bytes());save(new,doc)
    plan=load(root/'production_plan_v2.json');plan.update(manuscript=str(new),manuscript_sha256=sha(new.read_bytes()),all_reviewed_source_prose_page_bytes_andgates_unchanged=True)
    save(root/'production_plan_v3.json',plan)
    registry=Path('translations/release_stack.json');assert sha(registry.read_bytes())=='013b1aa0698652ea044c609de66d661f2d3460d1478c6e2a91519bd354b588aa'
    save(failed/'failure_receipt_v1.json',dict(failed_step='positive prepublication plan, before registry mutation',
      reason='New manuscript used retain-wording; registered Help schema requires retention. No prose,source,layout orruntime defect.',
      partial_preparation_all_outputs_preserved=True,registry_sha256=sha(registry.read_bytes()),new_credit=0))
    pins_path=Path('translations/rom_retention_pins.json');raw=pins_path.read_bytes();pins=load(pins_path)
    for p in failed.glob('*.nds'):
        if not any(Path(r['path']).resolve()==p.resolve()for r in pins):pins.append(dict(path=str(p.resolve()),reason='Preserve failed Help37 schema preparation reference;bytes andall priorROMs retained. SHA256 '+sha(p.read_bytes())))
    temp=pins_path.with_name('rom_retention_pins.HELP37_schema_failure.pending.json');assert not temp.exists();save(temp,pins)
    assert pins_path.read_bytes()==raw;os.replace(temp,pins_path)
    print('Ten retention metadata tags normalized;all37 prose/pages/gates unchanged.Failed preparation andROMs preserved,registry unchanged.')
