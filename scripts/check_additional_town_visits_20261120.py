"""Bind complete regional shop and tavern holds to the current source records."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_additional_town_visits_20261120 as capture
from scripts import observe_town_visit_followups_20261120 as followup
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base, head = capture.base, capture.head
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/additional_town_visits_20261120_v1.json')
HOLDS = {
    'copenhagen': ((5150, 656), (5950, 657), (6750, 657), (7550, 657), (8350, 658), (10350, 51)),
    'riga': ((5150, 658), (5950, 658), (6750, 656), (7950, 691), (8750, 656), (10750, 658)),
    'tripoli_town': ((5150, 657), (5950, 658), (6750, 656), (7950, 718), (8750, 656), (10750, 658)),
}
TEXT = {
    51: (('Welcome! What will you have?',), 'Barkeep', 'The greeting and question naturally lead into the drink menu.'),
    656: (('We only sell retail.',), 'Shopkeeper', 'The short reply directly explains the retailer’s scope.'),
    657: (("You're a sailor, aren't you?", 'Try the Market for bulk trade.'), 'Shopkeeper',
          'The tag sounds conversational and stays together. Market names the actual destination.'),
    658: (("Business? Oh, it's been all right.", "I'm hoping a good deal comes along."), 'Shopkeeper',
          'The echo and modest reply preserve the tone of a small-business conversation.'),
    691: (('Sweden only recently gained', 'independence from the Kalmar Union', 'with Denmark and Norway.'), 'Shopkeeper',
          'The shopkeeper gives the source’s recent event, union, and three countries in natural order.'),
    718: (('Admiral Hayreddin took his name', 'from the man he called his father.',
           'The man was so great, the Ottomans', 'made him Sultan of Algiers!'), 'Shopkeeper',
          'The report keeps the inherited name, family tie, and named title in the admiring voice of the shopkeeper.'),
}

namespace = dict(body_mask.__globals__)
exec(compile(checked_text(getsource(body_mask), {
    'range(297, 345, 16)': 'range(297, 361, 16)',
}), __file__, 'exec'), namespace)
four_row_mask = namespace['body_mask']


def read_run(case, schedule):
    folder = capture.ROOT / case
    paths = [folder / p for p in ('capture/capture_report.json', 'requests.json', 'terminal.json')]
    report, trace, terminal = map(base.load, paths)
    events, _, end, _, donor = schedule(case)
    assert report['ROM_sha256'] == terminal['ROM_sha256'] == base.digest(head.ROM)
    assert report['frames'] == end and report['scripted_input_schedule'] == events
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(val for key, val in report.items() if key.startswith('synthetic_'))
    assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256'] == base.digest(donor['source'])
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert all(base.digest(p) == sha for p, sha in terminal['evidence'].items())
    return shots(report), trace['source_requests'], {str(p): base.digest(p) for p in paths}


def main():
    assert not OUTPUT.exists()
    clean, current = map(base.NdsImage.open, (head.stage.CLEAN, head.ROM))
    arm = current.read_file(head.stage.ARM)
    common = '/COMMON/MESFILE.DK4'
    source = common_message_entries(clean.read_file(common), clean.read_file(head.stage.ARM))
    active = owned_entries(current.read_file(common), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    font = GameAsciiFont.from_arm9(arm)
    pending = {r['message_ID'] for r in base.load(Path(
        'translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_worklist_20261120_v1.json'))['records']}
    scenes, evidence = {}, {}
    for case, holds in HOLDS.items():
        sched = followup.schedule if case == 'tripoli_town' else capture.schedule
        frames, requests, files = read_run(case, sched)
        evidence.update(files)
        assert not pending.intersection(r['message_ID'] for r in requests)
        assert len(requests) == len(holds) * 2
        observed = []
        for (frame, key), first, copy in zip(holds, requests[::2], requests[1::2], strict=True):
            assert first['frame'] == copy['frame'] < frame and frame - first['frame'] < 150
            assert [first['PC'], copy['PC']] == [0x0205528C, 0x020534F4]
            assert key == first['message_ID'] == copy['message_ID']
            lines, role, note = TEXT[key]
            shot = frames[frame]
            image = captured(shot)
            assert ' '.join(lines) == ' '.join(active[key].text.decode('ascii').split())
            body = four_row_mask(image, font, lines)
            ink, bounds = complete_mask(font, role, image, 16, 277, (98, 97, 98))
            observed.append(dict(message_ID=key, capture=shot, lines=body, original_request=first,
                source_reference=reference(source[key]), current_reference=reference(active[key]),
                source_Japanese=source[key].text.decode('cp932'), current_English=active[key].text.decode('ascii'),
                localization_note=note, decision='retention', nameplate=dict(text=role, ink=ink, bounds=bounds)))
        scenes[case] = observed

    frames, requests, files = read_run('genoa_tavern', followup.schedule)
    evidence.update(files)
    assert [(r['frame'], r['message_ID']) for r in requests[::2]] == [(25417, 341), (25821, 51), (26610, 53)]
    visited = [10350, 17950, 21150, 25150, 25550, 25950, 26350]
    assert all(base.digest(frames[f]['path']) == frames[f]['PNG_sha256'] for f in visited)
    base.save(OUTPUT, dict(candidate_sha256=base.digest(head.ROM), scenes=scenes,
        genoa_tavern=dict(story_archive='/data/SC1.DK4', block=170, displayed_choices=['Yes...', "Ask what you don't know"],
            shared_join_notice=341, recruit='Julio Erneco', original_transition_into_tavern=True,
            visual_milestones=[frames[f] for f in visited], alternative_choices_unvisited=True),
        actual_saved_game_playback=True, town_conditions_injected=False, hardware=False,
        evidence=evidence, new_editorial_credit=0))
    print('Verified 18 regional dialogue and nameplate holds and documented Julio’s ordinary Tavern recruitment.')


if __name__ == '__main__':
    main()
