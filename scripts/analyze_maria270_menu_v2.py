"""Follow the exact stored-menu bridge to its original complete native receipt.

v1 rejected the bridge's lack of raster records before producing output. This
successor resolves and hash-checks those records without repeating native QA.
"""
from pathlib import Path
from scripts.analyze_maria270_menu_v1 import source,verified_existing_unlock
from dk4tool.rom.nds import NdsImage
from scripts.qualify_maria270_market_parent_v1 import qualify
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def qualified_menu_dependencies(image,proof):
    target,receipt=qualify(proof['runtime'])
    assert image.read_file('/__arm9__.bin')==target.read_file('/__arm9__.bin')
    original=NdsImage.open(proof['runtime']['candidate'])
    for resource in ['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:
        assert image.read_file(resource)==original.read_file(resource)==target.read_file(resource)
    return receipt

def menu_scopes(paths):
    fixture=load(args.fixture)
    declared={(m['block'],m['source_command_offset']) for m in fixture['menus']}
    seen=set()
    for path in paths:
        bridge=load(path)
        for menu in bridge['menus']:
            key=(menu['block'],menu['source_command_offset'])
            if key not in declared:continue
            assert key not in seen;seen.add(key)
            receipt=Path(menu['original_receipt'])
            assert digest(receipt)==menu['original_receipt_sha256']
            proof=load(receipt)
            assert proof['runtime']==bridge['runtime']
            assert proof['versions'][-1]['object_hex']==menu['target_object_hex']
            yield receipt,{**proof,'source_menu_scope':key}
    assert seen==declared

if __name__=='__main__':
    exec(compile(source,__file__+'::complete-native-receipts-through-exact-stored-menu-bridge','exec'),globals())
