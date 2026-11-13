"""Run all six earlier stages unchanged, then the byte-exact reviewed data planner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/build_integrated_release_with_reviewed_text_data.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.registered_reviewed_text_data_v1 import plan_release':
        'from dk4tool.patch.registered_reviewed_text_data_v3 import plan_release',
})
exec(compile(source, __file__ + '::same-seven-stages-byte-exact-source', 'exec'), globals())
