"""Fit all Ancient Map fields and rumors to their original visible text areas."""

from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.layout import format_markup
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import register_arrival_month_labels_v1 as parent
from scripts import review_ancient_map_rumors_v2 as rumor
from scripts import review_treasure_map_documents_v1 as document
from scripts import stage_golden_route_exchanges_v1 as previous
from scripts.probe_button_prompt_native import STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_mutiny_review_v1 import PROFILE
from scripts.stage_shared_notices_storage_v1 import relocate


base, ARM, COMMON, BASE = parent.base, document.ARM, document.COMMON, document.BASE
ROOT = Path('out/ancient_map_text_staged_20261111_v1')
ROM = ROOT / 'ancient_map_text_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
X, TOP, RIGHT, BOTTOM, ROW = 32, 32, 248, 160, 12
LAYOUT = replace(PROFILE, window_width_px=RIGHT - X, max_lines=3, guard_linebreaks=False,
                 pair_phase_safe_breaks=False, balanced_wrapping=True)
RENDERER = parent.stage.RENDERER


def stage(runtime, release, rows):
    assert sha256(runtime.arm).hexdigest() == release['target_ARM9_sha256']
    storage = {}
    for number, row in rows.items():
        value = row['english']
        assert value.isascii() and '%' not in value and '\n' not in value
        if number < 3658:
            lines = format_markup(value, LAYOUT).split('{LB}')
            assert ' '.join(lines) == value and all(len(line) * 6 <= RIGHT - X for line in lines)
            limit = 3 if row['native_field'] == 'artifact_lore' else 2 if row['native_field'] == 'sea_region' else 1
            assert len(lines) <= limit, (number, lines)
            value = '\n'.join(lines)
        storage[number] = value.encode('ascii')
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, allocation = repack(runtime.common, runtime.arm, rows, storage)
    assert allocation['all_41_blocks_fit_8KiB'] and allocation['touched_blocks'] == [40]
    assert arm[:DIRECTORY_OFFSET] == runtime.arm[:DIRECTORY_OFFSET] and arm[TABLE_END:] == runtime.arm[TABLE_END:]
    return arm, common, storage, rebound, allocation


def original_document_lookup(ctx, field, number, raw):
    cpu, _, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    result = {}

    def stop(u, pc, size, _):
        pointer = u.reg_read(UC_ARM_REG_R1)
        assert bytes(u.mem_read(pointer, len(raw) + 1)) == raw + b'\0'
        result.update(original_call=field['original_lookup'], original_renderer_entry=pc, original_input=pointer)
        u.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, stop, begin=RENDERER, end=RENDERER)
    index = field['ids'].index(number)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_R1, index)
    cpu.reg_write(UC_ARM_REG_R4, index)
    cpu.emu_start(field['original_load'], RENDERER + 4, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == RENDERER and result['original_renderer_entry'] == RENDERER
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return result | dict(native_index=index, original_file_reads=provider.reads)


def document_preview(font, fields):
    panel = Image.new('L', (256, BOTTOM), 255)
    y = TOP
    for raw in fields:
        for line in raw.decode('ascii').split('\n'):
            assert X + len(line) * 6 <= RIGHT and y + 11 <= BOTTOM
            for index, char in enumerate(line):
                glyph = font.decode(char)
                assert (glyph.width, glyph.height) == (6, 11)
                panel.paste(0, (X + index * 6, y), glyph)
            y += ROW
        y += ROW
    return panel


def document_sheets(pages):
    result = []
    for start in range(0, len(pages), 8):
        batch = pages[start:start + 8]
        sheet = Image.new('RGB', (1040, 348 * ((len(batch) + 1) // 2)), '#263238')
        labels = ImageDraw.Draw(sheet)
        for i, (ids, panel) in enumerate(batch):
            x, y = i % 2 * 520 + 4, i // 2 * 348
            labels.text((x + 6, y + 5), 'Display test  ' + ', '.join(map(str, ids)), fill='white')
            sheet.paste(panel.resize((512, 320), Image.Resampling.NEAREST), (x, y + 22))
        path = ROOT / f'document_sheet_{start // 8 + 1:02}.png'
        sheet.save(path)
        result.append(dict(path=str(path), sha256=base.digest(path), document_combinations=[ids for ids, _ in batch]))
    return result


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    rt = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    map_draft, rumor_draft = map(base.load, (document.OUTPUT, rumor.OUTPUT))
    assert map_draft['current_ROM_sha256'] == release['candidate_sha256'] and rumor_draft['registered_input'] == rt.receipt()
    rows = {row['message_ID']: row for row in map_draft['records'] + rumor_draft['records']}
    assert set(rows) == set(range(3607, 3668))
    arm, common, storage, rebound, allocation = stage(rt, release, rows)
    portrait = previous.fleet.portrait
    ctx = portrait.with_components(rt, arm, common)
    font = GameAsciiFont.from_arm9(arm)
    renderer, _, font_receipt = portrait.font_tools(rt.image)
    kanji = rt.image.read_file('/GRP/KANJI.FNT')
    rumor_display = previous.portrait_with_arguments()
    records, portrait_pages = [], []
    for number, row in rows.items():
        raw = storage[number]
        if number < 3658:
            native = original_document_lookup(ctx, map_draft['native_fields'][row['native_field']], number, raw)
            display, glyphs = raw, sum(char not in b' \n' for char in raw)
        else:
            native = rumor_display(ctx, row, None, raw, None, ())
            display = native.pop('display')
            pixels, glyphs = portrait.render_portrait(renderer, arm, kanji, display)
            assert [glyph['code'] for glyph in glyphs] == previous.glyph_codes(raw)
            glyphs = len(glyphs)
            portrait_pages.append((number, pixels))
        assert b' '.join(display.split()) == row['english'].encode('ascii')
        records.append(dict(message_ID=number, source_reference=row['source_reference'],
            previous_reference=row['current_reference'], staged_reference=document.reference(rebound[number]),
            staged_hex=raw.hex(), display_hex=display.hex(), complete_glyphs=glyphs,
            visible_lines=display.decode('ascii').split('\n'), original_consumer=native))
    combinations = []
    for i, pair in enumerate(map_draft['original_region_direction_pairs']):
        # Independently indexed artifact lore is cycled to cover every field in the previews.
        ids = [3648 + i % 10, pair['sea_region'], pair['direction'], 3607]
        combinations.append((ids, document_preview(font, [storage[number] for number in ids])))
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, rt.arm)
    image.replace_file(COMMON, rt.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    map_sheets = document_sheets(combinations)
    rumor_sheets = portrait.portrait_sheets(ROOT, portrait_pages)
    base.save(PROOF, dict(registered_input=rt.receipt(), research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        allocation=allocation, records=records, font=font_receipt, map_sheets=map_sheets, rumor_sheets=rumor_sheets,
        document_preview_scope='All 51 fields through the original loaders and exact font geometry. The 20 previews cycle the independent lore index for coverage.',
        documented_visible_rectangle=[X, TOP, RIGHT, BOTTOM], row_step=ROW,
        original_runtime_code_preserved=True, complete_parent_inverse_exact=True,
        manuscript_sha256={str(path): base.digest(path) for path in (document.OUTPUT, rumor.OUTPUT)},
        visual_review_pending=True, gameplay_pending=True, new_credit=0))
    print('Verified 51 original document lookups, 20 full map previews and ten native rumor portraits.')


if __name__ == '__main__':
    main()
