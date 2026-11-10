"""Qualify this batch's data fields directly; preserve frozen prior native-address guards."""
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

ROOT=Path('work/Maria_B286_B302_clean_20261110')

def main():
    out=ROOT/'scoped_terms_reference_v1.json';assert not out.exists()
    current_path=ROOT/'current_v1/current_effective.json';current=load(current_path);runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    def field(offset,source,english):
        a,b=[string(raw,struct.unpack_from('<I',arm,offset)[0]) for arm,raw in [(clean,clean),(ctx.arm,ctx.raw)]]
        assert a['text']==source and b['text']==english
        return dict(pointer_field_offset=offset,source=a,current=b,source_field_hex=clean[offset:offset+4].hex(),current_field_hex=ctx.arm[offset:offset+4].hex())
    item_path=Path('translations/all_item_names_arm9_v1.json');labels={r['offset']:r for r in load(item_path)['records'] if 'english' in r}
    items=[]
    for offset,source,english in [(1172296,'錬金術の書','Alchemy Book'),(1174984,'六分儀','Sextant'),
            (1175464,'高麗青磁の香炉','Goryeo Incense Burner'),(1176112,'古代都市遺跡への地図','Ancient City Map')]:
        row=field(offset,source,english);assert labels[offset]['english']==english
        assert labels[offset]['source_hex'].lower()==row['source_field_hex']
        items.append(dict(row,registered_record=labels[offset]['id']))
    locations=[field(1192580,'サン＝ジョルジェ','Sao Jorge'),field(1196292,'ハバナ','Havana'),field(1422112,'グアム','Guam')]
    commodities=[field(p,j,e) for p,j,e in [(1437920,'金','Gold'),(1438220,'象牙','Ivory'),(1438496,'鉄砲','Guns'),(1438508,'大砲','Cannon'),(1438532,'甲冑','Armor')]]
    short=[field(1295216,'覇者の証','Proof'),field(1503776,'覇者の証','Conq Proof')]
    prior_path=Path('translations/maria310_integrated_final_review_v1.json');prior=load(prior_path)
    anchor=next(r for r in prior['records'] if r['id']=='DK4_MES_B53_R0006')
    assert anchor['english']=='That makes all the Proofs of Conquest...' and all(anchor['review'].values())
    old=NdsImage.open(prior['target_ROM']);assert digest(prior['target_ROM'])==prior['target_ROM_sha256']
    assert old.read_file('/__arm9__.bin')==ctx.arm and old.read_file('/COMMON/MESFILE.DK4')==ctx.common
    old_blocks=IlnkContainer.parse(old.read_file('/data/SC3.DK4')).blocks;blocks=IlnkContainer.parse(ctx.image.read_file('/data/SC3.DK4')).blocks
    assert blocks[53]==old_blocks[53]
    ref=anchor['planned_integrated_reference'];raw=bytes.fromhex(ref['exact_stored_hex'])
    assert blocks[53][ref['offset']:ref['offset']+len(raw)+1]==raw+b'\0'
    save(out,dict(runtime=runtime,items=items,locations=locations,commodities=commodities,short_Proof_UI_consumers=short,
        full_Proof_term=dict(source='覇者の証',singular='Proof of Conquest',plural='Proofs of Conquest',short='Proof',
            approved_integrated_reference=dict(path=str(prior_path),id=anchor['id'],source_reference=anchor['source_reference'],source_hex=anchor['source_hex'],current_stored_reference=ref,english=anchor['english'],review=anchor['review']),
            exact_current_block53_sha256=sha(blocks[53]),same_ARM9_COMMON_andcomplete_anchor_block=True),
        descriptive_celadon_qualifier_is_source_material_not_new_UI_title=True,unnamed_rewards_not_named_from_unrelated_catalogue_data=True,
        term_reference_only_not_new_font_oractual_gameplay_approval=True,new_credit=0,
        failed_v1_changed_data_addresses_rejected_by_frozen_native_constant_guard=True,no_old_native_guard_removed_orrelaxed=True,
        evidence={str(p):digest(p) for p in [current_path,item_path,prior_path,Path('scripts/bind_maria328_terms_v1.py'),Path('scripts/bind_maria315_terms_v1.py'),Path(__file__)]}))
    print([(r['source']['text'],r['current']['text']) for r in [*items,*locations,*commodities]])

if __name__=='__main__':main()
