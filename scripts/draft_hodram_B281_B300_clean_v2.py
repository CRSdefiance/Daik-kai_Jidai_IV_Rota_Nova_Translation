"""Keep the source drafts while removing gender/relationship assumptions from party warnings."""
from copy import deepcopy
from types import FunctionType
from pathlib import Path
from scripts import draft_hodram_B281_B300_clean_v1 as previous

OUT=Path('translations/hodram_B281_B300_clean_drafts_v2.json')
DRAFT=deepcopy(previous.DRAFT);STYLE=deepcopy(previous.STYLE)
DRAFT[283][93]="I do not know. It seems unlikely that something so desperately sought by powerful figures could be worthless..."
DRAFT[300][174]="Hrrrgh! Ugh, I cannot do it alone... Everyone, give me a hand!"
for key in [(290,2398),(291,1246)]:
    STYLE[key]=[text.replace('our own men','our own people').replace('our men','our people').replace('our friends','each other') for text in STYLE[key]]
STYLE[(291,1246)][6]="Admiraaal! It's so cramped in here, we might hit the others!"
env={**previous.main.__globals__,**globals(),'__file__':__file__}
main=FunctionType(previous.main.__code__,env,argdefs=previous.main.__defaults__)
if __name__=='__main__':
    main()
    from scripts.audit_story_glyph_consistency import load,save
    from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
    before=load(previous.OUT);after=load(OUT)
    changes=[dict(id=a['id'],before=a['english'],after=b['english'],reason='The source refers to allies/party members or powerful people; do not assume male-only participants or personal friendship.') for a,b in zip(before['records'],after['records'],strict=True) if a['english']!=b['english']]
    assert len(changes)==14
    for a,b in zip(before['records'],after['records'],strict=True):
        assert {k:v for k,v in a.items() if k!='english'}=={k:v for k,v in b.items() if k!='english'}
    save(previous.ROOT/'clean_draft_source_refinement_v2.json',dict(previous=str(previous.OUT),previous_sha256=digest(previous.OUT),current=str(OUT),current_sha256=digest(OUT),changes=changes,all_other_fields_exact=True,current_ROM_story_English_still_unextracted=True,new_credit=0))
