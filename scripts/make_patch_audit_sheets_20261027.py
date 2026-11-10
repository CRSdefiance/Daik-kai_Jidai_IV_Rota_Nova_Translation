"""Deterministic representative sheets; successful execution is not visual approval."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path('work/patch_interaction_audit_20261027')


if __name__ == '__main__':
    destination = ROOT / 'sheets'
    destination.mkdir(exist_ok=True)
    index = {}
    for case in sorted((ROOT / 'cases').iterdir()):
        source = case / 'capture/capture_report.json'
        if not source.exists():
            continue
        report = json.loads(source.read_text(encoding='utf-8'))
        rows = [r for r in report['frames_captured'] if r['frame'] >= 3000]
        if not rows:
            continue
        selected = [rows[(len(rows)-1)*i//5] for i in range(6)]
        sheet = Image.new('RGB', (768, 832), '#20252b')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(selected):
            x, y = (i%3)*256, (i//3)*416
            draw.text((x+4,y+4),case.name+' frame '+str(row['frame']),fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB'),(x,y+24))
        output = destination / (case.name+'.png')
        sheet.save(output)
        index[case.name] = dict(sheet=str(output), selected_frames=[r['frame'] for r in selected],
            source_report=str(source), target_ROM_sha256=report['ROM_sha256'], visual_review_pending=True)
    (ROOT / 'visual_index.json').write_text(json.dumps(index,indent=2)+'\n')
    print('Prepared',len(index),'six-frame sheets using fixed evenly spaced frame selection.')
