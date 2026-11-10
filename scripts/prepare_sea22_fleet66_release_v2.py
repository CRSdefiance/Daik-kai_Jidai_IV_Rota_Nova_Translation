"""Preserve failed v1 references and source guards; compare files once and release temporary images."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_sea22_fleet66_release_v1.py').read_text(encoding='utf-8'),{
    'import os\n':'import os\nimport gc\n',
    "ROOT=Path('work/analysis/Sea22_Fleet66_release_20261104')":"ROOT=Path('work/analysis/Sea22_Fleet66_release_v2_20261104')",
    'translations/sea_help22_editorial_release_v1.json':'translations/sea_help22_editorial_release_v2.json',
    'translations/fleet_help66_amendment_release_v1.json':'translations/fleet_help66_amendment_release_v2.json',
    '_sea22_fleet66_release_v1.json':'_sea22_fleet66_release_v2.json',
    "            assert [p for _,p,b in image.iter_files()if target.read_file(p)!=b]==[doc['file_path']]":
        "            assert [(p,q)for (_,p,b),(_,q,c)in zip(image.iter_files(),target.iter_files(),strict=True)if p!=q or b!=c]==[(doc['file_path'],doc['file_path'])]",
    "                path=ROOT/f'layer{layer}_stage{i}_RESEARCH_REFERENCE.nds';target.save(path)":
        """                existing=Path('work/analysis/Sea22_Fleet66_release_20261104')/f'layer{layer}_stage{i}_RESEARCH_REFERENCE.nds'
                if layer==0 and existing.exists():
                    assert bytes(target.rom.save())==existing.read_bytes();path=existing
                else:
                    path=ROOT/f'layer{layer}_stage{i}_RESEARCH_REFERENCE.nds';target.save(path)""",
    '            states.append(path)':'            states.append(path)\n            del image,target,inverse\n            gc.collect()',
    'release_stack.sea22_fleet66.pending.json':'release_stack.sea22_fleet66_v2.pending.json',
    'rom_retention_pins.sea22_fleet66.pending.json':'rom_retention_pins.sea22_fleet66_v2.pending.json',
})
exec(compile(source,__file__+'::same-ordered-pure-plans-stage-contracts-and-atomic-registration-with-bounded-file-comparison','exec'),globals())
