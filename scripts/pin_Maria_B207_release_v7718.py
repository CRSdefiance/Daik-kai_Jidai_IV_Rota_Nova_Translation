"""Preserve the cumulative candidate and exact clean-input reconstruction; no pruning."""
import json,os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_release_pins_v7718')
if __name__=='__main__':
    assert not ROOT.exists();proof=Path('work/analysis/maria_B207_release_v7718/registered_release_verification.json');r=read(proof)
    assert r['whole_clean_input_ROM_reconstruction_byte_exact'] and r['whole_ROM_equals_pinned_approved_reference']
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);added=[]
    for key in ['candidate','exact_patch_reconstruction']:
        p=Path(r[key]).resolve();assert sha(p.read_bytes())==r['candidate_sha256'] and not any(Path(v['path']).resolve()==p for v in values)
        entry=dict(path=str(p),reason='V7717 registered cumulative629-batch Maria B207 integration orits exact clean-input reconstruction. Source/English reviews13 revisions5 retentions,all18 release checks110 regressions pass;own-ROM startup andledger credit pending. Preserve all ROMs;not a promotion orseparate test package. SHA256 '+r['candidate_sha256']);values.append(entry);added.append(entry)
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'pin_receipt.json',dict(added=added,before_sha256=sha(before),after_sha256=sha(encoded),release_proof=str(proof),release_proof_sha256=sha(proof.read_bytes()),all_prior_pins_andROMs_preserved=True,ROMs_deleted=0,no_promotion_orpruning_orhandoff_package=True,new_credit=0,full_goal_complete=False))
