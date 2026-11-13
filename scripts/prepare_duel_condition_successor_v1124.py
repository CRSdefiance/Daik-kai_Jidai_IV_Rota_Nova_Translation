"""Preserve the failed multline counterexample;keep original comparison flags."""
from pathlib import Path


def main():
    source = Path('scripts/duel_renderer_thumb_v1123.py').read_text(encoding='utf-8')
    target = Path('scripts/duel_renderer_thumb_v1124.py')
    assert not target.exists()
    before = 'ldr r0,[sp,#4]\ncmp r0,#1\nmovs r3,#0\nbne y_ready'
    assert source.count(before) == 1
    source = source.replace(before, 'ldr r0,[sp,#4]\nmovs r3,#0\ncmp r0,#1\nbne y_ready')
    source = source.replace("duel_renderer_thumb_v1123')", "duel_renderer_thumb_v1124')")
    target.write_text(source, encoding='utf-8')
    source = Path('scripts/probe_duel_thumb_equivalence_v1123.py').read_text(encoding='utf-8')
    target = Path('scripts/probe_duel_thumb_equivalence_v1124.py')
    assert not target.exists()
    source = source.replace('from scripts.duel_renderer_thumb_v1123 import', 'from scripts.duel_renderer_thumb_v1124 import')
    source = source.replace("duel_thumb_equivalence_v1123')", "duel_thumb_equivalence_v1124')")
    source = source.replace("'remaining_tail_not_yet_approved_without_incoming_reference_and_ownership_census': True,",
        "'remaining_tail_not_yet_approved_without_incoming_reference_and_ownership_census': True,\n"
        "        'earlier_multiline_counterexample':'work/analysis/duel_renderer_thumb_v1123/multiline_condition_failure.json',\n"
        "        'Thumb_MOVS_precedes_CMP_so_BNE_uses_original_line_count_condition':True,")
    target.write_text(source, encoding='utf-8')
    print('Created original-condition-preserving successor;rejected multiline prototype retained.')


if __name__ == '__main__':
    main()
