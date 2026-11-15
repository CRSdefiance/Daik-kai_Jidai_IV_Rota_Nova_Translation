"""Bind the actual Istanbul shop lines to their exact clean and registered entries."""

from hashlib import sha256
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_istanbul_shared_text_20261114 as capture
from scripts.checkpoint_market_shared_consumers_20261114 import ARM, COMMON, font_mask
from scripts.review_sound_bgm_titles_v1 import reference


base, current = capture.base, capture.current
OUTPUT = capture.LEGACY.with_name('istanbul_shop_observed_consumers_20261114_v1.json')
DECISIONS = {
    717: (4881, 'The Ottoman Empire controls the eastern Mediterranean.',
          'The shopkeeper answers with a matter-of-fact regional report. “Rules” preserves control without extending it to the whole Mediterranean.',
          ('The Ottoman Empire rules the', 'eastern Mediterranean.')),
    656: (5181, 'The shop specializes in retail sales.',
          'Keep the shopkeeper’s short explanation of how this shop sells goods. The nearby bulk-trade reply names the appropriate place.',
          ('We only sell retail.',)),
    657: (5581, 'The shopkeeper recognizes the visitor as a sailor and directs them to the trade house for transactions in quantity.',
          'The friendly tag and practical referral carry the whole exchange. The tag stays on the first line and “bulk trade” starts the second.',
          ("You're a sailor, aren't you? For", 'bulk trade, try the trade house.')),
    658: (5881, 'Business has been middling, and the shopkeeper hopes for a good opportunity.',
          'The conversational question and understated answer suit casual small talk. The second sentence keeps the deal a hope.',
          ("Business? Oh, it's been all right.", "I'm hoping a good deal comes along.")),
}


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    clean_path = current.parent.stage.CLEAN
    assert base.digest(clean_path) == release['clean_input_sha256']
    clean, rom = map(base.NdsImage.open, (clean_path, current.ROM))
    arm = rom.read_file(ARM)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(rom.read_file(COMMON)).hexdigest() == release['target_COMMON_sha256']
    originals = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    current_text = owned_entries(rom.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    folder = capture.ROOT / 'istanbul'
    report_path, terminal, requests = (folder / name for name in (
        'capture/capture_report.json', 'terminal.json', 'requests.json',
    ))
    report, summary, trace = map(base.load, (report_path, terminal, requests))
    events, frames, end, _, donor = capture.schedule('istanbul')
    assert report['ROM_sha256'] == summary['ROM_sha256'] == release['candidate_sha256']
    assert report['frames'] == summary['completed_frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == events
    assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert not summary['target_COMMON_calls'] and summary['COMMON_requests'] == 8
    frame_rows = {row['frame']: row for row in report['frames_captured'] if row['frame'] in frames}
    calls = trace['source_requests']
    assert len(calls) == 2 * len(DECISIONS)
    ledger = base.load(base.LEDGER)
    credits = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    evidence = {str(path): base.digest(path) for path in (
        report_path, terminal, requests, current.RELEASE, capture.PLAN, Path(capture.__file__), Path(__file__),
    )}
    font = GameAsciiFont.from_arm9(arm)
    observed = []
    for (number, (frame, meaning, reason, lines)), lookup, copy in zip(DECISIONS.items(), calls[::2], calls[1::2], strict=True):
        assert lookup['message_ID'] == copy['message_ID'] == number
        assert [lookup['PC'], copy['PC']] == [0x0205528C, 0x020534F4]
        assert lookup['frame'] == copy['frame'] < frame
        assert frame - lookup['frame'] < 100
        row = frame_rows[frame]
        assert base.digest(row['path']) == row['PNG_sha256']
        evidence[row['path']] = row['PNG_sha256']
        en, ja = current_text[number], originals[number]
        assert ' '.join(en.text.decode('ascii').split()) == ' '.join(lines)
        ident = f'COMMON_MESSAGE_{number}'
        assert ident in credits
        with Image.open(row['path']) as screenshot:
            image = screenshot.convert('RGB')
        masks = []
        for row_index, text in enumerate(lines):
            top = 296 + 16 * row_index
            masks.append(font_mask(image, font, text, 22, top + 1, (16, top, 232, top + 16), (0, 8, 0)))
        assert all(image.getpixel((x, y)) != (0, 8, 0)
                   for x in range(16, 232) for y in range(296 + 16 * len(lines), 353))
        observed.append(dict(id=ident, file_path=COMMON, clean_reference=reference(ja),
            current_reference=reference(en), clean_hex=ja.text.hex(), current_hex=en.text.hex(),
            Japanese=ja.text.decode('cp932'), English=en.text.decode('ascii'), source_meaning=meaning,
            rationale=reason, decision='retention', review=dict.fromkeys(
                ('source', 'context', 'localization', 'naturalness', 'formatting'), True),
            original_requests=[lookup, copy], frame=row, complete_line_masks=masks))
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        context='Ordinary Istanbul square shop visits from a copied existing save.',
        observed_shop_dialogue=observed, pending_keys_observed=[], hardware=False, new_dialogue_credit=0,
        evidence=evidence))
    print('Verified all four Istanbul shop lines against complete displayed line masks and the clean source.')


if __name__ == '__main__':
    main()
