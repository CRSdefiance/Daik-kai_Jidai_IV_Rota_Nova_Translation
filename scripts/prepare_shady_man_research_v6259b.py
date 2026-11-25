"""Preserve the caught absent-token failure;derive a corrected preparation successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/prepare_shady_man_research_v6259.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{
      "'three-label':'one-label','three_label':'one_label',":"'three-label':'one-label',",
      "ROOT=Path('work/analysis/shady_man_research_tools_v6259')":"ROOT=Path('work/analysis/shady_man_research_tools_v6259b')",
    })
    exec(compile(text,str(source)+'::corrected-absent-token-successor','exec'),dict(__name__='__main__',__file__=__file__))
