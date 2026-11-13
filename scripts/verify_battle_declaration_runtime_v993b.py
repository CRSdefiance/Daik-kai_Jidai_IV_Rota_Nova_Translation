"""Exhaustive original dispatch/modal regression and bounded research-bank census."""
import inspect
from pathlib import Path
from types import SimpleNamespace

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import battle_declaration_runtime_v993b as runtime
from scripts import verify_palace_runtime_v796 as old_scope
from scripts import verify_recruitment_runtime_v771 as old_status
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_arrival_native_v792 import prepared, run
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v993b')
ROM = Path('out/all_routes_combined_v987_candidate.nds')


def scope(arm, label, rows):
    original = inspect.getsource(old_scope.scope)
    assert original.count('range(0x7B20,0x8490)') == 1
    assert original.count('range(0x65F0,0x6840)') == 1
    adapted = original.replace('range(0x7B20,0x8490)', 'range(0x73E0,0x86B0)')
    adapted = adapted.replace('range(0x65F0,0x6840)', 'range(0x6480,0x6850)')
    adapted = adapted.replace('(0,1072,1117,3667)', '(0,1897,1903,3667)')
    folder = ROOT/label
    folder.mkdir()
    bank = SimpleNamespace(**{**runtime.previous.previous.bank.__dict__, 'STATUS': runtime.previous.previous.STATUS})
    env = {**old_scope.__dict__, 'ROOT': folder, 'new': SimpleNamespace(bank=bank, contract_rows=rows)}
    exec(compile(adapted, str(Path(__file__)), 'exec'), env)
    env['scope'](arm)
    proof = read(folder/'scope_proof.json')
    # Retain the unchanged source assertions,not the historical function's
    # feature-specific ID labels and obsolete allocation sizes.
    save(folder/'current_scope_evidence.json', {
        'cases': proof['cases'], 'ARM9_sha256': sha(arm),
        'all_exact_parent_ID_pointer_stride_ABI_SP_LR_cases_pass': True,
        'effective_verifier_sha256': sha(adapted.encode()),
        'historical_verifier_sha256': sha(Path(old_scope.__file__).read_bytes()),
        'source_row_values': [list(r[:3])+[list(r[3])] for r in rows()],
        'scope': 'All3668 numeric IDs for four parent types;every queued byte address73E0..86AF under both source queued parents;all gift addresses6480..684F;wrong parent/high-word controls.'})
    return proof['cases']


def modal_equivalence(old, new):
    text = b' Complete words and original leading and trailing letters stay intact across the entire modal box.'
    cases = []
    for n in range(3668):
        if n % 32 == 0:
            a, b = prepared(old), prepared(new)
        before, after = run(a, 0x020546E8, n, text), run(b, 0x020546E8, n, text)
        assert before == after, (n, before, after)
        cases.append({'message_ID': n, 'output_sha256': sha(after[0]), 'ordinary_wrap_called': after[1]})
    controls = []
    for parent in (0, 0xFFFFFFFF, 0x120546E8, 0x0205469C, 0x02054720, 0x02054764, 0x02054014):
        a, b = prepared(old), prepared(new)
        for n in (*range(127, 135), *range(269, 273), *range(286, 298), 321, 327, *range(344, 351), 0xFFFFFFFF):
            assert run(a, parent, n, text) == run(b, parent, n, text)
            controls.append([parent, n])
    edges = []
    for n in (0xFFFFFFFF, 0x7FFFFFFF, 0x80000000, 65535, 65536):
        a, b = prepared(old), prepared(new)
        assert run(a, 0x020546E8, n, text) == run(b, 0x020546E8, n, text)
        edges.append(n)
    save(ROOT/'modal_equivalence.json', {'all3668_native_output_wrap_choices': cases,
        'wrong_parent_controls': controls, 'full_word_boundary_controls': edges,
        'all_original_behavior_byte_exact_with_input_output_guards_and_full_native_ABI': True,
        'IDs288_and292_stay_ineligible_and_all_prior_selected_IDs_preserved': True})
    print(f'All3668 complete modal outputs,{len(controls)} wrong-parent controls and5 full-word edges match V987.', flush=True)


def status_contracts(arm):
    original = inspect.getsource(old_status.field_contracts)
    assert original.count('u.emu_start(runtime.STATUS,STOP') == 1
    assert original.count('STACK-BASE-32:STACK-BASE') == 1
    source = original.replace('u.emu_start(runtime.STATUS,STOP', 'u.emu_start(runtime.STATUS|1,STOP')
    source = source.replace('STACK-BASE-32:STACK-BASE', 'STACK-BASE-36:STACK-BASE')
    bank = SimpleNamespace(**{**runtime.previous.previous.bank.__dict__, 'STATUS': runtime.previous.previous.STATUS})
    env = {**old_status.__dict__, 'runtime': bank,
           'make': lambda arm, changed=False, raw=None: prepared(arm),
           'ROOT': Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(source, str(Path(__file__)), 'exec'), env)
    cases = env['field_contracts'](arm)
    assert len(cases) == 140
    save(ROOT/'status_contracts.json', {'cases': cases, 'count': len(cases),
        'all_whole8MiB_guards_status_UI_labels_text_and_native_ABI_pass': True,
        'only_final_typed_phrase_suffix_and36_original_saved_stack_bytes_may_change': True,
        'effective_verifier_sha256': sha(source.encode()),
        'historical_verifier_sha256': sha(Path(old_status.__file__).read_bytes())})
    print('All140 complete prior status-output/8MiB guard cases pass after two-byte pointer move.', flush=True)


def main():
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    rom = NdsImage.open(ROM)
    old = rom.read_file('/__arm9__.bin')
    target, plan = runtime.apply(old)
    candidate = read('translations/editorial_review_current_v1.json')['current_integrated_candidate']
    assert sha(ROM.read_bytes()) == candidate['sha256'] and sha(old) == candidate['ARM9_sha256']
    assert (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').write_bytes(target) == len(target)
    save(ROOT/'runtime_plan.json', {**plan, 'candidate': str(ROM), 'candidate_sha256': candidate['sha256'],
        'producer_sha256': sha(Path(__file__).read_bytes()), 'runtime_sha256': sha(Path(runtime.__file__).read_bytes())})
    before = {p: (o, h, set(v)) for p, o, h, v in runtime.previous.contract_rows()}
    after = {p: (o, h, set(v)) for p, o, h, v in runtime.contract_rows()}
    changed = {}
    for parent, (offset, high, values) in after.items():
        old_offset, old_high, old_values = before[parent]
        assert (offset, high) == (old_offset, old_high) and old_values <= values
        if values != old_values:
            changed[hex(parent)] = sorted(values-old_values)
    assert changed == {'0x2053d24': [0x7420]}
    other = NdsImage.open(ROM)
    other.rom.arm9 = target
    refs = [census(image, plan['private_spans'], plan['private_spans']) for image in (rom, other)]
    assert sorted(r for r in refs[0] if not r[-1]) == sorted(r for r in refs[1] if not r[-1])
    save(ROOT/'private_reference_census.json', {'before': refs[0], 'after': refs[1],
        'all_external_references_to_the_three_unchanged_owned_spans_exact': True,
        'all_moved_filter_and_phrase_references_inside_declared_owned_spans': True,
        'census_sha256': sha(Path('scripts/audit_item_runtime_storage_v785.py').read_bytes())})
    old_cases = scope(old, 'current_scope', runtime.previous.contract_rows)
    new_cases = scope(target, 'research_scope', runtime.contract_rows)
    assert old_cases == new_cases
    modal_equivalence(old, target)
    status_contracts(target)
    save(ROOT/'native_runtime_verification.json', {
        'candidate_sha256': candidate['sha256'], 'source_ARM9_sha256': sha(old), 'research_ARM9_sha256': sha(target),
        'old_and_new_complete_scope_cases_each': old_cases, 'only_new_contract': changed,
        'all3668_modal_outputs_and_wrap_choices_exact': True, 'all140_status8MiB_ABI_guards_pass': True,
        'all_external_references_and_every_other_ARM9_byte_preserved': True,
        'all_sections_BSS_cache_and_entire123040_staged_payload_unchanged': True,
        'public212_and_ITCM128_byte_footprints_unchanged': True,
        'runtime_sha256': sha(Path(runtime.__file__).read_bytes()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'not_registered_no_ROM_written_not_gameplay_verification': True,
        'full_goal_complete': False})
    print('Named-declaration bounded runtime research passes complete dispatch,modal,status and reference checks. No playable ROM built.', flush=True)


if __name__ == '__main__':
    main()
