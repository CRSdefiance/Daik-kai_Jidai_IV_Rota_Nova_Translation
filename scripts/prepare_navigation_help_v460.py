"""Final generic Help headings and complete source navigation rules."""

import json
from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare

PROSE = {
    76: ('Auto Move',
         'Auto Move takes you to a chosen city automatically. It requires a [[120|Captain]] and [[123|Surveyor]]. You can travel only between cities connected by a valid route: the starting city and destination must be linked on the [[104|Route Map]], and your faction must have [[150|market share]] in both cities and every intermediate city. Valid routes are shown in red.',
         'Automatic travel to chosen city requires captain/surveyor. Valid route means chart line connects endpoints and faction share at both endpoints and all intermediate cities;red on chart.',
         'Restore all four original links in order. Preserve every intermediate-city share condition, not merely a line on the map.'),
    83: ('Manual Movement',
         'During normal sailing, steer with the D-pad and adjust the sails with L and R. You can also steer [[101|with the touchscreen]]. Opening the sails increases speed; closing them reduces it. Ships leave port with their sails Half Open. Open them to change to Full Open. While Half Open, the sails adjust automatically if every mast has [[125|a Sail Handler]].',
         'Normal sailing D-pad rudder/L1R1 sails/touchscreen. Source circle/cross open/close sail spread,raising/lowering speed. Departure half-open;open gives full-open. All masts staffed by sail handlers enables automatic orientation at half-open.',
         'Use current D-pad/L/R controls and describe open/close actions without copying unsupported source-platform circle/cross symbols. Ordinary sailors do not replace assigned Sail Handlers.'),
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
    root = Path('work/analysis/navigation_help_v460')
    manuscript = Path('translations/navigation_help_manuscript_v2.json')
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
