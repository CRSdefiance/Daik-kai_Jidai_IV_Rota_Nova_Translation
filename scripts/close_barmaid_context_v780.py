"""Close original callers and verify all114 native town/NPC guard outcomes."""

import inspect
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R6, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import close_barmaid_latent_context_v779 as original
from scripts.classify_barmaid_windows_v780 import ROOT
from scripts.context_barmaid_dialogue_v779 import CURRENT, ROOT as SOURCE
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save


def main():
    classified = read(ROOT/'classified_source_windows.json')
    assert classified['source_ROM_sha256'] == sha(CURRENT.read_bytes())
    program = inspect.getsource(original.main)
    before = "assert not any(refs[hex(a)][k] for k in ('absolute', 'ADR', 'Thumb_BL_BLX')), (hex(a), refs[hex(a)])"
    after = "assert not any(r for k in ('absolute','ADR','Thumb_BL_BLX') for r in refs[hex(a)][k] if [k,*r] not in exclusions),(hex(a),refs[hex(a)])"
    assert program.count(before) == 1
    program = program.replace(before, after)
    # Keep the original captured/source context;only proof output moves to V780.
    marker = "context = read(ROOT/'native_context.json')"
    assert program.count(marker) == 1
    program = program.replace(marker, f"context = read({str(SOURCE/'native_context.json')!r})")
    env = {**original.__dict__, 'ROOT': ROOT, 'exclusions': classified['exact_classified_references'],
           '__file__': str(Path(__file__).resolve())}
    (ROOT/'effective_caller_closure.py').write_text(program, encoding='utf-8')
    exec(compile(program, str(ROOT/'effective_caller_closure.py'), 'exec'), env)
    env['main']()
    refs = read(ROOT/'latent996_reference_leads.json')
    found = sorted([kind, *r] for group in refs.values() for kind, entries in group.items()
                   for r in entries if kind != 'ARM_branch')
    assert found == sorted(classified['exact_classified_references'])
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0x59E00, 0x59E10), (0xB65E4, 0xB6650), (0x34674, 0x34688)):
        assert arm[a:b] == clean[a:b]
    context = read(SOURCE/'native_context.json')
    raw = Path(context['pre_fixture_snapshot']['path']).read_bytes()
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    root, current = get(0xCB1A8), get(0x2E58C)
    fleet = root+4+132*current
    assert not bytes(u.mem_read(fleet+0x50, 1))[0] & 8
    results = []
    hook = u.hook_add(UC_HOOK_CODE, lambda c, p, s, d: c.emu_stop(), begin=STOP, end=STOP)
    try:
        for row in context['all114_native_city_information_lookups']:
            n, info = row['town_ID'], row['information_row']
            u.mem_write(fleet+0x3C, bytes((n,)))
            assert get(0xB65E4) == n
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.mem_write(STACK, struct.pack('<6I', 1, 2, 3, 4, 5, STOP))
            u.emu_start(BASE+0x59E00, BASE+0x59E10, count=10000)
            if info:
                assert u.reg_read(UC_ARM_REG_PC) == BASE+0x59E10
                assert u.reg_read(UC_ARM_REG_R6) == info and u.reg_read(UC_ARM_REG_SP) == STACK
            else:
                assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK+24
                assert u.reg_read(UC_ARM_REG_R0) == 0
            results.append({'supplied_CPU_town_ID': n, 'original_town_getter': n,
                            'information_row': info, 'original_guard_exits_without_barmaid': not bool(info)})
    finally:
        u.hook_del(hook)
    assert next(r for r in results if r['supplied_CPU_town_ID'] == 58)['original_guard_exits_without_barmaid']
    proof = read(ROOT/'latent996_caller_closure.json')
    proof.update({'exact_source_window_classification': str(ROOT/'classified_source_windows.json'),
                  'all114_original_town_getter_and_main_NPC_guard_cases': results,
                  'retained_latent996_context_classified': True,
                  'ordinary_996_activation_not_claimed': True,
                  'original_source_dispatch_and_catalog_unchanged': True,
                  'scope': 'Original static caller chain and initialized town catalog. Native guard cases use a one-byte CPU-only fleet-town input and modeled caller return frame;no emulator travel or earned story state.',
                  'effective_program_sha256': sha(program.encode()),
                  'original_producer_sha256': sha(Path(original.__file__).read_bytes()),
                  'producer_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT/'latent996_caller_closure.json', proof)
    print('Original caller chains and114 town/NPC guards verified;996 is retained latent text with no invented normal activation.', flush=True)


if __name__ == '__main__':
    main()
