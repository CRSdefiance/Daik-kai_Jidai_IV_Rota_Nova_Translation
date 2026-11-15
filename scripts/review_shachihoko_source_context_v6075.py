"""Read all four complete source exchanges before any shared-name replacement."""
from pathlib import Path
from scripts.read_lil_B204_clean_context_v6059 import GLOSSES
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/shachihoko_source_context_v6075')
SOURCE=Path('work/analysis/shachihoko_context_inventory_v6074/all_route_clean_term_and_item116_candidates_and_current_pointer_aliases.json')
LIL=Path('work/analysis/lil_B204_clean_context_v6059/all20_clean_castle_figurehead_claim_missing_shachihoko_and_letter_glosses.json')
DISTINCT={
(0,19):('Jam,where have you been? I have been looking for you!','Rafael is upset over the absence and explicitly says he searched. Do not import Lil\'s theft condition or Hodram\'s all-day absence.'),
(0,26):('Wh-what is this? Where did it come from?','Rafael is surprised and asks about the object and its origin. Preserve the stammer without asserting an already established theft.'),
(0,38):('Oh...well,all right. We are leaving,so hurry and get ready.','Rafael accepts and asks for prompt departure preparations. No explicit theft qualification in this variant.'),
(1,19):('Jam,you are late. Where have you been all day?','Hodram is terse and reproachful;all-day absence is explicit here. No invented missed orders or relationship.'),
(1,25):('What is that? Where did you get it?','Two direct questions about the object and its origin. Keep the brisk voice.'),
(1,35):('You,teaching someone...? Well,never mind. We are leaving,so pack your things.','Hodram doubts Jam as a teacher,then gives departure preparations. Preserve the dry skepticism,not Lil\'s suspicion of theft.'),
(3,18):('Jam,where have you been?','Maria asks calmly about the absence. Do not import Rafael\'s search,Lil\'s exasperation or Hodram\'s all-day detail.'),
(3,24):('My...where did you get something like that?','Maria reacts with surprise and asks where it came from;no explicit identity question here.'),
(3,34):('I see. I am glad they understood how to use it properly. Now,it is nearly time for us to leave. Please get ready too.','Maria accepts Jam\'s story and is glad his supposed explanation was understood. Keep her composed,prompting voice and the mistaken acceptance;do not make the theft visible to her.')}
if __name__=='__main__':
    assert not ROOT.exists();inv,lil=map(read,[SOURCE,LIL]);by_text={r['source_Japanese']:(r['fresh_source_gloss'],r['whole_exchange_note'],r['source_record_index']) for r in lil['records']}
    reviewed=[];excluded=[]
    for b in inv['selected_native_blocks']:
        route=int(b['file_path'][8]);block=b['block']
        if (route,block) not in [(0,216),(1,208),(2,204),(3,177)]:
            assert route==3 and block in [28,105] and not b['picture116_commands'] and not b['packed3074_A000_candidates']
            terms=b['direct_cultural_term_records'];assert all('翔緋鯱' in r['Japanese'] for r in terms)
            excluded.append(dict(file_path=b['file_path'],block=block,whole_source_exchange=b['all_speech_records'],literal_hit_records=terms,
                reason='翔緋鯱 is Maria\'s feared sobriquet in an enemy threat and her complete reflection about fighting the wako. These uses of 鯱 do not name item116. Do not globally substitute the item name,alter the epithet,or infer that Maria is being called a roof ornament. Retain the FA/FI controls and conditional alternatives as evidence;no nickname/prose editorial closure here.'))
            continue
        rows=[]
        for r in b['all_speech_records']:
            if r['Japanese'] in by_text:g,n,i=by_text[r['Japanese']];reused=i
            else:g,n=DISTINCT[(route,r['source_record_index'])];reused=None
            rows.append(dict(**r,fresh_source_gloss=g,whole_exchange_note=n,identical_clean_Japanese_gloss_reused_from_Lil_index=reused))
        assert len(rows)==20
        reviewed.append(dict(file_path=b['file_path'],block=block,source_block_sha256=b['source_block_sha256'],records=rows,
            contextual_progression='Restless Jam asks the innkeeper for somewhere to walk and goes toward a castle to the east. The protagonist later questions his absence and heavy ornament. He calls it a genuine Japanese figurehead and claims a gift for teaching locals its use. The protagonist responds in their own distinct voice. A guard reports a missing shachihoko and foreign-script letter;the daimyo explicitly orders the thief found. The four-part letter presumptuously corrects castle use to ship use,says one spare is being taken instead of thanks,asserts one per ship,and signs Jam\'s full name.',
            source_speech_and_literal_item_name_are_distinct_consumers=True))
    assert len(reviewed)==4 and sum(len(x['records']) for x in reviewed)==80 and len(excluded)==2
    assert sum(r['identical_clean_Japanese_gloss_reused_from_Lil_index'] is None for x in reviewed for r in x['records'])==9
    ROOT.mkdir(parents=True)
    save(ROOT/'four_complete_clean_exchanges_and_two_nonitem_sobriquet_contexts.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),complete_four_source_exchanges=reviewed,excluded_nonitem_sobriquet_contexts=excluded,
        source_item_name='鯱の像',spoken_cultural_term='シャチホコ',current_shared_item_name='Orca Figurehead',
        proposed_shared_item_name='Shachihoko',provisional_localization_reason='The complete castle exchanges and actual upturned ornament image identify a shachihoko. Orca suggests a real killer whale and loses the architectural joke. Retain the Japanese cultural term as the item title;the existing Figurehead category and Jam\'s intentionally mistaken explanation remain distinct. The short noun fits the original owned English slot without shortening for display. Complete native consumers,glyphs,representative gameplay and registered release remain required.',
        external_primary_context=dict(url='https://www.nagoyajo.city.nagoya.jp/en/nagoyajo/',source_title='Nagoya Castle official English overview',
            narrow_support='The official description identifies shachihoko as tiger-fish architectural ornaments. Used only to verify the cultural referent.',
            does_not_identify_the_game_castle_ruler_location_date_material_or_statue_count=True),
        preserved_facts_and_limits=['East direction','Morning complaint','Gift remains Jam\'s claim','Thief accusation explicit','Foreign writing without exact language','Full Jam Jack Ludwyan signature','No aunt,king,emperor,named castle,new rank or proven legitimate gift','No invented explanation of the roof ornament in Jam\'s letter'],
        no_older_English_story_comparison_or_ROM_mutation=True,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,LIL,Path(__file__)]}))
    print('80 clean-source speeches contextualized across four variants;two whole nonitem sobriquet contexts distinguished. Shared title proposed,not approved/integrated;zero credit.')
