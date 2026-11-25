"""Independent full native font planes for the owned-location research samples."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_tavern_conversations_v764 import CURRENT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764')


def main():
    rom = NdsImage.open(CURRENT)
    arm, kanji = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    proof = read(ROOT / 'owned_storage_and_native_research.json')
    assert proof['source_ARM9_sha256'] == sha(arm)
    previews = []
    for i, row in enumerate(proof['complete_layout_samples']):
        pixels = raster(arm, bytes.fromhex(row['formatted_hex']), 0x01FFCE40 - 0x02000000,
                        size=(228, 64), instruction_limit=1000000)
        assert pixels == independent_font(arm, kanji, row['lines']), (i, row)
        path = ROOT / f'owned_font_{i:02d}_ID{row["id"]}.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(path)
        previews.append({**row, 'path': str(path), 'sha256': sha(path.read_bytes()),
                         'complete_native_font_plane_matches_independent_font': True})
    sheets = []
    for start in range(0, len(previews), 12):
        sheet = Image.new('RGB', (1428, 720), '#30343c'); draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(previews[start:start + 12]):
            x, y = i % 3 * 476, i // 3 * 180
            draw.text((x + 5, y + 4), f'RESEARCH ID{row["id"]} / {start + i}', fill='white')
            with Image.open(row['path']) as preview:
                sheet.paste(preview.convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x + 5, y + 24))
        path = ROOT / f'owned_fonts_{start // 12:02d}_2x.png'; sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(ROOT / 'complete_font_samples.json', {'source_ARM9_sha256': sha(arm),
        'all31_IDs': sorted({r['id'] for r in previews}), 'complete_planes': previews, 'sheets': sheets,
        'scope': '50 representative supplied-value font planes at mapped-runtime output; full wrapping matrix and actual gameplay remain required.',
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print(f'{len(previews)} full font planes exact; {len(sheets)} sheets await visual inspection.', flush=True)


if __name__ == '__main__': main()
