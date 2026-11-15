"""Verify original equipment navigation, retained dialogs and candidate startup."""

import argparse
from hashlib import sha256
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.equipment_removal_wrap_v1 import EQUIPMENT_PARAGRAPH, HOOK, NOTICE_PARENT, PRIOR
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_machine_scoped_v764 import machine
from scripts.replay_setup_save_equipment_v2 import ROOT as BASELINE
from scripts.stage_captain_biographies_v2 import ROOT as BIOGRAPHIES
from scripts.stage_setup_save_equipment_v1 import ARM, PROOF, ROM, ROOT
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


LIVE = ROOT / 'equipment_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/setup_save_equipment_repo_qa_20261111.xml')
PAPER = (16, 296, 244, 344)


def selector_cases(arm):
    cpu = machine(arm)
    results = []
    for parent, n in ((NOTICE_PARENT, 329), (NOTICE_PARENT, 328), (NOTICE_PARENT, 330),
                      (NOTICE_PARENT, 321), (NOTICE_PARENT, 327), (0x0205469C, 329),
                      (0x02054764, 329), (0x020546E4, 329)):
        target, values = dispatch(cpu, HOOK, {0xC4: parent, 0xD0: n}, (PRIOR, EQUIPMENT_PARAGRAPH))
        assert target == (EQUIPMENT_PARAGRAPH if (parent, n) == (NOTICE_PARENT, 329) else PRIOR)
        assert values[:3] == ARGS[:3]
        results.append(dict(parent=parent, message_ID=n, first_continuation=target))
    return results


def modal_mask(image, proof, number):
    rendered = [row for row in proof['rendered_variants'] if row['message_ID'] == number
                and row['arguments'] == ['Rafael Castor', 'Travels of Marco Polo']]
    row, = rendered
    ink = bytes(pixel == (0, 8, 0) for pixel in image.crop(PAPER).get_flattened_data())
    assert sha256(ink).hexdigest() == row['native_ink_sha256']
    return dict(lines=row['lines'], crop=PAPER, ink_pixels=ink.count(1), exact_ink_and_background=True)


def verify_live():
    proof = load(PROOF)
    old_report = BASELINE / 'equipment/capture/capture_report.json'
    new_report = ROOT / 'equipment/capture/capture_report.json'
    old, new = map(load, (old_report, new_report))
    assert old['ROM_sha256'] == proof['registered_input']['candidate_sha256'] and old['frames'] == 10800
    assert new['ROM_sha256'] == proof['research_ROM_sha256'] and new['frames'] == 12810
    assert all(run['cold_boot'] and not run['savestate_loaded'] and not run['callback_errors'] for run in (old, new))
    assert digest(ROM) == proof['research_ROM_sha256']
    terminal = ROOT / 'equipment/terminal.json'
    trace = load(terminal)
    assert all(digest(path) == expected for path, expected in trace['evidence'].items())
    requests = trace['target_requests']
    assert {row['message_ID'] for row in requests} == {320, 321, 329}
    assert any(row['message_ID'] == 320 and row['caller_LR'] == 0x0204C3A8 for row in requests)
    assert 11601 <= min(row['frame'] for row in requests if row['message_ID'] == 329) <= 12000
    assert old['core_options'] == new['core_options']
    assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
    assert not any(value for key, value in new.items() if key.startswith('synthetic_'))
    old_shots, new_shots = shots(old), shots(new)
    before, after = captured(old_shots[10400]), captured(new_shots[10400])
    changes = ImageChops.difference(before, after).getbbox()
    assert changes and changes[1] >= 207 and changes[3] <= 231
    arm = NdsImage.open(ROM).read_file(ARM)
    font = GameAsciiFont.from_arm9(arm)
    chooser = find_mask(font, 'Who should equip it?', after, (8, 208, 252, 231))
    assert old_shots[10800]['framebuffer_sha256'] == new_shots[10800]['framebuffer_sha256']
    equipped = modal_mask(captured(new_shots[10800]), proof, 321)
    removed = modal_mask(captured(new_shots[12000]), proof, 329)
    inventory = captured(new_shots[12400])
    assert inventory.tobytes() != captured(new_shots[12000]).tobytes()
    assert inventory.tobytes() == captured(new_shots[10000]).tobytes()
    assert new_shots[12800]['framebuffer_sha256'] != new_shots[12400]['framebuffer_sha256']
    save(LIVE, dict(candidate_sha256=digest(ROM), observed_ids=[320, 321, 329],
        original_chooser=chooser | dict(capture=new_shots[10400], changed_bounds=changes),
        equipped=equipped | dict(capture=new_shots[10800], exact_parent_frame=True),
        removed=removed | dict(capture=new_shots[12000], inventory_restored=new_shots[12400], back=new_shots[12800]),
        selector_positive_and_negative_cases=selector_cases(arm), request_trace=requests,
        original_controller_and_stylus_only=True, original_saved_game_copied=True, hardware=False,
        evidence={str(path): digest(path) for path in (old_report, new_report, terminal, PROOF, Path(__file__))}))
    print('The original equipment chooser, equip result, removal result and menu return all passed.')


def verify_startup():
    proof = load(PROOF)
    path = ROOT / 'own_startup/capture/capture_report.json'
    parent_path = BIOGRAPHIES / 'own_startup/capture/capture_report.json'
    term = load(ROOT / 'own_startup/terminal.json')
    assert term['candidate_sha256'] == digest(ROM) and term['report_sha256'] == digest(path)
    current, raw = checked_report(path, digest(ROM), 31000)
    parent, _ = checked_report(parent_path, proof['registered_input']['candidate_sha256'], 31000)
    assert current['core_options'] == parent['core_options']
    assert current['scripted_input_schedule'] == parent['scripted_input_schedule']
    old, new = shots(parent), shots(current)
    frames = (1600, 2200, 3340, 4000, 16000, 31000)
    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in frames)
    arm = NdsImage.open(ROM).read_file(ARM)
    assert raw[DIRECTORY_OFFSET:TABLE_END] == arm[DIRECTORY_OFFSET:TABLE_END]
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == 3
    prior_proof = BIOGRAPHIES / 'own_startup_verification.json'
    name_rows = load('work/ship_command_label_release_v1/own_registered_name_getters_v1.json')['own_name_consumers']['rows']
    names = []
    assert len(name_rows) == 24
    for row in name_rows:
        value = bytes.fromhex(row['text_hex'])
        ptr = get(row['getter'] - BASE, row['actor_object'])
        assert bytes(cpu.mem_read(ptr, len(value) + 1)) == value + b'\0'
        names.append({key: row[key] for key in ('actor_ID', 'consumer', 'getter', 'text', 'text_hex')})
    assert names == load(prior_proof)['original_protected_name_getters']
    save(BOOT, dict(candidate_sha256=digest(ROM), frames=31000, cold_boot=True, savestate=False,
        exact_matching_frames=[new[n] for n in frames], complete_deployed_payload_exact=True,
        original_protected_name_getters=names, actual_captain_getter=3,
        read_only_snapshot=current['read_only_RAM_snapshot'],
        evidence={str(p): digest(p) for p in (path, parent_path, prior_proof, Path(__file__))}))
    print('Candidate startup matched all six holds and 24 protected name getters.')


def approve(viewed):
    proof, live, startup = map(load, (PROOF, LIVE, BOOT))
    assert viewed == [sheet['sha256'] for sheet in proof['sheets']]
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in proof['sheets'])
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == startup['candidate_sha256'] == digest(ROM)
    save(CHECKPOINT, dict(candidate_sha256=digest(ROM), approved_for_registered_successor=True,
        observed_ids=live['observed_ids'], stored_records=len(proof['records']),
        viewed_pages=sum(sheet['pages'] for sheet in proof['sheets']),
        evidence={str(path): digest(path) for path in (PROOF, LIVE, BOOT, QA, Path(__file__))}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    elif args.action == 'live':
        verify_live()
    else:
        verify_startup()
