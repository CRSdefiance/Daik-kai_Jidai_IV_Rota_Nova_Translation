"""Clean-first alliance/map/patriotism exchanges; native names and current prose still pending."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B141_B160_clean_20261105')
DATA={
146:{
6:('The stranger identifies FU using the distinct formal-name substitution.',"...You are FU, aren't you?"),
10:('Rafael asks who the stranger is.',"And you are...?"),
15:('The stranger modestly introduces himself as Abraham ibn Uddin,a merchant based inBasra;exact approved name remains tobind.',"Forgive me. I should have introduced myself. I conduct a little business out of Basra. My name is Abraham ibn Uddin."),
18:('Rafael responds hesitantly topolite introduction.',"Oh... Pleased to meet you."),
23:('Uddin has often heard aboutFO forsome time andobserves its broad business activity.',"I've been hearing a great deal about FO for some time now. You seem to be doing rather well."),
26:('Rafael modestly dismisses the praise.',"Oh, not really..."),
31:('Uddin asks whether he may discuss something withRafael.',"There is something I'd like to discuss with you. May I?"),
34:('Rafael privately finds the quiet stranger dignified andprepares tochoose;not objectively sinister.',"(He's quiet, but he has quite a presence... All right...)"),
50:('On acceptance,Uddin says Rafael must travel some distance.',"I'm afraid I must ask you to come a little way."),
53:('Rafael agrees toaccompany him.',"Y-yes. I'll come with you."),
58:('Uddin sets their meeting atthe Guild inBasra.',"Let us meet at the Guild in Basra."),
62:('Rafael confirms the exact meeting place.',"Understood. The Guild in Basra."),
66:('Uddin confirms andsays he will go ahead.',"That's right. I shall go ahead and wait for you."),
69:('Rafael agrees tosee him later.',"All right. Until then."),
73:('Uddin takes leave.',"Until then."),
85:('On refusal,Rafael defers toconsult his companions,saying an admiral cannot decide alone.',"I'm sorry. I'd like to discuss this with my companions first. I can't make the decision on my own."),
90:('Uddin wanted Rafael’s own judgment,butapologizes andleaves withthe prospect ofmeeting again.',"It was your judgment I wished to hear... No, forgive me. I expect we shall meet again somewhere. Farewell."),
},
147:{
7:('Rafael is overwhelmed bywhat he sees;the source doesnot name the object here.',"Oh! Wow... Th-that's incredible...!"),
12:('Uddin apologizes forsurprising Rafael andchanges fromFI tohead-of-FO address,not a stated naval promotion.',"Forgive me for startling you, FI. Or perhaps I should address you as the head of FO."),
15:('Rafael self-corrects togreater deference towardUddin;no specific military rank is supplied.',"Mr. Uddin... I mean, sir..."),
19:('Uddin says he will get straight tothe matter.',"I shall come straight to the point."),
23:('Rafael nervously agrees.',"Y-yes."),
28:('Uddin asks Rafael toform a cooperative alliance withhim.',"Would you consider forming an alliance with us?"),
32:('Rafael hesitates overthe agreement.',"An alliance..."),
43:('One conditional response acknowledges that the sudden,forward request reasonably invites suspicion.',"I understand your suspicion. I am well aware that this is a sudden and rather forward request."),
47:('Uddin acknowledges that such an agreement is important forthe company andnot easy todecide.',"An alliance is an important matter for any company. It is not a decision to make lightly."),
53:('Another conditional response acknowledges suspicion andsays he investigated what happened tothem inAfrica.',"I understand your suspicion. Naturally, I have looked into what happened to you in Africa."),
56:('He understands their sensitivity toalliances,butdeliberately makes the request anyway.',"I know why an offer like this would trouble you. Even so, I am asking you to consider it."),
62:('Rafael remains silent anduncertain.',"..."),
67:('Uddin gives him a night tothink andprovides lodging,without demanding an immediate reply.',"I do not expect an answer now. Think it over tonight. That is all I wished to discuss. I have arranged a room for you. Please, go and rest."),
70:('An accompanying speaker guides Rafael;identity remains tobind.',"This way, please."),
74:('Rafael quietly thanks the guide.',"...Thank you."),
},
148:{
5:('Uddin asks whether Rafael has reached a decision.',"Have you decided?"),
9:('Rafael says he has thought it over.',"Yes. I've given it a great deal of thought..."),
13:('Uddin invites him tostate the decision.',"I see. Let me hear it."),
17:('Rafael pauses beforechoosing.',"..."),
33:('On acceptance,Rafael says he trusts Uddin andlooks forward tocooperation.',"I trust you. I look forward to working with you."),
37:('Uddin welcomes that trust andrespectfully addresses FA beforeproposing immediate business discussion.',"I'm glad to hear it. Now, Mr. FA, shall we get straight to business?"),
40:('Rafael nervously accepts.',"Y-yes. Of course."),
45:('Uddin has Rafael shown toanother room andinstructs the guide totake FA tothe reception room.',"I'll have you shown to another room. ...Please show Mr. FA to the reception room."),
48:('The guide formally acknowledges the instruction.',"Certainly, sir."),
53:('The alliance targets Lord Zamorin Nagalpur,whose power is concentrated aroundIndia;name/title binding remains pending.',"First, the purpose of our alliance. Our target is Lord Zamorin Nagalpur, who holds power around India."),
57:('Uddin criticizes Nagalpur’s greedy,undignified business practices asharmful tothem.',"The man worships money. His grasping, undignified business practices have caused us considerable trouble."),
62:('Nagalpur’s company is wealthy andpowerful,butUddin doesnot consider him an admirable man.',"His company has considerable wealth, and its power must not be underestimated. But I could hardly call him a man of character."),
66:('Uddin believes their combined forces caneventually defeat him.',"Together, we should be able to defeat him in time."),
69:('Rafael agrees.',"Yes."),
74:('Uddin raises the issue that may worry Rafael.',"Now, there is something I expect will concern you..."),
77:('Rafael anticipates the question ofwhat happens afterNagalpur isdefeated.',"What happens after we defeat the Nagalpur Company."),
82:('The alliance ends then;althoughnot a written contract,Uddin wants a subsequent nonaggression pact.',"Precisely. Our alliance will end there. We have no written contract, but afterward I would like us to agree to a nonaggression pact."),
85:('Rafael asks aboutthe nonaggression arrangement.',"A nonaggression pact...?"),
90:('Uddin allows limited shared markets aroundhis Arabian base,butleaves other cities andports toRafael’s discretion.',"My company is based in Arabia. We can share those markets, within reason. In other cities and ports, you may act as you see fit."),
93:('Rafael interprets the condition asavoiding excessive interference inArabia.',"So you want us to keep our distance in Arabia."),
97:('Uddin confirms andpromises nottointerfere withRafael either.',"Exactly. And I promise that we will not stand in your way, either."),
121:('The system says Uddin grants the player some market share inMuscat;no amount is given.',"Uddin granted you some of his market share in Muscat."),
152:('The system says Uddin grants some Socotra market share;no amount is given.',"Uddin granted you some of his market share in Socotra."),
163:('Rafael accepts andasks whether there isanything else.',"Understood. Is there anything else?"),
167:('Uddin says that isall andapologizes forthe time taken.',"No, that is all. Forgive me for taking up your time."),
170:('Rafael says his still-small FO will contribute tothe cooperation.',"Not at all. FO may still be small, but we'll do our part."),
174:('Uddin thanks Rafael andexpresses expectations.',"Thank you. I look forward to it."),
177:('Rafael enthusiastically commits todefeating Nagalpur.',"Then let's defeat Nagalpur!"),
182:('Uddin agrees that they will work together towardthat goal.',"Yes. Let us join forces and press onward."),
196:('On refusal,Uddin confirms that Rafael willnot accept an alliance.',"You will not accept the alliance, then?"),
200:('Rafael apologizes forrefusing.',"I'm sorry..."),
213:('One conditional response interprets refusal asunhealed hurt fromAfrica.',"The wounds you suffered in Africa have not healed, then."),
216:('Rafael denies that this iswhy he refused.',"No, that isn't it..."),
224:('Uddin respects Rafael’s judgment andproposes being rival enemies competing forIndian Ocean supremacy,thenquestions his phrasing.',"A man of your ability has made his choice. Then let us be rivals, each striving for supremacy in the Indian Ocean. ...Does that sound strange?"),
228:('Rafael uncertainly agrees andasks Uddin togo easy onhim.',"Y-yes... Go easy on us, won't you?"),
232:('Uddin bids farewell.',"Then farewell."),
},
149:{
5:('Rafael checks that the never-wilting lotus leaf is a map tothe Proof;exact item title remains pending.',"I've been wondering... This lotus leaf that never withers is a map to the Proof, right?"),
10:('Claudio considers Uddin a reliable source forthat claim.',"If Uddin says so, it must be."),
13:('Rafael wonders which other item shouldbe combined withit.',"I wonder what we're supposed to combine it with."),
32:('One alternative speaker proposes the Kushan-dynasty platter.',"What about this Kushan Platter?"),
40:('Another alternative speaker proposes the same platter;not an additional simultaneous proposal.',"What about this Kushan Platter?"),
46:('Rafael puts the leaf onthe platter,butnothing happens yet.',"Let's try putting the leaf on the platter. ...Nothing's happening."),
50:('Claudio asks what they shoulddo next.',"So what are we supposed to do?"),
},
150:{
5:('A woman recognizes the Kushan-dynasty platter andasks whether Rafael knows its old story;not an asserted family member.',"Oh? That's a Kushan Platter, isn't it? There's an old story about it. Have you heard it?"),
8:('Rafael asks forthe story.',"What sort of story?"),
13:('She reports that the platter was used fordivination:water withfloating flowers orleaves predicted the year’s events.',"They say it was used for divination. People would fill it with water and float flowers or leaves on it to predict the year's events."),
17:('Rafael wishes it might locate the Proof andtests floating the never-wilting leaf;water is now source-supported.',"If only it could tell us where the Proof is... Let's try floating the lotus leaf on the water."),
35:('One alternative speaker sees the leaf absorb water anda pattern appear inits veins,without identifying writing.',"Oh! The leaf's soaking up the water... Something's appearing in its veins!"),
44:('Another alternative speaker notices the same change.',"Oh! The leaf's soaking up the water... Something's appearing in its veins!"),
51:('Rafael identifies the pattern asthe map tothe Indian Ocean Proof.',"We did it! This is the map to the Proof in the Indian Ocean!"),
69:('One alternative speaker congratulates FI.',"We did it, FI!"),
77:('Another alternative speaker congratulates FI.',"We did it, FI!"),
83:('Rafael thanks the woman;おばさん is a familiar age/gender address,not proof ofkinship.',"It's all thanks to you, ma'am! Thank you!"),
106:('Hans explains that all Proof maps seem divided intotwo parts,andthey mustfirst find the two keys.',"The maps to the Proofs all seem to be divided in two. First, you must find the two keys."),
110:('Rafael asks aboutthe keys tothe maps.',"Keys to the maps...?"),
115:('Onlywhen two keys are obtained andproperly combined does a map tothe Proof appear.',"Only when you have both keys and combine them properly will the map to the Proof appear."),
118:('Rafael correctly infers that seven Proofs require fourteen keys inall.',"Then to find all seven Proofs, we'll need fourteen keys altogether?"),
123:('Hans confirms the arithmetic andrequirement.',"That's right."),
127:('Claudio is daunted byfourteen keys.',"Fourteen?! That won't be easy."),
130:('Hans laughs andsays somebody wouldalready have found them ifit wereeasy.',"Ho ho! If they were easy to find, someone would have done it long ago."),
134:('Claudio ruefully admits the logic andcomments that the world balances things that way.',"Fair point. Nothing ever comes easy, does it?"),
},
151:{
5:('A sailor urgently reports an emergency dispatch fromtheir homeland.',"Admiral! An urgent dispatch from home!"),
8:('Rafael asks the sailor toread it.',"Read it out."),
13:('The Spanish king will officially alsohold the Portuguese crown;no personal name ordate is given.',"It seems the King of Spain is now officially also King of Portugal!"),
17:('Claudio reacts inoutrage.',"What?!"),
29:('An alternative speaker reacts indisbelief.',"What?!"),
36:('Claudio fears their homeland Portugal has ceased toexist.',"Then Portugal... Our country's gone?!"),
46:('One speaker says Portugal exists inname,butimplies loss ofeffective independence.',"It still exists in name, but in practice..."),
52:('Another alternative makes the same distinction betweennominal andeffective existence.',"It still exists in name, but in practice..."),
58:('Rafael asks whether all Portuguese factions willfall underSpanish control.',"Does that mean every Portuguese faction will come under Spanish control?"),
63:('The sailor qualifies incomplete knowledge,butreports that Admiral Dinis de Albuquerque’s national forces have sided withSpain.',"We don't know the details, but the national fleet under Admiral Dinis de Albuquerque appears to have sided with Spain."),
66:('Rafael is wordlessly shocked.',"!!"),
71:('Claudio angrily condemns Albuquerque.',"That bastard Albuquerque!"),
101:('An alternative speaker is silently troubled.',"..."),
108:('Rafael says Albuquerque cannot beblamed iftheir country no longerexistsas an independent force.',"...If our country's gone, there's nothing he can do. We can't blame Admiral Albuquerque."),
113:('Claudio fears that Rafael tooaccepts Spanish rule andinsists he doesnot.',"FI! Not you, too! I won't accept this!"),
117:('Rafael proudly asserts Portuguese identity andrefuses toobey the Spanish king.',"Of course I'm Portuguese! And I'm proud of it! I'm not about to take orders from the King of Spain!"),
129:('Arcadius falls silent inrecognition ofthe loss ofa homeland.',"..."),
133:('Claudio asks what iswrong withArcadius.',"What's wrong, Arcadius?"),
137:('Arcadius says Greece was destroyed bythe Ottoman Turks long ago anddeeply understands Rafael’s feelings.',"It has been many years since my homeland, Greece, fell to the Ottoman Empire... I know all too well how the admiral feels."),
140:('Claudio is sobered into silence.',"..."),
147:('Rafael doesnot know howtorespond tothe crisis.',"But what can we do...?"),
152:('Claudio says rushing home wouldrequire too much time andsupplies,urging serious consideration.',"Even if we rushed home, it would take too much time and too many supplies... We need to think this through, FI."),
155:('Rafael says their present strength cannot defeat Spain afterits absorption ofPortugal’s forces.',"No. Even if we went home, we're not strong enough to defeat Spain now that it has absorbed the Portuguese fleet..."),
160:('He refuses toabandon their bid forcontrol inAsia just asit isgaining momentum.',"And we can't abandon our bid for control in Asia just as it's getting underway."),
171:('Claudio agrees that giving upFO’s rights inthis region wouldbe infuriating.',"True. I'd hate to just hand over FO's rights around here."),
176:('Julio likewise says they neednot giveAsian supremacy away forfree.',"Quite right. There's no reason to hand Asia over to someone else for nothing."),
183:('Rafael silently considers the decision.',"..."),
188:('Rafael decides nottoreturn home yet.',"I've decided! We're... not going back!"),
201:('An alternative speaker reacts inshock atthat decision.',"What?! Admiral!"),
208:('Claudio fears Rafael isgiving up entirely.',"FI, are you sure?! You're just going to give up?"),
212:('Rafael promises never togive up:he willgrow stronger inAsia,return andrestore Portugal.',"No! I'll never give up! We'll build our strength here in Asia, then go home! And we'll restore our homeland, Portugal!"),
224:('Arcadius is startled byRafael’s resolve.',"!!"),
239:('An alternative speaker is astonished.',"What?!"),
246:('Claudio wholeheartedly endorses Rafael’s spirited determination;男だ praises courage here.',"Yeah! That's it! That's the spirit, FI!"),
256:('Claudio laughs excitedly atthe ambitious new aim ofrestoring Portugal.',"Ha ha ha! Restoring Portugal! Now that's a big ambition!"),
261:('Another alternative speaker laughs atthe same ambitious aim,inthat speaker’s own slightlylessrough voice.',"Ha ha ha! Restoring Portugal! This has become quite an undertaking!"),
267:('Rafael challenges the Spanish fleet withan idiom ofpreparing fordefeat,not a literal washing instruction.',"Just you wait, Spanish fleet! We'll be coming for you!"),
293:('One companion recalls that the governor ofIndochina is Portuguese.',"Admiral FI! Come to think of it, isn't the governor of Indochina Portuguese?"),
297:('Rafael considers their commonnationality.',"A fellow Portuguese..."),
302:('That companion suggests forming an alliance throughshared origins.',"Why not try joining forces with him? Being from the same country might help."),
306:('Rafael agrees toconsider the suggestion.',"All right. I'll think about it."),
314:('Julio alternatively recalls the Portuguese governor ofIndochina.',"Oh, that's right. FI, listen. The governor of Indochina is Portuguese, if I remember correctly."),
317:('Rafael considers the same shared nationality onthis alternative branch.',"A fellow Portuguese..."),
322:('Julio believes the governor isbased inMalacca andmay sharetheir feelings,creating a possible alliance.',"I believe his base is Malacca. He may feel as you do. With a little luck, you might be able to join forces."),
325:('Rafael understands the possibility.',"I see."),
330:('Claudio asks whether Julio,whois Spanish,objects tohelping Portugal.',"But you're Spanish, Julio. That would mean helping Portugal. Are you all right with that?"),
334:('Julio values helping FI morethan nationality,andself-corrects his familiar kiddo address toadmiral;no family relationship is implied.',"I'd much rather help you, FI, kiddo... No, Admiral. That matters far more to me than petty distinctions like that."),
337:('Rafael is moved andthanks Julio respectfully.',"Julio... Thank you."),
}}

CONTEXT={
146:'A quiet,dignified merchant requests Rafael’s personal judgment. Acceptance leads tomeeting atthe Basra Guild;refusal is politelyexplained asconsulting the crew. Inner-choice fear isRafael’s reaction,not objectivevillainy. FU remains distinct.',
147:'Uddin’s imposing reception andformal offer are balanced byrespect forRafael’s deliberation. Alternative lines depend onthe African experience. No immediate acceptance ornaval promotion is asserted.',
148:'Acceptance negotiates limited Arabian coexistence,freedom elsewhere,an anti-Nagalpur alliance anda later nonaggression pact. Refusal remains courteous rivalry;one conditional line references Africa. Preserve every offer/limitation andavoid inventing a written treaty already signed.',
149:'The leaf andplatter are tried together without water,andnothing happens. Alternate speakers propose the same object. The nextcomplete exchange supplies the missing water step.',
150:'A woman’s reported old divination story prompts the water experiment. The map appears inleaf veins. Hans then explicitly teaches the two-keys-per-map rule:seven Proofs require fourteen keys. Do not turnthe olderwoman intoRafael’s aunt.',
151:'News ofSpain’s Portuguese crown provokes outrage,grief,deliberation andRafael’s resolute long-term plan. Keep nominalversuseffectiveindependence,his inability tofight now,the Asia objective andthe potentialPortuguese governor alliance. Julio’s Spanish identity makeshis personal loyalty meaningful. Do not add a monarch’s name,date,modernhistory explanation orfamily relationship.',
}


def main():
    out=ROOT/'B146_B151_meanings_andindependent_drafts_v1.json';assert not out.exists()
    packet_path=ROOT/'clean_source_packet.json';choices_path=ROOT/'clean_choice_objects.json'
    packet,choices=map(load,[packet_path,choices_path]);rows=[]
    for group in packet['groups']:
        b=group['block']
        if b not in DATA:continue
        assert {int(r['id'].split('_R')[-1]) for r in group['records']}==set(DATA[b]),b
        for original in group['records']:
            assert original['source_decode_error'] is None
            meaning,draft=DATA[b][int(original['id'].split('_R')[-1])];row=deepcopy(original)
            row.update(source_meaning=meaning,independent_English=draft,context=CONTEXT[b],
                speaker='Native source selector '+str(row['source_selector'])+'; approved binding pending',
                review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
                current_English_comparison_pending=True,approved_names_terms_titles_andruntime_substitutions_pending=True,new_credit=0)
            assert '\n' not in draft and not any(t in draft for t in ['{LB','{ALIGN','{PAD}'])
            rows.append(row)
    for original in choices['records']:
        if original['block'] not in [146,148]:continue
        row=deepcopy(original);b=row['block'];i=row['source_index']
        meaning,draft={
            (146,0):('Rafael privately feels that he canhardly refuse.','I can hardly refuse...'),
            (146,1):('Rafael finds the stranger intimidating anddecides againstacceptance.',"He's rather intimidating. Better not."),
            (148,0):('Accept the offered alliance.','I accept the alliance.'),
            (148,1):('Afterconsideration,politely decline the alliance.',"I'm afraid I can't accept."),
        }[(b,i)]
        row.update(source_meaning=meaning,independent_English=draft,context=CONTEXT[b],speaker='Player choice',
            review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
            current_English_comparison_pending=True,complete_native_menu_binding_andformatting_pending=True,new_credit=0)
        rows.append(row)
    assert len(rows)==145 and len({r['id'] for r in rows})==145
    save(out,dict(records=rows,records_count=145,ordinary_speeches=141,typed_captions=4,complete_blocks=list(DATA),source_contexts=CONTEXT,
        provisional_bindings=['Abraham ibn Uddin','Zamorin Nagalpur name/title','company-leader forms ofaddress',
            'Kushan Platter','never-wilting lotus-leaf item','nonaggression pact UI caption','Muscat/Socotra native city labels','FU native substitution'],
        all_five_gates_pending=True,no_current_English_extracted_for_this_intake_before_drafts=True,
        no_blanket_claim_of_historical_unexposure=True,no_ROM_or_registry_changes=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,choices_path,Path(__file__)]}))
    print('Sealed145 clean meanings/independent drafts acrosssix completeblocks;336 drafts total. All current comparisons/bindings/five gates pending;no credit.')


if __name__=='__main__':main()
