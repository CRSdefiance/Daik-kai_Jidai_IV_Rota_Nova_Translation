"""Keep the short opening sentence and I like animals phrase together in B103."""
import linecache
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/plan_editorial_scene_prose_v8.py').read_text(encoding='utf-8'),{
    "{('far','far'),('very','long'),('cook','them'),('cape','of'),":
    "{('my','interests'),('interests','never'),('never','last'),('last','very'),('like','animals'),('far','far'),('very','long'),('cook','them'),('cape','of'),",
})
filename=__file__+'::coherent-opening-successor'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),globals())
