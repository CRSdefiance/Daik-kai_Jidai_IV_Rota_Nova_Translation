"""Compile only the exact two reviewed B221 response labels as one native object."""
import struct
from dk4tool.dialogue.lil_B221_profile_v1 import contract

def compile_choices(rows):
    d=contract();bindings=d['choice_bindings']
    expected=sorted(bindings,key=lambda ident:bindings[ident]['option_index'])
    if not isinstance(rows,list) or len(rows)!=2 or [r.get('id') for r in rows]!=expected:
        raise ValueError('Exact B221 two-choice source order required')
    chunks=[];offsets=[];cursor=0
    for row in rows:
        binding=bindings[row['id']]
        for key in ['english','source_hex','current_hex','source_reference','current_reference','option_index','command_offset','block','kind']:
            if row.get(key)!=binding[key]:raise ValueError('B221 reviewed choice differs:'+key)
        if not all(row.get('review',{}).get(k) is True for k in ['source','context','localization','naturalness']):
            raise ValueError('Four individual B221 choice prose gates required before native compilation')
        if any(not row.get(k) for k in ['speaker','source_meaning','context','localization_note']):
            raise ValueError('Complete B221 choice meaning/context required')
        value=row['english'].encode('ascii');offsets.append(cursor)
        chunk=value+b'\0';chunk+=bytes(-len(chunk)%2)
        chunks.append(chunk);cursor+=len(chunk)
    result=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
    if offsets!=[0,4] or result.hex()!=d['choice_object_hex']:
        raise ValueError('Exact original-count/source-index B221 native choice object required')
    return result
