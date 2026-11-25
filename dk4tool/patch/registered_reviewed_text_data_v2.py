"""Use the exact native COMMON archive path in the qualified data-only planner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('dk4tool/patch/registered_reviewed_text_data_v1.py').read_text(encoding='utf-8'), {
    "image.read_file('/data/COMMON.DK4')": "image.read_file('/COMMON/MESFILE.DK4')",
})
exec(compile(source, __file__ + '::exact-current-COMMON-archive-path', 'exec'), globals())
