"""Seven-report completion;two preserved adapter failures made no ledger writes."""
from pathlib import Path
source=Path('scripts/complete_retreat_transfer_context_v2604.py').read_text();source=source.replace('reconcile_contextual_retreat_transfer_retentions_v2604 import','reconcile_contextual_retreat_transfer_retentions_v2604c import').replace('retreat_transfer_completion_v2604','retreat_transfer_completion_v2604c').replace('V2604','V2604c')
source=source.replace("'scripts/prepare_retreat_transfer_context_v2600.py'","'scripts/prepare_retreat_transfer_context_v2600.py','scripts/reconcile_contextual_retreat_transfer_retentions_v2604.py','scripts/reconcile_contextual_retreat_transfer_retentions_v2604b.py','scripts/complete_retreat_transfer_context_v2604.py','scripts/complete_retreat_transfer_context_v2604b.py'")
exec(compile(source,__file__,'exec'),globals())
