"""Preserve inspectable generated planner source across the qualified v6 derivation."""
import linecache
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

def run_generated(source,suffix):
    filename=__file__+suffix
    linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
    exec(compile(source,filename,'exec'),globals())

source=checked_text(Path('scripts/plan_editorial_scene_prose_v6.py').read_text(encoding='utf-8'),{
    "exec(compile(source,__file__+'::automatic-sentence-page-coherence','exec'),globals())":
    '''source=checked_text(source,{
        "exec(compile(source,__file__+'::source-scoped-coherence','exec'),globals())":
        "run_generated(source,'::source-scoped-coherence')",
    })
run_generated(source,'::automatic-sentence-page-coherence')''',
})
run_generated(source,'::inspectable-v6-producer')
