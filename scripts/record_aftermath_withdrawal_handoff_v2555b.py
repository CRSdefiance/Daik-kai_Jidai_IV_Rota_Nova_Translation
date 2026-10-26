"""Accept the prepare-script path already changed by its enclosing packet name."""
from pathlib import Path
OLD=Path('scripts/record_aftermath_withdrawal_handoff_v2555.py')
if __name__=='__main__':
 source=OLD.read_text();a="else:assert a=='aftermath_defeat_source_handoff_v2547',a";b="else:assert a in('aftermath_defeat_source_handoff_v2547','scripts/prepare_aftermath_defeat_context_v2546.py'),a"
 assert source.count(a)==1;source=source.replace(a,b).replace('aftermath_withdrawal_source_handoff_v2555','aftermath_withdrawal_source_handoff_v2555b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
