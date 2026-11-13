"""The complete-scene planner with separately bound native two-choice objects."""
import inspect
import struct
from dk4tool.script.reviewed_scene_rebuild import rebuild_block as original
from dk4tool.dialogue.reviewed_two_choice_object_v1 import labels
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(inspect.getsource(original),{
    'def rebuild_block(arm9, clean, current, records, compiled, inventory):':
        'def rebuild_block(arm9, clean, current, records, compiled, inventory, typed_choices=()):',
    '    patches = []':'''    patches = []
    typed_offsets=set()
    for choice in typed_choices:
        at=choice['offset'];previous=bytes.fromhex(choice['current_hex'])
        source=bytes.fromhex(choice['source_hex']);value=bytes.fromhex(choice['compiled_hex'])
        assert at not in typed_offsets and len(previous)==len(source) and len(value)%2==0
        assert current[at:at+len(previous)]==previous and clean[at:at+len(source)]==source
        assert labels(previous) and labels(source) and labels(value)
        match=[c for c in before if c['offset']==at and c['word']==0x2100]
        assert len(match)==1 and match[0]['native_extent']==len(previous)
        typed_offsets.add(at)
        patches.append(dict(id=choice['id'],kind='typed-choice',start=at,end=at+len(previous),
            old=previous,original=source,value=value,compiled=value,parity_space=False,
            records=choice['records']))''',
    "patches.append(dict(id=row['id'], start=at, end=at + len(previous),":
        "patches.append(dict(id=row['id'], kind='speech', start=at, end=at + len(previous),",
    "    assert {p['start'] - 5 for p in patches} == {c['offset'] for c in speeches}":
        "    assert {p['start'] - 5 for p in patches if p['kind']=='speech'} == {c['offset'] for c in speeches}",
    '        if word == 0x4000:':'''        if word == 0x2100 and at in typed_offsets:
            patch=next(p for p in patches if p['kind']=='typed-choice' and p['start']==at)
            assert a==patch['old'] and b==patch['value'] and c==patch['original']
        elif word == 0x4000:''',
    '    texts = []':'    texts = [];typed_objects=[]',
    "        assert target[at:at + len(patch['value']) + 1] == patch['value'] + b'\\0'":
    """        if patch['kind']=='typed-choice':
            assert target[at:at+len(patch['value'])]==patch['value']
            typed_objects.append(dict(id=patch['id'],old_offset=patch['start'],new_offset=at,
                current_hex=patch['old'].hex(),source_hex=patch['original'].hex(),
                compiled_hex=patch['compiled'].hex(),records=patch['records'],
                source_index_order=[0,1],count=2))
            continue
        assert target[at:at + len(patch['value']) + 1] == patch['value'] + b'\\0'""",
    'return target, dict(text_records=texts, relative_fixups=fixups, command_map=command_map,':
        'return target, dict(text_records=texts, typed_objects=typed_objects, relative_fixups=fixups, command_map=command_map,',
})
exec(compile(SOURCE,__file__+'::complete-scene-separate-menu','exec'),globals())
