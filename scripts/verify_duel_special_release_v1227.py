"""Exact combined ancestry,15 special paragraphs and clean-input patch proof."""
import inspect
from pathlib import Path
from dk4tool.patch import duel_special_editorial as owned
from dk4tool.patch.duel_bark_editorial import current_entries as previous_entries
from scripts.duel_special_layout_v1216 import IDS, compiled
from scripts import verify_duel_bark_release_v1208 as previous


def main():
    source = inspect.getsource(previous.main)
    replacements = {
        'all-routes-unified-v1206': 'all-routes-unified-v1224',
        'all16_exact_compiled_reactions_and3652_unselected_texts_preserved': 'all15_exact_special_paragraphs_and3653_unselected_texts_preserved',
        'only_COMMON21_metadata_and_owned108_front_changed': 'only_COMMON22_23_metadata_and_source_owned_helper64_front108_changed',
        'ordinary_startup_original_timed_feedback_and_completion_credit_pending': 'ordinary_startup_original_special_and_completion_credit_pending',
        'V1206 combined ancestry': 'V1224 combined ancestry',
    }
    for old, new in replacements.items():
        assert source.count(old) >= 1
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'owned': owned,
        'previous_entries': previous_entries, 'IDS': IDS, 'compiled': compiled,
        'ROOT': Path('work/analysis/duel_special_release_v1223'),
        'ROM': Path('out/all_routes_combined_v1224_candidate.nds'),
        'OLD': Path('out/all_routes_combined_v1206_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
