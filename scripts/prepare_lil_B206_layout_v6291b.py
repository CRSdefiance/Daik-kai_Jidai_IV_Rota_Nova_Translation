"""Use the source packet's relative-site count as an integer;preserve the caught schema assumption."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/prepare_lil_B206_layout_v6291.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{
      "ROOT=Path('work/analysis/lil_B206_layout_tools_v6291')":"ROOT=Path('work/analysis/lil_B206_layout_tools_v6291b')",
      "len(packet['source_relative_sites'])":"packet['source_relative_sites']",
      "len(source['source_relative_sites'])":"source['source_relative_sites']",
    })
    exec(compile(text,str(source)+'::source-count-schema-successor','exec'),dict(__name__='__main__',__file__=__file__))
