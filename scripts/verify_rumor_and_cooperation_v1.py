"""Verify the native cooperation portrait and the original town return."""

import argparse
import inspect
from hashlib import sha256
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts import replay_rumor_and_cooperation_v1 as refusal
from scripts import replay_rumor_and_cooperation_offer_v1 as offer
from scripts import stage_rumor_and_cooperation_v1 as stage
from scripts import verify_setup_save_equipment_v1 as precedent
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.record_navigation_v327 import dark_text
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.stage_shark_encounter_v1 import ROOT as SHARK
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_mutiny_release_inputs_v1 import portrait_ink
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
LIVE = ROOT / 'rumor_and_cooperation_gameplay_verification_v2.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/rumor_and_cooperation_repo_qa_20261111.xml')
PAPER = (16, 296, 244, 360)
FINAL = 9300


def run_data(root, proof, arm, fixture_builder, action):
    folder = root / 'cooperation_decline'
    term_path = folder / 'terminal.json'
    term = load(term_path)
    path = Path(term['report'])
    assert term['candidate_sha256'] == proof['research_ROM_sha256']
    assert term['report_sha256'] == digest(path)
    report, _ = checked_report(path, term['candidate_sha256'], FINAL)
    assert digest(refusal.previous.DONOR) == term['donor_sha256'] == report['battery_save_preloaded']['source_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert all(not value for key, value in report.items() if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snaps = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}

    def raw(frame):
        row = snaps[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    _, fixture = fixture_builder(arm, raw(3200), action)
    assert report['synthetic_condition_fixtures'] == [fixture | {'frame': 3200}]
    journal = folder / 'navigation_command_journal.json'
    actual_commands = load(journal)['commands_received']
    assert all(row['validation_passed'] for row in actual_commands)
    assert [row['command'] for row in actual_commands] == load(term['schedule'])
    return frames, raw, snaps, fixture, (path, term_path, journal)


def portrait_match(frame, number, frames, raw, snaps, arm, kanji, raster, font, proof):
    addr, dst = (struct.unpack_from('<I', arm, offset)[0] - stage.BASE for offset in (0x5444C, 0x54450))
    snapshot = raw(frame)
    plain, display = (snapshot[at:at + 256].split(b'\0', 1)[0] for at in (addr, dst))
    stored, = [row for row in proof['records'] if row['message_ID'] == number]
    template = bytes.fromhex(stored['stored_hex'])
    pattern = b'(.+?)'.join(re.escape(token) for token in template.split(b'%s'))
    match = re.fullmatch(pattern, plain)
    assert match, (frame, number, plain)
    arguments = tuple(value.decode('cp932') for value in match.groups())
    assert b' '.join(display.split()) == template % match.groups()
    plane, glyphs = render_portrait(raster, arm, kanji, display)
    ink = bytes(pixel == 1 for pixel in plane)
    assert ink == portrait_ink(frames[frame]['path'], PAPER)
    for native in proof['native_portrait_cases']:
        if native['message_ID'] == number and tuple(native['arguments']) == arguments:
            assert sha256(ink).hexdigest() == native['native_ink_sha256']
    count, bounds = complete_mask(font, 'Trader', captured(frames[frame]), 16, 277, (98, 97, 98))
    return dict(message_ID=number, original_arguments=arguments, capture=frames[frame], RAM=snaps[frame],
        lines=[line.strip() for line in display.decode('cp932').split('\n')], complete_glyphs=len(glyphs),
        original_formatted_bytes_hex=display.hex(), exact_live_ink_and_blank_margins=True,
        nameplate=dict(text='Trader', ink_pixels=count, bounds=bounds))


def cash_and_share(arm, raw, town_index, rival):
    cpu, get = get_machine(arm, raw)
    companies = get(0xCB160)
    faction = get(0x397D8, companies)
    town = get(0xCB178) + 4 + 108 * town_index
    result = dict(cash=get(0x3CCC8, companies + 4 + 76 * faction),
                  rival_share=get(0xB4AA8, town, rival), player_share=get(0xB4AA8, town, faction))
    assert bytes(cpu.mem_read(stage.BASE, len(raw))) == raw
    return result


def verify_refusal(proof, arm, kanji, raster, font):
    frames, raw, snaps, fixture, evidence = run_data(ROOT, proof, arm, refusal.set_condition, refusal.ACTION)
    reply = portrait_match(8500, 2805, frames, raw, snaps, arm, kanji, raster, font, proof)
    display = (
        (8100, 'In Istanbul, a broker for Pasha', (14, 292, 244, 318)),
        (8100, 'received the letter.', (14, 311, 244, 340)),
        (8900, 'Bribe failed.', (14, 292, 244, 318)),
        (9300, 'Stay 1 Day', (80, 258, 172, 290)),
    )
    transitions = [dict(capture=frames[frame], text=dark_text(font, text, captured(frames[frame]), box))
                   for frame, text, box in display]
    before = cash_and_share(arm, raw(8100), refusal.TOWN, refusal.RIVAL)
    after = cash_and_share(arm, raw(9300), refusal.TOWN, refusal.RIVAL)
    assert before == after and after['rival_share'] == 99
    return dict(original_refusal=reply, original_letter_notice_failure_and_inn_return=transitions,
                fee_and_shares_unchanged=after, fixture=fixture), evidence


def verify_offer(proof, arm, kanji, raster, font):
    frames, raw, snaps, fixture, evidence = run_data(offer.ROOT, proof, arm, offer.set_condition, offer.ACTION)
    fee = portrait_match(8500, 2802, frames, raw, snaps, arm, kanji, raster, font, proof)
    refusal_reply = portrait_match(8900, 2803, frames, raw, snaps, arm, kanji, raster, font, proof)
    amount, = fee['original_arguments']
    assert amount == '９７５２'
    before = cash_and_share(arm, raw(8100), offer.TOWN, offer.RIVAL)
    after = cash_and_share(arm, raw(9300), offer.TOWN, offer.RIVAL)
    assert before == after and after['rival_share'] == 100 and after['cash'] < int(amount)
    display = (
        (8100, 'In London, a broker for Clifford', (14, 292, 244, 318)),
        (8100, 'received the letter.', (14, 311, 244, 340)),
        (9300, 'Stay 1 Day', (80, 258, 172, 290)),
    )
    transitions = [dict(capture=frames[frame], text=dark_text(font, text, captured(frames[frame]), box))
                   for frame, text, box in display]
    return dict(original_fee=fee, original_insufficient_funds_reply=refusal_reply,
                original_letter_notice_and_inn_return=transitions, gold_fee=int(amount),
                fee_and_shares_unchanged=after, fixture=fixture), evidence


def verify_live():
    proof = load(PROOF)
    assert digest(ROM) == proof['research_ROM_sha256']
    image = NdsImage.open(ROM)
    arm = image.read_file(stage.ARM)
    kanji = image.read_file('/GRP/KANJI.FNT')
    raster, _, _ = font_tools(image)
    font = GameAsciiFont.from_arm9(arm)
    refused, refusal_evidence = verify_refusal(proof, arm, kanji, raster, font)
    quoted, offer_evidence = verify_offer(proof, arm, kanji, raster, font)
    save(LIVE, dict(candidate_sha256=digest(ROM), observed_ids=[2802, 2803, 2805],
        refusal=refused, fee_quote=quoted, hardware=False,
        evidence={str(path): digest(path) for path in (PROOF, *refusal_evidence, *offer_evidence, Path(__file__))}))
    print('The original broker notices, trader refusal, mixed-font fee and insufficient-funds path passed.')


def verify_startup():
    source = checked_text(inspect.getsource(precedent.verify_startup), {
        "parent_path = BIOGRAPHIES / 'own_startup/capture/capture_report.json'":
            "parent_path = SHARK / 'own_startup/capture/capture_report.json'",
        "prior_proof = BIOGRAPHIES / 'own_startup_verification.json'":
            "prior_proof = SHARK / 'own_startup_verification.json'",
    })
    env = {**vars(precedent), **globals()}
    exec(compile(source, __file__ + '::same-cold-boot-and-name-contract', 'exec'), env)
    env['verify_startup']()


def approve(viewed):
    proof, live, startup = map(load, (PROOF, LIVE, BOOT))
    assert viewed == [sheet['sha256'] for sheet in proof['sheets']]
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in proof['sheets'])
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == startup['candidate_sha256'] == digest(ROM)
    suites = list(ET.parse(QA).getroot().iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 30
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    save(CHECKPOINT, dict(candidate_sha256=digest(ROM), approved_for_registered_successor=True,
        observed_ids=live['observed_ids'], stored_records=len(proof['records']),
        viewed_pages=sum(len(sheet['messages']) for sheet in proof['sheets']),
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
