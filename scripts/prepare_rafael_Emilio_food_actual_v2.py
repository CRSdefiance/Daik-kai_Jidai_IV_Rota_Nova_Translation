"""Initialize only the nine-speech food/recruitment exchange using exact current commands."""
from pathlib import Path
from scripts import prepare_rafael330_actual_fixtures_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

FOOD_IDS={f'DK4_MES_B81_R{n:04d}' for n in [202,206,209,213,216,220,224,228,231]}
source=checked_text(Path(previous.__file__).read_text(encoding='utf-8'),{
    'Rafael330_actual_fixtures_20261105':'Rafael_Emilio_food_actual_v2_20261105',
    'Rafael330_stored_consumer_inputs_20261105':'Rafael330_stored_consumer_inputs_v2_20261105',
    'Rafael330_stored_native_20261105':'Rafael330_stored_native_v2_20261105',
    "[('B81_complete_bullfight','whole',24001),('names_pages_FE_transitions','display',18001),('B84_two_andthree_choice','menus',10001)]":
        "[('B81_food_recruitment','food',7201)]",
    "blocklist=[81] if mode=='whole'":"blocklist=[81] if mode in ['whole','food']",
    "keep=(text and text['id'] in selected) if mode=='display' else ((text and text['id'] in ['DK4_MES_B84_R0215','DK4_MES_B84_R0417','DK4_MES_B84_R0487']) or command['word'] in [0x2100,0x2200])":
        "keep=bool(text and text['id'] in FOOD_IDS)",
    "        changed=list(bank);changed[44]=fixtureblock;":
        "        assert {b['id'] for b in bindings}==FOOD_IDS and len(bindings)==9\n        changed=list(bank);changed[44]=fixtureblock;",
    'rom_retention_pins.Rafael330_actual.pending.json':'rom_retention_pins.Rafael_Emilio_food_v2.pending.json',
    'Prepared full51-speech B81/101-command scene,focused16-name/FE/page sequence andtwo/three-choice fixture;actual observations pending.':
        'Prepared one nine-speech food/recruitment exchange;full prior bullfight/menu/name runs are not repeated.',
})
exec(compile(source,__file__+'::same-initializers-controls-andparent-inverse-nine-food-speeches-only','exec'),globals())
