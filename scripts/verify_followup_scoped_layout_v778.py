"""Verify exact25-entry outputs through both voice parents and direct972 parent."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_followup_common_v778 import ROOT, MANUSCRIPT
from scripts.review_scheme_followup_v777 import ROOT as SOURCE
from scripts.verify_village_wrap_v608 import read, save


def formatter():
    source = inspect.getsource(original.format_case)
    marker = '    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    assert source.count(marker) == 1
    source = source.replace(marker, '''    n=row['message_id']
    parent=0x02054014 if n==972 else 0x02053D24 if 978<=n<=983 else 0x02053DB8
    for off,value in ((0x264,parent),(0x274,n),(0x27C,row['source_voice_table'] or 0)):
        u.mem_write(STACK+off,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)''')
    env = dict(original.__dict__)
    exec(compile(source, str(Path(__file__)), 'exec'), env)
    return env['format_case'], source


def main():
    rows = {r['message_id']: r for r in read(MANUSCRIPT)['records']}
    arm = (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == read(ROOT/'prospective_common_repack.json')['target_ARM9_sha256']
    matrix = SOURCE/'layouts_v1/native_layout_matrix.json'
    cases = read(matrix)['cases']
    assert len(cases) == 13699
    run, source = formatter()
    (ROOT/'scoped_format_case.py').write_text(source, encoding='utf-8')
    for i, case in enumerate(cases):
        if i % 64 == 0:
            u = machine(arm)
        result = run(u, rows[case['id']], tuple(bytes.fromhex(v) for v in case['source_values_hex']))
        assert not result['findings'] and result == case, (i, result)
    save(ROOT/'scoped_layout_verification.json', {
        'count': len(cases), 'all25_IDs': sorted(rows), 'target_ARM9_sha256': sha(arm),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'matrix_sha256': sha(matrix.read_bytes()),
        'all_production_outputs_printf_words_guards_and_ABI_exact_to_reviewed_layouts': True,
        'effective_program_sha256': sha(source.encode()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'actual_gameplay_pending': True, 'full_goal_complete': False})
    print('13699 production-parent/table layouts equal reviewed outputs without findings.', flush=True)


if __name__ == '__main__':
    main()
