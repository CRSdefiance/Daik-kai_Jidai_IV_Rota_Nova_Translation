"""Preserve the stopped harness; correct two expected-message literals and reuse its 23 completed cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_challenge_resume_tools_v8356b');prior=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356');assert not root.exists()
    assert len(list(prior.glob('case_*.json')))==23
    for i in range(23):
        record=read(prior/f'case_{i:03d}.json');assert record['rejected'] and record['commit_calls']==0 and record['actual_input_changes_asserted']
    anchor='''        for i,c in enumerate(cases):
            image=NdsImage'''
    replacement='''        for i,c in enumerate(cases):
            if i<23:
                priorpath=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356')/f'case_{i:03d}.json';record=base_load(priorpath)
                assert all(record[k]==c[k] for k in ['case','edits','expected_guard']) and record['rejected'] and record['commit_calls']==0
                assert record['dependency_digest_gate_deliberately_bypassed'] and record['whole_input_identity_andall_ROM_bytes_unchanged']
                record.update(exact_completed_case_reused=str(priorpath),exact_completed_case_sha256=sha(priorpath.read_bytes()))
                results.append(record);save(ROOT/f'case_{i:03d}.json',record)
                continue
            image=NdsImage'''
    d=derive('scripts/challenge_Hodram_outcomes_atomic_v8356.py','scripts/challenge_Hodram_outcomes_atomic_v8356b.py',{
        "ROOT=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356')":"ROOT=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356b')",
        'source-qualified complete Lil nameplane/events/final flush':'source-qualified complete Lil nameplane/events/flushes',
        'exact later RGB equality count':'all complete later framebuffer comparisons retained',
        anchor:replacement,
    })
    root.mkdir(parents=True);save(root/'expected_message_correction_23_exact_passed_cases_reused.json',dict(derivation=d,prior_completed_cases=23,stopped_case_rejected_correctly_only_message_expectation_differed=True,no_production_guard_orinput_orROM_change=True,new_credit=0,full_goal_complete=False))
