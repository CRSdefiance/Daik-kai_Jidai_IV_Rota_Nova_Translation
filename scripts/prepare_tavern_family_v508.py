"""Source-lock the Tavern formatter repair and create a research-only byte image."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_family_wrap import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries


def main():
    out = Path('work/analysis/tavern_family_v508')
    out.mkdir(parents=True,exist_ok=True)
    rom = NdsImage.open('out/all_routes_combined_v502_candidate.nds')
    common,arm = rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    manuscript_path = Path('translations/tavern_toast_manuscript_v1.json')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))[827]
    row = manuscript['records'][0]
    assert source.text.hex() == row['source_hex'] and source.text.decode('cp932') == row['japanese']
    target_common,target_arm,change = transform(common,arm,manuscript)
    config = {'format':'dk4-tavern-family-wrap-v1','source_common_sha256':sha(common),
              'source_arm9_sha256':sha(arm),'target_common_sha256':sha(target_common),
              'target_arm9_sha256':sha(target_arm),'manuscript':str(manuscript_path),
              'manuscript_sha256':sha(manuscript_path.read_bytes()),
              'helper_asm_sha256':sha(Path('dk4tool/patch/tavern_paragraph_helper.asm').read_bytes()),'scope':change}
    Path('translations/tavern_family_wrap_v1.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
    rom.replace_file('/COMMON/MESFILE.DK4',target_common)
    rom.replace_file('/__arm9__.bin',target_arm)
    rom.save(out/'research_only_tavern_family.nds')
    (out/'target_arm9.bin').write_bytes(target_arm)
    (out/'target_common.bin').write_bytes(target_common)
    print(json.dumps(config,indent=2))


if __name__ == '__main__':
    main()
