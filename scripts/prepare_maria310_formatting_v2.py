"""Retain the failed no-op derivation; run only necessary counted source changes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria310_formatting_v1.py').read_text(encoding='utf-8'),{
    '''    "row['kind']=='typed-choice-label'":"row['kind']=='typed-choice-label'",\n''':'',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-formatter-preparation-without-unneeded-absent-key','exec'),globals())
