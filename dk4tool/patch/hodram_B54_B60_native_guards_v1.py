"""Exact trusted B54-B60 source adapter bindings survive release-dependency challenge tests."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B54_B60_profile_v1 import contract
ADAPTERS={'pages': ('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json', 'source_owned_target_page_adapter'), 'dispatch': ('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json', 'source_owned_dispatch_adapters'), 'macro_body': ('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json', 'source_owned_macro_body_adapter'), 'progressive_macro': ('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json', 'source_owned_progressive_adapter'), 'seeded_end': ('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json', 'source_owned_seeded_end_adapter'), 'entry': ('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json', 'source_owned_entry_adapter'), 'skip': ('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json', 'source_owned_skip_probe'), 'query': ('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json', 'source_owned_query_probe')}
TRUSTED={'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json': '98af6074aab672ac5d6f9f76bed8b01df17f6a0a2d6c556bc7ec9dbb9e7f6214', 'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json': '2132eb62828abb94fda9df16f45a1a378c6d17a9d969de8655d5742f153e88b1'}

def trusted_adapter(name,declared):
    if name not in ADAPTERS:raise ValueError('B54-B60 native adapter:unknown source consumer')
    text,key=ADAPTERS[name];path=Path(text);raw=path.read_bytes();digest=sha(raw);frozen=contract()
    if digest!=TRUSTED[text] or (str(path.resolve()) in frozen['dependencies'] and frozen['dependencies'][str(path.resolve())]!=digest):
        raise ValueError('B54-B60 native adapter:exact trusted source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:raise ValueError('B54-B60 native adapter:exact trusted source-owned adapter required:'+name)
    return expected
