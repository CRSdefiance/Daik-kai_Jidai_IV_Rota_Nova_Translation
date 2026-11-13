"""Preserved pre-write failures;capture source with newline and file provenance."""
from pathlib import Path
source=Path('scripts/reconcile_contextual_retreat_transfer_retentions_v2604.py').read_text()
old='needle="exec(compile(source,__file__,\'exec\'),globals())"';assert source.count(old)==1;source=source.replace(old,'needle="\\nexec(compile(source,__file__,\'exec\'),globals())"')
old="outer.replace(needle,'captured=source')";assert source.count(old)==1;source=source.replace(old,"outer.replace(needle,'\\ncaptured=source')")
assert source.count('env={};')==1;source=source.replace('env={};',"env={'__file__':__file__};")
exec(compile(source,__file__,'exec'),globals())
