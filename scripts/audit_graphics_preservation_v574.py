"""Current complete PXL/FLS metadata/palette and embedded-extent comparison."""
import argparse
import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rom',type=Path,default=Path('out/all_routes_combined_v573_candidate.nds'))
    parser.add_argument('--out',type=Path,default=Path('work/analysis/plaque_current_v574/current_preservation_proof.json'))
    args=parser.parse_args()
    a,b=NdsImage.open('work/clean.nds'),NdsImage.open(args.rom);entries=[]
    for _,path,source in a.iter_files():
        saved=b.read_file(path)
        if path.lower().endswith('.pxl'):
            aa,bb=struct.unpack_from('<5I',source),struct.unpack_from('<5I',saved)
            assert aa==bb,path
            bits=aa[0]&255;assert bits in (4,8,16)
            if bits!=16:assert source[aa[3]:aa[4]]==saved[bb[3]:bb[4]],path
            assert len(source)-aa[4]==len(saved)-bb[4],path
            entries.append({'path':path,'kind':'PXL','depth':bits,'header_palette_when_indexed_and_extent_exact':True,
                            'changed_from_clean':source!=saved})
        elif path.lower().endswith('.fls'):
            aa,bb=FlsArchive(source),FlsArchive(saved)
            assert aa.count==bb.count and aa.compressed_storage==bb.compressed_storage,path
            for i in range(aa.count):
                x,y=aa.texture(i),bb.texture(i)
                assert (x.flags,x.width,x.height,x.palette,len(x.indices))==(y.flags,y.width,y.height,y.palette,len(y.indices)),(path,i)
                entries.append({'path':path,'kind':'FLS','texture':i,'original_flags_palette_dimensions_extent_exact':True,
                                'changed_from_clean':x.indices!=y.indices})
    assert len(entries)==921
    census=json.loads(Path('work/analysis/embedded_storage_census_v192.json').read_text())
    archives=[]
    for path in sorted({r['path'] for r in census['blocks']}):
        aa,bb=IlnkContainer.parse(a.read_file(path)),IlnkContainer.parse(b.read_file(path))
        assert len(aa.blocks)==len(bb.blocks)
        for i,(x,y) in enumerate(zip(aa.blocks,bb.blocks,strict=True)):
            assert len(x)==len(y),(path,i,len(x),len(y))
            archives.append({'path':path,'block':i,'bytes':len(x),'extent_exact':True,'changed_from_clean':x!=y})
    assert len(archives)==57
    proof={'candidate_sha256':sha(b.source.read_bytes()),'source_ROM_sha256':sha(a.source.read_bytes()),'entries':entries,
           'embedded_block_extents':archives,'current921_format_palette_extent_checks':True,
           'all57_embedded_block_extents_exact':True,'pixel_art_fidelity_translation_or_native_usage_not_inferred':True,
           'production_ROM_modified':False,'full_goal_complete':False}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(proof,indent=2)+'\n')
    print('All 660 PXL headers/indexed palette banks/extents,261 FLS textures,57 embedded block extents pass.')


if __name__=='__main__':main()
