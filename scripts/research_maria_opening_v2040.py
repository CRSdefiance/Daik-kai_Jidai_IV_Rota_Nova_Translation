"""CS0101 B33:38 complete final planes,85 typed commands and exact inverse."""
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.census_native_storylines_v1995 import complete_walk
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_relocation_v2040')
PARENT=Path('out/all_routes_combined_v2030_candidate.nds')
ROM=ROOT/'maria_opening_V2030_derived_RESEARCH_ONLY.nds'
SOURCE=Path('work/analysis/maria_opening_source_v2034/all38_clean_current_Hangzhou_opening_source.json')
DOC=Path('translations/maria_opening_contextual_editorial_manuscript_v1.json')
FONT=Path('work/analysis/maria_opening_fonts_v2037c/all38_progressive_native_macros_and_complete_font_planes.json')

if __name__=='__main__':
    assert not ROOT.exists()
    packet,doc,font=map(read,(SOURCE,DOC,FONT));assert font['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(font['cases'])==38 and not font['failures']and font['native_macro_calls']==308
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']
    image=NdsImage.open(PARENT);arm=image.read_file('/__arm9__.bin');old_file=image.read_file('/data/SC3.DK4')
    assert sha(old_file)==packet['current_SC3_sha256'];container=IlnkContainer.parse(old_file);source=container.blocks[33]
    commands=packet['native_commands']['current']['commands'];clean_commands=packet['native_commands']['clean']['commands']
    assert len(commands)==85 and [(r['word'],r['offset'],r['native_extent'],r['ancestor_0100_offsets'])for r in commands]==[(r['word'],r['offset'],r['native_extent'],r['ancestor_0100_offsets'])for r in clean_commands]
    assert not any(r['word']in(0x100,0x200,0x300,0x400)for r in commands)
    by_at={r['offset']:r for r in commands};fonts={r['id']:r for r in font['cases']};patches=[];texts=[]
    for row in doc['records']:
        proof=fonts[row['id']];at=row['current_reference']['header_offset'];command=by_at[at];length=command['native_extent']
        assert command['word']==0x4000 and source[at:at+6].hex()==row['source_complete_preamble_hex']
        offset=row['current_reference']['offset'];old=bytes.fromhex(row['current_text_hex'])
        assert source[offset:offset+len(old)]==old and source[offset+len(old)]==0
        encoded=bytes.fromhex(proof['encoded_text_excluding_speaker_hex']);added=len(encoded)%2!=len(old[1:])%2
        body=encoded+(b' 'if added else b'');target=source[at:at+6]+body+b'\0';target+=b'\0'*(-len(target)%2)
        expanded=bytes.fromhex(proof['native_expanded_hex'])+(b' 'if added else b'');pixels,glyphs,fontdata=raster(arm,expanded)
        assert pixels==expected_pixels(arm,fontdata,glyphs)and sha(pixels)==proof['native_font_plane_sha256']
        assert[e['code']for e in glyphs if e['code']!=32]==[c for c in expanded if c not in(32,10)]
        patches.append(dict(start=at,end=at+length,old=source[at:at+length],new=target))
        texts.append(dict(id=row['id'],old_command_offset=at,old_native_extent=length,source_preamble_hex=source[at:at+6].hex(),
            source_record_index=row['source_record_index'],current_source_record_index=row['record_index'],
            target_hex=target.hex(),target_text_excluding_speaker_hex=body.hex(),parity_space_added=added,
            final_parity_native_plane_exact=True,native_plane_sha256=sha(pixels)))
    patches.sort(key=lambda p:p['start']);end=8+struct.unpack_from('<H',source,4)[0]
    assert source[:4]==b'CS\1\1'and not any(source[end:])
    def mapped(offset):
        delta=0
        for p in patches:
            assert not p['start']<offset<p['end']
            if offset>=p['end']:delta+=len(p['new'])-len(p['old'])
        return offset+delta
    pieces=[];last=0
    for p in patches:pieces.extend((source[last:p['start']],p['new']));last=p['end']
    pieces.append(source[last:end]);logical=bytearray(b''.join(pieces));assert len(logical)==mapped(end)<0x2400
    struct.pack_into('<H',logical,4,len(logical)-8);logical_end=len(logical);target=bytes(logical)+b'\0'*(-len(logical)%4)
    walked=complete_walk(arm,target);assert not walked['errors']and len(walked['commands'])==85
    assert target[:4]==source[:4];new_by_at={r['offset']:r for r in walked['commands']};mapped_commands=[]
    for command in commands:
        at=command['offset'];new_at=mapped(at);new=new_by_at[new_at]
        assert new['word']==command['word']and new['native_extent']==mapped(at+command['native_extent'])-new_at
        assert not command['ancestor_0100_offsets']and not new['ancestor_0100_offsets']
        if command['word']==0x4000:assert source[at:at+6]==target[new_at:new_at+6]
        else:assert command['whole_command_hex']==new['whole_command_hex']
        mapped_commands.append(dict(word=command['word'],old_offset=at,new_offset=new_at,old_native_extent=command['native_extent'],
            new_native_extent=new['native_extent'],source_0100_ancestors=[],target_0100_ancestors=[]))
    for t in texts:
        t['new_command_offset']=mapped(t['old_command_offset']);t['new_offset']=t['new_command_offset']+5;t['new_record_index']=target[:t['new_offset']].count(b'\0')
    restored=bytearray(target[:logical_end]);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['new'])]=p['old']
    assert bytes(restored)==source[:end]
    ROOT.mkdir(parents=True);container.blocks[33]=target;image.replace_file('/data/SC3.DK4',container.to_bytes());image.save(ROM)
    parent,result=map(NdsImage.open,(PARENT,ROM));assert[p for _,p,v in parent.iter_files()if result.read_file(p)!=v]==['/data/SC3.DK4']
    assert all(result.read_file(p)==v for p,v in parent.iter_components())
    a,b=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks for im in(parent,result)]
    assert len(a)==len(b)==303 and[n for n,(x,y)in enumerate(zip(a,b,strict=True))if x!=y]==[33]
    save(ROOT/'complete_B33_CS0101_typed_relocation_research.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),ARM9_sha256=sha(arm),source_SC3_sha256=sha(old_file),
        target_SC3_sha256=sha(result.read_file('/data/SC3.DK4')),block=33,source_block_sha256=sha(source),target_block_sha256=sha(target),
        old_bytes=len(source),new_bytes=len(target),target_hex=target.hex(),text_records=texts,mapped_native_commands=mapped_commands,
        relative_skip_fixups=[],all85_typed_commands_and38_final_native_planes_exact=True,
        CS0101_header_and_all47_non_speech_commands_exact=True,exact_inverse_restores_current_block=True,
        all302_other_blocks_every_other_file_and_component_exact=True,loader_external_entry_actual_revised_and_registration_pending=True,
        not_a_playable_user_handoff=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(texts=38,commands=85,relative_sites=0,old_bytes=len(source),new_bytes=len(target),research_only=True))
