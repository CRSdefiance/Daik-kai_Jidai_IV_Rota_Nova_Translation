"""Source-bound two-caption native object; speech encoding is deliberately separate."""
import struct

def labels(raw):
    if not isinstance(raw,bytes) or len(raw)<10 or struct.unpack_from('<H',raw)[0]!=0x2100:
        raise ValueError('An original 0x2100 two-choice object is required')
    offsets=struct.unpack_from('<2H',raw,2)
    if offsets[0]!=0 or offsets[1]%2 or not 0<offsets[1]<len(raw)-6:
        raise ValueError('Original two-choice aligned index table required')
    values=[]
    for i,offset in enumerate(offsets):
        start=6+offset;stop=6+offsets[i+1] if i==0 else len(raw)
        chunk=raw[start:stop];end=chunk.find(b'\0')
        if end<1 or any(chunk[end:]) or len(chunk)%2:
            raise ValueError('Complete terminated caption and owned zero alignment required')
        values.append(chunk[:end])
    return values

def compile_choices(source,current,rows,*,require_formatting=True):
    original,prior=labels(source),labels(current)
    if not isinstance(rows,list) or len(rows)!=2 or [r.get('source_index') for r in rows]!=[0,1]:
        raise ValueError('Both original source indices in order are required')
    chunks=[];offsets=[];cursor=0
    for index,row in enumerate(rows):
        if row.get('kind')!='typed-choice-label' or row.get('source_choice_object_hex')!=source.hex() or row.get('current_choice_object_hex')!=current.hex():
            raise ValueError('Exact complete source/current choice bindings required')
        if row.get('source_hex')!=original[index].hex() or row.get('current_hex')!=prior[index].hex():
            raise ValueError('Exact individual source/current caption bindings required')
        gates=['source','context','localization','naturalness']+(['formatting'] if require_formatting else [])
        if any(row.get('review',{}).get(g) is not True for g in gates):
            raise ValueError('Individual editorial gates are required')
        text=row.get('english')
        if not isinstance(text,str) or not text or text!=text.strip() or '  ' in text or any(not 32<=ord(c)<127 or c in '%{}' for c in text):
            raise ValueError('One complete unpadded ASCII menu caption required')
        offsets.append(cursor);chunk=text.encode('ascii')+b'\0';chunk+=bytes(-len(chunk)%2)
        chunks.append(chunk);cursor+=len(chunk)
    if cursor>65535:raise ValueError('Native two-choice offset bounds exceeded')
    target=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
    if labels(target)!=[r['english'].encode('ascii') for r in rows]:
        raise ValueError('Native caption order or complete bytes changed')
    return target
