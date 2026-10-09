"""Prepare the source-locked village research layer; never creates a ROM."""
import json
from pathlib import Path

from dk4tool.patch.village_promised_words_release import CLEAN, transform
from dk4tool.rom.nds import NdsImage


def prepare():
    image = NdsImage.open('out/all_routes_combined_v154_candidate.nds')
    saved, plan = transform(image, NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    manuscript = {'format': 'dk4-arm9-village-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                  'target_locale': 'en-US', 'source_arm9_sha256': CLEAN,
                  'encoder': 'dialogue-relocatable-v1',
                  'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                  'records': plan['records'], 'status': 'reviewed-prose-formatting-pending-not-integrated'}
    Path('translations/village_promised_words_manuscript_v1.json').write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('work/analysis/village_promised_words_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('work/analysis/village_promised_words_research_arm9.bin').write_bytes(saved)
    print(f"54 clean-source village strings; 54 owner references plus one classified code coincidence; staged payload {plan['pool_payload_bytes']} bytes. Research only.")
    return image.read_file('/__arm9__.bin'), saved, plan


if __name__ == '__main__':
    prepare()
