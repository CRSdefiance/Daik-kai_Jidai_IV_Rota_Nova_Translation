"""Exact trusted B51 source adapter bindings survive release-dependency challenge tests."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B51_profile_v1 import contract
ADAPTERS={'pages': ('work/analysis/Hodram_B51_source_display_v8556/source_display.json', 'source_owned_target_page_adapter'), 'dispatch': ('work/analysis/Hodram_B51_source_display_v8556/source_display.json', 'source_owned_dispatch_adapters'), 'macro_body': ('work/analysis/Hodram_B51_source_display_v8556/source_display.json', 'source_owned_macro_body_adapter'), 'progressive_macro': ('work/analysis/Hodram_B51_source_display_v8556/source_display.json', 'source_owned_progressive_adapter'), 'seeded_end': ('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json', 'source_owned_seeded_end_adapter'), 'entry': ('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json', 'source_owned_entry_adapter'), 'skip': ('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json', 'source_owned_skip_probe'), 'query': ('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json', 'source_owned_query_probe')}
TRUSTED={'work/analysis/Hodram_B51_source_display_v8556/source_display.json': 'd0c3ac21329bbe11862db49e6a9cbb45a7ece9967c00f148d10adb1f991b42a8', 'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json': '68e5e6da1254fac674062be1e342d3ac6f216b3194f00bb11c384592e49745b6'}

def trusted_adapter(name,declared):
    if name not in ADAPTERS:raise ValueError('B51 native adapter:unknown source consumer')
    text,key=ADAPTERS[name];path=Path(text);raw=path.read_bytes();digest=sha(raw);frozen=contract()
    if digest!=TRUSTED[text] or (str(path.resolve()) in frozen['dependencies'] and frozen['dependencies'][str(path.resolve())]!=digest):
        raise ValueError('B51 native adapter:exact trusted source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:raise ValueError('B51 native adapter:exact trusted source-owned adapter required:'+name)
    return expected
