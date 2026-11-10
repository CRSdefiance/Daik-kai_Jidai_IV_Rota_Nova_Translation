"""Eight-slot native personality object with source-owned aliases and virtual prefix."""
import struct

def unpack(raw):
    if not isinstance(raw,bytes) or len(raw)<22 or raw[:2]!=b'\0A' or len(raw)%2:
        raise ValueError('A complete aligned original 4100 object is required')
    offsets=list(struct.unpack_from('<8H',raw,2));unique=sorted(set(offsets))
    if unique[0]!=0 or any(o%2 or o>=len(raw)-20 for o in unique):
        raise ValueError('Source-owned aligned style offsets required')
    texts={}
    for index,offset in enumerate(unique):
        end=20+unique[index+1] if index+1<len(unique) else len(raw)
        chunk=raw[20+offset:end];zero=chunk.find(b'\0')
        if zero<1 or any(chunk[zero:]) or len(chunk)%2:
            raise ValueError('Complete terminated style body and owned alignment required')
        texts[offset]=chunk[:zero]
    return offsets,texts

def compile_styles(source,current,rows,plans,*,require_formatting=True):
    old_offsets,original=unpack(source);current_offsets,prior=unpack(current)
    if source[18:20]!=current[18:20] or source[18]!=0:
        raise ValueError('Original style flag and selector must remain exact')
    if any((old_offsets[a]==old_offsets[b])!=(current_offsets[a]==current_offsets[b]) for a in range(8) for b in range(8)):
        raise ValueError('Exact original personality alias equivalence required')
    ordered=sorted(original)
    if len(rows)!=len(ordered):raise ValueError('Every physical source style body is required')
    chunks=[];new_offsets={};cursor=0
    for row,offset in zip(rows,ordered,strict=True):
        indices=[i for i,value in enumerate(old_offsets) if value==offset]
        if row.get('native_object_kind')!='4100-style-alternative' or row.get('source_style_indices')!=indices or row.get('current_style_indices')!=indices:
            raise ValueError('Source-ordered physical body and every alias slot required')
        if row.get('source_header_hex')!=source[:20].hex() or row.get('source_choice_object_hex')!=source.hex() or row.get('current_style_object_hex')!=current.hex():
            raise ValueError('Exact source/current complete object bindings required')
        if row.get('source_hex')!=original[offset].hex() or row.get('current_hex')!=prior[current_offsets[indices[0]]].hex():
            raise ValueError('Exact individual source/current body bindings required')
        if row.get('source_selector')!=source[19] or not row.get('virtual_formatter_prefix_is_not_part_of_stored_alternative_text'):
            raise ValueError('Original selector and formatter-only prefix declaration required')
        gates=['source','context','localization','naturalness']+(['formatting'] if require_formatting else [])
        if any(row.get('review',{}).get(g) is not True for g in gates):raise ValueError('Individual editorial gates required')
        plan=plans[row['id']]
        if plan['logical_English']!=row['english'] or plan['source_selector']!=source[19] or plan['planning_record']['source_hex']!=(bytes([source[19]])+original[offset]).hex():
            raise ValueError('Exact source-qualified virtual-prefix formatting plan required')
        raw=bytes.fromhex(plan['encoded_hex'])
        if len(raw)<2 or raw[0]!=source[19] or b'\0' in raw[1:]:raise ValueError('Complete compiled body and virtual selector required')
        # The 4100 command header carries the selector. Never duplicate it in a body.
        body=raw[1:]
        new_offsets[offset]=cursor;chunk=body+b'\0';chunk+=bytes(-len(chunk)%2)
        chunks.append(chunk);cursor+=len(chunk)
    if cursor>65535:raise ValueError('Native style offset bounds exceeded')
    result=struct.pack('<9H',0x4100,*[new_offsets[o] for o in old_offsets])+source[18:20]+b''.join(chunks)
    target_offsets,target_texts=unpack(result)
    if len(target_texts)!=len(original) or any((old_offsets[a]==old_offsets[b])!=(target_offsets[a]==target_offsets[b]) for a in range(8) for b in range(8)):
        raise ValueError('Source physical-body ownership and aliases changed')
    return result
