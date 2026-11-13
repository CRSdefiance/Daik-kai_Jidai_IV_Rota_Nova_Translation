"""Save the exact-source item parent position repair for native verification."""

import json
from pathlib import Path

from dk4tool.patch.item_parent_layout_research import transform


def main():
    saved, plan = transform(Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes())
    Path('work/analysis/item_parent_layout_research_arm9.bin').write_bytes(saved)
    Path('work/analysis/item_parent_layout_plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    print(plan['target_arm9_sha256'], 'four parent-position fields; all text/code/source crops preserved')


if __name__ == '__main__':
    main()
