"""Read/gloss all33 clean B174 speeches,including the conditional food aside."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_clean_context_v4451')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT='''Read B174 as one complete33-speech exchange,including source0E's conditional food remark. The source-named ユリアン recognizes Lil and thanks her for the earlier crown transfer;he explicitly says she found 新羅の金冠 first and let him have it. These newly supplied facts belong here;do not retroactively insert them into B172/B173. 美華 admires the crown's imposing/refined appearance andaccepts it as a promised gift,not a newly promised date. ユリアン thanks Lil and asks how she reached 武寧王陵 so quickly;Lil boasts about adventure experience,then clears her throat andcorrects his assumption:her occupation is sailing around the world to trade. He realizes her party used a ship,contrasts his own desperate run to 京城,andexplains that he collapsed after asking at the tavern andlost the lead while resting. Keep the extraordinary running claim andLil's disbelief;do not replace running with ordinary sailing to repair the joke's physical premise. Source0E's optional aside focuses on getting hungry from so much running;bind that actor's actual approved name andvoice later,without inventing eating or membership.

The man's extravagant fate-and-wonderful-woman flattery now targets Lil. Her puzzled private again-comment is explicitly licensed by また;it is not a new arrival. He asks to accompany her andsee the world. When she questions his purpose,he explains his childhood admiration for his actual grandfather's world voyages andwish to become an adventurer like him. 祖父 establishes genuine grandfather kinship here;do not apply an unrelated ban on literal kinship terms. Lil's seafarer/navigation-knowledge question tests his competence,his assurance promises not to be a burden,andshe agrees to take him along. Preserve his renewed cute-girl flattery andher conditional overboard threat as a comic retort,not an actual assault or a fabricated immediate punishment.

美華 challenges him about herself,then scolds him for openly courting another woman in front of her anddismissively tells him to go anywhere in the world. This jealousy andfamiliar courting do not establish marriage,an official romantic partnership or a prior unconditional date agreement. He calls Lil his new employer andtries to placate 美華. He proposes a new conditional plan:if he finds something even more wonderful than the crown,he will return promptly andthey should go on a date. 美華 asks whether he means it andsays she will wait expectantly. Preserve her softened reception andexpectation without erasing the condition or asserting completed travel,a new gift or present ownership. Lil's final private 大物かも reaction conveys bemused recognition of his exceptional boldness/caliber,not a literal physical size,official rank or newly verified reputation. Review the emotional progression from gratitude/gift,through competence banter andearnest aspiration,to flattery/jealousy/placation andLil's closing aside. Add no price,transfer bargain,grandfather name/rank,crew certification,numeric navigation skill,romance status or further item identity. Current approved names,titles,city/native voices,branch consumers andeffect semantics are to be bound separately. No predecessor English is read by this producer.'''
MEANINGS={
    6:'The man recognizes Lil andthanks her for what happened earlier. Preserve recognition andgratitude without supplying a name,rank,fee or earlier action beyond what the following speeches explain.',
    10:'美華 asks whether the two know each other. Preserve the question;do not invent friendship,family or an established professional relationship yet.',
    14:'He explains that he met Lil when she let him have this 新羅の金冠,andadmits that she actually found it first. Preserve the transfer andher earlier discovery without adding a sale,price,loan or promise not stated here.',
    18:'美華 marvels that this is the crown,andadmires its substantial/stately presence andrefinement. Preserve her aesthetic reaction without inventing an actual measured weight,material assay or magical property.',
    22:'He says he is giving it to 美華 as promised. Keep the promised crown gift distinct from a promised date or a new acquisition happening offscreen.',
    26:'She calls it wonderful andsays she will treasure it all her life. Preserve her pleased acceptance andfuture care without a marriage or permanent relationship claim.',
    30:'Lil comments,with a trailing dry tone,that it worked out well for him. Preserve her understated reaction to his successful gift rather than inserting a fee,resentment or her own romantic interest.',
    34:'He credits Lil andasks her to tell him how she reached 武寧王陵 so quickly. Preserve gratitude andthe genuine question about her speed,without answering it before the following exchange.',
    38:'Lil teasingly says there is a difference in their adventure experience. Preserve her confident boast without inventing a professional adventurer rank,years of service or a formal credential.',
    42:'He asks whether she is an adventurer,then flatters her as charming andapparently dependable as well. Preserve his question andpersonal compliment,not a confirmed occupation or numerical skill assessment.',
    46:'Lil clears her throat andhesitates,then clarifies she is not an adventurer:she sails around the world doing business. Preserve the flustered correction andactual trading activity without adding a rank or a new company name.',
    50:'He is impressed andrealizes that Lil andher companions used a ship to reach 京城. Preserve his realization andthe source plural without naming unmentioned companions or a whole fleet.',
    54:'He contrasts that with his own desperate run to 京城. After hearing information at its tavern,he collapsed;while he was resting,Lil got ahead of him. Preserve running,the order of tavern inquiry/collapse/rest,andthe lost lead without relocating the collapse or inventing a journey by ship.',
    57:'Lil repeats the claim of running to 京城 in disbelief andasks whether he is kidding. Preserve the incredulous reaction,not an accusation whose falsity is confirmed by narration.',
    69:'The conditionally present source0E speaker remarks that running the whole time would make one hungry. Preserve the food-focused aside without claiming the speaker actually ran,ate or supplied provisions;bind the actor identity later.',
    75:'The man declares that going to 京城 must have been destiny because he met a wonderful woman like Lil. Preserve his extravagant flattery toward Lil andhis own fate interpretation,not an objective supernatural event or an established romance.',
    78:'Lil reacts with a puzzled short question andprivately thinks he has started saying strange things again. Preserve the aside andthe explicitly sourced again;do not invent a new arrival or a public accusation.',
    81:'He asks Lil to take him along andlet him see the world with her. Preserve his eager request to accompany her,not a command or an already completed recruitment.',
    84:'Lil asks whether he is serious andwhat he wants to do out in the world. Preserve skepticism andthe question about purpose rather than a refusal or a demand for payment.',
    87:'He wants to travel around the world. His actual grandfather sailed all over the world,andhe has admired him since childhood. Preserve the explicit family relationship andlongstanding aspiration without naming the grandfather,his employer or a rank.',
    91:'He explicitly wants to become an adventurer like his grandfather. Keep that earnest aspiration distinct from being already qualified or inheriting a formal position.',
    94:'Lil reflects that his grandfather was a seafarer/navigator andasks whether he therefore knows about navigation. Preserve the inference andcompetence question,without adding a certification,test result or numerical threshold.',
    98:'He assures her that he does have the knowledge andwill not be a burden. Preserve confidence andthe promise,not a verified skill statistic or a guarantee that no future problem can occur.',
    102:'Lil agrees andinvites him to go with her. Preserve the acceptance andfuture joint departure without inventing salary,a contract document or an additional condition.',
    106:'He says simply going to sea with a cute girl like Lil makes him happy. Preserve his renewed flirtation andexuberance,not an established relationship or an explicit sexual proposition.',
    110:'Lil warns that if he keeps saying things like that,she will throw him into the sea. Preserve the conditional comic threat as a retort to his flattery;do not turn it into an actual assault or an immediate punishment.',
    113:'美華 addresses ユリアン andasks what he intends to do about her. Preserve her pointed challenge andthe shift of attention back to her,without inventing an official relationship status.',
    116:'He falters andaddresses 美華. Preserve his caught-off-guard hesitation rather than adding an excuse or apology before the source supplies it.',
    120:'美華 scolds him for openly courting another woman in front of her,anddismissively tells him to go out into the world or wherever he likes. Preserve her jealousy/anger andsarcasm without adding a breakup,marriage or a literal travel assignment.',
    124:'He tells 美華 there is no need to be jealous because Lil is his new employer,andasks her to cheer up/stop being upset. Preserve his placating explanation andnew employment relationship without inventing a salary,rank or an admission that he did not flirt.',
    128:'He proposes that if he obtains something even more wonderful than 新羅の金冠,he will come right back andthey should go on a date. Preserve the condition,comparison,prompt future return anddate proposal;do not name a new treasure or turn wonderful into a fixed monetary value.',
    132:'美華 asks whether he really means it andsays she will wait with anticipation. Preserve her softened,expectant response within his conditional plan,not a present date or an unconditional promise stripped of its preceding condition.',
    135:'Lil privately thinks he might be something remarkable/a person of exceptional boldness. Preserve her bemused closing assessment anduncertainty,not a literal size,official big-shot rank or a new reputation as established fact.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==174))
    clean=Path('work/clean.nds');image=NdsImage.open(clean);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[174]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='2cda89471cb7609824efb1b98e87b94bedfdc435bb0b1dfab60dfb196c5edf7c'
    assert len(block)==2092 and lead['speeches']==len(lead['records'])==33
    assert lead['source_selectors']==[2,14,26,201] and lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert lead['FE_panels']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==0 and lead['relative_sites']==4
    commands=lead['complete_native_commands']
    assert len(commands)==45 and [c['offset'] for c in commands if c['word']==0]==[2086]
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word'] in [0xA000,0x8000]]==[
        (874,'0080ffff0efe0030'),(2068,'00a0ffff020cc960'),(2076,'00a0ffff1a100120')]
    assert [(c['offset'],c['word']) for c in commands if c['word'] in [0x100,0x200,0x300,0x400]]==[(882,0x200),(886,0x300),(890,0x100),(938,0x100)]
    assert [c['word'] for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]==[0x6000,0x6340,0x8000,0x6240,0xA000,0xA000,0xC200,0]
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for row in lead['records']:
        at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and raw[1:].decode('cp932')==row['source_Japanese']
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    optional=next(r for r in lead['records'] if r['source_record_index']==69)
    assert optional['source_selector']==14 and optional['ancestor_0100_offsets']==[890]
    ROOT.mkdir(parents=True);transcript=ROOT/'SC2_B174_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for row in lead['records']:lines.extend(['\n'+row['id']+' selector'+format(row['source_selector'],'02X'),row['source_Japanese'],row['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all33_complete_B174_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead,total_editorial_objects=33,whole_exchange_context=CONTEXT,source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all33_clean_source_read_and_individually_glossed_before_predecessor_English=True,source_relative_site_count=4,
        source_predicate_count=1,source_A000_count=2,source_C200_count=1,single_source_end_offset=2086,
        conditional_food_aside_source_ID=optional['id'],source0E_identity_still_to_bind=True,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True,no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,
        new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=33,structural_commands=45,selectors=[2,14,26,201],FI=0,FE=0,relative_sites=4,predicates=1,A000=2,C200=1,
        conditional_food_aside=optional['id'],current_English_unexposed=True,ledger_credit=0,full_goal_active=True))
