"""Allow an explicit source-bound list of unchanged control-only reference blocks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v2.py').read_text(encoding='utf-8'),{
    "            assert block==doc['unchanged_control_only_reference_block'] and not group['records']":
    "            assert block in doc['unchanged_control_only_reference_blocks'] and not group['records']",
})
exec(compile(source,__file__+'::explicit-control-only-reference-list','exec'),globals())
