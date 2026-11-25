"""Preserve stopped inspection; compare equivalent Windows registry paths canonically."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    derive('scripts/inspect_Hodram_B50_builder_v8531.py','scripts/inspect_Hodram_B50_builder_v8531b.py',{
        "profile['hodram_B49_editorial']=='translations/hodram_B49_editorial_release_v3.json'":"Path(profile['hodram_B49_editorial']).as_posix()=='translations/hodram_B49_editorial_release_v3.json'",
    })
