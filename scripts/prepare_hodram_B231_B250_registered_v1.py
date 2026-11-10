"""Bind the sealed new scope to the exact registered Hodram predecessor."""
import inspect
from pathlib import Path
from scripts import prepare_hodram_B211_B230_registered_v1 as previous
from scripts.finalize_hodram_B231_B250_research_v1 import ROOT,READY,REBUILT,STORED,LOOKUP,LOADERS,NATIVE,FINAL,FINAL_NAMES
from dk4tool.patch.hodram_b231_b250_release_v1 import plan_release
from scripts.build_registered_hodram_B211_B230_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text

ARCHIVE=previous.ARCHIVE;ARM=previous.ARM;CLEAN=previous.CLEAN;REGISTRY=previous.REGISTRY
OUT=ROOT/'registered_preparation_v1';CONFIG=Path('translations/hodram_B231_B250_editorial_release_v1.json');QUALIFICATION=OUT/'qualification.json'
source=checked_text(inspect.getsource(previous.main),{
    '(700,114,35)':'(701,114,36)',
    'record_count=277,speech_count=270,typed_choice_count=7,menu_count=3,style_count=29,':'record_count=225,speech_count=223,typed_choice_count=2,menu_count=1,style_count=14,',
    'scoped_name_count=23,native_pages=284,relative_cases=150,FE_count=4,actual_frames=23441,':'scoped_name_count=19,native_pages=228,relative_cases=170,FE_count=4,actual_frames=21521,',
    'actual_runs=1,actual_speeches=65,actual_body_pages=74,offline_speeches=205':'actual_runs=1,actual_speeches=63,actual_body_pages=68,offline_speeches=160',
    'research_final_v3/':'research_final_v1/',
    'dk4tool/patch/hodram_b211_b230_release_v1.py':'dk4tool/patch/hodram_b231_b250_release_v1.py',
    'dk4-reviewed-hodram-b211-b230-release-v1':'dk4-reviewed-hodram-b231-b250-release-v1',
    "len(proof['changed_records'])==277":"len(proof['changed_records'])==225",
    'exact_277_stored_bindings_verified':'exact_225_stored_bindings_verified',
    'Qualified 277 Hodram records over Rafael5186.':'Qualified 225 Hodram records over registered B211-B230.',
})
env={**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(source,__file__+'::same-preparation-and-complete-parent-inverse','exec'),env)
if __name__=='__main__':env['main']()
