"""Project sealed Maria37-50 drafts without changing any source or prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria301_binding_inputs_v1.py').read_text(encoding='utf-8'), {
    'work/Maria_B0_B32_clean_20261109': 'work/Maria_B37_B50_clean_20261109',
    'all301_clean_meanings_andindependent_drafts_v1.json': 'all286_clean_meanings_andindependent_drafts_v2.json',
    "drafts['records_count'] == 301": "drafts['records_count'] == 286",
    'source_meanings_andlogical_drafts_all_saved_before_current_English_intake':
        'source_meanings_andlogical_drafts_all_saved_before_current_conversation_English_intake',
    '(292, 7, 2)': '(282, 0, 4)',
    'meanings=292': 'meanings=282',
    'source_objects=301, ordinary_speeches=292': 'source_objects=286, ordinary_speeches=282',
    'physical_style_alternatives=7, captions=2, complete_blocks=32':
        'physical_style_alternatives=0, captions=4, complete_blocks=14',
    'all301_meanings_anddrafts_unchanged': 'all286_meanings_anddrafts_unchanged',
    'Projected301 sealed drafts for unchanged native binders:292 speech/seven style/two menu;zero credit.':
        'Projected286 sealed drafts:282 speech/no styles/four menu captions;zero credit.',
})
exec(compile(source, __file__+'::same-schema-projection-disjoint286', 'exec'), globals())
