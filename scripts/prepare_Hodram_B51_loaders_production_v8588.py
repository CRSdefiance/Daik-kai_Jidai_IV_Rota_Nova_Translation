"""Bind all original B51 loaders/callers independently in the release pipeline."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_loaders_production_v8588')
    assert not root.exists()
    derivation = derive('dk4tool/patch/hodram_B50_loaders_v1.py', 'dk4tool/patch/hodram_B51_loaders_v1.py', {
        'B50': 'B51', "caller['block']==50": "caller['block']==51",
        "caller['all3_text_records']": "caller['all5_text_records']",
        'all12 caller-selected source/current/final command maps and3record references': 'all20 caller-selected source/current/final command maps and5record references',
        "a.get('native_selected_block')==50": "a.get('native_selected_block')==51",
        '[(50,50,[49])]': '[(51,51,[])]',
        'event50 original prerequisite49,not full eligibility orchronology': 'event51 hasno listed prerequisite,not full eligibility orchronology',
    })
    from dk4tool.patch.hodram_B51_loaders_v1 import check_loaders_and_census
    paths = dict(loaders='work/analysis/Hodram_B51_loaders_v8571/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
        callers='work/analysis/Hodram_B51_references_v8572/references.json', relocation='work/analysis/Hodram_B51_references_v8572/source_current_final_map.json',
        current='work/analysis/Hodram_B51_current_v8559/current_effective.json')
    data = {key: read(path) for key, path in paths.items()}
    docpath = Path('translations/hodram_B51_editorial_manuscript_v5.json')
    doc = read(docpath)
    parent, reference = [NdsImage.open(doc[key]) for key in ['current_ROM', 'reference_ROM']]
    def require(value, message):
        if not value:
            raise ValueError('B51 loader production: ' + message)
    result = check_loaders_and_census(data, parent, reference, data['relocation'], read, require)
    negatives = []
    def reject(label, mutate):
        changed = deepcopy(data)
        mutate(changed)
        assert changed != data
        try:
            check_loaders_and_census(changed, parent, reference, changed['relocation'], read, require)
        except ValueError as error:
            negatives.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed loader evidence accepted: ' + label)
    reject('missing-loader-count', lambda d: d['loaders'].__setitem__('fresh_native_whole_loads_andcache_hits', 324))
    reject('parent-mode-count', lambda d: d['loaders'].__setitem__('fresh_initial_parent_modes', 649))
    reject('caller-command-offset', lambda d: d['callers']['all_command_maps'][0].__setitem__('new_offset', 10))
    reject('wrong-event-prerequisite', lambda d: d['callers']['source_event_records'][0].__setitem__('must_be_completed', [50]))
    reject('natural-activation-scope', lambda d: d['loaders'].__setitem__('controlled_native_route_global_inputs_not_ordinary_event_activation', False))
    assert len(negatives) == 5
    root.mkdir(parents=True)
    save(root / 'loader_production_validation.json', dict(derivation=derivation, summary=result, negative_count=5, negative_cases=negatives,
        every_negative_actual_input_changed_andguard_rejected=True, original325_loads_cache_hits650_modes326_actions_andshipped_callers_independently_bound=True,
        no_ROM_file_mutation_new_emulator_run_atomic_commit_orcompletion_credit=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [*paths.values(), docpath, Path(__file__), Path('dk4tool/patch/hodram_B51_loaders_v1.py')]}))
    print('B51 production loaders:325 cache/load paths,650 parent modes,326 actions andshipped callers bind exactly;five changed evidence inputs reject. No new gameplay orROM commit.')
