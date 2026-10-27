"""Help skill names matching pixel-verified Vigor/Swords/Speech/Guile UI."""

import json
from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare
from scripts.prepare_crew_help_v448 import PROSE as CREW
from scripts.prepare_sailor_data_help_v446 import PROSE as DATA

TOPICS = {116, 117, 118, 121, 126, 128, 133, 158, 168, 170, 175, 177, 178}
PROSE = {}
for topic in sorted(TOPICS):
    title, english, meaning, note = (CREW if topic in CREW else DATA)[topic]
    if topic == 158:
        english = english.replace('[[168|HP and Health]]', '[[168|HP and Vigor]]')
    else:
        for old, new in (('Health', 'Vigor'), ('Combat', 'Swords'), ('Social', 'Speech'), ('Tactics', 'Guile')):
            title = title.replace(old, new)
            english = english.replace(old, new)
    if topic == 168:
        note = 'Vigor represents vitality/maxHP and physical resilience,distinct from the physical Health condition. Source facts and all original links remain.'
    elif topic == 178:
        english = 'The Swords skill measures swordsmanship. A higher Swords value gives an officer an advantage in [[98|boarding battles]] and [[99|duels]] and suits [[128|Boarding Leaders]]. It is influenced by Stamina and Agility.'
        note = 'Use the full active Swords label with natural singular-skill grammar;source facts and all three original links remain.'
    else:
        note = 'Use pixel-verified active skill names Vigor/Swords/Speech/Guile;the original numerical rules,roles,source facts and link order remain. Physical Health is unchanged.'
    PROSE[topic] = (title, english, meaning, note)


def main():
    root = Path('work/analysis/skill_terms_v463')
    manuscript = Path('translations/skill_terms_help_manuscript_v1.json')
    with patch.object(prepare, 'ROOT', root), patch.object(prepare, 'MANUSCRIPT', manuscript), \
            patch.object(prepare, 'PARENT', Path('out/all_routes_combined_v461_candidate.nds')), \
            patch.object(prepare, 'PARENT_TOPIC_COUNT', 211), patch.object(prepare, 'PROSE', PROSE), \
            patch.object(prepare, 'LAYOUT_BY_TOPIC', {133: 'semicolon-entries-v1'}), \
            patch.object(prepare, 'REUSED_CONTINUATIONS', {168: [208], 133: [209]}):
        prepare.main()
    data = json.loads(manuscript.read_text(encoding='utf-8'))
    for row in data['records']:
        row['context'] = 'Original job/skill Help and clean neighbors;actual V461 Sailor Info pixels and native runtime skill table reviewed.'
    manuscript.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    from dk4tool.patch.grand_race_menu_release import sha
    p = root / 'page_proposal.json'
    plan = json.loads(p.read_text(encoding='utf-8'))
    plan['manuscript_sha256'] = sha(manuscript.read_bytes())
    p.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
