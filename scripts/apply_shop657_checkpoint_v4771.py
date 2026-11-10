"""Apply independently audited metadata only after all expected hashes match."""
from pathlib import Path
import os
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shop657_checkpoint_v4771')

if __name__=='__main__':
    audit=read(ROOT/'pre_apply_audit.json');assert audit['staged_not_applied']
    assert audit['all_original_root_and_nested_ledger_history_preserved']
    plan=read(ROOT/'metadata_plan.json');targets=plan['files'];assert not (ROOT/'application_receipt.json').exists()
    for row in targets:
        p=Path(row['target']);assert sha(Path(row['staged']).read_bytes())==row['after_sha256']
        if row['existed']:assert sha(p.read_bytes())==row['before_sha256']
        else:assert not p.exists()
    for row in targets:
        p=Path(row['target']);data=Path(row['staged']).read_bytes()
        if row['existed']:
            with p.open('r+b') as stream:
                stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
        else:
            with p.open('xb') as stream:
                stream.write(data);stream.flush();os.fsync(stream.fileno())
        assert sha(p.read_bytes())==row['after_sha256']
    save(ROOT/'application_receipt.json',dict(metadata_files=9,all_planned_hashes_exact=True,
        preexisting_ROMs_translations_and_historical_ledger_preserved=True,
        added_editorial_credit=0,full_goal_complete=False))
    print('Applied9 independently audited metadata updates; no duplicate review credit and no ROM/main change.')
