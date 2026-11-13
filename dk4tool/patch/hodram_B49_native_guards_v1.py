"""Exact trusted B49 source adapter bindings survive release-dependency challenge tests."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B49_profile_v2 import contract
ADAPTERS={'pages': ('work\\analysis\\Hodram_B49_source_display_v8386b\\source_display.json', 'source_owned_target_page_adapter'), 'dispatch': ('work\\analysis\\Hodram_B49_source_display_v8386b\\source_display.json', 'source_owned_dispatch_adapters'), 'macro_body': ('work\\analysis\\Hodram_B49_source_display_v8386b\\source_display.json', 'source_owned_macro_body_adapter'), 'progressive_macro': ('work\\analysis\\Hodram_B49_source_display_v8386b\\source_display.json', 'source_owned_progressive_adapter'), 'FE_macro': ('work\\analysis\\Hodram_B49_source_display_v8386b\\source_display.json', 'source_owned_FE_adapter'), 'seeded_end': ('work\\analysis\\Hodram_B49_source_controls_v8384\\source_controls.json', 'source_owned_seeded_end_adapter'), 'picture': ('work\\analysis\\Hodram_B49_source_controls_v8384\\source_controls.json', 'source_owned_picture_adapter'), 'menu_VM': ('work\\analysis\\Hodram_B49_menu_v8400\\menu_provider_and_planes.json', 'source_owned_VM_adapter'), 'menu_painter': ('work\\analysis\\Hodram_B49_menu_v8400\\menu_provider_and_planes.json', 'source_owned_painter_adapter')}
TRUSTED={'work\\analysis\\Hodram_B49_source_display_v8386b\\source_display.json': '173a56ac4c2fa7edc9020d3486f0e9cb5f7d82cdf45e71bff5aeff6fdf616645', 'work\\analysis\\Hodram_B49_source_controls_v8384\\source_controls.json': '746ee2d43b59109c410e6c1d7b0d1154bbaa0dea582d05d3b03be33f869ba153', 'work\\analysis\\Hodram_B49_menu_v8400\\menu_provider_and_planes.json': '5135516bda8c29c4c2402e5d516b86e91137891099de57e1bd1d406f039fa7f7'}

def trusted_adapter(name,declared):
    if name not in ADAPTERS:raise ValueError('B49 native adapter:unknown source consumer')
    text,key=ADAPTERS[name];path=Path(text);raw=path.read_bytes();digest=sha(raw);frozen=contract()
    if digest!=TRUSTED[text] or (str(path.resolve()) in frozen['dependencies'] and frozen['dependencies'][str(path.resolve())]!=digest):
        raise ValueError('B49 native adapter:exact trusted source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:raise ValueError('B49 native adapter:exact trusted source-owned adapter required:'+name)
    return expected
