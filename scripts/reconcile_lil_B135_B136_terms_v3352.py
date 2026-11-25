"""Bind tablet names andthe existing narcotic name to exact source/current bytes."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B135_B136_terms_v3352')
SOURCE=Path('work/analysis/lil_remaining_B135_B140_source_v3345b/next35_B135_B136_clean_current_context.json')
VOICE=Path('work/analysis/lil_B135_B136_voices_v3346b/current_six_static_names_voices_and207_catalog_rebind.json')
CONTEXT=Path('work/analysis/lil_B135_B136_clean_context_v3349/all35_complete_clean_context_and_fresh_glosses.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
ITEMS={176:('謎の石版上部','Upper Stone Tablet'),183:('謎の石版下部','Lower Stone Tablet')}
if __name__=='__main__':
    assert not ROOT.exists();source,voice,context,catalog=map(read,[SOURCE,VOICE,CONTEXT,CATALOG]);assert context['all35_complete_clean_source_objects_read_before_older_English_comparison'];versions=[]
    for version,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000);views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if version=='current':assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        rows=[]
        for ident,(jp,en) in ITEMS.items():
            r=next(r for r in catalog['records'] if r['id']==f'DK4_ITEM_POINTER_{ident:03d}');assert r['english']==en;ptr=struct.unpack_from('<I',arm,r['offset'])[0]
            hits=[v for v in views if v[0]<=ptr<v[0]+len(v[1])];assert len(hits)==1;base,data,owner=hits[0];tail=data[ptr-base:];end=tail.index(b'\0');value=tail[:end].decode('cp932');assert value==(jp if version=='clean' else en)
            rows.append(dict(item_ID=ident,catalog_record_ID=r['id'],pointer_file_offset=r['offset'],pointer=ptr,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=value))
        versions.append(dict(version=version,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),items=rows))
    ledger=read('translations/editorial_review_current_v1.json');drug=[];current=NdsImage.open(source['current_ROM']);blocks=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks
    for family in ledger['completed_editorial_families']:
        for r in family['records']:
            if '女神の誘惑' not in r.get('source_Japanese',''):continue
            ref=r['integrated_reference'];value=bytes.fromhex(r['integrated_hex']);assert blocks[r['block']][ref['offset']:ref['offset']+ref['bytes']]==value and "Goddess' Temptation" in r['english']
            drug.append(dict(family=family['id'],final_review=family['final_review'],final_review_sha256=sha(Path(family['final_review']).read_bytes()),id=r['id'],source_reference=r['source_reference'],source_Japanese=r['source_Japanese'],integrated_reference=ref,integrated_hex=r['integrated_hex'],approved_name="Goddess' Temptation"))
    assert len(drug)==2
    names={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh_six_actor_names']['rows']};assert names[2]=='Lil Argot' and names[9]=='Camille Marinus Overijssel' and set(names)=={2,9,14,36,47,96}
    ROOT.mkdir(parents=True);save(ROOT/'clean_current_tablets_narcotic_names_and_wordplay_reconciliation.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),complete_clean_context=str(CONTEXT),complete_clean_context_sha256=sha(CONTEXT.read_bytes()),voice_proof=str(VOICE),voice_proof_sha256=sha(VOICE.read_bytes()),registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),two_complete_item_pointer_versions=versions,approved_item_names={str(k):v[1] for k,v in ITEMS.items()},exact_completed_narcotic_name_references=drug,narcotic_name="Goddess' Temptation",narcotic_is_explicitly_drug_trade_not_ordinary_medicine=True,exact_current_actor_names=names,approved_dialogue_names=dict(Lil='Lil',Camille='Camille',Emilio='Emilio',Espinosa='Espinosa',Gilberto='Gilberto',customer='Customer;generic unnamed distressed man,not invented kinship orrank'),Proof='Proof of Supremacy;source-short Proof stays Proof where clear',whole_goal_Proof_consistency_reconciliation_remains_open_separate_from_technical_reaudit=True,existing_Proof_terminology_lead=ledger['Proof_terminology_consistency_lead_v3286'],map_cheese_wordplay=dict(source_map='地図,chizu',source_food='チーズ,chiizu,cheese',context='Emilio hears map as cheese;Lil corrects him in the following speech.',localization_requirement='Preserve a natural food-based mishearing andexplicit corrective payoff as one exchange. Keep the clean cheese gloss exact;document any English phonetic adaptation without changing map discovery,items,relationships orplot.'),no_old_completed_record_reopened_recounted_or_silently_renamed=True,no_ROM_registry_or_editorial_credit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    old=Path('scripts/compare_lil_B131_B133_effective_v3314b.py');new=Path('scripts/compare_lil_B135_B136_effective_v3353.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={'lil_B131_B133_comparison_v3314b':'lil_B135_B136_comparison_v3353','work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json':str(SOURCE).replace('\\','/'),'lil_B131_B133_controls_v3308b/all61_source_current_dispatch_selector00_FE_and5_predicates.json':'lil_B135_B136_controls_v3347/all35_source_current_dispatches_and1_predicate.json','lil_B131_B133_clean_context_v3312/all63_complete_clean_context_and_fresh_glosses.json':str(CONTEXT).replace('\\','/'),'lil_B131_B133_terms_v3313/clean_current_items_names_and_share_ratio_reconciliation.json':'lil_B135_B136_terms_v3352/clean_current_tablets_narcotic_names_and_wordplay_reconciliation.json','all63_complete_clean_source_objects_read_before_older_English_comparison':'all35_complete_clean_source_objects_read_before_older_English_comparison','all63_fresh_source_glosses_precede_localized_English':'all35_fresh_source_glosses_precede_localized_English','len(rows)==63':'len(rows)==35','all63_current_effective_comparison_packet':'all35_current_effective_comparison_packet','fresh63_glosses':'fresh35_glosses','all63_current_English':'all35_current_English','source_current_comparisons=63':'source_current_comparisons=35','Current names including static00 Rafael,FE null actor,FI/FO,five predicates,item names andtwo-to-one share terms bound.':'Six static names,FO1,one predicate,tablet item names andthe existing narcotic name bound.'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    save(ROOT/'comparison_tool_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes())))
    print('Upper/LowerStoneTablet176/183 complete pointers andtwo completed Goddess\' Temptation references bound;Proof consistency remains open. CurrentEnglish comparison prepared.')
