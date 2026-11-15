"""Run all29 source relative sites with five previous results in both images."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/prove_lil_B142_B145_branches_v3578.py');t=p.read_text(encoding='utf-8');changes=[('lil_B142_B145_branches_v3578','lil_B155_branches_v3659'),('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json','work/analysis/lil_B155_source_v3658/all50_clean_current_complete_context.json'),("                for last in (0,1,2,3,0xFFFFFFFF):","                main_before=bytes(cpu.mem_read(0x02000000,0x400000))\n                for last in (0,1,2,3,0xFFFFFFFF):"),("                    assert bytes(cpu.mem_read(STREAM,len(block)))==block","                    assert bytes(cpu.mem_read(0x02000000,0x400000))==main_before\n                    assert bytes(cpu.mem_read(STREAM,len(block)))==block")]
    for a,b in changes:assert a in t,a;t=t.replace(a,b)
    exec(compile(t,str(p)+'::B155-all29-sites-and-main-RAM-guard','exec'),dict(__name__='__main__',__file__=__file__))
