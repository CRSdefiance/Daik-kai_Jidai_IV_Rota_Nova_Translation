"""Preserve all guards and use the original absolute producer identity in rehearsal."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source_module = checked_text(Path('dk4tool/patch/maria305_release_v1.py').read_text(encoding='utf-8'), {
    "'__file__':str(FINISHER)":"'__file__':str(FINISHER.resolve())",
})
exec(compile(source_module,__file__+'::same-pure-transaction-original-producer-path-identity','exec'),globals())
