"""Bind the existing advanced census file without importing its CLI-only namespace."""
from scripts.save_rafael_B181_B200_release_checkpoint_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'from scripts.qualify_rafael_B201_B220_clean_census_v2 import OUT as NEXT_CENSUS':
        "NEXT_CENSUS = Path('work/analysis/Rafael_B201_B220_clean_20261106/clean_source_census_v2.json')",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-integrated-handoff-with-explicit-census-file', 'exec'),globals())
