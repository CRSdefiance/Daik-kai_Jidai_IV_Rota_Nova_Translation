"""Preserve the rejected legacy alias attempt; qualify complete source-reference bindings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria301_registered_v1.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.maria301_release_v1 import plan_release': 'from dk4tool.patch.maria301_release_v2 import plan_release',
    "OUT = ROOT/'registered_preparation_v1'": "OUT = ROOT/'registered_preparation_v2'",
    "Path('dk4tool/patch/maria301_release_v1.py')]":
        "Path('dk4tool/patch/maria301_release_v1.py'),Path('dk4tool/patch/maria301_release_v2.py')]",
})
exec(compile(source,__file__+'::same-source-qualified-preparation-complete-caption-reference','exec'),globals())
