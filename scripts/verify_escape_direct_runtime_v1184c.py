"""Retain the second decoded literal in the unreachable old status tail."""
import inspect
from pathlib import Path
from scripts import verify_escape_direct_runtime_v1184b as previous


def main():
    source=inspect.getsource(previous.main)
    old="assert old_tail_access==[['Thumb_PC_relative','section0',runtime.STATUS_LOAD,runtime.GATE+164]]"
    new="assert old_tail_access==[['Thumb_PC_relative','section0',runtime.STATUS_LOAD,runtime.GATE+164],['Thumb_PC_relative','section0',runtime.SUFFIX_SLOT,runtime.GATE+164]]"
    assert source.count(old)==1
    source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/escape_direct_runtime_v1184c')}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
