"""Reuse the qualified complete-block reconstruction for15 reviewed SC3 exchanges."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/rebuild_maria337_reviewed_v1.py').read_text(encoding='utf-8'),{
    'from scripts.meaning_maria337_clean_v1 import ROOT':'from scripts.meaning_maria335_B137_B151_v1 import ROOT',
    "ROOT/'plan_visual_v5/automatic_plans.json'":"ROOT/'plan_native_v4/automatic_plans.json'",
    '==(337,335,335,339)':'==(335,333,333,333)',
    'list(range(125,137))':'list(range(137,152))',
    "approval['all339_final_pages_directly_viewed']":"approval['all333_final_pages_directly_viewed']",
    'len(ordinary)==335':'len(ordinary)==333',
    'len(groups)==12':'len(groups)==15',
    "sum(len(g['text_records']) for g in groups)==335":"sum(len(g['text_records']) for g in groups)==333",
    'source_editorial_objects=337,source_speeches=335,speech_count=335':'source_editorial_objects=335,source_speeches=333,speech_count=333',
    'total_rendered_speech_count=335':'total_rendered_speech_count=333',
    'rom_retention_pins.Maria337.pending.json':'rom_retention_pins.Maria335B137B151.pending.json',
    'Preserve Maria337 source-qualified':'Preserve Maria335 B137-B151 source-qualified',
    'source_objects=337,physical_bodies=335,reviewed_blocks=12':'source_objects=335,physical_bodies=333,reviewed_blocks=15',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-block-controls-relative-fixups-storage-andinverse-guards','exec'),globals())
