"""Focused Emilio name, coherent pagination and two-choice scene fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/create_hodram_representative_fixtures.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'Two complete revised scenes after original initializers; not natural event activation.':
        'Three focused revised scenes after original initializers; not natural event activation.',
    'work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json':
        'work/analysis/Hodram_B81_B89_name_research_20261101/research_reference.json',
    'work/analysis/Hodram_B61_B70_stored_native_20261101/stored_native_verification.json':
        'work/analysis/Hodram_B81_B89_stored_20261101/stored_native_verification.json',
    "    assert native['research_ROM_sha256'] == rebuilt['research_ROM_sha256']":
        "    assert native['reconstruction_sha256'] == rebuilt['story_reconstruction_sha256']",
    '[(67, 16001), (69, 8001)]':'[(84, 15001), (85, 7001), (87, 11001)]',
    'Hodram_pending_B{number}_20261101':'Hodram_B81_B89_B{number}_20261101',
    'Two full-script initialized scene fixtures prepared; no natural activation or gameplay coverage claimed yet.':
        'Three full-script initialized fixtures prepared for name, pagination andmenu QA; no natural activation or gameplay coverage yet.',
})
exec(compile(source,__file__+'::same-original-initializers-focused-scenes','exec'),globals())
