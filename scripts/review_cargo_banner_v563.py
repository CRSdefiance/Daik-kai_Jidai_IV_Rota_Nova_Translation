"""Research a source-local cargo banner repair, including original dark shadows."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.cargo_banner_texture import repair
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/action_consumers_v563')
FILE = '/_pxl/tempcargo.pxl'


def main():
    old_rom, clean = NdsImage.open('out/all_routes_combined_v558_candidate.nds'), NdsImage.open('work/clean.nds')
    original, current = PxlImage.from_bytes(clean.read_file(FILE)), PxlImage.from_bytes(old_rom.read_file(FILE))
    result, proof = repair(original, current)
    ROOT.mkdir(parents=True, exist_ok=True)
    target = ROOT/'tempcargo_RESEARCH_ONLY.pxl'
    target.write_bytes(result.to_bytes())
    canvas = Image.new('RGB', (1024, 3*104), '#263238')
    draw = ImageDraw.Draw(canvas)
    for row, (title, graphic) in enumerate((('Original Japanese source', original), ('V558 English: retained Japanese shadows', current),
                                           ('Research English: source-local stroke and shadow repair', result))):
        draw.text((8, row*104+4), title, fill='white')
        canvas.paste(graphic.render().convert('RGB').resize((1024, 64), Image.Resampling.NEAREST), (0, row*104+28))
    canvas.save(ROOT/'temporary_storage_review.png')
    proof.update({'source_file': FILE, 'source_sha256': sha(original.source), 'inherited_sha256': sha(current.source),
                  'target_sha256': sha(result.to_bytes()), 'research_only': True, 'production_ROM_changed': False})
    (ROOT/'temporary_storage_prototype.json').write_text(json.dumps(proof, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in proof.items() if not isinstance(v, list)}))


if __name__ == '__main__':
    main()
