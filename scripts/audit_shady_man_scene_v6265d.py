"""Correct an inferred B120 timestamp against the retained actual final command."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/audit_shady_man_scene_v6265c.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{
      "ROOT=Path('work/analysis/shady_man_scene_v6265c')":"ROOT=Path('work/analysis/shady_man_scene_v6265d')",
      'following_B120_end_frame=12697':'following_B120_end_frame=12693',
      "    assert pair_differences[0]['index']==21":"    assert following[-1]==dict(frame=12693,block=120,offset=2312,word=0,native_result=[0,0])\n    assert pair_differences[0]['index']==21",
    })
    exec(compile(text,str(source)+'::measured-following-end','exec'),dict(__name__='__main__',__file__=__file__))
