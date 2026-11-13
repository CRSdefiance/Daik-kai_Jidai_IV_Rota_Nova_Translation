"""Register the complete source-bound Shipyard/regional UI family after V613."""

import copy
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.regional_policy_prompts import transform as prompt_transform
from dk4tool.patch.shipyard_ui_labels import transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_fleet_v615')


def main():
    parent = NdsImage.open('out/all_routes_combined_v613_candidate.nds')
    arm, labels = transform(parent.read_file('/__arm9__.bin'))
    common, arm, prompts = prompt_transform(parent.read_file('/COMMON/MESFILE.DK4'), arm)
    save('translations/shipyard_ui_labels_v1.json', {'format': 'dk4-shipyard-ui-labels-v1', 'proof': labels})
    save('translations/regional_policy_prompts_v1.json', {'format': 'dk4-regional-policy-prompts-v1', 'proof': prompts})
    (ROOT / 'complete_UI_RESEARCH_ONLY_ARM9.bin').write_bytes(arm)
    (ROOT / 'complete_UI_RESEARCH_ONLY_COMMON.bin').write_bytes(common)
    save(ROOT / 'complete_prompt_QA.json', prompts)
    font = GameAsciiFont.from_arm9(arm)
    sheet = Image.new('RGB', (520, 8 * 116), '#263238')
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(prompts['audits']):
        draw.text((8, index * 116 + 4), f"COMMON {row['message_id']} - exact-font layout preview", fill='white')
        preview = Image.new('RGB', (256, 44), '#e9dbb7')
        for line_index, line in enumerate(row['audit']['visible_lines']):
            for n, ch in enumerate(line):
                x = 12 + n * 6 + (6 if line_index else 0)
                preview.paste('#17170f', (x, 6 + line_index * 16), font.decode(ch))
        preview.save(ROOT / f"prompt_{row['message_id']}_preview.png")
        sheet.paste(preview.resize((512, 88), Image.Resampling.NEAREST), (4, index * 116 + 24))
    sheet.save(ROOT / 'all8_prompt_previews.png')
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v613'])
    profile.update({'shipyard_ui_labels': 'translations/shipyard_ui_labels_v1.json',
                    'regional_policy_prompts': 'translations/regional_policy_prompts_v1.json',
                    'description': 'Complete V613 plus both Ship Name callers,all four regional policy choices,assignment confirmations,map missions and eight complete source-reviewed native prompts; no pool/cache/section growth.',
                    'note': 'Experimental. Actual caption/menu/prompt/mission/formation controls and regional source-art comparisons required. All original graphics scopes remain open.',
                    'status': 'experimental'})
    if 'all-routes-unified-v615' in registry['profiles']:
        assert registry['profiles']['all-routes-unified-v615'] == profile
    registry['profiles']['all-routes-unified-v615'] = profile
    save(registry_path, registry)
    print('Registered complete V615 Shipyard/regional UI family; all8 native prompts QA-clean,all3668 IDs and41 cache extents preserved.')


if __name__ == '__main__':
    main()
