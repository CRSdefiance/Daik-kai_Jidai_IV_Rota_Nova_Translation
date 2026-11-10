"""Qualify the finished speech-only batch before its separate middle-field stage."""
import inspect
from pathlib import Path
from dk4tool.patch.rafael_story_b0_b34_release_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts import finalize_rafael_B0_B34_research_v1 as reviewed
from scripts import prepare_rafael_B301_B320_registered_v1 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_rafael4903_v1 import ARCHIVE,ARM,CLEAN,REGISTRY,RELEASE as PARENT
from scripts.plan_rafael_B0_B34_v1 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.refine_rafael_B301_B320_plan_v1 import sha
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'registered_preparation_v1'
CONFIG=Path('translations/rafael_B0_B34_editorial_release_v1.json')
QUALIFICATION=OUT/'qualification.json'
source=checked_text(inspect.getsource(previous.main),{
    '(696, 114, 31)':'(698, 114, 33)',
    'record_count=453, speech_count=442, typed_choice_count=11, menu_count=5, style_count=145':
        'record_count=283, speech_count=283, typed_choice_count=0, menu_count=0, style_count=0',
    'scoped_name_count=19, native_pages=444, relative_cases=630, FE_count=16, actual_frames=17441':
        'scoped_name_count=39, native_pages=284, relative_cases=675, FE_count=0, actual_frames=28001',
    'actual_runs=1, actual_speeches=45, actual_body_pages=47, actual_choice_labels=11, offline_speeches=397':
        'actual_runs=1, actual_speeches=95, actual_body_pages=96, actual_choice_labels=0, offline_speeches=188',
    'rafael_story_b301_b320_release_v1.py':'rafael_story_b0_b34_release_v1.py',
    "len(proof['changed_records']) == 453":"len(proof['changed_records']) == 283",
    'exact_453_stored_bindings':'exact_283_stored_bindings',
    'Qualified all 453 dialogue records.':'Qualified all 283 dialogue records.',
})
exec(compile(source,__file__+'::same-qualified-dialogue-successor','exec'),globals())

if __name__=='__main__':main()
