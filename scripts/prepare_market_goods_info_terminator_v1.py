"""Prepare a guarded data-only correction without writing a ROM or registering a release."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile,loadOverlayTable
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.market_goods_info_terminator_v1 import transform,NEW_FORMAT,PAYLOAD
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/market_goods_info_terminator_20261109_v1')

def main():
    out=ROOT/'prepared_v1';assert not out.exists()
    diagnosis=load(ROOT/'diagnosis.json');release_path=Path('work/maria301_release_v1/registered_release_verification.json')
    release=load(release_path);rompath=Path(release['candidate'])
    assert sha(rompath.read_bytes())==release['candidate_sha256']==diagnosis['build_bindings'][1]['ROM_sha256']
    image=NdsImage.open(rompath);source=image.read_file('/__arm9__.bin');target,proof=transform(source)
    start,end=NEW_FORMAT,NEW_FORMAT+len(PAYLOAD)
    overlays=loadOverlayTable(image.rom.arm9OverlayTable,lambda oid,fid:image.rom.files[fid])
    assert all(o.ramAddress+len(o.data)+o.bssSize<=start or end<=o.ramAddress for o in overlays.values())
    units=[(f'section{i}',s.ramAddress,bytes(s.data)) for i,s in enumerate(MainCodeFile(source,0x02000000).sections)]
    units += [(f'overlay{i}',o.ramAddress,bytes(o.data)) for i,o in overlays.items()]
    aliases=[]
    for name,base,raw in units:
        for at in range(0,len(raw)-3,4):
            value=struct.unpack_from('<I',raw,at)[0]
            if start<=value<end:aliases.append(dict(owner=name,address=base+at,value=value))
    assert not aliases
    out.mkdir();(out/'source_arm9.bin').write_bytes(source);(out/'target_arm9.bin').write_bytes(target)
    save(out/'preparation.json',dict(**proof,parent_ROM=str(rompath),parent_ROM_sha256=release['candidate_sha256'],
        source_capture_instruction_address=0x01FFC6AC,
        new_declared_data_span=[start,end],all_existing_sections_andoverlays_BSS_disjoint=True,
        no_preexisting_aligned_pointer_literals_into_new_span=True,
        static_scan_does_not_claim_all_computed_indirect_users_orhardware=True,
        source_file='source_arm9.bin',target_file='target_arm9.bin',
        native_printf_rendering_andcandidate_startup_pending=True,no_ROM_written=True,no_registered_release_orpromotion=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [ROOT/'diagnosis.json',release_path,Path('dk4tool/patch/market_goods_info_terminator_v1.py'),Path(__file__)]}))
    print('Prepareddeclared16-byte format allocation/two pointers;all existing code andwhole inverse exact. Native/gameplay/registered checks pending.')

if __name__=='__main__':main()
