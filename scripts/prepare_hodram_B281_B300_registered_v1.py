"""Bind the complete sealed batch to the exact registered cumulative parent."""
from pathlib import Path
from scripts import prepare_hodram_B251_B280_registered_v1 as previous
from scripts.finalize_hodram_B281_B300_research_v1 import ROOT,READY,REBUILT,STORED,LOOKUP,LOADERS,NATIVE,FINAL,FINAL_NAMES
from scripts.build_registered_hodram_B251_B280_v1 import RELEASE as PARENT
from dk4tool.patch.hodram_b281_b300_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

ARCHIVE=previous.ARCHIVE;ARM=previous.ARM;CLEAN=previous.CLEAN;REGISTRY=previous.REGISTRY
OUT=ROOT/'registered_preparation_v1';CONFIG=Path('translations/hodram_B281_B300_editorial_release_v1.json');QUALIFICATION=OUT/'qualification.json'
source=checked_text(previous.source,{
    '(702,114,37)':'(703,114,38)',
    'record_count=216,speech_count=209,typed_choice_count=7,menu_count=3,style_count=16,':
        'record_count=384,speech_count=373,typed_choice_count=11,menu_count=5,style_count=131,',
    'scoped_name_count=21,native_pages=212,relative_cases=660,FE_count=31,actual_frames=26801,':
        'scoped_name_count=18,native_pages=374,relative_cases=1415,FE_count=16,actual_frames=38561,',
    'actual_runs=1,actual_speeches=86,actual_body_pages=88,offline_speeches=123':
        'actual_runs=1,actual_speeches=134,actual_body_pages=135,offline_speeches=239',
    'dk4tool/patch/hodram_b251_b280_release_v1.py':'dk4tool/patch/hodram_b281_b300_release_v1.py',
    'dk4-reviewed-hodram-b251-b280-release-v1':'dk4-reviewed-hodram-b281-b300-release-v1',
    "len(proof['changed_records'])==216":"len(proof['changed_records'])==384",
    'exact_216_stored_bindings_verified':'exact_384_stored_bindings_verified',
    'Qualified 216 Hodram records over registered B231-B250.':'Qualified 384 Hodram records over registered B251-B280.',
})
env={**previous.env,**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(source,__file__+'::same-registered-preparation-all-parent-guards','exec'),env)
if __name__=='__main__':env['main']()
