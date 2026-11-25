"""Preserve all clean letter/voice meanings and source name fields before older English."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B209_complete_clean_v6447b/all20_clean_objects_five_speeches15_stored_alternatives16_slots.json')
ROOT=Path('work/analysis/lil_B209_clean_context_v6448')
INTRO={
20:('Admiral,a letter from Yukihisa has arrived.','Friendly polite notice endingよ. Address提督 is explicit;bind the established English captain/admiral terminology rather than inventing a different military rank. No relationship or delivery destination is stated.'),
62:('Admiral,a missive from Yukihisa has arrived.','The written/formal書簡 and届いております distinguish a more formal voice. Preserve the fact and measured formality without copying Japanese syntax.'),
104:('Admiral,a letter has arrived from Yukihisa.','Casual polite届いてますよ. Original styles2/7 share this one stored body;retain the alias and give no duplicate object credit.'),
142:('Admiral,a letter from Yukihisa has arrived.','Politeさん/お手紙 adds courtesy,not kinship,rank or a new title. Localize social tone naturally instead of literal honorifics.'),
188:('Admiral,a letter from Yukihisa has arrived.','Rough/confidentますぜ ending;keep a conversational crew voice without invented piracy,nationality or comic dialect.'),
226:('Admiral,a letter from Yukihisa has arrived.','Older or emphaticおるぞ voice,not proof of the currently resolved speaker\'s age or biography. Dynamic D0 role and style must be mapped before assigning a final voice.'),
264:('Admiral! A letter from Yukihisa has arrived.','Drawn-out phoneticていとくー and accessible hiragana give an excited/simple voice. Do not invent a child relationship or misspell names;preserve the enthusiasm naturally.')}
REACTION={
20:('That is difficult writing. Just like Yukihisa.','Friendly polite observation;らしい is recognition of characteristic behavior. The reaction specifically follows the formal letter,not a claim that Yukihisa personally cannot write well.'),
58:('Difficult prose,indeed. Typical of Yukihisa.','Measuredますな voice. Preserve amused recognition;do not make the sword clue itself incomprehensible or add an insult.'),
90:('It is difficult writing,isn\'t it? Just like Yukihisa.','Conversationalだね/らしいよ and politeさん. A light observation about dense phrasing,not a factual dismissal of the rumor.'),
126:('This is difficult prose. Just like Yukihisa.','Politeですね withわ softening. Preserve voice by natural cadence,not a newly invented gender label or relationship.'),
164:('That is some rather convoluted writing. Typical of Yukihisa.','Roughだな/ぜ and小難しい connote needlessly difficult or fussy writing. A lightly teasing line should set up Lil\'s curiosity rather than hostility.'),
208:('Difficult prose,eh? Just like Yukihisa.','Olderじゃのう/わい manner. Preserve distinct voice without Shakespearean syntax or unsupported family address.'),
246:('It is so difficult that I cannot tell what it says.','This style uniquely says the speaker cannot understand the writing. It omits the usual typical-of-Yukihisa remark;do not homogenize that difference or turn it into general illiteracy.'),
290:('Difficult prose,indeed. Truly characteristic of Yukihisa.','Distinct style7 reaction emphasizesいや、実に. Unlike its aliased introduction,this stored body is unique;preserve its separate source reference and thoughtful formality.')}
SPEECH={
27:('I have heard rumors of the legendary妖刀 Muramasa. It is a renowned,finely made blade said to be the bane of Tokugawa,the leader of Japan,and attempts are being made to eradicate it from the world.','Yukihisa\'s written候 constructions are conspicuously formal/old fashioned. 妖刀 supplies a sinister or cursed-blade reputation;鬼門 is figurative bane/source of misfortune here,not a literal northeast gate. Preserve hearsay,craftsmanship,reputation and threatened eradication. The source does not prove real magic or name an issuer of an extermination order. 頭領 supports leader/ruler;do not silently add shogun,emperor,dates,actual history,smith biography or an invented clan relationship. The next paragraph\'s one of them supports a class of Muramasa blades;final English must keep that link clear.'),
30:('It appears that a family/clan bearing a grudge against Tokugawa has concealed one of these somewhere in East Asia. I am writing to inform you of this for the time being.','Retain appearance/reporting uncertainty and one blade among the class,an unspecified grudge-bearing family/clan,and only East Asia as location. No named clan,revenge mission,buried site,town,island,shrine or guaranteed possession is supplied. 取りあえず is a provisional passing-on of news,not a request for an immediate voyage or completed quest.'),
33:('There can be no doubt that this is the object I have sought for many years. Signed:白樹玄丞行尚 (Yukihisa).','拙者 and相違御座らぬ reinforce Yukihisa\'s distinctive formal self-reference and certainty about his own long-sought object. This is not proof he found or acquired the sword. Preserve the full signature identity and its explicit readingユキヒサ;bind all three clean name-table fields before deciding a natural Romanized signature order. Source blank line/indentation is letter staging to review under its actual consumer,not a reason to copy leading blanks or authored spaces.'),
65:('That is some rather convoluted writing. Just like Yukihisa.','The separate explicit actor11 line also teases Yukihisa\'s dense prose. Do not assume it runs immediately after all eight dynamic alternatives;the original8000/0200/0300/0100 control paths require native proof. Preserve actor11\'s identity and conversational tone.'),
71:('...Hmm,that sounds interesting. Maybe I will try looking for it.','Lil is intrigued and considers a search;かな is tentative. Do not turn this into a firm promise,an already-found blade,a gift or an effect. The amused reaction to formal writing develops into curiosity about the underlying clue.')}
CONTEXT='''Two original4100 actor-style objects provide a crew notice that Yukihisa has sent a letter and an amused reaction to its difficult prose. They are automatic voice variants,not player choices. The first has8slots/7stored bodies with styles2/7 aliased;the second has8unique bodies. Both command headers use D0. Three consecutive actor12 speeches contain the letter:rumors of legendary Muramasa妖刀,its reputation as a bane of Tokugawa,the leader of Japan,and threatened eradication;an apparently concealed example somewhere in East Asia by an unnamed family/clan with a grudge against him;then Yukihisa\'s certainty that this is the object he has sought for years and his full signature. The conspicuously formal/archaic wording motivates the following reaction. The simple style6 reaction uniquely admits not understanding it;other styles call it typical of Yukihisa. A separate explicit actor11 reaction is also stored behind source control flow;do not assert that it and every dynamic style are one linear exchange. Lil\'s last line expresses tentative interest in searching. Final prose must make the letter readable but noticeably formal so the joke survives. Preserve source commands,picture/style state,predicate and relative sites;no earned eligibility,location,stat/item effect or natural activation is established by this source-only reading. Cultural names and the full signature need exact current/name/item consumers. Do not add history,dates,Tokugawa\'s title beyond the source,real magic,named clan,kinship,guaranteed find or specific location.'''
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);assert d['prior_English_unread'] and d['total_editorial_objects']==20
    image=NdsImage.open(d['source_ROM']);arm=image.read_file('/__arm9__.bin');names=[]
    for ident in [2,11,12]:
        fields=[]
        for delta in [0,4,8]:
            field=TABLE+ident*32+delta;pointer=struct.unpack_from('<I',arm,field)[0]
            if not pointer:fields.append(dict(field_offset=field,column=delta,source_null=True));continue
            raw=cstring(arm,pointer-BASE);fields.append(dict(field_offset=field,column=delta,pointer=pointer,source_storage_offset=pointer-BASE,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
        names.append(dict(actor_ID=ident,clean_fields=fields))
    rows=[]
    for r in d['records']+d['typed_actor_style_records']:
        r=deepcopy(r)
        if r['kind']=='progressive':gloss,note=SPEECH[r['source_record_index']]
        else:gloss,note=(INTRO if r['command_offset']==8 else REACTION)[r['source_reference']['offset']-r['command_offset']]
        r.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(r)
    assert len(rows)==20 and len({r['id'] for r in rows})==20
    ROOT.mkdir(parents=True);save(ROOT/'all20_clean_letter_and_voice_alternative_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),whole_exchange_context=CONTEXT,records=rows,source_actor_name_fields=names,source_commands=18,source_progressive_speeches=5,source_typed_commands=2,source_typed_stored_alternatives=15,source_style_slots=16,source_typed_D0_selectors=[208,208],all20_clean_objects_read_before_prior_English=True,prior_English_unread=True,all_source_context_prose_name_and_native_gates_pending=True,no_English_manuscript_or_wording_decisions_yet=True,no_current_English_or_historical_translation_consulted=True,full_signature_source='白樹玄丞行尚（ユキヒサ）',new_review_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False))
    print('All20 source-only glosses preserved:3 formal letter paragraphs/signature,2 other speeches and15 stored automatic voice alternatives. Older English unread;no credit.')
