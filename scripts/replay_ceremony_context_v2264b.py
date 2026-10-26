"""Fresh CPU for each ceremony exchange; bind source-selected speakers explicitly."""
from pathlib import Path
source=Path('scripts/replay_ceremony_context_v2264.py').read_text().replace('ceremony_context_v2264','ceremony_context_v2264b')
marker="    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})"
insertion='''    old="    def run(fn,day,start,site,facility,hero,accept):\\n        u.mem_write(BASE,raw);"
    new="    def run(fn,day,start,site,facility,hero,accept):\\n        nonlocal u\\n        u=machine(arm)\\n        u.mem_write(BASE,raw);"
    assert source.count(old)==1;source=source.replace(old,new)
'''
assert source.count(marker)==1;source=source.replace(marker,insertion+marker)
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
