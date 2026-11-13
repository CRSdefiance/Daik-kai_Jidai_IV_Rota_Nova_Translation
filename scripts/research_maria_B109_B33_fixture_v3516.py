"""Relocate source-owned B109 objects; isolate its content in the New Game B33 slot."""
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.census_native_storylines_v1995 import complete_walk
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_B109_B33_fixture_v3516')
PARENT=Path('out/all_routes_combined_v3487_candidate.nds')
DOC=Path('translations/maria_B109_editorial_manuscript_v8.json')
FONT=Path('work/analysis/maria_B109_fonts_v3515/current_macro_QA_and_progressive_font_proof.json')
CONTROL=Path('work/analysis/maria_B109_controls_v3502/source_restored_UI_prefix_pause_C200_and34_commands_contract.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,font,control=map(read,[DOC,FONT,CONTROL])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']==control['candidate_sha256']
    assert font['manuscript_sha256']==sha(DOC.read_bytes())
    image=NdsImage.open(PARENT);clean=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks
    old=blocks[109];source=Path(control['control_restored_draft']).read_bytes()
    assert sha(source)==control['control_restored_draft_sha256'] and old[:8]==source[:8]
    assert old[:8]+bytes.fromhex(control['source_prefix_hex'])+old[18:]==source
    assert source[8:18]==IlnkContainer.parse(clean.read_file('/data/SC3.DK4')).blocks[109][8:18]
    commands=control['restored_native_walk']['commands'];by_at={c['offset']:c for c in commands}
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)
    raster.__kwdefaults__=original_raster.__kwdefaults__
    fonts={r['id']:r for r in font['cases']};patches=[];texts=[]
    for r in doc['records']:
        at=r['current_reference']['header_offset'];c=by_at[at];raw=bytes.fromhex(r['current_hex']);encoded=bytes.fromhex(r['compiled_hex'])
        assert c['word']==0x4000 and source[at:at+6].hex()==r['source_complete_preamble_hex']
        assert source[at+5:at+5+len(raw)]==raw and source[at+5+len(raw)]==0 and encoded[0]==raw[0]==r['source_selector']
        added=len(encoded[1:])%2!=len(raw[1:])%2;stored=encoded+(b' ' if added else b'')
        target=source[at:at+5]+stored+b'\0';target+=b'\0'*(-len(target)%2)
        pixels,glyphs,fontdata=raster(arm,stored[1:]);assert pixels==expected_pixels(arm,fontdata,glyphs) and sha(pixels)==fonts[r['id']]['whole_native_plane_sha256']
        assert [e['code'] for e in glyphs if e['code']!=32]==[c for c in stored[1:] if c not in (32,10)]
        patches.append(dict(start=at,end=at+c['native_extent'],old=source[at:at+c['native_extent']],new=target))
        texts.append(dict(id=r['id'],old_command_offset=at,old_native_extent=c['native_extent'],source_complete_preamble_hex=r['source_complete_preamble_hex'],stored_text_hex=stored.hex(),parity_space_added=added,final_native_plane_sha256=sha(pixels)))
    patches.sort(key=lambda p:p['start']);end=8+struct.unpack_from('<H',source,4)[0]
    assert len(patches)==26 and source[:4]==b'CS\1\1' and not any(source[end:])
    def mapped(offset):
        delta=0
        for p in patches:
            assert not p['start']<offset<p['end']
            if offset>=p['end']:delta+=len(p['new'])-len(p['old'])
        return offset+delta
    pieces=[];last=0
    for p in patches:pieces.extend([source[last:p['start']],p['new']]);last=p['end']
    pieces.append(source[last:end]);logical=bytearray(b''.join(pieces));assert len(logical)==mapped(end)<0x2400
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+b'\0'*(-len(logical)%4)
    walked=complete_walk(arm,target);assert not walked['errors'] and len(walked['commands'])==34
    new_by_at={c['offset']:c for c in walked['commands']};mapped_commands=[]
    for c in commands:
        at=c['offset'];n=new_by_at[mapped(at)];assert c['word']==n['word'] and n['native_extent']==mapped(at+c['native_extent'])-mapped(at)
        assert not c['ancestor_0100_offsets'] and not n['ancestor_0100_offsets']
        if c['word']==0x4000:assert source[at:at+6]==target[mapped(at):mapped(at)+6]
        else:assert c['whole_command_hex']==n['whole_command_hex']
        mapped_commands.append(dict(word=c['word'],old_offset=at,new_offset=mapped(at),old_extent=c['native_extent'],new_extent=n['native_extent']))
    for r in texts:r.update(new_command_offset=mapped(r['old_command_offset']),new_text_offset=mapped(r['old_command_offset'])+5)
    restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['new'])]=p['old']
    restored[8:18]=old[8:18]
    assert bytes(restored)==old[:end]
    ROOT.mkdir(parents=True);targetpath=ROOT/'SC3_B109_reviewed_relocated_DRAFT_ONLY.bin';targetpath.write_bytes(target)
    fixtures=[]
    for label,body in [('clean_Japanese',IlnkContainer.parse(clean.read_file('/data/SC3.DK4')).blocks[109]),('reviewed_English',target)]:
        im=NdsImage.open(PARENT);container=IlnkContainer.parse(im.read_file('/data/SC3.DK4'));container.blocks[33]=body
        im.replace_file('/data/SC3.DK4',container.to_bytes());path=ROOT/('Maria_B109_content_in_B33_'+label+'_RESEARCH_ONLY.nds');im.save(path);result=NdsImage.open(path)
        assert [p for _,p,v in image.iter_files() if result.read_file(p)!=v]==['/data/SC3.DK4']
        assert all(result.read_file(p)==v for p,v in image.iter_components())
        other=IlnkContainer.parse(result.read_file('/data/SC3.DK4')).blocks
        assert len(other)==303 and [n for n,(a,b) in enumerate(zip(blocks,other,strict=True)) if a!=b]==[33] and other[109]==old
        fixtures.append(dict(case=label,research_ROM=str(path),research_ROM_sha256=sha(path.read_bytes()),slot=33,body_from_block=109,body_sha256=sha(body),body_bytes=len(body),only_SC3_B33_changed=True,all302_other_SC3_blocks_every_other_file_component_exact=True))
    save(ROOT/'B109_source_owned_relocation_and_B33_entry_fixture.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),old_block_bytes=len(old),target_block_bytes=len(target),target_block=str(targetpath),target_block_sha256=sha(target),source_owned_prefix_span=dict(offset=8,bytes=10,before=old[8:18].hex(),after=target[8:18].hex(),five_physically_changed_byte_offsets=[13,14,15,16,17]),text_records=texts,mapped_native_commands=mapped_commands,all34_commands26_speech_preambles_and8_source_non_speech_commands_preserved=True,CS0101_header_preserved=True,all26_final_native_planes_equal_viewed_previews=True,exact_inverse_recovers_predecessor_bad_control_bytes_and_all_old_speech_bytes=True,relative_sites=[],fixtures=fixtures,fixture_scope='B109 content substituted into B33 New Game loader entry for initialized Maria3 UI; not selected source event109 or earned progression.',not_registered_or_user_handoff=True,gameplay_and_stored_target_macro_cases_pending=True,no_ledger_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(speeches=26,commands=34,bytes_before=len(old),bytes_after=len(target),research_fixtures=2,credit=0))
