"""Own one historical English terminator shift inside an unchanged native speech extent.

The semantic Japanese body stays immutable. Only its source inverse patch span
includes the first of two original NUL bytes; the second remains the terminator
outside the replacement span. This recovers both exact original blocks.
"""
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script import reviewed_scene_rebuild_with_fu_andcompounds_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

OWNER='DK4_MES_B62_R0053'
CLEAN='96c6399087792ecfa9f1b1150c8b8bc1117b6908b34dd815e5471d392c68d91b'
CURRENT='5ed294c6abbeef31f7c98724324349d16c885dab0fbce3c303df9107e873a2d1'
SOURCE=bytes.fromhex('0a82b182e882e18149814092f193c282c982c882f182c482b182c682f08149')
ENGLISH=bytes.fromhex('0a4d696e6420796f757220776f72647320746f207468652061646d6972616c21')

def source_storage_span(arm9,clean,current,row,original,prior,inventory):
    if len(original)==len(prior):return original
    assert row['id']==OWNER and row['block']==62
    assert sha(clean)==CLEAN and sha(current)==CURRENT
    assert original==SOURCE and prior==ENGLISH and (len(original),len(prior))==(31,32)
    assert row['source_reference']['offset']==row['current_reference']['offset']==753
    assert row['source_selector']==10 and row['source_complete_preamble_hex']=='0040ffff000a'
    assert clean[748:786]==bytes.fromhex('0040ffff00')+SOURCE+b'\0\0'
    assert current[748:786]==bytes.fromhex('0040ffff00')+ENGLISH+b'\0'
    before,speeches=inventory(arm9,current);source,source_speeches=inventory(arm9,clean)
    a=next(c for c in source_speeches if c['offset']==748)
    b=next(c for c in speeches if c['offset']==748)
    assert a['word']==b['word']==0x4000 and a['native_extent']==b['native_extent']==38
    assert len(before)==len(source) and [(c['offset'],c['word']) for c in before]==[(c['offset'],c['word']) for c in source]
    assert all(c['offset'] not in (784,785) for c in before+source)
    return original+b'\0'

QUALIFIED_SOURCE=checked_text(previous.SOURCE,{
    '        assert at == source_at and len(previous) == len(original)':
        '        assert at == source_at\n        source_span=source_storage_span(arm9,clean,current,row,original,previous,inventory)',
    'old=previous, original=original, value=stored,':'old=previous, original=source_span, value=stored,',
})
env={**previous.rebuild_block.__globals__,'source_storage_span':source_storage_span,'__file__':__file__}
exec(compile(QUALIFIED_SOURCE,__file__+'::complete-compound-inverses-one-exact-owned-source-alignment-span','exec'),env)
qualified_rebuild=env['rebuild_block']

def rebuild_block(arm9,clean,current,records,compiled,inventory,compound_objects=()):
    target,proof=qualified_rebuild(arm9,clean,current,records,compiled,inventory,compound_objects)
    owned=[r for r in records if r['id']==OWNER]
    for row in owned:
        item=next(t for t in proof['text_records'] if t['id']==OWNER)
        assert item['source_hex']==(SOURCE+b'\0').hex() and row['source_hex']==SOURCE.hex()
        item['source_storage_patch_span_hex']=item['source_hex']
        item['source_hex']=row['source_hex']
        item['source_owned_alignment']=dict(owner=OWNER,source_command_offset=748,source_body_offset=753,
            source_body_bytes=31,current_body_bytes=32,unchanged_native_extent=38,
            original_source_terminator_andalignment_hex='0000',current_terminator_hex='00',
            source_inverse_patch_includes_first_owned_NUL=True,semantic_source_body_unchanged=True,
            clean_block_sha256=CLEAN,current_block_sha256=CURRENT)
    assert len(owned)<=1
    return target,proof
