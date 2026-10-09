"""Generate native-pixel diagnostic sheets from the hooked monthly proof."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_modal_pixels import verify


def main():
    proof_path = Path('work/analysis/common_monthly_word_wrap_hook_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    unique = {(c['message_id'], c['amount']): c['complete_prepared_text'] for c in proof['cases']
              if c['amount'] in (999999, 42949672)}
    destination = Path('work/qa/common_monthly_native_wrapped')
    destination.mkdir(parents=True, exist_ok=True)
    sheets, panels = [], []
    for amount in (999999, 42949672):
        sheet = Image.new('RGB', (788, 7 * 166), 'white')
        draw = ImageDraw.Draw(sheet)
        for index, message in enumerate(range(76, 83)):
            text = unique[message, amount]
            native = verify(source, font, text, 16, portrait=True, guarded=True)
            colors = struct.unpack('<49152H', native['pixels'])
            panel = Image.new('RGB', (256, 192))
            panel.putdata([(255, 255, 255) if color == 9 else (128, 128, 128) if color == 14
                           else (0, 0, 0) for color in colors])
            panel = panel.crop((0, 0, 256, 96)).resize((768, 144), Image.Resampling.NEAREST)
            draw.text((10, index * 166 + 4), f'ID {message}, amount {amount}', fill='black')
            sheet.paste(panel, (10, index * 166 + 20))
            panels.append({'message_id': message, 'amount': amount, 'text': text,
                           'raw_native_pixels_sha256': sha(native['pixels']),
                           'visual_review': 'pending'})
        path = destination / f'amount_{amount}.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    report = {'status': 'native-ink-previews-awaiting-visual-review', 'panels': panels, 'sheets': sheets,
              'preparation_proof_sha256': sha(proof_path.read_bytes()),
              'limitations': 'Exact native glyph positions shown with white diagnostic background. Physical palette, portrait image composition, bitmap origin/routing and input are unproven.'}
    (destination / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Two native monthly sheets generated, covering all seven drafts at both maximum amounts.')


if __name__ == '__main__':
    main()
