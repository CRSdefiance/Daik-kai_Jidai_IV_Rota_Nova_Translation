"""Use the literal escaped source key in the preserved derivation wrapper."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_maria330_FE_pages_v1.py').read_text(encoding='utf-8'),{
    r"taking the commander\'s head andturning":'the beheading andturning',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-paragraph-FE-projection-exact-literal-source-key','exec'),globals())
