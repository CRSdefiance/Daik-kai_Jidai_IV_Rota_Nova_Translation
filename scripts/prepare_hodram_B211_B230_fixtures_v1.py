"""Reuse complete native-command fixtures with Hodram's own original initializers."""
from scripts import prepare_reviewed_dialogue_fixtures_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json':
        'work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json',
    "path == '/data/SC0.DK4'":"path == '/data/SC1.DK4'",
    'bank[44]':'bank[42]',
    'changed[44]':'changed[42]',
    'first == 40 and len([c for c in opening if c[\'offset\'] < first]) == 10':
        'first == 42 and len([c for c in opening if c[\'offset\'] < first]) == 8',
    "r['expanded_hex'] for r in [*stored['records'],*stored['style_records']]":
        "(r['stored_hex'] if r.get('virtual_prefix_not_stored') else r['expanded_hex']) for r in [*stored['records'],*stored['style_records']]",
})
exec(compile(source,__file__+'::same-initialized-fixtures-own-Hodram-no-state-override','exec'),globals())
