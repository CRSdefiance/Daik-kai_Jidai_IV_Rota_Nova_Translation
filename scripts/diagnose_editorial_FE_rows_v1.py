"""Inspect a concrete failed FE row-membership check on the exact registered consumer."""
import argparse
from pathlib import Path
from types import FunctionType
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['manuscript','plan','release','startup','out']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--record',required=True);a=p.parse_args();assert not a.out.exists()
    doc,plans=map(load,[a.manuscript,a.plan]);assert plans['manuscript_sha256']==digest(a.manuscript)
    row=next(r for r in doc['records'] if r['id']==a.record);plan=next(r for r in plans['records'] if r['id']==a.record)
    assert row['kind']=='system-FE' and row['source_selector']==254
    ctx=RegisteredRuntime(a.release,a.startup);assert ctx.receipt()==doc['runtime']
    ascii_factory=FunctionType(old_font.make_painter.__code__,{**old_font.make_painter.__globals__,'CURRENT_ARM9':digest_bytes(ctx.arm)},argdefs=old_font.make_painter.__defaults__)
    factory=FunctionType(source_FE.make_source_painter.__code__,{**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':digest_bytes(ctx.arm),'ASCII_painter':ascii_factory},argdefs=source_FE.make_source_painter.__defaults__)
    painter,calibration=factory(ctx.image)
    encoded=bytes.fromhex(plan['encoded_hex']);assert encoded[0]==254
    text=encoded[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
    rendered=painter(text);events=rendered['events']
    assert all(e['kind']=='ascii' and 0<=e['code']<128 for e in events)
    actual=[dict(y=y,text=bytes(e['code'] for e in events if e['y']==y).decode('ascii')) for y in sorted({e['y'] for e in events})]
    try:check_FE_rows(text,rendered)
    except AssertionError:failed=True
    else:failed=False
    assert failed
    expected_glyphs=bytes(c for c in text if c not in [10,32])
    actual_glyphs=bytes(e['code'] for e in events if e['code']!=32)
    save(a.out,dict(record=a.record,source_reference=row['source_reference'],current_reference=row['current_reference'],
        planned_lines=plan['lines'],encoded_hex=plan['encoded_hex'],actual_rows=actual,
        complete_nonspace_glyph_sequence_preserved=expected_glyphs==actual_glyphs,actual_row_membership_failed=True,
        no_ROM_font_engine_orprose_mutation=True,offline_only=True,new_credit=0,
        evidence={str(q):digest(q) for q in [a.manuscript,a.plan,a.release,a.startup,Path(__file__)]}))
    print(dict(record=a.record,planned_lines=plan['lines'],actual_rows=actual))

def digest_bytes(value):
    from dk4tool.patch.grand_race_menu_release import sha
    return sha(value)

if __name__=='__main__':main()
