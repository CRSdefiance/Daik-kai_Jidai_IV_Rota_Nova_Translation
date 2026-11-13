"""Validate all original long/focused state, timing, RNG, calendar and RGB limits."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B52_comparison_v1 import check_comparisons
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_comparison_production_v8685')
DOC=Path('translations/hodram_B52_editorial_manuscript_v6.json')
PATHS=dict(comparison='work/analysis/Hodram_B52_comparison_v8655/paired_selected_path_comparison.json',
    focus_comparison='work/analysis/Hodram_B52_focus_comparison_v8658/paired_selected_path_comparison.json',
    actual='work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json',
    opposition_actual='work/analysis/Hodram_B52_opposition_actual_v8653/B52/paired_actual_dialogue_headers_flow_returns.json',
    focus_actual='work/analysis/Hodram_B52_focus_actual_v8657/B52/paired_actual_dialogue_headers_flow_returns.json')

if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);data={k:read(p) for k,p in PATHS.items()};parent=NdsImage.open(doc['current_ROM'])

    def require(value,message):
        if not value:raise ValueError('B52 production comparison:'+message)

    result=check_comparisons(data,parent,read,require)
    assert result['later_full_RGB_pairs_recomputed']==199
    assert [g['whole_actors_equal'] for g in result['groups']]==[False,True,True]
    negatives=[]

    def reject(label,mutate):
        changed=deepcopy(data);mutate(changed);assert changed!=data
        try:check_comparisons(changed,parent,read,require)
        except ValueError as error:
            negatives.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=str(error)))
        else:raise AssertionError('Changed comparison evidence accepted:'+label)

    reject('discarded-command-timing-difference',lambda d:d['comparison']['groups'][0]['command_comparison_differences'].pop())
    reject('falsely-equal-long-withdrawal-state',lambda d:d['comparison']['groups'][0]['five_native_component_equality'].__setitem__('state',True))
    reject('falsely-equal-long-withdrawal-actors',lambda d:d['comparison']['groups'][0].__setitem__('whole_actors_equal',True))
    reject('discarded-long-opposition-RGB-difference',lambda d:d['comparison']['groups'][1].__setitem__('later_RGB_difference_count',0))
    reject('changed-focused-PRNG',lambda d:d['focus_comparison']['groups'][0]['final_PRNG_seeds'].__setitem__(1,1))
    reject('removed-focused-later-RGB',lambda d:d['focus_comparison']['groups'][0]['later_RGB_comparisons'].pop())
    assert len(negatives)==6
    ROOT.mkdir(parents=True)
    save(ROOT/'comparison_production_validation.json',dict(summary=result,negative_count=6,negative_cases=negatives,
         every_negative_is_genuinely_changed_evidence_andindependent_semantic_rejection=True,
         all199_later_whole_RGB_pairs_native_components_wholeactors_rawcalendars_PRNG_timing_andfollowing_commands_checked=True,
         long_withdrawal_divergence_andfocused_immediate_agreement_not_equated=True,
         no_new_capture_ROM_atomic_commit_orcompletion_credit=True,full_goal_complete=False,
         evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,*PATHS.values(),__file__,'dk4tool/patch/hodram_B52_comparison_v1.py']}))
    print('B52 production comparisons:all199 laterRGBpairs,three paired timing/RNG/calendar/component/actor contexts;6 real changed-evidence rejections. All long divergences/focused agreement retained. No new capture/ROM/credit.')
