"""Independently bind clean/current/final references and full reversible native command maps."""
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_rebuild_v1 import rebuild

PATH='/data/SC1.DK4'

def require(ok,message):
    if not ok:raise ValueError('Hodram source-qualified reconstruction: '+message)

def reconstruct_and_bind(image,clean,doc,research,packet):
    from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
    inventory,_,_=scoped_inventory();archive=image.read_file(PATH);arm=image.read_file('/__arm9__.bin')
    require(doc['file_path']==packet['file_path']==research['file_path']==PATH,'exact SC1 file')
    require(sha(archive)==doc['current_archive_sha256']==packet['current_archive_sha256']==research['source_archive_sha256'],'complete previous archive hash')
    current=IlnkContainer.parse(archive).blocks;original=IlnkContainer.parse(clean.read_file(PATH)).blocks
    result=rebuild(archive,arm,doc['records']);final=IlnkContainer.parse(result['target_archive']).blocks
    require(sha(result['target_archive'])==research['target_archive_sha256'],'independent entire target archive')
    require(len(result['groups'])==len(research['groups'])==len(packet['groups'])==2 and result['unchanged_archive_blocks']==323,'two complete groups/323 unowned blocks')
    totalclean=0;totalrelatives=0;totalspeeches=0
    for fresh,declared,prior in zip(result['groups'],research['groups'],packet['groups'],strict=True):
        number=fresh['block'];require(number==declared['block']==prior['block'] and number in [47,48],'ordered block identity')
        old,source,target=current[number],original[number],fresh['target_block']
        require(sha(old)==prior['current_block_sha256']==declared['source_block_sha256'] and sha(source)==prior['clean_block_sha256']==declared['clean_block_sha256'],'whole clean/current source blocks')
        require(old.hex()==prior['current_block_hex'] and source.hex()==prior['clean_block_hex'] and old[:8].hex()==prior['current_header_hex'] and source[:8].hex()==prior['source_header_hex'],'complete stored source literals/headers')
        cleancommands,cleantexts=inventory(arm,source);require(cleancommands==prior['all_source_commands']==declared['all_source_commands'],'independently parsed complete clean source commands')
        require(fresh['all_current_commands']==prior['all_current_commands']==declared['all_current_commands'],'independently parsed complete predecessor commands')
        require(fresh['all_target_commands']==declared['all_target_commands'],'independently parsed complete final commands')
        for key in ['source_block_sha256','target_block_sha256','source_bytes','source_logical_end','source_tail_bytes','target_bytes','target_logical_end','target_tail_bytes','source_header_hex','target_header_hex']:
            require(fresh[key]==declared[key],'whole block/length/tail/header identity:'+key)
        require(len(cleancommands)==len(fresh['command_map'])==len(declared['command_map']),'all clean/current/final command identities')
        clean_by_current={oldc['offset']:c for oldc,c in zip(fresh['all_current_commands'],cleancommands,strict=True)}
        for c,m,dm in zip(cleancommands,fresh['command_map'],declared['command_map'],strict=True):
            expected=dict(**m,clean_offset=c['offset'],clean_extent=c['native_extent'],clean_0100_ancestors=c['ancestor_0100_offsets'])
            require(expected==dm,'every original/current/final command map field')
            oldc=next(x for x in fresh['all_current_commands'] if x['offset']==m['old_offset'])
            require(c['word']==m['word'] and source[c['offset']:c['offset']+c['native_extent']].hex()==c['whole_command_hex'],'clean command bytes/identity')
            if c['word']==0x4000:require(c['whole_command_hex'][:12]==oldc['whole_command_hex'][:12],'complete clean/current sixbyte preamble')
            elif c['word'] not in [0x100,0x200,0x300,0x400]:require(c['whole_command_hex']==oldc['whole_command_hex'],'clean/current opaque command identity')
        require(len(fresh['relative_fixups'])==len(declared['relative_fixups']),'all native relative operands')
        for f,d in zip(fresh['relative_fixups'],declared['relative_fixups'],strict=True):
            require(all(d.get(k)==v for k,v in f.items()),'independently relocated relative operand')
            c=clean_by_current[f['offset']];clean_span=struct.unpack_from('<H',source,c['offset']+2)[0]
            require(d['unmatched_next']==f['offset']+4 and d['clean_offset']==c['offset'] and d['clean_span']==clean_span,'clean andunmatched relative identity')
        selected=[r for r in doc['records'] if r['block']==number];refs={r['id']:r for r in fresh['text_records']}
        declaredrefs={r['id']:r for r in declared['text_records']}
        require(len(selected)==len(cleantexts)==fresh['total_speeches']==len(refs) and fresh['unchanged_speeches']==0,'all source speeches owned exactly once')
        for row in selected:
            ident=row['id'];ref=refs[ident];d=declaredrefs[ident];sr,cr=row['source_reference'],row['current_reference'];raw=bytes.fromhex(row['source_hex']);before=bytes.fromhex(row['current_hex'])
            require(all(d.get(k)==v for k,v in ref.items()),'every independently relocated text reference:'+ident)
            require(row['file_path']==PATH and sr['block']==cr['block']==number and sr['offset']==sr['header_offset']+5 and cr['offset']==cr['header_offset']+5,'source qualified body/header reference:'+ident)
            require(source[sr['offset']:sr['offset']+len(raw)+1]==raw+b'\0' and old[cr['offset']:cr['offset']+len(before)+1]==before+b'\0','literal full source/current body andNUL:'+ident)
            require(sr['bytes']==len(raw) and cr['bytes']==len(before) and source[:sr['offset']].count(b'\0')==sr['record_index']==row['source_record_index'],'complete clean source boundary:'+ident)
            require(old[:cr['offset']].count(b'\0')==cr['record_index']==row['current_record_index'],'complete predecessor source boundary:'+ident)
            require(source[sr['offset']-5:sr['offset']+1].hex()==old[cr['offset']-5:cr['offset']+1].hex()==row['source_complete_preamble_hex'],'sixbyte source/current preamble:'+ident)
            finalref=dict(file_path=PATH,block=number,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=sha(target))
            pending={k:finalref[k] for k in ['offset','bytes','header_offset','record_index']}
            require(row['integrated_reference_pending']==pending and row['final_stored_hex']==ref['target_hex'],'complete final body/header/record reference inexact source-qualified block:'+ident)
            require(row['source_selector']==raw[0]==before[0]==bytes.fromhex(ref['target_hex'])[0],'original static speaker:'+ident)
        inverse=bytearray(target[:fresh['target_logical_end']]);inverse[:8]=source[:8]
        for fix in fresh['relative_fixups']:
            c=clean_by_current[fix['offset']];struct.pack_into('<H',inverse,fix['new_offset']+2,struct.unpack_from('<H',source,c['offset']+2)[0])
        for row in sorted(selected,key=lambda r:refs[r['id']]['new_offset'],reverse=True):
            ref=refs[row['id']];at=ref['new_offset'];inverse[at:at+ref['new_length']]=bytes.fromhex(row['source_hex'])
        sourceend=8+struct.unpack_from('<H',source,4)[0]
        require(bytes(inverse)+source[sourceend:]==source,'every clean Japanese source block byte inverses')
        fresh.update(clean_block_sha256=sha(source),complete_clean_source_block_inverse_exact=True)
        totalclean+=len(cleancommands);totalrelatives+=len(fresh['relative_fixups']);totalspeeches+=len(selected)
    require((totalclean,totalrelatives,totalspeeches)==(15,0,6),'all15 commands/zero relatives/6speeches')
    require([i for i,(a,b) in enumerate(zip(current,final,strict=True)) if a!=b]==[47,48],'only two owned blocks change')
    return result

def serializable_groups(result):
    return [{k:v for k,v in g.items() if k not in ['target_block','all_current_commands']} for g in result['groups']]
