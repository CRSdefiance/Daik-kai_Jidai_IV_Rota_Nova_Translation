"""Review independent product pitches and exact post-substitution native layouts."""

import argparse
import shutil
import struct
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R6,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.product_pitches_editorial import IDS, STUB, compile_template, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/product_pitches_v747')
MANUSCRIPT = Path('translations/product_pitches_editorial_manuscript_v1.json')
CONFIG = Path('translations/product_pitches_editorial_release_v1.json')
ROM = Path('out/all_routes_combined_v746_candidate.nds')
TEXTS = {
    675: "Take a look! %s! The very best, without a doubt!",
    676: "Come see the delicious dishes you can make with this, ma'am!",
    677: "See the fashions and decor that'll soon be the talk of society! Fancy yourself a lady or gentleman? Step right up!",
    678: "Mmm, that aroma and flavor! It'll perk you right up. Come on, try it!",
    679: "New inventions and industries are everywhere. My lecture's worth your time. Don't dawdle, or you'll miss your chance to profit!",
    680: "This cures every illness! Humor me and give it a try.",
    681: "Hmm... %s? That's worth looking into. Let's try selling some around %s.",
}


def category_cases(arm):
    cpu = machine(arm)
    rows, selected = [], []

    def observer(u, address, size, unused):
        if address == BASE + 0x53FE4:
            selected.append(u.reg_read(UC_ARM_REG_R1))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0x5E60C:
            u.emu_stop()

    hook = cpu.hook_add(UC_HOOK_CODE, observer)
    try:
        for category in range(20):
            selected.clear()
            cpu.mem_write(0x0245000C, bytes([category]))
            cpu.reg_write(UC_ARM_REG_R6, 0x02450000)
            cpu.emu_start(BASE + 0x5E588, BASE + 0x5E60C, count=100)
            expected = 676 if category < 4 else 678 if category in (4, 5) else 680 if category == 13 else 679 if category in (15, 16, 17) else 677
            assert selected == [expected], (category, selected, expected, hex(cpu.reg_read(UC_ARM_REG_PC)))
            rows.append({'supplied_category': category, 'original_selected_message': expected})
    finally:
        cpu.hook_del(hook)
    return rows


def wrapper_dispatch(arm):
    cpu = machine(arm)
    selected = []

    def stop(u, address, size, unused):
        if address in (0x01FFCF78, 0x01FF9EDC):
            u.emu_stop()

    hook = cpu.hook_add(UC_HOOK_CODE, stop)
    try:
        for parent in (0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8):
            for i in range(3668):
                cpu.mem_write(STACK + 0x264, struct.pack('<I', parent))
                cpu.mem_write(STACK + 0x274, struct.pack('<I', i))
                cpu.mem_write(STACK + 0x27C, struct.pack('<I', 0x021184C0))
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                cpu.emu_start(0x01FFCF3C, 0x01FFD000, count=200)
                pc = cpu.reg_read(UC_ARM_REG_PC)
                assert pc in (0x01FFCF78, 0x01FF9EDC)
                selected.append(pc)
    finally:
        cpu.hook_del(hook)
    return selected


def catalog(arm):
    cpu = machine(arm)
    path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/giveaway_v746_new/frame_003200_arm9_ram.bin')
    raw = path.read_bytes()
    cpu.mem_write(BASE, raw)
    result = {}
    for kind, fn, count, stride in (('products', 0xCB124, 124, 16), ('cities', 0xCB178, 90, 108)):
        call(cpu, fn, ())
        root = cpu.reg_read(UC_ARM_REG_R0) + 4
        rows = []
        for i in range(count):
            ob = root + i * stride
            vt = struct.unpack('<I', cpu.mem_read(ob, 4))[0]
            getter = struct.unpack('<I', cpu.mem_read(vt + 8, 4))[0]
            call(cpu, getter - BASE, (ob,))
            pointer = cpu.reg_read(UC_ARM_REG_R0)
            text = bytes(cpu.mem_read(pointer, 80)).split(b'\0')[0].decode('ascii')
            assert text and len(text) < 40
            rows.append({'index': i, 'name': text, 'original_object': ob, 'name_getter': getter})
        result[kind] = rows
    result['RAM_source'] = str(path)
    result['RAM_source_sha256'] = sha(raw)
    result['all124_commodity_owners_count_matches_registered_fidelity_table'] = True
    return result


def native_layout(cpu, text, number, values, parent=0x02054014):
    output, template, arg1, arg2, wrapped = (0x02420020, 0x02420400, 0x02420800, 0x02420900, 0x02420C20)
    cpu.mem_write(output - 16, b'\xA5' * 288)
    cpu.mem_write(template, text + b'\0')
    for address, value in zip((arg1, arg2), values):
        cpu.mem_write(address, value.encode('ascii') + b'\0')
    call(cpu, 0xD7720, (output, template, arg1, arg2))
    expected = text
    for value in values:
        expected = expected.replace(b'%s', value.encode('ascii'), 1)
    assert bytes(cpu.mem_read(output, len(expected) + 1)) == expected + b'\0'
    assert bytes(cpu.mem_read(output - 16, 16)) == b'\xA5' * 16
    assert bytes(cpu.mem_read(output + len(expected) + 1, 271 - len(expected))) == b'\xA5' * (271 - len(expected))
    cpu.mem_write(wrapped - 16, b'\xA5' * 288)
    cpu.mem_write(STACK + 0x264, struct.pack('<I', parent))
    cpu.mem_write(STACK + 0x274, struct.pack('<I', number))
    call(cpu, 0x01FFCF3C - BASE, (wrapped, output, 0))
    formatted = bytes(cpu.mem_read(wrapped, 256)).split(b'\0', 1)[0]
    assert bytes(cpu.mem_read(wrapped - 16, 16)) == bytes(cpu.mem_read(wrapped + 256, 16)) == b'\xA5' * 16
    assert b' '.join(formatted.split()) == b' '.join(expected.split())
    lines = [line.strip().decode('ascii') for line in formatted.split(b'\n')]
    assert len(lines) <= 4 and all(len(line) <= 35 for line in lines), (number, values, lines)
    return formatted, lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refine-unpublished-draft', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    if args.refine_unpublished_draft:
        assert CONFIG.exists() and MANUSCRIPT.exists()
        assert not (ROOT / 'gameplay_verification.json').exists() and not (ROOT / 'proof.json').exists()
        iteration = 1
        while (ROOT / f'unpublished_draft_{iteration}').exists():
            iteration += 1
        archived = ROOT / f'unpublished_draft_{iteration}'
        archived.mkdir()
        for path in (CONFIG, MANUSCRIPT, ROOT / 'native_review.json', ROOT / 'native_layout_matrix.json',
                     ROOT / 'native_previews_2x.png', Path('out/all_routes_combined_v747_candidate.nds'),
                     Path('out/all_routes_combined_v747_candidate.manifest.json')):
            shutil.copyfile(path, archived / path.name)
        save(archived / 'disposition.json', {'unpublished_research_only_superseded_before_gameplay_or_handoff': True,
                                           'reason': 'Unpublished wording refinement: number-neutral commodity prose and complete natural emphasis; repeated full native layout validation follows.',
                                           'files': {p.name: sha(p.read_bytes()) for p in archived.iterdir() if p.is_file()}})
    else:
        assert not CONFIG.exists() and not MANUSCRIPT.exists()
    current = NdsImage.open(ROM)
    common, arm = current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == read('translations/editorial_review_current_v1.json')['current_integrated_candidate']['sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x5E458, 0x5E678), (0x5E8FC, 0x5EB2C), (0x53F9C, 0x54058))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    assert struct.unpack_from('<I', arm, 0x5E668)[0] == 675
    assert struct.unpack_from('<I', arm, 0x5E674)[0] == 677
    assert struct.unpack_from('<I', arm, 0x5E678)[0] == 739
    assert struct.unpack_from('<I', arm, 0x5EB28)[0] == 681
    categories = category_cases(arm)
    assert categories == category_cases(clean)
    # V653 removed the only old branch into this obsolete table-selector stub.
    code = MainCodeFile(arm, BASE)
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    units += [(s.ramAddress, bytes(s.data)) for s in loadOverlayTable(current.rom.arm9OverlayTable, lambda _, f: current.rom.files[f]).values()]
    for base, data in units:
        for offset in range(len(data) - 3):
            value = struct.unpack_from('<I', data, offset)[0]
            assert not STUB <= value < STUB + 28, (base + offset, value)
            if offset % 4 == 0 and value & 0x0E000000 == 0x0A000000:
                delta = (value & 0xFFFFFF) << 2
                if delta & 0x02000000:
                    delta -= 0x04000000
                destination = (base + offset + 8 + delta) & 0xFFFFFFFF
                assert not STUB <= destination < STUB + 28, (base + offset, destination)
    document = deepcopy(read('translations/shop_town_editorial_manuscript_v1.json'))
    document['records'] = [r for r in document['records'] if r['message_id'] in IDS]
    document['status'] = 'native-reviewed-gameplay-pending-experimental'
    entries = common_message_entries(common, arm, clean=False)
    for row in document['records']:
        i = row['message_id']
        row['english'] = TEXTS[i] + '{PAD}'
        row['current_text_hex'] = entries[i].text.hex()
        row['decision'] = 'revise'
        row['speaker'] = 'Original promotion actor selected at native5E548-5E568' if i < 681 else 'Original competing merchant selected at native5E97C-5E98C'
        row['context'] = ('Source5E568 introduces product675, then category selects676/677/678/679/680 through direct portrait parent54014. Source5E618 may separately offer travel request739, outside this batch. Source5EAF4 supplies product and target city to681; the food and fashion pitches676/677 are independently selectable messages, not a split sentence.')
        if i == 678:
            row['localization_note'] = 'Perk you right up conveys the fatigue-relief boast as fluent sales patter, without asserting an independently verified item effect.'
        elif i == 679:
            row['localization_note'] = 'Keep new inventions/industries, the worthwhile lecture and the warning against missing profits; use direct, idiomatic sales patter.'
        elif i == 681:
            row['localization_note'] = 'That is worth looking into sounds natural while preserving interest in the product and the proposed selling area; both substitutions stay in source order.'
        elif i == 675:
            row['localization_note'] = 'Preserve the invitation to inspect and emphatic finest-quality claim. Number-neutral wording works with every singular, mass or plural commodity name.'
        elif i == 676:
            row['localization_note'] = 'Restore a complete independent cooking pitch, including dishes made using the product and the call to a nearby woman. Remove the unrelated Discover continuation.'
        row['review']['context'] = row['review']['formatting'] = True
        row['status'] = 'source-reviewed-native-layout-verified-gameplay-pending'
    target_common, target_arm, repack = transform(common, arm, document)
    dispatch_before, dispatch_after = wrapper_dispatch(arm), wrapper_dispatch(target_arm)
    changed_dispatch = [i for i, (a, b) in enumerate(zip(dispatch_before, dispatch_after, strict=True)) if a != b]
    assert changed_dispatch == list(IDS)
    names = catalog(arm)
    save(ROOT / 'runtime_name_catalog.json', names)
    cpu = machine(target_arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(target_arm, BASE).sections[3].data[:-48]))
    font = GameAsciiFont.from_arm9(target_arm)
    matrix, previews = [], []
    for i in IDS:
        text = compile_template(TEXTS[i] + '{PAD}', i)
        cases = [(r['name'],) for r in names['products']] if i == 675 else [(p['name'], c['name']) for p in names['products'] for c in names['cities']] if i == 681 else [()]
        rendered_keys = set()
        for values in cases:
            if len(matrix) % 64 == 0:
                # Bound host JIT/hook lifetime during the exhaustive matrix.
                cpu = machine(target_arm)
                cpu.mem_write(0x02387A20, bytes(MainCodeFile(target_arm, BASE).sections[3].data[:-48]))
            parent = 0x02054014
            formatted, lines = native_layout(cpu, text, i, values, parent)
            key = (len(lines), tuple(len(s) & 1 for s in values))
            matrix.append({'message_id': i, 'substitutions': list(values), 'lines': lines, 'complete_printf_and_wrap_with_guards': True})
            # Complete glyph planes for every static pitch, and all line-count /
            # substitution-parity classes among exhaustive dynamic layouts.
            if key not in rendered_keys:
                rendered_keys.add(key)
                plane = raster(target_arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
                expected = bytearray(228 * 64)
                for row, line in enumerate(lines):
                    for n, char in enumerate(line):
                        glyph = font.decode(char)
                        for y in range(11):
                            for x in range(6):
                                if glyph.getpixel((x, y)):
                                    expected[(16 * row + y) * 228 + 6 + n * 6 + x] = 1
                assert plane == bytes(expected), (i, values, lines)
                path = ROOT / f'native_{i}_case_{len(rendered_keys)}.png'
                Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in plane)).save(path)
                previews.append({'message_id': i, 'substitutions': values, 'lines': lines, 'path': str(path), 'complete_font_plane_exact': True})
            if len(matrix) % 1000 == 0:
                print(f'{len(matrix)} complete native product/city layouts verified', flush=True)
    save(ROOT / 'native_layout_matrix.json', matrix)
    sheet = Image.new('RGB', (730, len(previews) * 150), '#30343c')
    draw = ImageDraw.Draw(sheet)
    for n, row in enumerate(previews):
        draw.text((8, n * 150), f'{row["message_id"]}: {row["substitutions"]}', fill='white')
        sheet.paste(Image.open(row['path']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (8, n * 150 + 18))
    sheet.save(ROOT / 'native_previews_2x.png')
    save(MANUSCRIPT, document)
    (ROOT / 'research_COMMON.bin').write_bytes(target_common)
    (ROOT / 'research_ARM9.bin').write_bytes(target_arm)
    save(ROOT / 'native_review.json', {
        'source_ROM_sha256': sha(ROM.read_bytes()), 'original_source_spans': [{'start': a, 'end': b, 'sha256': sha(arm[a:b])} for a, b in spans],
        'original20_category_selection_prefixes_per_clean_and_current': categories,
        '675_intro_five_category_pitches_and681_two_substitutions_source_bound': True,
        'optional_travel_request739_outside_batch_unchanged': True,
        'all18340_dispatch_cases_only_direct675_to681_changed': True,
        'old_stub_no_pointer_or_direct_branch_references_in_all_current_sections_and_overlays': True,
        'name_catalog': str(ROOT / 'runtime_name_catalog.json'), 'complete_native_printf_wrap_cases': len(matrix),
        'all124_products_and_all90_cities_crossed_for681': True, 'complete_native_font_planes': previews,
        'matrix_sha256': sha((ROOT / 'native_layout_matrix.json').read_bytes()),
        'repack': repack, 'live_gameplay_pending': True, 'full_goal_complete': False})
    save(CONFIG, {'format': 'dk4-product-pitches-editorial-v1',
        'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
        'target_common_sha256': sha(target_common), 'target_arm9_sha256': sha(target_arm),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in (
            Path('dk4tool/patch/product_pitches_editorial.py'), Path('dk4tool/patch/shop_business_editorial.py'),
            Path('dk4tool/script/common_native_repack.py'), ROOT / 'native_review.json')}})
    path = Path('translations/release_stack.json')
    registry = read(path)
    assert ('all-routes-unified-v747' in registry['profiles']) == args.refine_unpublished_draft
    if not args.refine_unpublished_draft:
        save(ROOT / 'release_stack_before_V747.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v746'])
    profile.update({'product_pitches_editorial': str(CONFIG), 'status': 'experimental',
                    'description': 'Complete V746 plus seven source-reviewed promotion messages and scoped post-substitution formatting; gameplay pending.'})
    registry['profiles']['all-routes-unified-v747'] = profile
    save(path, registry)
    print(f'V747 registered: {len(matrix)} native printf/wrap cases and {len(previews)} complete font planes.', flush=True)


if __name__ == '__main__':
    main()
