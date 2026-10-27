"""Correct the failed generator's split without changing its preserved source."""
from pathlib import Path
if __name__=='__main__':
    old=Path('scripts/prepare_lil_B131_B133_completion_v3342.py')
    t=old.read_text(encoding='utf-8')
    a="    a=t.index('if __name__');prefix=t[:a];t=t[a:]"
    b="    t=t.replace('SUMMARY='+repr(SUMMARY),'SUMMARY=__SUMMARY__');prefix=''"
    assert a in t;t=t.replace(a,b)
    a='    t=prefix+t\n';b="    t=(prefix+t).replace('SUMMARY=__SUMMARY__','SUMMARY='+repr(SUMMARY))\n"
    assert a in t;t=t.replace(a,b)
    exec(compile(t,__file__,'exec'))
