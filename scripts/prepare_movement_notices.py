"""Prepare disposable movement/shortage research; never creates a ROM."""

import json
from pathlib import Path

from dk4tool.patch.movement_notice_release import CLEAN, transform
from dk4tool.rom.nds import NdsImage


def main():
    saved, common, plan = transform(NdsImage.open('out/all_routes_combined_v155_candidate.nds'),
                                    NdsImage.open('work/clean.nds'))
    Path('work/analysis/movement_notices_research_arm9.bin').write_bytes(saved)
    Path('work/analysis/movement_notices_research_common.bin').write_bytes(common)
    Path('work/analysis/movement_notices_plan.json').write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    manuscript = {'format': 'dk4-movement-notices-manuscript-v1',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'encoder': 'dialogue-relocatable-v1', 'source_arm9_sha256': CLEAN,
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': plan['records'], 'status': 'reviewed-prose-native-formatting-pending-not-integrated'}
    Path('translations/movement_notices_manuscript_v1.json').write_text(
        json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Nine movement/shortage records; five exact label owners; {plan['itcm_bytes']} ITCM bytes; research only.")


if __name__ == '__main__':
    main()
