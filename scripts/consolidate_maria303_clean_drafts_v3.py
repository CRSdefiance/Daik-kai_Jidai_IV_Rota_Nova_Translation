"""Seal the validated acknowledgment successor with all303 original source/macro guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/consolidate_maria303_clean_drafts_v1.py').read_text(encoding='utf-8'),{
    'all303_clean_meanings_andindependent_drafts_v1.json':'all303_clean_meanings_andindependent_drafts_v3.json',
    "ROOT/'B62_B70_independent_drafts_v1.json'":"ROOT/'B62_B70_independent_drafts_v3.json'",
    '[source_path,*paths,Path(__file__)]':"[source_path,*paths,Path('scripts/consolidate_maria303_clean_drafts_v1.py'),Path(__file__)]",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete303-source-control-macro-andindependent-prose-guards','exec'),globals())
