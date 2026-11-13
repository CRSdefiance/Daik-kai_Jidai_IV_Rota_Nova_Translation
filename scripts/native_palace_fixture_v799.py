"""Versioned adapter preserving the frozen V798 fixture and its receipts."""

from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_palace_fixture_v798 as original
from scripts.verify_village_wrap_v608 import read


def set_condition(arm,raw,request):
    cfg=read('translations/palace_label_boundaries_release_v1.json')
    assert sha(arm)==cfg['target_arm9_sha256'] and len(raw)==0x400000
    run=FunctionType(original.set_condition.__code__,{**original.__dict__,'ARMS':{sha(arm)}})
    if request=={'mode':'Istanbul-headquarters-recommendation'}:
        intermediate,a=run(arm,raw,{'mode':'Istanbul-treasure-headquarters'})
        after,b=run(arm,intermediate,{'mode':'Market-recommendation'})
        changes=[{'address':original.BASE+i,'before':x,'after':y} for i,(x,y) in enumerate(zip(raw,after,strict=True)) if x!=y]
        assert len(changes)==3
        return after,{'synthetic_Palace_qualification_fixture':True,'mode':request['mode'],
            'ARM9_sha256':sha(arm),'original_fixture_components':[a,b],
            'original_menu_eligibility_flags_after':b['original_menu_eligibility_flags_after'],
            'changes':changes,'all_other4MiB_RAM_bytes_exact':True,
            'no_menu_dialogue_outcome_or_game_logic_replacement':True,
            'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after)}
    return run(arm,raw,request)
