"""Research original diagonal shading through the Confirm lettering and shadows."""
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.confirm_material import recover
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT=Path('work/analysis/confirm_material_v572')
FILE='/_pxl/kakutei.pxl'


def main():
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open('out/all_routes_combined_v571_candidate.nds')
    original,before=(PxlImage.from_bytes(r.read_file(FILE)) for r in (clean,current))
    after,proof=recover(original,before,current.read_file('/__arm9__.bin'))
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'confirm_RESEARCH_ONLY.pxl').write_bytes(after.to_bytes())
    canvas=Image.new('RGB',(3*260,144),'#263238');draw=ImageDraw.Draw(canvas)
    for n,(label,p) in enumerate((('Original Japanese',original),('V571 English',before),('Research source shading',after))):
        draw.text((n*260+4,4),label,fill='white');canvas.paste(p.render().convert('RGB').resize((240,100),Image.Resampling.NEAREST),(n*260+4,28))
    canvas.save(ROOT/'source_current_repair_5x.png')
    proof.update(source_sha256=sha(before.source),clean_sha256=sha(original.source),target_sha256=sha(after.to_bytes()),
                 research_only=True,production_ROM_changed=False)
    (ROOT/'prototype_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in proof.items() if not isinstance(v,list)}))


if __name__=='__main__':main()
