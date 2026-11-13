"""Bind the named map, materials, cities and existing Proof terminology without UI overclaims."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.review_hodram_B281_B300_contextual_v1 import ROOT,CURRENT,OUT as PROSE

TERMS=ROOT/'scoped_terms_v1.json'


def main():
    assert not TERMS.exists()
    current,prose=map(load,(CURRENT,PROSE));r=current['runtime']
    ctx=RegisteredRuntime(r['release_proof'],r['startup_proof'],captain=1);assert ctx.receipt()==r
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    goods_asset=Path('translations/commodity_name_manuscript_v343.json')
    items_asset=Path('translations/all_item_names_arm9_v1.json')
    goods=[]
    for index,ja,en in [(93,'ショウ石','Saltpeter'),(94,'イオウ','Sulfur'),(95,'木材','Timber')]:
        approved=next(x for x in load(goods_asset)['records'] if x['index']==index)
        at=approved['pointer_field'];sp,tp=[struct.unpack_from('<I',a,at)[0] for a in (clean,ctx.arm)]
        source=clean[sp-0x02000000:clean.index(0,sp-0x02000000)];target=cstring(ctx.raw,tp)
        assert source.decode('cp932')==ja==approved['Japanese'] and target.decode('ascii')==en==approved['English']
        assert clean[at+4:at+12]==ctx.arm[at+4:at+12]==bytes.fromhex(approved['metadata_hex'])
        goods.append(dict(index=index,pointer_field=at,source_pointer=sp,source_Japanese=ja,source_hex=source.hex(),
            current_pointer=tp,current_hex=target.hex(),current_term=en,all_nonname_metadata_exact=True))
    item=next(x for x in load(items_asset)['records'] if x['id']=='DK4_ITEM_POINTER_172')
    at=item['offset'];sp,tp=[struct.unpack_from('<I',a,at)[0] for a in (clean,ctx.arm)]
    source=clean[sp-0x02000000:clean.index(0,sp-0x02000000)];target=cstring(ctx.raw,tp)
    assert source.decode('cp932')=='古代都市遺跡への地図' and target==b'Ancient City Map'
    assert clean[at+4:at+24]==ctx.arm[at+4:at+24]
    map_term=dict(index=172,pointer_field=at,source_pointer=sp,source_Japanese=source.decode('cp932'),source_hex=source.hex(),
        current_pointer=tp,current_term=target.decode(),current_hex=target.hex(),all_nonname_metadata_exact=True,
        source_record_ID='DK4_MES_B287_R0125')
    aliases=[]
    for entry in WORLD_CITY_ENTRIES:
        if entry.suggested_english not in {'Stockholm','Malacca'}:continue
        assert clean[entry.offset:entry.offset+entry.source_length]==entry.expected_bytes
        span=ctx.arm[entry.offset:entry.offset+entry.slot_size];value=entry.suggested_english.encode()
        assert span==value+bytes(entry.slot_size-len(value))
        aliases.append(dict(profile_ID=entry.row_id,offset=entry.offset,source_Japanese=entry.japanese,source_hex=entry.expected_bytes.hex(),
            current_span_hex=span.hex(),current_term=entry.suggested_english,inline_span_not_new_Cstring_ownership_orUI_proof=True))
    assert len(aliases)==4
    prior=Path('work/analysis/Hodram_B191_B210_clean_20261104/source_current_term_checkpoint_v1.json')
    old=next(x for x in load(prior)['cities'] if x['current_term']=='Havana');havana=[]
    for alias in old['source_qualified_typed_aliases']:
        at=alias['pointer_field'];sp,tp=[struct.unpack_from('<I',a,at)[0] for a in (clean,ctx.arm)]
        value=clean[sp-0x02000000:clean.index(0,sp-0x02000000)];target=cstring(ctx.raw,tp)
        assert value.decode('cp932')=='ハバナ' and target==b'Havana'
        havana.append(dict(pointer_field=at,source_pointer=sp,source_hex=value.hex(),current_pointer=tp,current_hex=target.hex(),current_term='Havana'))
    assert havana
    proof_ref=Path('translations/help_deck30_Coerce33_active_terms_final_review_v1.json')
    proof=next(x for x in load(proof_ref)['records'] if x['id']=='HELP_TOPIC_33')
    assert all(proof['review'].values()) and '[[4|Proof of Conquest]]' in proof['english']
    named_map=next(x for x in prose['records'] if x['id']=='DK4_MES_B287_R0125')
    assert 'Ancient City Map' in named_map['english']
    for row in prose['records']:
        if any(token in row['source_Japanese'] for token in ['硫黄','イオウ','木材','ショウ石']):
            expected=('sulfur' if any(t in row['source_Japanese'] for t in ['硫黄','イオウ']) else 'timber' if '木材' in row['source_Japanese'] else 'saltpeter')
            assert expected in row['english'].lower(),row['id']
    save(TERMS,dict(runtime=r,goods=goods,spoken_item_terms=[map_term],inline_city_aliases=aliases,Havana_aliases=havana,
        generic_Proof_term=dict(source_Japanese='覇者の証',approved_English='Proof of Conquest',plural='Proofs of Conquest',
            reference=str(proof_ref),reference_sha256=digest(proof_ref),record_ID=proof['id'],
            existing_reviewed_nonstory_term_reused_not_new_HELP_UI_approval=True),
        geographic_forms={'インド洋':'Indian Ocean','アラブ':'Arab waters/Arab pirate','地中海':'Mediterranean','新大陸':'New World',
            'メキシコ':'Mexico','イギリス':'England','スウェーデン王国':'Kingdom of Sweden','ビザンツ帝国':'Byzantine Empire'},
        contextual_semantics={'火薬':'gunpowder','木炭':'charcoal','大蛇':'giant snake','沼':'bog/swamp',
            '化け魚':'monster fish','隠れ里':'hidden settlement/village'},
        source_conditions_not_new_quantified_stat_orhistorical_claim=True,
        all_named_purchase_materials_andmap_match_current_labels=True,
        pointer_readbacks_not_new_ownership_termination_orwidget_gameplay_approval=True,
        no_new_full_catalogue_UI_orolder_record_technical_credit=True,no_ROM_orprose_changes=True,new_credit=0,
        evidence={str(p):digest(p) for p in (CURRENT,PROSE,goods_asset,items_asset,prior,proof_ref,Path('dk4tool/script/arm9_profiles.py'),Path(__file__))}))
    print('Bound Ancient City Map, Sulfur/Timber/Saltpeter, scoped city aliases and existing Proof terminology. Prose unchanged.')


if __name__=='__main__':main()
