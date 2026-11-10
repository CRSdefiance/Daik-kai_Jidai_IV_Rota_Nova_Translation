"""Bind B97's current names,faction,town,Proof title and tentative tablet presentation."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_terms_v5006')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
NAMES=Path('work/analysis/maria_B97_names_v5003/six_original_progressive_and_catalogue_name_consumers.json')
MACROS=Path('work/analysis/maria_B97_macros_v5004/three_actors_default_and_real_FO20_alignment_cases.json')
CONTROLS=Path('work/analysis/maria_B97_controls_v5005/eight_source_leaves_resource633E_item4820_hide_and_two_effects.json')
CITY=Path('translations/route_forces_arm9_v1.json')
ITEMS=Path('translations/all_item_names_arm9_v1.json')
FACTION=Path('translations/faction_help_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();source,names,macros,controls=map(read,[SOURCE,NAMES,MACROS,CONTROLS])
    assert all(d['source_context_sha256']==sha(SOURCE.read_bytes()) for d in [names,macros,controls])
    assert names['progressive_nameplate_values']=={'3':'Maria Li','10':'Xien Yan','180':'Bandit'}
    assert names['full_catalogue_values']=={'3':'Maria Huamei Li','10':'Xien Yan','180':'Bandit'}
    assert macros['macro_ascii_lengths']==dict(FI=5,FA=2,FO=7)
    assert controls['source_item_descriptor']==[0,176,1,5] and controls['source_item_layout']==[2,0,0]
    city=next(r for r in read(CITY)['records'] if r['id']=='DK4_ROUTE_CITY_SAO_JORGE_POOL')
    item=next(r for r in read(ITEMS)['records'] if r['id']=='DK4_ITEM_POINTER_176')
    assert city['offset']==0x15E64C and item['english']=='Upper Stone Tablet'
    help189=next(r for r in read(FACTION)['records'] if r['id']=='HELP_TOPIC_189')
    assert all(help189['review'].values()) and 'established Proof of Conquest term' in help189['localization_note']
    versions=[];images=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        image=NdsImage.open(path);images.append(image);arm=image.read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000)
        views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if label=='current':assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        field=item['offset'];ptr=struct.unpack_from('<I',arm,field)[0];hits=[v for v in views if v[0]<=ptr<v[0]+len(v[1])];assert len(hits)==1
        base,data,owner=hits[0];tail=data[ptr-base:];end=tail.index(0);text=tail[:end].decode('cp932')
        if label=='current':assert text=='Upper Stone Tablet'
        else:assert text=='謎の石版上部'
        cptr=struct.unpack_from('<I',arm,0x123284)[0];assert cptr==0x0215E64C
        craw=arm[city['offset']:city['offset']+20];assert craw==bytes.fromhex(city['source_hex' if label=='clean' else 'replacement_hex'])
        aliasptr=struct.unpack_from('<I',arm,0x122504)[0];assert aliasptr==0x0215E5D4
        alias=arm[0x15E5D4:];alias=alias[:alias.index(0)+1];assert alias=='サン＝ジョルジェ'.encode('cp932')+b'\0'
        helpblocks=IlnkContainer.parse(image.read_file('/COMMON/HELP.DK4')).blocks;topic=helpblocks[4];title=topic.split(b'\n',1)[0].decode('cp932').rstrip(' ')
        assert title==('覇者の証（ゲームの目的）' if label=='clean' else 'Proof of Conquest')
        if label=='current':assert b'Proof of Conquest' in helpblocks[189] and b"treasure proving its owner's supremacy" in topic
        versions.append(dict(version=label,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),city=dict(pointer_field=0x123284,pointer=cptr,owned_span_hex=craw.hex(),text=craw.split(b'\0')[0].decode('cp932')),separate_untranslated_city_alias=dict(pointer_field=0x122504,pointer=aliasptr,complete_hex=alias.hex(),consumer_status_unresolved=True),tablet=dict(item_ID=176,pointer_field=field,pointer=ptr,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=text),HELP4=dict(title=title,complete_topic_sha256=sha(topic)),HELP189=dict(complete_topic_sha256=sha(helpblocks[189]))))
    ledger=read('translations/editorial_review_current_v1.json');lead=ledger['Proof_terminology_consistency_lead_v3286'];variants=[]
    currentblocks=IlnkContainer.parse(images[1].read_file('/data/SC2.DK4')).blocks
    cleanblocks=IlnkContainer.parse(images[0].read_file('/data/SC2.DK4')).blocks
    for v in lead['variants']:
        finalpath=Path(v['final_review']);assert sha(finalpath.read_bytes())==v['final_review_sha256'];r=next(r for r in read(finalpath)['records'] if r['id']==v['id'])
        raw=bytes.fromhex(r['integrated_hex']);ref=r['integrated_reference'];assert currentblocks[r['block']][ref['offset']:ref['offset']+len(raw)+1]==raw+b'\0'
        jp=bytes.fromhex(r['source_hex']);sref=r['source_reference'];assert cleanblocks[r['block']][sref['offset']:sref['offset']+len(jp)]==jp
        variants.append(dict(v,current_hex=raw.hex(),current_reference=ref,source_reference=sref,no_completed_record_reopened_or_recounted=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'bound_Maria_Xien_Bandit_Li_Clan_Sao_Jorge_Proof_and_tablet_context.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],source_FO_measured_default='Li Clan',source_FO_preserved_as_runtime_macro=True,source_current_city_item_and_HELP_versions=versions,approved_city='Sao Jorge',chosen_full_Proof_term='Proof of Conquest',chosen_short_Proof_term='Proof',Proof_decision_reason='Use current Help4 heading and explicitly reviewed Help189 established term. The earlier exact Supremacy/Conquest consistency lead remains open for separate contextual correction;no silent older rename.',older_exact_Proof_variant_references=variants,whole_goal_Proof_consistency_lead_preserved=lead,source_tablet_generic_question_not_expanded_to_catalogue_title=True,source_tablet_hidden_in_unspecified_ruins_connection_to_Proof_explicitly_uncertain=True,source_item176_catalogue_not_completed_Proof_or_earned_inventory_proof=True,slave_trading_and_military_plunder_remain_character_explicit_and_no_historical_absolution_invented=True,European_power_partition_and_influence_claims_remain_character_statements=True,source_revenge_entrusting_invitation_preserves_voluntary_agency_no_specific_retaliatory_act_promised=True,separate_untranslated_Sao_Jorge_alias_still_open=True,no_predecessor_B97_English_compared_by_this_binding=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,MACROS,CONTROLS,CITY,ITEMS,FACTION,Path(__file__)]},new_emulator_runs=0,new_review_credit=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound Maria/Xien/Bandit,default Li Clan,Sao Jorge,Help Proof of Conquest and tablet176. Older Proof consistency and city alias stay open;zero credit.')
