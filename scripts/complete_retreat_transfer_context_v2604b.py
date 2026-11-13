"""Complete the verified seven-report batch after a pre-write adapter-match fix."""
from pathlib import Path
source=Path('scripts/complete_retreat_transfer_context_v2604.py').read_text();source=source.replace('reconcile_contextual_retreat_transfer_retentions_v2604 import','reconcile_contextual_retreat_transfer_retentions_v2604b import').replace('retreat_transfer_completion_v2604','retreat_transfer_completion_v2604b').replace('V2604','V2604b')
source=source.replace("'scripts/prepare_retreat_transfer_context_v2600.py'","'scripts/prepare_retreat_transfer_context_v2600.py','scripts/reconcile_contextual_retreat_transfer_retentions_v2604.py','scripts/complete_retreat_transfer_context_v2604.py'")
exec(compile(source,__file__,'exec'),globals())
