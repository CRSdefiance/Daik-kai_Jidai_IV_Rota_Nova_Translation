"""Bind every clean/current/final record and both complete blocks independently."""
from copy import deepcopy
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B31_B53_reconstruction_v1 import reconstruct
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
PATH='/data/SC1.DK4'

def reconstruct_and_bind(parent,clean,reference,doc,data,require):
    mapping,packet,source=data['relocation'],data['current'],data['source_controls']
    archive=parent.read_file(PATH);arm=parent.read_file('/__arm9__.bin')
    require(doc['file_path']==packet['file_path']==mapping['file_path']==PATH and doc['route']==1 and doc['blocks']==[31,53],'exact owned two-block scope')
    require(sha(bytes(parent.rom.save()))==doc['current_ROM_sha256']==packet['current_ROM_sha256']==mapping['candidate_sha256'],'whole in-memory registered predecessor')
    require(sha(bytes(reference.rom.save()))==doc['reference_ROM_sha256'],'whole reviewed reference')
    require(sha(archive)==doc['current_archive_sha256']==packet['current_archive_sha256']==mapping['source_archive_sha256'],'complete predecessor archive')
    require([g['block'] for g in packet['groups']]==[g['block'] for g in mapping['groups']]==[g['block'] for g in source['groups']]==[31,53],'complete ordered two-block source groups')
    current=IlnkContainer.parse(archive).blocks;original=IlnkContainer.parse(clean.read_file(PATH)).blocks
    require(len(current)==len(original)==325,'complete source/current block index')
    inventory,unused_walker,unused_fn=scoped_inventory();blocks=list(current);target_blocks={};finalgroups=[];allrefs=[]
    for group,prior,src in zip(mapping['groups'],packet['groups'],source['groups'],strict=True):
        number=group['block'];rows=[r for r in doc['records'] if r['block']==number]
        require(prior['block']==src['block']==number,'source/current group identity')
        old,japanese=current[number],original[number]
        require(old.hex()==prior['current_block_hex'] and japanese.hex()==prior['clean_block_hex'],'complete literal source/current blocks')
        target=reconstruct(old,japanese,group,prior,rows,src['operands_requiring_adjustment_when_resizing'])
        cleancommands,cleantexts=inventory(arm,japanese);oldcommands,oldtexts=inventory(arm,old);commands,texts=inventory(arm,target)
        require(cleancommands==prior['all_source_commands']==src['all_original_source_commands'] and oldcommands==prior['all_current_commands']==group['all_current_commands'] and commands==group['all_target_commands'],'independently parsed source/current/final command inventories')
        require(len(cleancommands)==len(oldcommands)==len(commands)==len(group['command_map'])==9 and len(cleantexts)==len(oldtexts)==len(texts)==len(rows)==(2 if number==31 else 1),'all9commands andcomplete speech membership')
        for a,b,c,m in zip(cleancommands,oldcommands,commands,group['command_map'],strict=True):
            require(a['word']==b['word']==c['word']==m['word'] and b['offset']==m['old_offset'] and c['offset']==m['new_offset'],'complete command correspondence')
            if c['word']==0x4000:require(a['whole_command_hex'][:12]==b['whole_command_hex'][:12]==c['whole_command_hex'][:12],'every original six-byte speaker/layout preamble')
            elif c['word'] not in [0x100,0x200,0x300,0x400]:require(a['whole_command_hex']==b['whole_command_hex']==c['whole_command_hex'],'all original queries/opaque controls/fullterminal')
        require(commands[-1]['word']==0 and commands[-1]['native_extent']==4 and commands[-1]['offset']+4==group['target_logical_end'],'complete terminal before separate alignment tail')
        require(len(group['relative_fixups'])==(4 if number==31 else 0) and sum(len(r['cases']) for r in group['relocated_skip_cases'])==(20 if number==31 else 0),'all mapped relative sites andnative cases')
        refs={r['id']:r for r in group['text_records']}
        require(len(refs)==len(rows)==len({r['id'] for r in rows}),'complete unique canonical speech identities')
        for row in rows:
            ref=refs[row['id']];sr,cr,fr=row['source_reference'],row['current_reference'],row['final_reference'];raw=bytes.fromhex(row['source_hex']);before=bytes.fromhex(row['current_hex']);value=bytes.fromhex(ref['target_hex'])
            for block,record,expected in [(japanese,sr,raw),(old,cr,before),(target,fr,value)]:
                at=record['offset'];require(record['block']==number and record['bytes']==len(expected) and block[at:at+len(expected)+1]==expected+b'\0' and block[:at].count(b'\0')==record['record_index'],'complete source/current/final reference:'+row['id'])
                require(record['header_offset']==at-5 and block[at-5:at+1].hex()==row['source_complete_preamble_hex'],'complete source/current/final header:'+row['id'])
            expected=dict(file_path=PATH,block=number,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=sha(target))
            require(fr==expected and row['final_hex']==row['stored_hex']==ref['target_hex'] and ref['compiled_hex']==row['compiled_hex'],'exact reviewed final reference/body/parity:'+row['id'])
            allrefs.append(dict(id=row['id'],source_reference=sr,current_reference=cr,final_reference=fr))
        target_blocks[number]=target;blocks[number]=target;finalgroups.append({**group,'target_block':target})
    require(len(allrefs)==len(doc['records'])==3 and len({r['id'] for r in allrefs})==3,'three disjoint source identities andcomplete batch coverage')
    target_archive=IlnkContainer(blocks).to_bytes();final=IlnkContainer.parse(target_archive).blocks
    require(sha(target_archive)==mapping['target_archive_sha256'] and target_archive==reference.read_file(PATH),'independent entire archive equals reviewed reference')
    require([i for i,(a,b) in enumerate(zip(current,final,strict=True)) if a!=b]==[31,53],'all323 other blocks unchanged')
    inverse=list(final)
    for number in [31,53]:inverse[number]=current[number]
    require(IlnkContainer(inverse).to_bytes()==archive,'complete predecessor archive inverse')
    planned=deepcopy(parent);planned.replace_file(PATH,target_archive)
    require(bytes(planned.rom.save())==bytes(reference.rom.save()),'independent whole reference image equality')
    require([p for _,p,v in parent.iter_files() if planned.read_file(p)!=v]==[PATH] and all(planned.read_file(p)==v for p,v in parent.iter_components()),'every unowned file/component unchanged')
    restored=deepcopy(planned);restored.replace_file(PATH,archive)
    require(bytes(restored.rom.save())==bytes(parent.rom.save()),'whole in-memory predecessor inverse including canonical-source lifecycle')
    return dict(target_blocks=target_blocks,target_archive=target_archive,groups=finalgroups,
        summary=dict(editorial_references=3,speeches=3,typed_choices=0,blocks=[31,53],commands=18,relative_sites=4,query_sites=1,unowned_blocks=323,
            exact_source_current_final_references=allrefs,complete_clean_current_block_inverses=True,complete_archive_andwhole_inmemory_ROM_inverse=True,whole_reference_ROM_equal=True,new_credit=0))
