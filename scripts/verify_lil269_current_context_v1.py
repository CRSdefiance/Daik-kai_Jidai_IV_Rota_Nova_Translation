"""Verify the current Lil snapshot with the unchanged original getter/payload guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/verify_lil382_current_context_v1.py').read_text(encoding='utf-8'), {
    'scripts.prepare_lil382_current_context_v1':'scripts.prepare_lil269_current_context_v1',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-exact-own-ROM-Lil-context-andnonmutation-guards','exec'),globals())
