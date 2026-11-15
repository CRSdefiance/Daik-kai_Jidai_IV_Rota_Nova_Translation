"""Bind source/current item terms and distinguish spoken proper names from catalogue titles."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.review_hodram_B301_B310_contextual_v1 import ROOT,CURRENT,OUT as PROSE

TERMS=ROOT/'scoped_terms_v1.json'

def main():
    assert not TERMS.exists();current,prose=map(load,(CURRENT,PROSE));runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=1);assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    asset=Path('translations/all_item_names_arm9_v1.json');items=[]
    for index,expected in [(45,"Kublai's Greatsword"),(171,'Golden Temple Map')]:
        approved=next(r for r in load(asset)['records'] if r['id']==f'DK4_ITEM_POINTER_{index:03d}')
        at=approved['offset'];sp,tp=[struct.unpack_from('<I',a,at)[0] for a in [clean,ctx.arm]]
        source=clean[sp-0x02000000:clean.index(0,sp-0x02000000)];target=cstring(ctx.raw,tp)
        assert target.decode('ascii')==expected==approved['english']
        assert clean[at+4:at+24]==ctx.arm[at+4:at+24]
        items.append(dict(index=index,pointer_field=at,source_pointer=sp,source_Japanese=source.decode('cp932'),source_hex=source.hex(),
            current_pointer=tp,current_term=target.decode(),current_hex=target.hex(),all_nonname_item_metadata_exact=True,
            label_reference_not_new_item_ownership_orcatalogue_UI_approval=True))
    assert items[0]['source_Japanese']=='フビライの大剣'
    assert '金閣寺' in items[1]['source_Japanese']
    byid={r['id']:r for r in prose['records']}
    assert "Kublai's Greatsword" in byid['DK4_MES_B306_R0019']['english']
    kinkaku=[r for r in prose['records'] if '金閣寺' in r['source_Japanese']]
    assert len(kinkaku)==3 and all('Kinkaku-ji' in r['english'] for r in kinkaku)
    proofref=Path('translations/help_deck30_Coerce33_active_terms_final_review_v1.json')
    proof=next(r for r in load(proofref)['records'] if r['id']=='HELP_TOPIC_33')
    assert all(proof['review'].values()) and '[[4|Proof of Conquest]]' in proof['english']
    save(TERMS,dict(runtime=runtime,equipment_andmap_terms=items,
        spoken_place_alias=dict(source_Japanese='金閣寺',spoken_English='Kinkaku-ji',
            descriptive_source='黄金の寺',descriptive_English='golden temple',existing_map_title='Golden Temple Map',
            context_record_IDs=[r['id'] for r in kinkaku],
            reason='The source uses the descriptive golden-temple phrase during Sakura’s invitation and the proper temple name in the monk reminders. Keep that distinction; do not add the catalogue map title where no item title is spoken.',
            no_new_map_purchase_location_ororiginal_event_trigger_claim=True),
        generic_Proof_term=dict(source_Japanese='覇者の証',approved_English='Proof of Conquest',plural='Proofs of Conquest',
            reference=str(proofref),reference_sha256=digest(proofref),record_ID=proof['id'],
            existing_reviewed_nonstory_term_reused_not_new_HELP_UI_approval=True),
        geographic_andcultural_forms={'コロッセウム':'Colosseum','ローマ時代':'Roman times','元帝':'Yuan emperor',
            '中華/中国':'China','仏教徒':'Buddhist','モスク':'mosque','鎖国':'isolation/closed-door policy'},
        source_qualified_semantics={'中国のずっと北東':'far northeast of China, not northeastern China',
            '巨大な半島の付け根':'base of a vast peninsula','装備からもはずす':'unequip as well',
            '離脱したようです':'apparent departures, not confirmed deaths',
            '祭った昔の王様':'king from long ago to whom the mosque is dedicated, not its stated builder'},
        source_cultural_andgeographic_statements_not_external_historical_verification=True,
        guide_mixed_version_purchase_destination_reports_not_used_as_DS_activation_proof=True,
        no_new_full_catalogue_UI_orolder_record_technical_credit=True,no_ROM_orprose_changes=True,new_credit=0,
        evidence={str(p):digest(p) for p in [CURRENT,PROSE,asset,proofref,Path(__file__)]}))
    print('Bound Kublai’s Greatsword, Golden Temple Map/Kinkaku-ji and existing Proof terminology. Prose unchanged.')

if __name__=='__main__':main()
