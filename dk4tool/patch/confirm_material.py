"""Restore original blue Confirm shading and complete native English lettering."""
import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha


def recover(original,current,arm):
    assert (original.width,original.height)==(48,20)
    assert current.source[:current.pixels_offset]==original.source[:original.pixels_offset]
    face={(x,y) for y in range(3,17) for x in range(4,43) if original.indices[y*48+x]<=6}
    white={(x,y) for y in range(20) for x in range(48) if original.indices[y*48+x]==13}
    hidden=white|{(x,y) for x,y in face if original.indices[y*48+x]==0
                  and any(abs(x-a)<=2 and abs(y-b)<=2 for a,b in white)}
    visible=face-hidden

    def prediction(point,controls):
        x,y=point
        ends=[]
        for direction in (-1,1):
            for distance in range(1,48):
                p=(x+direction*distance,y-direction*distance)
                if p in controls:
                    ends.append((distance,p))
                    break
        if len(ends)!=2:
            return None
        (da,a),(db,b)=ends
        ca=original.palette[original.indices[a[1]*48+a[0]]][:3]
        cb=original.palette[original.indices[b[1]*48+b[0]]][:3]
        colour=tuple((u*db+v*da)/(da+db) for u,v in zip(ca,cb,strict=True))
        index=min(range(7),key=lambda n:sum((a-b)**2 for a,b in zip(colour,original.palette[n][:3],strict=True)))
        return index,a,b

    controls=[]
    for point in sorted(visible):
        predicted=prediction(point,visible-{point})
        if predicted is not None:
            value,a,b=predicted;actual=original.indices[point[1]*48+point[0]]
            controls.append({'point':list(point),'actual':actual,'predicted':value,
                             'RGB_max_channel_error':max(abs(x-y) for x,y in zip(original.palette[value][:3],original.palette[actual][:3],strict=True))})
    result=PxlImage.from_bytes(original.source)
    sources=[]
    for point in sorted(hidden):
        predicted=prediction(point,visible)
        if predicted is None:
            raise ValueError(f'No two-sided original diagonal controls for {point}')
        value,a,b=predicted
        result.indices[point[1]*48+point[0]]=value
        sources.append({'point':list(point),'source_controls':[list(a),list(b)],'index':value})
    font=GameAsciiFont.from_arm9(arm);text='Confirm';ink=set();left=(48-len(text)*5)//2
    for n,ch in enumerate(text):
        glyph=font.decode(ch)
        assert not any(glyph.getpixel((x,y)) for y in range(2) for x in range(6))
        assert not any(glyph.getpixel((5,y)) for y in range(11))
        ink|={(left+n*5+x,5+y-2) for y in range(2,11) for x in range(5) if glyph.getpixel((x,y))}
    shadow={(x+1,y+1) for x,y in ink}-ink
    for x,y in shadow:result.indices[y*48+x]=0
    for x,y in ink:result.indices[y*48+x]=13
    assert {(x,y) for y in range(20) for x in range(48) if result.indices[y*48+x]==13}==ink
    material={(x,y) for y in range(20) for x in range(48) if (x,y) not in hidden|ink|shadow}
    assert all(result.indices[y*48+x]==original.indices[y*48+x] for x,y in material)
    assert all(result.indices[y*48+x]==original.indices[y*48+x] for y in range(20) for x in range(48)
               if original.indices[y*48+x] in range(7,13))
    assert all(result.indices[y*48+x]==original.indices[y*48+x] for y in range(20) for x in range(48)
               if x<4 or x>=43 or y<3 or y>=17)
    return result,{'source_white_points':len(white),'old_source_stroke_shadow_points_reconstructed':len(hidden),
                   'all_hidden_points_have_two_sided_original_controls':True,
                   'held_out_visible_control_points':len(controls),
                   'held_out_controls_exact':sum(p['actual']==p['predicted'] for p in controls),
                   'held_out_max_RGB_channel_error':max(p['RGB_max_channel_error'] for p in controls),
                   'complete_native_font_ink':len(ink),'new_English_shadow_points':len(shadow),
                   'all_visible_original_material_points_exact':len(material),
                   'original_grey_bevel_pixels_exact':True,'changed_pixels':sum(a!=b for a,b in zip(current.indices,result.indices,strict=True)),
                   'concealed_gradient_is_inferred_not_exact_recovery':True,'reconstruction_controls':sources,
                   'held_out_control_details':controls}


def apply_release(candidate, clean, config_path):
    config=json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format']!='dk4-confirm-material-v1':
        raise ValueError('Unknown Confirm material format')
    path='/_pxl/kakutei.pxl'
    before,source=candidate.read_file(path),clean.read_file(path)
    if (sha(before),sha(source))!=(config['source_sha256'],config['clean_sha256']):
        raise ValueError('Confirm source or inherited pixels differ')
    result,proof=recover(PxlImage.from_bytes(source),PxlImage.from_bytes(before),candidate.read_file('/__arm9__.bin'))
    output=result.to_bytes()
    if sha(output)!=config['target_sha256'] or len(output)!=len(before):
        raise ValueError('Confirm material target or extent differs')
    details={k:v for k,v in proof.items() if isinstance(v,list)}
    compact={k:v for k,v in proof.items() if not isinstance(v,list)}
    return output,{**compact,'file_path':path,'changed_records':['DK4_CONFIRM_SOURCE_SHADING_AND_NATIVE_GLYPHS'],
                   'source_sha256':sha(before),'target_sha256':sha(output),
                   'source_control_details_sha256':sha(json.dumps(details,sort_keys=True).encode('utf-8'))}
