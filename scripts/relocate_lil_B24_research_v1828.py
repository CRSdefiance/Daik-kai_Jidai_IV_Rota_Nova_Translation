"""Parity-preserving B24 resizing research;external/actual approval still open."""
import struct
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_relocation_v1828')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
DOC=Path('translations/lil_trade_routes_officers_editorial_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    source=container.blocks[24];doc=read(DOC);fonts=read(doc['native_font_proof']);profile=get_dialogue_profile('lil-opening-editorial-native-v1')
    assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256']and not doc['formatting_review_pending']
    assert read(doc['visual_review'])['complete_first_last_letters_including_Istanbul_andFI_Lil']
    by_id={r['id']:r for r in fonts['cases']};patches=[];texts=[]
    for row in doc['records']:
        old=bytes.fromhex(row['current_text_hex']);at=row['current_reference']['offset'];assert source[at:at+len(old)]==old
        encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),profile).encoded
        assert encoded.hex()==by_id[row['id']]['encoded_hex']
        pad=len(encoded)%2!=len(old)%2;value=encoded+(b' 'if pad else b'')
        assert value[0]==old[0]and b'\0'not in value and len(value)%2==len(old)%2
        pixels,events,font=raster(arm,value[1:].replace(b'FI',b'Lil'))
        assert sha(pixels)==by_id[row['id']]['native_font_plane_sha256']
        patches.append({'start':at,'end':at+len(old),'value':value,'old':old,'id':row['id']})
        texts.append({'id':row['id'],'source_record_index':row['record_index'],'old_offset':at,'old_bytes':len(old),
            'new_bytes':len(value),'parity_space_added':pad,'encoded_hex':value.hex(),
            'complete_font_plane_equal_approved_native_even_with_parity_space':True})
    patches.sort(key=lambda p:p['start']);assert all(a['end']<=b['start']for a,b in zip(patches,patches[1:]))
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            if p['start']<offset<p['end']:raise ValueError('Unclassified interior target:'+str(offset))
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    end=8+struct.unpack_from('<H',source,4)[0];parts=[];last=0
    for p in patches:parts.extend((source[last:p['start']],p['value']));last=p['end']
    parts.append(source[last:end]);logical=bytearray(b''.join(parts));assert len(logical)==mapped(end)
    struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4);assert len(target)<=0x2400
    old_commands,old_speech=inventory(arm,source);new_commands,new_speech=inventory(arm,target)
    assert len(old_commands)==len(new_commands)==17 and len(old_speech)==len(new_speech)==13
    new_by={r['offset']:r for r in new_commands};commands=[]
    for old in old_commands:
        now=new_by[mapped(old['offset'])];assert now['word']==old['word']and now['ancestor_0100_offsets']==[]
        assert now['native_extent']==mapped(old['offset']+old['native_extent'])-mapped(old['offset'])
        if old['word']==0x4000:
            assert source[old['offset']:old['offset']+6]==target[now['offset']:now['offset']+6]
        else:assert source[old['offset']:old['offset']+old['native_extent']]==target[now['offset']:now['offset']+now['native_extent']]
        commands.append({'word':old['word'],'old_offset':old['offset'],'new_offset':now['offset'],
            'old_extent':old['native_extent'],'new_extent':now['native_extent'],
            'complete_nonspeech_or_six_byte_speech_preamble_preserved':True})
    assert [r['word']for r in commands if r['word']!=0x4000]==[0x61FF,0xA000,0xC200,0]
    for row,p in zip(texts,patches,strict=True):
        row['new_offset']=mapped(p['start']);row['new_record_index']=target[:row['new_offset']].count(b'\0')
        assert target[row['new_offset']:row['new_offset']+row['new_bytes']].hex()==row['encoded_hex']
    inverse=bytearray(target[:len(logical)])
    for p in reversed(patches):inverse[mapped(p['start']):mapped(p['end'])]=p['old']
    struct.pack_into('<H',inverse,4,end-8)
    assert bytes(inverse)==source[:end]
    path=ROOT/'block24_RESEARCH_ONLY.bin';path.write_bytes(target)
    save(ROOT/'parity_and17_native_command_research.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'ARM9_sha256':sha(arm),
        'block':24,'old_block_sha256':sha(source),'target_block_sha256':sha(target),
        'old_bytes':len(source),'target_bytes':len(target),'growth_bytes':len(target)-len(source),
        'old_logical_end':end,'new_logical_end':len(logical),'texts':texts,'all17_commands':commands,
        'inverse_reconstruction_of_every_original_logical_byte_exact':True,
        'all13_original_six_byte_preambles_and_string_parity_preserved':True,
        'all4_nonspeech_commands_exact_at_mapped_positions':True,
        'all_native_parser_extents_and_original_speech_headers_match_independent_inventory':True,
        'no_0100_0200_0300_or2100_commands_in_this_block':True,
        'external_reference_map_complete':False,'actual_B24_control_flow_and_all13_displays_pending':True,
        'research_only_no_ROM_or_registered_release_created':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'old_bytes':len(source),'research_bytes':len(target),'growth':len(target)-len(source),'native_commands':17,
        'all13_parity_and_native_font_planes_preserved':True,'external_andactual_gates_open':True},flush=True)
