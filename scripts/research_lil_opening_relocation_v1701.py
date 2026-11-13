"""Research49 parity-preserving text expansions;external references remain open."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_wedding_command_v676 import walk
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_relocation_v1701')
ROM=Path('out/all_routes_combined_v1676_candidate.nds')


if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_opening_editorial_manuscript_v2.json')
    fonts=read(doc['native_font_proof']);cases={r['id']:r for r in fonts['cases']}
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');source=rom.read_file('/data/SC2.DK4')
    container=IlnkContainer.parse(source);block=container.blocks[22];parts=block.split(b'\0');before=list(parts)
    assert len(block)==8+struct.unpack_from('<H',block,4)[0]==3000
    rows=[]
    for row in doc['records']:
        n=row['record_index'];value=bytes.fromhex(row['compiled_hex']);old=parts[n]
        assert old.hex()==row['current_text_hex'] and value[:1]==old[:1]
        pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        assert b'\0' not in value and len(value)%2==len(old)%2
        old_at=sum(len(p)+1 for p in before[:n]);parts[n]=value
        rows.append({'id':row['id'],'record_index':n,'old_offset':old_at,'old_length':len(old),
            'new_length':len(value),'one_parity_space_added':pad,'target_hex':value.hex()})
        if pad:
            pixels,events,_=raster(arm,value[1:].replace(b'FI',b'Lil'))
            assert sha(pixels)==cases[row['id']]['native_font_plane_sha256']
            assert all(e['y']<=48 for e in events if e['code']!=32)
    target=bytearray(b'\0'.join(parts));struct.pack_into('<H',target,4,len(target)-8)
    target=bytes(target)+b'\0'*(-len(target)%4)
    original_walk,changed_walk=[walk(arm,b) for b in (block,target)]
    assert all(not w['error'] and w['stopped_offset']==w['logical_end'] for w in (original_walk,changed_walk))
    assert len(original_walk['rows'])==len(changed_walk['rows'])==90
    commands=[]
    for a,b in zip(original_walk['rows'],changed_walk['rows'],strict=True):
        assert a['word']==b['word'] and a['offset']%2==b['offset']%2
        if a['word']!=0x4000:
            assert a['native_extent']==b['native_extent'] and block[a['offset']:a['offset']+a['native_extent']]==target[b['offset']:b['offset']+b['native_extent']]
            assert a['result']==b['result']
        commands.append({'opcode':a['word'],'old_offset':a['offset'],'new_offset':b['offset'],
            'old_extent':a['native_extent'],'new_extent':b['native_extent'],'speech_payload_only_or_identical_non_speech_command':True})
    for row in rows:
        row['new_offset']=sum(len(p)+1 for p in parts[:row['record_index']])
        assert target[row['new_offset']-5:row['new_offset']]==b'\0\x40\xff\xff\0'
        assert target[row['new_offset']]==block[row['old_offset']]
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_context_v1697_1676/frame_006000_arm9_ram.bin')
    raw=snapshot.read_bytes();resident=[];at=0
    while (at:=raw.find(block,at))>=0:resident.append(0x02000000+at);at+=1
    assert len(resident)==1;address=resident[0];pointers=[]
    for at in range(0,len(raw)-3,4):
        value=struct.unpack_from('<I',raw,at)[0]
        if address<=value<address+len(block):
            pointers.append({'stored_at':0x02000000+at,'points_to':value,'block_offset':value-address,
                'unclassified_candidate_not_an_entry_point_claim':True})
    ROOT.mkdir(parents=True)
    (ROOT/'block22_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'parity_and_native_command_research.json',{'ROM':str(ROM),'ROM_sha256':sha(ROM.read_bytes()),
        'current_source_file_sha256':sha(source),'current_source_block_sha256':sha(block),'research_block_sha256':sha(target),
        'old_block_bytes':len(block),'research_block_bytes':len(target),'block_growth':len(target)-len(block),
        'all49_speaker_headers_and_message_parity_preserved':True,'all41_non_speech_commands_byte_exact_at_mapped_positions':True,
        'native_90_command_extents':commands,'mapped_texts':rows,
        'all_added_single_parity_spaces_repaint_complete_font_plane_identically':True,
        'current_actual_resident_block_address':address,'current_actual_snapshot':str(snapshot),'current_actual_snapshot_sha256':sha(raw),
        'raw_aligned_pointer_candidates':pointers,'native_walk_linear_extents_not_runtime_branch_reachability':True,
        'external_references_complete':False,'not_a_release_relocation_map':True,
        'remaining_reference_gate':'Classify original external script-entry and control-flow consumers;raw pointer/value scans and native linear walking alone do not authorize resizing. Then verify original initialization,next-command progression and actual entire revised scene.',
        'no_ROM_or_registry_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'49_texts_parity_preserved':True,'41_other_commands_exact':True,'old_bytes':len(block),'new_bytes':len(target),
        'external_reference_map_complete':False,'ROM_changed':False})
