"""Reconcile all exact source/complete IDs and register three new coverage units."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/aftermath_coverage_v1278')


def main():
    assert not ROOT.exists()
    path = Path('translations/editorial_review_current_v1.json')
    ledger = read(path)
    complete = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(complete) == len(set(complete)) == 1279
    assert sum(len(f.get('records',[])) for f in ledger['completed_editorial_families']) == 1280
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(pending) == len(set(pending)) == 93 and not set(complete).intersection(pending)
    assert len(set(complete)|set(pending)) == 1372
    assert ledger['completed_editorial_record_counts_by_file'] == {'/COMMON/MESFILE.DK4':1279,'/data/SC2.DK4':1}
    assert ledger['source_prose_reviewed_counts_by_file'] == {'/COMMON/MESFILE.DK4':1372,'/data/SC2.DK4':1}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (1280,953,327,1373)
    units = {u['id'] for u in ledger['coverage_units']}
    new = ledger['completed_editorial_families'][-3:]
    assert sum(len(f['native_message_IDs']) for f in new) == 20
    for family in new:
        assert family['id'] not in units
        final = read(family['final_review'])
        assert set(family['native_message_IDs']) <= set(final['native_message_IDs'])
        ledger['coverage_units'].append({'id':family['id'],
            'status':'complete-with-source-native-and-representative-gameplay-evidence',
            'native_message_IDs':family['native_message_IDs'],'final_review':family['final_review'],
            'actual_proof':final['actual_gameplay'],'full_goal_complete':False})
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_unit_reconciliation.json',read(path))
    save(path,ledger)
    save(ROOT/'exact_coverage_reconciliation.json',{'unique_completed_COMMON_IDs':sorted(complete),
        'reviewed_incomplete_COMMON_IDs':pending,'completed_counts_by_file':ledger['completed_editorial_record_counts_by_file'],
        'source_prose_counts_by_file':ledger['source_prose_reviewed_counts_by_file'],
        'new_completed20_in_three_original_source_families':{f['id']:f['native_message_IDs'] for f in new},
        'no_duplicate_source_or_completion_credit':True,'all_three_coverage_units_registered':True,
        'global_goal_still_active':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('1279 unique complete COMMON IDs+1SC2;93 reviewed-incomplete COMMON;1373 source/prose total. All three new coverage units reconciled.',flush=True)


if __name__ == '__main__':
    main()
