"""Review Rafael's East Asia conclusion, the Spanish confrontation and its aftermath."""

from inspect import getsource
from pathlib import Path

from scripts import register_rafael_tradehouse_festival_20261121 as parent
from scripts import review_rafael_pereira_village_20261121 as prior
from scripts import stage_late_trade_exchanges_20261118 as company
from scripts.review_company_name_dialogue_20261121 import TOKEN, logical
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_east_asia_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v4.json"
BLOCKS = (tuple(range(71, 81)), (), (), ())
CONTEXTS = {
    71: "Kurushima's defeat opens another lead on the Proof. The local trader gives alternate directions to Maria in Hangzhou and explains why crossing her would be a mistake.",
    72: "Maria acknowledges Rafael's strength in one exchange and hands over the promised plan in another. She keeps her distance in the first. In the second, Rafael slips into familiar address and Claudio makes the most of it.",
    73: "Claudio notices that Rafael is steadier. Rafael credits Eirene's advice after their argument. Claudio's reactions turn the discussion into teasing, and Rafael is left wondering why Claudio got so worked up.",
    74: "Townspeople anticipate the naval confrontation and warn Rafael when to approach Seville. The port worker also remembers the king's request.",
    75: "Simon's arrogance escalates a collision into a challenge. Rafael bursts out when Simon claims Portuguese merchants depend on Spain. Valdes intervenes, promises to settle it at sea and reveals why he dismissed them.",
    76: "Hayreddin acknowledges Rafael's growth and advises him to visit the priest in Alexandria if he defeats the Pasha. Rafael catches himself slipping into deferential speech.",
    77: "Rafael celebrates Mediterranean supremacy. Claudio acknowledges their naval defeat by Valdes and urges him to take pride in the wider victory. Rafael names the next objective.",
    78: "Claudio connects their strength to restoring Portugal's royal house. Rafael hesitates, then accepts the encouragement and rallies the crew.",
    79: "A priest recognizes their Mediterranean victory and offers an object. Arcadius guesses it leads to a Proof, but the pattern on the cloth puzzles Rafael.",
    80: "Two alternate summons. One port worker has been looking for Rafael and confirms his identity. The other publicly greets his return.",
}

# Wording stays in one paragraph. The phrases are constraints for the native formatter.
DECISIONS = """
71 5|||Rafael quietly acknowledges the faction's defeat. Kurushima remains the established shorthand.
71 10|Now we might have a shot at finding East Asia's Proof of Conquest.|a shot at finding;Proof of Conquest.|Keep Claudio's tentative optimism and name the object before the trader brings it up.
71 13|||The trader's exclamation is an immediate response to the news.
71 17|||Claudio answers with a short, self-satisfied laugh.
71 27|||The trader's direct question starts another lead and uses the established item term.
71 30|Yes, we are. Do you know anything about it?|Do you know anything|Rafael confirms the search and politely asks what the trader knows.
71 34|Word is Admiral Li knows something. You'll find her in Hangzhou.|Admiral Li knows something.;in Hangzhou.|The trader relays hearsay about her knowledge and gives the city where she is based.
71 39|Yes. Um, do you know where I can find Admiral Maria Li?|where I can find;Admiral Maria Li?|Preserve the affirmative opening and hesitation in this alternate approach.
71 43|Sure do. She's usually in Hangzhou.|usually in Hangzhou.|The trader readily answers and preserves the usual location rather than a certainty.
71 58|Is Admiral Li famous around here?|Admiral Li;famous around here?|Rafael asks an earnest question about her local reputation.
71 63|Famous? Around here, the Kurushima pirates were just about the only fools who'd dare cross Admiral Li.|the Kurushima pirates;cross Admiral Li.|Keep the trader's amused incredulity, regional scope and judgment about who dared oppose Maria.
71 67|Huh. Guess we'd better not take her on directly...|take her on directly...|Claudio draws a practical conclusion in his usual informal register.
71 74||Thank you for your help.;let's head for Hangzhou!|Keep the courtesy toward the trader and the immediate turn toward setting out.
72 11|It seems I'll have to recognize you as the strongest power in these waters. Here, take this.|the strongest power;in these waters.|Maria's concession is cool and formal, with the power limited to this region.
72 21|||The pause and understated thanks show Rafael taking in the acknowledgment.
72 25|I suppose I have little choice. I'll stay here and see whether you're worthy of it.|I suppose I have little choice.;whether you're worthy of it.|Maria stays behind to judge whether he deserves the position she has just acknowledged.
72 31|||Rafael's unfinished question is appropriate when she starts to withdraw.
72 36|Who I am doesn't matter. You can forget about me.|Who I am doesn't matter.;forget about me.|Maria answers the unfinished question but declines to make her identity matter.
72 39|||Keep the unspoken response to her dismissal.
72 58|||Maria's brief praise fits the direct fulfillment of their bargain.
72 62|||The quick correction from Maria to Admiral Li preserves the joke about overfamiliarity.
72 67|Indeed. The admiral has been waiting here. Now then...|has been waiting here.|Xien's measured confirmation preserves the prior waiting and makes room for Maria's handover.
72 71|||The delivered plan is clearly the one she promised during their bargain.
72 77|FI, was it? Keep your guard up in other waters, too.|Keep your guard up;in other waters, too.|Maria recalls the substituted given name and cautions him beyond her own waters.
72 81|||Rafael's stammer and emphatic thanks give Claudio material for the next tease.
72 86|Heh. Look at you blush.|Look at you blush.|Claudio sounds like he is teasing Rafael right in front of him.
72 90|E-enough! Clau, we're leaving!|Clau, we're leaving!|Restore Rafael's flustered start and immediate order to leave.
72 94|Heh heh. Aye, aye, Admiral. Let's go!|Aye, aye, Admiral.|Claudio exaggerates his obedience to needle Rafael one last time.
73 6||changed lately, haven't you?;you've grown up...|Keep the friendly observation and the tentative tag question together where the width allows.
73 10|||Rafael's pleased laugh invites Claudio to explain.
73 15|You don't worry as much as you used to. You seem steadier, I guess.|as much as you used to.;You seem steadier,|Claudio describes the change in two understated observations.
73 18|You can tell, too? Well, I guess I can tell you. It's thanks to Eirene, actually.|Well, I guess I can tell you.;thanks to Eirene, actually.|Restore Rafael's decision to share the confidence before naming Eirene.
73 23|Eirene...? What's that supposed to mean?!|What's that supposed to mean?!|Claudio hears an implication Rafael hasn't made and gets sharp with him.
73 26|What do you mean? Huh? What are you getting mad about?|What are you getting mad about?|Rafael is confused by Claudio's tone before he explains the earlier fight.
73 31|Remember that fight we had? Eirene told me I didn't have to worry about everything by myself.|Remember that fight we had?;by myself.|Keep the particular argument and Eirene's advice about worrying alone.
73 36|I guess being the admiral and running FO went to my head. I thought I had to handle everything myself...|went to my head.;everything myself...|Rafael acknowledges both positions and admits that their responsibility had gone to his head. Place the company name inside the sentence so its suffix supplies no second period.
73 40|She said talking things over can make them easier. She was right. Eirene's like an older sister to me!|talking things over;like an older sister to me!|Rafael uses a simile for her steady advice and identifies talking as what actually helped.
73 44|||Claudio's silence lets Rafael continue without interpreting it aloud.
73 48|She's kind, she notices what people need, and she never makes you feel small.|she notices what people need,;makes you feel small.|Rafael admires her attentiveness and ease with people in conversational terms.
73 52|||Rafael's playful speculation preserves Eirene's secret and sets up Claudio's reaction.
73 56|||Claudio's pointed tag tips the swing from casual talk to personal defensiveness.
73 60|What? I just meant in general. Why are you getting so worked up? Oh! Wait a minute...|I just meant in general.;getting so worked up?;Wait a minute...|Rafael defuses the question, notices the reaction and leaves his realization unfinished.
73 65|||The double stammer and raised voice land the joke without making him confess his feelings.
73 69|Come on, I'm only kidding... You don't have to yell.|I'm only kidding...;don't have to yell.|Rafael walks back the tease and asks Claudio to stop shouting.
73 73|Y-you're the one saying weird stuff! I-I'm going out!|saying weird stuff!;I-I'm going out!|Claudio flings the accusation back and announces his exit through a stammer.
73 77|Yeah, yeah. See you later! ...Clau's the one acting strange...|See you later!;acting strange...|Keep the spoken send-off separate in tone from Rafael's trailing thought.
74 5|Mr. FA! You're finally settling things with Valdes, huh? Give Spain hell!|Mr. FA!;with Valdes, huh?;Give Spain hell!|The port worker greets Rafael with established respectful address and boisterous support for the fight. The name itself carries the exclamation.
74 8|The big fight's off Seville, right? Watch yourself out there!|off Seville, right?;Watch yourself out there!|Keep the location a confirmation question and the trader's parting concern direct.
74 12|Looks like more and more fleets are gathering.|more and more fleets|The shopkeeper reports an impression about the growing number of fleets.
74 16|So we head for Seville when we're ready to fight Spain. Keep that in mind, FI.|head for Seville;fight Spain.;mind, FI.|Claudio gets the practical instruction right and addresses Rafael by the substituted given name.
74 19|Right. The deciding battle with Valdes's forces will be at Seville. We'd better get ready first.|Valdes's forces;at Seville.;get ready first.|Rafael repeats the intended confrontation with Valdes's force and decides to prepare first.
74 24|||The guildmaster's concise warning tells him to stay clear until ready.
74 27|||Rafael's courteous promise suits the guildmaster's advice.
74 32||The king wanted to see you, sir.|The port worker remembers a separate request from the king and keeps the respectful voice.
75 6|Out of my way.|Out of my way.|Simon's curt order opens the collision without an animal insult absent from the source.
75 10|||Rafael's punctuation-only shock is timed to the collision.
75 15|Hey! You there!|You there!|Claudio sharply calls the stranger back before demanding an apology.
75 19|||Simon's deliberately formal question challenges Claudio's manners and status.
75 23|Who cares? You bumped into me, and now you're acting all high and mighty?!|You bumped into me,;high and mighty?!|Claudio throws the blame for the collision back at Simon and mocks his bearing.
75 27|You'd dare speak to me that way, knowing I'm of the Linares family of Cordoba...?|the Linares family;of Cordoba...?|Simon explicitly leans on his family and its city while keeping the original question.
75 30|||Rafael repeats the unfamiliar family name rather than pretending to recognize it.
75 43|D-do you suppose he's a nobleman?|he's a nobleman?|Preserve Janus's hesitation and speculation about status.
75 57|I have a feeling this is going to get ugly...|this is going to get ugly...|Julio sees the quarrel escalating and quietly warns of trouble.
75 64|I don't care if you're a Linares! You don't shove somebody and walk away without an apology!|if you're a Linares!;without an apology!|Claudio rejects the family name as an excuse and demands ordinary courtesy.
75 68|||Keep Simon's silence immediately before the glove appears.
75 72|Whoa! ...A glove?!|...A glove?!|Claudio reacts first and then recognizes the glove with surprise.
75 75||I challenge you to a duel.|Simon's measured challenge follows the glove and suits his formal tone.
75 79|||Claudio's one-word disbelief supports Rafael's more anxious protest.
75 83||Just like that?!;going a bit too far?|Preserve Rafael's stammer, disbelief and attempt to talk Simon down.
75 88|No man in the Spanish navy would stand silent while his honor is insulted.|in the Spanish navy;his honor is insulted.|Simon justifies the duel through naval honor and his refusal to remain silent.
75 91|Honor? Oh, come on. Is this who gets to run our Portugal? A bunch of crazed, spoiled noble brats?|run our Portugal?;spoiled noble brats?|Claudio's disbelief turns to a class insult and fear that men like Simon will rule Portugal.
75 94|Ah, you're Portuguese. That explains your attitude toward men of the Spanish navy.|you're Portuguese.;the Spanish navy.|Simon makes a condescending deduction without assigning an officer's rank to everyone he means.
75 98||Listen carefully.;under the protection;our Invincible Armada.|The order and named Armada keep Simon's claim of protection clear before Rafael challenges it.
75 102||trade in peace;day and night.|Simon's claim ties their trade directly to his fleet's continual fighting.
75 106|||Rafael is too angry to speak yet. Preserve the punctuation-only beat before Simon dismisses him.
75 111|I'll overlook your insolence today. Get out of my sight.|your insolence today.;Get out of my sight.|Simon grants a contemptuous reprieve for this encounter and orders them out of sight.
75 114|||Rafael's abrupt command interrupts Simon's dismissal and marks a shift in who is speaking up.
75 119|...You still don't understand?|still don't understand?|Simon's question is a threat and a rebuke after his explicit order.
75 123|You think you're the reason we're safe? You've got some nerve saying that!|the reason we're safe?;some nerve saying that!|Rafael repeats the protection claim in disbelief and angrily rejects it.
75 128|||Simon's short outburst shows that Rafael's reply surprised him.
75 132|We stand on our own two feet. FO will never bow to Spain!|on our own two feet.;bow to Spain!|Keep the faction substitution and Rafael's assertion of independence.
75 137|...So you're the insolent boy who's still pretending to be Portuguese.|the insolent boy;pretending to be Portuguese.|Simon's accusation of false nationality gives Rafael something specific to refute.
75 141|I'm not pretending! Portugal will always be my homeland! Never Spain!|I'm not pretending!;my homeland!;Never Spain!|Rafael repeats and refutes Simon's charge, then claims Portugal as his enduring homeland.
75 146|Still clinging to a country that's gone? How pathetic.|Still clinging;How pathetic.|Simon sneers at Rafael's refusal to let go of Portugal.
75 150|Portugal isn't gone... We'll bring it back! Just watch us!|Portugal isn't gone...;We'll bring it back!|Rafael builds from denial to a collective promise of restoration.
75 155|Restore Portugal? You have some nerve.|Restore Portugal?;You have some nerve.|Simon echoes the pledge before treating it as treason.
75 158||the Spanish crown.;cannot be allowed to live.|Simon uses the language of rebellion as his justification for what follows.
75 162||no need to trouble Valdes.;cut you down myself,|Keep Simon's threat in his own voice and keep cut you down together.
75 166|||Rafael's stammer concedes fear while the volunteer accepts the challenge.
75 171|Heh. You can cry all you want once we get started. I'm not going easy on you!|once we get started.;going easy on you!|Claudio keeps the taunting laugh and says he will show no mercy even if Simon starts crying mid-duel.
75 174|Simon! What are you doing?!|What are you doing?!|Valdes calls Simon to account as soon as he arrives.
75 177|||Simon's startled stutter and respectful address show his composure giving way.
75 180|Ah! We're surrounded!|We're surrounded!|The discovery is sudden. Rafael blurts it out before Claudio confirms there's no route away.
75 184|W-we can't get out of here...!|can't get out of here...!|Claudio loses his swagger and stammers at being surrounded.
75 188||His Imperial Majesty.;I was about to execute them.|Simon gives his deferential report and states his own intent to execute them.
75 191|||Valdes asks for the charge before hearing Simon's explanation.
75 195|Yes, sir. They've been talking openly about restoring Portugal. Sedition, plain and simple.|about restoring Portugal.;plain and simple.|Simon characterizes Rafael's stated aim as seditious. The judgment remains his.
75 198|Portugal? Are you with FO, then?|with FO, then?|Valdes recognizes the faction after hearing Portugal and asks for confirmation. Leave the supplied company suffix inside the sentence.
75 202|||Rafael's terse confirmation holds his ground before Valdes sends them away.
75 207|||The pause and abrupt dismissal give Simon and both sailors room for their stunned reactions.
75 210|||Rafael's reaction is silent and surprised at the unexpected order.
75 215|||Simon's brief question contrasts with his earlier certainty about the execution.
75 219|||Claudio has a wordless reaction distinct from Simon's spoken question.
75 223|We'll settle this at sea. Get out of this city now.|settle this at sea.;out of this city now.|Valdes defers the confrontation to the sea and orders immediate departure.
75 226|||Rafael voices frustration before Claudio openly questions the apparent mercy.
75 231|Think you're showing us mercy?!|showing us mercy?!|Claudio challenges Valdes's presumed reason for letting them go.
75 235||You expect to defeat us?|Valdes laughs off the suggestion of mercy and lays bare his contempt.
75 238|My fleet is invincible, as its name says. We stand firm in our ranks, with tradition and dignity. You're beneath my notice.|as its name says.;with tradition and dignity.;beneath my notice.|Keep the explicit boast behind the Invincible Armada's name, its standing and Valdes's personal contempt.
75 242|Damn it. You'll regret this!|You'll regret this!|Claudio throws a raw warning back at Valdes before leaving.
75 246|||Simon addresses Valdes formally as the exchange turns to their private response.
75 250|It ill suits you to quarrel with children, Simon.|to quarrel with children,|Valdes reprimands Simon while belittling their adversaries as children.
75 253|||Simon's deference, hesitation and unfinished objection make way for Valdes's explanation.
75 256|Don't you understand? I won't have the blood of the defeated staining this great royal capital.|the blood of the defeated;this great royal capital.|Valdes explains the ostensible reason and speaks as if the challengers were already defeated.
75 260|Ah! I-I see. I spoke rashly.|I spoke rashly.|Simon's immediate deference follows a moment of surprise. He acknowledges his rashness.
75 264||ideal target practice;our newly assembled;combined fleet.|Valdes then discloses the colder practical reason, which explains the earlier decision to fight at sea.
75 267|Of course, sir. You see further than I do.|You see further than I do.|Simon's flattery comes after Valdes reveals how he intends to use the encounter.
76 7|||Rafael's spontaneous greeting preserves Hayreddin's approved name and established rank.
76 12|...You've grown, FI. The Ottoman Pasha's forces are formidable, but you and your crew...|The Ottoman Pasha's forces;you and your crew...|Hayreddin acknowledges growth, assesses the opponent and leaves his confidence in Rafael implicit.
76 15||(...No, wait!)|Rafael catches himself answering too deferentially and immediately gives a bolder response.
76 20|If you manage to defeat the Pasha's forces, go to Alexandria and see the priest.|the Pasha's forces,;go to Alexandria;see the priest.|Hayreddin makes the visit conditional and names the city and the priest.
76 23|The priest in Alexandria...? All right. I'll remember.|The priest in Alexandria...?;All right.;I'll remember.|Rafael repeats the destination and means to remember the instruction. Keep his two-word acknowledgment together.
76 27|||Hayreddin closes with a short warning suitable for the stakes laid out.
76 31|||Claudio's rough familiarity fits his easy confidence and creates no kinship.
76 34|||Hayreddin's low chuckle and farewell answer Claudio's familiarity.
76 37|||Rafael sends him off with the respect he showed at the start.
77 5|We did it! FO is the top power in the Mediterranean!|the top power;in the Mediterranean!|The celebratory opening and defined region preserve Rafael's collective victory.
77 10|Valdes gave us a beating at sea, sure. A win's a win! Hold your head high!|gave us a beating at sea,;A win's a win!;Hold your head high!|Claudio frankly admits they lost the direct fight and insists the overall victory still counts.
77 13|You're right. Winning battles at sea isn't everything. Let's take over the Estado, the overseas trading network!|overseas trading network!|Restore the named Estado while keeping the established explanation of the objective.
78 5|We're the top Mediterranean power! FO backs the return of Portugal's royal house. Even Spain can't ignore us!|Portugal's royal house.;Even Spain can't ignore us!|Claudio links their regional power, support for restoring Portugal's royal house, and newfound influence with Spain.
78 9|Y-yeah. I hope so...|I hope so...|Rafael recognizes the claim but hesitates to share Claudio's confidence.
78 13|You've really earned the right to call yourself ruler of the seas! Hold your head up!|ruler of the seas!;Hold your head up!|Keep Claudio's exhortation as praise for power in practice and in name.
78 17|Y-yeah. You're right. Thanks, Clau!|Thanks, Clau!|Rafael's stammer relaxes into genuine gratitude.
78 21|You're our admiral, after all! We're almost there. Keep at it!|You're our admiral, after all!;We're almost there.|Claudio's familiar pride turns into a final push for effort.
78 24||the world's seas!|Rafael turns encouragement into a shared call for mastery of the seas.
78 29|||A drawn-out cheer is an idiomatic collective answer to Rafael's rally.
79 5|Well done, Mr. FA! You've won supremacy in the Mediterranean. Please accept this.|Well done, Mr. FA!;in the Mediterranean.;Please accept this.|The priest respectfully recognizes the regional victory and offers the object without naming it. The surname stays with the opening congratulations.
79 10|||Rafael's exhale and relief fit the long campaign just completed.
79 22|This must be another map to a Proof of Conquest. If I remember right, the Mediterranean treasure is some kind of crown...|a Proof of Conquest.;the Mediterranean treasure;some kind of crown...|Arcadius interprets the item and keeps his recollection about the crown qualified.
79 29|||Claudio turns Arcadius's explanation into a plain shared plan to look for it.
79 32|Huh? The pattern on this cloth doesn't look anything like a map...|The pattern on this cloth;anything like a map...|Rafael reacts to the object, then explains what about its appearance puzzles him.
80 13|Whew! I finally found you. You're Mr. FA, right? The king of Portugal is asking for you!|You're Mr. FA, right?;The king of Portugal;is asking for you!|The port worker is relieved to find him, checks the surname and states the king's request.
80 19||Mr. FA's back!;The king wants to see you!|Keep the public greeting on Rafael's return and the excited message in this separate alternative.
"""


company_source = checked_text(company.source, {
    'budget = b" " * (len(template) + 32)': (
        'budget = b" " * (len(template) + 64)\n'
        '    if current.count(10) >= 4:\n'
        '        budget = b"\\n" * 4 + budget'
    ),
    'assert plan["expected_native_pages"] == 1 and all':
        'assert 1 <= plan["expected_native_pages"] <= (2 if current.count(10) >= 4 else 1) and all',
})
company_scope = company.planner_scope.copy()
exec(compile(company_source, __file__ + "::company-width-and-existing-pagination", "exec"), company_scope)


def plan_progressive(row, selector, current, original):
    planner = company_scope["plan_progressive"] if "FO" in TOKEN.findall(row["english"]) else prior.plan_progressive
    return planner(row, selector, current, original)


source = checked_text(getsource(prior.main), {
    'context=CONTEXTS[block] if block in CONTEXTS else village_context(number)': 'context=CONTEXTS[block]',
    'assert len(records) == 197 and not earlier and not decisions': 'assert len(records) == 142 and not earlier and not decisions',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
