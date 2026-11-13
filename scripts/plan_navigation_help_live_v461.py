"""Normal linked Help navigation to four restored navigation articles."""

import json
from pathlib import Path

ROOT = Path('work/analysis/navigation_help_release_v461')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    pages = {}
    for name in ('general_help_v431', 'crew_help_v448', 'navigation_help_v460'):
        pages.update({r['topic_id']: r for r in read(Path('work/analysis') / name / 'page_proposal.json')['pages']})
    pages[202] = {'visible_lines': ['Help Index', 'The World of Uncharted Waters IV', 'Town Commands',
                                  'Commands at Town', 'Shared Commands', 'Data Guide'],
                  'links': [{'id': 0, 'label': 'The World of Uncharted Waters IV', 'row': 1},
                            {'id': 103, 'label': 'Shared Commands', 'row': 4}]}
    entry = [r for r in read(Path('work/analysis/help_footer_release_v455/semantic_regression_inputs.json')) if r['start'] <= 21001]
    (ROOT / 'entry_inputs.json').write_text(json.dumps(entry, indent=2) + '\n', encoding='utf-8')
    now, current, history = 21200, 202, [202]
    commands, captures, visits = [], {}, []

    def key(button):
        nonlocal now, current
        now += 200
        commands.append({'until': now, 'duration': 8, 'buttons': [button]})
        if button == 'L':
            history.pop()
            current = history[-1]

    def click(topic):
        nonlocal now, current
        page = pages[current]
        link = next(r for r in page['links'] if r['id'] == topic)
        label = link['label'].strip()
        text = page['visible_lines'][link['row']]
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

    click(103)
    click(104)
    key('L')
    click(105)
    click(110)
    click(120)
    click(76)
    key('L')
    key('L')
    click(125)
    click(83)
    click(101)
    key('L')
    first = now
    now += 200
    commands.append({'until': now, 'duration': 8, 'buttons': ['R']})
    now += 200
    commands.append({'until': now, 'duration': 8, 'buttons': ['L']})
    expected = {76, 83, 101, 104}
    assert expected <= set(map(int, captures))
    plan = {'page_frames': {k: v for k, v in captures.items() if int(k) in expected},
            'commands': commands, 'visited_links': visits, 'history_frames': [first, now], 'terminal_frame': now}
    (ROOT / 'navigation_plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'navigation_commands.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in commands), encoding='utf-8')
    print('Four actual page targets;original Captain/Masts links used;final frame', now)


if __name__ == '__main__':
    main()
