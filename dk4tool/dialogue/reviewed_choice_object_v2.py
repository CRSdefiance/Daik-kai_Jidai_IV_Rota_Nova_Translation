"""Source-bound native two/three-caption objects; no speech encoder or authored padding."""
import struct

def count_and_base(raw):
    if not isinstance(raw,bytes) or len(raw)<2:
        raise ValueError('An original typed choice object is required')
    count={0x2100:2,0x2200:3}.get(struct.unpack_from('<H',raw)[0])
    if count is None or len(raw)<2+count*4:
        raise ValueError('A complete original two/three-choice object is required')
    return count,2+count*2

def labels(raw):
    count,base=count_and_base(raw)
    offsets=struct.unpack_from('<'+str(count)+'H',raw,2)
    if offsets[0]!=0 or list(offsets)!=sorted(set(offsets)) or any(o%2 or o>=len(raw)-base for o in offsets):
        raise ValueError('Original aligned ordered native index table required')
    values=[]
    for index,offset in enumerate(offsets):
        stop=base+offsets[index+1] if index+1<count else len(raw)
        chunk=raw[base+offset:stop];end=chunk.find(b'\0')
        if end<1 or any(chunk[end:]) or len(chunk)%2:
            raise ValueError('Complete terminated caption and owned zero alignment required')
        values.append(chunk[:end])
    return values

def compile_choices(source,current,rows,*,require_formatting=True):
    original,prior=labels(source),labels(current)
    count=len(original)
    if len(prior)!=count or not isinstance(rows,list) or len(rows)!=count or [r.get('source_index') for r in rows]!=list(range(count)):
        raise ValueError('Every original source index in order is required')
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
    if cursor>65535:raise ValueError('Native choice offset bounds exceeded')
    target=struct.pack('<'+str(count+1)+'H',0x2100 if count==2 else 0x2200,*offsets)+b''.join(chunks)
    if labels(target)!=[r['english'].encode('ascii') for r in rows]:
        raise ValueError('Native caption order or complete bytes changed')
    return target
