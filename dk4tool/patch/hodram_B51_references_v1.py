"""Bind every clean/current/final B51 record and full reversible NDS image independently."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B51_reconstruction_v1 import reconstruct
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

PATH='/data/SC1.DK4'

def reconstruct_and_bind(parent,clean,reference,doc,data,require):
    mapping,packet,source=data['relocation'],data['current'],data['source_controls']
    archive=parent.read_file(PATH);arm=parent.read_file('/__arm9__.bin')
    require(doc['file_path']==packet['file_path']==mapping['file_path']==PATH and doc['blocks']==[51],'exact owned B51 scope')
    require(sha(bytes(parent.rom.save()))==doc['current_ROM_sha256']==packet['current_ROM_sha256']==mapping['candidate_sha256'],'whole in-memory predecessor')
    require(sha(bytes(reference.rom.save()))==doc['reference_ROM_sha256'],'whole reviewed reference')
    require(sha(archive)==doc['current_archive_sha256']==packet['current_archive_sha256']==mapping['source_archive_sha256'],'complete predecessor archive')
    require(len(packet['groups'])==len(mapping['groups'])==1,'one complete exchange')
    group,prior=mapping['groups'][0],packet['groups'][0]
    current=IlnkContainer.parse(archive).blocks;original=IlnkContainer.parse(clean.read_file(PATH)).blocks
    require(group['block']==prior['block']==51 and len(current)==len(original)==325,'complete source/current block index')
    old,japanese=current[51],original[51]
    require(old.hex()==prior['current_block_hex'] and japanese.hex()==prior['clean_block_hex'],'complete literal source/current blocks')
    target=reconstruct(old,japanese,group,prior,doc['records'],source['operands_requiring_adjustment_when_resizing'])
    inventory,_,_=scoped_inventory();cleancommands,cleantexts=inventory(arm,japanese);oldcommands,oldtexts=inventory(arm,old);commands,texts=inventory(arm,target)
    require(cleancommands==prior['all_source_commands']==source['all_original_source_commands'] and oldcommands==prior['all_current_commands']==group['all_current_commands'] and commands==group['all_target_commands'],'independently parsed source/current/final command inventories')
    require(len(cleancommands)==len(oldcommands)==len(commands)==len(group['command_map'])==20 and len(cleantexts)==len(oldtexts)==len(texts)==5,'all20 commands and5 speech identities')
    for a,b,c,m in zip(cleancommands,oldcommands,commands,group['command_map'],strict=True):
        require(a['word']==b['word']==c['word']==m['word'] and b['offset']==m['old_offset'] and c['offset']==m['new_offset'],'complete command correspondence')
        if c['word']==0x4000:require(a['whole_command_hex'][:12]==b['whole_command_hex'][:12]==c['whole_command_hex'][:12],'every six-byte speaker/layout preamble')
        elif c['word'] not in [0x100,0x200,0x300,0x400]:require(a['whole_command_hex']==b['whole_command_hex']==c['whole_command_hex'],'all unowned effects/resources/fullterminal')
    require(commands[-1]['word']==0 and commands[-1]['native_extent']==4 and commands[-1]['offset']+4==group['target_logical_end'],'complete terminal before separate alignment tail')
    require(len(group['relative_fixups'])==8 and sum(len(r['cases']) for r in group['relocated_skip_cases'])==40,'all eight relative sites/forty cases andno menu')
    refs={r['id']:r for r in group['text_records']};rows=doc['records']
    require(len(refs)==len(rows)==len({r['id'] for r in rows})==5,'five disjoint canonical speech identities')
    for row in rows:
        ref=refs[row['id']];sr,cr,fr=row['source_reference'],row['current_reference'],row['final_reference']
        raw=bytes.fromhex(row['source_hex']);before=bytes.fromhex(row['current_hex']);value=bytes.fromhex(ref['target_hex'])
        for block,reference_,expected in [(japanese,sr,raw),(old,cr,before),(target,fr,value)]:
            at=reference_['offset'];require(reference_['block']==51 and reference_['bytes']==len(expected) and block[at:at+len(expected)+1]==expected+b'\0' and block[:at].count(b'\0')==reference_['record_index'],'complete source/current/final reference:'+row['id'])
        expected=dict(file_path=PATH,block=51,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=sha(target))
        require(fr==expected and row['final_hex']==row['stored_hex']==ref['target_hex'],'exact reviewed final reference/body/parity:'+row['id'])
    blocks=list(current);blocks[51]=target;target_archive=IlnkContainer(blocks).to_bytes();final=IlnkContainer.parse(target_archive).blocks
    require(sha(target_archive)==mapping['target_archive_sha256'] and target_archive==reference.read_file(PATH),'independent entire archive equals reviewed reference')
    require([i for i,(a,b) in enumerate(zip(current,final,strict=True)) if a!=b]==[51],'all324 other blocks unchanged')
    inverse=list(final);inverse[51]=old;require(IlnkContainer(inverse).to_bytes()==archive,'complete archive inverse')
    planned=deepcopy(parent);planned.replace_file(PATH,target_archive)
    require(bytes(planned.rom.save())==bytes(reference.rom.save()),'independent whole reference image equality')
    require([p for _,p,v in parent.iter_files() if planned.read_file(p)!=v]==[PATH] and all(planned.read_file(p)==v for p,v in parent.iter_components()),'every unowned file/component unchanged')
    restored=deepcopy(planned);restored.replace_file(PATH,archive);require(bytes(restored.rom.save())==bytes(parent.rom.save()),'whole in-memory predecessor inverse including canonical-source lifecycle')
    return dict(target_block=target,target_archive=target_archive,groups=[{**group,'target_block':target}],summary=dict(editorial_references=5,speeches=5,typed_choices=0,commands=20,relative_sites=8,query_sites=2,unowned_blocks=324,complete_clean_current_block_inverses=True,complete_archive_andwhole_inmemory_ROM_inverse=True,whole_reference_ROM_equal=True,new_credit=0))
