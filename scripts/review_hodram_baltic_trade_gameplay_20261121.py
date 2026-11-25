"""Revisit Hodram's complete Baltic trade lesson after its ordinary port trigger."""

from argparse import ArgumentParser
from pathlib import Path

from scripts import verify_seville_square_gameplay_20261121 as square


FOLDER = square.runs.VOYAGES['hamburg'][0]
EARLIER = Path('translations/hodram_opening_contextual_final_review_v1.json')
REVIEW = FOLDER / 'hodram_baltic_trade_contextual_review.json'
SCENE = '/data/SC1.DK4'
BLOCK = 43
SPEAKERS = {1: 'Hodram Bergstrom', 16: 'Gerhard Adernkatz', 18: 'Charles Rochefort', 23: 'Manuel Almeida'}
CONTEXT = ('At the port after the Speyer encounter, the officers connect naval strength with trade. '
           'Gerhard calls for retaking Baltic trading rights, Charles explains how victory and investment '
           'affect towns, and Manuel recommends spreading contracts before growing individual shares. '
           'Hodram turns the advice into a plan for reaching the open ocean.')
DECISIONS = {
    5: ("Let's crush Speyer and take back the Baltic trade rights his fleet seized by violating our territorial waters.",
        'Gerhard is urging two actions. Joining them directly keeps his resolve and identifies how the rival gained the rights.'),
    16: (None, "Charles's concise explanation connects a victory at sea to the enemy's weaker hold on towns."),
    19: ("Only a strong fleet can hold on to a wide trade network. The profits can pay for an even stronger fleet.",
         'Restore the source condition that a fleet needs strength to maintain a large network. Two sentences make the cycle easy to follow.'),
    33: (None, 'Manuel grounds the theory in the cost of building a fleet and the practical need for regular trade.'),
    39: (None, "Hodram follows the argument and sums up the link between the world's largest trading network and its strongest fleet."),
    42: (None, "Gerhard's formal reply makes the long-term funding point without adding a rank or an absolute financial threshold."),
    54: ("Sign contracts in as many towns as you can, even at one percent. That'll open plenty of routes. We can build up our shares later.",
         "Preserve both the source's advice to reach as many towns as possible and its low initial share. Manuel explains why raising shares can wait."),
    68: ("If we're at war with a faction that also has a contract there, we're free to invest in the town and take its share.",
         "Charles distinguishes wartime competitors and spells out how investment gains their share. 'We're free to' reads naturally beside Manuel's advice."),
    75: (None, "Hodram's decision names the major North Sea towns and the strategic reason for signing contracts there."),
}


def source_and_current(clean, current):
    base, native = square.base, square.native
    original, installed = [native.IlnkContainer.parse(rom.read_file(SCENE)).blocks[BLOCK] for rom in (clean, current)]
    old = [row for row in base.load(EARLIER)['records'] if row['block'] == BLOCK]
    assert len(old) == 9 and {row['source_record_index'] for row in old} == DECISIONS.keys()
    result = []
    for row in old:
        source = row['source_reference']
        source_text = bytes.fromhex(source['hex'])
        assert original[source['offset']:source['offset'] + len(source_text)] == source_text
        assert source_text[1:].decode('cp932') == row['source_Japanese']
        start = row['target_command_offset']
        command = bytes.fromhex(row['target_native_command_hex'])
        assert installed[start:start + len(command)] == command
        assert command[:6] == bytes.fromhex(source['complete_preamble_hex']) and command[-1] == 0
        selector = command[5]
        end = command.index(0, 6)
        assert not any(command[end:])
        body = command[6:end].decode('ascii')
        previous = ' '.join(body.split())
        revised, reason = DECISIONS[row['source_record_index']]
        target = revised or previous
        assert not any(control in source_text[1:] or control in command[6:] or
                       control in target.encode('ascii') for control in (b'FI', b'FA', b'FO'))
        result.append(dict(id=row['id'], file_path=SCENE, block=BLOCK, source_selector=selector,
            source_record_index=row['source_record_index'], source_reference=dict(file_path=SCENE,
                block=BLOCK, offset=source['offset'], command_offset=source['header_offset'],
                block_sha256=native.digest(original), exact_stored_hex=source['hex']),
            registered_reference=dict(file_path=SCENE, block=BLOCK, offset=start + 5, command_offset=start,
                block_sha256=native.digest(installed), exact_stored_hex=command[5:end].hex(),
                complete_native_command_hex=command.hex(), terminator_and_alignment_hex=command[end:].hex()),
            Japanese=row['source_Japanese'], speaker=SPEAKERS[selector], context=CONTEXT,
            source_meaning=row['source_meaning'], english=previous, proposed_english=target,
            decision='revision' if revised else 'retention', localization_note=reason,
            review=row['review'], historical_evidence=str(EARLIER)))
    return result


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    args = parser.parse_args()
    base, native, active = square.base, square.native, square.runs.active
    report_path = FOLDER / 'capture/capture_report.json'
    journal = FOLDER / 'capture/navigation_command_journal.json'
    report, inputs, plan, release = map(base.load, (report_path, journal, args.plan, active.RELEASE))
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert report['ROM_sha256'] == inputs['ROM_sha256'] == release['candidate_sha256'] == base.digest(active.ROM)
    assert release['clean_input_sha256'] == base.digest(native.CLEAN)
    clean, current = map(base.NdsImage.open, (native.CLEAN, active.ROM))
    rows = source_and_current(clean, current)
    frames = {r['frame']: r for r in report['frames_captured'] if r['path'].endswith('_navigation.png')}
    command_at = {record['frame']: record['command'] for record in inputs['commands_received']}
    sequence = [plan['dock_prompt'], *plan['panels'], plan['port_return']]
    assert len(sequence) == 11 and sequence == sorted(set(sequence))
    for frame, following in zip(sequence, sequence[1:]):
        assert command_at[frame]['buttons'] == ['A'] and command_at[frame]['until'] == following
    panels, previews = square.observe(current, rows, frames, plan['panels'], SPEAKERS)
    returned, image = square.town.read_frame(frames, plan['port_return'])
    previews.append(('Returned to Hamburg port menu', image))
    sheets = []
    for at in range(0, len(previews), 6):
        target = FOLDER / f'hodram_baltic_trade_{at // 6 + 1}.png'
        square.town.sheet(previews[at:at + 6], target)
        sheets.append(dict(path=str(target), sha256=base.digest(target)))
    for row, panel in zip(rows, panels, strict=True):
        row['observed_current_english'] = panel
        row['review'] = row['review'] | {'formatting': row['decision'] == 'retention'}
        row['previous_english'] = row['english']
        row['english'] = row.pop('proposed_english')
        row['protected_phrases'] = []
    assert not REVIEW.exists()
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', candidate_sha256=release['candidate_sha256'],
        clean_sha256=release['clean_input_sha256'], block=BLOCK, file_path=SCENE, route=1,
        records=rows, proposed_revisions=sum(r['decision'] == 'revision' for r in rows),
        justified_retentions=sum(r['decision'] == 'retention' for r in rows), individual_new_credit=0,
        ordinary_port_trigger=True, after_dialogue=returned, screenshots=sheets,
        proposed_revisions_need_fresh_formatting_gameplay_and_registration=True,
        original_campaign_coverage='Hodram, SC1 B43, starting from the original Hamburg docking prompt',
        evidence={str(path): base.digest(path) for path in (EARLIER, report_path, journal, args.plan)}))
    print('Verified nine ordinary port tutorial panels. Four editorial proposals and five justified retentions recorded.')


if __name__ == '__main__':
    main()
