"""Bind draft terminology and identify remaining name-field leads, without approving display."""
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_rafael_B0_B34_clean_v1 import ROOT, SEALED
from scripts.write_rafael_B169_contextual_v1 import fields


RELEASE = Path('work/rafael4903_release_v1/registered_release_verification.json')
STARTUP = Path('work/rafael4903_release_v1/own_registered_startup_verification.json')
OUT = ROOT / 'scoped_terms_and_name_field_leads_v1.json'
ITEMS = Path('translations/all_item_names_arm9_v1.json')
PRIOR = Path('translations/rafael_B281_B300_integrated_final_review_v1.json')


def main():
    assert not OUT.exists()
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=0)
    jp = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    drafts = load(SEALED/'sealed_drafts.json')
    actors = sorted({r['source_selector'] for r in drafts['records']})
    assert actors == [0,4,5,6,7,8,12,13,16,17,19,20,23,25,27,30,31,35,36,37,39,40,41,
                      48,49,59,61,62,63,65,69,70,71,151,153,176,183,184,185]
    bindings = [dict(actor_ID=i, source_andcurrent_fields=fields(i,jp,ctx)) for i in actors]
    xien = fields(10,jp,ctx)
    assert xien[0]['source']['text'] == 'シエン' and xien[0]['current']['text'] == 'Xien'
    registered = {r['offset']:r for r in load(ITEMS)['records'] if 'english' in r}
    items = []
    for offset, source, english in [(1172848,'血塗られたシャムシール','Bloodstained Shamshir'),
                                     (1173136,'妖刀村正','Muramasa')]:
        sp, cp = [struct.unpack_from('<I', raw, offset)[0] for raw in (jp,ctx.arm)]
        original, target = string(jp,sp), string(ctx.raw,cp)
        assert original['text'] == source and target['text'] == registered[offset]['english'] == english
        items.append(dict(pointer_field_offset=offset, source=original,current=target,
            registered_record=registered[offset]['id']))
    proof = next(r for r in load(PRIOR)['records'] if r['id']=='DK4_MES_B300_R0063')
    assert '覇者' in proof['source_Japanese'] and 'Proof of Conquest' in proof['english']
    assert all(proof['review'].values())
    leads = []
    for row in bindings:
        for field in row['source_andcurrent_fields']:
            text = field['current']['text']
            if any('\uff01' <= char <= '\uff5e' or '\u3040' <= char <= '\u30ff' for char in text):
                leads.append(dict(actor_ID=row['actor_ID'],column=field['column'],text=text,
                    field=field,scope='Stored name-field lead; final consumer localization and glyph review pending.'))
    save(OUT,dict(runtime=ctx.receipt(),scoped_actor_fields=bindings,Xien_source_andcurrent_fields=xien,
        registered_items=items,Proof_of_Conquest=dict(reference=str(PRIOR),record_ID=proof['id'],
            source_reference=proof['source_reference'],english=proof['english']),
        remaining_name_field_leads=leads,does_not_approve_all_names_or_display_consumers=True,
        iron_armored_ship_terminology_pending_consumer_review=True,new_credit=0,
        evidence={str(p):digest(p) for p in (RELEASE,STARTUP,ITEMS,PRIOR,SEALED/'sealed_drafts.json',Path(__file__))}))
    print('Bound Xien, Proof of Conquest and both named weapons;',len(leads),'stored name-field leads remain.')


if __name__ == '__main__':
    main()
