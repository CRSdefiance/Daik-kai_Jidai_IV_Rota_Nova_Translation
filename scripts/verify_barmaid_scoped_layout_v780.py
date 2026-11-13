"""Verify every supplied layout through the actual direct parent/ID dispatcher."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_barmaid_common_v780 import ROOT, MANUSCRIPT
from scripts.context_barmaid_dialogue_v779 import ROOT as SOURCE
from scripts.verify_village_wrap_v608 import read, save


def formatter():
    source = inspect.getsource(original.format_case)
    marker = '    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    assert source.count(marker) == 1
    source = source.replace(marker, '''    for off,value in ((0x264,0x02054014),(0x274,row['message_id']),(0x27C,0)):
        u.mem_write(STACK+off,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)''')
    env = dict(original.__dict__)
    exec(compile(source, str(Path(__file__)), 'exec'), env)
    return env['format_case'], source


def main():
    doc = read(MANUSCRIPT)
    rows = {r['message_id']: r for r in doc['records']}
    arm = (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == read(ROOT/'prospective_common_repack.json')['target_ARM9_sha256']
    matrix_path = SOURCE/'layouts_v1/native_layout_matrix.json'
    cases = read(matrix_path)['cases']
    assert len(cases) == 273
    typed = read(SOURCE/'layouts_v1/name_token_findings.json')
    recognized = [r['case'] for r in typed['five_naive_article_diagnostics_are_exactly_bound_to_name_bytes']]
    assert not typed['unresolved_prose_or_layout_findings'] and typed['literal_prose_negative_control_rejected']
    run, source = formatter()
    (ROOT/'scoped_format_case.py').write_text(source, encoding='utf-8')
    for i, case in enumerate(cases):
        if i % 64 == 0:
            u = machine(arm)
        actual = run(u, rows[case['id']], tuple(bytes.fromhex(v) for v in case['source_values_hex']))
        assert actual == {k: v for k, v in case.items() if k != 'supplied_editor_boundary_case'}, (i, actual)
        if actual['findings']:
            assert case in recognized
    save(ROOT/'scoped_layout_verification.json', {
        'count': len(cases), 'all31_IDs': sorted(rows), 'target_ARM9_sha256': sha(arm),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'matrix_sha256': sha(matrix_path.read_bytes()),
        'all_outputs_printf_words_guards_ABI_exact_to_reviewed_layouts': True,
        'five_raw_name_initial_diagnostics_preserved_with_exact_typed_proof': True,
        'unresolved_layout_findings': [], 'effective_program_sha256': sha(source.encode()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'actual_gameplay_pending': True, 'full_goal_complete': False})
    print('273 production-parent/ID layouts exact,including16-byte and CP932 names;typed diagnostics remain source-bound.', flush=True)


if __name__ == '__main__':
    main()
