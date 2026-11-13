"""Stage and verify the complete Price Info descriptions without a runtime patch."""

from dataclasses import replace
from hashlib import sha256
from inspect import getsource
from pathlib import Path
import re
from struct import unpack_from
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R3
from unicorn.arm_const import UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_SP

from dk4tool.dialogue.layout import format_markup
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import preflight_diplomatic_outcome_wrap_v1 as sheets
from scripts import review_trade_good_descriptions_v2 as editorial
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, pagination
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import PROFILE
from scripts.stage_shared_notices_storage_v1 import relocate


previous = editorial.previous
parent, base = previous.parent, previous.parent.base
ARM, COMMON = previous.ARM, previous.COMMON
ROOT = Path('out/trade_good_descriptions_staged_20261111_v1')
ROM = ROOT / 'trade_good_descriptions_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
OUTPUT = editorial.OUTPUT
FIRST, LAST = previous.FIRST, previous.LAST
PROFILE = replace(PROFILE, window_width_px=216, max_lines=8, guard_linebreaks=False,
                  pair_phase_safe_breaks=False, balanced_wrapping=True)
ROWS_PER_PAGE = 3


def rows_for(text):
    return format_markup(text, PROFILE).split('{LB}')


def plan(text):
    lines = rows_for(text)
    if len(lines) <= ROWS_PER_PAGE:
        return lines
    # Fit a complete thought on either side of the native page boundary when possible.
    candidates = []
    for gap in re.finditer(r'(?<=[.!?]) ', text):
        left, right = rows_for(text[:gap.start()]), rows_for(text[gap.end():])
        if len(left) == ROWS_PER_PAGE and len(right) <= ROWS_PER_PAGE:
            candidates.append((left, right))
    if candidates:
        left, right = min(candidates, key=lambda pair: (abs(len(pair[1]) - 2), len(pair[1])))
        return left + right
    return lines


def repack(runtime, rows):
    storage = {}
    for n, row in rows.items():
        text = row['english']
        assert text.isascii() and text == ' '.join(text.split()) and '%' not in text
        lines = plan(text)
        assert 1 <= len(lines) <= 6 and all(0 < len(line) <= 36 for line in lines), (n, lines)
        assert ' '.join(lines) == text
        # The legacy painter reads ASCII in pairs. An even byte count before LF
        # keeps the following line's first character out of the preceding pair.
        aligned = [line + ' ' * (len(line) % 2) for line in lines[:-1]]
        storage[n] = '\n'.join([*aligned, lines[-1]]).encode('ascii')
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    move = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, packing = move(runtime.common, runtime.arm, rows, storage)
    assert arm[:DIRECTORY_OFFSET] == runtime.arm[:DIRECTORY_OFFSET]
    assert arm[TABLE_END:] == runtime.arm[TABLE_END:] and packing['all_41_blocks_fit_8KiB']
    return common, arm, rebound, packing, storage


def stored_case(runtime, n, text):
    cpu, _, provider = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R6, n - FIRST + 21)
    cpu.reg_write(UC_ARM_REG_R7, 0)
    cases = []

    def original_template(u, address, size, data):
        assert u.reg_read(UC_ARM_REG_R0) == u.reg_read(UC_ARM_REG_R3) == 0
        assert u.reg_read(UC_ARM_REG_LR) == 0x020546E8
        pointer = u.reg_read(UC_ARM_REG_R1)
        assert bytes(u.mem_read(pointer, len(text) + 1)) == text + b'\0'
        cases.append(pointer)

    cpu.hook_add(UC_HOOK_CODE, original_template, begin=0x02054774, end=0x02054774)
    cpu.emu_start(0x020BE51C, 0x0205479C, count=3_000_000)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x0205479C
    assert {0x020BE534, 0x020BF328, 0x020546B8} <= provider.executed_current
    for address in unpack_from('<2I', runtime.arm, 0x54890):
        assert bytes(cpu.mem_read(address, 256)).split(b'\0', 1)[0] == text, n
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    pointer, = cases
    return dict(native_modal_template_pointer=pointer, original_source_selector=0x020BE51C,
                mode=0, original_loader_and_formatter_exact=True, substitutions=[])


def native_pages(raster, arm, kanji, text):
    # A full 36-cell row is valid. Aligned LF leaves the next row at column zero,
    # including the continuation after the third row.
    source = checked_text(getsource(pagination), {
        "assert segment.endswith(b'\\n') and remaining.startswith(b'  ')":
            "assert segment.endswith(b'\\n') and remaining[0] > 32",
    })
    env = dict(pagination.__globals__)
    exec(compile(source, __file__ + '::mode-zero-pagination', 'exec'), env)
    return env['pagination'](raster, arm, kanji, text)


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    draft = base.load(OUTPUT)
    assert draft['current_ROM_sha256'] == release['candidate_sha256']
    rows = {n: row for n, row in enumerate(draft['records'], FIRST)}
    assert list(rows) == list(range(FIRST, LAST + 1))
    common, arm, rebound, packing, storage = repack(runtime, rows)
    staged = with_components(runtime, arm, common)
    raster, _, _ = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    records, pages, labels = [], [], []
    for n, row in rows.items():
        text = storage[n]
        case = stored_case(staged, n, text)
        renders = native_pages(raster, arm, kanji, text)
        assert 1 <= len(renders) <= 2
        visual = []
        for i, page in enumerate(renders, 1):
            pixels = page.pop('pixels')
            glyphs = page.pop('glyphs')
            visible = [line.rstrip() for line in page['visible_text']]
            assert ''.join(chr(g['code']) for g in glyphs) == ''.join(visible).replace(' ', '')
            assert all(g['x'] + 6 <= 216 and g['y'] + 12 <= 48 for g in glyphs)
            assert 1 <= len(visible) <= ROWS_PER_PAGE
            assert i == len(renders) or len(visible) == ROWS_PER_PAGE
            visual.append(dict(page | {'visible_text': visible, 'pixel_sha256': sha256(pixels).hexdigest(),
                                      'glyphs': len(glyphs)}))
            pages.append(pixels)
            labels.append(dict(message_ID=n, arguments=[row['commodity_name'], f'{i}/{len(renders)}']))
        assert ' '.join(line for page in visual for line in page['visible_text']) == row['english']
        records.append(dict(message_ID=n, source_reference=row['source_reference'],
            previous_reference=row['current_reference'], staged_reference=previous.reference(rebound[n]),
            display_hex=text.hex(), pages=visual, **case))

    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    sheet_maker = FunctionType(sheets.preview_sheets.__code__, vars(sheets) | {'ROOT': ROOT})
    views = sheet_maker(labels, pages)
    base.save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        parent_inverse_exact=True, allocation=packing, native_runtime_code_changed=False, records=records,
        sheets=views, manuscript_sha256=base.digest(OUTPUT), native_pages=len(pages),
        formatting_pending_visual_review=True, gameplay_pending=True, registered_release_pending=True,
        new_credit=0, full_goal_complete=False))
    print(f'{len(records)} original selector and loader paths, {len(pages)} complete native pages.')


if __name__ == '__main__':
    main()
