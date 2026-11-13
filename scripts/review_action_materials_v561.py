"""Research-only local-source inpainting for twelve textured action captions."""
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/action_materials_v561')
GROUPS = ([(0,120),(0,136),(0,192),(40,192),(0,208),(40,208)],
          [(40,160),(40,176),(136,160),(136,192),(88,160),(88,176)])


def main():
    current = NdsImage.open('out/all_routes_combined_v558_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    batch = json.loads(Path('translations/frame_action_buttons_graphics_v7.json').read_text(encoding='utf-8'))
    original = PxlImage.from_bytes(clean.read_file(batch['file_path']))
    before = PxlImage.from_bytes(current.read_file(batch['file_path']))
    result = PxlImage.from_bytes(before.source)
    rows, allowed = [], set()
    for group_index, cells in enumerate(GROUPS):
        width = 40 if group_index == 0 else 48
        tiles = [[original.indices[(sy+y)*256+sx+x] for y in range(16) for x in range(width)]
                 for sx, sy in cells]
        hidden = []
        for tile in tiles:
            white = {(x,y) for y in range(2,13) for x in range(3,width-3) if tile[y*width+x] == 15}
            shadow = {(x,y) for y in range(2,13) for x in range(3,width-3)
                      if tile[y*width+x] == 0 and any(abs(x-xx)<=2 and abs(y-yy)<=2 for xx,yy in white)}
            hidden.append(white | shadow)
        for bank, (sx, sy) in enumerate(cells):
            record = batch['records'][group_index*6+bank]
            l,t,r,b = record['box']
            assert [l,t,r,b] == [sx+3,sy+2,sx+width-3,sy+13]
            reconstructed, restored, fallback = 0, 0, 0
            for y in range(2,13):
                for x in range(3,width-3):
                    pos = (sy+y)*256+sx+x
                    allowed.add(pos)
                    if before.indices[pos] == 15:
                        continue
                    value = tiles[bank][y*width+x]
                    if (x,y) in hidden[bank]:
                        candidates = []
                        for other in range(6):
                            if other == bank or (x,y) in hidden[other]:
                                continue
                            errors = []
                            for dy in range(-2,3):
                                for dx in range(-2,3):
                                    xx,yy=x+dx,y+dy
                                    if (0<=xx<width and 0<=yy<16 and
                                            (xx,yy) not in hidden[bank] and (xx,yy) not in hidden[other]):
                                        a=original.palette[tiles[bank][yy*width+xx]][:3]
                                        c=original.palette[tiles[other][yy*width+xx]][:3]
                                        errors.append(sum((aa-cc)**2 for aa,cc in zip(a,c,strict=True)))
                            if errors:
                                candidates.append((sum(errors)/len(errors),other,tiles[other][y*width+x]))
                        if candidates:
                            _,_,value=min(candidates)
                        else:
                            # Same original plate, along its diagonal material stripe.
                            samples=[(abs(delta),tiles[bank][(y-delta)*width+x+delta])
                                     for delta in range(-12,13) if delta and
                                     3<=x+delta<width-3 and 2<=y-delta<13 and
                                     (x+delta,y-delta) not in hidden[bank]]
                            assert samples, (record['text'],x,y)
                            _,value=min(samples)
                            fallback+=1
                        assert value != 15
                        reconstructed+=1
                    else:
                        restored += before.indices[pos] != value
                    result.indices[pos]=value
            assert {p for p in allowed if before.indices[p]==15} == {p for p in allowed if result.indices[p]==15}
            rows.append({'id':record['id'],'English':record['text'],'box':record['box'],
                         'Japanese_face_and_two_pixel_shadow_mask':len(hidden[bank]),
                         'concealed_background_points_reconstructed':reconstructed,
                         'same_plate_diagonal_fallback_points':fallback,
                         'source_visible_points_restored':restored,'fully_completed':False})
    assert all(a==b for p,(a,b) in enumerate(zip(before.indices,result.indices,strict=True)) if p not in allowed)
    output=result.to_bytes()
    assert output[:result.pixels_offset]==before.source[:before.pixels_offset]
    (ROOT/'action_RESEARCH_ONLY.pxl').write_bytes(output)
    sheet=Image.new('RGB',(900,len(rows)*85+30),(40,45,50));draw=ImageDraw.Draw(sheet)
    for col,label in enumerate(('Original source','Current V558','Local source prototype')):draw.text((col*300+5,5),label,fill='white')
    for n,row in enumerate(rows):
        draw.text((5,n*85+30),row['English'],fill='white')
        for col,atlas in enumerate((original,before,result)):
            crop=atlas.render().crop(row['box']).convert('RGB');sheet.paste(crop.resize((crop.width*5,crop.height*5),Image.Resampling.NEAREST),(col*300+5,n*85+45))
    sheet.save(ROOT/'local_texture_prototype_review.png')
    proof={'candidate':'out/all_routes_combined_v558_candidate.nds','candidate_sha256':sha(current.source.read_bytes()),
           'file_path':batch['file_path'],'source_sha256':sha(before.source),'target_sha256':sha(output),
           'records':rows,'all12_English_masks_positions_and_all_other_controls_retained':True,
           'header_all83_palettes_dimensions_unowned_pixels_retained':True,
           'concealed_texture_is_reconstruction_not_original_recovery':True,
           'visual_native_embedded_sync_and_integration_pending':True,'production_ROM_changed':False,'full_goal_complete':False}
    (ROOT/'local_texture_prototype_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Prepared12 local-source action texture prototypes; full English masks and all unrelated art retained.')


if __name__ == '__main__':
    main()
