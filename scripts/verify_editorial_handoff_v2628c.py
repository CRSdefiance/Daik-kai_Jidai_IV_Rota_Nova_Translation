"""Preserve both prior audit refusals;use canonical source-entry start field."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2628.py').read_text().replace('219_current_native_font_cases_32_copies_43_compiler_negatives_verified=','all219_current_native_font_cases_32_copies_43_compiler_negatives_verified=').replace('start_in_record=j.start_in_record','start_in_record=j.start').replace('editorial_handoff_verification_v2628','editorial_handoff_verification_v2628c')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
