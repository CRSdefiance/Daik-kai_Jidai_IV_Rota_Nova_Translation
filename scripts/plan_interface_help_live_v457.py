"""Ordinary Help navigation through ship, crew, item and Golden Route articles."""

import json
from pathlib import Path

ROOT = Path('work/analysis/interface_help_release_v457')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    pages = {}
    for path in ('work/analysis/general_help_v431/page_proposal.json',
                 'work/analysis/faction_help_v439/page_proposal.json',
                 'work/analysis/interface_help_v456/page_proposal.json'):
        pages.update({r['topic_id']: r for r in read(Path(path))['pages']})
    pages[202] = {'visible_lines': ['Help Index', 'The World of Uncharted Waters IV', 'Town Commands',
                                  'Commands at Town', 'Shared Commands', 'Data Guide'],
                  'links': [{'id': 0, 'label': 'The World of Uncharted Waters IV', 'row': 1},
                            {'id': 1, 'label': 'Town Commands', 'row': 2}, {'id': 7, 'label': 'Commands at Town', 'row': 3},
                            {'id': 103, 'label': 'Shared Commands', 'row': 4}, {'id': 143, 'label': 'Data Guide', 'row': 5}]}
    entry = read(Path('work/analysis/help_footer_release_v455/semantic_regression_inputs.json'))
    (ROOT / 'entry_inputs.json').write_text(json.dumps(entry, indent=2) + '\n', encoding='utf-8')
    now, current, history = 21600, 143, [143]
    commands, visits, captures = [], [], {}

    def key(button):
        nonlocal now, current
        now += 200
        commands.append({'until': now, 'duration': 8, 'buttons': [button]})
        if button == 'L':
            history.pop()
            current = history[-1]
        elif button == 'X':
            current = 202
            history[:] = [202]

    def click(topic):
        nonlocal now, current
        page = pages[current]
        links = [r for r in page['links'] if r['id'] == topic]
        assert len(links) == 1
        link = links[0]
        text = page['visible_lines'][link['row']]
        label = link['label'].strip()
        assert text.count(label) == 1
        x = (text.index(label) + len(label) // 2) * 6 + 2
        y = 24 + (link['row'] - 1) * 16 + 5
        assert 0 <= x < 256 and 0 <= y < 192
        origin = current
        if page['links'][0]['id'] != topic:
            now += 200
            commands.append({'until': now, 'duration': 8, 'buttons': [], 'touch': [x, y]})
        now += 200
        commands.append({'until': now, 'duration': 8, 'buttons': ['A']})
        current = topic
        history.append(topic)
        captures.setdefault(str(topic), now)
        visits.append({'from': origin, 'to': topic, 'frame': now, 'touch': [x, y]})

    key('X')
    click(103)
    click(134)
    click(135)
    key('L')
    click(136)
    click(195)
    for topic in (196, 197, 198, 199, 200):
        click(topic)
        key('L')
    key('L')
    key('L')
    click(137)
    key('L')
    click(141)
    click(201)
    key('L')
    key('L')
    click(142)
    key('L')
    key('L')
    assert current == 103
    click(138)
    key('L')
    click(139)
    first = now
    click(210)
    click(139)
    returned = now
    key('L')
    key('L')
    key('L')
    assert current == 103
    click(140)
    key('L')
    history_first = now
    now += 200
    commands.append({'until': now, 'duration': 8, 'buttons': ['R']})
    now += 200
    commands.append({'until': now, 'duration': 8, 'buttons': ['L']})
    expected = {135, 136, 137, 138, 139, 140, 141, 142, 195, 196, 197, 198, 199, 200, 201, 210}
    assert expected <= set(map(int, captures))
    plan = {'page_frames': {k: v for k, v in captures.items() if int(k) in expected},
            'visited_links': visits, 'commands': commands, 'crew_return_frames': [first, returned],
            'history_frames': [history_first, now], 'terminal_frame': now}
    (ROOT / 'navigation_plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'navigation_commands.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in commands), encoding='utf-8')
    print('Ordinary navigation planned:', len(expected), 'revised pages;', len(commands), 'commands;final frame', now)


if __name__ == '__main__':
    main()
