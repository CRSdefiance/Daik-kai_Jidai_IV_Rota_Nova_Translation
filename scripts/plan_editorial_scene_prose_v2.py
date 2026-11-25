"""Same native formatter, with source-scoped complete-page phrase preferences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/plan_editorial_scene_prose.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    '    pairs=previous.PAIRS|':'''    page_phrases={
        'DK4_MES_B85_R0018': 'I have absolutely no intention of getting married!',
        'DK4_MES_B85_R0123': 'but would you consider joining my ship?',
        'DK4_MES_B89_R0067': 'You can say you found it yourself.',
    }
    def page_cut_penalty(row,words,stop,line,final):
        phrase=page_phrases.get(row['id'])
        if not phrase or final or (line+1)%4:return 0
        target=phrase.split()
        spans=[(i,i+len(target)) for i in range(len(words)-len(target)+1) if words[i:i+len(target)]==target]
        assert len(spans)==1
        start,end=spans[0]
        return 4*int(start<stop<end)
    adapter=checked_text(adapter,{
        'cost[0]+tiny+weak,':'cost[0]+tiny+weak+page_cut_penalty(row,words,stop,line,final),',
    })
    pairs=previous.PAIRS|''',
    "'source_bound_existing_literal':source_bound_existing_literal}":
        "'source_bound_existing_literal':source_bound_existing_literal,'page_cut_penalty':page_cut_penalty}",
    '        coherent_pairs=sorted(pairs),progressive_width_px=216,FE_original_width_px=228,':
        '        coherent_pairs=sorted(pairs),source_scoped_page_coherence_preferences=page_phrases,progressive_width_px=216,FE_original_width_px=228,',
})
exec(compile(source,__file__+'::source-scoped-page-preference','exec'),globals())
