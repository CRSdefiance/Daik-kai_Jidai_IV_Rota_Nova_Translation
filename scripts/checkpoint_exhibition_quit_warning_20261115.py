"""Verify the retail Quit Game selector and preflight its separate legacy warning."""

from pathlib import Path
import re
from struct import iter_unpack, pack, unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.village_promised_words_release import resident_components
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_cristina_recruitment_name_20261115 as current
from scripts.checkpoint_race_quit_common_20261114 import OUTPUT as EARLIER
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.preflight_setup_save_equipment_v1 import check_modal, font_tools, HEIGHT, WIDTH
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_setup_save_equipment_v1 import OUTPUT as MANUSCRIPT
from scripts.review_sound_bgm_titles_v1 import reference


stage, base = current.stage, current.base
ROOT = Path('work/exhibition_quit_warning_20261115_v2')
SHEET = ROOT / 'offline_warning.png'
OUTPUT = EARLIER.with_name('exhibition_quit_warning_20261115_v2.json')
HELPER, CALLER, WRAPPER = 0x0203FC08, 0x0203FBC0, 0x0205466C
GETTER, FORMAT = 0x0205528C, 0x02054774
SELECTOR_END = BASE + 0x3FC40
FLAGS = (0, 1, 2, 0x7fffffff, 0x80000000, 0xffffffff)
DRAFT = 'You will lose this exhibition data if you quit. Quit anyway?'


def sites(image):
    refs, literals = [], []
    for name, origin, raw in resident_components(image):
        for index, (word,) in enumerate(iter_unpack('<I', raw[:len(raw) // 4 * 4])):
            at = origin + 4 * index
            if direct_bl_target(word, at) == HELPER:
                refs.append((name, at))
        literals.extend((name, origin + m.start()) for m in re.finditer(re.escape(pack('<I', HELPER)), raw))
    assert refs == [('arm9_section_0', CALLER)] and not literals
    return dict(direct_ARM_callers=refs, literal_entry_pointer_references=literals)


def flags_on_source(arm, flag_addr):
    cpu = machine(arm)
    rows = []
    for flag in FLAGS:
        cpu.mem_write(flag_addr, pack('<I', flag))
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.reg_write(UC_ARM_REG_R0, 0xA5A5A5A5)
        cpu.emu_start(HELPER, WRAPPER if flag == 1 else STOP, count=32)
        end = cpu.reg_read(UC_ARM_REG_PC)
        argument = cpu.reg_read(UC_ARM_REG_R0)
        assert (end, argument, cpu.reg_read(UC_ARM_REG_SP)) == (
            (WRAPPER, 319, STACK - 8) if flag == 1 else (STOP, 1, STACK))
        assert bytes(cpu.mem_read(flag_addr, 4)) == pack('<I', flag)
        rows.append(dict(flag=flag, stop=end, COMMON_argument=argument if flag == 1 else None))
    return rows


def current_template(runtime, flag_addr, record):
    u, _, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    u.mem_write(flag_addr, pack('<I', 1))
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    seen = []

    def getter(uc, pc, size, data):
        seen.append(uc.reg_read(UC_ARM_REG_R0))

    u.hook_add(UC_HOOK_CODE, getter, begin=GETTER, end=GETTER)
    u.emu_start(HELPER, FORMAT, count=500000)
    assert u.reg_read(UC_ARM_REG_PC) == FORMAT and seen == [319]
    pointer = u.reg_read(UC_ARM_REG_R1)
    raw = bytes(u.mem_read(pointer, len(record.text) + 1))
    assert raw == record.text + b'\0'
    assert bytes(u.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    assert bytes(u.mem_read(flag_addr, 4)) == pack('<I', 1)
    runtime.calls.clear()
    return dict(original_modal_entry=FORMAT, native_lookup=seen, text_pointer=pointer, complete_template_hex=raw.hex())


def main():
    assert not ROOT.exists() and not OUTPUT.exists()
    release = base.load(current.RELEASE)
    runtime = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    source = base.NdsImage.open(stage.CLEAN)
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    clean, arm = source.read_file(stage.ARM), runtime.arm
    assert clean[HELPER - BASE:SELECTOR_END - BASE] == arm[HELPER - BASE:SELECTOR_END - BASE]
    assert clean[CALLER - BASE:CALLER - BASE + 4] == arm[CALLER - BASE:CALLER - BASE + 4]
    caller_bound = sites(runtime.image)
    assert sites(source) == caller_bound
    root, message = unpack_from('<2I', clean, 0x3FC38)
    assert message == 319
    flag_addr = root + 0x54
    selected = flags_on_source(arm, flag_addr)
    assert flags_on_source(clean, flag_addr) == selected

    original = common_message_entries(source.read_file(stage.COMMON), clean)
    stored = owned_entries(runtime.common, arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    prior = base.load(EARLIER)
    assert prior['actual_quit']['common_ID'] == 319
    for ident, section, key in ((319, 'actual_quit', 'source_reference'), (318, 'legacy318', 'source_reference')):
        assert prior[section][key] == reference(original[ident])
    assert prior['legacy318']['current_hex'] == stored[318].text.hex()
    assert stored[319].text.decode('ascii').strip() == 'Quit the game?'
    proved = current_template(runtime, flag_addr, stored[319])

    earlier = next(row for row in base.load(MANUSCRIPT)['records'] if row['message_ID'] == 318)
    assert earlier['source_hex'] == original[318].text.hex()
    assert earlier['native_substitution_count'] == 0 and 'Ｉf' in stored[318].text.decode('cp932')
    assert earlier['english'] == "This is exhibition data. If you quit, you'll lose it. Quit anyway?"
    # Deliberately supplying this unused-in-tested-flow key tests the draft's fit in
    # a proven Yes/No consumer. It does not identify the original caller for 318.
    raster, _, meta = font_tools(runtime.image)
    case, pixels = check_modal(runtime, earlier | dict(current_hex=stored[318].text.hex(), english=DRAFT,
        native_callers=[dict(target=WRAPPER)]), (), raster, GameAsciiFont.from_arm9(arm))
    assert pixels is not None and case['complete_glyphs_bounds_and_words']
    storage = case['storage_markup'].replace('{LB}', '\n').encode('ascii')
    available = stored[318].copy_end - stored[318].block_offset
    assert len(storage) + 1 <= available
    assert case['native_lines'] == ['You will lose this exhibition data', 'if you quit. Quit anyway?']
    ROOT.mkdir()
    sheet = Image.new('RGB', (488, 130), '#222d33')
    ImageDraw.Draw(sheet).text((12, 6), 'COMMON 318   Offline confirmation-box preview', fill='white')
    plane = Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if p else 255 for p in pixels))
    sheet.paste(plane.resize((456, 96), Image.Resampling.NEAREST), (12, 24))
    sheet.save(SHEET)
    report = dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        normal_quit=dict(helper=HELPER, stock_flag_address=flag_addr, caller_bound=caller_bound,
            clean_current_code_equal=True, paired_selector_cases=selected, exact_active_template=proved,
            reused_actual_quit_evidence=prior['actual_quit'], source=reference(original[319]),
            current=reference(stored[319]), english='Quit the game?', decision='retention',
            reason='Keep the brief direct question for ending an ordinary session.', review=dict.fromkeys(earlier['review'], True)),
        exhibition_warning=earlier | dict(current_reference=reference(stored[318]), english=DRAFT,
            prior_draft=earlier['english'], current_hex=stored[318].text.hex(), controlled_native_confirmation=case,
            localization_note='Keep the source data type and consequence. The conditional phrase and the confirmation question both fit intact on the second line.',
            possible_context_open=True),
        supplied_key_318_not_a_qualified_consumer_binding=True, template_bytes=len(storage) + 1,
        existing_slot_bytes=available,
        font_contract=meta, sheet=str(SHEET), sheet_sha256=base.digest(SHEET), gameplay_new=False, ROM_changed=False,
        evidence={str(path): base.digest(path) for path in (EARLIER, MANUSCRIPT, current.RELEASE)})
    base.save(OUTPUT, report)
    print('Six paired original selector cases pass. Ordinary Quit Game reaches 319 only. The prospective 318 warning fits the tested native confirmation box.')


if __name__ == '__main__':
    main()
