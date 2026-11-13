"""Exact trusted B50 source adapter bindings survive release-dependency challenge tests."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B50_profile_v2 import contract
ADAPTERS={'pages': ('work\\analysis\\Hodram_B50_source_display_v8487\\source_display.json', 'source_owned_target_page_adapter'), 'dispatch': ('work\\analysis\\Hodram_B50_source_display_v8487\\source_display.json', 'source_owned_dispatch_adapters'), 'macro_body': ('work\\analysis\\Hodram_B50_source_display_v8487\\source_display.json', 'source_owned_macro_body_adapter'), 'progressive_macro': ('work\\analysis\\Hodram_B50_source_display_v8487\\source_display.json', 'source_owned_progressive_adapter'), 'FE_macro': ('work\\analysis\\Hodram_B50_source_display_v8487\\source_display.json', 'source_owned_FE_adapter'), 'seeded_end': ('work\\analysis\\Hodram_B50_source_controls_v8486\\source_controls.json', 'source_owned_seeded_end_adapter'), 'picture': ('work\\analysis\\Hodram_B50_source_controls_v8486\\source_controls.json', 'source_owned_picture_adapter')}
TRUSTED={'work\\analysis\\Hodram_B50_source_display_v8487\\source_display.json': 'b477a2fcb43f3164760b838a733cad0230e7bb48507923c0d9671da58a5f4615', 'work\\analysis\\Hodram_B50_source_controls_v8486\\source_controls.json': '90fcd790cd233a5e8219b49e905630c75a61e46ec79b4711d758a2974dd028aa'}

def trusted_adapter(name,declared):
    if name not in ADAPTERS:raise ValueError('B50 native adapter:unknown source consumer')
    text,key=ADAPTERS[name];path=Path(text);raw=path.read_bytes();digest=sha(raw);frozen=contract()
    if digest!=TRUSTED[text] or (str(path.resolve()) in frozen['dependencies'] and frozen['dependencies'][str(path.resolve())]!=digest):
        raise ValueError('B50 native adapter:exact trusted source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:raise ValueError('B50 native adapter:exact trusted source-owned adapter required:'+name)
    return expected
