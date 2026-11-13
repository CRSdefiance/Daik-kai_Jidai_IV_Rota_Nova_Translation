"""Trusted frozen adapter bindings remain enforced when release dependency checks are challenged."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v8 import contract
SOURCE=Path('work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json')
CONTROLS=Path('work/analysis/Hodram_B47_B48_source_controls_v8314/two_EV1_entries15_commands6_preambles7_opaque_effect_pairs50_complete_seeded_ends.json')
ADAPTERS={
    'pages':(SOURCE,'source_owned_target_page_adapter'),
    'dispatch':(SOURCE,'source_owned_dispatch_adapters'),
    'macro_body':(SOURCE,'source_owned_macro_body_adapter'),
    'progressive_macro':(SOURCE,'source_owned_progressive_adapter'),
    'FE_macro':(SOURCE,'source_owned_FE_adapter'),
    'seeded_end':(CONTROLS,'source_owned_seeded_end_adapter'),
}

def trusted_adapter(name,declared):
    path,key=ADAPTERS[name];frozen=contract();raw=path.read_bytes()
    if frozen['dependencies'].get(str(path.resolve()))!=sha(raw):
        raise ValueError('Hodram native adapter: original frozen source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:
        raise ValueError('Hodram native adapter: exact trusted source-owned adapter required:'+name)
    return expected
