"""Verify the original chooser's complete glyphs and unchanged selection flow."""

import argparse
from collections import Counter
from hashlib import sha256
from pathlib import Path
import struct

from ndspy.code import MainCodeFile
from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1,
    UC_ARM_REG_R4, UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END
from scripts import stage_captain_biographies_v2 as stage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.stage_captain_biographies_v1 import ARM, BASE, CALLER, INVENTORY, STATES, STORAGE, TABLE
from scripts.verify_personal_gameplay_v841 import get_machine

ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
LIVE = ROOT / 'captain_chooser_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/captain_biographies_repo_qa_exact_20261111.xml')
SHEET = ROOT / 'captain_biographies_contact.png'
BAND = (0, 330, 256, 366)
INK = (230, 230, 230)


def shots(report):
    return {frame['frame']: frame for frame in report['frames_captured']}


def captured(shot):
    assert digest(shot['path']) == shot['PNG_sha256']
    with Image.open(shot['path']) as image:
        return image.convert('RGB')


def mask(font, rows, image):
    assert image.size == (256, 384)
    plane = Image.new('1', (256, BAND[3] - BAND[1]))
    bounds = []
    for index, row in enumerate(rows):
        x, y = 17, index * 12
        for character in row:
            plane.paste(font.decode(character), (x, y))
            x += 6
        assert x <= 251 and y + 11 <= plane.height
        bounds.append([17, BAND[1] + y, x, BAND[1] + y + 11])
    expected = bytes(bool(value) for value in plane.get_flattened_data())
    actual = bytes(pixel == INK for pixel in image.crop(BAND).get_flattened_data())
    assert actual == expected
    return dict(ink_mask_sha256=sha256(actual).hexdigest(), ink_pixels=actual.count(1), bounds=bounds,
                complete_first_last_and_blank_cells=True)


def changed_only_in_biography(before, after):
    change = ImageChops.difference(before, after).getbbox()
    assert change and change[1] >= BAND[1] and change[3] <= BAND[3]
    return list(change)


def native_selector(arm, raw, row):
    cpu, _ = get_machine(arm, raw)
    view, model, stack = 0x023F7000, 0x023F7100, 0x023F7200
    cpu.mem_write(view + 0x54, struct.pack('<I', model))
    cpu.mem_write(model + 4, struct.pack('<I', row['chooser_index']))
    cpu.reg_write(UC_ARM_REG_R4, view)
    cpu.reg_write(UC_ARM_REG_SP, stack)
    start, renderer = BASE + CALLER[0], 0x020D5404
    cpu.emu_start(start, renderer, count=8)
    ref = row['staged_reference']
    pointer = cpu.reg_read(UC_ARM_REG_R1)
    assert cpu.reg_read(UC_ARM_REG_PC) == renderer and cpu.reg_read(UC_ARM_REG_LR) == 0x0209E758
    assert cpu.reg_read(UC_ARM_REG_R0) == cpu.reg_read(UC_ARM_REG_SP) == stack
    assert pointer == ref['runtime_address']
    assert bytes(cpu.mem_read(pointer, ref['byte_count'])).hex() == ref['exact_hex']
    return dict(native_selection_index=row['chooser_index'], selected_address=pointer, renderer=renderer,
                cloned_selector_with_initialized_view_fields=True)


def verify_live():
    staged = load(PROOF)
    parent_path = stage.previous.ROOT / 'parent/capture/capture_report.json'
    candidate_path = ROOT / 'candidate/capture/capture_report.json'
    failed_path = stage.previous.ROOT / 'candidate/capture/capture_report.json'
    assert staged['research_ROM_sha256'] == digest(ROM)
    parent, _ = checked_report(parent_path, staged['registered_input']['candidate_sha256'], 5550)
    candidate, _ = checked_report(candidate_path, digest(ROM), 5550)
    failed, _ = checked_report(failed_path, load(stage.previous.PROOF)['research_ROM_sha256'], 5550)
    for key in ('core_DLL_sha256', 'core_options', 'scripted_input_schedule'):
        assert parent[key] == candidate[key] == failed[key]
    for report in (parent, candidate, failed):
        assert len(report['synthetic_gallery_fixtures']) == 1
        assert not any(value for key, value in report.items()
                       if key.startswith('synthetic_') and key != 'synthetic_gallery_fixtures')
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and digest(donor['source']) == donor['source_sha256']
    old, new, broken = map(shots, (parent, candidate, failed))
    assert all(old[frame]['framebuffer_sha256'] == new[frame]['framebuffer_sha256'] for frame in (2200, 5500))
    assert any(action['start'] == 5201 and action['buttons'] == ['B']
               for action in candidate['scripted_input_schedule'])
    arm = NdsImage.open(ROM).read_file(ARM)
    parent_arm = NdsImage.open(staged['registered_input']['candidate']).read_file(ARM)
    font = GameAsciiFont.from_arm9(arm)
    assert font.glyphs == GameAsciiFont.from_arm9(parent_arm).glyphs
    snapshots = {row['frame']: row for row in candidate['read_only_capture_RAM_snapshots']}
    evidence = []
    sheet = Image.new('RGB', (512, 4 * 132), (20, 25, 32))
    title = ImageDraw.Draw(sheet)
    owners = []
    rejected = []
    for frame, index in STATES:
        record = staged['records'][index]
        current = captured(new[frame])
        verified = mask(font, record['staged_rows'], current)
        previous = captured(old[frame])
        change = changed_only_in_biography(previous, current)
        snapshot = snapshots[frame]
        assert snapshot['read_only_export'] and digest(snapshot['path']) == snapshot['sha256']
        raw = Path(snapshot['path']).read_bytes()
        assert raw[TABLE:TABLE + 16] == arm[TABLE:TABLE + 16]
        assert raw[STORAGE[0]:STORAGE[1]] == arm[STORAGE[0]:STORAGE[1]]
        assert raw[CALLER[0]:CALLER[1]] == arm[CALLER[0]:CALLER[1]]
        if index not in {row['native_selection_index'] for row in owners}:
            owners.append(native_selector(arm, raw, record))
            crop = current.crop((0, 324, 256, 379)).resize((512, 110), Image.Resampling.NEAREST)
            title.text((12, index * 132 + 5), record['actor'], fill='white')
            sheet.paste(crop, (0, index * 132 + 22))
            if index < 3:
                try:
                    mask(font, record['staged_rows'], captured(broken[frame]))
                except AssertionError:
                    rejected.append(record['actor'])
        evidence.append(dict(actor=record['actor'], frame=frame, glyphs=verified,
            candidate_capture=new[frame], predecessor_capture=old[frame], changed_bounds=change, live_RAM=snapshot))
    assert len(owners) == 4 and rejected == ['Rafael', 'Hodram', 'Lil']
    visits = Counter(entry['actor'] for entry in evidence)
    assert visits == {'Rafael': 2, 'Hodram': 2, 'Lil': 2, 'Maria': 1}
    for actor in visits:
        assert len({entry['glyphs']['ink_mask_sha256'] for entry in evidence if entry['actor'] == actor}) == 1
    sheet.save(SHEET)
    save(LIVE, dict(candidate_sha256=digest(ROM), live_captains=list(visits), live_cases=evidence,
        controller_only_with_existing_unlock=True, reverse_switch_verified=True, back_return=new[5500],
        native_selections=owners, bare_LF_negative_controls_rejected=rejected,
        contact_sheet=dict(path=str(SHEET), sha256=digest(SHEET), pages=4), hardware=False,
        evidence={str(path): digest(path) for path in (PROOF, INVENTORY, parent_path, candidate_path, failed_path, Path(__file__))}))
    print('Seven original chooser selections and Back passed. Complete glyphs and margins match on all four biographies.')


def verify_startup():
    staged, live = map(load, (PROOF, LIVE))
    candidate_sha = digest(ROM)
    assert staged['research_ROM_sha256'] == live['candidate_sha256'] == candidate_sha
    path = ROOT / 'own_startup/capture/capture_report.json'
    old_path = stage.PRIOR / 'capture/capture_report.json'
    term = load(ROOT / 'own_startup/terminal.json')
    assert term['candidate_sha256'] == candidate_sha and term['report_sha256'] == digest(path)
    candidate, raw = checked_report(path, candidate_sha, 31000)
    previous, _ = checked_report(old_path, staged['registered_input']['candidate_sha256'], 31000)
    assert candidate['core_options'] == previous['core_options']
    assert candidate['scripted_input_schedule'] == previous['scripted_input_schedule']
    old, new = shots(previous), shots(candidate)
    exact_frames = (1600, 2200, 4000, 16000, 31000)
    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in exact_frames)
    arm = NdsImage.open(ROM).read_file(ARM)
    maria = captured(new[3340])
    proof = mask(GameAsciiFont.from_arm9(arm), staged['records'][3]['staged_rows'], maria)
    proof['changed_bounds'] = changed_only_in_biography(captured(old[3340]), maria)
    assert raw[DIRECTORY_OFFSET:TABLE_END] == arm[DIRECTORY_OFFSET:TABLE_END]
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == 3
    prior_getters = Path('work/ship_command_label_release_v1/own_registered_name_getters_v1.json')
    name_rows = load(prior_getters)['own_name_consumers']['rows']
    assert len(name_rows) == 24 and len({row['actor_ID'] for row in name_rows}) == 12
    names = []
    for row in name_rows:
        expected = bytes.fromhex(row['text_hex'])
        ptr = get(row['getter'] - BASE, row['actor_object'])
        assert bytes(cpu.mem_read(ptr, len(expected) + 1)) == expected + b'\0'
        names.append({key: row[key] for key in ('actor_ID', 'consumer', 'getter', 'text', 'text_hex')})
    save(BOOT, dict(candidate_sha256=candidate_sha, frames=31000, cold_boot=True, savestate=False,
        exact_matching_frames=[new[n] for n in exact_frames], changed_Maria_chooser=dict(capture=new[3340], **proof),
        complete_deployed_payload_exact=True, actual_captain_getter=3, original_protected_name_getters=names,
        read_only_snapshot=candidate['read_only_RAM_snapshot'], existing_system_unlock_fixture=candidate['synthetic_gallery_fixtures'],
        evidence={str(path): digest(path) for path in (path, old_path, prior_getters, Path(__file__))}))
    print('Candidate cold boot passed through Hangzhou. Five frame holds and 24 protected name getters passed.')


def approve(viewed):
    live, boot = map(load, (LIVE, BOOT))
    assert viewed == live['contact_sheet']['sha256'] == digest(SHEET)
    assert live['candidate_sha256'] == boot['candidate_sha256'] == digest(ROM)
    assert all(digest(path) == sha for proof in (live, boot) for path, sha in proof['evidence'].items())
    assert not CHECKPOINT.exists()
    save(CHECKPOINT, dict(candidate_sha256=digest(ROM), approved_for_registered_successor=True,
        live_captains=live['live_captains'], stored_cases=4, viewed_pages=4,
        evidence={str(path): digest(path) for path in (PROOF, INVENTORY, BOOT, LIVE, QA, SHEET, Path(__file__))}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheet-sha256')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheet_sha256)
    elif args.action == 'live':
        verify_live()
    else:
        verify_startup()
