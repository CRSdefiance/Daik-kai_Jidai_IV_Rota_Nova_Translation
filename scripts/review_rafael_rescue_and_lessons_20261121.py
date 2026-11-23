"""Contextual review of Rafael's rescue, tutorial and clue encounters."""

from inspect import getsource

from scripts import register_rafael_ruins_and_proof_20261121 as parent
from scripts import review_rafael_ruins_and_proof_20261121 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
TOKEN, logical, plan_progressive = template.TOKEN, template.logical, template.plan_progressive
ROOT = template.ROOT.with_name("rafael_B121_B140_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source_final_parent.json", ROOT / "rafael_rescue_review_v4.json"
PRIOR = template.PRIOR.with_name("rafael_B121_B140_contextual_final_review_v2.json")
NAMES = template.NAMES.with_name("rafael_B121_B140_scoped_names_final_v2.json")
BLOCKS = ((121, 122, 123, 124, 125, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 138, 139, 140), (), (), ())
CONTEXTS = {
    121: "After the palace visit, a selected companion notices someone on a sandbar. A traveler asks for his grandson to be saved and another companion volunteers. The grateful grandfather offers a reward he'd earned from the governor.",
    122: "A selected companion calls attention to the jade. Carlo considers the value of jade in the New World and the East and what the quantities suggest about the building.",
    123: "The ruin has a foreign stone tablet. Janus or Arcadius argues from the lack of local stone and the dried-mud mosque. In the connected encounter, Maria challenges the bandits' revenge and offers their leader a place aboard.",
    124: "Benazir returns a gift with a tip about a building in India. Finding a map is the condition for getting there.",
    125: "A selected companion says the statue doesn't suit the building. Another set of lines considers whether it was once a figurehead or could be used as one.",
    126: "A villager links the finding to the tribe's spiritual well-being, leaves the knife with its finders, and gives a reward of 24,000 gold coins.",
    127: "Julio teaches the steering controls on the voyage to Ceuta. The player can voice concern about the wind before Julio explains when to seek port.",
    128: "Julio teaches sail settings, trimming and anchoring. He then asks Rafael to head to Athens, where the crew hopes to learn about its future and the promise to Hayreddin.",
    129: "Julio offers trading advice for Madeira, then expansion through Las Palmas and Verde. The player can also say they already understand.",
    132: "The Portuguese fleet prepares to face Valdes. Each side gives its own orders and labels for the opposing fleet.",
    133: "Julio proposes bringing his granddaughter Cristina aboard. Claudio nearly gives Arcadius away, and the crew comes to agree that they should sail for London.",
    134: "Vels's surprise attack injures Claudio. Rafael orders a retreat and Claudio warns them against seeking shelter in Amsterdam.",
    135: "Julian advises Rafael to build relationships in taverns for information. Rafael teases him about why he has been flirting, and Julian encourages him to follow his example.",
    136: "Claudio has a price for the Guiding Staff but no location. Julio tries to cheer him up by telling Rafael the legend or explaining Claudio's distress, depending on the player's choice.",
    137: "Julio explains how to profit from trade, what holds and market share limit, and which menu action completes the deal.",
    138: "Julio gives advice about recruiting sailors, offering a round and assigning enough crew to the flagship.",
    139: "Julio teaches how a connected sea route and two Deck View assignments make Auto Move possible. A sextant from Lisbon can qualify him as Surveyor when equipped.",
    140: "Janus explains how to invest in Arms and why Portugal may be able to raise it with less investment.",
}

# An empty English field retains the installed wording. The third field protects phrases when needed.
DECISIONS = """
121 6|||Rafael marvels at the size of the palace before proposing that they go back to town.
121 12|||The wordless reaction marks the interruption before a companion locates someone.
121 30|||The first companion variant spots the person and gives the exact sandbar location.
121 32|Wait. There's someone on that sandbar!||The quick change from uncertainty to alarm fits this variant and keeps the location.
121 34|Hmm? Look, there's someone out on the sandbar.||The deliberate delivery distinguishes this version of the same discovery.
121 36|Huh? Someone's out on the sandbar!||The more boyish variant keeps the location explicit as in the Japanese.
121 40|What's the matter?||Rafael addresses the distressed stranger he has just approached.
121 45|||The man is relieved to see travelers and urgently asks them to save his grandson.
121 48|||The selected companion repeats the relationship in surprise.
121 52|Grandpaa!||The child calls to his actual grandfather in a drawn-out cry.
121 56|||Rafael identifies an immediate threat in short, direct language.
121 72|I'll handle it!||The courteous variant volunteers to help while keeping the first-person commitment.
121 74|||The concise offer keeps the informal variant ready to leap in.
121 76|||This companion says she will go without identifying who the runtime will choose.
121 78|I've got this!||The rougher variant takes charge immediately.
121 80|||This more deliberate self-offer fits the elder register and urgent action.
121 82|I'm going in!||Keep the youthful resolve and immediate action distinct from the earlier volunteers.
121 86|||The drawn-out cry releases the child's fear after the rescue.
121 90|You're safe now! Oh, thank goodness!||The grandfather's relief follows the boy's fear and keeps the repeated reassurance in spirit.
121 93|Thank you, travelers! I can't thank you enough!|I can't thank you enough!|The grandfather's two emphatic expressions of gratitude read as a real outpouring.
121 96|||Rafael focuses on the grandson's safety instead of seeking a reward.
121 100|I have nothing to thank you with... Oh, wait! Just a moment!||Retain his initial uncertainty and the sudden thought of a suitable gift.
121 104|||The simple polite request lets him present the object before describing it.
121 108|||Rafael asks what the object is before hearing how it was earned.
121 113|When I was young, I drove off the bandits around here. The governor gave me this as a reward.||The grandfather attributes the object to the governor and names the deed that earned it.
121 116|||He distinguishes his lack of knowledge of its history from its reputed value.
121 120|Oh, I couldn't. You earned it for your bravery, sir. You should keep it.|You earned it;You should keep it.|Rafael respectfully treats the gift as a mark of the grandfather's own achievement.
121 124|No, no. You saved my grandson. I can't let you leave empty-handed. Please take it. It does me no good here.|leave empty-handed.|The grandfather insists that rescuing his grandson matters more to him than keeping the reward.
121 127|Then... Thank you. I'll take it.||Rafael relinquishes his objection and explicitly accepts the gift.
121 134|Safe travels, all of you.||The grandfather offers a parting wish to the travelers who helped.
121 138|Bye!||The boy calls a familiar goodbye to his rescuer. The source address adds no sibling relationship.
122 19|||The direct call to the admiral suits the first physical companion style at the find.
122 21|||The abrupt repeated summons suits the shorter companion style without naming the object first.
122 23|Admiral! Look what I found!||The youthful excitement signals a discovery without spoiling Rafael's identification.
122 27|Wow! Look at that jade!||Rafael identifies the stone and expresses admiration without making a new quality assessment.
122 40|Jade is highly prized in the New World, just as it is in the East.|the New World,;just as it is|The comparison is about how much both regions value this gem.
122 43|Anyone who offered this much jade must have thought this building was very important.|this much jade|The amount of the offerings supports an inference about the place's significance.
123 17|||The polite companion's summons leads Rafael to look without naming the tablet in advance.
123 19|||The brief summons suits the familiar styles sharing that body.
123 21|||The rougher call names the admiral and points to the discovery directly.
123 23|Look here, Admiral!||The elder variant gives a forceful prompt that is distinct from the polite one.
123 25|||The youthful body calls out in two beats and leaves the discovery unnamed.
123 29|||Rafael's unremarkable first impression gives Janus or Arcadius something to challenge.
123 48|...There's more to it than that. There's no local stone. That's why they built the mosque out of dried mud.|out of dried mud.|Janus uses the nearby mosque as evidence instead of claiming the tablet looks mystical.
123 51|Then the tablet wasn't made here?|wasn't made here?|Rafael makes the inference from the lack of stone and checks it with Janus.
123 55|||Janus confirms that the conclusion is probable and leaves room for uncertainty.
123 63|Admiral... There's more to this tablet than meets the eye.|than meets the eye.|Arcadius politely draws attention back to the tablet before explaining the evidence.
123 66|||Rafael asks for the explanation on this companion branch.
123 71|There's no stone around here at all. That's why even the mosque is made from dried mud.|even the mosque;from dried mud.|Arcadius stresses the absence of building stone and uses the mosque as an example.
123 75|||Rafael starts to infer the tablet's origin before Arcadius states it.
123 80|It means someone brought this tablet here from another place.|from another place.|Arcadius spells out the inference while leaving the place of origin unspecified.
123 83|||Rafael's acknowledgment closes the tablet observation naturally.
123 98|||The quiet voice-free notice alerts the viewer to a nearby conversation.
123 102|||Maria's wordless response precedes her hearing and challenging the bandits.
123 106|We're in a bind. We can't make a move like this...|make a move like this...|The bandit is frustrated because conditions have made a raid impractical.
123 109|Were you the ones raiding Sao Jorge?|raiding Sao Jorge?|Maria asks directly whether these are the people who kept attacking the town.
123 112|Wh-what?! Who the hell are you?||The stammer turns from surprise to hostility when the bandit realizes someone overheard him.
123 115|FO, that's who I'm with.|who I'm with.|Maria answers the bandit directly by naming her company. The name stays inside the sentence so its own period does not double the sentence punctuation.
123 119|What?! You're the ones who helped guard the town! You've made a mess of things for us!|helped guard the town!|The bandit blames their defense of the town for ruining his plans.
123 123|Now we can't raid it! How are we supposed to make a living?|make a living?|The bandit says raids were his livelihood, which prompts the next speaker's retort.
123 126|You've got some nerve for a bandit! We couldn't leave those townspeople to fend for themselves.|to fend for themselves.|Xien rebukes the bandit and explicitly grounds their aid in the townspeople's need.
123 130|Shut up! Those Europeans tore our village apart!|tore our village apart!|The bandit names the people he holds responsible and the harm they caused.
123 133|Say what you like. We're getting our revenge!|getting our revenge!|The bandit's resolve is defiant and collective.
123 136|Wait. Blame the merchants who trade in slaves and the soldiers who raid and plunder here in Africa.|trade in slaves;raid and plunder|Maria identifies the particular merchants and military men she holds responsible.
123 139|If you hate every European and attack them all alike, you'll be just as guilty as the people who wronged you.|just as guilty;who wronged you.|Maria confronts indiscriminate revenge in the terms of this exchange.
123 142|You talk like you've got it all figured out!|got it all figured out!|The bandit resents being lectured and lets Maria defend her claim.
123 146|Let go of your revenge. It won't do any good. It won't give you back what you've lost, will it?|what you've lost, will it?|Maria appeals to the losses he has just shared without telling him to forget them.
123 150|It'll only start the fighting all over again. More of your own people will suffer.|all over again.;will suffer.|Maria names the likely result and who will bear its cost.
123 154|||The stammer shows that the bandit is rattled as he asks what else they can do.
123 157|We have to end the rivalry among Europe's powers. It's behind conflicts all over the world's seas.|Europe's powers.|Maria connects the broader rivalry to the many conflicts without claiming it is their only cause.
123 161|||The startled punctuation marks the scale of what Maria is now proposing.
123 165|The great powers are carving up the world. They seek the Proofs to justify it. We're gathering them to stop that.|to justify it.|Maria explains why the other powers want the Proofs and why her company wants them.
123 168|||The bandit's disbelief at opposing the great powers keeps both the challenge and his stammer.
123 171|This isn't a bluff. Our influence already reaches Africa. I'm confident we can match the great powers and more.|I'm confident|Maria points to her own company's reach and states what she thinks it can do.
123 174|||The pause lets the proposition sink in before Maria makes the offer personal.
123 178|Well? What if you left that revenge of yours in our hands?|in our hands?|Maria asks him to place his grievance in their hands as the bridge to joining them.
123 181|||His short exclamation shows he has never considered that offer.
123 185|Come to sea with us. With that much resolve, I know you're up to it.|you're up to it.|Maria values his resolve as a reason to invite him aboard.
123 189|||The second pause precedes his own judgment of what staying would mean.
123 193|||The bandit concludes that he can accomplish nothing more by staying.
123 196|All right. I'll take my chances with you!|I'll take my chances with you!|The bandit chooses to trust Maria after weighing the alternative.
123 200|Glad to have you with us.||Maria welcomes the new ally without naming a new title or post.
123 207|I don't know if it has anything to do with the Proof you're after, but I found this tucked away in the ruins.|tucked away in the ruins.|The new ally offers the object while acknowledging that he does not know whether it is related.
123 210|||Maria reacts to the tablet by name and leaves its purpose open.
124 6|||The small interruption gets the captain's attention before the speaker gives her reason.
124 10|||The captain reacts wordlessly while she explains why she called him back.
124 14|You gave me a gift. I can't let it go at that. Let me tell you something in return.|something in return.|Her tip is her return gesture, with no commercial transaction implied.
124 18|There's a magnificent building in India. Now that you've come this far, it's well worth a visit.|well worth a visit.|She names India and encourages a detour without naming the site prematurely.
124 22|The catch is you'll need a map to find it. Do go if you get the chance.|a map to find it.|She identifies the actual obstacle and ends with encouragement.
124 25|Thanks. I'll go if I find a map.|if I find a map.|Rafael accepts the advice and makes the visit conditional on finding the map.
125 6|||The brief opening draws the admiral's eye to the statue before anyone offers an explanation.
125 10|||Rafael's neutral prompt leaves the observation to whichever companion speaks.
125 22|Its design doesn't seem to fit the building.|fit the building.|The first courteous variant notes a mismatch in design.
125 23|||The second formal variant already states the mismatch smoothly without explaining it too soon.
125 24|It sticks out, doesn't it?|sticks out, doesn't it?|The conversational variant notices the same mismatch with a natural tag.
125 25|||This lightly skeptical phrasing already gives the appropriate voice and keeps the question.
125 26|That doesn't go with the building at all, does it?|at all, does it?|This rougher variant asks the admiral to agree with the mismatch.
125 27|Hmm. Doesn't look as if it belongs here, does it?|belongs here, does it?|The deliberative register keeps its initial thought and question.
125 28|||This youthful variant gives a simple observation about the fit.
125 30|Wouldn't you say the design looks out of place here?|out of place here?|The more formal variant invites agreement after identifying the design as the issue.
125 33|||Rafael's small question leaves the chosen companion to explain their reasoning.
125 44|||The first variant describes a likeness and tentatively suggests former use.
125 45|It's shaped like a figurehead. In fact, it might be one.|shaped like a figurehead.|The speaker revises the description into a possibility while thinking aloud.
125 46|Doesn't it look like a figurehead? Maybe it really is one.|look like a figurehead?|The variant first checks the visual resemblance and then wonders aloud.
125 48|It looks like a figurehead... Oh, maybe it was one all along.|one all along.|This voice makes the discovery mid-thought and keeps it tentative.
125 49|Looks like a figurehead... Come to think of it, I bet it is.|a figurehead...|The casual version thinks aloud before landing on the explanation.
125 50|It has the shape of a figurehead... Why, that's what it is.|that's what it is.|The elder voice moves from careful observation to a confident conclusion.
125 51|See? We can use it as a figurehead.||The youthful style sees a possible use without claiming it was originally made for one.
125 52|It has the shape of a figurehead. Perhaps that's what it originally was.|the shape of a figurehead.|The formality and explicit reference to its original use distinguish the final variant.
125 55|||Rafael confirms the observation and gives the companion credit implicitly.
126 6|||The delighted interruption marks the discovery before the speaker explains what it means.
126 10|||The speaker bases the right to the knife specifically on who found it.
126 16|Thanks to you, our tribe has finally found something to sustain our spirits. Please accept this.|Please accept this.|The gift follows the tribe's finding something it can draw spiritual strength from.
126 20|||The notice preserves the exact reward of 24,000 gold coins.
126 27|Let's get back. The people in your fleet must be waiting.|must be waiting.|The speaker proposes returning and remembers that the whole fleet is waiting.
127 5|||The short opening names Ceuta as the first destination in the same order as the route.
127 9|||Julio turns the lesson from preparations to actually moving the ship.
127 13|||Checking which way the ship faces is the first step and the current wording is direct.
127 16|Give the crew a heading. Point the ship the way you want to sail.|Give the crew a heading.|Julio names the instruction to the crew and explains what giving a heading means.
127 20|||The control notice accurately offers either the D-Pad or the stylus.
127 23|||The two parallel instructions clearly connect both inputs to choosing a direction.
127 26|With the stylus, the sails turn to the best angle automatically. Tap the flagship to stop.|Tap the flagship to stop.|Clarify what the stylus does and keep the exact ship players need to touch.
127 29|||Julio's short check-in is enough to introduce the two original answers.
127 34|||The confident caption answers Julio naturally and keeps its original result.
127 36|What if the wind's against us?||The worried question answers the lesson clearly and leads to the wind explanation.
127 44|||Julio encourages the confident player without adding another lesson.
127 49|I can set a course. What if the wind doesn't fill the sails?|What if the wind|Rafael understands heading but asks whether the ship will make headway without useful wind.
127 54|||Julio distinguishes a headwind from the expected tailwind on the way to Ceuta.
127 58|Are we sure about that?|sure about that?|Rafael stays anxious after the reassurance without asking for a different destination.
127 63|||Julio gives the idiomatic reassurance and keeps Lisbon as the fallback.
127 70|||The list is direct and preserves the causes of trouble Julio names.
127 73|||Julio already distinguishes the limits of repairs at sea from the next action in port.
127 77|If your fleet runs into trouble, put in at a town to recover.|put in at a town to recover.|The notice gives the stated recovery rule and connects it to the problems just described.
127 80|||The southeast heading and the Route Map label are both correct.
128 12|||Julio offers another lesson and the given-name substitution gives the personal address.
128 15|||The brief polite acceptance lets Julio go directly to the controls.
128 20|||The overview identifies full sail and anchoring as the two practical topics.
128 23|||Keep the maximum-speed effect and the captain's need to direct the Sail Handlers at full sail.
128 26|||Keep one Sail Handler per mast and the resulting automatic adjustment at half sail.
128 29|||Julio contrasts the handling difficulty at full sail with half sail's utility in battle.
128 32|||Both uses of anchoring are stated directly, regrouping and waiting for an enemy.
128 36|||Rafael's small acknowledgment precedes the on-screen control summary.
128 42|||The two short sentences explain speed and stopping and work in the native panel.
128 46|||The A and B functions follow the actual increase and decrease in sail setting.
128 50|||This single input takes the ship from full sail to half sail and lowers speed.
128 53|||This single input takes the ship from half sail to anchor.
128 56|||Both presses and the intermediate half-sail state are spelled out.
128 60|||Julio already makes clear that half sail still needs the captain's help if the ship lacks Sail Handlers.
128 63|||Rafael's brief surprise is natural after the staffing caveat.
128 68|||Julio connects the captain's skill to a future need for full speed.
128 72|||Rafael stammers assent before the basic lesson continues.
128 77|||The short explanation states where useful wind should catch the sails.
128 81|||Keep the L and R labels and the relation between angle and speed.
128 85|||The left and right directions match the respective buttons and are paired cleanly.
128 89|||The stylus and tap-to-stop directions are already clear and were observed in this exact lesson.
128 93|||Julio relates heading to wind coming from behind the sails.
128 97|||The easy tailwind and more difficult headwind make a clear contrast in Julio's familiar voice.
128 101|||The gauge and longest-bar advice give players something concrete to watch.
128 104|||Julio hands off from instruction to practice.
128 107|||Rafael's upbeat reply accepts the chance to try the controls.
128 111|||Julio notices a forgotten matter without revealing the new destination yet.
128 114|||Rafael's brief pause leaves room for Julio's recollection.
128 128|||Julio asks for Athens with the original name substitution and a courteous tone.
128 132|||Rafael checks Athens with both Greece and its approximate eastern Mediterranean position.
128 137|||Julio gives the errand as a simple reason, leaving the details for the following exchange.
128 140|Wait. We're changing course for Julio's errand now?|Julio's errand|Claudio questions the destination and uses the older man's established name to avoid implying a family tie.
128 143|It's everyone's business. There's something I want to look into that'll matter to all of us later.|matter to all of us later.|Julio clarifies why he wants them all to go and leaves its nature open.
128 147|Something that'll matter to all of us... You mean like a goal for the crew?|a goal for the crew?|Rafael echoes Julio and proposes a goal as a hypothesis.
128 152|||Julio agrees cautiously and leaves Rafael's description approximate.
128 155|||The current reply distinguishes eventual importance from immediate urgency.
128 164|||Rafael connects the information to reaching Athens and asks for confirmation.
128 168|||Julio's plain confirmation suits the short question.
128 174|||The conditional line preserves the reason this also matters to the existing promise to Hayreddin.
128 180|||Claudio's enthusiasm uses Rafael's name substitution as the earlier request does.
128 184|||Rafael is immediately on board with the idea.
128 189|FI, let's not waste any time. I'm counting on you.|not waste any time.;I'm counting on you.|Use the familiar American idiom while keeping Julio's trust and the original name.
128 200|||Janus's question expresses curiosity. The ordinary Lisbon departure also showed it intact.
128 207|||Claudio deliberately turns the vague talk of goals into a rallying cry.
128 210|||Rafael is puzzled by how Claudio puts it, which is the joke's quiet ending.
129 5|||Julio asks about making money in trade and keeps Rafael's original name substitution.
129 11|||The short negative response naturally asks for help in the following branch.
129 13|||The confident reply conveys that the player already understands the basics.
129 20|||The advice specifies Madeira, its Portuguese ownership and its position southwest of Lisbon.
129 24|||The line keeps sugar as a local good, the company substitution and both regions for expansion.
129 27|||The amount to invest depends on the availability of market share in Madeira.
129 30|||Keep all three ports in the triangular trade and both ports for the expansion step.
129 33|||Julio states the two ports' geographic role and why Verde is particularly accessible.
129 36|||The strategy clearly connects repeated trade to larger ships and town market share.
129 39|||The relation between cargo holds, goods and profit per trip is clear in the current version.
129 42|||The short conclusion tells the player when to move on to more distant markets.
129 45|||The exact Commercial Investment label and how it might unlock local goods should carry forward.
129 48|||Julio makes the New World option conditional on the fleet's finances and tempers the advice.
129 52|||Rafael accepts the plan and promises effort rather than claiming the trade worked.
129 58|Will he be all right? An old man worries too much, I suppose.|worries too much,|Julio voices the unnecessary worry as he lets Rafael handle trade himself.
129 62|||Julio ends by encouraging the player to do things their own way.
132 13|All right! It's time to face Valdes. I'm counting on all of you!|I'm counting on all of you!|Rafael announces the deciding battle and asks everyone to do their part.
132 25|||The check of the crew's readiness fits the moment before the battle.
132 40|Heh! I'm ready anytime. Let 'em come!|Let 'em come!|Fernando's contempt and challenge answer the readiness check directly.
132 46|Yeah! We'll show 'em!||Claudio is eager to prove himself and answers in his own voice.
132 58|||The immediate assurance is enthusiastic without adding another instruction.
132 65|So that's the Portuguese fleet. Look at those reckless pups, defying the Spanish Empire even now.|the Spanish Empire|Valdes treats the fleet as insolent beginners and voices his allegiance himself.
132 68|I'll teach them a lesson. All ships, prepare for battle!|All ships, prepare for battle!|Keep Valdes's intent and the fleet-wide order intact.
132 71|||The subordinate repeats the exact order in a crisp acknowledgment.
132 75|||The silence leaves the command to form the line as the next beat.
132 79|||The compact command is clear naval language and retains formation.
132 83|||The speaker identifies the fleet as rebels from his own side's perspective and then orders the charge.
133 5|Oh, that reminds me...||Julio starts to remember someone they could bring along.
133 9|||Rafael waits for Julio to finish the thought.
133 14|Yes, of course. We should bring Cristina along.|bring Cristina along.|Julio arrives at the idea as he speaks and uses her established name.
133 17|Who's Cristina?||Rafael reasonably asks who Julio means.
133 22|My granddaughter. She's quite good with a sword, you know.|with a sword, you know.|Julio gives the real kinship and proudly supplies a specific skill.
133 25|A woman?! Sailing's a man's adventure. No way. We've already got a woman... Oops!|already got a woman...|Claudio voices his own prejudice, starts giving Arcadius away and catches himself.
133 28|||The private warning starts as a pointed throat-clearing to get Claudio's attention.
133 32|||Claudio stammers and falls back on his prior objection rather than revealing what he nearly said.
133 35|I think it's a good idea. If she's that good with a sword, she'll be a help.|good with a sword,|Rafael supports the idea and takes Julio's description of Cristina's skill seriously.
133 40|No, I still say no! Ow, ow! Wh-what are you doing?|Wh-what are you doing?|Claudio protests until the interruption makes him yelp, without naming an action the text leaves implicit.
133 43|(What's the difference between one and two?)|between one and two?|Arcadius quietly challenges Claudio's objection with the same logic about another woman.
133 47|(Right. You'd probably feel more at ease with another woman around, Arcadius.)|another woman around,|Rafael speaks privately to Arcadius and keeps the reason for the reassurance.
133 52|Ahem. I think we should bring her, too.|bring her, too.|Arcadius gives public support after the private aside without stating the reason out loud.
133 56|It'd make the trip more fun to have women aboard. What do you say, Clau?|What do you say, Clau?|Rafael makes the public case and leaves room for Claudio to relent.
133 60|(You too, FI? All right, fine.)|All right, fine.)|Claudio privately registers Rafael's part in the decision and preserves the name substitution.
133 64|If you all feel that strongly, I guess it's fine...|I guess it's fine...|Claudio concedes grudgingly after his private reply.
133 67|||Julio's wordless puzzlement follows the others' partly private dispute.
133 71|||Rafael returns the conversation to the practical question of where Cristina lives.
133 76|||Julio names London with no extra travel details.
133 80|All right. Let's head to London.|Let's head to London.|Rafael accepts the destination and makes the next action clear.
134 6|||The stammer starts the ambush before Rafael knows what it is.
134 11|We're under attack! Looks like pirates! Th-they caught us off guard. We can't fight back!|Looks like pirates!;caught us off guard.;We can't fight back!|The lookout reports an ambush, the probable attackers and why they cannot return fire.
134 15|That flag! It's Vels the pirate! We're in trouble, Admiral!|Vels the pirate!|Claudio knows the flag and confirms whom the lookout suspects.
134 19|I've heard of him. He's dangerous. Of all the people to run into...|Of all the people|Janus reacts from reputation and recognizes the danger of being discovered by Vels.
134 23|||Claudio uses Rafael's name substitution in the urgent warning.
134 27|||The wordless reaction falls before Claudio's cry and does not describe a blow.
134 32|||The sharp cry shows Claudio is hit or hurt without supplying an invented injury.
134 44|||Arcadius uses Claudio's full given name in a spontaneous cry.
134 51||Are you all right?!|Rafael calls him Clau and urgently asks about the injury. Keep the whole question readable.
134 56|It's just a scratch! Don't worry about me!|Don't worry about me!|Claudio minimizes the injury in his own words and tells Rafael where to put his attention.
134 60|Damn! Get us out of here, full speed!|full speed!|Rafael gives an urgent escape order with the full-speed instruction.
134 65|I think we lost them... We can't go on like this, though. Let's put in at the nearest port.|Let's put in|Rafael believes they escaped and decides they need a nearby port.
134 70|Amsterdam's too risky. Let's find another port.|another port.|Claudio warns against Amsterdam in particular and suggests an alternative without naming it.
135 5|You've sailed all over the world, Admiral. You must know the girls at a lot of taverns by now, right?|by now, right?|Julian assumes Rafael has made familiar acquaintances in taverns as he traveled.
135 9|||Rafael pushes back on the assumption of closeness without denying he knows some people.
135 14|Come on, Admiral. The girls who work in taverns know all sorts of things an adventurer needs to hear.|who work in taverns|Julian identifies useful sources of information as people Rafael should get to know.
135 18|They hear about treasures and enemy fleets. They might even know where to find ruins only the locals know about.|only the locals|Keep the two ordinary examples and the rarer local lead.
135 21|Make friends with girls all over the world! How can you call yourself an adventurer if you don't?|call yourself an adventurer|Julian exaggerates the idea as a standard for adventurers in his own breezy voice.
135 25|But... getting that close can't be easy, can it?|can't be easy, can it?|Rafael doubts the ease of the advice without assuming romantic success.
135 29|You can't just be another customer. They have dozens of people to talk to every day.|another customer.|Julian explains why normal customer conversation does not stand out.
135 32|A well-chosen gift is the surest way to win her over.|win her over.|Julian presents gift-giving as his favored approach and keeps the claim in his voice.
135 35|They all like different things. Find out what she's interested in, then give her something she'll like.|what she's interested in,|The instruction starts with finding out the person's own tastes.
135 43|Take Sakura in Osaka. I hear the Snow-Silk Robe she wants is sold in some town on the North Sea.|Snow-Silk Robe;the North Sea.|Keep both the recipient and item, and leave the town unspecified as a rumor.
135 52|Even someone who asks for very little is happy to get something she really wants.|she really wants.|Julian says a thoughtful gift can please even someone who asks for very little.
135 56|Oh, I get it. Flirting with one tavern girl after another was just part of being an adventurer...|being an adventurer...|Rafael applies Julian's justification to Julian's own behavior and leaves the deadpan implication open.
135 60|||Julian's stammer betrays his surprise at the turn in the conversation.
135 64|All right! I'll follow your lead!||Rafael says he will follow Julian's example in a quick enthusiastic reply.
135 69|Ha ha! That's the spirit!||Julian laughs and encourages the response with a contraction appropriate to his voice.
136 5|||Claudio calls out to Rafael with the exact substitution.
136 9|||Rafael's short question lets Claudio get to the rumor.
136 14|I heard about an amazing treasure!||Claudio's enthused lead-in leaves room for Rafael to ask what it is.
136 18|||Rafael is curious and asks what Claudio heard about.
136 23|||Claudio gives the established item title with some uncertainty.
136 26|What's so special about it?||Rafael looks for the reason Claudio is so excited.
136 31|The Guild's buying list shows a price higher than anything I've ever seen. And no one's even found it yet!|no one's even found it yet!|Keep the Guild's unusually high asking-for-find price and that nobody has found the item yet.
136 34|||Rafael's dry prompt lets Claudio reveal that he wants to look for it.
136 39|We'd be rich if we found it! Come on, what are we waiting for?|Come on,|Claudio is already eager to leave on the strength of the price alone.
136 43|||Rafael's pause exposes the missing destination.
136 48|Where the Guiding Staff is, of course!|the Guiding Staff|Claudio answers the obvious part of the question without naming a place.
136 52|||Rafael repeats the question more precisely.
136 57|||The small pause lands the anticlimax before Claudio admits he has no idea.
136 60|How are we supposed to look for it, then?|look for it, then?|Rafael points out that the search has no starting point.
136 65|||Claudio quietly concedes the obvious point.
136 69|Come on, Clau. With a lead that vague, we don't even know if it's real.|if it's real.|Rafael scolds Claudio and says there is also reason to doubt the treasure itself exists.
136 73|...Yeah, you're right. I guess that's that.|I guess that's that.|Claudio gives up on the search and begins taking the remark personally.
136 76|Why do I fall for things so easily...?|so easily...?|Claudio's dejection is about his own credulity.
136 79|||Rafael's hesitant use of the nickname registers Claudio's change in mood.
136 84|||Julio uses the affectionate older address that Rafael asks him to stop using next.
136 88|Oh, Julio. Could you stop calling me 'my boy'?|calling me 'my boy'?|Rafael asks Julio to retire the exact address he just used.
136 92|Oh, sorry. Old habits, you know.|Old habits, you know.|Julio apologizes and explains how it slipped out.
136 95|||The hesitant pivot returns to the established item title.
136 98|||Rafael checks that Julio means the object Claudio just described.
136 102|Well? Want to hear what I know?||Julio asks before sharing the legend and naturally opens the player choice.
136 107|||The affirmative caption politely asks Julio to tell the story and keeps the same result slot.
136 109|No, I've heard enough.||The dissatisfied reply keeps Julio's alternate branch and sounds spoken.
136 116|They say the Guiding Staff guides people to do good.|the Guiding Staff|Julio explains why it bears that name and attributes the virtue to the legend.
136 120|So it really exists?||Rafael takes the legend almost as proof and asks for confirmation.
136 125|||Julio's qualification keeps the story at the level of legend before the location is given.
136 129|||Rafael wonders about a location once he is convinced enough to ask.
136 134|||The line gives India as hearsay without inventing a more precise location.
136 138|||Rafael leaps back to certainty in his excitement, setting Julio up to repeat the caution.
136 143|||Julio repeats that it is only a legend in a way that undercuts Rafael's certainty.
136 147|Oh. I shouldn't have talked to Clau like that. I'd better apologize.|I'd better apologize.|Rafael realizes how dismissive he was and decides to make amends.
136 152|||The thanks is immediate and comes before Rafael hurries away.
136 157|||Julio calls after Rafael, who is already leaving.
136 161|||The brief observation gives Julio a chance to share his motive privately.
136 165|That ought to cheer Claudio up. When he's gloomy, it spoils the taste of my drink.|cheer Claudio up.;spoils the taste|Julio's concern comes through his joke about the effect on his drinking.
136 168|I'd forgotten all about the legend of the Guiding Staff, though. Is FI really going to look for it?|the Guiding Staff,;going to look for it?|Julio recalls how far the legend had slipped his mind and wonders whether Rafael will actually search.
136 179|Oh well. I'll see if Janus wants a drink.|I'll see if Janus wants a drink.|Julio shrugs off the question and names whom he might invite.
136 189|Here we go again. You and Clau are trying to fool me, aren't you? I'm not falling for it.|fool me, aren't you?|On the alternate branch Rafael is suspicious of both men and refuses to be taken in.
136 193|||Julio's incredulous denial sounds natural after the accusation.
136 196|You just want something to laugh at over drinks. I know what you're up to.|I know what you're up to.|Rafael conveys the idea of being their drinking conversation without literalizing the Japanese snack metaphor.
136 200|||Julio repeats his denial strongly and then gives up on arguing.
136 203|Clau's down about what just happened. I only came over because I thought you could help.|I thought you could help.|Julio states the actual reason he approached Rafael in this branch.
136 206|Oh, th-that's why? I'm sorry, Julio.|I'm sorry, Julio.|Rafael's stammer gives way to a direct apology after he realizes the motive.
136 210|...All right, you understand. Go on and cheer Clau up.|cheer Clau up.|Julio accepts the apology and returns the focus to Claudio.
136 214|||Rafael readily takes the advice after realizing the misunderstanding.
136 219|What a handful. And now all that talk of drinks has made me thirsty.|has made me thirsty.|Julio picks up the suggestion of drinking as the scene's comic payoff.
136 230|I'll see if Janus wants a drink.||Julio moves toward the same invitation as in the other branch.
136 236|||The sly little laugh keeps Julio delighted by the prospect.
137 6|||The maxim gives the fundamental instruction in the familiar form.
137 9|||The short explanation gives both regions and the possibility of a quick profit.
137 13|||Julio sensibly tells beginners to trade locally first and gives his reason.
137 16|||The two direct instructions explain how to use the towns' price differences.
137 19|||The direction of the Lisbon-to-Ceuta trade and both starting goods stay intact.
137 22|||The text connects the starter fleet's ship and hold limits to trade volume.
137 26|||The unit-to-hold rule and the practical buying limit are both explicit.
137 30|||The explanation repeats market share while identifying how a higher share affects quantities.
137 35|||The first caption naturally asks about the unfamiliar term and keeps its original slot.
137 37|||The second caption indicates that the player already understands.
137 44|||Rafael asks specifically how to increase market share as the player would at this point.
137 48|||The condition of unclaimed share and both investment venues are explicit.
137 52|||Julio keeps this step optional at the beginning and encourages actual trading first.
137 60|||The instructions name the visible Finish control and tell the player when to use it.
138 6|||Julio gives the practical need for sailors before discussing how to attract them.
138 10|||The current text gives the action and the impression Julio expects it to create.
138 14|||The reassurance is natural and keeps buying a round optional for the starter fleet.
138 18|||The directions name Recruit Crew exactly and lead to trying it.
138 21|||The example is explicitly for one ship and preserves the Flagship choice.
138 25|Extra sailors mean fewer days at sea. Be careful about hiring more than you need.|more than you need.|Keep the stay-at-sea trade-off and make clear the warning concerns crew beyond the needed count.
138 29|||Julio finishes with a short invitation to use the controls now.
139 5|||The field uses Rafael's name substitution and asks permission before teaching sea routes.
139 10|||The affirmative answer is polite, short and in the correct choice slot.
139 12|||The alternate answer naturally says the player already understands.
139 19|||The route-creation rule clearly requires contracts in neighboring towns or ports.
139 23|||The example uses the player's company substitution and names both current contracts.
139 27|||The two places and the company substitution remain intact in the explanation of why a route exists.
139 30|||The correct job titles, Deck View and Auto Move appear in the same sentence as the route prerequisite.
139 34|||Rafael's exact echo introduces the explanation of Auto Move.
139 39|Once the sea route is connected, just pick a destination. We'll take care of the sailing.|pick a destination.;We'll take care of the sailing.|Julio makes clear what the player does and what the navigators do after the route is connected.
139 42|||The Port action and the destination on the Route Map are clear and use the installed labels.
139 55|||Julio's unfinished caveat leaves room for Rafael's response and the staffing problem.
139 59|||The wordless reaction lets Julio state the missing role.
139 64|||The exact Surveyor role is the missing prerequisite, and the line explains it plainly.
139 67|All that talk, Julio, and you can't even survey?|you can't even survey?|Claudio needles Julio by name without implying kinship.
139 71|Can't be helped. Go to Lisbon and buy a sextant. With that, I can manage.|buy a sextant.|Julio names the location and item and explains why it will help him.
139 74|||The player must equip the sextant on Julio. The wording makes its recipient clear.
139 77|||Rafael's echo supplies the prompt for Julio's equipment advice.
139 82|||The player is told when to inspect the purchased item and where to go now.
139 85|||Rafael stammers his assent as he does when handed other jobs by Julio.
139 102|||Julio's wish of good luck closes the shorter branch without repeating the lesson.
140 5|||The Arms label and both named investment venues are already accurate.
140 9|||Janus names the forts and their role as trading bases on Portugal's Indian Ocean route.
140 12|||The Portuguese construction advantage remains a qualified expectation about relative military investment.
140 16|||Rafael acknowledges the advice and says he'll remember it.
"""

source = checked_text(getsource(template.main), {
    'assert all(speakers[r["actor_ID"]] == r["english"] for r in names["records"] if r["actor_ID"] != 135)\n    assert speakers[135] == "Officiant"':
        'assert all(speakers[r["actor_ID"]] == r["english"] for r in names["records"])',
    'speakers.update({207: "Captain selected by the scene", 208: "Companion selected by the scene",\n                     254: "System panel", None: "Player choice"})':
        'speakers.update({n: f"Companion selected by the scene (role {n - 207})" for n in (208, 209, 214, 215, 220)})\n'
        '    speakers.update({207: "Captain selected by the scene", 254: "System panel", None: "Player choice"})',
    "len(rows) == 255": "len(rows) == 351",
})
scope = vars(template) | globals()
exec(compile(source, __file__ + "::review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()

