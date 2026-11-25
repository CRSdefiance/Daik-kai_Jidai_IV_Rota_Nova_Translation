"""Review the shared exchanges witnessed on Rafael's recorded return to Lisbon."""

from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_rafael_lisbon_return_20261119 as replay
from scripts import register_rafael_trade_and_arms_20261119 as latest
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.stage_town_shortage_20261119 import PENDING

base, native = latest.base, latest.native
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/lisbon_return_shared_20261119_v2.json')
COMMON = '/COMMON/MESFILE.DK4'
RUMOR = ("It's supposed to be a twisted horn. Some say it came from a dragon. "
         'Word is, you can turn it into medicine that cures any illness.')
DECISIONS = {
    62: (56260, 'Guildmaster', 'Need something?', 'The familiar greeting invites Rafael to state his business before the Guild menu.'),
    67: (55540, 'Sailor', 'Shall we dock at Lisbon?', 'The simple question suits the Sailor and the Yes/No decision. It preserves the substituted town.'),
    97: (54345, 'System', 'Rafael leveled up!', 'The short notice names the recipient and uses standard game language for the increase.'),
    297: (53655, 'System', 'Discovered Seville.', 'The map notice follows the sighting and identifies the precise substitution.'),
    397: (55282, 'Sailor', 'Admiral, it looks like the sailors have scurvy!', 'Keep the rough report, the address and the source’s uncertainty about the illness.'),
    426: (53165, 'Sailor', 'Damn, fog is rolling in.', 'The mild swear conveys the rough Japanese ending and the verb conveys the fog’s approach.'),
    633: (51905, 'Sailor', "Trouble is, we've got no Surveyor.", 'The informal phrasing matches the Sailor. Surveyor matches the actual job label and distinguishes it from the equipped Sextant.'),
    1071: (57220, 'Guildmaster', 'Which one would you like?', 'A natural prompt before the corresponding item list.'),
    1293: (53415, 'Sailor', "Admiral, we've got a town in sight!", 'The lookout reports a sighting before the game identifies Seville.'),
    2903: (57460, 'Item description', 'Completed in the 13th century, this book tells what Marco Polo saw and heard on his travels in the East.',
           'Keep the date, attribution, and account of observations exactly as localized from the item source.'),
    2940: (58660, 'Item description', 'A navigation tool for pinpointing your position at sea.',
           'The equipped Sextant description preserves its original navigational function and reads naturally.'),
    3665: (56980, 'Guildmaster', "They say it's a twisted horn. Some say it's a dragon's. I hear it can be made into medicine for any illness.",
           'The live final row contains only “illness.” Keep both uncertain claims distinct and let the cure finish as a full phrase.'),
}


def main():
    assert not OUTPUT.exists()
    report, trace, joint, prefix, release = map(base.load, (
        replay.CAPTURE / 'capture_report.json', replay.ROOT / 'observer/commands.json',
        replay.CAPTURE / 'navigation_command_journal.json', replay.PREFIX, latest.RELEASE))
    active_hash = base.digest(replay.active.ROM)
    assert active_hash == report['ROM_sha256'] == joint['ROM_sha256'] == prefix['ROM_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert report['frames'] == joint['last_command_frame'] == 59380
    assert joint['commands_received'][-1]['command'] == {'stop': True}
    tail = []
    for event in joint['commands_received']:
        cmd = event['command']
        assert event['validation_passed']
        if cmd.get('buttons') or cmd.get('touch'):
            entry = dict(start=event['frame']+1, duration=cmd['duration'], buttons=cmd['buttons'])
            if 'touch' in cmd:
                entry['touch'] = cmd['touch']
            tail.append(entry)
    assert report['scripted_input_schedule'] == prefix['scripted_input_schedule'] + tail
    assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert base.digest(latest.ROM) == release['candidate_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    clean, observed, current = map(base.NdsImage.open, (native.CLEAN, replay.active.ROM, latest.ROM))
    stock_arm, replay_arm, registered_arm = (r.read_file(native.ARM) for r in (clean, observed, current))
    common = observed.read_file(COMMON)
    assert common == current.read_file(COMMON) and native.digest(common) == release['target_COMMON_sha256']
    directory = registered_arm[DIRECTORY_OFFSET:TABLE_OFFSET]
    assert replay_arm[DIRECTORY_OFFSET:TABLE_OFFSET] == directory
    source = common_message_entries(clean.read_file(COMMON), stock_arm)
    installed = owned_entries(common, registered_arm, native.digest(directory))
    requests = trace['COMMON_requests']
    assert len(requests) == 34 and not trace['rows']
    ids = {r['message_ID'] for r in requests}
    assert ids == DECISIONS.keys() | {85, 86}
    pending = {r['message_ID'] for r in base.load(PENDING)['records']}
    assert len(pending) == 276 and not ids & pending
    captures = {r['frame']: r for r in report['frames_captured']}
    rows = []
    for number, (frame, voice, display, note) in DECISIONS.items():
        held = captures[frame]
        assert base.digest(held['path']) == held['PNG_sha256']
        nearby = [r for r in requests if r['message_ID'] == number and 0 <= frame - r['frame'] < 300]
        call_frames = {r['frame'] for r in nearby}
        assert len(call_frames) == (2 if number in (2903, 2940) else 1)
        for called in call_frames:
            assert sorted(r['PC'] for r in nearby if r['frame'] == called) == [0x020534F4, 0x0205528C]
        english = installed[number].text.decode('ascii')
        assert ('%s' not in english and english.strip() == display) or (
            number in (67, 97, 297) and english % {67: 'Lisbon', 97: 'Rafael', 297: 'Seville'}[number] == display)
        rows.append(dict(id=f'COMMON_MESSAGE_{number}', message_ID=number, file_path=COMMON,
            source_reference=reference(source[number]), current_reference=reference(installed[number]),
            source_hex=source[number].text.hex(), source_Japanese=source[number].text.decode('cp932'),
            current_hex=installed[number].text.hex(), current_English=english,
            english=RUMOR if number == 3665 else english.strip(), speaker=voice, decision='revision' if number == 3665 else 'retention',
            review_scope='ordinary gameplay with source and current archive binding', localization_note=note,
            current_text_observed=display, read_only_requests=nearby, held=held,
            fresh_rendering_pending=number == 3665))
    assert rows[-1]['source_Japanese'] == 'ねじまがったツノなんだそうだ\n竜のツノだって言うやつもいる\nどんな病にも効く薬になるって\n噂もある'
    base.save(OUTPUT, dict(registered_candidate_sha256=release['candidate_sha256'], actual_replay_candidate_sha256=active_hash,
        common_sha256=release['target_COMMON_sha256'], input_donor_sha256=donor['source_sha256'],
        records=rows, registered_numeral_followup=str(latest.parent.REVIEW),
        ordinary_gameplay=True, hardware=False, new_coverage_credit=0, pending_shared_overlap=[],
        evidence={str(p): base.digest(p) for p in (replay.CAPTURE / 'capture_report.json', replay.ROOT / 'observer/commands.json',
            replay.CAPTURE / 'navigation_command_journal.json', replay.PREFIX, latest.RELEASE, Path(__file__))}))
    print('Bound twelve shared lines to ordinary gameplay, with eleven retentions and one wrap-driven revision.')


if __name__ == '__main__':
    main()
