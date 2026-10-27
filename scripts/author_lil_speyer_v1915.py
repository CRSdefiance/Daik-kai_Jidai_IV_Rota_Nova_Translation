"""Full Hamburg Speyer exchange,its choices,andthe separate aftermath: prose only."""
from copy import deepcopy
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Speyer_prose_v1915')
SOURCE=Path('work/analysis/lil_followups_after_London_v1914/source_followup_packets_and_random_query_classification.json')
DOC=Path('translations/lil_speyer_encounter_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_speyer_choices_editorial_draft_v1.json')

# Reviewed in the complete conversational exchange,including the alternate
# responses. These are localized paragraphs,not fitting edits to old slots.
SPEYER=[
('R',"Get that cargo aboard! Time is money. Move!",'Speyer orders the cargo loaded quickly and invokes time is money.','Retain the natural forceful commands andsource proverb,which establish his impatient commercial priorities.'),
('V',"Yessir...",'His subordinate gives a deferential drawn-out acknowledgment.','Localize the vocal reply rather than leave Japanese inEnglish;Sir ispolite address,not aknightly rank orkinship.'),
('V',"Young people these days... Pathetic! No wonder the Hanseatic League's in decline. But I won't let that happen while I'm around!",'Speyer blames young people for the Hanseatic League\'s decline and vows to prevent it.','Restore his disdain,causal complaint andself-important vow;these arehis opinions,not narrator judgments.'),
('V',"The Speyer Company has to make money if we're going to revive the Hanseatic League!",'Speyer says his company must profit to accomplish the League\'s revival.','Preserve the claimed obligation andmotive;the old line made profitable growth aguarantee ofrevival.'),
('V',"Yessir, yessir...",'The subordinate repeats the same deferential acknowledgment.','Keep the repeated weary compliance andits connection tothe first reply without inventing a newtopic.'),
('V',"Come on, everyone! Hurry up, or I'll leave you behind!",'Lil urges everyone to hurry and threatens to leave them behind.','Keep the conditional threat rather than claim shehas already abandoned them.'),
('R',"Wait for me! Still eating over here!",'Emilio asks them to wait because he is still eating.','Retain the natural shouted fragment andfood-focused humor;the complete exchange establishes whyhe trails behind.'),
('V',"What an impatient admiral...",'Fernando comments on how impatient the admiral is.','Preserve the trait andexasperation,not merely aone-time statement that sheisin arush.'),
('V',"{MACRO:FI}, wait! ...Oh no. It's him... This is bad!",'Camille calls for Lil to wait,recognizes the man and reacts with alarm.','Restore the full progression fromcalling torecognition andworry;do not invent howhe knows the man.'),
('V',"{MACRO:FI}... That name rings a bell... Ah, yes! You, little girl! Aren't you with that new company, {MACRO:FO}?",'Speyer recalls hearing Lil\'s name and identifies her with the newcomer company.','Keep his recollection,belittling address,newcomer status andboth genuine macros.'),
('V',"Little girl?! Who is this guy? What an obnoxious old man!",'Lil objects to being called a little girl and calls the stranger an irritating older man.','Preserve her rude offense. おじさん isnot anactual uncle;the older-man insult setsup his protest aboutage.'),
('V',"O-old man?! How dare you! I'm still young! And is that any way to speak to someone you've just met?!",'Speyer protests the older-man address,claims youth and complains about first-meeting manners.','Keep allthree reactions andhis wounded dignity;no actual age orrelationship isasserted.'),
('V',"Admiral, he's with the Speyer Company...",'The unnamed subordinate begins to identify the man by his company.','Keep the incomplete warning without prematurely adding head;the next optional line supplies his precise position. Normalize the sourcecompany spelling variant fromits unambiguous neighbors.'),
('R',"Careful, {MACRO:FI}! That's Martin Speyer, head of the Speyer Company!",'Camille identifies Martin Speyer as the company\'s head and warns Lil.','Retain the existing complete,natural warning. Martin matches clean マルティン andthe current native catalog;head isexplicit in総帥.'),
('V',"So what?! It's rude to call a lady a little girl! You... old... MAN!",'Lil dismisses his status and returns the etiquette complaint with a deliberately drawn-out older-man insult.','Preserve the taunting emphasis andself-description asa lady,not anoble title. No family relationship isintroduced.'),
('V',"You little brat! The Speyer Company will use its full strength to crush that puny company of yours!",'Speyer threatens to use his company\'s full strength to destroy Lil\'s small company.','Restore both the belittled company size andfull-strength threat without adding physical violence against individuals.'),
('V',"Come on, you two. This isn't some kids' quarrel...",'Fernando objects that this is not a children\'s quarrel.','Restore the sourceじゃない negation,which the older affirmative This is a kid\'s quarrel reversed.'),
('V',"Oh, shut up! That threat goes right back at you, with interest!",'Lil angrily returns Speyer\'s threat with added emphasis.','Localize the noshi gift-wrapping idiom byeffect aswith interest,not aliteral gift orfinancial transaction. Speyer\'s threat remains the referent evenwhen Fernando interjects.'),
('V',"W-wait, {MACRO:FI}! Mr. Speyer, she's joking! Joking! She can be a little... odd...",'Camille tries to smooth things over by calling Lil\'s words a joke and awkwardly describing her as odd.','Restore the repeated placation andawkward excuse that lead intoOw;do not add amental-health diagnosis or narrate anunshown strike.'),
('R',"Ow!",'Camille makes a brief cry of pain.','Retain the natural exclamation;the source doesnot require inventing the exact cause orinjury.'),
('V',"Just you watch! I won't let you ruin {MACRO:FO}!",'Lil declares that she will not allow her company to be destroyed.','Keep her determination andgenuine company macro rather than turn itinto anomniscient guarantee.'),
('V',"You little brat! Mark my words! We're leaving! I can't stand the sight of her!",'Speyer warns Lil to remember this,orders departure and says looking at her infuriates him.','Keep the warning,departure andirritation inhis pompous angry voice without asserting a newbattle outcome.'),
('V',"Yessir...",'The subordinate acknowledges Speyer\'s departure order.','Repeat the established subordinate\'s deferential reply;do not invent a newidentity.'),
('V',"One sharp word leads to another... It was like having two of you, {MACRO:FI}.",'Camille comments on the traded provocations and says it was like having two Lils present.','Keep both the escalating-insults observation andthe two-of-you joke withthe genuine captain-name macro.'),
('V',"Why do you have to pick a fight over everything? You're making enemies for no reason!",'Camille complains that Lil needlessly fights and increases their enemies.','Express both parts asnatural frustrated speech without introducing a different strategic danger.'),
('V',"Because that old man was so obnoxious!",'Lil defends herself by saying Speyer was extremely unpleasant.','Preserve her childish justification andthe socially irritating manner rather than add a newmoral accusation.'),
('R',"Honestly... such a child.",'Camille reacts to Lil\'s childishness.','Retain the idiomatic exasperated fragment;her following pout supplies the response andcontext.'),
('V',"Hmph! It's already over, Camille. What's the point of going on about it now?",'Lil dismisses Camille\'s complaints about what has already happened.','Restore her pout andcountercomplaint while replacing the superseded Kamil spelling withCamille.'),
('R',"So selfish...",'Camille calls Lil self-centered.','Retain the natural short reaction toher dismissal;it works aspart ofthe exchange.'),
('R',"Now we'll beat the Speyer Company fair and square!",'Lil resolves to defeat the Speyer Company openly and fairly.','Retain the existing natural declaration;the subsequent contract/share tutorial makes its commercial goal clear without adding physical destruction.'),
('V',"Hey, Camille! To beat the Speyer Company, we drive them out of the towns they have contracts with, right?",'Lil asks whether defeating the company means expelling it from its contracted towns.','Restore the explicit contracts andthe confirmation question,anduse approvedCamille.'),
('V',"Oh, you knew that? That's a surprise. I thought you'd ask how to put them out of business.",'Camille is surprised Lil knows and expected her to ask how to defeat the company.','Restore his explicit surprise andteasing setup forboth player-choice responses.'),
('V',"Sorry, sorry. Then let's fight them your way, {MACRO:FI}, whether that's in battle or through investment.",'Camille apologizes and proposes resisting by whichever method Lil favors,battle or investment.','Keep his repeated apology,collective plan andtwo methods;this is the response toher offended reaction,not the later tutorial explanation.'),
('V',"I know, I know! Just you watch, Speyer Company!",'Lil insists she understands and challenges the company.','Keep her insistence onalready knowing,rather than the oldGot it implying she hasjust learned the lesson.'),
('R',"Huh?",'Fernando reacts briefly.','Retain the natural short response inthis conditional exchange.'),
('R',"Wait... you don't know how?",'Camille realizes Lil is asking how because she does not know.','Retain the complete natural question;it follows the explanatory player choice.'),
('R',"Uh...",'Lil hesitates.','Retain the existing idiomatic hesitation without inventing a spoken excuse.'),
('V',"And you call yourself a merchant... This is as basic as it gets.",'Camille is incredulous that a merchant does not know this most basic principle.','Use a natural teasing rebuke rather than the awkward How are you a merchant construction.'),
('V',"Is it? Well, never mind that. Tell me how!",'Lil brushes off the embarrassment and asks to be taught.','Keep her nonchalance anddirect request rather than make her apologetic.'),
('V',"All right, {MACRO:FI}. To drive a rival out of a town, you have to cut its market share there to zero percent.",'Camille explains that expelling an opposing faction requires reducing its town share to zero.','Keep the threshold exact andspell literal percent asaword;preserve the real FI macro.'),
('V',"Oh, that's easy! Invest plenty, help the town out, and it'll take our side!",'Lil assumes that heavy investment and contributions will make the town support them.','Keep this asher premature assumption,which Camille immediately corrects;do not present itasa narrator rule.'),
('R',"Let me finish. You can't drive them out by investing alone.",'Camille says Lil should listen because investment alone cannot expel the rival.','Retain the existing natural correction andits explicit restriction.'),
('R',"What? Why not?",'Lil asks why investment is insufficient.','Retain the natural surprised follow-up.'),
('V',"If both sides are investing in a town, they're both useful to it, right? It can't just favor one of us.",'Camille explains that a town benefits from both investing factions and cannot simply side with one.','Restore the conditional reasoning;the old town needs both investors added anunnecessary claim ofneed.'),
('R',"Go to war with them. Then the town has to choose a side.",'Camille says entering a state of war forces the town to choose between the sides.','Retain the clear existing explanation ofthe required war state.'),
('V',"Which side will the town choose, then...? Oh, I get it! The one that gives it more money, right?",'Lil wonders which side the town chooses and realizes it favors the one giving more money.','Restore her question andmoment ofrealization;keep the money directed tothe town,not aninvented bribe toanindividual.'),
('V',"Right. Once we're at war, investing in the town lowers their share and raises ours by the same amount.",'Camille explains that investment during war transfers the same amount of town share from the opponent to the player.','Restore the explicit same-amount relationship andthe condition that war hasstarted.'),
('R',"So the town switches sides. How do we start a war?",'Lil summarizes the town switching sides and asks how to enter war.','Retain the existing natural transition tothe next mechanic.'),
('V',"Have your First Mate write a declaration of war at a Guild, or start a naval battle against their ships.",'Camille gives the alternatives of a declaration drafted by the adjutant at the Guild or attacking enemy ships in naval combat.','Use the current source-bound副官 UI label First Mate,verified through native86314 index1,while preserving both alternatives andthe written declaration.'),
('R',"Once at war, invest in their towns. Bit by bit, you'll drive them out.",'Camille says investing in the opponent\'s contracted towns during war gradually expels it.','Retain the natural existing instructions. Their towns refers back tothe explicitly established contracted towns inthe full exchange.'),
('V',"But what if they have 100 percent of the share in a town? We can't invest there!",'Lil asks what to do when the rival has a full town share and investment is unavailable.','Restore the exact 100 percent threshold andits consequence;never encode the literal amount withanASCII percent command.'),
('R',"Attack their ships near town.",'Camille says to initiate naval combat with the rival near the town in that case.','Retain the concise natural answer;the previous question supplies the specific town andcircumstance.'),
('V',"A naval defeat hurts a faction's reputation and cuts its share below 100 percent in towns near the battle.",'Camille explains that losing a naval battle lowers reputation and ends a full share in towns near that sea area.','Keep both consequences andthe local area,clarifying below100 rather than implying all share disappears. Spell literal percent asaword.'),
('R',"Then we can get in there and sign a contract! Nice work, Camille! Just you wait, Speyer Company!",'Lil realizes they can enter the market and sign a contract,praises Camille,and renews her challenge.','Retain the complete natural sequence andapprovedCamille name;get in iscommercial entry here,not aninvented invasion.'),
]
AFTERMATH=[
('R',"Poor Speyer...",'Camille expresses sympathy for Speyer.','Retain the existing natural expression ofsympathy;no death isasserted.'),
('V',"Getting his company ruined over a stupid feud like that... He's got to have regrets.",'Fernando supposes Speyer must regret his company being ruined over a pointless quarrel.','Keep the inference aboutregret inFernando\'s conversational voice;do not invent death orloss ofpersonal possessions.'),
('V',"Hmph. He brought it on himself. That's what he gets for trying to ruin {MACRO:FO}.",'Lil says Speyer deserved the outcome because he tried to destroy their company.','Preserve her vindictive judgment andthe attempt toruin the company,not merely attack it;keep FO.'),
]

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not CHOICES.exists()
    packet=read(SOURCE)
    image=NdsImage.open(packet['candidate'])
    clean=NdsImage.open('work/clean.nds')
    current=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    japanese=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    assert len(SPEYER)==54 and len(AFTERMATH)==3
    names={2:'Lil Argot',9:'Camille',14:'Emilio',20:'Fernando',29:'Martin Speyer',151:'Unnamed player-side voice;catalog Retainer',152:'Unnamed Speyer-side voice;catalog Retainer'}
    records=[]
    for number,lines in ((128,SPEYER),(25,AFTERMATH)):
        source=next(p for p in packet['packets'] if p['block']==number)
        assert len(source['records'])==len(lines)
        for index,(original,(decision,english,gloss,note)) in enumerate(zip(source['records'],lines,strict=True)):
            raw=bytes.fromhex(original['source_hex'])
            old=bytes.fromhex(original['current_hex'])
            ja,at=original['source_offset'],original['current_offset']
            assert japanese[number][ja:ja+len(raw)]==raw and current[number][at:at+len(old)]==old
            prefix=int(original['provisional_first_byte_hex'],16)
            ident=original['id']
            records.append(dict(id=ident,file_path='/data/SC2.DK4',block=number,
                record_index=int(ident.split('_R')[-1]),source_reference=dict(offset=ja,bytes=len(raw),header_offset=ja-5),
                current_reference=dict(offset=at,bytes=len(old),header_offset=at-5,record_index=current[number][:at].count(b'\0')),
                source_hex=raw.hex(),current_text_hex=old.hex(),source_complete_preamble_hex=original['complete_source_preamble_hex'],
                source_presentation_prefix_hex=f'{prefix:02x}',source_Japanese=original['source_Japanese_after_first_byte'],
                current_stored_English=original['current_English_after_first_byte'],speaker=names[prefix],
                source_meaning=gloss,english=f'{{SPEAKER:{prefix:02X}}}'+english+'{PAD}',
                editorial_decision='retain-wording' if decision=='R' else 'revise',localization_note=note,
                context=('Full Hamburg Speyer cargo encounter,reciprocal insults,optional crew responses,both player choices andthe complete town-share/war tutorial reviewed together. B25 isaseparate later aftermath requiring completed event128,not the next scene afterLondon. '
                    'The merchant rivalry iscommercial destruction,not anasserted death. No literaluncle relationship ornewrank isintroduced. Newscene display/preamble scope,choice dispatch,layout,actual capture andregistered integration remainpending.'),
                spoken_sequence_index=index,ancestor_0100_offsets=original['ancestor_0100_offsets'],
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    choices=[]
    event128=next(p for p in packet['packets'] if p['block']==128)
    commands=[c for c in event128['all_current_native_commands'] if c['word']==0x2100]
    assert len(commands)==1 and commands[0]['offset']==2314
    command=commands[0]
    for option,text in enumerate(("So how do we drive them out?","Don't mock me!")):
        refs=[]
        for b in (japanese[128],current[128]):
            at=command['offset']+6+struct.unpack_from('<H',b,command['offset']+2+option*2)[0]
            end=b.index(b'\0',at)
            refs.append(dict(offset=at,bytes=end-at,hex=b[at:end].hex(),text=b[at:end].decode('cp932')))
        assert refs[1]['text'].rstrip()==text
        choices.append(dict(id=f'DK4_CHOICE_B128_C2314_O{option}',file_path='/data/SC2.DK4',block=128,
            command_offset=2314,option_index=option,source_reference=refs[0],current_reference=refs[1],
            source_hex=refs[0]['hex'],current_text_hex=refs[1]['hex'],english=text,speaker='Lil Argot',
            source_meaning='Lil asks how to drive them out.' if option==0 else 'Lil objects to being treated as foolish.',
            localization_note='Retain the existing natural response toCamille\'s teasing. Stored option index andexact pointers are preserved;visible menu/result association still needs native dispatch proof.',
            context='The complete B128 exchange includes both the apology branch andthe full market-share tutorial. This labels the stored choice without assuming its native result index.',
            editorial_decision='retain-wording',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    arm=image.read_file('/__arm9__.bin')
    raw=Path(packet['snapshot']).read_bytes()
    cpu,get=get_machine(arm,raw)
    field=get(0x86314,1)
    pointer=struct.unpack('<I',cpu.mem_read(field,4))[0]
    label=bytes(cpu.mem_read(pointer,64)).split(b'\0')[0]
    assert label==b'First Mate' and bytes(cpu.mem_read(0x02000000,0x400000))==raw
    assert len(records)==57
    assert all(all(r['source_Japanese'].count(k)==r['english'].count('{MACRO:'+k+'}') for k in ('FI','FA','FO')) for r in records)
    ROOT.mkdir(parents=True)
    common=dict(translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',
        review_gates=['source','context','localization','naturalness'],formatting_review_pending=True,
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_ROM=packet['candidate'],
        current_ROM_sha256=packet['candidate_sha256'],source_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        approved_names=['Rafael','Hodram','Joakim','Maria','Camille'],full_goal_complete=False)
    save(DOC,dict(**common,format='dk4-editorial-source-manuscript-v1',encoder='dialogue-fixed-v1',
        dialogue_profile='lil-opening-editorial-native-v1',status='57-full-exchange-source-prose-reviewed;newscene-native-andrelease-pending',records=records))
    save(CHOICES,dict(**common,format='dk4-editorial-typed-choice-manuscript-v1',encoder='dialogue-relocatable-v1',
        status='two-source-context-choice-labels-retained;typed-dispatch-fonts-andrelease-pending',records=choices))
    revised=sum(r['editorial_decision']=='revise' for r in records)
    retained=57-revised+2
    save(ROOT/'source_context_and59_prose_reviews.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        reviewed_speeches=57,reviewed_choices=2,proposed_revisions=revised,justified_retentions=retained,
        original_FI_FA_FO_macro_counts_preserved=True,First_Mate_native_role_selector=0x02086314,
        role_index=1,role_pointer_field=field,role_pointer=pointer,current_native_label='First Mate',role_query_all4MiB_unchanged=True,
        body_format_full_controls_choice_dispatch_native_fonts_actual_gameplay_andrelease_pending=True,
        no_ROM_orledger_completion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_records=59,speeches=57,choice_labels=2,proposed_revisions=revised,
        justified_retentions=retained,native_role_label='First Mate',no_completion_credit=True))
