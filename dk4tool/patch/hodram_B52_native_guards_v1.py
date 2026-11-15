"""Exact trusted B52 source adapter bindings survive release-dependency challenge tests."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import contract
ADAPTERS={'pages': ('work/analysis/Hodram_B52_source_display_v8626/source_display.json', 'source_owned_target_page_adapter'), 'dispatch': ('work/analysis/Hodram_B52_source_display_v8626/source_display.json', 'source_owned_dispatch_adapters'), 'macro_body': ('work/analysis/Hodram_B52_source_display_v8626/source_display.json', 'source_owned_macro_body_adapter'), 'progressive_macro': ('work/analysis/Hodram_B52_source_display_v8626/source_display.json', 'source_owned_progressive_adapter'), 'seeded_end': ('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json', 'source_owned_seeded_end_adapter'), 'entry': ('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json', 'source_owned_entry_adapter'), 'skip': ('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json', 'source_owned_skip_probe'), 'query': ('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json', 'source_owned_query_probe')}
TRUSTED={'work/analysis/Hodram_B52_source_display_v8626/source_display.json': '89248e189d089c9c63f9bc6b51cd94befa0aacb17a9fede0e1f33cc1974c279e', 'work/analysis/Hodram_B52_source_controls_v8620/source_controls.json': 'a0748b0a067f4e091d0f147f7a42883424252e0ec5784896105e1fc160c2a3b5'}

def trusted_adapter(name,declared):
    if name not in ADAPTERS:raise ValueError('B52 native adapter:unknown source consumer')
    text,key=ADAPTERS[name];path=Path(text);raw=path.read_bytes();digest=sha(raw);frozen=contract()
    if digest!=TRUSTED[text] or (str(path.resolve()) in frozen['dependencies'] and frozen['dependencies'][str(path.resolve())]!=digest):
        raise ValueError('B52 native adapter:exact trusted source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:raise ValueError('B52 native adapter:exact trusted source-owned adapter required:'+name)
    return expected
