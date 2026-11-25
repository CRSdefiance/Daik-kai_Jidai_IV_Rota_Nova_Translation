"""Bind the item names mentioned or described in Rafael B241–B260."""
from pathlib import Path
import struct

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.draft_rafael_B249_B260_clean_v1 import OUT as ROOT
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B221_B240_contextual_v1 import digest

CATALOGUE = Path('translations/all_item_names_arm9_v1.json')
CURRENT = ROOT/'current_effective.json/current_effective.json'
OUT = ROOT/'item_title_bindings_v1.json'
ITEMS = {
    52: ('不死鳥のバシネット', ['DK4_MES_B242_R0023','DK4_MES_B242_R0068'], []),
    53: ('巨大ゾウガメの盾', ['DK4_MES_B241_R0022'], []),
    95: ('悪魔を貫く矢', ['DK4_MES_B249_R0020','DK4_MES_B249_R0027'], []),
    97: (None, [], ['DK4_MES_B245_R0022']),
    99: (None, [], ['DK4_MES_B243_R0013','DK4_MES_B243_R0021']),
    127: ('凍てついたバラ', ['DK4_MES_B253_R0019'], []),
    134: ('嘆きの壺', ['DK4_MES_B256_R0006'], ['DK4_MES_B256_R0010']),
}


def main():
    assert not OUT.exists()
    current, catalogue = map(load,(CURRENT,CATALOGUE))
    rt = current['runtime']
    ctx = RegisteredRuntime(rt['release_proof'],rt['startup_proof'],captain=0)
    assert ctx.receipt() == rt
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    rows = {row['id']:row for row in catalogue['records']}
    ids = {row['id'] for group in current['groups'] for row in group['records']}
    bindings = []
    for item,(title,literal,descriptive) in ITEMS.items():
        ident = f'DK4_ITEM_POINTER_{item:03d}'
        row = rows[ident]
        at = row['offset']
        old = clean[at:at+4]
        new = ctx.arm[at:at+4]
        assert old.hex() == row['source_hex'].lower()
        source = string(clean,struct.unpack('<I',old)[0])
        target = string(ctx.raw,struct.unpack('<I',new)[0])
        assert target['text'] == row['english'] and (title is None or title == source['text'])
        assert set(literal+descriptive) <= ids
        bindings.append(dict(item_ID=item,registered_item_record=ident,pointer_field_offset=at,
            source=source,current=target,source_field_hex=old.hex(),current_field_hex=new.hex(),
            scoped_dialogue_ids=literal,descriptive_or_partial_title_ids=descriptive))
    save(OUT,dict(runtime=rt,items=bindings,new_credit=0,inventory_and_item_acquisition_unvisited=True,
        evidence={str(path):digest(path) for path in (CURRENT,CATALOGUE,Path(__file__))}))
    print([(r['item_ID'],r['source']['text'],r['current']['text']) for r in bindings])


if __name__ == '__main__':
    main()

