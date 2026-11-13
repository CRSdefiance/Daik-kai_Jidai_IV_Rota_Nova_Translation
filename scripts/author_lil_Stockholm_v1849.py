"""Source-first51-line Stockholm review;no formatting or release completion credit."""
from copy import deepcopy
from pathlib import Path
import re
import unicodedata
from dk4tool.dialogue.encoder import encode_fixed_dialogue,encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_prose_v1849')
OUT=Path('translations/lil_Stockholm_encounter_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json')

# Meaning precedes localization. All51 original spoken objects and neighbors,
# including the conditional Gerhard exchange,were read as a complete source unit.
PROSE=[
 (5,'Hodram has not seen the ship before and hopes it is not a pirate ship.',
  "I haven't seen that ship before. I hope they're not pirates...",
  'Restore the first-person observation in natural restrained speech;his worry is not an actual accusation.'),
 (9,'Lil demands to know what the strangers want with her ship and calls them rude for staring at it and suggesting piracy.',
  'Hey, you! What do you want with my ship? First you stare at it, then you call us pirates? How rude!',
  'Preserve staring,the ship andpiracy accusation in her indignant interpretation;use natural confrontational questions.'),
 (12,'Hodram asks whether the ship belongs to Lil,using a familiar form of address.',
  "So... that's your ship?",
  'English cannot reproduce the social register ofおまえ through the literal word you;the next line localizes her offended response without inventing an insult orrelationship.'),
 (16,'Lil confirms ownership and objects to Hodram addressing her so familiarly.',
  "Yes, it's mine! And watch how you talk to me!",
  'Replace the nonsensical literal objection to the English pronoun you with an idiomatic reprimand that conveys the same offense.'),
 (20,'Lil identifies Hodram as a military man from his appearance oruniform.',
  "You're in the military. I can tell by your uniform.",
  'Keep both identification andits visible basis;military is broader than army soldier andfits the naval context.'),
 (24,'Lil says she hates military people because they all use their authority to behave violently orbully others.',
  "I hate the military. They're all bullies who hide behind their authority!",
  'Preserve her angry generalization andthe abuse ofpower without presenting her opinion as narrator fact.'),
 (35,'Fernando addresses Lil andurges her to calm down.',
  '{MACRO:FI}, calm down.',
  'Retain the existing natural,brief attempt to defuse her anger;preserve the genuine captain-name macro.'),
 (41,'Camille reprimands Lil for being rude to someone she has only just met.',
  "{MACRO:FI}! That's no way to speak to someone you've only just met!",
  'Restore the first-meeting context omitted by the older generic admonishment;no friendship orrank is invented.'),
 (44,'Lil tells Camille to keep quiet.',
  'Keep quiet, Camille!',
  'Retain the direct,brusque existing command;it matches her irritation andthe explicit source name.'),
 (48,'Lil warns Hodram that trying to find fault with her orpick a fight will not succeed.',
  "If you're looking to pick a fight with me, think again!",
  'Keep the challenge andher determination without adding a gendered boast ornew threat.'),
 (52,'Hodram suppresses an irritated grunt.',
  '...Tch...!',
  'Retain the existing restrained vocal reaction;it is not an attack ornew spoken claim.'),
 (56,'Lil challenges Hodram to try violence,saying that is what a man withnothing butphysical strength would think of.',
  "What, are you going to hit me? Typical of a man who's got nothing going for him but muscle. Go on, try it!",
  'Express the physical-strength insult idiomatically without adding an explicit intelligence judgment;keep the challenge.'),
 (60,'Hodram tells Lil not to misunderstand andsays he has no intention ofstriking women orchildren.',
  'Do not get the wrong idea. I have no intention of striking women or children.',
  'Restore the warning against misunderstanding andhis explicit personal refusal;do not turn this into a targeting-policy slogan.'),
 (63,'Lil mockingly asks whether Hodram fancies himself a gentleman.',
  'Oh... Trying to play the gentleman?',
  'Preserve the skeptical response in natural English,including the article absent from the old fragment.'),
 (66,'Lil says she will not be fooled by that behavior.',
  "That still won't fool me!",
  'Retain the natural source-faithful refusal to trust his gentlemanly stance.'),
 (69,'Lil tells Camille they are leaving.',
  "Let's go, Camille!",
  'Retain the existing idiomatic departure instruction andthe approved name.'),
 (73,'Camille stammers for Lil to wait,apologizes to Hodram andtakes his leave.',
  "W-wait, {MACRO:FI}! Um... I'm sorry. Please excuse us...",
  'Preserve the flustered wait,apology andpolite departure,without adding a reason for leaving.'),
 (83,'Gerhard respectfully confirms that the man is Hodram Bergstrom.',
  'Hodram Bergstrom, I presume?',
  '殿 conveys respectful address here;it does not establish a peerage. Remove invented Lord while retaining formal courtesy andthe source abbreviated name.'),
 (87,'Hodram confirms his identity.',
  'Yes.',
  'Retain the brief,complete existing answer.'),
 (91,'Gerhard says he has heard ofHodram andintroduces himself as Gerhard Ardelknatts.',
  "I've heard of you. I'm Gerhard Ardelknatts.",
  'Match the existing native catalog spelling Gerhard Ardelknatts instead ofthe inconsistent Adelknauts in old prose;preserve both hearing ofHodram andself-introduction.'),
 (94,'Hodram recognizes Gerhard as Admiral Ardelknatts,the man known for hunting pirates.',
  'Ah, Admiral Ardelknatts, the pirate hunter?',
  'Preserve the explicit source admiral rank andpirate-hunting reputation;use the established native surname consistently.'),
 (97,'Gerhard says that was a long time ago.',
  'That was a long time ago...',
  'Use a natural complete reply that still conveys his restrained trailing reflection.'),
 (101,'Gerhard asks Hodram why he tolerated Lils earlier insults.',
  'Tell me, Hodram. Why did you put up with those insults?',
  'Preserve respectful inquiry without the invented Lord title oroverstating insults as physical abuse.'),
 (105,'Hodram says she was in no state to listen to reason and,pardon his bluntness,people like her are exhausting to deal with.',
  "She wasn't in any state to listen to reason. Forgive my bluntness, but people like that are exhausting.",
  'Preserve his judgment andthe qualifying apology,with natural phrasing rather than Japanese topic syntax.'),
 (108,'Gerhard acknowledges the explanation andsays he thinks he understands.',
  'I see... I think I understand.',
  'Restore his qualified understanding;the clipped old Understood removed that nuance.'),
 (121,'Hodram reacts to an approaching interruption andasks what it is.',
  'Hm? What is it?',
  'Express the source question naturally without implying a threat ornew event.'),
 (127,'Gerhard recognizes Camille withmild surprise.',
  'Hm? Camille...?',
  'Retain the existing name recognition andhesitation.'),
 (134,'Out ofbreath,Camille hesitantly apologizes for the earlier incident.',
  "Huff... huff... Um... I'm sorry about earlier.",
  'Preserve breathlessness andhesitant apology in natural youthful speech.'),
 (137,'Hodram asks whether Camille has something else to say.',
  'Is there something else?',
  'Restore the implied question in idiomatic English;More? sounded abruptly incomplete.'),
 (141,'Camille says he felt compelled to apologize andis truly sorry.',
  "I just had to apologize properly. I'm truly sorry!",
  'Keep his urgency andsincerity;do not replace the apology witha request that Hodram accept it.'),
 (144,'Hodram is silent.',
  '...',
  'Retain the deliberate silent response;normalize only English ellipsis punctuation.'),
 (148,'Camille asks them to forgive Lil andsays she was not trying to pick a fight withthem.',
  "Please forgive {MACRO:FI}. She wasn't trying to pick a fight with you.",
  'Preserve the runtime name andthe denial ofintent;English you covers the source plural without adding party composition.'),
 (151,'Camille explains she previously had a bad experience witha man who swaggered justbecause he was military,andis a little sensitive about it.',
  "She had a bad run-in with a man who threw his weight around just because he was in the military. She's a bit sensitive about it.",
  'Do not upgrade an unspecified bad experience into physical abuse. Preserve the man abusing military status andher present sensitivity.'),
 (154,'Camille insists Lil is kind anda very good girl,though she jumps to conclusions andis strongly convinced ofher assumptions.',
  "She's kind and a wonderful girl! She jumps to conclusions and can be awfully sure of herself, but {MACRO:FI} really is a good person!",
  'Keep kindness,the emphatic defense,both hasty conclusions andoverconfidence,andthe genuine FI macro. Do not erase her flaws orshorten to an old allocation.'),
 (157,'Hodram recalls Camilles name andgently checks it.',
  "Camille, wasn't it?",
  'Localize the friendly name check without inventing a title orfamily relationship for君.'),
 (161,'Camille is surprised,then confirms.',
  'Huh? Oh, yes.',
  'Retain the existing natural surprised confirmation.'),
 (165,'Hodram appreciates the courteous apology andsays he took no offense.',
  'I appreciate your gracious apology. I took no offense.',
  'Restore appreciation for the careful apology,while keeping his formal butcalm voice.'),
 (168,'Camille stammers in surprise andasks whether that is really true.',
  'R-really?!',
  'Retain the existing natural stammered question.'),
 (172,'Hodram imagines that having someone as capable as Camille nearby helps Lil make use ofher talents.',
  'Yes. I imagine having someone as capable as you by her side helps her make the most of her talents.',
  'Restore praise ofCamilles ability andthe source inference;do not assert that Lils talents newly become morally good.'),
 (176,'Camille modestly andhesitantly demurs at the praise.',
  "N-no, you're too kind...",
  'Use a natural modest response rather than an isolated denial that could suggest he rejects the substantive explanation.'),
 (180,'Hodram says not to worry about him andassures Camille that notone such bad military man serves in their fleet.',
  "You needn't worry about me. And no one in our fleet is anything like the man you described.",
  'Preserve the categorical reassurance andcomparison to the described man without narrowing naval personnel to army soldiers.'),
 (184,'Hodrams goal is simply to become one ofthe worlds strongest navies;he promises notto harm Camille andhis companions.',
  "My goal is simply to build one of the world's strongest navies. I won't harm any of you. You have my word.",
  'Restore one of rather than the sole strongest navy,andpreserve his explicit personal promise ofno harm.'),
 (196,'Camille thanks Hodram andhesitantly turns to address Gerhard.',
  'Thank you! And... Gerhard...',
  'Retain the existing natural gratitude andhesitant change ofaddressee.'),
 (200,'Gerhard responds to being addressed.',
  'Yes?',
  'Retain the natural English response to his name;it conveys the source prompt without adding a new question topic.'),
 (204,'Camille asks that Lil notbe told he came here.',
  "Please don't tell {MACRO:FI} I came here...",
  'Restore the specific secret,his visit,instead ofthe vague this. Preserve the genuine FI macro andhis hesitant request.'),
 (207,'Gerhard agrees to keep quiet.',
  "All right. I won't say a word.",
  'Replace the telegraphic Secret safe witha complete natural reassurance.'),
 (214,'Camille thanks them andpolitely takes his leave.',
  "Thank you! I'll be going, then!",
  'Use a natural polite departure suitable for the flustered young man;avoid the literal connector Then... please excuse me.'),
 (217,'Hodram is silent after Camille leaves.',
  '...',
  'Retain the source pause andexisting silent response;normalize only punctuation.'),
 (227,'Hodram regards Camille as a young man witha promising future.',
  'A young man with a promising future...',
  'Preserve the future-focused praise that isechoed at the scenes end.'),
 (233,'Gerhard agrees that Camille is a good young man.',
  "He's a fine young man...",
  'Make the third-person judgment explicit so it isnot mistaken for a direct address to someone whohas already left.'),
 (237,'Hodram agrees andsays he looks forward to Camilles future.',
  'Yes... I look forward to seeing what he accomplishes.',
  'Restore his affirmative reply andpersonal anticipation;A bright future awaits stated a certainty the source does not guarantee.')]

def visible(text):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip()

if __name__=='__main__':
    assert not ROOT.exists()and not OUT.exists()
    packet=read(PACKET);assert len(packet['records'])==len(PROSE)==51
    assert[r['record_index']for r in packet['records']]==[r[0]for r in PROSE]
    profile=get_dialogue_profile('lil-opening-editorial-native-v1');rows=[];allocations=[]
    for source,(index,meaning,english,note)in zip(packet['records'],PROSE,strict=True):
        row=deepcopy(source);row.pop('not_yet_source_prose_formatting_or_actual_completion',None)
        expected=[m for m in('FI','FA','FO')for _ in range(row['source_Japanese'].count(m))]
        authored=re.findall(r'\{MACRO:(FI|FA|FO)\}',english)
        assert sorted(authored)==sorted(expected),(index,expected,authored)
        expanded=english.replace('{MACRO:FI}','Lil').replace('{MACRO:FA}','Argot').replace('{MACRO:FO}','Argot Co.')
        decision='retain-wording'if visible(expanded)==visible(row['current_native_macro_English'])else'revise'
        row.update(source_meaning=meaning,english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english+'{PAD}',
            editorial_decision=decision,localization_note=note,
            context='Lil SC2B27 Stockholm/Hodram encounter. Full clean/current51 spoken objects and102 nested commands reviewed,including immediate spoken neighbors andconditional Gerhard exchange. '
                'Original event27/category5 explicitly selects town7 Stockholm;full native predicate accepts only in an offline destination copy,not a new actual visit. '
                'Original speaker mapping andcurrent native macro outputs are source-bound. Actual branch reachability,portraits,formatting andintegration remain pending.',
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False})
        rows.append(row);case={'id':row['id']}
        for mode,encoder,text in [('fixed',encode_fixed_dialogue,row['english']),
            ('size_independent_research',encode_relocatable_dialogue,row['english'].removesuffix('{PAD}'))]:
            try:
                result=encoder(bytes.fromhex(row['source_hex']),text,profile)
                case[mode]={'encodes':True,'formatted_markup':result.formatted_markup,
                    'diagnostics':[{'severity':d.severity,'code':d.code,'message':d.message}for d in result.diagnostics]}
            except ValueError as error:case[mode]={'encodes':False,'error':str(error),'prose_not_shortened_to_fit':True}
        allocations.append(case)
    doc={'format':'dk4-editorial-source-manuscript-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-fixed-v1','dialogue_profile':'lil-opening-editorial-native-v1','file_path':'/data/SC2.DK4',
        'review_gates':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
        'formatting_review_pending':True,'status':'51-source-context-prose-reviewed;native-format-reference-actual-release-pending',
        'source_context':str(PACKET),'source_context_sha256':sha(PACKET.read_bytes()),
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':packet['candidate'],
        'current_ROM_sha256':packet['candidate_sha256'],'records':rows,
        'approved_names':['Rafael','Hodram','Joakim','Maria','Camille'],
        'speaker_catalog':packet['native_speaker_catalog'],
        'scope':'Complete original B27 source/prose review;allocation probe only. No approved relocation map,actual scene,integrated release orfull editorial completion.',
        'source_macro_counts_preserved_in_all51_logical_paragraphs':True}
    try:validate_natural_dialogue_batch(doc)
    except ValueError as error:assert 'formatting'in str(error).lower()
    else:raise AssertionError('Unreviewed formatting was accepted')
    ROOT.mkdir(parents=True);save(OUT,doc)
    revised=sum(r['editorial_decision']=='revise'for r in rows)
    save(ROOT/'all51_source_prose_and_allocation_probe.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),
        'source_context':str(PACKET),'source_context_sha256':sha(PACKET.read_bytes()),'cases':allocations,
        'revisions_proposed':revised,'wordings_retained_after_source_review':51-revised,
        'source_facts_rank_scope_and_approved_names_reviewed':True,'no_authored_linebreaks_oralignment':True,
        'no_formatting_warnings_waived':True,'no_ROM_registry_or_completion_count_change':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'source_prose_reviewed':51,'proposed_revisions':revised,'retained_wordings':51-revised,
        'fixed_encodes':sum(r['fixed']['encodes']for r in allocations),
        'size_independent_research_encodes':sum(r['size_independent_research']['encodes']for r in allocations),
        'formatting_native_reference_andactual_gates_open':True},flush=True)
