"""Bind the batch's item/UI labels and spoken Mihwa identity to its own registered RAM."""
import inspect
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.write_rafael_B169_contextual_v1 import fields,getter
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    out=ROOT/'scoped_terms_reference_v1.json';assert not out.exists()
    current_path=ROOT/'current_v1/current_effective.json';current=load(current_path)
    ctx=RegisteredRuntime(current['runtime']['release_proof'],current['runtime']['startup_proof'],captain=3)
    assert ctx.receipt()==current['runtime']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    def field(offset,source,english):
        sp,cp=[struct.unpack_from('<I',raw,offset)[0] for raw in [clean,ctx.arm]]
        a,b=string(clean,sp),string(ctx.raw,cp)
        assert a['text']==source and b['text']==english
        return dict(pointer_field_offset=offset,source=a,current=b,
                    source_field_hex=clean[offset:offset+4].hex(),current_field_hex=ctx.arm[offset:offset+4].hex())
    item_path=Path('translations/all_item_names_arm9_v1.json');registered={r['offset']:r for r in load(item_path)['records'] if 'english' in r}
    items=[]
    for offset,source,english in [(1172008,'トマトの苗木','Tomato Seedling'),
        (1172752,'掃滅のカッツバルゲル','Sweeping Katzbalger'),
        (1173496,'抜け忍の黒装束','Ninja Garb'),
        (1174216,'奇跡の弾丸のペンダント','Miracle Bullet Charm'),
        (1175272,'新羅の金冠','Silla Gold Crown')]:
        row=field(offset,source,english);assert registered[offset]['english']==english
        row['registered_record']=registered[offset]['id'];items.append(row)
    ui=[field(0x118eb0,'改造','Remodel'),field(0x1483ac,'運勢','Luck'),field(0x1483a8,'精神','Spirit')]
    code=checked_text(inspect.getsource(getter),{'for ident in [2,4,13,23,109]:':'for ident in [201]:'})
    env={**getter.__globals__};exec(compile(code,__file__+'::same-original-getters-spoken-Mihwa','exec'),env)
    names=ctx.execute(env['names']);consumers=names['rows']
    assert len(consumers)==2 and {r['consumer'] for r in consumers}=={'progressive-nameplate','full-catalogue'}
    assert all(r['actor_ID']==201 and r['text']=='Mihwa' for r in consumers)
    name_fields=fields(201,clean,ctx);assert name_fields[0]['source']['text']=='美華'
    prior_path=Path('translations/hodram_B301_B310_scoped_names_review_v1.json');prior=load(prior_path)
    # The established public spelling was individually reviewed before this batch.
    def find(value):
        if isinstance(value,dict):
            if value.get('actor_ID')==201 and value.get('approved_forms')=={'progressive-nameplate':'Mihwa','full-catalogue':'Mihwa'}:yield value
            for v in value.values():yield from find(v)
        elif isinstance(value,list):
            for v in value:yield from find(v)
    prior_rows=list(find(prior));assert len(prior_rows)==1 and prior_rows[0]['decision']=='retention'
    ctx.calls.clear()
    save(out,dict(runtime=ctx.receipt(),items=items,UI=ui,
        spoken_Mihwa=dict(actor_ID=201,source_andcurrent_fields=name_fields,current_consumers=consumers,
            prior_individual_review=dict(path=str(prior_path),sha256=digest(prior_path),finding=prior_rows[0]['finding']),
            decision='retention',finding='Retain established Mihwa for 美華, distinct from Maria Huamei/華梅. Provisional Meihua in the clean draft is not a new naming approval; Hangzhou alone does not establish a different reading or nationality.'),
        source_Katzbalger_description_does_not_identify_named_Sweeping_Katzbalger=True,
        bullet_pendant_reputation_not_confirmed_magic=True,
        natural_generic_plant_description_does_not_require_title_case=True,
        read_only_bindings_not_new_font_or_actual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [current_path,item_path,prior_path,Path(__file__)]}))
    print('Bound five exact item labels, Remodel/Luck/Spirit, and both Mihwa getters; offline reference only, zero credit.')

if __name__=='__main__':main()
