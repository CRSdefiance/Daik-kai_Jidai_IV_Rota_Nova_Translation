"""Correct the B171 timing-summary count; preserve the original checkpoint/producers."""
from collections import Counter
import gzip
import json
import os
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B171_timing_count_amendment_v4349')
PROOF=Path('work/analysis/lil_B171_repeat_verification_v4344/post_B171_actor_captain_and_same_ROM_repeat_comparison.json')

if __name__=='__main__':
    assert not ROOT.exists()
    proof=read(PROOF)
    count=Counter(r['source']['word'] for r in proof['cross_language_command_timing_differences'])
    assert count==Counter({0x4000:17,0x4621:1,0x61FF:1,0x6325:1,0xC200:1,0:1})
    lp=Path('translations/editorial_review_current_v1.json');before=lp.read_bytes();ledger=json.loads(before)
    receipt=read('work/analysis/lil_B171_reference_checkpoint_v4347/checkpoint_receipt.json')
    assert sha(before)==receipt['ledger_sha256']
    old='Twenty-two cross-language command timestamp differences include16 speeches andsix presentation/resource/C200/end commands'
    new='Twenty-two cross-language command timestamp differences include17 speeches andfive presentation/resource/C200/end commands'
    assert ledger['latest_checkpoint'].count(old)==1
    amendment=dict(original_checkpoint='V4347',failed_independent_audit='scripts/verify_editorial_handoff_v4348.py',
        finding='The independent assertion caught a prose-summary arithmetic error; the exact22 command timing pairs were already correct.',
        original_summary_phrase=old,corrected_summary_phrase=new,
        timing_command_census={format(k,'04X'):v for k,v in sorted(count.items())},
        exact22_timing_pairs=proof['cross_language_command_timing_differences'],
        evidence={str(PROOF):sha(PROOF.read_bytes())},
        no_ROM_prose_source_control_or_gameplay_evidence_change=True,new_source_prose_reviews=0,new_completed_records=0,
        full_goal_complete=False)
    ledger['lil_B171_command_timing_count_amendment_v4349']=amendment
    ledger['latest_checkpoint']=ledger['latest_checkpoint'].replace('V4347 seals37','V4349 preserves the V4347 approval of37',1).replace(old,new)
    ROOT.mkdir(parents=True)
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    encoded=lambda d:(json.dumps(d,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    planned={lp:encoded(ledger)}
    text=('V4349 corrects the V4347 descriptive timing split to17 speeches andfive control/end commands:4621,61FF,6325,C200 and the first end. Total22 pairs, all command bytes, return times, native/gameplay proofs and37 approved speeches were already recorded correctly. Preserve the V4347 checkpoint and the V4348 failed count assertion. No ROM, prose, source-control, coverage or completion credit changes. All37 B171 reviews remain reference/gameplay approved and pending registered integration. Main V4303 and the full editorial objective remain intact.\n\n'
        'Next: Create the atomic B171 compiler, register after full V4303, build through the sole integrated builder, verify the clean-input patch and fresh registered startup, then complete the37 pending reviews. Existing source/native/reference/gameplay proofs need no repeat without a change. Continue every wider editorial family; graphics and the later older-record re-audit remain separate and open.')
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;first,rest=p.read_text(encoding='utf-8').split('\n',1)
        if name=='editorial_handoff_current.md':first='# Current editorial handoff - V4349'
        planned[p]=(first+'\n\n## V4349: B171 timing-count amendment; integration pending\n\n'+text+'\n\n'+rest).encode('utf-8')
    stable={str(p):sha(p.read_bytes()) for p in [Path('translations/release_stack.json'),Path('translations/promoted_build.json'),Path('scripts/build_integrated_release.py')]}
    stage=ROOT/'staged';stage.mkdir();mutations=[]
    for n,(p,data) in enumerate(planned.items()):
        oldbytes=p.read_bytes();backup=ROOT/f'{n}.before';backup.write_bytes(oldbytes)
        target=stage/f'{n}.planned';target.write_bytes(data)
        mutations.append(dict(path=str(p),before_copy=str(backup),before_sha256=sha(oldbytes),planned=str(target),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',mutations)
    for r in mutations:
        assert sha(Path(r['path']).read_bytes())==r['before_sha256']
        assert sha(Path(r['planned']).read_bytes())==r['planned_sha256']
    for r in mutations:
        p=Path(r['path']);data=Path(r['planned']).read_bytes()
        with p.open('r+b') as f:
            f.write(data)
            if f.seek(0,os.SEEK_END)!=len(data):f.truncate(len(data))
            f.flush();os.fsync(f.fileno())
        assert sha(p.read_bytes())==r['planned_sha256']
    assert all(sha(Path(p).read_bytes())==v for p,v in stable.items())
    save(ROOT/'amendment_receipt.json',dict(checkpoint='V4349',prior_checkpoint='V4347',prior_ledger_sha256=sha(before),
        ledger_sha256=sha(lp.read_bytes()),amendment=amendment,updated_files={r['path']:r['planned_sha256'] for r in mutations},
        preserved_release_files=stable,producer_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,
        new_source_prose_reviews=0,new_completed_records=0,full_goal_complete=False))
    print('V4349 timing-count amendment applied:17 speeches +5 control/end commands =22. All source,ROM,prose,proofs and credit preserved.')
