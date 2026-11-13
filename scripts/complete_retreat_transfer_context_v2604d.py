"""Seven-report completion after preserving pre-write capture-adapter failures."""
from pathlib import Path
source=Path('scripts/complete_retreat_transfer_context_v2604.py').read_text();source=source.replace('reconcile_contextual_retreat_transfer_retentions_v2604 import','reconcile_contextual_retreat_transfer_retentions_v2604d import').replace('retreat_transfer_completion_v2604','retreat_transfer_completion_v2604d').replace('V2604','V2604d')
source=source.replace("'scripts/prepare_retreat_transfer_context_v2600.py'","'scripts/prepare_retreat_transfer_context_v2600.py',*[f'scripts/reconcile_contextual_retreat_transfer_retentions_v2604{s}.py'for s in('','b','c')],*[f'scripts/complete_retreat_transfer_context_v2604{s}.py'for s in('','b','c')]")
exec(compile(source,__file__,'exec'),globals())
