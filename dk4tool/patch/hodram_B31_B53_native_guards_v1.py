"""Exact trusted B31/B53 source adapter bindings survive release-dependency challenge tests."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import contract
ADAPTERS={'pages': ('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json', 'source_owned_target_page_adapter'), 'dispatch': ('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json', 'source_owned_dispatch_adapters'), 'macro_body': ('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json', 'source_owned_macro_body_adapter'), 'progressive_macro': ('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json', 'source_owned_progressive_adapter'), 'seeded_end': ('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json', 'source_owned_seeded_end_adapter'), 'entry': ('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json', 'source_owned_entry_adapter'), 'skip': ('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json', 'source_owned_skip_probe'), 'query': ('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json', 'source_owned_query_probe')}
TRUSTED={'work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json': 'd052892fa0047378b78f38ae2da882d52f8d3efa5c4e3dc5f70e69460de624ff', 'work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json': '7c0145b879065b4e318785970b411699fa5963e3c9e4834b5970d4a8e7a1fcc9'}

def trusted_adapter(name,declared):
    if name not in ADAPTERS:raise ValueError('B31/B53 native adapter:unknown source consumer')
    text,key=ADAPTERS[name];path=Path(text);raw=path.read_bytes();digest=sha(raw);frozen=contract()
    if digest!=TRUSTED[text] or (str(path.resolve()) in frozen['dependencies'] and frozen['dependencies'][str(path.resolve())]!=digest):
        raise ValueError('B31/B53 native adapter:exact trusted source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:raise ValueError('B31/B53 native adapter:exact trusted source-owned adapter required:'+name)
    return expected
