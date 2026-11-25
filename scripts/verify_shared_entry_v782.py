"""Recheck the actual original call target and trampoline before private dispatch."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.recruitment_editorial_runtime import ENTRY
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_machine_scoped_v764 import machine
from scripts.register_shared_release_v782 import ROOT, MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save
import re


def main():
    path = ROOT/'production_layout/effective_format_case.py'
    source = path.read_text(encoding='utf-8')
    old, new = 'call(u, ENTRY - BASE,', 'call(u, 0x01FFCF3C - BASE,'
    assert source.count(old) == 1
    source = source.replace(old, new)
    env = {**original.__dict__, 'ENTRY': ENTRY, 're': re}
    exec(compile(source, str(ROOT/'full_entry_format_case.py'), 'exec'), env)
    (ROOT/'full_entry_format_case.py').write_text(source, encoding='utf-8')
    arm = (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    matrix = read(ROOT/'production_layout/verification.json')
    assert sha(arm) == matrix['research_ARM9_sha256']
    rows = {r['message_id']: r for r in read(MANUSCRIPT)['records']}
    for i, case in enumerate(matrix['cases']):
        if i % 64 == 0:
            u = machine(arm)
        result = env['format_case'](u, rows[case['id']], tuple(bytes.fromhex(v) for v in case['source_values_hex']))
        assert result == case
    save(ROOT/'full_entry_layout_verification.json', {
        'research_ARM9_sha256': sha(arm), 'native_original_call_target': 0x01FFCF3C,
        'all857_original_target_trampoline_and_private_dispatch_outputs_exact': True,
        'cases': len(matrix['cases']), 'effective_program_sha256': sha(source.encode()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('All857 original call-target/trampoline/dispatcher cases match.', flush=True)


if __name__ == '__main__':
    main()
