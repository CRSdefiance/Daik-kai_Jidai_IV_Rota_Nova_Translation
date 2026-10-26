"""Run all8 original relative sites withboth images andall4MiB guard preservation."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/prove_lil_B155_branches_v3659.py');t=p.read_text(encoding='utf-8');# This successor reuses the source-owned implementation inside the wrapper.
    a=Path('scripts/prove_lil_B142_B145_branches_v3578.py');s=a.read_text(encoding='utf-8');changes=[('lil_B142_B145_branches_v3578','lil_B157_branches_v3747'),('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json','work/analysis/lil_B157_source_v3746/all75_clean_current_complete_context.json'),('                for last in (0,1,2,3,0xFFFFFFFF):','                main_before=bytes(cpu.mem_read(0x02000000,0x400000))\n                for last in (0,1,2,3,0xFFFFFFFF):'),('                    assert bytes(cpu.mem_read(STREAM,len(block)))==block','                    assert bytes(cpu.mem_read(0x02000000,0x400000))==main_before\n                    assert bytes(cpu.mem_read(STREAM,len(block)))==block')]
    for x,y in changes:assert x in s,x;s=s.replace(x,y)
    exec(compile(s,str(a)+'::B157-all8-relative-sites-main-RAM-guards','exec'),dict(__name__='__main__',__file__=__file__))
