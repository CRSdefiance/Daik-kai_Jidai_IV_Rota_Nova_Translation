"""Independently bind complete B51 fixtures, observed traces and all actual masks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_actual_production_v8593')
    assert not root.exists()
    derivation = derive('dk4tool/patch/hodram_B50_actual_evidence_v1.py', 'dk4tool/patch/hodram_B51_actual_evidence_v1.py', {
        'B50': 'B51',
        'original[50]': 'original[51]',
        "else target)[50]": "else target)[51]",
        'len(source_commands)==12': 'len(source_commands)==20',
        'all12 original B50 commands': 'all20 original B51 commands',
        'len(selected_speeches)==3 and len(selected_commands)==12': 'len(selected_speeches)==5 and len(selected_commands)==20',
        "f['source_block']==50": "f['source_block']==51",
        'original_block=50': 'original_block=51',
        "relative==f['source_relative_sites']==0": "relative==f['source_relative_sites']==8",
        'len(objects)==12 and len(texts)==3': 'len(objects)==20 and len(texts)==5',
        "group['block']==50": "group['block']==51",
        'Hodram_B50_scene_runs_v8505': 'Hodram_B51_scene_runs_v8574',
        "['DK4_MES_B50_R0007','DK4_MES_B50_R0010','DK4_MES_B50_R0013']": "['DK4_MES_B51_R0006','DK4_MES_B51_R0010','DK4_MES_B51_R0014','DK4_MES_B51_R0039']",
        'len(pairs)==20': 'len(pairs)==23',
        'whole B50 exchange all12commands/3speeches/no menu': 'whole B51 exchange selected15commands/four observed speeches/no menu',
        'page_occurrences==6 and totalholds==50': 'page_occurrences==8 and totalholds==56',
        'both actual groups/6page occurrences/50complete body-name orabsent-header holds': 'both actual groups/eight observed page occurrences/56 complete body-name holds',
        'complete_actual_page_occurrences=6,complete_actual_holds=50,unique_speech_IDs=3': 'complete_actual_page_occurrences=8,complete_actual_holds=56,unique_speech_IDs=4',
        'all12_original_commands_andnormal_value_carry_verified=True': 'all20_original_commands_retained_selected15_andnormal_value_carry_verified=True',
    })
    from dk4tool.dialogue.hodram_B51_profile_v1 import validate_approved_batch, validate_runtime
    from dk4tool.patch.hodram_B51_references_v1 import reconstruct_and_bind
    from dk4tool.patch.hodram_B51_native_evidence_v1 import check_native_models
    from dk4tool.patch.hodram_B51_actual_evidence_v1 import check_actual
    paths = dict(relocation='work/analysis/Hodram_B51_references_v8572/source_current_final_map.json', current='work/analysis/Hodram_B51_current_v8559/current_effective.json',
        source_controls='work/analysis/Hodram_B51_source_controls_v8555/source_controls.json', source_display='work/analysis/Hodram_B51_source_display_v8556/source_display.json',
        stored='work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json', models='work/analysis/Hodram_B51_models_v8575/native_models.json',
        pages='work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json', fixtures='work/analysis/Hodram_B51_fixtures_v8573/two_whole_scripts.json',
        actual='work/analysis/Hodram_B51_actual_v8576/B51/paired_actual_dialogue_headers_flow_returns.json')
    data = {key: read(path) for key, path in paths.items()}
    docpath = Path('translations/hodram_B51_editorial_manuscript_v5.json')
    doc = read(docpath)
    parent, clean, reference = NdsImage.open(doc['current_ROM']), NdsImage.open('work/clean.nds'), NdsImage.open(doc['reference_ROM'])
    before = bytes(parent.rom.save())
    validate_approved_batch(doc)
    validate_runtime(parent)
    def require(value, message):
        if not value:
            raise ValueError('B51 actual production: ' + message)
    rebuilt = reconstruct_and_bind(parent, clean, reference, doc, data, require)
    native = check_native_models(data, doc['records'], parent, read, require)
    result = check_actual(data, doc['records'], parent, clean, rebuilt, native, read, require)
    assert result['summary']['complete_actual_holds'] == 56 and result['summary']['unique_speech_IDs'] == 4
    assert bytes(parent.rom.save()) == before
    negatives = []
    def reject(label, mutate):
        changed = deepcopy(data)
        mutate(changed)
        assert changed != data
        try:
            check_actual(changed, doc['records'], parent, clean, rebuilt, native, read, require)
        except ValueError as error:
            assert 'Native dependency changed' not in str(error)
            negatives.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed actual evidence accepted: ' + label)
        assert bytes(parent.rom.save()) == before
    reject('wrong-initializer-shift', lambda d: d['fixtures']['fixtures'][0].__setitem__('constant_shift_bytes', 32))
    reject('omitted-original-query', lambda d: d['fixtures']['fixtures'][0]['all_original_exchange_commands'].pop(5))
    reject('lost-complete-body-name-hold', lambda d: d['actual']['groups'][0]['speeches'][0]['complete_holds'].pop())
    reject('false-Charles-visit', lambda d: d['actual']['groups'][1].__setitem__('unvisited_conditional_text_IDs', []))
    reject('invented-speaker-title', lambda d: d['actual']['groups'][1]['speeches'][0].__setitem__('name', 'Port Captain'))
    assert len(negatives) == 5
    root.mkdir(parents=True)
    save(root / 'actual_production_validation.json', dict(derivation=derivation, summary=result['summary'], negative_count=5, negative_cases=negatives,
        every_negative_actual_input_changed_andguard_rejected_with_frozen_dependencies_enabled=True,
        two_whole_fixture_ROMs_original_preludes_all20commands_resident_payloads_inputs_callbacks_andall_observed_glyph_name_masks_independently_bound=True,
        source_Charles_R32_not_observed_offline_checks_andall_actual_scope_limits_preserved=True,
        no_new_emulator_capture_retiming_state_forcing_ROM_write_atomic_commit_orcompletion_credit=True,
        new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [*paths.values(), docpath, Path(__file__), Path('dk4tool/patch/hodram_B51_actual_evidence_v1.py')]}))
    print('B51 production actual reader independently binds both full fixtures,all selected source/control traces,eight observed pages/56 exact holds andnormalreturns;five changed defects reject. Charles remains explicitly unvisited;no replay orROM commits.')
