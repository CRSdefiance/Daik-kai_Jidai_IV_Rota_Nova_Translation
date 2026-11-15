"""Bind the dormant DS load-message sink and the observed Continue confirmation."""

from collections import deque
from hashlib import sha256
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R11, UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_continue_empty_slot_20261115 as capture
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.probe_button_prompt_native import STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_captain_biographies_v1 import captured, shots


base, current = capture.base, capture.current
ARM, COMMON, CLEAN = current.stage.ARM, current.stage.COMMON, current.stage.CLEAN
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/continue_legacy_calls_20261115_v1.json')
BASE = 0x02000000
SETUP = (0xEDCC8, 0xEDCFC)
BRANCH = (0xEDF54, 0xEDFD4)
SINK = BASE + 0xEF068
GETTER = BASE + 0x5528C
CONFIRM = 0x169F2C


def branch_execution(runtime, stored, fp, slot_flag, inputs, warning_latch):
    cpu, _, provider = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    block = stored[111].block
    assert block == stored[112].block
    payload = IlnkContainer.parse(runtime.common).blocks[block]
    assert len(payload) <= 0x2000
    cpu.mem_write(provider.owner + 0x2C, bytes((block, 255, 0, 1)))
    cpu.mem_write(provider.owner + 0x30, payload)
    cpu.mem_write(STACK, bytes(0x80))
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.emu_start(BASE + SETUP[0], BASE + SETUP[1], count=32)
    for offset, n in ((0x34, 112), (0x38, 111)):
        assert bytes(cpu.mem_read(STACK + offset, 4)) == n.to_bytes(4, 'little')
    for register, value in ((UC_ARM_REG_R11, fp), (UC_ARM_REG_R9, slot_flag), (UC_ARM_REG_R4, inputs)):
        cpu.reg_write(register, value)
    cpu.mem_write(STACK + 0x10, warning_latch.to_bytes(4, 'little'))

    selections, discarded = [], []
    state = None
    sink_writes = []
    recent = deque(maxlen=16)

    def watched(u, address, size, _):
        nonlocal state
        recent.append(hex(address))
        if address == GETTER:
            selections.append(u.reg_read(UC_ARM_REG_R0))
        elif address == SINK:
            value = stored[selections[-1]].text + b'\0'
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(value))) == value
            assert state is None
            state = (pointer, u.reg_read(UC_ARM_REG_LR), tuple(sink_writes))
        elif state is not None:
            pointer, ret, prior_writes = state
            assert address == ret and u.reg_read(UC_ARM_REG_R0) == pointer
            assert tuple(sink_writes) == prior_writes
            discarded.append(dict(message_ID=selections[-1], pointer=pointer, return_address=ret))
            state = None
        if address == BASE + SETUP[1]:
            # The warning path jumps back to the next GUI event iteration.
            u.emu_stop()

    def write(_, access, address, size, value, data):
        if state is not None:
            sink_writes.append((address, size))

    cpu.hook_add(UC_HOOK_CODE, watched)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    try:
        cpu.emu_start(BASE + BRANCH[0], BASE + BRANCH[1], count=500_000)
    except UcError as error:
        raise RuntimeError((hex(cpu.reg_read(UC_ARM_REG_PC)), selections, fp, slot_flag, inputs,
                            warning_latch, list(recent))) from error
    terminal = cpu.reg_read(UC_ARM_REG_PC)
    assert terminal in (BASE + BRANCH[1], BASE + SETUP[1]) and state is None and not sink_writes
    assert len(discarded) == len(selections)
    assert (GETTER in provider.executed_current) == bool(selections)
    assert not provider.reads and not provider.opens
    return dict(offline_supplied_branch_inputs=[fp, slot_flag, inputs, warning_latch],
                loaded_ids=selections, immediate_no_write_returns=discarded,
                branch_end=terminal, exact_warm_block_input=block, warm_block_sha256=sha256(payload).hexdigest())


def verify_continue(release, font, evidence):
    folder = capture.ROOT / 'continue'
    paths = [folder / path for path in ('capture/capture_report.json', 'requests.json', 'terminal.json')]
    report, trace, terminal = map(base.load, paths)
    schedule, _, end, _, donor = capture.schedule('continue')
    assert report['ROM_sha256'] == terminal['ROM_sha256'] == release['candidate_sha256']
    assert report['frames'] == terminal['completed_frames'] == end
    assert report['scripted_input_schedule'] == schedule
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert [(row['PC'], row['message_ID']) for row in trace['source_requests']] == [
        (0x0205528C, 63), (0x020534F4, 63)]
    assert all(row['frame'] == 4811 for row in trace['source_requests'])
    evidence.update({str(path): base.digest(path) for path in paths})
    by_frame = shots(report)
    frames = {}
    for n in (2200, 2600, 3000, 3400, 3800, 5000):
        shot = by_frame[n]
        frames[n] = captured(shot)
        evidence[shot['path']] = shot['PNG_sha256']
    for n in (2200, 2600):
        panel = frames[n]
        assert not any(pixel == (0, 8, 0) for pixel in panel.crop((10, 290, 245, 350)).get_flattened_data())
    holds = [dict(frame=n, complete_glyph_mask_pixels=font_mask(
        frames[n], font, 'Load this data?', 16, 297, (10, 290, 245, 350), (0, 8, 0))) for n in (3000, 3400)]
    inn = font_mask(frames[5000], font, 'Welcome! Come in.', 22, 297, (16, 296, 232, 348), (0, 8, 0))
    return dict(scope='Ordinary Continue with an existing copied Lisbon save. Down and A still selected the populated Rafael slot.',
                displayed_confirmation=holds, original_lookups=trace['source_requests'],
                Lisbon_after_confirm_frame=3800, Lisbon_Inn_frame=5000, inn_complete_glyph_pixels=inn)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    runtime = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    assert sha256(runtime.arm).hexdigest() == release['target_ARM9_sha256']
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    arm = runtime.arm
    stored = owned_entries(runtime.common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    assert arm[SINK - BASE:SINK - BASE + 4] == clean_arm[SINK - BASE:SINK - BASE + 4] == bytes.fromhex('1eff2fe1')
    locks = (SETUP, BRANCH, (0xEDE38, 0xEDE4C), (0xEE078, 0xEE088), (0xEE674, 0xEE678))
    assert all(arm[lo:hi] == clean_arm[lo:hi] for lo, hi in locks)
    assert int.from_bytes(arm[0xEE674:0xEE678], 'little') == BASE + CONFIRM
    assert arm[CONFIRM:CONFIRM + 16] == b'Load this data?\0'
    evidence = {str(path): base.digest(path) for path in (current.RELEASE, Path(__file__), Path(capture.__file__))}

    controlled = [branch_execution(runtime, stored, *inputs) for inputs in (
        (0, 1, 0, 0), (0, 1, 2, 0), (0, 1, 2, 1), (1, 1, 2, 0))]
    assert [row['loaded_ids'] for row in controlled] == [[111], [112, 111], [112], []]
    observed = verify_continue(release, GameAsciiFont.from_arm9(arm), evidence)
    records = []
    for n, reason in ((111, 'The standalone sentence states that game data is absent and the game cannot load it.'),
                      (112, 'The distinct system-data notice names system data and describes its absence.')):
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
            clean_reference=reference(source[n]), current_reference=reference(stored[n]),
            clean_Japanese=source[n].text.decode('cp932'), current_English=stored[n].text.decode('cp932'),
            clean_hex=source[n].text.hex(), current_hex=stored[n].text.hex(), localization_note=reason,
            scope='Original code fetches the string and passes its pointer to an immediate no-op return.'))
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        records=records, native_fixture=runtime.receipt(), controlled_offline_cases=controlled,
        verified_code_spans=[dict(start=BASE + lo, end=BASE + hi, sha256=sha256(arm[lo:hi]).hexdigest()) for lo, hi in locks],
        sink=dict(address=SINK, instruction='bx lr', original_no_op=True),
        ordinary_gameplay=observed, visible_confirmation=dict(clean_file_offset=CONFIRM,
            clean_Japanese=clean_arm[CONFIRM:clean_arm.index(0, CONFIRM)].decode('cp932'),
            current_English='Load this data?', original_call=0x020EE07C),
        other_consumers='open', hardware=False, new_editorial_credit=0, evidence=evidence))
    print('Bound COMMON 111 and 112 to the silent native load paths and verified the independent Continue confirmation.')


if __name__ == '__main__':
    main()
