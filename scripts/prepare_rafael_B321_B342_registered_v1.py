"""Qualify the finished 556-record dialogue batch against the registered parent."""
import inspect
from pathlib import Path

from dk4tool.patch.rafael_story_b321_b342_release_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts import finalize_rafael_B321_B342_research_v1 as reviewed
from scripts import prepare_rafael_B301_B320_registered_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael4347_v1 import ARCHIVE, ARM, CLEAN, REGISTRY, RELEASE as PARENT
from scripts.verify_rafael_B321_B342_visual_v1 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.refine_rafael_B301_B320_plan_v1 import sha
from scripts.source_locked_derivation_v5118 import checked_text


OUT = ROOT / 'registered_preparation_v3'
CONFIG = Path('translations/rafael_B321_B342_editorial_release_v1.json')
QUALIFICATION = OUT / 'qualification.json'
source = checked_text(inspect.getsource(previous.main), {
    '(696, 114, 31)': '(697, 114, 32)',
    'record_count=453, speech_count=442, typed_choice_count=11, menu_count=5, style_count=145':
        'record_count=556, speech_count=540, typed_choice_count=16, menu_count=7, style_count=298',
    'scoped_name_count=19, native_pages=444, relative_cases=630, FE_count=16, actual_frames=17441':
        'scoped_name_count=16, native_pages=552, relative_cases=650, FE_count=20, actual_frames=24881',
    'actual_runs=1, actual_speeches=45, actual_body_pages=47, actual_choice_labels=11, offline_speeches=397':
        'actual_runs=1, actual_speeches=72, actual_body_pages=76, actual_choice_labels=16, offline_speeches=468',
    'rafael_story_b301_b320_release_v1.py': 'rafael_story_b321_b342_release_v1.py',
    "len(proof['changed_records']) == 453": "len(proof['changed_records']) == 556",
    'exact_453_stored_bindings': 'exact_556_stored_bindings',
    'Qualified all 453 dialogue records.': 'Qualified all 556 dialogue records.',
})
exec(compile(source, __file__ + '::qualified-dialogue-only-successor', 'exec'), globals())


if __name__ == '__main__':
    main()
