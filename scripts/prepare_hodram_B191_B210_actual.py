"""Build broad town and complete representative random-scene coldboot fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_hodram_B171_B190_actual.py').read_text(encoding='utf-8'), {
    'Hodram_B171_B190_actual_fixtures_20261104': 'Hodram_B191_B210_actual_fixtures_20261104',
    'Hodram_B171_B190_rebuilt_20261104': 'Hodram_B191_B210_rebuilt_20261104',
    'Hodram_B171_B190_stored_qualified_20261104': 'Hodram_B191_B210_stored_20261104',
    "stored['complete_stored_pages'] == 439": "stored['complete_stored_pages'] == 355",
    "[('sail_lesson', [171], True, 14001),\n                                       ('pirate_transition', [179], True, 14001),\n                                       ('town_exchanges', list(range(180, 191)), False, 44001)]":
    """[('town_exchanges', list(range(191, 200)), False, 42001),
                                       ('book_offer', [201], True, 10001),
                                       ('castle_letter', [208], True, 12001),
                                       ('parrot', [209], True, 10001),
                                       ('earrings', [210], True, 14001)]""",
    "[r['records'] for r in created] == [27, 30, 130]": "[r['records'] for r in created] == [128, 21, 20, 17, 27]",
    'B171–B190 disclosed initialized English QA fixture': 'B191–B210 disclosed initialized English QA fixture',
    'rom_retention_pins.B171_actual.pending.json': 'rom_retention_pins.B191_actual.pending.json',
    'Prepared three pinned content fixtures: full B171 menu scene, full B179 transitions, 11 complete town exchanges.':
        'Prepared five pinned content fixtures: nine town exchanges and complete B201/B208/B209/B210 random scenes.',
})
exec(compile(source, __file__ + '::same-complete-source-command-fixtures-current-scope', 'exec'), globals())
