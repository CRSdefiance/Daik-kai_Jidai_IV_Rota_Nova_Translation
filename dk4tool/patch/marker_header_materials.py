"""Restore complete marker header ownership and source material."""
import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.cargo_banner_texture import components
from dk4tool.patch.grand_race_menu_release import sha

ROWS = (('tempcargo',184,0,64,'一時置き場','Temp Storage',(2,3),13),
        ('haifuhin',168,64,48,'配布品','Issued',(0,1,4),14),
        ('senrihin',168,80,48,'戦利品','Spoils',(0,1),14))


def repair(clean, current):
    original = PxlImage.from_bytes(clean.read_file('/_pxl/__marker.pxl'))
    before = PxlImage.from_bytes(current.read_file('/_pxl/__marker.pxl'))
    result = PxlImage.from_bytes(before.source)
    font = GameAsciiFont.from_arm9(current.read_file('/__arm9__.bin'))
    cases, owned = [], set()
    for stem,left,top,width,jp,text,shadow_indices,bottom in ROWS:
        donor = PxlImage.from_bytes(clean.read_file(f'/_pxl/{stem}.pxl'))
        white = {(x,y) for y in range(16) for x in range(width) if donor.indices[y*256+x]==15}
        actual_white = {(x,y) for y in range(16) for x in range(width)
                        if original.indices[(top+y)*256+left+x]==15}
        assert white == actual_white
        if stem == 'tempcargo':
            shadows = {(x+1,y+1) for x,y in white if x+1<width and y+1<16
                       and donor.indices[(y+1)*256+x+1] in shadow_indices}
        else:
            shadows = {(x,y) for y in range(1,bottom) for x in range(2,width)
                       if donor.indices[y*256+x] in shadow_indices
                       and any(abs(x-a)<=2 and abs(y-b)<=2 for a,b in white)}
        assert all(original.indices[(top+y)*256+left+x] <= 3 for x,y in shadows)
        hidden = white | shadows
        for y in range(16):
            for x in range(width):
                n=(top+y)*256+left+x
                owned.add(n)
                result.indices[n]=original.indices[n]
        mapping = [min(range(16), key=lambda n: sum((a-b)**2 for a,b in
                   zip(colour[:3],original.palette[n][:3],strict=True))) for colour in donor.palette]
        groups = []
        for group in components(hidden):
            l,r=min(x for x,y in group),max(x for x,y in group)
            context = {(x+dx,y+dy) for x,y in group for dx in range(-2,3) for dy in (-1,0,1)
                       if 2<=x+dx<width-2 and 1<=y+dy<bottom and (x+dx,y+dy) not in hidden}
            assert context
            choices=[]
            for offset in range(128-l,248-r):
                if not all(128<=x+offset<248 for x,y in context):
                    continue
                score=sum(sum(abs(a-b) for a,b in zip(
                    original.palette[original.indices[(top+y)*256+left+x]][:3],
                    original.palette[mapping[donor.indices[y*256+x+offset]]][:3],strict=True)) for x,y in context)
                choices.append((score,abs(offset-128),offset))
            score,_,offset=min(choices)
            for x,y in group:
                value=donor.indices[y*256+x+offset]
                assert value != 15 and mapping[value] != 15
                result.indices[(top+y)*256+left+x]=mapping[value]
            groups.append({'points':len(group),'source_offset':offset,'context_points':len(context),'RGB_distance':score})
        def advance(ch):
            return 3 if ch==' ' else 5
        text_width=sum(advance(ch) for ch in text)
        assert text_width<=width-6
        cursor=left+(width-text_width)//2
        ink=set()
        for ch in text:
            glyph=font.decode(ch)
            assert not any(glyph.getpixel((x,y)) for y in range(2) for x in range(6))
            assert not any(glyph.getpixel((5,y)) for y in range(11))
            ink|={(cursor+x,top+3+y-2) for y in range(2,11) for x in range(5) if glyph.getpixel((x,y))}
            cursor+=advance(ch)
        for x,y in ink:result.indices[y*256+x]=15
        assert {(x,y) for y in range(top,top+16) for x in range(left,left+width)
                if result.indices[y*256+x]==15}==ink
        material={(left+x,top+y) for y in range(16) for x in range(width)
                  if (x,y) not in hidden and (left+x,top+y) not in ink}
        assert all(result.indices[y*256+x]==original.indices[y*256+x] for x,y in material)
        outside_legacy={(x,y) for x,y in white if stem!='tempcargo' and not 176<=left+x<209}
        assert all(before.indices[(top+y)*256+left+x]==15 for x,y in outside_legacy)
        assert all(result.indices[(top+y)*256+left+x]!=15 for x,y in outside_legacy)
        cases.append({'stem':stem,'Japanese':jp,'English':text,'source_box':[left,top,left+width,top+16],
                      'standalone_glyph_geometry_exact':True,'source_strokes':len(white),'source_shadows':len(shadows),
                      'complete_English_ink':len(ink),'original_visible_material_points_exact':len(material),
                      'legacy_outside_box_Japanese_points_removed':len(outside_legacy),
                      'palette_mapping':mapping,'donor_file':f'/_pxl/{stem}.pxl','donor_sha256':sha(donor.source),
                      'component_donors':groups,'concealed_material_is_inferred':True})
    assert all(result.indices[n]==before.indices[n] for n in range(65536) if n not in owned)
    assert result.source[:result.pixels_offset]==original.source[:original.pixels_offset]
    return result,{'cases':cases,'changed_pixels':sum(a!=b for a,b in zip(before.indices,result.indices,strict=True)),
                   'outside_all3_source_panels_exact_V569':True,'all_metadata_palettes_dimensions_exact_clean':True}


def apply_release(candidate, clean, config_path):
    config=json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format']!='dk4-marker-header-materials-v1':
        raise ValueError('Unknown marker header materials format')
    path, archive_path='/_pxl/__marker.pxl','/GRP/CMMNIMG.DK4'
    before, source, archived=candidate.read_file(path),clean.read_file(path),candidate.read_file(archive_path)
    if (sha(before),sha(source),sha(archived))!=(config['source_sha256'],config['clean_sha256'],config['source_archive_sha256']):
        raise ValueError('Marker header source locks differ')
    for donor_path,expected in config['original_donor_sha256'].items():
        if sha(clean.read_file(donor_path))!=expected:
            raise ValueError('Original marker header donor differs')
    result,proof=repair(clean,candidate)
    output=result.to_bytes()
    if sha(output)!=config['target_sha256'] or len(output)!=len(before):
        raise ValueError('Marker header target or extent differs')
    previous=PxlImage.from_bytes(before)
    archive=IlnkContainer.parse(archived)
    block=archive.blocks[5]
    packed=bytearray(block[20:])
    if len(packed)!=65536:
        raise ValueError('Unexpected shared atlas extent')
    for y in range(256):
        for x in range(0,256,2):
            pos=(y*512+x)//2
            old=packed[pos]
            if (old&15,old>>4)!=(previous.indices[y*256+x],previous.indices[y*256+x+1]):
                raise ValueError('Inherited marker copy is not synchronized')
            packed[pos]=result.indices[y*256+x]|result.indices[y*256+x+1]<<4
    archive.blocks[5]=block[:20]+bytes(packed)
    archive_output=archive.to_bytes()
    if sha(archive_output)!=config['target_archive_sha256'] or len(archive_output)!=len(archived):
        raise ValueError('Marker header embedded target or extent differs')
    return {path:output,archive_path:archive_output},[
        {'file_path':path,'changed_records':config['record_ids'],'source_sha256':sha(before),'target_sha256':sha(output),**proof},
        {'file_path':archive_path,'changed_records':['DK4_MARKER_HEADERS_EMBEDDED_SYNC'],
         'source_sha256':sha(archived),'target_sha256':sha(archive_output),'left_marker_only_synchronized':True}]
