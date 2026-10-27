"""Compare discriminator tests with their bounded current-code context baseline."""
from pathlib import Path
if __name__ == '__main__':
    source = Path('scripts/probe_admiral_shot_return_v2662.py').read_text()
    old = '        scratch = 0x02666100'
    assert source.count(old) == 1
    source = source.replace(old,"        baseline = bytes(u.mem_read(BASE,0x400000))\n"+old)
    source = source.replace('assert bytes(u.mem_read(BASE,0x400000)) == ctx.raw','assert bytes(u.mem_read(BASE,0x400000)) == baseline')
    source = source.replace('admiral_shot_return_v2662','admiral_shot_return_v2662b')
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
