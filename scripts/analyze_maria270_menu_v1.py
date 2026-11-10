"""Match each declared Maria270 menu against its complete source-scoped native proof.

The only ARM9 change since the offline proof is the separately qualified market
literal transform. Renderer/code/COMMON/font dependencies remain exact.
"""
from pathlib import Path
from scripts.analyze_native_choice_fixture_samples_v3 import source as previous,menu_scopes as original_scopes
from scripts.analyze_maria301_display_v1 import verified_existing_unlock
from scripts.qualify_maria270_market_parent_v1 import qualify
from scripts.source_locked_derivation_v5118 import checked_text

def menu_scopes(paths):
    fixture=load(args.fixture)
    declared={(m['block'],m['source_command_offset']) for m in fixture['menus']}
    seen=set()
    for path,proof in original_scopes(paths):
        key=tuple(proof['source_menu_scope'])
        if key in declared:
            assert key not in seen;seen.add(key)
            yield path,proof
    assert seen==declared

def qualified_menu_dependencies(image,proof):
    target,receipt=qualify(proof['runtime'])
    assert image.read_file('/__arm9__.bin')==target.read_file('/__arm9__.bin')
    original=NdsImage.open(proof['runtime']['candidate'])
    for resource in ['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:
        assert image.read_file(resource)==original.read_file(resource)==target.read_file(resource)
    return receipt

source=checked_text(previous,{
    " and not report.get('battery_save_preloaded')":' and verified_existing_unlock(report)',
    "        original=NdsImage.open(proof['runtime']['candidate'])\n        for resource in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert image.read_file(resource)==original.read_file(resource)":
        "        qualified_market_parent=qualified_menu_dependencies(image,proof)",
    'actual_gameplay=True,disclosed_initialized_fixture=True,':
        'actual_gameplay=True,disclosed_initialized_fixture=True,existing_system_only_unlock_not_earned=True,exact_registered_market_parent_reuse=qualified_market_parent,',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::complete-declared-menu-pixels-andqualified-market-only-parent','exec'),globals())
