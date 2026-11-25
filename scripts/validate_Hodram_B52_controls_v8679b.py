"""Exercise B52 production native consumers and genuinely changed evidence failures."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import validate_approved_batch, validate_runtime
from dk4tool.patch.hodram_B52_controls_v2 import check_controls
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_controls_production_v8679b')
DOC = Path('translations/hodram_B52_editorial_manuscript_v6.json')
PATHS = dict(relocation='work/analysis/Hodram_B52_references_v8647/source_current_final_map.json',
    current='work/analysis/Hodram_B52_current_v8631/current_effective.json',
    source_controls='work/analysis/Hodram_B52_source_controls_v8620/source_controls.json',
    source_display='work/analysis/Hodram_B52_source_display_v8626/source_display.json',
    stored='work/analysis/Hodram_B52_stored_v8643/stored_native_controls_andrefs.json',
    result_flow='work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    source_menu_VM='work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, data = read(DOC), {k: read(p) for k,p in PATHS.items()}
    parent, reference = NdsImage.open(doc['current_ROM']), NdsImage.open(doc['reference_ROM'])
    validate_approved_batch(doc)
    validate_runtime(parent)
    before = bytes(parent.rom.save())
    group = data['relocation']['groups'][0]
    rebuilt = dict(target_block=Path(group['target_block']).read_bytes())
    # The independently verified stored native-body models are reused by exact
    # raw bytes; this control test does not repeat the completed display reader.
    native = dict(bodies={'revised_English': {r['id']: dict(expanded_body=bytes.fromhex(r['stored_hex'])[1:]) for r in doc['records']}})

    def require(value, message):
        if not value:
            raise ValueError('B52 production controls:' + message)

    summary = check_controls(data, doc['records'], parent, reference, rebuilt, native, read, require)
    assert (summary['native_relative_cases'], summary['distinct_seeded_ends'], summary['exact_reused_original_result_channel_cases']) == (20,50,50)
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
            raise AssertionError('Changed control evidence accepted:' + label)
        assert bytes(parent.rom.save()) == before

    reject('untrusted-end-adapter', lambda d: d['source_controls'].__setitem__('source_owned_seeded_end_adapter', d['source_controls']['source_owned_seeded_end_adapter']+'\n'))
    reject('missing-relative-site', lambda d: d['relocation']['groups'][0]['relocated_skip_cases'].pop())
    reject('false-normal-value-carry', lambda d: d['stored']['distinct_seeded_ends'][1]['native_result'].__setitem__(1,0))
    reject('false-flagged-return-kind', lambda d: d['stored']['distinct_seeded_ends'][25]['native_result'].__setitem__(0,0))
    reject('discarded-sixth-end-word', lambda d: d['stored']['distinct_seeded_ends'][26]['native_result'].__setitem__(5,1))
    reject('false-caller-value-channel', lambda d: d['result_flow']['caller_fragment_cases'][0].__setitem__('next_parser_r3',1))
    reject('wrong-source-voice', lambda d: d['stored']['stored_dispatches'][0].__setitem__('source_voice_class',1))
    reject('falsely-added-query', lambda d: d['stored']['stored_queries'].append(dict(native_result=[2,0,0,0,0,0])))
    reject('opaque-effect-reinterpretation', lambda d: d['stored']['four_opaque_structural_decodes'][0].__setitem__('word',0))
    assert len(negatives) == 9 and bytes(parent.rom.save()) == before
    ROOT.mkdir(parents=True)
    save(ROOT / 'control_production_validation.json',dict(summary=summary, negative_cases=negatives, negative_count=9,
        every_negative_actual_input_changed_andguard_rejected_with_frozen_dependencies_enabled=True,
        complete_source_current_native_dispatch_event_branch_distinct_end_andopaque_structural_fields_independently_checked=True,
        original50_caller_cases_reused_by_exact_artifact_script_complete_code_span_andall_sixword_guards=True,
        display_reader_not_repeated_no_previous_producer_oractual_capture_replay=True,
        historical_source_V8543_provenance_andunequal_whole_RAM_snapshots_explicit=True,caller_image_unchanged_andzero_atomic_commits=True, no_ROM_registry_orcompletion_credit=True,
        full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,*PATHS.values(),__file__,'dk4tool/patch/hodram_B52_controls_v2.py']}))
    print('B52 controls:3 native dispatches/20 branches/3 event getters/4 opaque pairs/50 distinct ends;50 original caller cases exactly reused;9 semantic rejections. No ROM commit/credit.')
