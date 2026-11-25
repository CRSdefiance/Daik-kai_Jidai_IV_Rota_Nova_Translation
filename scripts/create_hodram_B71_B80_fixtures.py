"""Source-locked reuse of complete-scene initialization; no gameplay credit yet."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/create_hodram_representative_fixtures.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'Two complete revised scenes after original initializers; not natural event activation.':
        'B72 dialogue/paging and B76 FE notices after original initializers; not natural event activation.',
    'work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json':
        'work/analysis/Hodram_B71_B80_rebuilt_20261101/reconstruction.json',
    'work/analysis/Hodram_B61_B70_stored_native_20261101/stored_native_verification.json':
        'work/analysis/Hodram_B71_B80_stored_20261101/stored_native_verification.json',
    "native['research_ROM_sha256'] == rebuilt['research_ROM_sha256']":
        "native['reconstruction_sha256'] == sha(rebuild_path.read_bytes())",
    '[(67, 16001), (69, 8001)]':'[(72, 18001), (76, 7001)]',
    "Hodram_pending_B{number}_20261101":"Hodram_B71_B80_B{number}_20261101",
})
exec(compile(source,__file__+'::unchanged-initialization-and-script-copy','exec'),globals())
