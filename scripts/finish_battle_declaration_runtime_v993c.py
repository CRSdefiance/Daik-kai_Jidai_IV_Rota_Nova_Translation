"""Finish only the remaining status regression;preserve prior complete native matrices."""
import inspect
from pathlib import Path
from types import SimpleNamespace

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import battle_declaration_runtime_v993b as runtime
from scripts import verify_recruitment_runtime_v771 as historical
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v993c')
PREVIOUS = Path('work/analysis/battle_declaration_v993b')
ROM = Path('out/all_routes_combined_v987_candidate.nds')


def main():
    assert not ROOT.exists()
    arm = (PREVIOUS/'ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()
    old = NdsImage.open(ROM).read_file('/__arm9__.bin')
    rebuilt, plan = runtime.apply(old)
    assert rebuilt == arm
    source_paths = [PREVIOUS/p for p in ('runtime_plan.json', 'private_reference_census.json',
        'current_scope/current_scope_evidence.json', 'research_scope/current_scope_evidence.json', 'modal_equivalence.json')]
    proofs = [read(p) for p in source_paths]
    assert proofs[0]['research_ARM9_sha256'] == sha(arm)
    assert proofs[0]['runtime_sha256'] == sha(Path(runtime.__file__).read_bytes())
    assert proofs[1]['all_external_references_to_the_three_unchanged_owned_spans_exact']
    assert proofs[2]['cases'] == proofs[3]['cases'] == 54904
    assert proofs[2]['ARM9_sha256'] == sha(old) and proofs[3]['ARM9_sha256'] == sha(arm)
    assert proofs[2]['source_row_values'] == [list(r[:3])+[list(r[3])] for r in runtime.previous.contract_rows()]
    assert proofs[3]['source_row_values'] == [list(r[:3])+[list(r[3])] for r in runtime.contract_rows()]
    assert len(proofs[4]['all3668_native_output_wrap_choices']) == 3668
    assert len(proofs[4]['wrong_parent_controls']) == 238 and len(proofs[4]['full_word_boundary_controls']) == 5
    assert proofs[4]['all_original_behavior_byte_exact_with_input_output_guards_and_full_native_ABI']
    source = inspect.getsource(historical.field_contracts)
    assert source.count('u.emu_start(runtime.STATUS,STOP') == 1
    # Both the before and after slices use the saved-stack span. The previous
    # unexecuted adapter wrongly expected one textual occurrence,not two.
    assert source.count('STACK-BASE-32:STACK-BASE') == 2
    adapted = source.replace('u.emu_start(runtime.STATUS,STOP', 'u.emu_start(runtime.STATUS|1,STOP')
    adapted = adapted.replace('STACK-BASE-32:STACK-BASE', 'STACK-BASE-36:STACK-BASE')
    bank = SimpleNamespace(**{**runtime.previous.previous.bank.__dict__, 'STATUS': runtime.previous.previous.STATUS})
    env = {**historical.__dict__, 'runtime': bank, 'make': lambda arm, changed=False, raw=None: prepared(arm),
           'ROOT': Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(adapted, str(Path(__file__)), 'exec'), env)
    cases = env['field_contracts'](arm)
    assert len(cases) == 140
    ROOT.mkdir(parents=True)
    status = ROOT/'status_contracts.json'
    save(status, {'cases': cases, 'count': len(cases),
        'all_whole8MiB_guards_status_UI_labels_text_and_native_ABI_pass': True,
        'only_typed_phrase_suffix_and36_saved_stack_bytes_may_change': True,
        'effective_verifier_sha256': sha(adapted.encode()), 'historical_verifier_sha256': sha(Path(historical.__file__).read_bytes()),
        'predecessor_failure': 'V993b completed both54904-case dispatch matrices and all3668 modal outputs,238 wrong-parent controls and5 full-word edges. It then stopped before status execution on an adapter preflight assertion expecting one occurrence of a stack-slice expression that actually occurs twice. No native status failure was observed.',
        'no_successful_native_matrix_repeated_or_coverage_added': True})
    source_paths.append(status)
    save(ROOT/'native_runtime_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'source_ARM9_sha256': sha(old), 'research_ARM9_sha256': sha(arm),
        'all_completed_source_proofs': {str(p): sha(p.read_bytes()) for p in source_paths},
        'old_and_new_complete_scope_cases_each': 54904,
        'only_new_contract': {'parent02053D24': [0x02117420]},
        'all3668_modal_outputs_and_wrap_choices_exact': True,
        'all238_wrong_parent_and5_full_word_edge_controls_exact': True,
        'all140_status8MiB_ABI_guards_pass': True,
        'all_external_references_and_every_other_ARM9_byte_preserved': True,
        'all_sections_BSS_cache_and_entire123040_staged_payload_unchanged': True,
        'public212_and_ITCM128_byte_footprints_unchanged': True,
        'runtime': str(Path(runtime.__file__).relative_to(Path.cwd())),
        'runtime_sha256': sha(Path(runtime.__file__).read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'native_font_dynamic_name_matrix_registered_integration_and_actual_scenes_pending': True,
        'not_registered_no_ROM_written_not_gameplay_verification': True,
        'completed_entries_added': 0, 'full_goal_complete': False})
    print('Bounded runtime research complete:54904 source+54904 research selector cases,3668 byte-exact prior modal outputs,238 wrong-parent+5 edges and140 status/8MiB guards pass. Fonts,registration and actual scenes pending.')


if __name__ == '__main__':
    main()
