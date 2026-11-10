"""Validate independent production controls; actual changing defects never commit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B51_profile_v1 import validate_approved_batch, validate_runtime
from dk4tool.patch.hodram_B51_references_v1 import reconstruct_and_bind
from dk4tool.patch.hodram_B51_native_evidence_v1 import check_native_models
from dk4tool.patch.hodram_B51_controls_v1 import check_controls
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_controls_production_v8592')
DOC = Path('translations/hodram_B51_editorial_manuscript_v5.json')
PATHS = dict(relocation='work/analysis/Hodram_B51_references_v8572/source_current_final_map.json', current='work/analysis/Hodram_B51_current_v8559/current_effective.json',
    source_controls='work/analysis/Hodram_B51_source_controls_v8555/source_controls.json', source_display='work/analysis/Hodram_B51_source_display_v8556/source_display.json',
    stored='work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json', result_flow='work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    models='work/analysis/Hodram_B51_models_v8575/native_models.json', pages='work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, data = read(DOC), {key: read(path) for key, path in PATHS.items()}
    parent, reference, clean = NdsImage.open(doc['current_ROM']), NdsImage.open(doc['reference_ROM']), NdsImage.open('work/clean.nds')
    before = bytes(parent.rom.save())
    validate_approved_batch(doc)
    validate_runtime(parent)
    def require(value, message):
        if not value:
            raise ValueError('B51 controls production: ' + message)
    rebuilt = reconstruct_and_bind(parent, clean, reference, doc, data, require)
    native = check_native_models(data, doc['records'], parent, read, require)
    summary = check_controls(data, doc['records'], parent, reference, rebuilt, native, read, require)
    assert bytes(parent.rom.save()) == before and summary['native_relative_cases'] == 40 and summary['original_result_channel_cases'] == 50
    negatives = []
    def reject(label, mutate):
        changed = deepcopy(data)
        mutate(changed)
        assert changed != data
        try:
            check_controls(changed, doc['records'], parent, reference, rebuilt, native, read, require)
        except ValueError as error:
            assert 'Native dependency changed' not in str(error)
            negatives.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed control evidence accepted: ' + label)
        assert bytes(parent.rom.save()) == before
    reject('untrusted-query-adapter', lambda d: d['source_controls'].__setitem__('source_owned_query_probe', d['source_controls']['source_owned_query_probe'] + '\n'))
    reject('missing-relative-site', lambda d: d['relocation']['groups'][0]['relocated_skip_cases'].pop())
    reject('wrong-query-value', lambda d: d['stored']['stored_queries'][0]['native_result'].__setitem__(1, 1))
    reject('discarded-sixth-query-word', lambda d: d['stored']['stored_queries'][1]['native_result'].__setitem__(5, 1))
    reject('wrong-normal-value-carry', lambda d: d['stored']['normal_seeded_ends'][1]['native_result'].__setitem__(1, 0))
    reject('false-caller-value-channel', lambda d: d['result_flow']['caller_fragment_cases'][0].__setitem__('next_parser_r3', 1))
    assert len(negatives) == 6
    ROOT.mkdir(parents=True)
    save(ROOT / 'control_production_validation.json', dict(summary=summary, negative_count=6, negative_cases=negatives,
        every_negative_actual_input_changed_andguard_rejected_with_frozen_dependencies_enabled=True,
        all_native_control_fields_independently_executed_not_summary_boolean_approval=True,
        original_actor_ABI_unowned4MiB_input_output_canary_andcaller_register_guards_preserved=True,
        caller_image_unchanged_andzero_atomic_commits=True, no_new_capture_ROM_write_registered_stage_orcompletion_credit=True,
        new_credit=0, full_goal_complete=False, evidence={str(p): sha(Path(p).read_bytes()) for p in [DOC, *PATHS.values(), Path(__file__), Path('dk4tool/patch/hodram_B51_controls_v1.py')]}))
    print('B51 production controls: five dispatches/forty branch cases/two queries/four opaque pairs/twenty-five full ends/fifty caller-value cases pass; six real changed defects reject. Frozen guards enabled, no ROM commits.')
