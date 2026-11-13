"""Research native layout matrix; reports defects without approving the draft.

The experimental dispatcher exists only inside the in-memory ARM9 supplied to
Unicorn. It is not registered, integrated, distributed or ownership-approved.
"""

from itertools import product

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout, wrapper_dispatch
from scripts.probe_button_prompt_native import BASE, machine
from scripts.review_market_stock_v755 import CURRENT, MANUSCRIPT, ROOT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save


def experimental_arm(arm):
    code = MainCodeFile(arm, BASE)
    section = code.sections[4]
    assert section.ramAddress == 0x01FFC000 and len(section.data) == 4096
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    start = 0x01FFCF54
    old = bytes(ks.asm('cmp r3,#168; bls 0x01ffcf78; sub r3,r3,#50; cmp r3,#3; '
                       'bls 0x01ffcf78; sub r3,r3,#0xa00; sub r3,r3,#0xda; '
                       'cmp r3,#19; bhi 0x01ffcff8', start)[0])
    new = bytes(ks.asm('cmp r3,#168; bls 0x01ffcf78; add ip,r3,#53; cmp ip,#3; '
                       'bls 0x01ffcf78; sub r3,r3,#0xa00; sub r3,r3,#0x10c; '
                       'cmp r3,#19; bhi 0x01ffcff8', start)[0])
    assert len(old) == len(new) == 36
    assert bytes(section.data[0xF54:0xF78]) == old
    section.data[0xF54:0xF78] = new
    target = bytes(code.save())
    restored = MainCodeFile(target, BASE)
    restored.sections[4].data[0xF54:0xF78] = old
    assert bytes(restored.save()) == arm
    return target, {'start': start, 'old_hex': old.hex(), 'new_hex': new.hex(),
                    'explanation': 'The old870-873 test was already covered by820-988. The replacement tests767-770, retaining the identical total subtraction on the later3648-3667 and fallback path.',
                    'all_branch_and_pointer_owners_not_yet_audited': True}


def main():
    doc = read(MANUSCRIPT)
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    target, dispatch = experimental_arm(arm)
    old, new = wrapper_dispatch(arm), wrapper_dispatch(target)
    differences = [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b]
    assert differences == [767, 768, 769, 770]
    assert all(new[i] == 0x01FFCF78 for i in differences)
    save(ROOT / 'experimental_dispatch.json', {'current_ARM9_sha256': sha(arm),
        'research_ARM9_sha256': sha(target), 'patch': dispatch,
        'all18340_dispatch_cases_differ_only_in767_770_direct_parent': True,
        'not_integrated_or_approved_for_release': True})
    names = read('work/analysis/product_pitches_v747/runtime_name_catalog.json')['products']
    assert len(names) == 124
    names = [r['name'] for r in names]
    font = GameAsciiFont.from_arm9(target)
    weak = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    checks, problems, preview_rows, static_failures = [], [], [], []
    count, cpu, seen = 0, None, set()
    for row in doc['records']:
        number = row['message_id']
        paragraph = row['english'].removesuffix('{PAD}')
        slots = paragraph.count('%s')
        if slots:
            raw = b' ' + paragraph.encode('ascii')
            cases = product(names, repeat=slots)
        else:
            try:
                raw, _ = compile_paragraph(row['english'])
            except ValueError as error:
                static_failures.append({'id': number, 'error': str(error)})
                continue
            cases = [()]
        for values in cases:
            if count % 64 == 0:
                cpu = machine(target)
                cpu.mem_write(0x02387A20, bytes(MainCodeFile(target, BASE).sections[3].data[:-48]))
            formatted, lines = native_layout(cpu, raw, number, values)
            defects = []
            if len(lines) > 1 and len(lines[-1]) <= 8:
                defects.append('short_or_orphaned_final_row')
            if any(s.split()[-1].strip('.,!?;:').lower() in weak for s in lines[:-1]):
                defects.append('weak_word_at_line_end')
            case = {'id': number, 'values': values, 'lines': lines,
                    'formatted_hex': formatted.hex(), 'defects': defects}
            checks.append(case)
            if defects:
                problems.append(case)
            # Review complete font planes for every static text and each dynamic
            # row-count/parity class, plus the first defect per message.
            shape = (number, len(lines), *(len(s) % 2 for s in lines))
            want = shape not in seen or (defects and ('defect', number) not in seen)
            if want:
                seen.add(shape)
                if defects:
                    seen.add(('defect', number))
                pixels = raster(target, formatted, 0x01FFCE40 - BASE,
                                size=(228, 64), instruction_limit=1000000)
                expected = bytearray(228 * 64)
                for n, line in enumerate(lines):
                    for column, char in enumerate(line):
                        glyph = font.decode(char)
                        for y in range(11):
                            for x in range(6):
                                if glyph.getpixel((x, y)):
                                    expected[(16 * n + y) * 228 + 6 + column * 6 + x] = 1
                assert pixels == bytes(expected)
                preview = ROOT / f'draft_{number}_{len(preview_rows):03d}.png'
                Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(preview)
                preview_rows.append({**case, 'preview': str(preview), 'sha256': sha(preview.read_bytes())})
            count += 1
            if count % 2000 == 0:
                print(f'{count} native complete printf/wrap cases; {len(problems)} layout findings', flush=True)
        print(f'ID{number} finished; cumulative{count}', flush=True)
    save(ROOT / 'native_layout_matrix_DRAFT.json', {'all_cases': checks,
        'all_complete_native_word_bytes_and_buffer_guards_pass': True,
        'count': count, 'layout_findings_count': len(problems),
        'static_compile_failures': static_failures, 'sampled_complete_font_planes': preview_rows,
        'research_only_not_approved_for_release': True})
    save(ROOT / 'layout_findings_DRAFT.json', {'count': len(problems),
        'first50': problems[:50], 'static_compile_failures': static_failures,
        'by_message': {str(n): sum(r['id'] == n for r in problems) for n in range(767, 784)},
        'next': 'Resolve line-ending findings naturally or improve the bounded formatter with reviewed ownership and regression evidence; do not approve or integrate these drafts yet.'})
    # Split contact sheets to keep individual text previews readable.
    sheets = []
    for start in range(0, len(preview_rows), 18):
        group = preview_rows[start:start + 18]
        sheet = Image.new('RGB', (1404, 6 * 175), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for k, r in enumerate(group):
            x, y = (k % 3) * 468, (k // 3) * 175
            draw.text((x + 4, y + 2), f"DRAFT {r['id']} {','.join(r['defects'])}", fill='white')
            sheet.paste(Image.open(r['preview']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x + 4, y + 22))
        out = ROOT / f'draft_previews_{start // 18 + 1:02d}.png'
        sheet.save(out)
        sheets.append(str(out))
    print(f'{count} native cases, {len(problems)} wrap findings, {len(static_failures)} static failures; draft NOT approved. Sheets: {sheets}', flush=True)


if __name__ == '__main__':
    main()
