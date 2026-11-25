"""Refresh changed voice objects and qualify exact unchanged native object proofs."""
import argparse
from copy import deepcopy
from pathlib import Path
import subprocess
import sys
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['manuscript','before-plan','after-plan','current-objects','previous-native','release','startup','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    a=parser.parse_args();assert not a.out.exists()
    doc,before,after,current,previous=map(load,[a.manuscript,a.before_plan,a.after_plan,a.current_objects,a.previous_native])
    assert previous['manuscript_sha256']==before['manuscript_sha256']==after['manuscript_sha256']==digest(a.manuscript)
    assert previous['plan_sha256']==digest(a.before_plan)
    assert previous['runtime']==current['runtime']==doc['runtime']
    assert not before['failures'] and not after['failures']
    original={r['id']:r for r in before['records']};plans={r['id']:r for r in after['records']}
    assert original.keys()==plans.keys()
    assert previous['evidence'][str(a.current_objects)]==digest(a.current_objects)
    changed=[];same=[]
    for obj in previous['objects']:
        assert digest(obj['target_path'])==obj['target_sha256']
        ids=obj['physical_record_IDs']
        assert all(original[k]['logical_English']==plans[k]['logical_English'] for k in ids)
        (changed if any(original[k]['encoded_hex']!=plans[k]['encoded_hex'] for k in ids) else same).append(obj)
    assert changed
    keys={(o['block'],o['source_command_offset']) for o in changed}
    count=len(changed);physical=sum(len(o['physical_record_IDs']) for o in changed);slots=8*count
    a.out.mkdir(parents=True)
    source=checked_text(Path('scripts/check_editorial_style_objects.py').read_text(encoding='utf-8'),{
        "    for item in current['style_objects']:":
            "    for item in current['style_objects']:\n        if (item['block'],item['source_command_offset']) not in "+repr(keys)+":continue",
        "assert len(objects)==8 and cases==64 and sum(len(o['physical_record_IDs']) for o in objects)==48":
            f"assert len(objects)=={count} and cases=={slots} and sum(len(o['physical_record_IDs']) for o in objects)=={physical}",
        'physical_alternatives=48,':f'physical_alternatives={physical},',
        'PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks;':
            f'PASS{count} changed compiled4100 objects/{physical} physical alternatives/{slots} original target slot cases/{count*9} semantic rejection checks;',
    })
    driver=a.out/'source_locked_changed_style_driver.py';driver.write_text(source,encoding='utf-8')
    subprocess.run([sys.executable,str(driver),'--manuscript',str(a.manuscript),'--plan',str(a.after_plan),
        '--current-objects',str(a.current_objects),'--release',str(a.release),'--startup',str(a.startup),
        '--out',str(a.out/'fresh')],check=True)
    freshpath=a.out/'fresh/compiled_style_objects.json';fresh=load(freshpath)
    assert fresh['runtime']==previous['runtime']
    mapped={(o['block'],o['source_command_offset']):o for o in fresh['objects']};assert mapped.keys()==keys
    merged=deepcopy(previous)
    merged.update(plan=str(a.after_plan),plan_sha256=digest(a.after_plan),
        objects=[mapped.get((o['block'],o['source_command_offset']),o) for o in previous['objects']],
        compiler_negatives=fresh['compiler_negatives']+[n for n in previous['compiler_negatives'] if (n['block'],n['command_offset']) not in keys],
        changed_voice_objects=count,exact_reused_voice_objects=len(same),fresh_native_target_slot_cases=slots,
        exact_reused_native_target_slot_cases=8*len(same),previous_native=str(a.previous_native),previous_native_sha256=digest(a.previous_native),
        fresh_native=str(freshpath),fresh_native_sha256=digest(freshpath),
        all_unchanged_physical_inputs_andcompiled_bytes_exact=True,
        evidence={**previous['evidence'],**fresh['evidence'],**{str(p):digest(p) for p in [a.manuscript,a.before_plan,a.after_plan,a.current_objects,a.previous_native,freshpath,driver,Path(__file__)]}})
    assert len(merged['objects'])==len(previous['objects']) and len(merged['compiler_negatives'])==len(previous['objects'])
    save(a.out/'compiled_style_objects.json',merged)
    print(dict(changed_voice_objects=count,exact_reused_voice_objects=len(same),fresh_native_slots=slots))

if __name__=='__main__':main()
