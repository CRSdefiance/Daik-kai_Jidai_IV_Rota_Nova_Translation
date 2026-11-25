"""Independently reconstruct all6 Hodram outcome speeches and every affected relative operand in memory."""
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha

def rebuild(archive,arm,rows):
    from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
    inventory,_,_=scoped_inventory()
    container=IlnkContainer.parse(archive)
    if len(container.blocks)!=325 or len(rows)!=6 or sorted({r['block'] for r in rows})!=[47,48]:
        raise ValueError('Exact6 SC1 B47/B48 records and325 blocks required')
    blocks=list(container.blocks);groups=[]
    for number in [47,48]:
        original=container.blocks[number];end=8+struct.unpack_from('<H',original,4)[0]
        if end>len(original) or len(original)-end not in [0,2] or original[end:]!=bytes(len(original)-end):
            raise ValueError('Original logical end andseparate zero storage tail required')
        commands,speeches=inventory(arm,original);by_old={c['offset']:c for c in commands}
        boundaries=set(by_old)|{end};patches=[]
        selected=[r for r in rows if r['block']==number]
        if len(selected)!={47:3,48:3}[number]:raise ValueError('Exact per-block complete speech count required')
        for row in selected:
            at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);value=bytes.fromhex(row['compiled_hex']);header=at-5
            if header not in by_old or by_old[header]['word']!=0x4000 or original[at:at+len(old)+1]!=old+b'\0':
                raise ValueError('Exact original source-qualified speech reference required')
            if original[header:at+1].hex()!=row['source_complete_preamble_hex'] or old[0]!=row['source_selector']:
                raise ValueError('Complete source six-byte speech preamble required')
            if value[0]!=old[0] or b'\0' in value[1:] or not value[1:] or value[0] not in [2,254]:
                raise ValueError('Exact source actor andcomplete NUL-free reviewed body required')
            pad=len(value)%2!=len(old)%2;stored=value+(b' ' if pad else b'')
            if len(stored)%2!=len(old)%2:raise ValueError('Original speech byte parity required')
            patches.append(dict(id=row['id'],start=at,end=at+len(old),old=old,new=stored,compiled=value,parity_space_added=pad,
                source_complete_preamble_hex=row['source_complete_preamble_hex']))
        patches.sort(key=lambda r:r['start'])
        if any(a['end']>b['start'] for a,b in zip(patches,patches[1:])):raise ValueError('Overlapping sparse speech spans')
        def location(offset):
            change=0
            for patch in patches:
                if offset<patch['start']:break
                if patch['start']<offset<patch['end']:raise ValueError('Interior command reference inside replaced speech')
                if offset==patch['start']:return offset+change
                change+=len(patch['new'])-len(patch['old'])
            return offset+change
        output=bytearray();cursor=0
        for patch in patches:output.extend(original[cursor:patch['start']]);output.extend(patch['new']);cursor=patch['end']
        output.extend(original[cursor:end])
        if len(output)!=location(end) or len(output)>=0x2400:raise ValueError('Original complete native cache bound required')
        fixups=[]
        for command in commands:
            word=command['word'];offset=command['offset']
            if word not in [0x100,0x200,0x300,0x400]:continue
            span=struct.unpack_from('<H',original,offset+2)[0];destination=offset+4+span
            if offset+4 not in boundaries or destination not in boundaries:raise ValueError('Original relative target isnot acommand boundary')
            new_offset,new_target=location(offset),location(destination);new_span=new_target-new_offset-4
            if not 0<=new_span<=0xFFFF or new_span%2:raise ValueError('Complete even native relative span required')
            struct.pack_into('<H',output,new_offset+2,new_span)
            fixups.append(dict(offset=offset,word=word,source_span=span,matched_skip_target=destination,new_offset=new_offset,
                new_unmatched_next=new_offset+4,new_matched_skip_target=new_target,target_span=new_span))
        struct.pack_into('<H',output,4,len(output)-8);target=bytes(output)+bytes(-len(output)%4)
        final_commands,final_speeches=inventory(arm,target);by_new={c['offset']:c for c in final_commands}
        if len(final_commands)!=len(commands) or len(final_speeches)!=len(speeches):raise ValueError('All original commands andspeech memberships required')
        maps=[];unchanged=0
        for before in commands:
            after=by_new.get(location(before['offset']));word=before['word']
            if after is None or after['word']!=word or after['native_extent']!=location(before['offset']+before['native_extent'])-after['offset']:
                raise ValueError('Native command order,extent ormapped boundary changed')
            if after['ancestor_0100_offsets']!=[location(a) for a in before['ancestor_0100_offsets']]:raise ValueError('Nested source conditional scopes changed')
            oldraw,newraw=bytes.fromhex(before['whole_command_hex']),bytes.fromhex(after['whole_command_hex'])
            if word==0x4000:
                if oldraw[:6]!=newraw[:6]:raise ValueError('Original full speech preamble changed')
                if before['offset'] not in {p['start']-5 for p in patches}:
                    if oldraw!=newraw:raise ValueError('Unowned speech changed')
                    unchanged+=1
            elif word in [0x100,0x200,0x300,0x400]:
                if oldraw[:2]!=newraw[:2]:raise ValueError('Relative opcode changed')
            elif oldraw!=newraw:raise ValueError('Opaque effect,typed choice ornormal end changed')
            maps.append(dict(word=word,old_offset=before['offset'],new_offset=after['offset'],old_extent=before['native_extent'],new_extent=after['native_extent'],
                source_0100_ancestors=before['ancestor_0100_offsets'],target_0100_ancestors=after['ancestor_0100_offsets']))
        if final_commands[-1]['word']!=0 or final_commands[-1]['native_extent']!=4 or final_commands[-1]['offset']+4!=len(output):
            raise ValueError('Complete four-byte terminal must be distinct from storage tail')
        inverse=bytearray(target[:len(output)]);inverse[:8]=original[:8]
        for fixup in fixups:struct.pack_into('<H',inverse,fixup['new_offset']+2,fixup['source_span'])
        texts=[]
        for patch in reversed(patches):
            start=location(patch['start']);inverse[start:start+len(patch['new'])]=patch['old']
        if bytes(inverse)+original[end:]!=original:raise ValueError('Every predecessor block byte must invert exactly')
        for patch in patches:
            start=location(patch['start'])
            if target[start:start+len(patch['new'])+1]!=patch['new']+b'\0' or target[start-5:start+1].hex()!=patch['source_complete_preamble_hex']:
                raise ValueError('Complete final source-qualified speech reference required')
            texts.append(dict(id=patch['id'],old_offset=patch['start'],old_length=len(patch['old']),old_hex=patch['old'].hex(),new_offset=start,
                new_length=len(patch['new']),target_hex=patch['new'].hex(),compiled_hex=patch['compiled'].hex(),parity_space_added=patch['parity_space_added'],
                new_record_index=target[:start].count(b'\0')))
        blocks[number]=target
        groups.append(dict(block=number,source_block_sha256=sha(original),target_block_sha256=sha(target),source_bytes=len(original),source_logical_end=end,
            source_tail_bytes=len(original)-end,target_bytes=len(target),target_logical_end=len(output),target_tail_bytes=len(target)-len(output),
            source_header_hex=original[:8].hex(),target_header_hex=target[:8].hex(),text_records=texts,relative_fixups=fixups,command_map=maps,
            all_current_commands=commands,all_target_commands=final_commands,total_speeches=len(speeches),unchanged_speeches=unchanged,target_block=target,
            complete_predecessor_block_inverse_exact=True,clean_source_inverse_checked_separately_by_sourcequalified_seal=True))
    result=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(result)
    if [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]!=[47,48]:raise ValueError('Exactly two reviewed blocks may change')
    inverse_blocks=list(parsed.blocks)
    for g in groups:inverse_blocks[g['block']]=container.blocks[g['block']]
    if IlnkContainer(inverse_blocks).to_bytes()!=archive:raise ValueError('Every predecessor archive byte must invert exactly')
    if sum(len(g['all_target_commands']) for g in groups)!=15 or sum(len(g['relative_fixups']) for g in groups)!=0 or sum(g['unchanged_speeches'] for g in groups)!=0:
        raise ValueError('Complete15commands/zerorelative sites/all6speech bodies required')
    return dict(target_archive=result,groups=groups,unchanged_archive_blocks=323,complete_predecessor_archive_inverse_exact=True)
