"""Correct the stale COMMON-directory input;retain all strict source and RAM guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/prove_shady_man_names_v6263.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{
      "ROOT=Path('work/analysis/shady_man_names_v6263')":"ROOT=Path('work/analysis/shady_man_names_v6263b')",
      "conf=read('translations/shop657_full_width_reflow_release_v1.json')":"conf=read('work/analysis/current_V6220_native_v6228/current_capture_context.json')",
    })
    exec(compile(text,str(source)+'::current-directory-successor','exec'),dict(__name__='__main__',__file__=__file__))
