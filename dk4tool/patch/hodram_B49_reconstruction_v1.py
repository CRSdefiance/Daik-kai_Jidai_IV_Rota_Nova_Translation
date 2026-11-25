"""Reconstruct only approved speech bodies andsource-owned relative/header lengths."""
import struct
from dk4tool.patch.grand_race_menu_release import sha
def require(value,label):
    if not value:raise ValueError('Hodram B49 reconstruction: '+label)
def reconstruct(old,clean,group,packet,rows,edges,choice_rows,typed):
    require(group['block']==packet['block'] and group['file_path']=='/data/SC1.DK4','file/block identity')
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

    require(len(group['choice_commands'])==1 and len(choice_rows)==2,'one complete two-choice menu')
    choice=group['choice_commands'][0];at=choice['old_offset'];before=bytes.fromhex(choice['old_hex']);ja=bytes.fromhex(choice['clean_hex'])
    require(at==574 and len(before)==len(ja)==choice['old_length']==26 and choice['count']==2 and choice['word']==0x2100,'source menu extent/count')
    require(old[at:at+26]==before and clean[at:at+26]==ja,'literal source/current complete menu')
    require(typed.hex()==choice['target_hex'] and len(typed)==choice['new_length']==22,'compiled complete menu')
    require(choice['record_IDs']==[r['id'] for r in choice_rows] and choice['labels']==[r['english'] for r in choice_rows],'original choice order')
    for index,(row,ref) in enumerate(zip(choice_rows,choice['label_references'],strict=True)):
        require(row['option_index']==ref['option_index']==index and row['current_choice_command_offset']==at and row['block']==group['block'] and row['file_path']==group['file_path'],'choice scope/index')
        require(row['id']==ref['id'] and row['source_reference']==ref['source_reference'] and row['current_reference']==ref['old_reference'],'source/current choice references')
        for data,key,reference in [(old,'current_hex',row['current_reference']),(clean,'source_hex',row['source_reference'])]:
            offset=reference['offset'];raw=bytes.fromhex(row[key])
            require(data[offset:offset+len(raw)+1]==raw+b'\0' and data[:offset].count(b'\0')==reference['record_index'],'literal choice record')
        require(row['english'].encode('ascii').hex()==ref['target_hex']==row['compiled_hex'] and len(row['english'])==ref['new_length'],'choice bytes')
    patches.append(dict(start=at,end=at+36,old=before,source=ja,value=typed,id='complete-native-menu'))

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
        elif word==0x2100:require(a==choice['old_offset'] and z==choice['new_offset'] and target[z:z+new['native_extent']]==typed,'complete original-provider menu')
        else:require(previous['whole_command_hex']==new['whole_command_hex'],'opaque control/resource/effect/wait/end')
    require(commands[-1]['word']==newcommands[-1]['word']==0 and newcommands[-1]['native_extent']==4 and newcommands[-1]['offset']+4==len(logical),'complete four-byte terminal')
    for ref in refs.values():
        at=ref['new_offset']
        require(mapped(ref['old_offset'])==at and target[at:at+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0' and target[:at].count(b'\0')==ref['new_record_index'],'final stored references')

    require(mapped(choice['old_offset'])==choice['new_offset']==518,'relocated complete menu offset')
    for ref in choice['label_references']:
        field=choice['new_offset']+2+2*ref['option_index'];base=choice['new_offset']+6;relative=struct.unpack_from('<H',target,field)[0]
        at=base+relative
        require(field==ref['relative_table_field'] and base==ref['relative_base'] and relative==ref['relative_offset'],'native menu internal table')
        require(at==ref['new_offset'] and target[at:at+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0' and target[:at].count(b'\0')==ref['new_record_index'],'final choice reference')

    for clean_version in [False,True]:
        base=clean if clean_version else old;restored=bytearray(target[:len(logical)]);restored[:8]=base[:8]
        for fix in group['relative_fixups']:struct.pack_into('<H',restored,fix['new_offset']+2,fix['source_span'])
        for patch in reversed(patches):
            at=mapped(patch['start']);restored[at:at+len(patch['value'])]=patch['source'] if clean_version else patch['old']
        baseend=8+struct.unpack_from('<H',base,4)[0]
        require(bytes(restored)+base[baseend:]==base,'full clean/predecessor block inverse')
    return target
