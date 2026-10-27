"""Read/gloss all fourteen B179 wine-fashion speeches before predecessor English."""
from copy import deepcopy
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_clean_context_v4707')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT=(
    'Read all fourteen B179 speeches as a complete boisterous tavern exchange. Selector98 '
    'notices that60 is still drinking that unspecified stuff.60 snaps back,is that a problem. '
    '98 concedes that it is not bad,but insists wine is the thing now,repeating wine for '
    'emphasis.60 asks whether wine tastes good.98 enthusiastically says it is excellent.60 '
    'asks again whether it is really that good.98 says wine makes him feel he needs nothing '
    'else.60 decides to try it too,calls the server マスター,and orders one serving of wine. '
    '5C casually acknowledges the order.60 makes three gulping/drinking sounds.98 asks how '
    'it is.60 exclaims that it tastes wonderful and calls for another serving.98 asks the '
    'server to bring him some too. The impersonal FE notice predicts that wine seems likely '
    'to catch on in サン＝ジョルジェ. Preserve the initial challenge/defensive reply,the shift '
    'to enthusiastic persuasion,repeated curious questions,the personal hyperbole,trial '
    'order,casual service,gulping,pleased verdict and extra orders,then prospective news.\n\n'
    'Native names and voices for98,60,5C remain to bind. Source selectors alone do not license '
    'a named character,friendship,kinship,military rank or formal relationship. The previous '
    'drink is unnamed;do not invent beer,ale,rum,water,a cheap brand or a quality judgment '
    'beyond the speaker\'s rough such-stuff wording.60\'s defensive 悪いか is a retort,not '
    'evidence of a crime or harmful act.98\'s concession and wine-is-currently-the-thing claim '
    'belong to his speech,not a confirmed narrator boom. The questions ask whether wine is '
    'good,not what wine is;do not turn60 into someone who has never heard of it.\n\n'
    'The nothing-else-needed line is98\'s emphatic personal impression. Preserve its comic '
    'hyperbole without inventing a literal diet,addiction,medical advice,abandoned family '
    'or lost job. マスター addresses the person serving at the tavern;bind that native role '
    'before choosing an English address. Do not translate it as a new superior/master '
    'relationship or proper name. One serving is explicit in the first order;another is '
    'explicit in the delighted follow-up. The final98 request means bring him some too; '
    'it does not establish that he already emptied a prior glass. The three ゴキュ sounds '
    'are audible gulping/drinking with the60 selector;preserve that source presentation '
    'without adding a narrator,spilling,choking,a toast,slurred drunkenness or hangover.\n\n'
    'The final しそう remains prospective likelihood,not a confirmed or earned wine boom. '
    'The city is explicit only in the closing FE notice;retain Japanese spelling until '
    'approved current-name binding. Do not assign the preceding exchange a location or '
    'invent continuity with B178. There are thirteen progressive speeches and one impersonal '
    'FE,zero FI/FA/FO substitutions,and16 linear structural commands:opaque A0008 '
    'raw00a0ffff01221da1,fourteen speeches,single four-byte end508,logical512/stored512. '
    'There is no C200,relative site,predicate,2000 pause,resource,presentation word or typed '
    'object. Preserve the complete preambles and exact leaf bytes without inferring packed '
    'effect semantics. Native entry,names,controls,layout,actual coverage and registered '
    'integration remain open. This producer reads no predecessor English and adds no credit.'
)
MEANINGS={
    6:'98 notices or challenges60 for still drinking that unspecified stuff. Preserve the conversational challenge and still;do not invent the beverage,brand,price or a specific relationship.',
    9:'60 gives a sharp defensive retort:what is wrong with that/is that a problem. Preserve the challenge,not a claim of criminal wrongdoing or an invented insult.',
    13:'98 concedes that there is nothing wrong with it,but says wine is the thing now,repeating wine for emphasis. Preserve the concession,current-fashion claim and enthusiasm as his speech;do not assert an impersonal confirmed boom.',
    16:'60 asks,wine,and whether it tastes good. Preserve the brief curious question;he is not asking for a definition or proving he has never heard of wine.',
    20:'98 enthusiastically affirms that it is excellent. Preserve the confident recommendation without adding a vintage,place,price or objective award.',
    24:'60 asks again whether it really tastes that good. Preserve the repeated question as growing curiosity rather than deleting it as redundant or inventing hostility.',
    28:'98 says he feels that with wine he needs nothing else. Preserve the enthusiastic personal hyperbole and impression,not a literal diet,medical claim,addiction or invented backstory.',
    31:'60 decides to try it too,addresses the server as マスター,and requests one serving of that wine. Preserve the decision,address function and single serving;bind the native server role before localizing the address. Do not invent a master/subordinate relationship or completed delivery here.',
    35:'5C casually acknowledges the wine order. Preserve the brisk service reply and exact speaker;no rank,proper name,fee or completed additional act is stated.',
    39:'60 makes three ゴキュ gulping/drinking sounds. Preserve the repeated drinking sound and source selector;do not add a narrator,spilling,choking,toast,empty-glass declaration or slurred drunkenness.',
    43:'98 asks how it is after60 drinks. Preserve the short invitation for a verdict rather than an accusation or a new story fact.',
    47:'60 exclaims emphatically that it tastes wonderful,then calls the server and orders another serving. Preserve the excited stretched praise,address function and explicit another;add no price,larger quantity,drunkenness or future consequence.',
    50:'98 asks the server to bring him some too. Preserve joining the order;do not assume that he already finished a prior glass or change it into an order for both speakers.',
    54:'An impersonal FE notice predicts that wine seems likely to become fashionable in サン＝ジョルジェ. Preserve the explicit city and prospective likelihood;no active/earned boom,completed commercial sale or earlier scene location is asserted.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==179))
    clean=Path('work/clean.nds');im=NdsImage.open(clean);block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[179]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='c430628d8ee957e7b54dee2d7bf7020a7e5d22e7c0a6727c8de24fe51fdf1b3b'
    assert len(block)==8+struct.unpack_from('<H',block,4)[0]==512 and lead['speeches']==len(lead['records'])==14
    assert lead['source_selectors']==[92,96,152,254] and lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert lead['FE_panels']==1 and lead['relative_sites']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==0
    commands=lead['complete_native_commands'];assert len(commands)==16
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']!=0x4000]==[(8,'00a0ffff01221da1'),(508,'00000000')]
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2000,0xC200] or c['word']&0xFF00==0x6300 for c in commands)
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for r in lead['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex'] and raw[1:].decode('cp932')==r['source_Japanese']
        r.update(fresh_source_gloss=MEANINGS[r['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True);transcript=ROOT/'SC2_B179_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for r in lead['records']:lines.extend(['\n'+r['id']+' selector'+format(r['source_selector'],'02X'),r['source_Japanese'],r['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all14_complete_B179_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',source_ROM=str(clean),
        source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(im.read_file('/data/SC2.DK4')),block=lead,total_editorial_objects=14,
        whole_exchange_context=CONTEXT,source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all14_clean_source_read_and_individually_glossed_before_predecessor_English=True,source_progressive_speeches=13,source_FE_speeches=1,
        source_relative_site_count=0,source_predicate_count=0,source_A000_count=1,source_C200_count=0,source_declared_end_offsets=[508],
        source_static_actor_selectors=[92,96,152],source_FE_notice_is_impersonal_prospective_city_commodity_fashion=True,
        previous_drink_unspecified_and_rough_persuasion_three_gulps_single_then_another_serving_preserved=True,
        native_names_voices_server_address_city_wine_and_complete_controls_to_bind=True,no_predecessor_English_exposed=True,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,
        no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=14,progressive=13,FE=1,commands=16,selectors=[92,96,152,254],FI=0,FA=0,FO=0,A000=1,C200=0,
        end=508,current_English_unexposed=True,credit=0))
