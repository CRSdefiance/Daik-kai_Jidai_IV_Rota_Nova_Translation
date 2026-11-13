"""Normal Help index, Deck trees, list continuation and role-glossary pages."""

import json
from pathlib import Path

ROOT = Path('work/analysis/skill_terms_release_v464')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    pages = {}
    for path in ('work/analysis/general_help_v431/page_proposal.json',
                 'work/analysis/faction_help_v439/page_proposal.json',
                 'work/analysis/sailor_data_help_v446/page_proposal.json',
                 'work/analysis/crew_help_v448/page_proposal.json',
                 'work/analysis/skill_terms_v463/page_proposal.json'):
        pages.update({r['topic_id']: r for r in read(Path(path))['pages']})
    pages[202] = {'visible_lines': ['Help Index', 'The World of Uncharted Waters IV', 'Town Commands',
                                  'Commands at Town', 'Shared Commands', 'Data Guide'],
                  'links': [{'id': 0, 'label': 'The World of Uncharted Waters IV', 'row': 1},
                            {'id': 1, 'label': 'Town Commands', 'row': 2},
                            {'id': 7, 'label': 'Commands at Town', 'row': 3},
                            {'id': 103, 'label': 'Shared Commands', 'row': 4},
                            {'id': 143, 'label': 'Data Guide', 'row': 5}]}
    entry = [r for r in read(Path('work/analysis/help_footer_release_v455/semantic_regression_inputs.json')) if r['start'] <= 21001]
    (ROOT / 'entry_inputs.json').write_text(json.dumps(entry, indent=2) + '\n', encoding='utf-8')
    now, current = 21200, 202
    history = [202]
    commands, captures, visits = [], {}, []

    def key(button):
        nonlocal now, current
        now += 200
        commands.append({'until': now, 'buttons': [button], 'duration': 8})
        if button == 'L':
            assert len(history) > 1
            history.pop()
            current = history[-1]
        elif button == 'X':
            current = 202
            history[:] = [202]

    def click(topic):
        nonlocal now, current
        page = pages[current]
        matches = [r for r in page['links'] if r['id'] == topic]
        assert len(matches) == 1, (current, topic)
        link = matches[0]
        label = link['label'].strip()
        text = page['visible_lines'][link['row']]
        assert text.count(label) == 1
        x = (text.index(label) + len(label) // 2) * 6 + 2
        y = 24 + (link['row'] - 1) * 16 + 5
        assert 0 <= x < 256 and 0 <= y < 192
        origin = current
        if page['links'][0]['id'] != topic:
            now += 200
            commands.append({'until': now, 'buttons': [], 'touch': [x, y], 'duration': 8})
        now += 200
        commands.append({'until': now, 'buttons': ['A'], 'duration': 8})
        current = topic
        history.append(topic)
        captures.setdefault(str(topic), now)
        visits.append({'from': origin, 'to': topic, 'frame': now, 'touch': [x, y]})

    click(103)
    click(105)
    click(110)
    for topic in (116, 117, 118, 121, 126):
        click(topic)
        key('L')
    key('L')
    click(127)
    for topic in (128,):
        click(topic)
        key('L')
    key('L')
    click(133)
    first_list = now
    click(209)
    click(133)
    returned_list = now
    key('L')
    key('L')
    key('L')
    assert current == 105
    key('X')
    click(143)
    click(158)
    click(168)
    first_hp = now
    click(208)
    click(168)
    returned_hp = now
    key('L')
    key('L')
    key('L')
    click(170)
    for topic in (175, 177, 178):
        click(topic)
        key('L')
    history_first = now
    now += 200
    commands.append({'until': now, 'buttons': ['R'], 'duration': 8})
    now += 200
    commands.append({'until': now, 'buttons': ['L'], 'duration': 8})
    expected = {116, 117, 118, 121, 126, 128, 133, 158, 168, 170, 175, 177, 178, 208, 209}
    assert expected <= set(map(int, captures))
    plan = {'page_frames': {k: v for k, v in captures.items() if int(k) in expected},
            'visited_links': visits, 'commands': commands,
            'list_return_frames': [first_list, returned_list],
            'HP_return_frames': [first_hp, returned_hp],
            'history_frames': [history_first, now], 'terminal_frame': now}
    (ROOT / 'navigation_plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'navigation_commands.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in commands), encoding='utf-8')
    print('Ordinary navigation planned:', len(plan['page_frames']), 'revised pages;', len(commands), 'commands; final frame', now)


if __name__ == '__main__':
    main()
