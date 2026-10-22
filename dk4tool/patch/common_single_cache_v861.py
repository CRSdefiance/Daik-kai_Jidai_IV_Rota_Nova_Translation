"""Bounded single8KiB COMMON cache in the existing two4KiB input allocation."""

import struct
from hashlib import sha256

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.livestock_prayer_editorial import current_entries as previous_entries
from dk4tool.script.common_message_table import CODE_LOCKS,DIRECTORY_OFFSET,TABLE_OFFSET,MESSAGE_COUNT,CommonMessageEntry

CACHE_AT=0x535E0
ORIGINAL=struct.pack('<2I',0xE3A03000,0xE0802003)
SINGLE=struct.pack('<2I',0xE3A00000,0xE12FFF1E)
CAPACITY=8192


def patch_cache(arm):
    assert arm[CACHE_AT:CACHE_AT+8]==ORIGINAL
    target=bytearray(arm);target[CACHE_AT:CACHE_AT+8]=SINGLE
    return bytes(target)


def entries(common,arm,directory_sha256):
    """Exact-directory parser for the specifically guarded single-cache policy."""
    assert arm[CACHE_AT:CACHE_AT+8]==SINGLE
    assert sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()==directory_sha256
    for low,high,digest in CODE_LOCKS:
        assert sha256(arm[low:high]).hexdigest()==digest
    blocks=IlnkContainer.parse(common).blocks;assert len(blocks)==41
    directory=[struct.unpack_from('<HH',arm,DIRECTORY_OFFSET+i*4) for i in range(41)]
    first_ids=[row[0] for row in directory]
    assert first_ids[0]==0 and first_ids==sorted(set(first_ids)) and first_ids[-1]<MESSAGE_COUNT
    offsets=struct.unpack_from(f'<{MESSAGE_COUNT+1}H',arm,TABLE_OFFSET);assert offsets[-1]==0
    result=[]
    for block_index,(first,size) in enumerate(directory):
        block=blocks[block_index];assert len(block)==size and 0<size<=CAPACITY
        last=first_ids[block_index+1] if block_index<40 else MESSAGE_COUNT
        starts=offsets[first:last];assert starts==tuple(sorted(set(starts)))
        records=[];position=0
        for index,raw in enumerate(block.split(b'\0')):
            if raw:records.append((index,position,position+len(raw)))
            position+=len(raw)+1
        for n in range(first,last):
            start,following=offsets[n:n+2];finish=following if following>=start else size
            owners=[(i,lo,hi) for i,lo,hi in records if lo<=start<hi]
            assert 0<=start<finish<=size and 0<finish-start<512 and len(owners)==1
            record,lo,hi=owners[0];end=min(finish,hi);text=block[start:end];text.decode('cp932')
            result.append(CommonMessageEntry(n,block_index,TABLE_OFFSET+n*2,start,finish,record,start-lo,end-lo,text))
    assert len(result)==MESSAGE_COUNT
    return result


def repack(common,arm,authored):
    before=previous_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    low,high=min(before[n].block for n in authored),max(before[n].block for n in authored)
    attempts=[]
    for count in range(high-low+1,len(blocks)+1):
        for first in range(max(0,high-count+1),min(low,len(blocks)-count)+1):
            last=first+count-1;selected=[e for e in before if first<=e.block<=last]
            if any(set(blocks[b][:next(e.block_offset for e in selected if e.block==b)])-{0,32} for b in range(first,last+1)):continue
            opaque,parts,part={},[],[];used=0
            for e in selected:
                payload=authored.get(e.message_id,e.text)+b'\0'
                tail=blocks[e.block][e.block_offset+len(e.text)+1:e.copy_end]
                if set(tail)-{0,32}:
                    assert e.message_id not in authored
                    payload=blocks[e.block][e.block_offset:e.copy_end];opaque[e.message_id]=payload
                assert 0<len(payload)<512
                if used+len(payload)>CAPACITY:parts.append(part);part=[];used=0
                part.append((e.message_id,payload));used+=len(payload)
            parts.append(part)
            attempts.append({'first':first,'last':last,'available_blocks':count,'minimum_blocks':len(parts),
                'payload_bytes':sum(len(p) for group in parts for n,p in group)})
            if len(parts)>count:continue
            # Preserve exactly41 nonempty directory groups when more blocks than
            # the minimum are available;whole messages remain in native ID order.
            while len(parts)<count:
                candidates=[(sum(len(p) for n,p in group),i) for i,group in enumerate(parts) if len(group)>1]
                assert candidates
                total,i=max(candidates);group=parts[i];running=0;cut=1
                for j,(n,payload) in enumerate(group[:-1],1):
                    running+=len(payload);cut=j
                    if running>=total//2:break
                parts[i:i+1]=[group[:cut],group[cut:]]
            groups=[]
            for group in parts:
                items=[];body=bytearray()
                for n,payload in group:items.append((n,len(body),payload));body.extend(payload)
                assert 0<len(body)<=CAPACITY;groups.append((items,bytes(body)))
            return before,blocks,first,last,selected,opaque,groups,attempts
    raise AssertionError('Complete reviewed prose exceeds existing41-block8KiB capacity')
