"""Independently rebuild both blocks from command atoms, without sparse patches."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_independent_v8810')
MAP=Path('work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
CURRENT=Path('work/analysis/Hodram_B54_B60_current_v8799/current_effective.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,doc,packet=map(read,[MAP,DOC,CURRENT]);assert mapping['manuscript_sha256']==sha(DOC.read_bytes())
    image=NdsImage.open(doc['current_ROM']);archive=image.read_file('/data/SC1.DK4')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==mapping['candidate_sha256']
    container=IlnkContainer.parse(archive);assert len(container.blocks)==325
    inventory,unused_walker,unused_fn=scoped_inventory();blocks=list(container.blocks);groups=[]
    for p in packet['groups']:
        number=p['block'];old=container.blocks[number];clean=bytes.fromhex(p['clean_block_hex'])
        commands,speeches=inventory(image.read_file('/__arm9__.bin'),old);assert len(commands)==len(p['all_current_commands']) and len(speeches)==len(p['records'])
        end=8+struct.unpack_from('<H',old,4)[0];starts=[c['offset'] for c in commands]+[end]
        assert starts[0]==8 and starts==sorted(set(starts))
        speech_by_header={r['current_reference']['header_offset']:r for r in doc['records'] if r['block']==number}
        fragments=[];relocation={};cursor=8;atoms=[]
        for i,c in enumerate(commands):
            at,stop=c['offset'],starts[i+1];original=old[at:stop];word=c['word'];value=original
            assert stop>at and original[:2]==struct.pack('<H',word)
            if word==0x4000:
                row=speech_by_header[at];body=bytes.fromhex(row['current_hex']);compiled=bytes.fromhex(row['compiled_hex'])
                assert original[5:5+len(body)]==body
                suffix=original[5+len(body):];assert suffix in [b'\0',b'\0\0']
                parity=len(compiled)%2!=len(body)%2;value=original[:5]+compiled+(b' ' if parity else b'')+suffix
                assert original[:6].hex()==row['source_complete_preamble_hex']==value[:6].hex()
            elif word==0x100:assert len(original)==4 and c['native_extent']>=4
            else:assert len(original)==c['native_extent']
            assert len(value)%2==len(original)%2==0
            relocation[at]=cursor;atoms.append(dict(word=word,source_offset=at,target_offset=cursor,source_atom_bytes=len(original),target_atom_bytes=len(value),original_hex=original.hex(),target_hex=value.hex()))
            fragments.append(value);cursor+=len(value)
        relocation[end]=cursor;result=bytearray(old[:8]+b''.join(fragments));assert len(result)==cursor
        fixups=[]
        for c in commands:
            if c['word'] not in [0x100,0x200,0x300,0x400]:continue
            at=c['offset'];destination=at+4+struct.unpack_from('<H',old,at+2)[0];assert destination in relocation and at+4 in relocation
            start,finish=relocation[at],relocation[destination];span=finish-start-4;assert span%2==0 and 0<=span<=0xffff
            struct.pack_into('<H',result,start+2,span);fixups.append(dict(old_offset=at,new_offset=start,new_span=span))
        struct.pack_into('<H',result,4,len(result)-8);logical=len(result);result=bytes(result)+bytes(-len(result)%4)
        group=next(g for g in mapping['groups'] if g['block']==number)
        assert result==Path(group['target_block']).read_bytes() and sha(result)==group['target_block_sha256'] and logical==group['target_logical_end']
        assert len(fixups)==len(group['relative_fixups']) and all(relocation[c['old_offset']]==c['new_offset'] for c in group['command_map'])
        for base,version in [(old,'predecessor'),(clean,'clean-Japanese')]:
            reverse=bytearray(result[:logical]);reverse[:8]=base[:8]
            for fix in fixups:reverse[fix['new_offset']+2:fix['new_offset']+4]=base[fix['old_offset']+2:fix['old_offset']+4]
            for atom in reversed(atoms):
                if atom['word']!=0x4000:continue
                a,z=atom['source_offset'],atom['target_offset'];n,m=atom['source_atom_bytes'],atom['target_atom_bytes'];reverse[z:z+m]=base[a:a+n]
            baseend=8+struct.unpack_from('<H',base,4)[0];assert bytes(reverse)+base[baseend:]==base,version+' complete inverse'
        blocks[number]=result;groups.append(dict(block=number,atoms=atoms,independently_computed_command_offsets=relocation,independently_computed_relative_fixups=fixups,
            target_block_sha256=sha(result),complete_clean_andpredecessor_block_inverse_exact=True))
    rebuilt=IlnkContainer(blocks).to_bytes();assert rebuilt==Path(mapping['target_archive']).read_bytes() and sha(rebuilt)==mapping['target_archive_sha256']
    restored=IlnkContainer.parse(rebuilt)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,restored.blocks,strict=True)) if a!=b]==[p['block'] for p in packet['groups']]
    for i in [p['block'] for p in packet['groups']]:restored.blocks[i]=container.blocks[i]
    assert restored.to_bytes()==archive
    planned=deepcopy(image);planned.replace_file('/data/SC1.DK4',rebuilt);target_ROM_sha256=sha(bytes(planned.rom.save()))
    assert [p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==['/data/SC1.DK4'] and all(planned.read_file(p)==v for p,v in image.iter_components())
    planned.replace_file('/data/SC1.DK4',archive);assert bytes(planned.rom.save())==bytes(image.rom.save())
    ROOT.mkdir(parents=True);save(ROOT/'independent_reconstruction.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),
        method='152 disjoint command atoms across seven complete blocks;0100 contributes only its four-byte header while nested commands contribute their own atoms',
        groups=groups,whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild=True,complete_clean_andpredecessor_block_inverses_exact=True,
        whole_predecessor_archive_inverse_exact=True,other318_blocks_exact=True,all_other_ROM_files_components_andwhole_inmemory_ROM_inverse_exact=True,
        independently_reconstructed_complete_target_ROM_sha256=target_ROM_sha256,target_archive_sha256=sha(rebuilt),
        no_ROM_write_orcompletion_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [MAP,DOC,CURRENT,Path(__file__)]}))
    print('Independent152-command-atom reconstruction equals all seven sparse blocks/archive;24fixups recomputed;clean/current/wholearchive/wholeNDS inverses pass.No ROM/credit.',flush=True)
