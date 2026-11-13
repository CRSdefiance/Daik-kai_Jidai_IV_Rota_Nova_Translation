"""Prospective supplied-value native layouts;no production routing approval."""

import argparse
from itertools import product
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.review_scheme_followup_v777 import CURRENT, ROOT, MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save


def main(manuscript=MANUSCRIPT, out=ROOT/'layouts_v1'):
    manuscript, out = Path(manuscript), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    doc = read(manuscript)
    context = read(ROOT/'native_context.json')
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    assert context['candidate_sha256'] == sha(CURRENT.read_bytes())
    raw = Path(context['pre_fixture_snapshot']['path']).read_bytes()
    assert sha(raw) == context['pre_fixture_snapshot']['sha256']
    factions = [bytes.fromhex(r['name_hex']) for r in read('work/analysis/tavern_schemes_editorial_v774/native_context.json')['all21_initialized_native_faction_names'] if r['name_hex']]
    towns = [bytes.fromhex(r['name_hex']) for r in read('work/analysis/tavern_recruitment_editorial_v771/native_context.json')['actual114_native_town_objects']]
    assert len(factions) == 20 and len(towns) == 114
    cases, warnings = [], []
    for row in doc['records']:
        variants = product(towns, factions) if 978 <= row['message_id'] <= 983 else ((),)
        count = 0
        for i, args in enumerate(variants):
            if i % 64 == 0:
                u = machine(arm)
                u.mem_write(BASE, raw)
            result = format_case(u, row, args)
            cases.append(result)
            if result['findings']:
                warnings.append(result)
            count += 1
        print(row['message_id'], count, 'layouts;', len(warnings), 'findings so far', flush=True)
    save(out/'native_layout_matrix.json', {'count': len(cases), 'cases': cases, 'findings': warnings,
                                          'manuscript_sha256': sha(manuscript.read_bytes()),
                                          'original_catalog_supplied_values_only': True})
    previews, seen = [], set()
    kanji = NdsImage.open(CURRENT).read_file('/GRP/KANJI.FNT')
    for result in cases:
        marker = (result['id'], tuple(len(line.encode('cp932')) % 2 for line in result['lines']))
        if marker in seen:
            continue
        seen.add(marker)
        plane = raster(arm, bytes.fromhex(result['formatted_hex']), 0x01FFCE40-BASE,
                       size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, kanji, result['lines'])
        path = out/f'font_{len(previews):03d}_ID{result["id"]}.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in plane)).save(path)
        previews.append({**result, 'path': str(path), 'sha256': sha(path.read_bytes()),
                         'independent_complete_font_plane_exact': True})
    sheets = []
    for start in range(0, len(previews), 12):
        sheet = Image.new('RGB', (1428, 720), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for i, result in enumerate(previews[start:start+12]):
            x, y = i % 3 * 476, i // 3 * 180
            draw.text((x+5, y+4), f'RESEARCH ID{result["id"]} / {start+i}', fill='white')
            sheet.paste(Image.open(result['path']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x+5, y+24))
        path = out/f'fonts_{start//12:02d}_2x.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(out/'verification.json', {
        'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
        'manuscript': str(manuscript), 'manuscript_sha256': sha(manuscript.read_bytes()),
        'native_supplied_layouts': len(cases), 'findings_count': len(warnings),
        'complete_font_planes': previews, 'sheets': sheets,
        'all25_IDs_covered': sorted({r['id'] for r in cases}),
        'production_dispatcher_ownership_integration_and_gameplay_pending': True,
        'mutable_edited_player_company_reachability_not_yet_proven_for_bribe': True,
        'no_playable_ROM_or_completion_claim': True, 'full_goal_complete': False,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print(len(cases), 'native layouts;', len(warnings), 'findings;', len(previews), 'complete fonts. Production gates remain pending.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manuscript', type=Path, default=MANUSCRIPT)
    parser.add_argument('--out', type=Path, default=ROOT/'layouts_v1')
    args = parser.parse_args()
    main(args.manuscript, args.out)
