"""Complete-scene relocation with source-bound 2100/2200 menus and 4100 variants."""
import struct
from dk4tool.script.reviewed_scene_rebuild_v2 import SOURCE as previous
from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.dialogue.reviewed_actor_style_object_v1 import unpack
from scripts.source_locked_derivation_v5118 import checked_text

def verify_compound(word,source,current,target):
    assert source[:2]==current[:2]==target[:2]==word.to_bytes(2,'little')
    if word in (0x2100,0x2200):
        count=2 if word==0x2100 else 3
        assert len(labels(source))==len(labels(current))==len(labels(target))==count
    elif word==0x4100:
        a,aa=unpack(source);b,bb=unpack(current);c,cc=unpack(target)
        assert source[18:20]==current[18:20]==target[18:20]
        assert len(aa)==len(bb)==len(cc)
        assert all((a[i]==a[j])==(b[i]==b[j])==(c[i]==c[j]) for i in range(8) for j in range(8))
    else:raise ValueError('Unqualified compound text consumer')

SOURCE=checked_text(previous,{
    'typed_choices=()':'compound_objects=()',
    'for choice in typed_choices:':'for choice in compound_objects:',
    'typed_offsets':'compound_offsets',
    "'typed-choice'":"'compound-object'",
    'typed_objects':'native_objects',
    '        assert labels(previous) and labels(source) and labels(value)':
        "        verify_compound(choice['word'],source,previous,value)",
    "c['word']==0x2100":"c['word']==choice['word']",
    "            records=choice['records']))":"            records=choice['records'],word=choice['word']))",
    'if word == 0x2100 and at in typed_offsets:':
        'if word in (0x2100,0x2200,0x4100) and at in compound_offsets:',
    '                source_index_order=[0,1],count=2))':
        "                word=patch['word'],source_index_order=list(range(8 if patch['word']==0x4100 else len(patch['records']))),count=8 if patch['word']==0x4100 else len(patch['records'])))",
})
exec(compile(SOURCE,__file__+'::same-complete-scene-inverse-source-bound-compound-objects','exec'),globals())
