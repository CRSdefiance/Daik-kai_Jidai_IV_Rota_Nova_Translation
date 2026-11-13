"""Source-bound crown/name/UI terminology;not a new editorial or graphics approval."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Recruits_Julian_terms_v3076')
SOURCE=Path('work/analysis/lil_Recruits_Julian_source_v3072/complete199_clean_current_native_context.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
NAMEPROOF=Path('translations/residual_character_names_native_review_v1.json')
ALIAS=Path('translations/lil_deep_route_v20.json')
START=Path('work/analysis/lil_Christina_Mivor_startup_v3069/cold_boot_Lil_startup_town_verification.json')
def walk(value):
    if isinstance(value,dict):
        yield value
        for child in value.values():yield from walk(child)
    elif isinstance(value,list):
        for child in value:yield from walk(child)
if __name__=='__main__':
    assert not ROOT.exists();source,catalog,names,alias,start=map(read,[SOURCE,CATALOG,NAMEPROOF,ALIAS,START])
    item=next(r for r in catalog['records'] if r['id']=='DK4_ITEM_POINTER_137');assert item['english']=='Silla Gold Crown'
    name=next(r for r in walk(names) if r.get('index')==201 and r.get('text')=='Mihwa');versions=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000)
        views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if label=='current':
            assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        def string(pointer):
            hits=[v for v in views if v[0]<=pointer<v[0]+len(v[1])];assert len(hits)==1
            start,data,owner=hits[0];tail=data[pointer-start:];end=tail.index(b'\0');return dict(pointer=pointer,owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=tail[:end].decode('cp932'))
        crown=string(struct.unpack_from('<I',arm,item['offset'])[0]);mihwa=string(name['pointer'])
        assert crown['text']==('新羅の金冠' if label=='clean' else 'Silla Gold Crown')
        assert mihwa['text']==('美華' if label=='clean' else 'Mihwa')
        versions.append(dict(version=label,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),crown_item137=crown,Mihwa_catalog201=mihwa))
    aliasrow=next(r for r in alias['records'] if 'Luo Yuli' in r.get('english',''))
    assert aliasrow['id']=='DK4_MES_B79_R0009' and '羅郁麗' in next(r['source_Japanese'] for r in source['records'] if r['id']==aliasrow['id'])
    assert start['candidate_sha256']==source['current_ROM_sha256'];town=next(r for r in start['runs'] if r['case']=='town')
    capture=next(r for r in town['paired_whole_frames'] if r['frame']==11900);assert sha(Path(capture['capture']).read_bytes())==capture['capture_sha256']
    assert sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'clean_current_crown_Mihwa_alias_and_shipyard_UI_terms.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),versions=versions,
        registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),crown_record_ID=item['id'],crown_pointer_file_offset=item['offset'],approved_item_name='Silla Gold Crown',
        Mihwa_registered_name_proof=str(NAMEPROOF),Mihwa_registered_name_proof_sha256=sha(NAMEPROOF.read_bytes()),Mihwa_original_catalog_index=201,
        Luo_Yuli_existing_name_spelling=dict(source='羅郁麗',English='Luo Yuli',prior_record=aliasrow['id'],prior_file=str(ALIAS),prior_file_sha256=sha(ALIAS.read_bytes()),old_dialogue_not_used_as_translation_source_or_fresh_review_credit=True),
        exact_native_actor_names={k:r['historical_native_catalog_name'] for k,r in source['speaker_catalog'].items()},
        speaker_annotation_reconciliation=dict(actor109_original_catalog='Shipwright',provisional_Townsman_annotation_is_not_unique_name=True,use_editorial_speaker='Shipwright;original actor109',actor41_catalog='Sojin Kurushima',spoken_surname_only='Kurushima',actor158_native_class='Retainer',source_role='Kurushima follower,not a new noble rank'),
        current_shipyard_menu_evidence=dict(startup_proof=str(START),startup_proof_sha256=sha(START.read_bytes()),actual_frame=capture,viewed_sheet=start['review_sheet'],viewed_sheet_sha256=start['review_sheet_sha256'],viewed=True,visible_labels=['Dock','Remodel'],header_Refit_is_distinct_from_menu_Remodel=True,inherited_five_ship_battery_is_unearned=True,no_selected_Janus_scene_or_rename_workflow_claim=True),
        prose_policy='Use Silla Gold Crown andMihwa exactly. Keep Luo Yuli as the source Chinese alias using the existing project spelling;Julian remains Julian Lopes. Preserve Ming birth/upbringing,distinct grandparents/parents andpersonal fate question without adding a historical royal rank. The one FE Janus guide tells the player to take the ship out of the dock andname it using the visible Remodel menu;Refit is a different header. Do not invent a Rename button absent fromthis sentence orclaim current earned ship receipt. No UI/name/graphics oritem-effect change.',
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Clean/current item137 SillaGoldCrown andcatalog201Mihwa match;LuoYuli project spelling andactual Dock/Remodel menu terms bound. Zero credit.')
