"""Retain the reviewed sentence-page preferences and coherent repeated/verb phrases."""
import ast
import linecache
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

def run_generated(source,suffix):
    filename=__file__+suffix
    linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
    exec(compile(source,filename,'exec'),globals())

# Reuse the immutable v6 source edits, including all unchanged engine contracts.
tree=ast.parse(Path('scripts/plan_editorial_scene_prose_v6.py').read_text(encoding='utf-8'))
edits=ast.literal_eval(next(n.value.args[1] for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='source' for t in n.targets)))
key="    pairs=previous.PAIRS|''',"
edits[key]=edits[key].replace("{('cape','of'),", "{('far','far'),('very','long'),('cook','them'),('cape','of'),")
source=checked_text(Path('scripts/plan_editorial_scene_prose_v5.py').read_text(encoding='utf-8'),edits)
source=checked_text(source,{
    "exec(compile(source,__file__+'::source-scoped-coherence','exec'),globals())":
    "run_generated(source,'::source-scoped-coherence')",
})
run_generated(source,'::readable-phrase-successor')
