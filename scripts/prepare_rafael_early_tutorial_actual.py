"""Preserve complete tutorial commands behind Rafael's original initialized opening."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_hodram_B171_B190_actual.py').read_text(encoding='utf-8'), {
    'Hodram_B171_B190_actual_fixtures_20261104': 'Rafael_early_tutorial_B42_B43_actual_fixtures_20261104',
    'Hodram_B171_B190_rebuilt_20261104/reconstruction.json': 'Rafael_early_tutorial_B42_B43_storage_20261104/reconstruction_v2/reconstruction.json',
    'Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json': 'Rafael_early_tutorial_B42_B43_storage_20261104/stored_native_v1/stored_native_verification.json',
    'work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json':
        'work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json',
    "stored['complete_stored_pages'] == 439": "stored['complete_stored_pages'] == 42",
    '/data/SC1.DK4': '/data/SC0.DK4',
    'bank[42]': 'bank[44]', 'changed[42]': 'changed[44]',
    'assert first == 42 and len([c for c in opening if c[\'offset\'] < first]) == 8':
        'assert first == 40 and len([c for c in opening if c[\'offset\'] < first]) == 10',
    "[('sail_lesson', [171], True, 14001),\n                                       ('pirate_transition', [179], True, 14001),\n                                       ('town_exchanges', list(range(180, 191)), False, 44001)]":
        "[('first_voyage', [42], True, 14001), ('crew_duties', [43], True, 11001)]",
    "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'", "b'Bergstrom Fleet'": "b'Castor Co.'",
    "[r['records'] for r in created] == [27, 30, 130]": "[r['records'] for r in created] == [28, 12]",
    'B171–B190 disclosed initialized English QA fixture': 'Rafael B42/B43 complete-command initialized English tutorial QA fixture',
    'rom_retention_pins.B171_actual.pending.json': 'rom_retention_pins.Rafael_early_tutorial_actual.pending.json',
    'Prepared three pinned content fixtures: full B171 menu scene, full B179 transitions, 11 complete town exchanges.':
        'Prepared two pinned complete tutorial fixtures: 28 first-voyage speeches and 12 crew-duty speeches with all original commands.',
})
exec(compile(source, __file__ + '::same-whole-scene-fixtures-current-Rafael-opening', 'exec'), globals())
