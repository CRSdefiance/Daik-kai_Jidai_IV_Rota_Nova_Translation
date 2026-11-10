"""Reconcile public terms and bridge existing decisions to the formatter schema."""
import struct
from copy import deepcopy
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.audit_story_glyph_consistency import load,save
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_hodram_B0_B41_contextual_v1 import ROOT,CURRENT,OUT as PRIOR

TERMS=ROOT/'scoped_terms_v1.json'
PROSE=Path('translations/hodram_B0_B41_contextual_review_v2.json')
CITY=Path('work/analysis/maria_B97_terms_v5006/bound_Maria_Xien_Bandit_Li_Clan_Sao_Jorge_Proof_and_tablet_context.json')
HAVANA=Path('work/analysis/Hodram_B191_B210_clean_20261104/source_current_term_checkpoint_v1.json')


def main():
    assert not TERMS.exists() and not PROSE.exists()
    current,prose,reference=map(load,(CURRENT,PRIOR,CITY));runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=1)
    assert ctx.receipt()==runtime
    image=NdsImage.open(current['current_ROM'])
    assert digest(current['current_ROM'])==current['current_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==ctx.arm and image.read_file('/COMMON/MESFILE.DK4')==ctx.common
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    original=reference['source_current_city_item_and_HELP_versions'][0]['city'];at=original['pointer_field']
    sp,tp=[struct.unpack_from('<I',a,at)[0] for a in (clean,ctx.arm)]
    assert sp==tp==original['pointer'] and reference['approved_city']=='Sao Jorge'
    assert cstring(clean,sp).decode('cp932')==original['text']=='サン＝ジョルジェ'
    assert cstring(ctx.raw,tp)==b'Sao Jorge'
    sao=dict(pointer_field=at,source_pointer=sp,source_hex=cstring(clean,sp).hex(),
        source_Japanese=original['text'],current_pointer=tp,current_hex=cstring(ctx.raw,tp).hex(),current_term='Sao Jorge',
        source_qualified_reference=str(CITY),source_qualified_reference_sha256=digest(CITY),
        separate_legacy_alias_open=reference['separate_untranslated_Sao_Jorge_alias_still_open'])
    aliases=[]
    wanted={'Malacca','Calicut','Hangzhou','Athens','Basra','Stockholm'}
    for entry in WORLD_CITY_ENTRIES:
        if entry.suggested_english not in wanted:continue
        assert clean[entry.offset:entry.offset+entry.source_length]==entry.expected_bytes
        raw=ctx.arm[entry.offset:entry.offset+entry.slot_size];en=entry.suggested_english.encode()
        assert raw==en+bytes(entry.slot_size-len(en))
        aliases.append(dict(profile_ID=entry.row_id,offset=entry.offset,source_Japanese=entry.japanese,
            source_hex=entry.expected_bytes.hex(),current_span_hex=raw.hex(),current_term=entry.suggested_english))
    assert {r['current_term'] for r in aliases}==wanted and len(aliases)==9
    havana=[]
    for alias in next(r for r in load(HAVANA)['cities'] if r['current_term']=='Havana')['source_qualified_typed_aliases']:
        field=alias['pointer_field'];sp,tp=[struct.unpack_from('<I',a,field)[0] for a in (clean,ctx.arm)]
        assert cstring(clean,sp).decode('cp932')=='ハバナ' and cstring(ctx.raw,tp)==b'Havana'
        havana.append(dict(pointer_field=field,source_pointer=sp,source_hex=cstring(clean,sp).hex(),
            current_pointer=tp,current_hex=cstring(ctx.raw,tp).hex(),current_term='Havana'))
    assert havana
    label_path=Path('translations/ship_battery_labels_v1.json');labels=load(label_path)
    from dk4tool.patch.grand_race_menu_release import sha
    assert sha(image.read_file('/_pxl/shipinfo.pxl'))==labels['target_sha256']['/_pxl/shipinfo.pxl']
    names=load(ROOT/'draft_names_andterms_reference_v1.json');items=names['registered_item_names']
    for item in items:
        field=item['pointer_field_offset'];sp,tp=[struct.unpack_from('<I',a,field)[0] for a in (clean,ctx.arm)]
        assert cstring(clean,sp).hex()==item['source']['hex'] and cstring(ctx.raw,tp).hex()==item['current']['hex']
        assert clean[field+4:field+24]==ctx.arm[field+4:field+24]
    revised=deepcopy(prose);changed=[]
    for row in revised['records']:
        if row['id']=='DK4_MES_B20_R0009':
            assert row['editorial_decision']=='revision' and 'San Jorge' in row['english']
            previous=row['english'];row['english']=previous.replace('San Jorge','Sao Jorge')
            row['editorial_finding']+=' Exact public-name reconciliation confirms Sao Jorge.'
            row['localization_note']=row['editorial_finding']
            changed.append(dict(id=row['id'],previous_English=previous,revised_English=row['english'],source_reference=row['source_reference'],current_reference=row['current_reference']))
        row.update(decision=row['editorial_decision'],logical_English=row['english'],exchange_context=row['context'])
    assert len(changed)==1 and revised['counts']==dict(revision=221,retention=173)
    before={r['id']:r for r in prose['records']}
    assert all(all(row[k]==v for k,v in before[row['id']].items()) for row in revised['records'] if row['id']!='DK4_MES_B20_R0009')
    revised.update(remaining_contextual_comparisons=0,previous_contextual_manuscript=str(PRIOR),previous_contextual_manuscript_sha256=digest(PRIOR),
        only_one_English_city_spelling_refined=True,all32_tutorial_editorial_decisions_unchanged=True,
        formatter_metadata_aliases_do_not_change_other_prose_or_gates=True,scoped_terms=str(TERMS))
    save(TERMS,dict(runtime=runtime,inline_city_aliases=aliases,Sao_Jorge=sao,Havana_aliases=havana,registered_item_names=items,
        battle_UI_labels=labels['source_Japanese'],complete_current_shipinfo_matches_qualified_target=True,
        source_geography={'インド':'India','インド洋':'Indian Ocean','地中海':'Mediterranean','南地中海':'southern Mediterranean',
            'カリブ海':'Caribbean','オスマン帝国':'Ottoman Empire','イギリス':'English/Britain by context','アルジェ':'Algiers','明':'Ming'},
        cultural_forms={'大和魂':'spirit of Yamato','南蛮人':'southern barbarians as an in-character cultural epithet','ムスリム':'Muslims'},
        Hanseatic_cog_is_source_design_description_not_new_vessel_name_orcatalogue_claim=True,
        generic_plate_book_andunidentified_item_not_expanded_to_named_items=True,
        symbol_foreign_cries_have_no_invented_lexical_translation=True,
        source_character_claims_not_external_history_law_religion_orbiography=True,
        older_legacy_city_alias_technical_reaudit_preserved=True,pointer_readbacks_not_new_global_ownership_orcity_UI_approval=True,
        prose_reconciliation=changed,new_credit=0,evidence={str(p):digest(p) for p in (CURRENT,PRIOR,CITY,HAVANA,label_path,ROOT/'draft_names_andterms_reference_v1.json',Path(__file__))}))
    revised['scoped_terms_sha256']=digest(TERMS);save(PROSE,revised)
    print('Bound eight spoken ports/two weapons/battle UI. One San-to-Sao spelling corrected; other393 decisions and32 tutorial decisions preserved.')


if __name__=='__main__':main()
