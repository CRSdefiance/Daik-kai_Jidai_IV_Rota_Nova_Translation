"""Require measured source/English command results,not only their summary approval flag."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B198_compiler_result_guards_v5753')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('dk4tool/patch/lil_B198_editorial_v1.py','dk4tool/patch/lil_B198_editorial_v2.py',{
        "    require(sample['fifteen_actual_native_panels56_holds_and_two_offline_conditionals_explicit']":
        """    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(actual['versions'][0])==shape(actual['versions'][1])
        and actual['versions'][0]['input_schedule_sha256']==actual['versions'][1]['input_schedule_sha256'],
        'measured source/English command results or inputs differ')
    for version in actual['versions']:
        require([(r['source_offset'],r['native_result']) for r in version['command_pairs'] if r['word']==0x8000]==[(306,[2,0]),(480,[2,0])],
            'both original unforced predicate results required')
        require(version['command_pairs'][-1]['source_offset']==540 and version['command_pairs'][-1]['native_result']==[0,0],
            'observed original source ending required')
        require([r['source_record_index'] for r in version['selected_intervals']]==[10,14,18,22,26,30,34,38,42,49,53,72,76,80,84],
            'fifteen actual source IDs required')
    require(sample['fifteen_actual_native_panels56_holds_and_two_offline_conditionals_explicit']"""})
    ROOT.mkdir(parents=True);save(ROOT/'explicit_measured_command_result_guards.json',dict(tool=tool,
        measured_source_English_command_results_inputs_predicates_end_and15_source_IDs_required=True,
        original_atomic_v1_preserved=True,all_source_control_inverse_and_single_mutation_guards_unchanged=True,
        new_review_credit=0,full_goal_complete=False))
    print('B198 v2 adds direct measured command-result/input/predicate/end/actual-ID guards before the sole mutation.')
