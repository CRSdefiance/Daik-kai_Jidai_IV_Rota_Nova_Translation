"""Preserve the terminal count failure and resume only unsaved policy cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B54_B60_policy_count_v8834')
OLD=Path('scripts/validate_Hodram_B54_B60_policy_v8831.py')
NEW=Path('scripts/validate_Hodram_B54_B60_policy_v8831b.py')
PARTIAL=Path('work/analysis/Hodram_B54_B60_policy_validation_v8831/partial_checked_cases.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    assert sha(PARTIAL.read_bytes())=='7c519f97d304f57ebc6c92390c805e0e5b5dbe536276df5807d7f1fc831caf72'
    prior=read(PARTIAL)
    assert len(prior['positive_speech_compilers'])==80 and len(prior['negative_cases'])==542
    resume="""before={str(p):sha(p.read_bytes()) for p in protected}
    partial_path=Path('work/analysis/Hodram_B54_B60_policy_validation_v8831/partial_checked_cases.json')
    assert sha(partial_path.read_bytes())=='7c519f97d304f57ebc6c92390c805e0e5b5dbe536276df5807d7f1fc831caf72'
    previous=read(partial_path)
    assert previous['contract_sha256']==sha(CONTRACT.read_bytes()) and previous['terminal'] is False
    positives=deepcopy(previous['positive_speech_compilers']);negatives=deepcopy(previous['negative_cases'])
    assert len(positives)==80 and len(negatives)==542
    assert [r['id'] for r in positives]==[r['id'] for r in doc['records'][:80]]
    assert CHALLENGED.issubset({r['id'] for r in positives})
    assert len({r['label'] for r in negatives})==542
    for approved,record in zip(doc['records'][:80],positives,strict=True):
        binding=frozen['record_bindings'][approved['id']]
        assert record['compiled_hex']==approved['compiled_hex']==binding['compiled_hex']
        assert record['source_reference']==approved['source_reference'] and record['current_reference']==approved['current_reference'] and record['final_reference']==approved['final_reference']
        assert record['qa']['base_QA_issues']==approved['original_QA_issues']==binding['base_QA_issues']
        assert record['qa']['native_page_count']==approved['expected_native_pages']==binding['native_page_count']
        assert record['qa']['qa_waivers']==[] and not any(i['severity'] in ['warning','error'] for i in record['qa']['issues'])
        cases=[r for r in negatives if r['label'].startswith(approved['id']+':')]
        assert len(cases)==(67 if approved['id'] in CHALLENGED else 1)
        assert any(r['label']==approved['id']+':gate:formatting' for r in cases)
    assert all(r['actual_changed_input'] and r['rejected'] and r['original_sha256']!=r['changed_sha256'] and r['diagnostic'] for r in negatives)
    ROOT.mkdir(parents=True)"""
    changes={
        "Hodram_B54_B60_policy_validation_v8831'":"Hodram_B54_B60_policy_validation_v8831b'",
        "before={str(p):sha(p.read_bytes()) for p in protected};positives=[];negatives=[];ROOT.mkdir(parents=True)":resume,
        "for index,row in enumerate(doc['records']):":"for index,row in enumerate(doc['records']):\n        if index<80:continue # Exact immutable saved evidence; no completed compiler/challenge replay.",
        'len(negatives)==646':'len(negatives)==625',
        'positive_speech_compilers=positives,positive_no_typed_menu=True':"positive_speech_compilers=positives,resumed_from=str(partial_path),resumed_from_sha256=sha(partial_path.read_bytes()),reused_positive_compilers=80,reused_negative_cases=542,fresh_positive_compilers=2,fresh_negative_cases=83,original_terminal_count_failure_preserved=True,positive_no_typed_menu=True",
    }
    result=derive(OLD,NEW,changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_failure_and_count_qualification.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),observed_terminal_session=63525,observed_exit_code=1,terminal_diagnostic='AssertionError at final expected negative count 646',actual_defined_case_count=82+7*66+16+10*6+5,partial=str(PARTIAL),partial_sha256=sha(PARTIAL.read_bytes()),reused_positive_compilers=80,reused_negative_cases=542,remaining_positive_compilers=2,remaining_negative_cases=83,derivation=result,all_original_dependency_andsemantic_guards_preserved=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Original terminal failure preserved; count625 derived; exact80/542 saved evidence qualified; successor runs only2/83 missing receipts.',flush=True)
