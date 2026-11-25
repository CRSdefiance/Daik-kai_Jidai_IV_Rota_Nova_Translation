"""Qualify the single additive original VM entry target for read-only return tracing."""
from collections import Counter
from pathlib import Path
import re
from scripts.source_locked_derivation_v5118 import native_numbers

def qualified_additive_targets(source,changes):
    assert all(k in source for k in changes)
    target=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source)
    compile(target,'<qualified-readonly-observer>','exec')
    before,after=native_numbers(source),native_numbers(target)
    # v5 stopped before output because the immutable-builder derivation guard
    # intentionally disallows new native PCs. This local observer-only contract
    # permits precisely two references to the existing source dispatcher entry.
    # The inherited runner additionally asserts its instruction equals clean ARM9
    # and uses the original core handler and nonmutation/restoration checks.
    assert not before-after and after-before==Counter({0x2A510:2})
    return target

if __name__=='__main__':
    path=Path('scripts/trace_hodram_QA_return_v5.py')
    source=path.read_text(encoding='utf-8')
    assert source.count('source=checked_text(previous,{')==1
    source=source.replace('source=checked_text(previous,{','source=qualified_additive_targets(previous,{')
    exec(compile(source,__file__+'::qualified-single-added-readonly-VM-target','exec'),globals())
