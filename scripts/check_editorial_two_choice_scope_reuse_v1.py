"""Keep every menu provider/pixel guard while qualifying the unchanged own runtime."""
from pathlib import Path
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_editorial_two_choice_display.py').read_text(encoding='utf-8'),{
    "    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']":
        '    scope_reuse=qualified_current_native_context(doc,ctx)',
    'runtime=ctx.receipt(),': 'runtime=ctx.receipt(),native_context_reuse=scope_reuse,',
})
exec(compile(source,__file__+'::same-original-menu-VM-centering-bounds-and-pixel-contract','exec'),globals())
