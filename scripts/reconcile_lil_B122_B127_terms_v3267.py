"""Bind item/stat/actor terms and preserve exact existing terminology evidence."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B122_B127_terms_v3267')
SOURCE=Path('work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json')
VOICES=Path('work/analysis/lil_B122_B127_voices_v3264/current_eight_static_names_voices_and207_catalog_rebind.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
NATIVE=Path('translations/person_info_arm9_v1.json')
STATS=Path('translations/person_info_graphics_v3.json')
ITEMS={85:('善導のステッキ','Guiding Staff'),144:('細雪のローブ','Snow-Silk Robe')}
if __name__=='__main__':
    assert not ROOT.exists();source,voices,catalog,native,stats=map(read,[SOURCE,VOICES,CATALOG,NATIVE,STATS]);versions=[]
    for version,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000);views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if version=='current':assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        items=[]
        for ident,(jp,en) in ITEMS.items():
            r=next(r for r in catalog['records'] if r['id']==f'DK4_ITEM_POINTER_{ident:03d}');assert r['english']==en
            ptr=struct.unpack_from('<I',arm,r['offset'])[0];hits=[v for v in views if v[0]<=ptr<v[0]+len(v[1])];assert len(hits)==1
            base,data,owner=hits[0];tail=data[ptr-base:];end=tail.index(b'\0');value=tail[:end].decode('cp932');assert value==(jp if version=='clean' else en)
            items.append(dict(item_ID=ident,catalog_record_ID=r['id'],pointer_file_offset=r['offset'],pointer=ptr,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=value))
        spirit=next(r for r in native['records'] if r['id']=='DK4_PERSON_STAT_SPIRIT');assert spirit['english']=='Spirit';at=spirit['offset'];value=arm[at:at+8].split(b'\0')[0].decode('cp932');assert value==('精神' if version=='clean' else 'Spirit')
        versions.append(dict(version=version,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),items=items,Spirit=dict(offset=at,text=value,span_hex=arm[at:at+8].hex())))
    ui_spirit=next(r for r in stats['records'] if r['id']=='DK4_PERSON_STAT_PLAQUE_4_V2');ui_mood=next(r for r in stats['records'] if r['id']=='DK4_PERSON_MOOD_PLAQUE')
    assert (ui_spirit['source_japanese'],ui_spirit['text'])==('精神','Spirit') and (ui_mood['source_japanese'],ui_mood['text'])==('精神','Mood')
    names={r['actor_ID']:r['current_catalog_name'] for r in voices['fresh_eight_actor_names']['rows']};assert names[6]=='Julio Erneco' and names[26]=='Julian Lopes' and names[92]=='Barkeep' and names[95]=='Patron' and names[151]=='Retainer'
    previous=Path('translations/lil_clifford_north_new_world_contextual_final_review_v1.json');prior=read(previous);oldproof=next(r for r in prior['records'] if r['id']=='DK4_MES_B68_R0090');newproof=next(r for r in source['records'] if r['id']=='DK4_MES_B122_R0152')
    assert oldproof['source_hex']==newproof['source_hex'] and oldproof['english']=="{SPEAKER:97}It's the Proof of Supremacy he stole!"
    shrine=Path('translations/lil_B111_B119_contextual_final_review_v1.json');other=read(shrine);conquest=next(r for r in other['records'] if 'Proof of Conquest' in r['english'])
    term_variants=[dict(final_review=str(previous),final_review_sha256=sha(previous.read_bytes()),id=oldproof['id'],block=68,english=oldproof['english'],source_hex=oldproof['source_hex'],integrated_reference=oldproof['integrated_reference']),dict(final_review=str(shrine),final_review_sha256=sha(shrine.read_bytes()),id=conquest['id'],block=conquest['block'],english=conquest['english'],source_hex=conquest['source_hex'],integrated_reference=conquest['integrated_reference'])]
    overlaps=[]
    for r in source['records']:
        if len(bytes.fromhex(r['source_hex']))<13:continue
        hit=[q for q in prior['records'] if q['source_hex']==r['source_hex']]
        for q in hit:overlaps.append(dict(next_id=r['id'],prior_id=q['id'],prior_block=q['block'],identical_source_paragraph=True,distinct_original_source_record_not_duplicate_completion_credit=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'clean_current_items_Spirit_static_actors_and_related_terms.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),voice_proof=str(VOICES),voice_proof_sha256=sha(VOICES.read_bytes()),registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),two_item_pointer_versions=versions,approved_item_names={str(k):v[1] for k,v in ITEMS.items()},native_stat_config=str(NATIVE),native_stat_config_sha256=sha(NATIVE.read_bytes()),stat_UI_config=str(STATS),stat_UI_config_sha256=sha(STATS.read_bytes()),source_plus1_is_Spirit_stat_not_Mood_condition=True,no_stat_gain_or_graphics_completion_claim=True,exact_current_static_catalog_names=names,
        approved_new_context_roles={'6':'Julio Erneco; explicitly Christina\'s grandfather, not Lil kin','26':'Julian Lopes; advice and self-serving flirting joke','92':'Barkeep; source親父 does not establish fatherhood','95':'Patron; no invented personal name','151':'Static Retainer151; not dynamicD0 fallback or a new noble rank'},
        approved_new_context_terms=dict(Snow_Silk_Robe='Snow-Silk Robe',Guiding_Staff='Guiding Staff',Spirit='Spirit',Christina='Christina',Camille='Camille',Fernando='Fernando',ship_Galahad='Galahad;sourceギャラハット/current existing ship wording',city_Bruges='Bruges',city_Osaka='Osaka',sea_North_Sea='North Sea',barmaid_Sakura='Sakura',regional_India='India',English_Crown='English Crown',card_game='Old Maid'),
        Guiding_Staff_moral_guidance_is_legend_and_India_location_is_vague=True,Snow_Silk_Robe_is_optional_Sakura_example_not_a_new_gift_earned=True,
        source_clifford_repeated_paragraphs_in_other_completed_exchange=overlaps,
        B122_related_B68_full_Proof_form='Proof of Supremacy;retain the established related exchange term while preserving source abbreviation Proof where used',
        existing_completed_Proof_terminology_variants=term_variants,
        later_editorial_terminology_reconciliation_still_required_before_whole_goal_completion=True,
        terminology_lead_is_separate_from_deferred_older_record_technical_reaudit=True,
        no_completed_record_reopened_recounted_renamed_or_changed=True,
        no_ROM_registry_or_editorial_credit_change=True,new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Two clean/current item pointers andSpirit stat bound;Julio/Julian/Barkeep/Patron/Retainer identities reconciled. Existing Proof termvariants recorded forlater editorial consistency;no olderrecord edited orrecounted.')
