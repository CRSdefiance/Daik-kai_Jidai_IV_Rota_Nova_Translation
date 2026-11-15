"""Correct only the new checkpoint's uppercase heading;preserve byte-exact inverse backups."""
import gzip,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B218_checkpoint_heading_v6892b');PRIOR=Path('work/analysis/editorial_handoff_verification_v6893/verified_handoff.json');VERIFY=Path('work/analysis/editorial_handoff_verification_v6893b');LEDGER=Path('translations/editorial_review_current_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not VERIFY.exists();prior=read(PRIOR);assert sha(LEDGER.read_bytes())==prior['ledger_sha256'] and prior['B218_all13_four_prose_gates_true_formatting_false'];root=Path.cwd().resolve();planned=[];wrong=b'## V6847: B218 whole-exchange source/native progress; Lil Argot and Ian Dukov retained';right=wrong.replace(b'V6847',b'V6892')
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;before=path.read_bytes();assert path.resolve().is_relative_to(root) and before.count(wrong)==1;after=before.replace(wrong,right,1)
        if name=='editorial_handoff_current.md':
            a,b=b'# Current editorial handoff - V6847',b'# Current editorial handoff - V6892';assert before.startswith(a);after=b+after[len(a):];inverse=a+after[len(b):]
        else:assert before.startswith(wrong);inverse=after
        inverse=inverse.replace(right,wrong,1);assert inverse==before;planned.append((path,before,after))
    ROOT.mkdir(parents=True);files=[]
    for index,(path,before,after) in enumerate(planned):
        backup=ROOT/f'{index:02d}.before.gz';backup.write_bytes(gzip.compress(before,mtime=0));target=ROOT/f'{index:02d}.after';target.write_bytes(after);files.append(dict(path=str(path.resolve()),before_sha256=sha(before),after_sha256=sha(after),backup=str(backup),planned=str(target)))
    assert all(path.read_bytes()==before for path,before,after in planned) and sha(LEDGER.read_bytes())==prior['ledger_sha256'];save(ROOT/'preapplication_audit.json',dict(files=files,all_five_heading_changes_have_complete_byte_inverse=True,ledger_ROM_translation_data_and_all_counters_unchanged=True,full_goal_complete=False))
    for path,before,after in planned:
        with path.open('r+b') as stream:stream.write(after);stream.truncate();stream.flush();os.fsync(stream.fileno())
        assert path.read_bytes()==after
    assert sha(LEDGER.read_bytes())==prior['ledger_sha256'];save(ROOT/'heading_repair_receipt.json',dict(files=files,prior_verification=str(PRIOR),prior_verification_sha256=sha(PRIOR.read_bytes()),source_producer='scripts/checkpoint_lil_B218_native_v6892.py',source_producer_preserved=True,correction='Uppercase V6847 header was not changed by the lowercase v6847 derivation;only the five newest B218 headings now say V6892',all_prior_document_body_bytes_preserved=True,no_ROM_translation_ledger_count_or_emulator_change=True,full_goal_complete=False));out=deepcopy(prior);out.update(checkpoint_heading='V6892',checkpoint_heading_repair=str(ROOT/'heading_repair_receipt.json'),checkpoint_heading_repair_sha256=sha((ROOT/'heading_repair_receipt.json').read_bytes()),verified_document_sha256={str(p):sha(p.read_bytes()) for p,_,_ in planned},verified_ledger_unchanged=True,full_goal_active=True,full_goal_complete=False);VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',out);print('V6892 heading corrected in five documents with complete inverse backups;ledger,ROM,translations,counts and tests unchanged. Verified handoff6893b.')
