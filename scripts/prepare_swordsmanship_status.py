"""Prepare the source-owned duel statistics translation and research evidence."""

import json
from pathlib import Path

from dk4tool.patch.swordsmanship_status_release import CLEAN
from dk4tool.patch.swordsmanship_status_release import transform as prepare
from dk4tool.rom.nds import NdsImage


def main():
    source, plan = prepare(NdsImage.open('out/all_routes_combined_v156_candidate.nds'), NdsImage.open('work/clean.nds'))
    Path('work/analysis/swordsmanship_status_research_arm9.bin').write_bytes(source)
    Path('work/analysis/swordsmanship_status_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    manuscript = {'format': 'dk4-swordsmanship-status-manuscript-v1',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'encoder': 'dialogue-relocatable-v1', 'source_arm9_sha256': CLEAN,
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': plan['records'], 'status': plan['status']}
    Path('translations/swordsmanship_status_manuscript_v1.json').write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared one complete Fencing/HP/state template; inherited helpers unchanged; twelve-byte tail helper; native proof pending.')


if __name__ == '__main__':
    main()
