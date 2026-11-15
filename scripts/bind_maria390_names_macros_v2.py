"""Bind actual actors; keep historical Rocco outside the207-entry catalogue scope."""
from scripts.bind_maria390_names_macros_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    "expected={'ロッコ'}":"expected=set()",
    'assert len(spoken)==1 and expected==':'assert len(spoken)==0 and expected==',
    'names_andterms_reference_only_not_editorial_orfont_approval=True':
        'names_andterms_reference_only_not_editorial_orfont_approval=True,spoken_Rocco_reference_not_in207_actor_catalogue=True,source_Rocco_spelling_requires_separate_binding=True',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-getter-guards-no-invented-historical-actor-binding','exec'),globals())
