"""Use Madeira's existing docked defender from the actual departure snapshot.

Amsterdam's defender had already sailed by frame5000;the predecessor's
presence guard stopped before any output. No defender is created or moved.
"""
import inspect
from scripts import native_aftermath_city_fixture_v1282 as previous

ROM = previous.ROM


def apply_fixture(arm,raw,request):
    source = inspect.getsource(previous.apply_fixture)
    replacements = {
        "{'city_context':'Amsterdam'}":"{'city_context':'Madeira'}",
        'fleets+4+2*132':'fleets+4+22*132',
        'get(0x35320,defender) == 1':'get(0x35320,defender) == 6',
        'get(0x34674,defender) == 2':'get(0x34674,defender) == 30',
        'get(0x7EE08,get(0x3697C,defender)) == 2':'get(0x7EE08,get(0x3697C,defender)) == 46',
        'town = towns+4+2*108':'town = towns+4+30*108',
        'get(0xB4AA8,town,1)':'get(0xB4AA8,town,6)',
        'get(0xCD6B8,2)':'get(0xCD6B8,30)',
        'companies+4+76':'companies+4+6*76',
        'companies+4+2*76+0x1F+1':'companies+4+2*76+0x1F+6',
        "'context':'Amsterdam_city_approach'":"'context':'Madeira_city_approach'",
        "'town_ID':2":"'town_ID':30",
        "'original_defender_fleet_ID':2":"'original_defender_fleet_ID':22",
        "'original_defender_captain_ID':2":"'original_defender_captain_ID':46",
    }
    for old,new in replacements.items():
        assert source.count(old) >= 1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__}
    exec(compile(source,__file__,'exec'),env)
    return env['apply_fixture'](arm,raw,request)
