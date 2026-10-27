"""Correct the Angelo/Fernando pairing from executed source LDR literals."""
import inspect
from pathlib import Path
from scripts import research_duel_special_context_v1215 as previous


def main():
    cases=tuple((actor,method,1988 if actor==15 else 1987 if actor==20 else number)
        for actor,method,number in previous.CASES)
    source=inspect.getsource(previous.main)
    old="assert len(seen)==1 and seen[0]['message_ID']==number"
    new="assert len(seen)==1 and seen[0]['message_ID']==number,(actor_id,hex(method),number,seen,hex(cpu.reg_read(UC_ARM_REG_PC)))"
    assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'CASES':cases,'ROOT':Path('work/analysis/duel_special_context_v1215b')}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
