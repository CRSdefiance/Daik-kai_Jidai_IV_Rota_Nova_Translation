"""Review the remaining contextual exchanges in Rafael's B221–240 packet."""

from inspect import getsource

from scripts import review_rafael_B221_B224_20261122 as first
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = first.paired.ROOT / "contextual_decisions_B227_B239_v3.json"
DECISIONS = {
    227: """
5|||Manuel wonders who built the ruins and why, then compares them to the mines from the Old Testament. Preserve this as his impression.
8|||The guard recognizes the subject of their conversation and asks whether they know the legend.
11|||Manuel reacts with a short question before the man addresses Rafael directly.
15|Excuse the interruption. Are you Admiral FA?|Are you Admiral FA?|The guard respectfully checks the captain's title and name. Preserve the surname substitution and the question tag.
19|||Rafael confirms both his names in their original order and asks what the guard wants.
24|||The guard starts by thanking Rafael on behalf of the townspeople for the investment. Keep the specific reason for their gratitude.
27|||Rafael downplays his contribution modestly before hearing what else the man has to say.
31|||The guard asks whether Rafael knows the rumor associated with King Solomon and continues to address him formally.
35|||Rafael's brief question prompts the guard to tell the full rumor.
40|They say King Solomon was so skilled in his arts, he could command even a demon king.|a demon king.|Keep Solomon's skill, its claimed extent and the legendary framing.
44|||Rafael repeats the unfamiliar detail and asks the guard to continue.
49|According to the rumor, a weapon tied to that demon king was sealed away on an icy island far to the northwest.|that demon king;on an icy island;far to the northwest.|The guard qualifies the weapon's association and its location as a rumor and describes the island relative to this town.
52|||The guard explains why he chose to tell this admiral, politely suggesting Rafael could wield such a weapon. Keep the surname token.
55|An icy island, far northwest... Could that be Iceland?|far northwest...;Could that be Iceland?|Manuel repeats the clue and tentatively offers Iceland. Preserve the pause and the question.
58|A weapon named for a demon king, huh? Thanks for telling me. I'll look for it.|a demon king, huh?;Thanks for telling me.|Rafael repeats his interpretation of the weapon's name and thanks the source before committing to look.
""",
    228: """
5|||The woman asks about the king before identifying herself. The trailing words sustain the uncertainty.
9|You again! You're bad for business. Get out of here!|You're bad for business.;Get out of here!|The shopkeeper recognizes her and angrily orders her away for disrupting business.
13|||She keeps searching for the king and the sword bearer despite the shopkeeper's interruption.
16|Are you all right? Who are you?||Rafael first asks what is wrong, then asks for her identity. Keep his concern after the rudeness.
20|||She introduces herself as Vivian and claims to have forged King Arthur's sacred sword.
23|||Rafael repeats Arthur's name in surprise before she explains further.
28|||Vivian says the king sleeps and the sword still seeks a champion. The poetic turn belongs to her account.
31|Champion, seek the sacred sword Excalibur! The king sleeps on Avalon, and the sword is waiting for you there!|sacred sword Excalibur!;The king sleeps on Avalon,;waiting for you there!|Vivian gives the sword's name and search command and identifies Avalon as the king's resting place. She addresses Rafael as the champion.
34|||Rafael repeats the place name and admits it is unfamiliar.
44|||Claudio tentatively suggests asking at the tavern. Keep his uncertainty.
50|||Arcadius gives the same practical advice more directly in the alternate voice.
""",
    229: """
5|||Rafael politely asks the barkeep about Avalon. The familiar source address creates no family relationship.
9|This again? You believe that nonsense from the woman who calls herself a witch, too?|calls herself a witch, too?|The barkeep is weary of the question and scorns the woman's claims. The identification as a witch is her claim as he describes it.
13|They say Avalon lies just west of here.|just west of here.|The barkeep gives the broad location as hearsay, consistent with his skepticism.
17|||The barkeep dismisses Arthur as a fairy tale, says the question is familiar, and has heard of nobody finding Avalon.
""",
    230: """
5|||Ian respectfully tells the admiral he heard about a remarkable weapon in town. Preserve the source of the lead.
8|||Rafael asks both what kind of weapon and its name. The two direct questions fit his eagerness.
13|||Keep the item title, the association with Ares and the number of Olympian gods as Ian's account.
16|Hmm. What's so special about it? Where is it?|What's so special about it?;Where is it?|Rafael has heard the name but doesn't yet grasp the significance. He turns quickly to the location.
21|||Ian reports that armor named for other Olympian gods may also be nearby. The rumor remains qualified.
24|||Rafael starts to acknowledge the information and then realizes it gives him no definite location.
28|From the way people in town spoke, I'd say it's somewhere nearby. I'd dearly like to find it.|it's somewhere nearby.;I'd dearly like to find it.|Ian infers the general vicinity and personally wants to find the object. Keep his formal, understated enthusiasm.
32|||Rafael privately admits that Ian's interest surprised him before Ian notices his expression.
36|Admiral? What's that look for? Surprised I take an interest in legends?|What's that look for?;in legends?|Ian notices the look and asks Rafael directly whether he finds his interest in legends surprising.
40|||Rafael answers honestly and briefly, leaving Ian room to explain.
45|||Ian acknowledges the surprise and explains that these stories stir him. The imagined gods roam the surrounding lands.
48|To think a weapon they might have used could still be out there... It takes my mind straight back to ancient times.|could still be out there...;back to ancient times.|Ian imagines the possible survival of an ancient weapon and says the thought transports him. Keep both layers of uncertainty.
51|||Rafael ends with a thoughtful acknowledgment. The brief line leaves Ian's fascination with the last substantial word.
""",
    232: """
5|||Julian asks how Lucia is and immediately flatters her beautiful, regal eyes. His story about why he visits stays openly flirtatious.
8|Well, hello, Julian. Smooth as ever, I see.|Smooth as ever, I see.|Lucia greets him warmly and dryly points out his familiar charm.
12|||Julian pauses at a connection that has only just occurred to him.
16|||Lucia asks why he is staring and wonders whether there is something on her face.
19|||Julian conjectures that the legendary empress might have been like Lucia. Keep the comparison tentative as he introduces it.
23|||Lucia is skeptical and directly asks what the comparison is supposed to mean.
27|Sorry, that was out of nowhere. I just heard about some armor called the Empress Gown. It got me thinking.|that was out of nowhere.;the Empress Gown.;It got me thinking.|Julian acknowledges the abrupt change in subject and identifies the item with its approved name.
31|||Lucia repeats the item title, prompting the explanation.
35|||Julian reports the beautiful Chinese empress, her tyranny and her tragic end as a story he heard.
39|I imagine she was almost frighteningly beautiful. One look and she'd steal a man's heart. Doesn't that sound like you?|One look;a man's heart.;sound like you?|Julian imagines the empress's beauty, dramatizes its effect at a glance and then applies the compliment to Lucia.
42|||Lucia reasons that a tyrant would be spoiled and overbearing and asks whether he really thinks that of her.
46|||Julian turns the objection into a teasing claim about being charming when a little spoiled. Keep the judgment and the final tease in his voice.
50|Still, a gown that could protect a beautiful woman... Romantic, don't you think?|a beautiful woman...;Romantic, don't you think?|Julian pictures protective clothing for a beautiful woman and asks Lucia to share his view of it. Keep the short tag together.
53|||Lucia answers the romantic language dryly and says she's more interested in the empress's rings and necklaces.
57|You mean how much they cost? Women are so practical! Oh, I'd better go. See you later.|how much they cost?;Women are so practical!|Julian assumes she's thinking about price, makes his own generalization and abruptly leaves.
61|||Lucia says goodbye briefly before voicing her private frustration.
65|Oh, honestly... He always slips away right when I'm about to ask for something.|He always slips away;ask for something.|Lucia complains that Julian leaves whenever she's about to ask for a gift. Keep the timing and her rueful frustration.
""",
    233: """
5|Hey, you there! Don't just walk through our square!|our square!|The shopkeeper calls Rafael to a stop and frames the square as his own community's.
8|||Rafael asks whether there is something to see, taking the summons as local advice.
13|||The shopkeeper asks whether Rafael knows about the Crusades before challenging the telling he expects.
136_0|||The first choice affirms familiarity with the Crusades. It leads to the shopkeeper's challenge to that version.
136_1|||The second choice denies familiarity and leads to his description of the version told in Europe.
29|||On the familiar path he guesses Rafael learned about chivalrous knights reclaiming the Holy Land. Keep his skeptical framing and the short opening.
35|||On the unfamiliar path he attributes the chivalric account to Europe before contradicting it. Keep that attribution.
41|But those lies are meant to make them look good. The people here know the truth about the Crusaders.|make them look good.;the truth about the Crusaders.|The shopkeeper condemns that telling as self-serving and appeals to what his town remembers. This remains his accusation.
44|||Rafael asks what the man means by truth rather than adopting the claim himself.
49|I've heard a bit myself. They were after the wealth here, weren't they? They looted and killed all along the way. Nothing was off limits, from what I heard.|weren't they?;from what I heard.|Al Shin shares his own hearsay about wealth, looting and killing. Keep his question and the limits of his knowledge.
52|I can't stand hearing history twisted to suit them! The Crusaders weren't the heroes. Our Saladin was!|twisted to suit them!;Our Saladin was!|The shopkeeper rejects the account as distorted in their favor and names Saladin as his community's hero.
55|||Rafael repeats the unfamiliar name as a question, giving Al Shin the chance to explain.
60|||Al Shin places Saladin in Islamic history and says his significance goes beyond driving off the Crusaders.
64|He showed humanity in how he fought, how he treated prisoners and civilians, even in his terms for peace. He never stooped to anything dishonorable. An admirable man.|prisoners and civilians,;terms for peace.;An admirable man.|Al Shin gives three specific reasons for admiring Saladin's conduct and summarizes his personal judgment.
67|||Rafael reacts with straightforward admiration after hearing the account.
72|Come to think of it, I heard Saladin's armor went missing. If you'd like to follow his example, why not look for it?|Saladin's armor went missing.;why not look for it?|Al Shin recalls a rumor about the missing armor and ties the search to following Saladin's example. Keep the loss reported rather than confirmed.
""",
    234: """
5|......||Gerhard watches the sunset in silence. Use six ASCII periods to preserve the extended pause.
9|||Rafael recognizes Gerhard and asks what is on his mind as he watches the sunset.
13|||Gerhard says a story he heard in Japan moved him and admits that this is unusual for him.
17|||Rafael asks about the man in the story, drawing Gerhard out.
22|||Gerhard identifies Noritsune and places him centuries in the past, with the established name.
25|That long ago... What was he like?|What was he like?|Rafael pauses at how far back the story goes before asking what kind of man Noritsune was.
29|||Gerhard recounts the clan's former power, successive losses and looming destruction.
32|||Gerhard contrasts Noritsune's courage with the weakness he attributes to his kin. The unfinished clause leads into the battle.
35|They say that in the last battle at sea, he leaped across seven boats to reach the enemy commander's ship.|the last battle at sea,;leaped across seven boats;enemy commander's ship.|Preserve the story's number, the goal of reaching the enemy commander's ship and the reported framing.
39|||Gerhard says the warrior grew exhausted and disappeared into the strait with his armor and a soldier under each arm. Keep the account qualified.
42|||Keep Gerhard's surprise and the way he interprets the man's courage as revealing something about the East. The view remains his.
46|||Rafael shares the admiration with a pause and a simple reaction to that courage.
51|||Gerhard agrees and says men like him are hard to find now.
55|||Rafael notices how strongly the story affected Gerhard, echoing the admission that started the exchange.
59|...Into the strait, splendid armor and all...|Into the strait,;splendid armor and all...|Rafael turns the report over in his mind and picks out both the strait and the splendid armor as a clue.
63|I got carried away. I'd better get back to work.|I got carried away.;get back to work.|Gerhard catches himself telling a long story and returns to his duties.
""",
}

DECISIONS.update({
    235: """
STYLE_8_0|||The crew voice reports Ian's letter directly to the admiral. Keep the understated announcement.
STYLE_8_40|||The formal received-letter phrasing distinguishes this voice from the more casual announcers.
STYLE_8_80|||Keep the conversational announcement in the original two alias slots.
STYLE_8_116|||This voice politely offers the letter to the admiral. The phrasing needs no additional role or relationship.
STYLE_8_156|||You've got a letter retains the rougher voice and the writer's name.
STYLE_8_192|||The letter comes first and the admiral is addressed at the end. Keep the older voice's rhythm.
STYLE_8_228|||The direct exclamation and Ian as the subject suit the livelier original.
28|I found an interesting book at an antique shop the other day.|an interesting book;at an antique shop|Ian begins his letter with a recent find and preserves the kind of shop where he found it.
31|It's about Timur. Some two hundred years ago, he continued the line of the fading Mongol Empire. He built a vast empire stretching from Central to Western Asia.|Some two hundred years ago,;the fading Mongol Empire.;from Central to Western Asia.|Ian recounts the book's position on the fading Mongol line and the size and reach of Timur's new empire. The chronology is approximate.
34|The book says his coat of mail turned arrows aside and chipped the blades of enemy swords and spears.|turned arrows aside;enemy swords and spears.|Ian attributes the armor's protective qualities to the book and gives the two distinct effects described there.
37|||Keep the burial with Timur and the theft of the coat with other grave goods decades later.
40|||The thieves flee into the scorching desert, nearly see the sea, and die of exhaustion. Keep all three points in Ian's account.
44|Apparently nobody knew about this for a long time. The coat of mail still hasn't been found.|coat of mail;hasn't been found.|Ian says the account stayed unknown and the armor remains undiscovered. Keep both the uncertainty and the present state.
48|||Ian makes his suggestion conditional on the recipient's interest. Keep his own signature on its separate line.
56|Huh. Ian knows his Asian history, too.|Ian knows his Asian history, too.|Rafael is surprised at the range of Ian's knowledge. Keep Asian history as the subject.
68|The Mongol Empire once ruled the Russian people and was their enemy for years. No wonder Ian takes an interest.|the Russian people;enemy for years.;No wonder Ian takes an interest.|Cesare explains Ian's interest by recounting the Mongol Empire's rule and long enmity. This is Cesare's explanation.
71|||Rafael says he did not know that and compliments Cesare on his knowledge.
""",
    236: """
5|||Julian addresses Safia and immediately compliments her mysterious eyes. The line establishes his flirtation before the awkward comparison.
8|||Safia greets him by name without taking up the compliment yet.
11|...||Keep Julian's pause as he is drawn into the comparison. Use the ordinary ASCII ellipsis.
15|||Safia notices him looking at her and asks whether there is something on her face.
18|No... I nearly got lost in your eyes. Is that what it feels like to turn to stone?|lost in your eyes.;turn to stone?|Julian starts with a compliment and then wonders aloud about turning to stone. Preserve the metaphor and its awkward timing.
22|||Safia asks what he is talking about before the source of the comparison is clear.
26|I had the story of the Medusa Shield on my mind. It's supposed to be in the Tasman Sea. Your eyes made me think of it.|the Medusa Shield;in the Tasman Sea.;Your eyes|Julian explains the rumor that prompted the association, preserving the named shield and the Tasman Sea as hearsay.
29|||Safia recalls Medusa's snakes and asks whether Julian is calling her as frightening and ugly as the monster.
32|What? Of course not. Those beautiful eyes could capture me without your even uncovering your hair.|Those beautiful eyes;uncovering your hair.|Julian rejects the insult and means that her eyes alone could capture him. Preserve the reference to her covered hair without supplying a reason for it.
35|||Safia dismisses it as more of his joking. Keep her dry response before he elaborates.
39|||Julian imagines becoming a statue and spending eternity in the moonlight near her. Keep the extravagance in his own fantasy.
43|||Safia says she will not care for him if he turns to stone. The literal answer is part of her joke.
46|||Julian calls her cold, immediately makes that part of her charm, then says he's leaving.
50|||Safia says goodbye simply before examining her own reaction.
54|What a strange thing to say... Still, it made my heart flutter a little!|my heart flutter|Safia privately admits a small reaction after calling the comparison strange. Keep that change of feeling without adding a relationship.
""",
    237: """
5|||The child playing Charles Martel makes a grand challenge using the religious insult in the game they are playing.
9|||The other child cries out, surrenders and stammers through the retreat. His function here is the defeated participant in the children's game. Keep the separate actor 151 nameplate lead open.
12|||Rafael sees the children playing and asks Gerhard what they are doing.
17|||Gerhard explains that children play at being heroes and admire their own country's champions. Keep this as his broad observation.
21|||Rafael remembers Charles and asks for the rest of the name before hearing the explanation.
25|||Gerhard gives Charles Martel's name and the source's more-than-eight-hundred-years interval.
28|Between Tours and Poitiers, he drove back a Muslim army that had invaded Iberia and was pushing north.|Between Tours and Poitiers,;invaded Iberia;was pushing north.|Gerhard attributes the repulse to Martel and describes the army's movement from Iberia. Keep the named places and his account intact.
31|||Rafael recognizes that winning battles is common and asks what made this victory heroic.
36|||Gerhard directs attention to the significance of the victory.
40|||The claim about all of Europe becoming Muslim is Gerhard's counterfactual. Preserve his certainty and the fictional dialogue attribution.
44|||Rafael takes Gerhard's account to mean that Martel protected traditions and understands why the children admire him.
49|You've done no less than Charles Martel, Admiral.|Charles Martel, Admiral.|Gerhard compliments Rafael by comparing his deeds to Martel's and retains the direct address.
53|I look forward to seeing how future generations remember you, Admiral.|future generations;remember you, Admiral.|Gerhard closes by wondering how later generations will speak of the admiral. Keep his forward-looking admiration.
""",
    238: """
5|||Manuel courteously recognizes the admiral as they meet in the square.
8|||Rafael recognizes Manuel in return with the approved given name.
13|||Manuel asks whether Rafael is checking fashions and remarks on how busy he stays.
16|Ha ha, not exactly. Sometimes I just like to take in the town.|take in the town.|Rafael admits that he is enjoying the view on his walk. Keep his friendly laugh and reply to Manuel's assumption.
21|||Manuel briefly acknowledges Rafael's answer before Rafael asks after him.
25|What about you, Manuel? What brings you to the square?|What brings you to the square?|Rafael returns the question and asks what brought Manuel to the square.
29|Same as you, really. I'm out for a walk, picking up a little news as I go.|a little news as I go.|Manuel is taking a walk while listening for news, keeping the stated reason for his outing.
32|Admiral, do you know Attila, king of the Huns?|king of the Huns?|Manuel changes the subject by asking about Attila and identifies whose king he was.
36|||Rafael echoes the unfamiliar name and asks who he was.
40|||Manuel describes the Huns as nomadic horsemen of Asian origin and relays the threat Attila posed to both Roman empires. Keep the account in his speech.
44|||Rafael is impressed that Attila could cause trouble even for Rome.
48|||Manuel starts with the strongest empire's eventual rival and draws out his maxim about lasting power. Keep the two-part thought.
51|I see... Will FO ever rule the world's seas?|rule the world's seas?|Rafael applies Manuel's observation to his own company and wonders whether it can ever achieve supremacy. Keep the company substitution.
55|||Manuel answers with encouragement and makes their prospects depend on how hard they work.
58|Right. ...What made you bring him up?|What made you bring him up?|Rafael accepts the encouragement and pauses before asking why Manuel raised the subject.
62|||Manuel heard about armor associated with Attila and explicitly qualifies it as a rumor.
66|||Rafael asks for the details Manuel has yet to share.
71|They say someone took Attila's armor northwest after he died.|after he died.|Manuel relays the supposed direction, the removal and its timing after Attila's death.
75|||Rafael repeats the formulation about a king's armor taken northwest and infers how much Attila must have been feared.
79|Yes. Northwest of here... Northern Europe, perhaps?|Northern Europe, perhaps?|Manuel offers a tentative reading of the clue without supplying a confirmed destination.
""",
    239: """
5|||Yifa's two shouts come from her practice before Rafael speaks.
9|||Rafael notices that she's practicing the Taoist arts late and recognizes her effort.
13|||Yifa explains the courage it takes to face someone holding a sword. The remark sets up what she's been practicing.
16|If the blade scares you into holding back when you go in, you can get hurt even worse. You need the nerve to commit.|you can get hurt even worse.;You need the nerve to commit.|Yifa connects hesitation with being hurt and describes the mental resolve she needs. Keep her earnest explanation in her own voice.
19|||Yifa recalls a rumor about a training outfit that can chip a sword striking it and asks if Rafael has heard of it.
22|||Rafael's quick question conveys surprise at the claim.
27|||Yifa imagines being able to give her all if she had such an outfit. Keep it hypothetical before she catches herself.
30|Oops. My teacher would scold me for relying on gear. I can hear it now. 'Train yourself first!'|for relying on gear.;'Train yourself first!'|Yifa checks her own eagerness for the outfit and quotes her teacher's instruction to work on herself first.
34|||Yifa goes straight back to practicing, with the original two shouts to close the exchange.
""",
})

source = checked_text(getsource(first.main), {
    'len(records) == 56 and len({row["id"] for row in records}) == 56':
        'len(records) == 166 and len({row["id"] for row in records}) == 166',
    'for row in records) == 15': 'for row in records) == 7',
    'for row in records) == 5': 'for row in records) == 2',
    '            records.append(entry)':
        '''            if old == "……" and english == "......":
                entry["change_class"] = "glyph"
            records.append(entry)''',
})
scope = vars(first) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
