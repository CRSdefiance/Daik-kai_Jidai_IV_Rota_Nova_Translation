"""Remove one overconstraining soft pair; keep the invitation on a single page."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/plan_editorial_scene_prose_v2.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "        'cost[0]+tiny+weak,':'cost[0]+tiny+weak+page_cut_penalty(row,words,stop,line,final),":
    """        'cost[0]+tiny+weak,':'cost[0]+tiny+weak+page_cut_penalty(row,words,stop,line,final),
        'ordinary=pair in set();':\"ordinary=pair in ({('quite','a')} if row['id']=='DK4_MES_B85_R0123' else set());\",""",
})
exec(compile(source,__file__+'::ordinary-soft-wrap-preference','exec'),globals())
