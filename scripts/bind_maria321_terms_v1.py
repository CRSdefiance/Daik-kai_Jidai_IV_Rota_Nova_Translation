"""Bind exact installed item/stat names without inventing titles for generic clues."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

ROOT=Path('work/Maria_B196_B215_clean_20261110')


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
    items_path=Path('translations/all_item_names_arm9_v1.json')
    registered={r['offset']:r for r in load(items_path)['records'] if 'english' in r}
    items=[]
    for offset,source,english in [
        (1173184,'アルマジロの鉄皮','Armadillo Hide'),(1173232,'不死鳥のバシネット','Phoenix Bascinet'),
        (1173256,'巨大ゾウガメの盾','Giant Tortoise Shield'),(1173304,'刃折りの武道着','Bladebreaker Gi'),
        (1173424,'ティムールの鎖かたびら',"Timur's Chainmail"),(1173664,'メデューサの盾','Medusa Shield'),
        (1173760,'魔法の革手袋','Magic Leather Gloves'),(1174264,'悪魔を貫く矢','Demon-Piercing Arrow'),
        (1174312,'フェイディアスの鑿',"Phidias' Chisel"),(1174360,'ヘロフィロスの医学書',"Herophilus' Medicine"),
        (1174624,'グプタの霊獣','Gupta Spirit Beast'),(1174912,'王者の像','King Figurehead'),
        (1175032,'凍てついたバラ','Frozen Rose')]:
        row=field(offset,source,english);assert registered[offset]['english']==english
        row['registered_record']=registered[offset]['id'];items.append(row)
    spirit=field(0x1483A8,'精神','Spirit')
    save(out,dict(runtime=ctx.receipt(),items=items,UI=[spirit],
        exact_named_body_terms=['Armadillo Hide','Phoenix Bascinet','Giant Tortoise Shield','Medusa Shield','Demon-Piercing Arrow','Frozen Rose'],
        descriptive_sacred_beast_can_use_registered_spirit_beast_noun_without_inventing_formal_title=True,
        unnamed_mail_training_clothes_gloves_chisel_andfigurehead_do_not_authorize_adding_catalogue_titles=True,
        stolen_royal_armor_story_epithet_has_no_exact_matching_registered_name_andremains_descriptive=True,
        governors_office_is_descriptive_authority_reference_not_new_UI_label=True,
        no_ROM_RAM_registry_orfont_changes=True,no_actual_gameplay_ornew_display_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [current_path,items_path,Path(__file__)]}))
    print('Bound13 installed item names andSpirit; generic clues remain unnamed; zero credit.')


if __name__=='__main__':main()
