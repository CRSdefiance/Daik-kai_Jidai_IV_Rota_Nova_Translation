"""Read/gloss B180's complete fragrance exchange before predecessor English."""
from copy import deepcopy
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B180_clean_context_v4755')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT=(
    'Read all eleven B180 speeches as one polite,animated exchange. A6 draws attention '
    'to あの方 and asks whether A7 agrees that this person wore a very pleasant scent. '
    'A7 confirms that A6 noticed it too. A6 wonders what the fragrance was. A7 does '
    'not know,but confidently predicts that the scent will become fashionable. A6 '
    'reacts with sudden urgency:then they must obtain it before other people. A7 '
    'agrees. A6 proposes that,next time they encounter that person,they take the '
    'initiative or summon the nerve to ask. A7 warmly endorses the idea and agrees '
    'that they should. A6 politely takes leave;A7 returns the farewell. After '
    'conditional native commands,the impersonal FE notice predicts that 香料 seems '
    'likely to become fashionable in リスボン.\n\n'
    'Native role names and voices for A6/A7 remain to bind. The courteous あの方 and '
    'honorific らした identify a respectfully mentioned person,not a lord,lady,royalty, '
    'superior,customer,lover,relative or named character. The source does not specify '
    'that person\'s gender;do not invent a man,woman or gendered pronoun. The two '
    'speakers share an impression of a nice scent and a desire to acquire it. They '
    'are not proven friends,relatives,rivals or business partners. Bind native labels '
    'before choosing role words,without inferring rank from a generic label.\n\n'
    'Preserve both speakers\'s courtesy,the shared observation,curiosity,explicit lack '
    'of identification,the confident fashion prediction,the comic urgency to obtain '
    'it first,the proposal to ask on a future encounter,the warm agreement and the '
    'mutual formal parting. 思い切って conveys taking the initiative/working up the '
    'nerve;do not flatten it into a past inquiry or invent danger,rejection,permission '
    'or an appointment. Asking about the fragrance is implied by the exchange,not '
    'a stated demand for a gift,free sample,secret recipe,brand,price,shop or supplier. '
    'Neither an inquiry nor acquisition has happened yet. まあ、大変 is conversational '
    'urgency,not proof of a disaster. 他の方よりも先に is getting it before others, '
    'not a claim of monopoly,hoarding,scarcity,exclusive sales or completed commerce.\n\n'
    'ごきげんよう is a courteous farewell and its return. Preserve the gracious register '
    'in natural American English without invented aristocratic rank,kinship,archaic '
    'grammar or literal concern about the other person\'s mood. A7\'s prediction is '
    'confident speech;the final しそう notice remains impersonal prospective likelihood. '
    'リスボン appears only in the closing notice;do not assign the preceding conversation '
    'a location or continuity with B179. Keep the city and commodity in clean Japanese '
    'until approved current-term binding.\n\n'
    'There are ten progressive speeches and one impersonal FE,zero FI/FA/FO,28 native '
    'commands,ten relative sites,two original8000 predicate/query500 objects,three '
    'distinct A000 leaves at472/504/516,C200570 and one four-byte end572,logical/stored576. '
    'Speech begins at8;there is no leading A000. Preserve every nested branch,complete '
    'preamble,predicate,A000 packed operand,C200 and end byte. No typed-choice/actor-style '
    'object or2000 pause exists. Do not infer query500 or packed-effect semantics from '
    'numbers or the notice. Native source/current mapping,branches,predicates,effects, '
    'entry,names,voices,terms,layout,representative actual coverage and registered '
    'integration remain open. This producer reads no predecessor English and adds no credit.'
)
MEANINGS={
    5:'A6 politely asks whether A7 agrees that the respectfully mentioned person wore a very pleasant scent. Preserve the initial attention-getter,slight pause,shared-impression question and gracious register. No gender,name,rank,relationship,brand or earlier scene location is stated.',
    9:'A7 responds that A6 noticed/thought so too. Preserve shared recognition and the responsive question,without adding a friendship,rivalry or new factual description of the third person.',
    13:'A6 wonders what the fragrance was. Preserve curiosity about its identity;no particular flower,ingredient,brand,perfume name,price or supplier is identified.',
    17:'A7 says politely that they do not know,but confidently predicts that the fragrance will become fashionable. Preserve the explicit lack of knowledge and the contrast with confident prediction;no confirmed narrator boom or past purchase is asserted.',
    20:'A6 reacts with sudden polite urgency and says they must obtain it before other people do. Preserve the comic first-to-have-it concern and prospective need;do not invent danger,scarcity,monopoly,a quantity,a price,a gift or a completed acquisition.',
    24:'A7 courteously agrees. Preserve the brief assent and exact speaker;no additional plan,purchase or relationship is established.',
    28:'A6 proposes that,next time they encounter the person,they take the initiative or work up the nerve to ask. Preserve the future encounter,deliberate boldness and shared proposal. The surrounding fragrance question supplies the topic;do not invent an appointment,demand for a gift,shop/supplier request or completed inquiry.',
    31:'A7 warmly calls this a good idea and agrees emphatically that they should do so. Preserve both the endorsement and the willing commitment,without inventing that the person has already agreed to reveal anything.',
    34:'A6 politely takes leave,with a then/well transition into the courteous farewell ごきげんよう. Preserve gracious parting,not literal mood/health advice,a new rank or an invented next meeting time.',
    38:'A7 returns the courteous farewell ごきげんよう. Preserve the matching gracious response and source speaker;no new event,time or relationship is stated.',
    73:'An impersonal FE notice predicts that 香料 seems likely to become fashionable in リスボン. Preserve the city,commodity and prospective likelihood. Bind approved terms later;the notice proves neither earlier conversation location nor an active/earned boom or completed commercial sale.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==180))
    clean=Path('work/clean.nds');image=NdsImage.open(clean)
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[180]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='b3fed143e22eb0a7378a64d45cf59f76d749e91ddd11bb18c6589e5d6ed8cf35'
    assert len(block)==8+struct.unpack_from('<H',block,4)[0]==576
    assert lead['speeches']==len(lead['records'])==11 and lead['source_selectors']==[166,167,254]
    assert lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0} and lead['FE_panels']==1
    assert lead['relative_sites']==10 and lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==0
    commands=lead['complete_native_commands'];assert len(commands)==28 and commands[0]['offset']==8 and commands[0]['word']==0x4000
    assert sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands)==10
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']==0x8000]==[(452,'0080fffff4010000'),(484,'0080fffff4010000')]
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']==0xA000]==[
        (472,'00a0ffff013d0ba1'),(504,'00a0ffff013b0ba1'),(516,'00a0ffff013c0ba1')]
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word'] in [0xC200,0]]==[(570,'00c2'),(572,'00000000')]
    assert not any(c['word'] in [0x2000,0x2100,0x4100,0x8100] or c['word']&0xFF00==0x6300 for c in commands)
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for r in lead['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex'] and raw[1:].decode('cp932')==r['source_Japanese']
        r.update(fresh_source_gloss=MEANINGS[r['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    transcript=ROOT/'SC2_B180_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for r in lead['records']:lines.extend(['\n'+r['id']+' selector'+format(r['source_selector'],'02X'),r['source_Japanese'],r['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all11_complete_B180_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead,total_editorial_objects=11,whole_exchange_context=CONTEXT,
        source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all11_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        source_progressive_speeches=10,source_FE_speeches=1,source_relative_site_count=10,source_predicate_count=2,
        source_query_fields=[500,500],source_A000_offsets=[472,504,516],source_C200_offsets=[570],source_declared_end_offsets=[572],
        source_static_actor_selectors=[166,167],source_FE_notice_is_impersonal_prospective_city_commodity_fashion=True,
        respectful_unspecified_person_gender_rank_relationship_and_fragrance_identity_not_invented=True,
        future_inquiry_acquisition_and_courteous_mutual_farewells_preserved=True,
        conditional_source_shape_is_not_the_prior_B179_linear_A000_end_shape=True,
        no_predecessor_English_exposed=True,current_names_voices_terms_branches_predicates_effects_entry_native_layout_actual_and_release_still_pending=True,
        no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=11,progressive=10,FE=1,commands=28,selectors=[166,167,254],relative_sites=10,predicates=2,
        query_fields=[500,500],A000=3,C200=1,end=572,current_English_unexposed=True,credit=0))
