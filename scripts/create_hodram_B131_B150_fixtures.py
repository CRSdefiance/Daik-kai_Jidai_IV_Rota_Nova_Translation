"""Initialize complete checked scripts for representative QA, retaining all source conditions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/create_hodram_representative_fixtures.py').read_text(encoding='utf-8'), {
    'Hodram_B61_B70_stored_20261101/reconstruction.json': 'Hodram_B131_B150_name_research_20261102/research_reference.json',
    'Hodram_B61_B70_stored_native_20261101/stored_native_verification.json': 'Hodram_B131_B150_stored_20261102/stored_native_verification.json',
    "    assert native['research_ROM_sha256'] == rebuilt['research_ROM_sha256']":
    "    assert native['reconstruction_sha256']==rebuilt['story_reconstruction_sha256']\n    assert native['reconstruction']==rebuilt['story_reconstruction']",
    '[(67, 16001), (69, 8001)]': '[(133,8001),(136,10001),(142,24001),(143,12001)]',
    "Hodram_pending_B{number}_20261101": "Hodram_B131_B150_English_20261102_B{number}",
    'Two full-script initialized scene fixtures prepared; no natural activation or gameplay coverage claimed yet.':
    'Four full-script initialized scene fixtures prepared; no natural activation or gameplay coverage claimed yet.',
})
exec(compile(source, __file__ + '::original-initializers-complete-targets-no-condition-overrides', 'exec'), globals())
