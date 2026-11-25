"""Final generic Help headings and complete source navigation rules."""

import json
from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare

PROSE = {
    101: ('Touchscreen Sailing',
          'During normal sailing, you can steer with the touchscreen. Touch the direction you want to sail, and the ship moves that way. Touch farther from the ship to sail faster. Touch the ship itself to stop in place.',
          'Normal sailing supports touch direction; greater touch distance from ship increases speed; touching ship stops in place.',
          'Restore manual-sailing scope and proper heading. Direction is not restricted to ahead; no Auto Move or compass formula is invented.'),
    104: ('Route Map',
          'The Route Map shows the current sea region and faction names. In a region containing cities you have not visited, only [[145|City-level settlements]] are shown. Select a city or fleet to view its data. Lines between cities are routes; you can use Auto Move along red routes. To view another sea region, zoom out to the world map, then select the region.',
          'Current sea map/faction names. Regions with unvisited cities show city-level settlements only. City/fleet selection displays data; intercity lines are routes; red routes enable automatic movement. Source square action zooms to world, then choose other region.',
          'Preserve City versus Port distinction, red-route condition and both zoom/region steps. Describe the world-map action rather than copying an unsupported source-platform square glyph.'),
}


def main():
    root = Path('work/analysis/navigation_help_v458')
    manuscript = Path('translations/navigation_help_manuscript_v1.json')
    with patch.object(prepare, 'ROOT', root), patch.object(prepare, 'MANUSCRIPT', manuscript), \
            patch.object(prepare, 'PARENT', Path('out/all_routes_combined_v457_candidate.nds')), \
            patch.object(prepare, 'PARENT_TOPIC_COUNT', 211), patch.object(prepare, 'PROSE', PROSE):
        prepare.main()
    data = json.loads(manuscript.read_text(encoding='utf-8'))
    for row in data['records']:
        row['context'] = 'Original normal-sailing touch or Shared Commands Route Map article;clean neighboring articles and source link145 reviewed.'
    manuscript.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    from dk4tool.patch.grand_race_menu_release import sha
    p = root / 'page_proposal.json'
    plan = json.loads(p.read_text(encoding='utf-8'))
    plan['manuscript_sha256'] = sha(manuscript.read_bytes())
    p.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
