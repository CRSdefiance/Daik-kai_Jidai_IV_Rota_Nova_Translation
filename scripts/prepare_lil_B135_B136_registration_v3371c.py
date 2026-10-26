"""Correct generator ordering while preserving its failed predecessor."""
from pathlib import Path
if __name__=='__main__':
    t=Path('scripts/prepare_lil_B135_B136_registration_v3371.py').read_text(encoding='utf-8')
    a="      'B135/B136 must run once after the complete V3300 stack':'B135/B136 must run once after the complete V3338 stack',\n";assert a in t;t=t.replace(a,'')
    a="    a=t.index('    deps.update([\\'scripts/research_')";assert a in t;t=t.replace(a,"    t=t.replace('B135/B136 must run once after the complete V3300 stack','B135/B136 must run once after the complete V3338 stack')\n"+a)
    exec(compile(t,__file__,'exec'))
