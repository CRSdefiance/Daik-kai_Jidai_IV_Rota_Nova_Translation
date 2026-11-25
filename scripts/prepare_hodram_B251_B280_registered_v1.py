"""Bind the sealed scope to the exact registered cumulative predecessor."""
from pathlib import Path
from scripts import prepare_hodram_B231_B250_registered_v1 as previous
from scripts.finalize_hodram_B251_B280_research_v1 import ROOT,READY,REBUILT,STORED,LOOKUP,LOADERS,NATIVE,FINAL,FINAL_NAMES
from scripts.build_registered_hodram_B231_B250_v1 import RELEASE as PARENT
from dk4tool.patch.hodram_b251_b280_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

ARCHIVE=previous.ARCHIVE;ARM=previous.ARM;CLEAN=previous.CLEAN;REGISTRY=previous.REGISTRY
OUT=ROOT/'registered_preparation_v1';CONFIG=Path('translations/hodram_B251_B280_editorial_release_v1.json');QUALIFICATION=OUT/'qualification.json'
source=checked_text(previous.source,{
    '(701,114,36)':'(702,114,37)',
    'record_count=225,speech_count=223,typed_choice_count=2,menu_count=1,style_count=14,':
        'record_count=216,speech_count=209,typed_choice_count=7,menu_count=3,style_count=16,',
    'scoped_name_count=19,native_pages=228,relative_cases=170,FE_count=4,actual_frames=21521,':
        'scoped_name_count=21,native_pages=212,relative_cases=660,FE_count=31,actual_frames=26801,',
    'actual_runs=1,actual_speeches=63,actual_body_pages=68,offline_speeches=160':
        'actual_runs=1,actual_speeches=86,actual_body_pages=88,offline_speeches=123',
    'dk4tool/patch/hodram_b231_b250_release_v1.py':'dk4tool/patch/hodram_b251_b280_release_v1.py',
    'dk4-reviewed-hodram-b231-b250-release-v1':'dk4-reviewed-hodram-b251-b280-release-v1',
    "len(proof['changed_records'])==225":"len(proof['changed_records'])==216",
    'exact_225_stored_bindings_verified':'exact_216_stored_bindings_verified',
    'Qualified 225 Hodram records over registered B211-B230.':'Qualified 216 Hodram records over registered B231-B250.',
})
env={**previous.env,**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(source,__file__+'::same-cumulative-preparation-exact-new-scope','exec'),env)
if __name__=='__main__':env['main']()
