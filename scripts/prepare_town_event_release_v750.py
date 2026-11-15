"""Verify every product expansion and both native portrait contracts before registration."""

import argparse
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_events_editorial import IDS, compile_template, transform
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import catalog, native_layout, wrapper_dispatch
from scripts.probe_button_prompt_native import BASE, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_events_v750')
MANUSCRIPT = Path('translations/town_events_release_manuscript_v1.json')
CONFIG = Path('translations/town_events_editorial_release_v1.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refine-unpublished', action='store_true')
    args = parser.parse_args()
    assert CONFIG.exists() == MANUSCRIPT.exists() == args.refine_unpublished
    if args.refine_unpublished:
        assert not (ROOT / 'gameplay_verification.json').exists()
        assert (ROOT / 'unpublished_first_draft').is_dir()
    context = read(ROOT / 'native_context.json')
    assert [len(context['clean_and_current_original_selection_cases'][k]) for k in ('trend', 'relief', 'promoter')] == [288, 432, 6]
    current = NdsImage.open('out/all_routes_combined_v749_candidate.nds')
    common, arm = current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin')
    doc = deepcopy(read('translations/town_events_editorial_manuscript_v1.json'))
    doc['records'] = [r for r in doc['records'] if r['message_id'] in IDS]
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    for row in doc['records']:
        assert all(row['review'][k] for k in ('source', 'context', 'localization', 'naturalness'))
        row['review']['formatting'] = True
        row['speaker'] = 'Original town Square shopkeeper' if row['message_id'] <= 737 else 'Traveling promoter selected from the original player-state actor entries'
        row['status'] = 'source-context-reviewed-native-format-check-in-progress'
    target_common, target_arm, repack = transform(common, arm, doc)
    before, after = wrapper_dispatch(arm), wrapper_dispatch(target_arm)
    assert [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b] == list(range(730, 742))
    names = catalog(arm)
    save(ROOT / 'runtime_names.json', names)
    font = GameAsciiFont.from_arm9(target_arm)
    checks, selected_previews, cpu = [], [], None
    count = 0
    for row in doc['records']:
        i = row['message_id']
        cases = [(r['name'],) for r in names['products']] if i in (731, 733) else [()]
        longest = max(names['products'], key=lambda r: len(r['name']))['name']
        for n, values in enumerate(cases):
            if count % 64 == 0:
                cpu = machine(target_arm)
                cpu.mem_write(0x02387A20, bytes(MainCodeFile(target_arm, BASE).sections[3].data[:-48]))
            count += 1
            raw = compile_template(row['english'], i)
            parent = 0x02053FCC if i == 739 else 0x02054014
            formatted, lines = native_layout(cpu, raw, i, values, parent=parent)
            pixels = raster(target_arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
            expected = bytearray(228 * 64)
            for line_no, line in enumerate(lines):
                for column, char in enumerate(line):
                    glyph = font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x, y)):
                                expected[(16 * line_no + y) * 228 + 6 + column * 6 + x] = 1
            assert pixels == bytes(expected), (i, values, lines)
            case = {'message_id': i, 'substitutions': values, 'parent': parent, 'lines': lines,
                'formatted_hex': formatted.hex(), 'complete_native_font_and_blank_cells_exact': True}
            checks.append(case)
            if n == 0 or values == (longest,):
                preview = ROOT / f'native_{i}_{n}.png'
                Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(preview)
                selected_previews.append({**case, 'preview': str(preview), 'preview_sha256': sha(preview.read_bytes())})
    # ID730 is only newly wrapped, not rewritten or counted editorially complete.
    from dk4tool.script.common_message_table import common_message_entries

    old730 = common_message_entries(common, arm, clean=False)[730].text
    layouts730 = []
    for entry in context['category_arguments']:
        formatted, lines = native_layout(cpu, old730, 730, (entry['current_category_argument'],))
        layouts730.append({'category': entry, 'lines': lines, 'formatted_hex': formatted.hex()})
    sheets = []
    for start in range(0, len(selected_previews), 7):
        group = selected_previews[start:start + 7]
        sheet = Image.new('RGB', (730, 150 * len(group)), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for n, case in enumerate(group):
            draw.text((8, n * 150), f'{case["message_id"]}: {case["substitutions"]}', fill='white')
            sheet.paste(Image.open(case['preview']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (8, n * 150 + 18))
        path = ROOT / f'native_previews_{len(sheets) + 1}_2x.png'
        sheet.save(path)
        sheets.append(str(path))
    assert count == 257
    for row in doc['records']:
        row['status'] = 'source-context-native-font-reviewed-gameplay-pending'
    doc['status'] = 'experimental-native-reviewed-gameplay-pending'
    save(MANUSCRIPT, doc)
    (ROOT / 'research_COMMON.bin').write_bytes(target_common)
    (ROOT / 'research_ARM9.bin').write_bytes(target_arm)
    save(ROOT / 'native_review.json', {'source_ROM_sha256': sha(current.source.read_bytes()),
        'context_report_sha256': sha((ROOT / 'native_context.json').read_bytes()),
        'all257_complete_printf_wrap_and_native_font_cases': checks, 'preview_cases': selected_previews, 'sheets': sheets,
        'all18340_dispatch_cases_only12_new_direct_IDs730_741': True,
        '739_static_compiler_preserves_original_question_parent_and_native_controls': True,
        '730_18_format_only_cases_not_editorial_completion': layouts730,
        'revised_IDs': [r['message_id'] for r in doc['records'] if r['decision'] == 'revise'],
        'retained_wording_IDs': [r['message_id'] for r in doc['records'] if r['decision'] == 'retain-wording'],
        'repack': repack, 'gameplay_pending': True, 'full_goal_complete': False})
    save(CONFIG, {'format': 'dk4-town-events-editorial-v1',
        'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
        'target_common_sha256': sha(target_common), 'target_arm9_sha256': sha(target_arm),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in (
            Path('dk4tool/patch/town_events_editorial.py'), Path('dk4tool/patch/shop_business_editorial.py'),
            Path('dk4tool/script/common_native_repack.py'), ROOT / 'native_review.json', ROOT / 'native_context.json')}})
    path = Path('translations/release_stack.json')
    registry = read(path)
    assert ('all-routes-unified-v750' in registry['profiles']) == args.refine_unpublished
    if not args.refine_unpublished:
        save(ROOT / 'release_stack_before_V750.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v749'])
    profile.update({'town_events_editorial': str(CONFIG), 'status': 'experimental',
        'description': 'Complete V749 plus reviewed731-741 trends/relief/promoter prose;730 receives formatting only and remains editorially pending.'})
    registry['profiles']['all-routes-unified-v750'] = profile
    save(path, registry)
    print('V750 registered:11 source-reviewed entries,257 whole font planes; gameplay pending.', flush=True)


if __name__ == '__main__':
    main()
