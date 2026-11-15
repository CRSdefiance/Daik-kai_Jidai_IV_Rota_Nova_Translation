"""Independently preserve every B51 measured timing/RNG/state/RGB difference."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_comparison_production_v8589')
    assert not root.exists()
    source = Path('dk4tool/patch/hodram_B50_comparison_v1.py').read_text('utf-8')
    resource = source[source.index('        display=[next('):source.index('        boundaries=[]')]
    derivation = derive('dk4tool/patch/hodram_B50_comparison_v1.py', 'dk4tool/patch/hodram_B51_comparison_v1.py', {
        'B50': 'B51', 'number=50': 'number=51',
        resource: "        require(declared['source_has_no_picture_orhide_sites'] and declared['unvisited_conditional_text_IDs']==old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032'],'exact unforced four-speech path andoffline-only Charles scope')\n",
        "[g['later_RGB_differences'] for g in result['groups']]==[4]": "[g['later_RGB_differences'] for g in result['groups']]==[3]",
        'all four laterRGB differences andtwo command-duration differences retained': 'all three laterRGB differences andtwo command-duration differences retained',
        "['3867090476','3028864251']": "['2294662370','3116913577']",
        'all_source_qualified_item148_layout0_show_hide_intervals_checked=True': 'all_source_qualified_query_branch_path_andunvisited_Charles_scope_checked=True',
    })
    from dk4tool.patch.hodram_B51_comparison_v1 import check_comparisons
    paths = dict(comparison='work/analysis/Hodram_B51_comparison_v8577/paired_selected_path_comparison.json',
        actual='work/analysis/Hodram_B51_actual_v8576/B51/paired_actual_dialogue_headers_flow_returns.json')
    data = {key: read(path) for key, path in paths.items()}
    docpath = Path('translations/hodram_B51_editorial_manuscript_v5.json')
    doc = read(docpath)
    parent = NdsImage.open(doc['current_ROM'])
    def require(value, message):
        if not value:
            raise ValueError('B51 comparison production: ' + message)
    result = check_comparisons(data, parent, read, require)
    assert result['later_full_RGB_pairs_recomputed'] == 89 and result['groups'][0]['later_RGB_differences'] == 3
    negatives = []
    def reject(label, mutate):
        changed = deepcopy(data)
        mutate(changed)
        assert changed != data
        try:
            check_comparisons(changed, parent, read, require)
        except ValueError as error:
            negatives.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed comparison evidence accepted: ' + label)
    reject('hide-final-RNG-difference', lambda d: d['comparison']['groups'][0].__setitem__('final_PRNG_seeds', [1, 1]))
    reject('hide-RGB-difference', lambda d: d['comparison']['groups'][0]['later_RGB_comparisons'][0].__setitem__('whole_RGB_equal', not d['comparison']['groups'][0]['later_RGB_comparisons'][0]['whole_RGB_equal']))
    reject('hide-timing-difference', lambda d: d['comparison']['groups'][0].__setitem__('duration_differences', []))
    reject('false-Charles-visit', lambda d: d['comparison']['groups'][0].__setitem__('unvisited_conditional_text_IDs', []))
    assert len(negatives) == 4
    root.mkdir(parents=True)
    save(root / 'comparison_production_validation.json', dict(derivation=derivation, summary=result, negative_count=4, negative_cases=negatives,
        every_negative_actual_input_changed_andguard_rejected=True, all89_RGBpairs_native_components_wholeactors_rawcalendar_final_rng_andtiming_differences_recomputed=True,
        no_retiming_capture_replay_state_forcing_ROM_write_atomic_commit_orcompletion_credit=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [*paths.values(), docpath, Path(__file__), Path('dk4tool/patch/hodram_B51_comparison_v1.py')]}))
    print('B51 production comparisons independently reproduce89RGBpairs/three differences,two duration differences andunequal final RNG;four changing false-equivalence/coverage claims reject. No replay orROM commit.')
