"""Relocate32 exact B97 speech objects and prepare disclosed source/English B33 content fixtures."""
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.census_native_storylines_v1995 import complete_walk
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster
from scripts.lil_current_font_oracles_v4792 import expected_pixels,make_painter
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_fixture_v5014')
DOC=Path('translations/maria_B97_editorial_manuscript_v3.json')
FONT=Path('work/analysis/maria_B97_fonts_v5013b/all32_font_matrices_256_alignments_and_source72_page_projection.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,font=map(read,[DOC,FONT]);packet=read(doc['source_context']);parent=Path(doc['current_ROM'])
    assert sha(parent.read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256'] and font['manuscript_sha256']==sha(DOC.read_bytes())
    image=NdsImage.open(parent);clean=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');sc=image.read_file('/data/SC3.DK4')
    blocks=IlnkContainer.parse(sc).blocks;old=blocks[97];source=IlnkContainer.parse(clean.read_file('/data/SC3.DK4')).blocks[97]
    commands=packet['blocks'][0]['all_current_native_commands'];byat={c['offset']:c for c in commands};proofs={r['id']:r for r in font['cases']}
    assert len(old)==1904 and sha(old)==packet['blocks'][0]['current_block_sha256']
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    paint,calibration=make_painter(image);patches=[];texts=[]
    for r in doc['records']:
        at=r['current_reference']['header_offset'];c=byat[at];raw=bytes.fromhex(r['current_hex']);encoded=bytes.fromhex(r['compiled_hex'])
        assert c['word']==0x4000 and old[at:at+6].hex()==r['source_complete_preamble_hex']==source[at:at+6].hex()
        assert old[at+5:at+5+len(raw)+1]==raw+b'\0' and encoded[0]==raw[0]==r['source_selector']
        parity=len(encoded[1:])%2!=len(raw[1:])%2;stored=encoded+(b' ' if parity else b'')
        target=old[at:at+5]+stored+b'\0';target+=b'\0'*(-len(target)%2)
        effective=stored[1:].replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
        if r['kind']=='system-FE':
            out=paint(effective);pixels=out['physical'];glyphs=out['events'];assert sha(pixels)==proofs[r['id']]['physical_plane_sha256']
        else:
            height=96 if r['source_record_index']==72 else 64;pixels,glyphs,fontdata=raster(arm,effective,canvas_height=height)
            assert pixels==expected_pixels(arm,fontdata,glyphs,canvas_height=height) and sha(pixels)==proofs[r['id']]['font_matrix_sha256']
        assert [e['code'] for e in glyphs if e['code']!=32]==[c for c in effective if c not in [32,10]]
        patches.append(dict(start=at,end=at+c['native_extent'],old=old[at:at+c['native_extent']],new=target))
        texts.append(dict(id=r['id'],old_command_offset=at,old_native_extent=c['native_extent'],source_complete_preamble_hex=r['source_complete_preamble_hex'],stored_text_hex=stored.hex(),parity_space_added=parity,final_font_plane_sha256=sha(pixels),physical_page_count=2 if r['source_record_index']==72 else 1,actual_page_advance_still_pending=r['source_record_index']==72))
    patches.sort(key=lambda p:p['start']);end=8+struct.unpack_from('<H',old,4)[0];assert end==1902 and len(patches)==32 and old[:4]==b'CS\1\1' and old[end:]==bytes(2)
    def mapped(offset):
        delta=0
        for p in patches:
            assert not p['start']<offset<p['end']
            if offset>=p['end']:delta+=len(p['new'])-len(p['old'])
        return offset+delta
    pieces=[];last=0
    for p in patches:pieces.extend([old[last:p['start']],p['new']]);last=p['end']
    pieces.append(old[last:end]);logical=bytearray(b''.join(pieces));assert len(logical)==mapped(end)<0x2400
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    walked=complete_walk(arm,target);assert not walked['errors'] and len(walked['commands'])==40
    bynew={c['offset']:c for c in walked['commands']};mappedcommands=[]
    for c in commands:
        at=c['offset'];n=bynew[mapped(at)];assert c['word']==n['word'] and n['native_extent']==mapped(at+c['native_extent'])-mapped(at)
        assert not c['ancestor_0100_offsets'] and not n['ancestor_0100_offsets']
        if c['word']==0x4000:assert old[at:at+6]==target[mapped(at):mapped(at)+6]
        else:assert c['whole_command_hex']==n['whole_command_hex']
        mappedcommands.append(dict(word=c['word'],old_offset=at,new_offset=mapped(at),old_extent=c['native_extent'],new_extent=n['native_extent']))
    for r in texts:r.update(new_command_offset=mapped(r['old_command_offset']),new_text_offset=mapped(r['old_command_offset'])+5)
    restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,end-8)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['new'])]=p['old']
    assert bytes(restored)+old[end:]==old
    ROOT.mkdir(parents=True);targetpath=ROOT/'SC3_B97_reviewed_relocated_DRAFT_ONLY.bin';targetpath.write_bytes(target);fixtures=[]
    for label,body in [('clean_Japanese',source),('reviewed_English',target)]:
        im=NdsImage.open(parent);container=IlnkContainer.parse(sc);container.blocks[33]=body;im.replace_file('/data/SC3.DK4',container.to_bytes())
        path=ROOT/('Maria_B97_content_in_B33_'+label+'_RESEARCH_ONLY.nds');im.save(path);result=NdsImage.open(path)
        assert [p for _,p,v in image.iter_files() if result.read_file(p)!=v]==['/data/SC3.DK4'] and all(result.read_file(p)==v for p,v in image.iter_components())
        other=IlnkContainer.parse(result.read_file('/data/SC3.DK4')).blocks
        assert len(other)==303 and [n for n,(a,b) in enumerate(zip(blocks,other,strict=True)) if a!=b]==[33] and other[97]==old
        fixtures.append(dict(case=label,research_ROM=str(path),research_ROM_sha256=sha(path.read_bytes()),slot=33,body_from_block=97,body_sha256=sha(body),body_bytes=len(body),only_SC3_B33_changed=True,all302_other_SC3_blocks_every_other_file_component_exact=True))
    save(ROOT/'B97_reversible_relocation_and_B33_content_fixture.json',dict(parent=str(parent),parent_sha256=sha(parent.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),source_context=doc['source_context'],source_context_sha256=doc['source_context_sha256'],old_block_bytes=len(old),old_logical_end=end,target_block_bytes=len(target),target_logical_end=len(logical),target_block=str(targetpath),target_block_sha256=sha(target),text_records=texts,mapped_native_commands=mappedcommands,all40_source_commands32_complete_preambles_and8_nonspeech_leaves_preserved=True,no_inherited_B109_prefix_restoration_or_extra_B33_initializer_assumption=True,CS0101_and_complete_setup6000_4620_633E_two_A000_item4820_hide4700_and_end_preserved=True,all32_final_stored_font_matrices_equal_viewed_previews=True,source72_native_page_advance_requires_actual_test=True,exact_inverse_recovers_every_predecessor_B97_byte_and_tail=True,relative_sites=[],fixtures=fixtures,fixture_scope='Complete B97 source/reviewed content substituted into B33 New Game entry in V4987. Original source B97 setup/resource/effect/presentation commands remain intact. Not naturally selected event97,earned recruitment,earned tablet or full-route proof.',not_registered_or_user_handoff=True,no_ledger_credit=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(speeches=32,commands=40,before=len(old),after=len(target),logical=len(logical),research_fixtures=2,credit=0))
