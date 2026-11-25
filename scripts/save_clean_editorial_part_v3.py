"""Admit B283's exact clean D7 warning for source-only intake, without dispatch approval."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/save_clean_editorial_part_v2.py').read_text(encoding='utf-8'), {
    "assert selector in [207,208,254] or (ident=='DK4_MES_B252_R0095' and selector==215 and raw.hex()=='d78aeb82c882a282c18149')":
    "assert selector in [207,208,254] or (ident in ['DK4_MES_B252_R0095','DK4_MES_B283_R0096'] and selector==215 and raw.hex()=='d78aeb82c882a282c18149')",
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::exact-source-only-D7-warning-contract', 'exec'), globals())
