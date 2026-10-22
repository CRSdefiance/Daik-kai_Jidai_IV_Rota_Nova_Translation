"""Native ABI/scope/modal/quantity and private-reference proof; research only."""

import inspect
import struct
from pathlib import Path
from types import SimpleNamespace

from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import refit_dialogue_runtime_v833 as runtime
from scripts import verify_palace_runtime_v796 as scope_probe
from scripts import verify_recruitment_runtime_v771 as status_probe
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_arrival_native_v792 import prepared, run
from scripts.verify_village_wrap_v608 import read, save

ROOT = runtime.ROOT
ROM = Path('out/all_routes_combined_v831_candidate.nds')


def scopes(old, new):
    source = inspect.getsource(scope_probe.scope)
    assert 'range(0x7B20,0x8490)' in source and 'range(0x65F0,0x6840)' in source
    source = source.replace('range(0x7B20,0x8490)', 'range(0x7B20,0x86B0)')
    source = source.replace('range(0x65F0,0x6840)', 'range(0x6480,0x6850)')
    bank = SimpleNamespace(**{**runtime.previous.bank.__dict__, 'STATUS': runtime.previous.STATUS})
    for label, arm, rows in (('current', old, runtime.previous.contract_rows), ('research', new, runtime.contract_rows)):
        folder = ROOT / f'{label}_scope'
        folder.mkdir(exist_ok=True)
        if (folder / 'scope_proof.json').exists():
            known = read(folder / 'scope_proof.json')
            assert known['ARM9_sha256'] == sha(arm) and known['effective_verifier_sha256'] == sha(source.encode())
            continue
        env = {**scope_probe.__dict__, 'ROOT': folder,
               'new': SimpleNamespace(bank=bank, contract_rows=rows)}
        exec(compile(source, __file__, 'exec'), env)
        env['scope'](arm)
        proof = read(folder / 'scope_proof.json')
        save(folder / 'scope_proof.json', {
            'cases': proof['cases'], 'exact_parent_ID_pointer_stride_ABI_SP_LR_cases_pass': True,
            'source_row_values': [list(r[:3]) + [list(r[3])] for r in rows()],
            'effective_verifier_sha256': sha(source.encode()), 'ARM9_sha256': sha(arm),
            'scope': 'All3668 numeric IDs for four parents;complete queued low-address windows including8680,source pointer alignment and wrong-parent/high-word controls.'})
    before = {p: (o, h, set(v)) for p, o, h, v in runtime.previous.contract_rows()}
    after = {p: (o, h, set(v)) for p, o, h, v in runtime.contract_rows()}
    changes = {}
    for p, (off, high, values) in after.items():
        old_off, old_high, old_values = before[p]
        assert (off, high) == (old_off, old_high) and old_values <= values
        if values != old_values:
            changes[hex(p)] = sorted(values - old_values)
    assert changes == {'0x2054014': list(range(1263, 1268)), '0x2053db8': [0x8680]}
    save(ROOT / 'scope_delta.json', {'only_new_exact_memberships': changes,
                                     'all_other_source_memberships_identical': True})


def modal_equivalence(old, new):
    text = b' Complete words and original leading and trailing letters stay intact across the entire modal box.'
    cases = []
    for number in range(3668):
        if number % 32 == 0:
            a, b = prepared(old), prepared(new)
        x, y = run(a, 0x020546E8, number, text), run(b, 0x020546E8, number, text)
        assert x == y, (number, x, y)
        cases.append({'message_id': number, 'output_sha256': sha(y[0]), 'ordinary_wrap_selected': y[1]})
    parents = []
    for parent in (0, 0xFFFFFFFF, 0x120546E8, 0x0205469C, 0x02054720, 0x02054764, 0x02054014):
        a, b = prepared(old), prepared(new)
        for number in (*range(127, 135), *range(269, 273), *range(287, 298), 321, 327, *range(344, 351), 0xFFFFFFFF):
            assert run(a, parent, number, text) == run(b, parent, number, text)
            parents.append([parent, number])
    save(ROOT / 'modal_equivalence.json', {
        'all3668_complete_native_output_and_wrap_choices_identical': cases,
        'wrong_parent_and_edge_controls': parents,
        '128_byte_wrapper_and12_byte_filter_move_preserve_all_original_modal_behavior': True,
        'complete_output_input_guards_and_callee_saved_ABI_pass': True})
    print('All3668 modal outputs and wrong-parent controls equal current.', flush=True)


def quantities(old, new, plan):
    raw_path = Path('work/emulation_v193/refit_editorial_v831_after/frame_020000_arm9_ram.bin')
    raw = raw_path.read_bytes()
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)

    def loaded(arm, changed):
        cpu = machine(arm)
        cpu.mem_write(BASE, raw)
        if changed:
            for patch in plan['patches']:
                cpu.mem_write(patch['address'], bytes.fromhex(patch['target_hex']))
        return cpu

    a, b = loaded(old, False), loaded(new, True)
    values = (0, 1, 2, 9, 10, 16, 99, 1000, 65535, 1000000, 2147483647)
    inputs = [(ret, value) for ret in (*runtime.PRICE_RETURNS, runtime.DAY_RETURN) for value in values]
    inputs += [(runtime.NEW_DAY_RETURN, value) for value in range(256)]
    cases = []
    for ret, number in inputs:
        if ret == runtime.NEW_DAY_RETURN and number == 0:
            # This baseline changes its scratch thunk from the helper to the
            # original getter. Use fresh machines rather than a translated TB
            # cached from the previous direct-branch target.
            a, b = loaded(old, False), loaded(new, True)
        outputs, pointers, writes = [], [], []
        for cpu, target in ((a, BASE + 0xABF50 if ret == runtime.NEW_DAY_RETURN else runtime.QUANTITY), (b, runtime.QUANTITY)):
            thunk = 0x02464000
            cpu.mem_write(thunk, bytes(ka.asm(f'ldr lr,[pc,#0];b {target};.word {ret}', thunk)[0]))
            cpu.mem_write(ret, bytes(ka.asm(f'b {STOP}', ret)[0]))
            touched = set()
            hook = cpu.hook_add(UC_HOOK_MEM_WRITE, lambda c, access, at, size, value, unused: touched.update(range(at, at + size)))
            try:
                call(cpu, thunk - BASE, (number,), instruction_limit=100000)
            finally:
                cpu.hook_del(hook)
            p = cpu.reg_read(UC_ARM_REG_R0)
            output = bytes(cpu.mem_read(p, 80)).split(b'\0')[0]
            outputs.append(output)
            pointers.append(p)
            writes.append(touched)
        digits = str(number).translate(str.maketrans('0123456789', '０１２３４５６７８９')).encode('cp932')
        is_day = ret in (runtime.DAY_RETURN, runtime.NEW_DAY_RETURN)
        suffix = (' day' if number == 1 else ' days') if is_day else (' gold coin' if number == 1 else ' gold coins')
        assert outputs[1] == digits + suffix.encode()
        assert outputs[0] == (digits if ret == runtime.NEW_DAY_RETURN else outputs[1]), (hex(ret), number, outputs)
        bare_pointer = pointers[0] if ret == runtime.NEW_DAY_RETURN else pointers[0] + len(suffix)
        lo, hi = bare_pointer + len(digits) - 127, bare_pointer + len(digits) + 1
        assert lo <= pointers[1] < hi and pointers[1] + len(outputs[1]) < hi
        assert not (writes[1] - writes[0] - set(range(lo, hi)) - set(range(STACK - 512, STACK)))
        cases.append({'return_PC': ret, 'value': number, 'output_hex': outputs[1].hex(),
                      'original_128_byte_numeric_buffer': [lo, hi],
                      'earlier_seven_callers_exact_or_new_duration_digits_plus_correct_unit': True,
                      'native_callee_saved_ABI_and_write_bounds_pass': True})
    save(ROOT / 'quantity_equivalence.json', {'cases': cases,
                                              'original_fullwidth_digits_and_native_numeric_buffer_preserved': True,
                                              'all256_new_duration_bytes_and77_previous_cases_pass': True,
                                              'source_RAM': str(raw_path), 'source_RAM_sha256': sha(raw)})
    print('77 prior quantity cases and all256 new duration values pass.', flush=True)


def storage(old, new, plan):
    owned = read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    owned += read('work/analysis/shipyard_storage_v760/owned_source_storage.json')['owned_banks']
    owned += [[runtime.modal.ADDRESS, runtime.modal.ADDRESS + 128]]
    existing_banks = [[runtime.previous.LITERAL, runtime.previous.LITERAL + 168],
                      [runtime.previous.OLD_LITERAL, runtime.previous.END],
                      [runtime.QUANTITY, runtime.QUANTITY + 104],
                      [runtime.previous.bank.GATE, runtime.previous.bank.GATE + 164]]
    assert all(any(lo <= a and b <= hi for lo, hi in owned) for a, b in existing_banks)
    restored = bytearray(new)
    for patch in plan['patches']:
        at = patch['address'] - BASE
        restored[at:at + len(bytes.fromhex(patch['source_hex']))] = bytes.fromhex(patch['source_hex'])
    restored_code = MainCodeFile(bytes(restored), BASE)
    restored_code.sections[4].data = MainCodeFile(old, BASE).sections[4].data
    assert bytes(restored_code.save()) == old
    source, target = NdsImage.open(ROM), NdsImage.open(ROM)
    target.rom.arm9 = new
    # A quantity helper is private: identify every incoming reference, including
    # ARM/Thumb branches, data pointers and ADR across resident code/overlays.
    spans = [[runtime.QUANTITY, runtime.QUANTITY + 104]]
    before_refs, after_refs = [census(r, spans, spans) for r in (source, target)]
    external = lambda refs: sorted(row for row in refs if not row[-1])
    before, after = external(before_refs), external(after_refs)
    added = [r for r in after if r not in before]
    removed = [r for r in before if r not in after]
    assert added == [['ARM_branch', 'section0', runtime.NEW_DAY_RETURN - 4, runtime.QUANTITY, False]], added
    assert not removed
    branch_sources = {row[2] for row in after if row[0] in ('ARM_branch', 'Thumb_BL_BLX')}
    assert branch_sources == {r - 4 for r in runtime.returns_for_proof()}
    source_all, target_all = [census(r, existing_banks, owned) for r in (source, target)]
    assert [r for r in external(target_all) if r not in external(source_all)] == added
    assert not [r for r in external(source_all) if r not in external(target_all)]
    save(ROOT / 'storage_and_quantity_closure.json', {
        'all_repacked_code_data_within_previously_proven_owned_allocations': existing_banks,
        'all_declared_patches_restored_recover_exact_current_ARM9': True,
        'quantity_reference_census_before': before_refs, 'quantity_reference_census_after': after_refs,
        'only_new_external_reference': added, 'no_removed_external_reference': True,
        'private_exact_eight_caller_closure': sorted(branch_sources),
        'all_repacked_bank_external_references_before': external(source_all),
        'all_repacked_bank_external_references_after': external(target_all),
        'all_old_external_bank_references_preserved_only_declared_new_BL': True,
        'all_original_sections_BSS_cache_and123040_staged_bytes_unchanged': True})
    print('Owned footprints, exact restore and eight-caller quantity closure pass.', flush=True)


def status(new):
    bank = SimpleNamespace(**{**runtime.previous.bank.__dict__, 'STATUS': runtime.previous.STATUS})
    source = inspect.getsource(status_probe.field_contracts)
    source = source.replace('u.emu_start(runtime.STATUS,STOP', 'u.emu_start(runtime.STATUS|1,STOP')
    source = source.replace('STACK-BASE-32:STACK-BASE', 'STACK-BASE-36:STACK-BASE')

    def make(arm, changed=False, raw=None):
        cpu = prepared(arm)
        if raw is not None:
            cpu.mem_write(BASE, raw)
        return cpu

    env = {**status_probe.__dict__, 'runtime': bank, 'make': make,
           'ROOT': Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(source, __file__, 'exec'), env)
    cases = env['field_contracts'](new)
    assert len(cases) == 140
    save(ROOT / 'status_phrase_contracts.json', {'count': 140, 'cases': cases,
                                                'complete12_status_phrases_and_source_ABI_memory_contracts_pass': True,
                                                'effective_verifier_sha256': sha(source.encode())})
    print('All140 status phrase contracts pass after table-index relocation.', flush=True)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    old = NdsImage.open(ROM).read_file('/__arm9__.bin')
    new, plan = runtime.apply(old)
    assert new == (ROOT / 'ARM9_RESEARCH_ONLY.bin').read_bytes()
    scopes(old, new)
    modal_equivalence(old, new)
    quantities(old, new, plan)
    storage(old, new, plan)
    status(new)
    save(ROOT / 'native_runtime_verification.json', {
        'source_ARM9_sha256': sha(old), 'research_ARM9_sha256': sha(new),
        'runtime_sha256': sha(Path(runtime.__file__).read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'new_prose_fonts_COMMON_registration_patch_and_actual_scenes_pending': True,
        'full_goal_complete': False})
    print('V833 bounded runtime native verification complete;no ROM release or new prose completion claim.', flush=True)


if __name__ == '__main__':
    main()
