"""Review complete product expansions and static specialty/shop replies."""

import argparse
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_responses_editorial import IDS, compile_template, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_product_pitches_v747 import catalog, native_layout, wrapper_dispatch
from scripts.probe_button_prompt_native import BASE, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_responses_v751')
MANUSCRIPT = Path('translations/town_responses_manuscript_v1.json')
CONFIG = Path('translations/town_responses_editorial_release_v1.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refine-unpublished', action='store_true')
    args = parser.parse_args()
    assert CONFIG.exists() == MANUSCRIPT.exists() == args.refine_unpublished
    if args.refine_unpublished:
        assert (ROOT / 'unpublished_first_draft').is_dir() and not (ROOT / 'gameplay_verification.json').exists()
    context = read(ROOT / 'native_context.json')
    assert context['script_sha256'] == sha(Path('scripts/verify_town_responses_context_v751.py').read_bytes())
    current_path = Path('out/all_routes_combined_v750_candidate.nds')
    assert sha(current_path.read_bytes()) == read('out/editorial_review_latest.json')['sha256']
    current = NdsImage.open(current_path)
    common, arm = current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin')
    clean, canonical = (NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds'))
    path = '/COMMON/MESFILE.DK4'
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = common_message_entries(common, arm, clean=False)
    drafts = read('work/analysis/town_events_v750/related_trend_entries_653_655.json')['records'] + read('translations/town_events_editorial_manuscript_v1.json')['records']
    rows = [deepcopy(next(r for r in drafts if r['message_id'] == i)) for i in IDS]
    for row in rows:
        i = row['message_id']
        assert bytes.fromhex(row['source_hex']) == source[i].text
        row.update({'canonical_source_hex': accepted[i].text.hex(), 'current_text_hex': before[i].text.hex(),
            'current_English': ' '.join(before[i].text.decode('cp932').split()),
            'source_reference': {'block': source[i].block, 'record': source[i].record_index, 'offset': source[i].block_offset},
            'current_reference': {'block': before[i].block, 'record': before[i].record_index, 'offset': before[i].block_offset},
            'status': 'source-context-reviewed-native-format-check-in-progress'})
        if i in (743, 744):
            row['speaker'] = 'Original Square local-specialty requester selected by town actor getter'
            row['context'] = 'OriginalBAD0C-BADB4 fragment obtains item/product names, asks742 through Yes/No parent53FCC, and selects743 on acceptance or744 on refusal. Native supplied-result fragments verify this sequence and product-flag change; full inventory eligibility/transfer is separate.'
        elif i in (745, 746):
            row['speaker'] = 'Original Square shopkeeper'
            row['context'] = 'Source BA3D4/BA428 forwards745 from the shop continuation loop; BC244/BC248 and BC970/BC978 bind746 to ordinary portrait replies in two original shop flows. Preserve both independent selections in their shared NUL owner.'
        if i == 743:
            row.update({'english': "Really? You're so kind! You're the best!{PAD}", 'decision': 'revise',
                'localization_note': 'Preserve the enthusiastic thanks and praise; so kind naturally conveys ii hito in response to accepting a gift, without adding a reward or relationship.'})
        if i in (653, 654, 655):
            wording = {653: "We're selling %s like hotcakes!", 654: 'Brought %s? Sell your cargo at the trade house now!',
                655: "Let's sell %s and profit handsomely!"}
            row.update({'english': wording[i] + '{PAD}', 'decision': 'revise',
                'localization_note': {
                    653: 'Like hotcakes is natural American sales patter for selling extremely well now. The product is a grammatical object, so mass and plural names both work. No actual stock-out or quantity mechanic is asserted.',
                    654: 'Keep the conditional arrival with the product, the trade house and urgency. Cargo is a number-neutral object; now expresses early/prompt disposal without inventing a new demand fact.',
                    655: 'Preserve the self-rally to sell the product and make a large profit. Profit handsomely is natural merchant language for janjan moukeru, and works with all product names without a tiny trailing row.'}[i]})
        row['review'] = dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True)
    doc = {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'], 'file_path': path,
        'source_clean_COMMON_sha256': sha(clean.read_file(path)), 'source_canonical_COMMON_sha256': sha(canonical.read_file(path)),
        'source_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(current_path.read_bytes()), 'records': rows}
    target_common, target_arm, repack = transform(common, arm, doc)
    old_dispatch, new_dispatch = wrapper_dispatch(arm), wrapper_dispatch(target_arm)
    assert [i for i, (a, b) in enumerate(zip(old_dispatch, new_dispatch, strict=True)) if a != b] == [653, 654, 655]
    names = catalog(arm)
    save(ROOT / 'runtime_names.json', names)
    font = GameAsciiFont.from_arm9(target_arm)
    checks, previews, count = [], [], 0
    longest = max(names['products'], key=lambda r: len(r['name']))['name']
    cpu = None
    for row in rows:
        i = row['message_id']
        cases = [(r['name'],) for r in names['products']] if i < 700 else [()]
        for n, values in enumerate(cases):
            if count % 64 == 0:
                cpu = machine(target_arm)
                cpu.mem_write(0x02387A20, bytes(MainCodeFile(target_arm, BASE).sections[3].data[:-48]))
            count += 1
            formatted, lines = native_layout(cpu, compile_template(row['english'], i), i, values)
            assert len(lines) == 1 or len(lines[-1]) > 8, (i, values, lines)
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
            case = {'message_id': i, 'substitutions': values, 'lines': lines, 'formatted_hex': formatted.hex(),
                'complete_native_font_and_blank_cells_exact': True}
            checks.append(case)
            if n == 0 or values == (longest,):
                preview = ROOT / f'native_{i}_{n}.png'
                Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(preview)
                previews.append({**case, 'preview': str(preview), 'preview_sha256': sha(preview.read_bytes())})
    assert count == 376
    sheets = []
    for start in range(0, len(previews), 6):
        group = previews[start:start + 6]
        sheet = Image.new('RGB', (730, 150 * len(group)), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for n, case in enumerate(group):
            draw.text((8, n * 150), f'{case["message_id"]}: {case["substitutions"]}', fill='white')
            sheet.paste(Image.open(case['preview']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (8, n * 150 + 18))
        path = ROOT / f'native_previews_{len(sheets) + 1}_2x.png'
        sheet.save(path)
        sheets.append(str(path))
    for row in rows:
        row['status'] = 'source-context-native-font-reviewed-gameplay-pending'
    doc['status'] = 'experimental-native-reviewed-gameplay-pending'
    save(MANUSCRIPT, doc)
    save(ROOT / 'source_context_packet.json', {'current_ROM': str(current_path), 'current_ROM_sha256': sha(current_path.read_bytes()),
        'clean_ROM_sha256': doc['source_ROM_sha256'], 'reviewed_records': rows,
        'neighbors': [{'message_id': i, 'Japanese_hex': source[i].text.hex(), 'current_hex': before[i].text.hex()}
            for i in (*range(652, 657), *range(742, 748))], 'full_goal_complete': False})
    (ROOT / 'research_COMMON.bin').write_bytes(target_common)
    (ROOT / 'research_ARM9.bin').write_bytes(target_arm)
    save(ROOT / 'native_review.json', {'source_ROM_sha256': sha(current_path.read_bytes()),
        'context_report_sha256': sha((ROOT / 'native_context.json').read_bytes()), 'all376_complete_native_font_cases': checks,
        'preview_cases': previews, 'sheets': sheets, 'all18340_dispatch_cases_only3_new_direct_IDs653_655': True,
        'four_static_responses_use_existing_guarded_compiler': True,
        'revised_IDs': [r['message_id'] for r in rows if r['decision'] == 'revise'],
        'retained_wording_IDs': [r['message_id'] for r in rows if r['decision'] == 'retain-wording'],
        'repack': repack, 'gameplay_pending': True, 'full_goal_complete': False})
    save(CONFIG, {'format': 'dk4-town-responses-editorial-v1',
        'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
        'target_common_sha256': sha(target_common), 'target_arm9_sha256': sha(target_arm),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in (Path('dk4tool/patch/town_responses_editorial.py'),
            Path('dk4tool/patch/shop_business_editorial.py'), Path('dk4tool/script/common_native_repack.py'),
            ROOT / 'native_review.json', ROOT / 'native_context.json')}})
    path = Path('translations/release_stack.json')
    registry = read(path)
    assert ('all-routes-unified-v751' in registry['profiles']) == args.refine_unpublished
    if not args.refine_unpublished:
        save(ROOT / 'release_stack_before_V751.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v750'])
    profile.update({'town_responses_editorial': str(CONFIG), 'status': 'experimental',
        'description': 'Complete V750 plus source-reviewed653-655 and743-746. Category730 and dynamic question742 remain open.'})
    registry['profiles']['all-routes-unified-v751'] = profile
    save(path, registry)
    print('V751 registered:7 reviewed entries,376 complete native font cases; gameplay pending.', flush=True)


if __name__ == '__main__':
    main()
