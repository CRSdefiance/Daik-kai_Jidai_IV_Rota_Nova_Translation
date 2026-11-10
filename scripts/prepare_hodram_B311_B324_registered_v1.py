"""Bind the sealed400-record batch to the exact705-entry registered cumulative predecessor."""
from pathlib import Path
from scripts import prepare_hodram_B301_B310_registered_v1 as previous
from scripts.finalize_hodram_B311_B324_research_v1 import ROOT, READY, REBUILT, STORED, LOOKUP, LOADERS, NATIVE, FINAL, FINAL_NAMES, EXIT
from scripts.build_registered_hodram_B301_B310_v1 import RELEASE as PARENT
from dk4tool.patch.hodram_b311_b324_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

ARCHIVE = previous.ARCHIVE
ARM = previous.ARM
CLEAN = previous.CLEAN
REGISTRY = previous.REGISTRY
OUT = ROOT/'registered_preparation_v1'
CONFIG = Path('translations/hodram_B311_B324_editorial_release_v1.json')
QUALIFICATION = OUT/'qualification.json'
source = checked_text(previous.source, {
    '(704,114,39)': '(705,114,40)',
    'record_count=234,speech_count=225,typed_choice_count=9,menu_count=4,style_count=152,':
        'record_count=400,speech_count=387,typed_choice_count=13,menu_count=6,style_count=236,',
    'scoped_name_count=8,native_pages=228,relative_cases=190,FE_count=8,actual_frames=34162,':
        'scoped_name_count=11,native_pages=389,relative_cases=495,FE_count=14,actual_frames=57202,',
    'actual_runs=2,actual_speeches=96,actual_body_pages=97,offline_speeches=129':
        'actual_runs=2,actual_speeches=189,actual_body_pages=191,offline_speeches=198',
    'dk4tool/patch/hodram_b301_b310_release_v1.py': 'dk4tool/patch/hodram_b311_b324_release_v1.py',
    'dk4-reviewed-hodram-b301-b310-release-v1': 'dk4-reviewed-hodram-b311-b324-release-v1',
    "len(proof['changed_records'])==234": "len(proof['changed_records'])==400",
    'exact_234_stored_bindings_verified': 'exact_400_stored_bindings_verified',
    'Qualified234 Hodram records over registered B281-B300.': 'Qualified400 Hodram records over registered B301-B310.',
})
env = {**previous.env, **vars(previous), **globals(), 'previous':previous, '__file__':__file__}
exec(compile(source,__file__+'::same-registered-parent-and-evidence-qualification-new-scope','exec'),env)
if __name__ == '__main__':
    env['main']()
