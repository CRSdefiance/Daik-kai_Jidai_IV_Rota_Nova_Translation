"""Bind every sealed record and bounded QA return to the exact registered parent."""
from pathlib import Path
from scripts import prepare_hodram_B281_B300_registered_v1 as previous
from scripts.finalize_hodram_B301_B310_research_v2 import ROOT,READY,REBUILT,STORED,LOOKUP,LOADERS,NATIVE,FINAL,FINAL_NAMES,EXIT
from scripts.build_registered_hodram_B281_B300_v1 import RELEASE as PARENT
from dk4tool.patch.hodram_b301_b310_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

ARCHIVE=previous.ARCHIVE;ARM=previous.ARM;CLEAN=previous.CLEAN;REGISTRY=previous.REGISTRY
OUT=ROOT/'registered_preparation_v1';CONFIG=Path('translations/hodram_B301_B310_editorial_release_v1.json');QUALIFICATION=OUT/'qualification.json'
source=checked_text(previous.source,{
    '(703,114,38)':'(704,114,39)',
    'record_count=384,speech_count=373,typed_choice_count=11,menu_count=5,style_count=131,':
        'record_count=234,speech_count=225,typed_choice_count=9,menu_count=4,style_count=152,',
    'scoped_name_count=18,native_pages=374,relative_cases=1415,FE_count=16,actual_frames=38561,':
        'scoped_name_count=8,native_pages=228,relative_cases=190,FE_count=8,actual_frames=34162,',
    'actual_runs=1,actual_speeches=134,actual_body_pages=135,offline_speeches=239':
        'actual_runs=2,actual_speeches=96,actual_body_pages=97,offline_speeches=129',
    'native_styles=rebuilt[\'styles\'],research_completion=str(READY))':
        'native_styles=rebuilt[\'styles\'],research_completion=str(READY),bounded_QA_return_proof=str(EXIT))',
    'dk4tool/patch/hodram_b281_b300_release_v1.py':'dk4tool/patch/hodram_b301_b310_release_v1.py',
    'dk4-reviewed-hodram-b281-b300-release-v1':'dk4-reviewed-hodram-b301-b310-release-v1',
    "len(proof['changed_records'])==384":"len(proof['changed_records'])==234",
    'exact_384_stored_bindings_verified':'exact_234_stored_bindings_verified',
    'Qualified 384 Hodram records over registered B251-B280.':'Qualified234 Hodram records over registered B281-B300.',
})
env={**previous.env,**vars(previous),**globals(),'previous':previous,'__file__':__file__}
exec(compile(source,__file__+'::same-registered-preparation-with-capacity-safe-QA-evidence','exec'),env)
if __name__=='__main__':env['main']()
