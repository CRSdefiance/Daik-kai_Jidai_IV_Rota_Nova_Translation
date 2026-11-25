"""Reference registered names and terms after clean meanings, without story-English intake."""
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT, OUT as MEANINGS
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B169_contextual_v1 import fields

OUT = ROOT/'draft_names_andterms_reference_v1.json'
RELEASE = Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
STARTUP = RELEASE.with_name('own_registered_startup_verification.json')


def main():
    assert not OUT.exists()
    meanings = load(MEANINGS)
    assert meanings['records_count'] == 394
    assert all(digest(p) == h for p,h in meanings['evidence'].items())
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=0)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    actors = sorted({r['source_selector'] for r in meanings['records'] if r.get('source_selector',254)<207}
                    |{0,3})
    bindings = [dict(actor_ID=i, source_andcurrent_fields=fields(i,clean,ctx)) for i in actors]
    items = []
    labels = load('translations/all_item_names_arm9_v1.json')['records']
    for offset, expected in [(1172848,'血塗られたシャムシール'),(1173136,'妖刀村正')]:
        source_pointer,current_pointer = [struct.unpack_from('<I', data, offset)[0] for data in (clean,ctx.arm)]
        source,current = string(clean,source_pointer),string(ctx.raw,current_pointer)
        original = next(r for r in labels if r.get('offset')==offset)
        assert source['text'] == expected and current['text'] == original['english']
        items.append(dict(pointer_field_offset=offset,source=source,current=current,registered_record=original['id']))
    save(OUT,dict(records=bindings,registered_item_names=items,runtime=ctx.receipt(),
        source_meanings=str(MEANINGS),source_meanings_sha256=digest(MEANINGS),
        name_data_reference_only_not_new_name_localization_orconsumer_approval=True,
        current_eligible_story_English_not_extracted=True, native_role_assignment_andfuture_roster_not_inferred=True,
        remaining_UI_place_full_name_andglyph_binding_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in (RELEASE,STARTUP,MEANINGS,Path('translations/all_item_names_arm9_v1.json'),Path(__file__))}))
    for row in bindings:
        print(row['actor_ID'], [(f['source']['text'],f['current']['text']) for f in row['source_andcurrent_fields']])
    print('Items:',[(r['source']['text'],r['current']['text']) for r in items])


if __name__ == '__main__':
    main()
