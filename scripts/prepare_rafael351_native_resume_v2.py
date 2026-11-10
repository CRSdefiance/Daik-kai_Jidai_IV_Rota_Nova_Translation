"""Require the original FE ABI guard key for FE and original progressive key for speech."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

ORIGINAL=Path('scripts/prepare_rafael351_native_resume_v1.py')
source=checked_text(ORIGINAL.read_text(encoding='utf-8'),{
    "c['original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact']":
        "c['original_macro_ABI_input_output_canaries_and4MiB_exact' if row['kind']=='system-FE' else 'original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact']",
    'evidence=[DOC,PLAN,TERMS,FAILURE,Path(__file__)]': 'evidence=[DOC,PLAN,TERMS,FAILURE,ORIGINAL,Path(__file__)]',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-reuse-checks-exact-native-ABI-key-per-consumer','exec'),globals())
