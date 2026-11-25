"""Retain the rejected preparation and qualify the corrected exact COMMON lookup."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_shared_tutorial_name_data_release.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.registered_reviewed_text_data_v1 import plan_release':
        'from dk4tool.patch.registered_reviewed_text_data_v2 import plan_release',
    'Shared_tutorial_name_data_release_v2_20261104': 'Shared_tutorial_name_data_release_v3_20261104',
    'shared_tutorial_pedro_hayreddin_data_release_v1.json': 'shared_tutorial_pedro_hayreddin_data_release_v2.json',
    "Path('dk4tool/patch/registered_reviewed_text_data_v1.py'), Path(__file__)":
        "Path('dk4tool/patch/registered_reviewed_text_data_v1.py'), Path('dk4tool/patch/registered_reviewed_text_data_v2.py'), Path('scripts/prepare_shared_tutorial_name_data_release.py'), Path(__file__)",
})
exec(compile(source, __file__ + '::same-six-span-composition-and-eight-rejections-exact-COMMON-path', 'exec'), globals())
