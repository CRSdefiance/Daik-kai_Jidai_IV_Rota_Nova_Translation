"""Reconstruct only approved speech bodies andsource-owned relative/header lengths."""
import struct
from dk4tool.patch.grand_race_menu_release import sha
def require(value,label):
    if not value:raise ValueError('Rafael B47 reconstruction: '+label)
def reconstruct(old,clean,group,packet,rows,edges):
    require(group['block']==packet['block'] and group['file_path']=='/data/SC0.DK4','file/block identity')
    require(sha(old)==group['source_block_sha256']==packet['current_block_sha256'] and sha(clean)==group['clean_block_sha256']==packet['clean_block_sha256'],'complete source/current block')
    end=8+struct.unpack_from('<H',old,4)[0]
    require(end==group['source_logical_end']==packet['current_logical_end'] and len(old)==group['source_bytes'] and old[end:]==bytes(group['source_tail_bytes']),'complete source extent/tail')
    require(old[:4]==clean[:4]==b'CS\0\1' and old[6:8]==clean[6:8],'source header andmetadata')
    refs={r['id']:r for r in group['text_records']}
    require(set(refs)=={r['id'] for r in rows} and len(refs)==len(rows),'complete unique paragraph set')
    patches=[]
    for row in rows:
        ident=row['id'];ref=refs[ident];raw=bytes.fromhex(row['source_hex']);before=bytes.fromhex(row['current_hex'])
        at=row['current_reference']['offset'];ja=row['source_reference']['offset'];value=bytes.fromhex(row['compiled_hex'])
        require(row['block']==group['block'] and row['file_path']==group['file_path'],'record file/block:'+ident)
        require(row['source_reference']==ref['source_reference'] and row['current_reference']==ref['current_reference'],'exact references:'+ident)
        require(old[at:at+len(before)+1]==before+b'\0' and clean[ja:ja+len(raw)+1]==raw+b'\0','literal source/current:'+ident)
        require(old[:at].count(b'\0')==row['current_record_index'] and at==ref['old_offset'] and len(before)==ref['old_length'] and before.hex()==ref['old_hex'],'current record boundary:'+ident)
        require(raw[0]==before[0]==value[0]==row['source_selector']==ref['source_selector'],'selector:'+ident)
        preamble=row['source_complete_preamble_hex']
        require(old[at-5:at+1].hex()==clean[ja-5:ja+1].hex()==preamble==ref['source_complete_preamble_hex'],'complete six-byte preamble:'+ident)
        require(value.hex()==ref['compiled_hex'] and b'\0' not in value[1:],'compiled bytes:'+ident)
        pad=len(value)%2!=len(before)%2
        if pad:value+=b' '
        require(pad==ref['parity_space_added'] and value.hex()==ref['target_hex'] and len(value)==ref['new_length'],'stored parity:'+ident)
        for token in [b'FI',b'FA',b'FO']:require(raw[1:].count(token)==value[1:].count(token),'original runtime substitution:'+ident)
        patches.append(dict(start=at,end=at+len(before),old=before,source=raw,value=value,id=ident))
    patches.sort(key=lambda p:p['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'disjoint source replacements')
    def mapped(at):
        delta=0
        for patch in patches:
            if at<patch['start']:break
            require(not patch['start']<at<patch['end'],'interior reference in replaced body')
            if at==patch['start']:return at+delta
            delta+=len(patch['value'])-len(patch['old'])
        return at+delta
    chunks=[];last=0
    for patch in patches:chunks.extend([old[last:patch['start']],patch['value']]);last=patch['end']
    chunks.append(old[last:end]);logical=bytearray(b''.join(chunks))
    require(len(logical)==mapped(end)==group['target_logical_end'] and len(logical)<0x2400,'bounded original native cache')
    selected=[e for e in edges if e['block']==group['block']]
    require(len(selected)==len(group['relative_fixups']),'all original relative operands')
    for edge,fix in zip(selected,group['relative_fixups'],strict=True):
        require(all(fix[k]==v for k,v in edge.items()),'original relative operand identity')
        start=mapped(edge['offset']);finish=mapped(edge['matched_skip_target']);span=finish-start-4
        require(0<=span<=0xFFFF and span%2==0 and struct.unpack_from('<H',logical,start)[0]==edge['word'],'source-owned relative word/span')
        require(fix['new_offset']==start and fix['new_unmatched_next']==start+4 and fix['new_matched_skip_target']==finish and fix['target_span']==span,'exact mapped relative endpoints')
        require(struct.unpack_from('<H',old,edge['offset']+2)[0]==edge['source_span'],'original relative span')
        struct.pack_into('<H',logical,start+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    require(len(target)==group['target_bytes'] and len(target)-len(logical)==group['target_tail_bytes'] and sha(target)==group['target_block_sha256'],'whole target block andseparate tail')
    require(target[:8].hex()==group['target_header_hex'],'exact target header')
    commands=packet['all_current_commands'];mapping=group['command_map'];newcommands=group['all_target_commands']
    require(len(commands)==len(mapping)==len(newcommands),'all source/control commands')
    for previous,cm,new in zip(commands,mapping,newcommands,strict=True):
        a,z=previous['offset'],cm['new_offset'];word=previous['word']
        require(cm['word']==new['word']==word and cm['old_offset']==a and z==mapped(a)==new['offset'],'command identity/offset')
        require(cm['old_extent']==previous['native_extent'] and cm['new_extent']==new['native_extent']==mapped(a+previous['native_extent'])-z,'complete native extent')
        require(cm['source_0100_ancestors']==previous['ancestor_0100_offsets'] and cm['target_0100_ancestors']==new['ancestor_0100_offsets']==[mapped(v) for v in previous['ancestor_0100_offsets']],'nested ancestor scope')
        require(target[z:z+new['native_extent']].hex()==new['whole_command_hex'],'target full command bytes')
        if word==0x4000:require(old[a:a+6]==target[z:z+6],'speaker/style/layout preamble')
        elif word in [0x100,0x200,0x300,0x400]:require(old[a:a+2]==target[z:z+2],'original relative opcode')
        else:require(previous['whole_command_hex']==new['whole_command_hex'],'opaque control/resource/effect/wait/end')
    require(commands[-1]['word']==newcommands[-1]['word']==0 and newcommands[-1]['native_extent']==4 and newcommands[-1]['offset']+4==len(logical),'complete four-byte terminal')
    for ref in refs.values():
        at=ref['new_offset']
        require(mapped(ref['old_offset'])==at and target[at:at+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0' and target[:at].count(b'\0')==ref['new_record_index'],'final stored references')
    for clean_version in [False,True]:
        base=clean if clean_version else old;restored=bytearray(target[:len(logical)]);restored[:8]=base[:8]
        for fix in group['relative_fixups']:struct.pack_into('<H',restored,fix['new_offset']+2,fix['source_span'])
        for patch in reversed(patches):
            at=mapped(patch['start']);restored[at:at+len(patch['value'])]=patch['source'] if clean_version else patch['old']
        baseend=8+struct.unpack_from('<H',base,4)[0]
        require(bytes(restored)+base[baseend:]==base,'full clean/predecessor block inverse')
    return target
