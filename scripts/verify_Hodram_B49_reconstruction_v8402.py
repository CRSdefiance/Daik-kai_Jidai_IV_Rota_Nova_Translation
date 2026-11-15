"""Independently rebuild B49 by disjoint command atoms, not sparse edit spans."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_independent_v8402')
MAP=Path('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')
DOC=Path('translations/hodram_B49_editorial_manuscript_v2.json')
CURRENT=Path('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')

if __name__=='__main__':
    assert not ROOT.exists();mapping,doc,packet=map(read,[MAP,DOC,CURRENT])
    assert mapping['manuscript_sha256']==sha(DOC.read_bytes())
    image=NdsImage.open(doc['current_ROM']);archive=image.read_file('/data/SC1.DK4')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==mapping['candidate_sha256']
    container=IlnkContainer.parse(archive);old=container.blocks[49];clean=bytes.fromhex(packet['groups'][0]['clean_block_hex'])
    inventory,_,_=scoped_inventory();commands,speeches=inventory(image.read_file('/__arm9__.bin'),old)
    assert len(commands)==36 and len(speeches)==14
    end=8+struct.unpack_from('<H',old,4)[0];starts=[c['offset'] for c in commands]+[end]
    assert starts[0]==8 and starts==sorted(set(starts))
    speech_by_header={r['current_reference']['header_offset']:r for r in doc['records']}
    fragments=[];relocation={};cursor=8;atoms=[]
    for index,c in enumerate(commands):
        at,stop=c['offset'],starts[index+1];original=old[at:stop];word=c['word'];value=original
        assert stop>at and original[:2]==struct.pack('<H',word)
        if word==0x4000:
            row=speech_by_header[at];body=bytes.fromhex(row['current_hex']);compiled=bytes.fromhex(row['compiled_hex'])
            assert original[:5]+body+original[5+len(body):]==original and original[5:5+len(body)]==body
            suffix=original[5+len(body):];assert suffix in [b'\0',b'\0\0']
            parity=len(compiled)%2!=len(body)%2;value=original[:5]+compiled+(b' ' if parity else b'')+suffix
            assert original[:6].hex()==row['source_complete_preamble_hex']==value[:6].hex()
        elif word==0x2100:
            options=[r['english'].encode('ascii') for r in doc['typed_choice_records']]
            assert len(options)==2 and all(t and t==t.strip() and b'\0' not in t for t in options)
            chunks=[t+b'\0'+bytes(-(len(t)+1)%2) for t in options]
            value=struct.pack('<3H',0x2100,0,len(chunks[0]))+b''.join(chunks)
            assert len(original)==26 and len(value)==22
        elif word==0x100:assert len(original)==4 and c['native_extent']>=4
        else:assert len(original)==c['native_extent']
        assert len(value)%2==len(original)%2==0
        relocation[at]=cursor;atoms.append(dict(word=word,source_offset=at,target_offset=cursor,source_atom_bytes=len(original),target_atom_bytes=len(value),original_hex=original.hex(),target_hex=value.hex()))
        fragments.append(value);cursor+=len(value)
    relocation[end]=cursor;result=bytearray(old[:8]+b''.join(fragments));assert len(result)==cursor
    fixups=[]
    for c in commands:
        if c['word'] not in [0x100,0x200,0x300,0x400]:continue
        at=c['offset'];destination=at+4+struct.unpack_from('<H',old,at+2)[0]
        assert destination in relocation and at+4 in relocation
        start,finish=relocation[at],relocation[destination];span=finish-start-4
        assert span%2==0 and 0<=span<=0xffff
        struct.pack_into('<H',result,start+2,span);fixups.append(dict(old_offset=at,new_offset=start,new_span=span))
    struct.pack_into('<H',result,4,len(result)-8);logical=len(result);result=bytes(result)+bytes(-len(result)%4)
    group=mapping['groups'][0];assert result==Path(group['target_block']).read_bytes() and sha(result)==group['target_block_sha256']
    assert logical==group['target_logical_end'] and len(fixups)==8
    assert all(relocation[c['old_offset']]==c['new_offset'] for c in group['command_map'])
    for base,version in [(old,'predecessor'),(clean,'clean-Japanese')]:
        reverse=bytearray(result[:logical]);reverse[:8]=base[:8]
        for fix in fixups:reverse[fix['new_offset']+2:fix['new_offset']+4]=base[fix['old_offset']+2:fix['old_offset']+4]
        for atom in reversed(atoms):
            a,z=atom['source_offset'],atom['target_offset'];n=atom['source_atom_bytes'];m=atom['target_atom_bytes']
            if atom['word'] in [0x4000,0x2100]:reverse[z:z+m]=base[a:a+n]
        baseend=8+struct.unpack_from('<H',base,4)[0]
        assert bytes(reverse)+base[baseend:]==base,version+' complete inverse'
    blocks=list(container.blocks);blocks[49]=result;rebuilt=IlnkContainer(blocks).to_bytes()
    assert rebuilt==Path(mapping['target_archive']).read_bytes() and sha(rebuilt)==mapping['target_archive_sha256']
    restored=IlnkContainer.parse(rebuilt);restored.blocks[49]=old;assert restored.to_bytes()==archive
    ROOT.mkdir(parents=True);save(ROOT/'independent_reconstruction.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),method='36 disjoint command atoms;0100 contributes only its four-byte header while nested commands contribute their own atoms',atoms=atoms,independently_computed_command_offsets=relocation,independently_computed_relative_fixups=fixups,whole_target_block_andarchive_byte_equal_to_sparse_rebuild=True,complete_clean_andpredecessor_block_inverse_exact=True,whole_predecessor_archive_inverse_exact=True,other324_blocks_exact=True,target_block_sha256=sha(result),target_archive_sha256=sha(rebuilt),no_ROM_write_orcompletion_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [MAP,DOC,CURRENT,Path(__file__)]}))
    print('Independent36-command-atom reconstruction equals sparse block/archive;8 offsets recomputed;clean/current block andwhole parent archive recover exactly.No ROM/credit.')
