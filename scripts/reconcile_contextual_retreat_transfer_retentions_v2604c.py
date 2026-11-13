"""Keep both pre-write failures;preserve the newline when capturing adapter source."""
from pathlib import Path
source=Path('scripts/reconcile_contextual_retreat_transfer_retentions_v2604.py').read_text()
old='needle="exec(compile(source,__file__,\'exec\'),globals())"';assert source.count(old)==1;source=source.replace(old,'needle="\\nexec(compile(source,__file__,\'exec\'),globals())"')
old="outer.replace(needle,'captured=source')";assert source.count(old)==1;source=source.replace(old,"outer.replace(needle,'\\ncaptured=source')")
exec(compile(source,__file__,'exec'),globals())
