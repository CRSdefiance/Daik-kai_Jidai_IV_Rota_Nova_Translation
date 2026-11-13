"""Ordinary touchscreen and L/R navigation for all reviewed Help pages."""

import json
from pathlib import Path

ROOT = Path('work/analysis/sailor_data_help_release_v447')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    proposal = read(Path('work/analysis/sailor_data_help_v446/page_proposal.json'))
    pages = {r['topic_id']: r for r in proposal['pages']}
    pages[143] = next(r for r in read(Path('work/analysis/faction_help_v439/page_proposal.json'))['pages'] if r['topic_id'] == 143)
    entry = read(Path('work/analysis/faction_help_release_v440/entry_inputs.json'))
    entry += [{'start': 21201, 'duration': 8, 'buttons': [], 'touch': [30, 96]},
              {'start': 21401, 'duration': 8, 'buttons': ['A']}]
    (ROOT / 'entry_inputs.json').write_text(json.dumps(entry, indent=2) + '\n', encoding='utf-8')
    now, current = 21600, 143
    commands, captures, visits = [], {}, []
    history = [143]

    def key(button):
        nonlocal now, current
        now += 200
        commands.append({'until': now, 'buttons': [button], 'duration': 8})
        if button == 'L':
            assert len(history) > 1
            history.pop()
            current = history[-1]

    def click(topic):
        nonlocal now, current
        page = pages[current]
        links = [r for r in page['links'] if r['id'] == topic]
        assert len(links) == 1, (current, topic, links)
        link = links[0]
        text = page['visible_lines'][link['row']]
        label = link['label'].strip()
        assert text.count(label) == 1
        column = text.index(label)
        x = (column + len(label) // 2) * 6 + 2
        y = 24 + (link['row'] - 1) * 16 + 5
        assert 0 <= x < 256 and 0 <= y < 192
        # Fresh/recreated Help pages select their first child. Touching that
        # already selected child activates it immediately; do not then press A
        # a second time. Other targets need a selection touch followed by A.
        if page['links'][0]['id'] != topic:
            now += 200
            commands.append({'until': now, 'buttons': [], 'touch': [x, y], 'duration': 8})
        now += 200
        commands.append({'until': now, 'buttons': ['A'], 'duration': 8})
        current = topic
        history.append(topic)
        captures.setdefault(str(topic), now)
        visits.append({'from': history[-2], 'to': topic, 'frame': now, 'touch': [x, y]})

    click(153)
    for topic in range(154, 158):
        click(topic)
        key('L')
    key('L')
    click(158)
    for topic in (159, 160):
        click(topic)
        key('L')
    click(161)
    for topic in range(162, 168):
        click(topic)
        key('L')
    key('L')
    click(168)
    first_hp = now
    click(208)
    click(168)
    returned_hp = now
    key('L')
    key('L')
    key('L')
    assert current == 158
    click(169)
    key('L')
    click(170)
    for topic in (171, 172, 174, 176, 179, 173, 178, 175, 177):
        click(topic)
        key('L')
    key('L')
    click(180)
    key('L')
    key('L')
    history_first = now
    # R and L restore the exact history page; no link is activated here.
    now += 200
    commands.append({'until': now, 'buttons': ['R'], 'duration': 8})
    now += 200
    commands.append({'until': now, 'buttons': ['L'], 'duration': 8})
    history_return = now
    assert set(map(int, captures)) == set(range(153, 181)) | {208}
    plan = {'page_frames': captures, 'visited_links': visits, 'commands': commands,
            'HP_return_frames': [first_hp, returned_hp], 'history_frames': [history_first, history_return],
            'terminal_frame': now}
    (ROOT / 'navigation_plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'navigation_commands.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in commands), encoding='utf-8')
    print('Ordinary navigation planned:', len(captures), 'pages;', len(commands), 'commands; final frame', now)


if __name__ == '__main__':
    main()
