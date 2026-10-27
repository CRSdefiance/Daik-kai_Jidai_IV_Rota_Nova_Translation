"""Bind Deck/officer/items/Brunei vocabulary without inventing a degree or UI title."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_terms_v4176')
SOURCE=Path('work/analysis/lil_B168_source_v4168/all54_clean_current_complete_context.json')
CREW=Path('translations/crew_help_manuscript_v1.json')
PAGES=Path('work/analysis/crew_help_v448/page_proposal.json')
SKILL=Path('translations/skill_terms_help_release_v1.json')
ITEM=Path('translations/item_interface_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);clean=NdsImage.open('work/clean.nds')
    arm=image.read_file('/__arm9__.bin');helpraw=image.read_file('/COMMON/HELP.DK4');blocks=IlnkContainer.parse(helpraw).blocks
    skill,crew,pages,item=map(read,[SKILL,CREW,PAGES,ITEM]);assert sha(helpraw)==skill['target_HELP_sha256']
    page=next(p for p in pages['pages'] if p['topic_id']==106);assert blocks[106]==bytes.fromhex(page['encoded_hex'])
    prose=next(r for r in crew['records'] if r['topic_id']==106)
    assert 'officers' in prose['english'] and 'Deck screen' in prose['english'] and all(prose['review'].values())
    assert pages['all35_native_previews_visually_reviewed'] and pages['all34_clean_source_context_and_natural_English_reviews_complete']
    at=0x15C4D0;raw=clean.read_file('/__arm9__.bin')[at:at+12];value=arm[at:at+12]
    assert raw.split(b'\0')[0].decode('cp932')=='ブルネイ' and value.split(b'\0')[0]==b'Brunei'
    primary=Path('dk4tool/script/arm9_profiles.py');assert 'Arm9ProfileEntry("DK4_CITY_BRUNEI", 0x15C4D0, "ブルネイ", "Brunei"' in primary.read_text(encoding='utf-8')
    counter=next(r for r in item['records'] if r['id']=='ITEMS_ACQUIRED');literal=counter['compiled'].encode('ascii')+b'\0';pos=arm.find(literal)
    assert pos>=0 and arm.find(literal,pos+1)==-1 and counter['compiled']=='Items Acquired %3d/%3d' and all(counter['review'].values())
    field=counter['source_fields'][0]['field'];pointer=struct.unpack_from('<I',arm,field)[0]
    assert pointer==0x02000000+pos
    ROOT.mkdir(parents=True)
    save(ROOT/'current_Deck_officers_items_X_Brunei_and_naturalist_wording.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_HELP_sha256=sha(helpraw),Deck_and_officers_bound_to_complete_current_reviewed_topic106=dict(source_manuscript=str(CREW),source_prose=prose,current_topic_sha256=sha(blocks[106]),page_proposal=str(PAGES)),source_B168_historical_scholar_title_localized_as_naturalist_without_PhD_or_rank_invention=True,source_historical_title_is_not_claimed_as_an_existing_UI_job_label=True,source_navigator_category_localized_as_reviewed_ship_officer_category_not_a_specific_Deck_job=True,current_Brunei_city_slot=dict(offset=at,owned_bytes=12,clean_hex=raw.hex(),current_hex=value.hex(),primary_profile='DK4_CITY_BRUNEI'),current_items_counter=dict(offset=pos,pointer_field=field,current_pointer=pointer,whole_cstring_hex=literal.hex(),reviewed_manuscript=str(ITEM)),item_information_is_lowercase_source_description_not_an_invented_formal_menu_title=True,source_X_button_and_only_while_item_information_displayed_condition_preserved=True,source_Mikhail_cannot_Deck_assign_and_detailed_item_information_benefits_not_general_stat_bonuses=True,new_actual_gameplay_or_native_UI_calls=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CREW,PAGES,SKILL,ITEM,primary,Path(__file__)]},source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('B168 terms:current complete Deck/officer Help,Items counter pointer and Brunei slot bound;naturalist preserves source role without invented degree. No credit.')
