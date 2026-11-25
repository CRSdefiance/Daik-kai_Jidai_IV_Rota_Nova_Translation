"""Research-only complete tutorial reconstruction, preserving every inherited layer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/rebuild_reviewed_editorial_batch.py').read_text(encoding='utf-8'), {
    'from dk4tool.script.reviewed_scene_rebuild import rebuild_block':
        'from dk4tool.script.rafael_early_tutorial_rebuild_v1 import rebuild_block',
})
exec(compile(source, __file__ + '::complete-source-current-SC0-research-only', 'exec'), globals())
