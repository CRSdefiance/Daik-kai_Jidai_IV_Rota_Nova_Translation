"""Isolated black/white versions of the existing M28 English coverage masks."""
import json
import struct
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import compress_lz10, decompress_lz10
from scripts.build_integrated_release import rom_files

ROOT=Path('work/analysis/movie_fades_v575')
ROM=Path('out/all_routes_combined_v573_candidate.nds')
FILE='/FLS/M28.fls'
EDITED=[4,5,*range(27,47)]


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    parent=NdsImage.open(ROM);data=parent.read_file(FILE)
    clean=FlsArchive(NdsImage.open('work/clean.nds').read_file(FILE))
    original=FlsArchive(data)
    assert [i for i in range(original.count) if original.texture(i).indices!=clean.texture(i).indices]==EDITED
    manifest=json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    stack=json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    assert manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['profile']=='all-routes-unified-v573' and len(stack['accepted_layers'])==114
    assert len(manifest['batches'])==470
    fixtures=[]
    for kind,value in (('black',0),('white',0x7FFF)):
        archive=FlsArchive(data);owned=set()
        for i in EDITED:
            texture=archive.texture(i)
            texture.indices[:]=bytes(1 if n else 0 for n in texture.indices)
            start=archive.data_offset+archive.records[i][4]
            owned.update(range(start,start+archive.records[i][5]))
        result=bytearray(archive.to_bytes())
        for i in EDITED:
            record=archive.records[i]
            start=archive.data_offset+record[2];end=archive.data_offset+record[4]
            palette=bytearray(decompress_lz10(data[start:]))
            assert len(palette)==record[3]
            old=struct.unpack_from('<H',palette,2)[0]
            struct.pack_into('<H',palette,2,(old&0x8000)|value)
            compressed=compress_lz10(bytes(palette))
            assert len(compressed)<=end-start
            result[start:end]=compressed+bytes(end-start-len(compressed))
            owned.update(range(start,end))
        assert len(result)==len(data)
        assert all(a==b for n,(a,b) in enumerate(zip(data,result,strict=True)) if n not in owned)
        saved=FlsArchive(bytes(result));cases=[]
        assert saved.records==original.records and saved.data_offset==original.data_offset
        for i in range(original.count):
            a,b=original.texture(i),saved.texture(i)
            if i in EDITED:
                assert (a.flags,a.width,a.height)==(b.flags,b.width,b.height)
                assert [bool(n) for n in a.indices]==[bool(n) for n in b.indices]
                assert set(b.indices)<={0,1}
                expected=(0,0,0) if kind=='black' else (255,255,255)
                assert b.palette[1][:3]==expected and b.palette[0]==a.palette[0]
                assert all(a.palette[n]==b.palette[n] for n in range(len(a.palette)) if n!=1)
                cases.append({'texture':i,'all_original_nonzero_mask_points_retained':sum(bool(n) for n in a.indices),
                              'flags_dimensions_palette0_exact':True,'control_palette1_RGB':list(expected)})
            else:assert a==b
        fixture=NdsImage.open(ROM);fixture.replace_file(FILE,bytes(result))
        target=ROOT/f'M28_{kind}_COLOR_CONTROL_RESEARCH.nds';fixture.save(target)
        a,b=rom_files(parent),rom_files(NdsImage.open(target))
        assert a.keys()==b.keys() and [p for p in a if a[p]!=b[p]]==[FILE]
        fixtures.append({'kind':kind,'ROM':str(target),'ROM_sha256':sha(target.read_bytes()),
                         'only_changed_file':FILE,'parent':str(ROM),'parent_sha256':sha(ROM.read_bytes()),
                         'movie_sha256':sha(bytes(result)),'cases':cases,'research_only':True,
                         'not_a_localized_release_candidate':True})
    proof={'production_ROM':str(ROM),'production_ROM_sha256':sha(ROM.read_bytes()),
           'production_movie_sha256':sha(data),'edited_textures':EDITED,'fixtures':fixtures,
           'scope':'Same geometry and opaque coverage, palette0 unchanged; nonzero indices map to1 and only palette1 is recolored. All other textures/code/files exact. Original startup caller, no slot substitution.',
           'production_ROM_modified':False,'full_goal_complete':False}
    (ROOT/'color_control_fixtures.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Two isolated black/white M28 controls:22 existing English masks retained; only M28 changes; production V573 unchanged.')


if __name__=='__main__':main()
