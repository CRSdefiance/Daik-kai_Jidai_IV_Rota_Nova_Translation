"""Source-scoped complete-page preferences with an ordinary within-page soft wrap."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/plan_editorial_scene_prose_v2.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    pairs=previous.PAIRS|":'''    adapter=checked_text(adapter,{
        'ordinary=pair in set();':"ordinary=pair in ({('quite','a')} if row['id']=='DK4_MES_B85_R0123' else set());",
    })
    pairs=previous.PAIRS|''',
})
exec(compile(source,__file__+'::ordinary-soft-wrap-preference','exec'),globals())
