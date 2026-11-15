"""Use the existing clean-source seal contract for Rafael's final SC0 intake."""
import inspect
from pathlib import Path

from scripts import seal_rafael_B301_B320_clean_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael4347_registered_v1 import LEDGER, MENUS, PACKET, ROOT, STYLES
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_rafael_B321_B323_clean_v1 import SEALED as EARLIER
from scripts.source_locked_derivation_v5118 import checked_text


SEALED = ROOT / 'sealed_clean_first_v1'
BLOCKS = list(range(321, 343))
DRAFTS = [Path(f'translations/rafael_{label}_clean_drafts_v1.txt')
          for label in ('B321_B323', 'B324_B326', 'B327_B329', 'B330_B331',
                        'B332', 'B333_B334', 'B335_B338', 'B339_B342')]

source = checked_text(inspect.getsource(previous.main), {
    '(297, 145, 11)': '(242, 298, 16)',
    '== 453': '== 556',
    'records_count=453, ordinary_speeches=297': 'records_count=556, ordinary_speeches=242',
    'physical_style_alternatives=145, style_objects=19, style_alias_slots=152':
        'physical_style_alternatives=298, style_objects=48, style_alias_slots=384',
    'typed_captions=11, typed_choice_objects=5': 'typed_captions=16, typed_choice_objects=7',
    'meanings=297': 'meanings=242',
    'Sealed 453 clean-first drafts': 'Sealed 556 clean-first drafts',
    '    SEALED.mkdir()': """    earlier = load(EARLIER)
    assert earlier['complete_blocks'] == BLOCKS[:3]
    assert earlier['records_count'] == 42
    assert all(digest(path) == checksum for path, checksum in earlier['evidence'].items())
    assert records[:42] == [{**row, 'current_English_comparison_pending': True} for row in earlier['records']]
    SEALED.mkdir()""",
    '(PACKET, STYLES, MENUS, *DRAFTS, Path(__file__))': '(PACKET, STYLES, MENUS, EARLIER, *DRAFTS, Path(__file__))',
})


if __name__ == '__main__':
    namespace = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::exact-clean-source-seal', 'exec'), namespace)
    namespace['main']()
