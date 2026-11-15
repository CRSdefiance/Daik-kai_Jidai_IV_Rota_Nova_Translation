"""Match the dedented callback body while retaining v6's additive-PC qualification."""
from pathlib import Path
from scripts.trace_hodram_QA_return_v6 import qualified_additive_targets

if __name__=='__main__':
    source=Path('scripts/trace_hodram_QA_return_v5.py').read_text(encoding='utf-8')
    source=source.replace('source=checked_text(previous,{','source=qualified_additive_targets(previous,{')
    old='"                r0,r1,r9=values[4],values[5],values[13]"'
    assert source.count(old)==1
    source=source.replace(old,'"            r0,r1,r9=values[4],values[5],values[13]"')
    start=source.index('"""                r0,r1,r9=')+3
    end=source.index('return"""',start)+len('return')
    block=source[start:end].splitlines()
    assert all(line.startswith('    ') for line in block)
    source=source[:start]+'\n'.join(line[4:] for line in block)+source[end:]
    # Reuse the exact already-read full buffer length in the additive assertion.
    # Preserve every numeric constant in the inherited callback itself.
    assert source.count('ct.string_at(self.wram,0x400000)==raw')==1
    source=source.replace('ct.string_at(self.wram,0x400000)==raw','ct.string_at(self.wram,len(raw))==raw')
    exec(compile(source,__file__+'::same-readonly-native-trace-correct-callback-indent','exec'),globals())
