"""Successor uses unchanged FE formatter metadata from its original reviewed row."""
from pathlib import Path

SOURCE = Path('scripts/complete_lil_lessons_contextual_v1989.py')

if __name__ == '__main__':
    assert Path('work/analysis/lil_lessons_contextual_completion_v1989').exists()
    assert Path('translations/lil_lessons_contextual_final_review_v1.json').exists()
    text = SOURCE.read_text(encoding='utf-8')
    old = "            historical['formatted_markup'] = native_cases[current['id']]['formatted_markup']"
    new = """            native = native_cases[current['id']]
            if 'formatted_markup' in native:
                historical['formatted_markup'] = native['formatted_markup']
            else:
                assert current['source_presentation_prefix_hex'] == 'fe'
                assert current['current_text_hex'] == old_rows[current['id']]['current_text_hex']
                historical['formatted_markup'] = old_rows[current['id']]['formatted_markup']"""
    assert text.count(old) == 1
    text = text.replace(old,new)
    text = text.replace('lil_lessons_contextual_completion_v1989','lil_lessons_contextual_completion_v1989b')
    text = text.replace('lil_lessons_contextual_final_review_v1.json','lil_lessons_contextual_final_review_v2.json')
    old = "        all_ROMs_and_earlier_translations_preserved=True,full_goal_remains_active=True,"
    new = """        all_ROMs_and_earlier_translations_preserved=True,full_goal_remains_active=True,
        frozen_partial1989_review_preserved='translations/lil_lessons_contextual_final_review_v1.json',
        frozen1989_failed_before_ledger_commit_on_FE_distinct_formatter_schema=True,"""
    assert text.count(old) == 1
    text = text.replace(old,new)
    text = text.replace('V1989','V1989b')
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
