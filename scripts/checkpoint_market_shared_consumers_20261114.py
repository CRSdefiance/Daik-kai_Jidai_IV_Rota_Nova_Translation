"""Seal exact current and clean text ownership for the observed Lisbon Trade paths."""

from hashlib import sha256
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_legacy_common_35_v1 as legacy
from scripts import observe_market_restart_common_20261114 as capture
from scripts.review_sound_bgm_titles_v1 import reference


base, current = capture.base, capture.current
COMMON, ARM = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
OUTPUT = legacy.OUTPUT.with_name('market_trade_observed_consumers_20261114_v1.json')
PATHS = {
    'back': (8,),
    'finish': (8, 14),
    'confirm': (8, 14, 9),
}
DECISIONS = {
    8: ('The trader opens by asking if the customer needs anything.',
        'The short greeting fits an ordinary opening. The replays recorded the request and then showed the Market menu.'),
    14: ('The crew member checks that the proposed trade is acceptable.',
         'The brief question keeps the player in control and reads naturally over the pending purchase and Yes/No controls.'),
    9: ('After the player confirms the purchase, the trader thanks them and invites them to return.',
        'The two short clauses communicate thanks and future business in the trader’s normal farewell.'),
}


def font_mask(image, font, text, x, y, box, color):
    wanted = {(x + 6 * index + dx, y + dy) for index, char in enumerate(text)
              for glyph in (font.decode(char),)
              for dx in range(6) for dy in range(11) if glyph.getpixel((dx, dy))}
    left, top, right, bottom = box
    found = {(u, v) for u in range(left, right) for v in range(top, bottom)
             if image.getpixel((u, v)) == color}
    assert wanted and wanted == found, (text, box, len(wanted), len(found))
    return len(found)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    clean_path = current.parent.stage.CLEAN
    assert base.digest(clean_path) == release['clean_input_sha256']
    clean, rom = map(base.NdsImage.open, (clean_path, current.ROM))
    source_arm, arm = clean.read_file(ARM), rom.read_file(ARM)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(rom.read_file(COMMON)).hexdigest() == release['target_COMMON_sha256']
    source = common_message_entries(clean.read_file(COMMON), source_arm)
    stored = owned_entries(rom.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in DECISIONS)
    assert all(f'COMMON_MESSAGE_{n}' not in credited for n in capture.FOCUS)
    evidence = {str(path): base.digest(path) for path in (legacy.OUTPUT, current.RELEASE, capture.PLAN, Path(__file__))}
    observations, captures = {}, {}
    for case, ids in PATHS.items():
        folder = capture.ROOT / case
        terminal, requests = [folder / name for name in ('terminal.json', 'requests.json')]
        data, trace = map(base.load, (terminal, requests))
        events, frames, end, _, donor = capture.schedule(case)
        report_path = folder / 'capture/capture_report.json'
        report = base.load(report_path)
        assert data['completed_frames'] == end == report['frames']
        assert data['ROM_sha256'] == report['ROM_sha256'] == release['candidate_sha256']
        assert report['scripted_input_schedule'] == events
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
        assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
        rows = trace['source_requests']
        assert len(rows) == data['COMMON_requests'] == 2 * len(ids) and not data['target_COMMON_calls']
        for n, direct, copy in zip(ids, rows[::2], rows[1::2], strict=True):
            assert [direct['PC'], copy['PC']] == [0x0205528C, 0x020534F4]
            assert direct['message_ID'] == copy['message_ID'] == n
            assert direct['frame'] == copy['frame']
            assert direct['caller_LR'] == copy['caller_LR'] == (0x02053D10 if n == 14 else 0x02053FF8)
        observations[case] = rows
        captures[case] = {row['frame']: row for row in report['frames_captured'] if row['frame'] in frames}
        evidence.update({str(path): base.digest(path) for path in (terminal, requests, report_path)})

    def screen(case, frame):
        row = captures[case][frame]
        path = row['path']
        assert base.digest(path) == row['PNG_sha256']
        evidence[path] = row['PNG_sha256']
        with Image.open(path) as opened:
            assert opened.size == (256, 384)
            return opened.convert('RGB')

    font = GameAsciiFont.from_arm9(arm)
    displayed = {}
    for n, case, frame in ((14, 'finish', 11881), (9, 'confirm', 12281)):
        text = stored[n].text.decode('ascii')
        mask = font_mask(screen(case, frame), font, text, 22, 297, (16, 296, 232, 348), (0, 8, 0))
        displayed[n] = dict(frame=frame, case=case, complete_glyph_mask_pixels=mask)
    for case, frame in (('back', 11881), ('finish', 12281), ('confirm', 11600), ('confirm', 12681)):
        screen(case, frame)
    no_change_before_trade = screen('back', 9600).crop((86, 345, 130, 356))
    after_back = screen('back', 11881).crop((86, 345, 130, 356))
    after_confirm = screen('confirm', 12681).crop((86, 345, 130, 356))
    assert no_change_before_trade.tobytes() == after_back.tobytes()
    assert no_change_before_trade.tobytes() != after_confirm.tobytes()

    def compare(n):
        return dict(message_ID=n, id=f'COMMON_MESSAGE_{n}', file_path=COMMON,
            clean_reference=reference(source[n]), current_reference=reference(stored[n]),
            clean_Japanese=source[n].text.decode('cp932'), current_English=stored[n].text.decode('cp932'),
            clean_hex=source[n].text.hex(), current_hex=stored[n].text.hex())

    retained = [compare(n) | dict(source_meaning=meaning, rationale=reason, existing_credit=True,
        distinct_actual_requests=sum(n == row['message_ID'] for rows in observations.values() for row in rows) // 2,
        display=displayed.get(n)) for n, (meaning, reason) in DECISIONS.items()]
    pending = [compare(n) | dict(observed_requests=0, status='original consumer remains open')
               for n in sorted(capture.FOCUS)]
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'],
        clean_sha256=release['clean_input_sha256'], observation=observations, retained=retained,
        pending=pending, observed_scope='One pending Lisbon purchase, direct back, No and Yes from Finish.',
        controller_and_touch_only=True, observed_hardware=False, new_editorial_credit=0, evidence=evidence))
    print('Verified Lisbon back, No and Yes, two complete dialogue masks and three pending source keys.')


if __name__ == '__main__':
    main()
