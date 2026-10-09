"""Prepare source-reviewed name labels; no playable ROM."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import STAGE, transform
from dk4tool.rom.nds import NdsImage


def main():
    rom = NdsImage.open('out/all_routes_combined_v153_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    saved, plan = transform(rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'))
    if STAGE < rom.rom.arm7RamAddress + len(rom.rom.arm7):
        raise ValueError('Name staging overlaps ARM7 initial image')
    Path('work/analysis/ordinary_name_fidelity_research_arm9.bin').write_bytes(saved)
    Path('work/analysis/ordinary_name_fidelity_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('translations/ordinary_name_fidelity_manuscript_v1.json').write_text(json.dumps({
        'format': 'dk4-ordinary-name-fidelity-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'target_locale': 'en-US', 'source_arm9_sha256': sha(clean.read_file('/__arm9__.bin')),
        'records': plan['records']}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"17 complete name/role corrections prepared; reserved payload {plan['pool_payload_bytes']} bytes, {plan['pool_used_bytes']} used. No playable ROM created.")


if __name__ == '__main__':
    main()
