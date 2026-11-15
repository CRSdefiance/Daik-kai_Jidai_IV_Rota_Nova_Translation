"""Extend the original caller/name proof to Bribe on the current candidate."""

import inspect
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_scheme_input_contract_v776 as original
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_machine_scoped_v764 import machine
from scripts.review_scheme_followup_v777 import ROOT, CURRENT
from scripts.verify_village_wrap_v608 import read, save


def main():
    context = read(ROOT/'native_context.json')
    assert context['candidate_sha256'] == sha(CURRENT.read_bytes())
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    # A bytewise Thumb scan also decodes this original ARM B instruction as
    # Thumb BLX. Bind the one exclusion to the complete original ARM thunk.
    assert arm[0x89614:0x89624] == clean[0x89614:0x89624] == bytes.fromhex('04c09fe50c0080e0cdf700eab0ffffff')
    odd = []
    even = []
    for name, base, raw in units(rom):
        for at in range(len(raw)-3):
            target = struct.unpack_from('<I', raw, at)[0]
            if 0x02089614 <= (target & ~1) < 0x02089624:
                (odd if target & 1 else even).append([name, base+at, target])
    assert not odd and any(r[2] == 0x02089614 for r in even)
    u = machine(arm)
    u.reg_write(UC_ARM_REG_R0, 0x02401050)
    observed = []
    def stop(c, at, size, unused):
        observed.append({'pc': at, 'r0': c.reg_read(UC_ARM_REG_R0), 'Thumb': bool(c.reg_read(UC_ARM_REG_CPSR) & 32)})
        c.emu_stop()
    hook = u.hook_add(UC_HOOK_CODE, stop, begin=0x020C7558, end=0x020C7558)
    u.emu_start(0x02089614, 0x02089624, count=20)
    u.hook_del(hook)
    assert observed == [{'pc': 0x020C7558, 'r0': 0x02401000, 'Thumb': False}]
    source = inspect.getsource(original.main)
    replacements = {
        "path=Path('out/all_routes_combined_v773_candidate.nds')": f'path=Path({str(CURRENT)!r})',
        "raw=Path(context['read_only_snapshot']['path']).read_bytes()":
            f"snapshot=read({str(ROOT/'native_context.json')!r})['pre_fixture_snapshot']\n    raw=Path(snapshot['path']).read_bytes()",
        "assert sha(raw)==context['read_only_snapshot']['sha256']": "assert sha(raw)==snapshot['sha256']",
        "print('Five private calling paths": "print('Six private calling paths",
        "if a is not None and not a<=base+at<FUNCTIONS[a][0]:refs[hex(a)]['Thumb_BL_BLX'].append([name,base+at,target])":
            "if a is not None and not a<=base+at<FUNCTIONS[a][0] and (name,base+at,target)!=('section0',0x0208961C,0x02056A20):refs[hex(a)]['Thumb_BL_BLX'].append([name,base+at,target])",
    }
    for old, new in replacements.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    functions = {**original.FUNCTIONS, 0x02056998: (0x02056AE8, 0x0205703C)}
    env = {**original.__dict__, 'ROOT': ROOT, 'FUNCTIONS': functions}
    effective = ROOT/'effective_input_contract.py'
    effective.write_text(source, encoding='utf-8')
    exec(compile(source, str(effective), 'exec'), env)
    env['main']()
    path = ROOT/'input_contract.json'
    proof = read(path)
    assert proof['source_ROM_sha256'] == context['candidate_sha256']
    proof.update({
        'six_original_paths_include_Bribe_function_02056998': True,
        'current_ROM_pre_fixture_snapshot': context['pre_fixture_snapshot'],
        'source_research_producer_sha256': sha(Path(original.__file__).read_bytes()),
        'effective_program_sha256': sha(source.encode('utf-8')),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'new13699_prospective_layouts': str(ROOT/'layouts_v1/verification.json'),
        'new_production_dispatcher_and_gameplay_pending': True})
    proof['one_Thumb_scan_candidate_proven_original_ARM_thunk'] = {
        'scan_candidate': ['section0', 0x0208961C, 0x02056A20],
        'source_current_complete_thunk_hex': arm[0x89614:0x89624].hex(),
        'native_ARM_execution': observed, 'even_pointer_references': even,
        'odd_Thumb_pointer_references': odd,
        'scope': 'Only this exact unchanged original ARM branch instruction is classified;no general Thumb-reference waiver.'}
    save(path, proof)
    print('Bribe target name uses the original nonplayer fixed-name path;no edited-player-name waiver required.', flush=True)


if __name__ == '__main__':
    main()
