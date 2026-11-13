"""Map complete original header glyphs and reconstruct only concealed source wood."""
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.marker_header_materials import repair
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/marker_headers_v570')
def main():
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open('out/all_routes_combined_v569_candidate.nds')
    result,proof=repair(clean,current)
    before=PxlImage.from_bytes(current.read_file('/_pxl/__marker.pxl'))
    original=PxlImage.from_bytes(clean.read_file('/_pxl/__marker.pxl'))
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'marker_headers_RESEARCH_ONLY.pxl').write_bytes(result.to_bytes())
    canvas=Image.new('RGB',(780,360),'#263238');draw=ImageDraw.Draw(canvas)
    for row,case in enumerate(proof['cases']):
        draw.text((8,row*120+4),case['English']+' / original / V569 / research',fill='white')
        for col,img in enumerate((original,before,result)):
            l,t,r,b=case['source_box'];crop=img.render().crop((l,t,r,b)).convert('RGB')
            canvas.paste(crop.resize((crop.width*3,48),Image.Resampling.NEAREST),(8+col*260,row*120+28))
    canvas.save(ROOT/'material_and_bounds_review.png')
    proof.update(source_sha256=sha(before.source),clean_sha256=sha(original.source),target_sha256=sha(result.to_bytes()),
                 research_only=True,production_ROM_changed=False)
    (ROOT/'prototype_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'changed_pixels':proof['changed_pixels'],'cases':[{k:v for k,v in c.items()
          if k not in ('palette_mapping','component_donors')} for c in proof['cases']]},ensure_ascii=False))


if __name__=='__main__':main()
