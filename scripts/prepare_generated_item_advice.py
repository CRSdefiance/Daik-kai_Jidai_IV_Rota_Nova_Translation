"""Prepare complete static/default/generated item paragraph research."""

import json
from pathlib import Path

from dk4tool.patch.generated_item_advice_research import transform
from dk4tool.rom.nds import NdsImage


def main():
    source = Path('work/analysis/item_parent_layout_research_arm9.bin').read_bytes()
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    target, updated = transform(source, image.read_file('/COMMON/MESFILE.DK4'), plan)
    Path('work/analysis/generated_item_advice_research_arm9.bin').write_bytes(target)
    Path('work/analysis/generated_item_advice_plan.json').write_text(json.dumps(updated, indent=2) + '\n', encoding='utf-8')
    print(updated['target_arm9_sha256'])


if __name__ == '__main__':
    main()
