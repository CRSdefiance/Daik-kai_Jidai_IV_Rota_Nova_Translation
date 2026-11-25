"""Contextual review of Rafael's item leads, Proof of Conquest clues and ruin encounters."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_followup_encounters_20261121 as parent
from scripts.review_rafael_gerhard_tutorial_20261121 import GATES, TOKEN, logical
from scripts.review_rafael_spain_london_20261121 import plan_progressive


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B101_B120_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source_registered_parent.json", ROOT / "rafael_ruins_review_v3.json"
PRIOR = Path("translations/rafael_B101_B120_contextual_final_review_v1.json")
NAMES = Path("translations/rafael_B101_B120_scoped_names_final_v1.json")
CATALOGUE = Path("translations/editorial_checkpoints/SharedText_20261110_v1/default_actor_names_current_20261120_v1.json")
BLOCKS = ((101, 102, 103, 104, 105, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120), (), (), ())
CONTEXTS = {
    101: "Julio worries about Cristina. Rafael likens her to Athena, reminding Julio about a shield that he wants her to have.",
    102: "Samwell describes Peacock Mail and a little island far southeast of the Cape of Good Hope.",
    103: "Samwell gives a vague western New World lead on the Jaguar God's Vest and says he is done collecting rumors on purpose.",
    104: "Janus recalls a Portuguese wreck and suggests that the rumored Aristarchus Telescope may have washed ashore.",
    105: "Emilio ties his excitement about food in Greece to a rumor about Hestia's Pot, then returns to the question of lunch.",
    108: "Yukihisa asks to see the cursed blade Muramasa that his report helped Rafael find.",
    109: "Margrete has heard about the search for mysterious treasures and recommends a priest nearby.",
    110: "A priest explains how two Map Keys make the map useful, gives Rafael a sword, and asks the party to act justly.",
    111: "Donna describes the pilgrimages to Santiago Cathedral and offers directions while the crew is in Seville.",
    112: "A priest offers pilgrims crosses and misunderstands Rafael's observation that one looks especially old.",
    113: "The selected companion style calls the admiral's attention to the temple. A voice addresses the visitors and encourages debate.",
    114: "The Sphinx asks the riddle about morning, noon, and evening. The menus distinguish whether Rafael knows and which answer he gives.",
    115: "Rafael and Claudio discuss the sect's planned gathering and the balance of light and darkness. The leader addresses a follower and announces an attack.",
    116: "An officiant guarding the ruins says why the temple was built and refuses entry to anyone who does not know the Vedas. The text changes his reception and he entrusts the group with a coin.",
    117: "A villager recognizes visitors of the same faith and entrusts them with an old lamp needed in the search for the Proof.",
    118: "A voice gives the bean-doubling riddle. Two wrong answers form a comic exchange with Claudio, while Rafael supplies the correct answer.",
    119: "The selected companion style announces a dead end. An inscription and three actions concern a jar-shaped tablet. The captain reasons about the turn and a sailor can be injured.",
    120: "Hans vouches for Rafael. A senior monk gives precise directions to the descendants of the clan that guarded the map and warns about the dangers of the voyage and the Proof.",
}

# Empty English keeps installed wording. The phrase field protects words that should read together.
DECISIONS = """
101 5|||The sigh opens a private conversation before Rafael knows what is troubling Julio.
101 9|What's on your mind, Julio?||Rafael notices the sigh and asks with familiar concern.
101 14|||Julio names his granddaughter before Rafael identifies her as Cristina.
101 18|||Rafael recognizes the person Julio means without repeating the relationship.
101 23|I just wonder how she's getting on. Call me a doting father... grandfather, I should say.|a doting father...;I should say.|Julio corrects his own stock expression and gently makes fun of himself.
101 26|Cristina will be fine. She's as strong as if Athena herself had come back to life.|Athena herself|Rafael compares Cristina to Athena reborn while reassuring Julio.
101 31|||Julio echoes the unfamiliar name and gives Rafael a reason to explain it.
101 35|A goddess from Greek myth. The Romans call her Minerva.|call her Minerva.|Name both traditions and give the Roman name that will jog Julio's memory.
101 39|I might've heard of her long ago. I never did know much about the gods.||Julio admits the gap in his knowledge in a familiar rather than scholarly voice.
101 42|...Still, that Miner-whatever sounds familiar.||The half-remembered Roman name leads to the shield and keeps Julio's little joke.
101 45||Cristina will be all right.|The repeated reassurance is intentional. It brings Julio back to why Rafael brought up Athena.
101 49|It means a lot that you trust her so much. But to me, she's my granddaughter. An old man worries, you know.|she's my granddaughter.;you know.|Julio is grateful for Rafael's confidence while admitting that his own concern comes from family.
101 52|||The quiet beat lets Julio's admission land before his recollection interrupts it.
101 57|||Julio jumps from reflection to recognition without explaining too early what he remembers.
101 60|||Rafael's short prompt leaves the explanation with Julio.
101 65|That's it. The Minerva Shield, I think it was called.|Minerva Shield,|Julio reaches for the exact item name and still qualifies the recollection.
101 68|Was it the Mediterranean or the Black Sea? They say there's legendary armor hidden there. I never looked in earnest, but...|the Black Sea?;I never looked in earnest, but...|Julio gives both possible waters and takes care to call the location a rumor.
101 71|Now that you've likened Cristina to Minerva, I want to find it. If it really exists, I'd like her to have it.|If it really exists,|Julio wants the shield for Cristina after hearing the comparison and does not assume the rumor is true.
101 74|||Rafael's quiet use of Julio's name shows he is touched without spelling out his reaction.
101 79|Forgive an old man for rambling. Best forget it. I'd better get back to work.|back to work.|Julio apologizes, downplays the story, and uses work to close a personal moment.
101 83|||Julio's brisk instruction for Rafael follows his own return to duty.
101 87|||Rafael agrees to move on without dismissing Julio's hope.
102 5|||Samwell's casual request for a moment opens this rumor and the one that follows.
102 9|||Rafael's brief reply lets Samwell present the apparently unrelated bird.
102 14|Ever seen a peacock? They're some of the most beautiful birds in the world. Wouldn't you like to see one?|beautiful birds;Wouldn't you like|Samwell is delighted by the bird and wants Rafael to share the curiosity.
102 17|Well, that's out of the blue... Oh, you've heard another rumor, haven't you?|out of the blue...;haven't you?|Rafael moves from surprise to recognition while keeping the quick tag together.
102 22|You guessed it. It's something called Peacock Mail.|Peacock Mail.|Samwell acknowledges the rumor and introduces the exact armor label.
102 25|||Rafael guesses the armor itself is made from feathers so Samwell can correct him.
102 29|Close! You're really close! It's mail with peacock tail feathers fastened to the back.|peacock tail feathers|Samwell's drawn-out excitement becomes a repeated compliment and he describes where the feathers go.
102 33|Doesn't sound like much protection.||Rafael doubts the armor as armor rather than making a claim about its statistics.
102 38|Just the sight of it stops enemies in their tracks, or so they say. That's the main thing it does.|in their tracks,|Samwell describes a rumored effect and avoids turning it into a guaranteed combat rule.
102 42|Hmm... Would that really help? Well, where are we supposed to find it?|Would that really help?|Rafael doubts the usefulness but remains interested in the location.
102 46|I hear it's on a little island way, way, way southeast of the Cape of Good Hope. That's all I found out.|Cape of Good Hope.|Keep the emphatic distance, southeast direction, island and exact named cape.
102 50|||Rafael succinctly points out the location is still too broad to use.
102 54|But I still want to see it! I bet it's unlike anything I've ever seen.|I still want to see it!|Samwell remains curious and imagines the armor without claiming to have seen it.
102 58|All right, I'll keep it in mind. No promises.|keep it in mind.|Rafael promises to remember the lead and keeps expectations modest.
102 63|||Samwell's repeated acknowledgment makes a natural end to the exchange.
103 5|||The same casual opening recalls Samwell's Peacock Mail lead.
103 9|||Rafael again gives Samwell room to make his request.
103 14||Jaguar God's Vest.|Keep the installed title intact as Samwell proposes a search.
103 18|What's that?||Rafael wants to know what the oddly named object is.
103 23|||The vest's supposed inhabitant and the New World location both remain clearly hearsay.
103 27|So you've heard another rumor.||Rafael recognizes Samwell's usual reason for asking to talk.
103 31|Yeah, but this is my last one.||Samwell casually announces he is giving up deliberate rumor hunting.
103 34|||Rafael's echo invites an explanation of why this one is the last.
103 39|Tracking down where these things are is pretty hard. I'm bored with it anyway.|I'm bored with it anyway.|Samwell gives both the labor of investigating and his lost interest.
103 42|I get bored fast. I like animals, but if I can't cook 'em, what's the fun? I'll pass along any rumors I happen to hear.|if I can't cook 'em,;what's the fun?|Keep the food joke, the short attention span and the promise to pass on incidental leads.
103 45|R-right. About the vest, then. Any idea where in the New World it might be?|where in the New World|Rafael recovers from the joke and asks for a more useful location.
103 50|Hmm... I'd guess the western side of the New World.|the western side|Keep the western direction as Samwell's guess and name the landmass he is talking about.
103 53|||Rafael's two short sentences express why the large area is not a useful search location.
103 57|Sorry, that's all I could find out. Just keep it in mind, okay?|keep it in mind, okay?|Samwell admits the limit of the lead and gives Rafael back his own earlier advice.
103 60|||The small laugh and agreement accept the tip without a promise to search right away.
104 5|||The question preserves the Portuguese fleet, approximate twenty years and the local waters.
104 9|||Rafael plainly says he had not heard of the wreck.
104 14|The admiral had a telescope that could see for miles, they say. You could even see bumps and hollows on the moon.|bumps and hollows;on the moon.|Janus gives the rumored range and the more extraordinary example as part of the tale.
104 17|Really? That's incredible!||Rafael reacts with excitement before Janus qualifies the story.
104 22|They say Aristarchus made it, the brilliant astronomer from the Hellenistic age.|the Hellenistic age.|The attribution is only reports, and Aristarchus's historical period is still explicit.
104 26|||Rafael's small pause leaves room for skepticism instead of treating the claim as established fact.
104 31|||Janus clearly identifies the lens-polishing precision he doubts for that time.
104 35|I can't tell you if it's true. In any case, they called it the Aristarchus Telescope, after him.|Aristarchus Telescope,|Keep the named item and the reason for the name despite doubt about its provenance.
104 38|What about it?||Rafael prompts Janus to connect the story to their own location.
104 43|Given the currents, I think there's a good chance the telescope washed ashore somewhere around here.|washed ashore|Janus bases his tentative search advice on the currents.
104 46|I see! Sounds like it's worth looking for.|worth looking for.|Rafael responds to the reasoning before agreeing the lead merits a search.
105 5|We're in port! Come on, let's get something to eat!|something to eat!|Emilio is eager to get off the ship for food, and his request is echoed later.
105 8|You say that every time we dock, Emilio. 'Come on, let's get something to eat!'|something to eat!'|Rafael names Emilio and repeats the same food request in a friendly tease.
105 13|||Emilio keeps both the importance of eating and the hint that he is actually looking for something.
105 17|||The plain question sets up Emilio's simple answer.
105 22|||The exclamation gives Emilio's ambitious answer without adding a particular dish.
105 26|...How will you know it's the best food in the world?|best food in the world?|Rafael pauses before pointing out the practical problem with choosing a world's best.
105 31|Oh, I'll know! The best food in the world is cooked in Hestia's Pot.|Hestia's Pot.|Emilio confidently explains that the pot is how he knows, using its established name.
105 34|||Rafael's hesitation on the unfamiliar item's name leaves Emilio to explain it.
105 39|The goddess of the hearth had it made, or so they say. I hear it's far across the sea, south of Greece.|goddess of the hearth;south of Greece.|Keep Hestia's commission and the clue's far-off direction as heard, preserving the complete phrases.
105 42|That's why I can't wait to eat around Greece. Now, can we go? Come on, let's get something to eat!|Come on,;something to eat!|Emilio's reasons lead right back to the same impatient request.
108 5|Admiral, I hear you've finally found the cursed blade Muramasa. Might I see it for myself?|cursed blade Muramasa.|Yukihisa's courteous request names the object and asks to see it firsthand.
108 8|Of course. We found it thanks to your tip, Yukihisa.|thanks to your tip,|Rafael gives credit for the prior report without making a formal speech of it.
108 13||cursed blade Muramasa...|Yukihisa's faltering recognition conveys awe, with the full epithet held together.
108 17|Hmm... That strange glow almost draws you in, doesn't it?|draws you in, doesn't it?|The glow is eerie and seems to pull him toward it, without an added supernatural action.
108 21|I'm glad I had the chance to see it.||Yukihisa conveys the courteous gratitude of the short closing expression.
109 7|Say, I hear you're looking for mysterious treasures hidden all over the world. Is that right?|Is that right?|Margrete asks about what she overheard and lets the crew confirm it.
109 10|The priest at the church nearby knows all sorts of things. He might have something useful to tell you.|something useful|Margrete offers a person to ask and leaves any useful knowledge as a possibility.
110 5|||The priest opens with the exact established name of the Proof of Conquest.
110 8|You've heard of it?||Rafael is surprised this priest already knows their goal.
110 13|I can tell you this. The map to the Proof works only after you join two Map Keys.|The map to the Proof;two Map Keys.|The necessary combination and the exact number remain explicit, and the term matches the other references in this exchange.
110 17|Neither key means anything on its own.||The priest reinforces that a single key will not give them a usable map.
110 20|You may already know this. A Map Key might be hidden in ruins or in the hands of someone you'd never expect.|a Map Key|Two different sources for keys remain possibilities and no specific person is invented.
110 23|||The captain takes in the information in silence before the priest offers the sword.
110 27|||The concise imperative accompanies a real gift of a sword.
110 34|Face the trials before you, and help those in need.|help those in need.|The two injunctions remain connected in the priest's blessing and advice.
110 37|Don't let greed rule you. Give to those who have little. Put an end to the causes of strife and bring peace.|who have little.;bring peace.|Preserve all the priest's moral injunctions, including addressing the cause of conflict.
110 41|||The traditional short blessing sends the travelers on their way.
111 7||Santiago Cathedral?|Donna's interruption leads directly to a question naming the cathedral.
111 11|||The captain's puzzled response lets Donna supply the reason for the question.
111 15|||The current line covers both the long pilgrimage tradition and its reach across Europe.
111 19|As long as you're in Seville, why not go? I'll show you the way.|I'll show you the way.|Donna suggests a visit while they are in town and offers directions herself.
112 5|Are you pilgrims? Please take these crosses as a keepsake of your visit.|a keepsake|The priest addresses the group and offers multiple crosses as a remembrance.
112 9|||Rafael thanks him and then spots the unusual cross mid-thought.
112 14|||The priest's unembellished question prompts Rafael to explain what caught his eye.
112 18|This one looks very old.||Rafael points out the single noticeably old cross without appraising its worth.
112 22|Don't talk that way. A sacred cross is sacred, old or new.|old or new.|The priest takes the observation as irreverence and stresses that age is immaterial.
112 26|||Rafael protests the misunderstanding softly without disputing the priest's belief.
112 30|As long as you understand. In the name of the Father, and of the Son, and of the Holy Spirit... Amen.|In the name of the Father,;and of the Son,;and of the Holy Spirit...|The priest ends the misunderstanding and uses the familiar full Trinitarian formula.
113 15|Admiral, would you look at this?||The first physical companion line is courteous and stays shared by its two original style slots.
113 17|||The two shared middle slots use the plain exclamation to get the admiral's attention.
113 19|Hey, Admiral, take a look at this!||The more casual companion style calls out briskly without changing what was found.
113 21|Look here, Admiral!||The familiar elder register makes an urgent call with natural word order.
113 23|Admiraaal, look!||The childlike variant stretches the call to the admiral to reflect the original delivery.
113 25|||The final variant stays formal and uses the same attention-getting act.
113 29|You who have entered this temple!||The disembodied address names the visitor through an appropriately formal invocation.
113 33|||The punctuation marks the captain's wordless surprise without giving the voice a new body.
113 37|I lend you my power. Speak freely and debate well.|debate well.|The temple voice offers its own power and urges the visitors to deliberate.
114 5|Whoa... Look at that!||Rafael's spontaneous awe sets up his shock when the Sphinx answers.
114 11|Answer my question.||The speaker demands an answer to a question without revealing the riddle early.
114 15|||Rafael's startled stammer keeps his disbelief that the figure just spoke.
114 24|What animal walks on four legs in the morning, two at noon, and three in the evening?|four legs;two at noon,;three in the evening?|Keep the animal and all three times and counts explicit so the answer follows from the familiar riddle.
114 28|||Rafael's brief perplexity comes before Claudio's literal search for an animal.
114 33|I-I've never heard of any animal like that!|like that!|Claudio stammers and clearly believes the question concerns an actual animal.
114 36|Answer my question!||Repeat the Sphinx's earlier wording with greater force.
114 40|||Claudio's hesitant question passes the decision to Rafael.
114 47|||This option says Rafael knows and leads to the original second menu.
114 49|||This slot admits that Rafael does not know.
114 51|||The third option rejects the premise rather than simply admitting ignorance.
114 63|||The Sphinx's abrupt repeated banishment works in its formal riddle voice.
114 67|||The captain's cry follows the first failed answer without describing an unspoken cause.
114 79|||The same wording marks the same banishment when the other opening answer fails.
114 83|||Match the startled cry on the other failed opening answer.
114 96|Then name the animal.||The Sphinx accepts the first response provisionally and demands the actual answer.
114 103|||The compact caption represents the correct human answer.
114 105|||The second option identifies the Sphinx itself explicitly.
114 107|||The third option remains a distinct unspecified guess.
114 119|||Use the same short banishment if the player guesses the Sphinx.
114 123|||Keep the captain's matching startled cry in this failed identification branch.
114 135|||The final unrecognized guess receives the same banishment.
114 139|||The last failure cry matches the other unsuccessful paths.
114 152|I've got it! The day stands for a whole lifetime.|a whole lifetime.|Rafael draws out the metaphor that makes the riddle solvable.
114 156|||Claudio's bafflement invites Rafael to explain the morning stage.
114 160|Morning means you've just been born. Babies crawl on all fours.|on all fours.|Rafael explains the four legs with the familiar description of crawling.
114 164|Oh, right! Then the baby grows up and walks on two legs!|on two legs!|Claudio catches on and supplies the midpoint of the explanation.
114 167|Evening means old age. An old person walks with a cane, right? That's the third leg.|with a cane, right?;the third leg.|Rafael retains the cane and connects it plainly to the last number.
114 171|||Claudio reaches the conclusion without taking Rafael's final answer from him.
114 175|||Rafael names humans and includes himself and Claudio, completing the previous sentence.
114 185|||The Sphinx recognizes the correct answer and presents a reward without the dialogue inventing what the object is.
115 9|Those ruins must be ancient.||Claudio opens with an impression from what he and Rafael just saw.
115 13|Who were those people, anyway? Offering up a living sacrifice like that...|a living sacrifice|Rafael is disturbed by the sacrifice and wonders about the people they encountered.
115 17|Those people are out of their minds! But... they said they'd meet here again, right?|meet here again, right?|Claudio calls out the behavior and recalls their specific plans to gather here again.
115 21|||Rafael uses a short question to turn from what happened to what might happen next.
115 25|Beats me. They said something about 'the night before the day of revelation.' When's that supposed to be?|the day of revelation.';supposed to be?|The timing clue still points to the preceding night, and Claudio asks when it falls.
115 28|Remember the incantation? 'When light and darkness are evenly matched.' Could that be the day they meant?|'When light and darkness;are evenly matched.'|The balance of light and darkness stays exact, and Rafael offers the connection as a guess.
115 33|Huh? That doesn't tell me a thing.||Claudio admits the clue still means nothing to him.
115 36|We need a plan. We have to stop them from making any more sacrifices!|stop them|Rafael wants to act regardless of his uncertainty about the riddle's timing.
115 44|||The drawn-out sound from the leader marks the cut from the crew to the sect.
115 48|||Keep the follower's answering chant as a separate reaction.
115 52||Civilization Research Society,;conquer the world!|The leader gives the group's full established name and grandiose prediction.
115 56|We are the chosen ones! We shall dig up the treasure described here and rule over those godless fools!|the treasure described here;godless fools!|The leader promises to unearth the specified treasure and uses contemptuous language about the people the sect means to rule.
115 59|||The follower answers the leader's promise with another enthusiastic sound.
115 63|||The leader orders the first attack, names the village as the target and gives the insult as his motive.
115 67|||The last chant affirms the leader's command without naming a new actor.
116 5|Huh? There's someone here!||Claudio notices a person where the party expected only ruins.
116 9|||The surprised punctuation is the guardian's corresponding first reaction.
116 13|I never expected to see anyone here...|anyone here...|The guardian is surprised the party reached him and pauses before answering.
116 16|||Rafael hesitates and asks the stranger to identify himself.
116 21|||The guardian plainly says what he is doing without naming an office or rank.
116 24|||Rafael naturally asks about the place after learning the stranger guards it.
116 29|This was built as a temple for Suryavarman II. He meant to unite with Vishnu and become a god.|Suryavarman II.;with Vishnu|The guardian attributes the building and gives the stated religious purpose.
116 32|Surya...? Vish...? Ah, none of this makes any sense to me!||Claudio tries the unfamiliar names before admitting he is lost.
116 41|I cannot let anyone approach who doesn't know the Vedas. Now go.|know the Vedas.|Knowledge of the texts is his stated condition, followed by an order to leave.
116 47|How do we get him to let us through? And what are the Vedas, anyway?|what are the Vedas, anyway?|Rafael asks how to earn the man's approval and admits that he does not know the key term.
116 60|I think they're the myths that laid the foundations of Hinduism, the faith practiced in India and the surrounding lands.|I think;the faith practiced in India|Arcadius explains his understanding tentatively as a character in the scene.
116 76|Vishnu is a Hindu god, isn't he?|a Hindu god, isn't he?|Arcadius seeks confirmation of the god's identity and his tag should stay whole.
116 79|Ah, you know your subject.||The guardian is impressed that the visitor understands the reference.
116 86|||The guardian sees something unexpected and asks what it is.
116 89|The very first text of the Vedas! W-who are you people?|the Vedas!|The guardian recognizes the actual text and is shaken enough to stammer.
116 92|Ah... Now I understand. You've finally come. And you're still so young...|You're still so young...|The guardian connects the object with someone expected and marvels at the captain's youth.
116 96|||Rafael's puzzled sound shows he does not share the guardian's understanding.
116 101|Very well. I'll entrust this to you.|entrust this to you.|The guardian's formal assent leads into his entrusting something to the party.
116 107|||Rafael recognizes only the age and physical form of the coin and asks what it means.
116 112|My part is done. It's up to you to figure out the rest. Now go.|figure out the rest.|The guardian gives them responsibility for solving the rest and dismisses them.
116 118|||Rafael stays uncertain about the final instruction.
117 6|Who are you? Wait, could it be...?||The villager's suspicion turns to the beginning of recognition.
117 9|Oh! It's been so long since we met someone who shares our faith!|shares our faith!|The villager welcomes fellow believers and stresses how unusual the meeting is.
117 12|We fled Muslim rule and have lived quietly here ever since, keeping our faith.|keeping our faith.|The villager gives the community's history in its own voice and retains the motive for living quietly.
117 16|Forgive the sudden question, but do you know of a treasure that goes to whoever conquers the seven seas?|conquers the seven seas?|Rafael politely asks about the specific fabled reward and its condition.
117 21|What! You're looking for the Proof of Conquest? God must have brought you here!|Proof of Conquest?|The villager gives the full name at first mention and interprets the meeting as divine guidance.
117 25|You... know something about it?||Rafael is surprised by the recognition and asks the villager to explain.
117 29|Do I ever...||The villager's short answer leads straight into evidence that the story is well known there.
117 33|This lamp has been in our village for generations. They say anyone who seeks the Proof will need it. I'm entrusting it to you.|will need it.|The villager links the heirloom to the search and explicitly gives it into the party's care.
117 38|Please... Do what you can to keep the Proof out of the Ottoman Empire's hands.|the Ottoman Empire's hands.|The villager asks the party for help and names the historical power exactly.
117 42|I understand. We'll find it, I promise.|We'll find it, I promise.|Rafael assures the villager he intends to find the Proof without claiming it already.
118 7|Visitor to the Colosseum, answer my question!|answer my question!|The voice addresses their present location and asks them to answer.
118 10|||Rafael repeats the surprising demand as a short question.
118 15|||The short announcement introduces the riddle before the multi-panel explanation.
118 19|I have a strange bean. In one second it splits in two, then there are four at two seconds and eight at three seconds.|In one second;four at two seconds;and eight at three seconds.|Keep the starting bean and the exact timed sequence of doubling.
118 23|Start with one bean and the bag is full after 60 seconds. If you start with two beans, how many seconds will it take?|after 60 seconds.;two beans,|Give both initial conditions explicitly and ask for elapsed time in seconds.
118 26|||The imperative ends the explanation and leads directly into the original options.
118 33|||One second remains the first original wrong answer with the correct unit.
118 35|||Thirty seconds remains the tempting half-time answer in the second slot.
118 37|||Fifty-nine seconds remains the correct answer in the third slot.
118 46|||Claudio suddenly believes he knows the first answer.
118 50|Really? I can always count on you when it matters, Clau!|when it matters, Clau!|Rafael's confidence in Clau makes the incorrect answer that follows funny.
118 55|You bet! One second. How's that?|One second.|Claudio proposes the exact one-second answer with unearned confidence.
118 58|Yeah! That's what I was thinking, too!|what I was thinking, too!|Rafael echoes the wrong answer enthusiastically before the rebuke.
118 62|||The voice calls the failed guess foolish in a single abrupt word.
118 66|||Claudio's brief confusion follows the verdict on his confident answer.
118 78|||Use the same excited realization on the other wrong-answer path.
118 82|Really? I can always count on you when it matters, Clau!|when it matters, Clau!|Keep Rafael's identical praise on the second wrong-answer path.
118 87|Sure! Half the time. Thirty seconds! How's that?|Thirty seconds!|Claudio gives the exact second wrong answer and his half-time reasoning.
118 90|Yeah! That's what I was thinking, too!|what I was thinking, too!|The matching enthusiastic agreement preserves the joke on both mistaken paths.
118 94|||The second wrong answer earns the same curt rebuke.
118 98|||Keep Claudio's bewildered response to the second failed guess.
118 111|||Rafael claims the answer himself on the correct path.
118 116|Oh yeah? What's the answer?||Claudio wants to hear Rafael's answer and no longer supplies the guess.
118 120|It's 59 seconds!||Rafael gives the correct time directly and keeps the result plainly audible.
118 125|Well done! You have wisdom and courage. Accept this!|wisdom and courage.|The voice recognizes both virtues and tells them to accept the reward.
119 15|||The first style is matter-of-fact and respectfully addresses the admiral.
119 17|Admiral, the passage ends here.||Give the second polite style its own wording while retaining the observation.
119 19|||The third style notices the dead end with casual surprise and does not use a title.
119 21|Looks like a dead end, Admiral.||The fourth style speaks conversationally and keeps its direct address.
119 23|Whoa. Dead end.||This style reacts informally and bluntly without adding an address.
119 25|A dead end, Admiral, by the look of it.||This elder style sounds deliberate while giving the same information.
119 27|Admiraaal, it's a dead end!||The youthful style stretches its call to the admiral consistently with the temple discovery.
119 29|||The final variant's quiet, formal surprise already sounds distinct.
119 33|A stone tablet shaped like a jar is embedded here.|stone tablet;shaped like a jar;is embedded here.|The panel describes the shape and embedding without saying the object is an actual jar.
119 36|Traveler, pour from the sacred jar with your left hand.|the sacred jar;with your left hand.|The inscription preserves the exact hand used for the action that determines the direction.
119 39|The jar... with my left hand?|with my left hand?|The captain repeats both parts of the clue while working out what it means.
119 46|||The first option remains pushing the tablet.
119 48|Turn it to the right.||State the direction explicitly using the original right-turn slot.
119 50|Turn it to the left.||Mirror the other caption while keeping the original left-turn slot.
119 60|||The captain's abrupt punctuation preserves the immediate surprise after the action.
119 66|If I pour with my left hand, the jar ought to tilt to the right...|with my left hand,;to the right...|Keep the rule linking the specified hand to the actual rightward tilt.
119 70|||The next brief reaction accompanies the mechanism rather than explaining it in speech.
119 82|||A separate startled beat signals the danger before Rafael yells to run.
119 89|||The direct command is urgent and readable as the party reacts.
119 94|||The sailor's cry remains separate from the explicit injury notification.
119 101|||The system notice says a sailor was injured and leaves the exact individual unspecified.
120 6|||The monk's polite opening gives no hint yet how much he knows.
120 10|Hm? Can I help you?||Rafael turns his attention to the monk and invites him to speak.
120 14|||The monk names the Proof of Conquest and asks whether Rafael is seeking it.
120 17|||Rafael is immediately surprised that a stranger knows his goal.
120 21|You seem to know something about the map to the Proof.|the map to the Proof.|Hans infers the monk knows about the map from the way he addresses Rafael.
120 24|Indeed. But that is something I cannot tell just anyone.|tell just anyone.|The monk confirms without yielding the information to strangers.
120 28|You fear what someone with evil intentions might do with it?|with evil intentions|Hans asks whether the problem is what a malicious person might do with the information.
120 32|...Yes.||The monk quietly confirms Hans's reading of the situation.
120 36|You can put your mind at ease. I've studied the Proof for many years.|for many years.|Hans offers reassurance based on the length of his own research.
120 40|I am certain this young man has what it takes to rule the seas.|to rule the seas.|Hans firmly vouches for Rafael's potential without claiming he has already earned the Proof.
120 44|||The monk takes a moment to weigh Hans's assurance.
120 48|Please. If you know something, tell us.|tell us.|Rafael asks directly while acknowledging that the monk can decline.
120 52|...Very well.||The monk deliberates before consenting to share the clue.
120 56|Long ago, a clan guarded the map in China. They say the ruler pursued them, so they fled far, far to the northeast.|far, far to the northeast.|Keep the Chinese origin, pursuit by the ruler of the time and repeated direction.
120 59|||Rafael echoes the long journey's direction so the monk can narrow it down.
120 64|They reached a small village in the far north, near an icy sea. Their descendants should still be living quietly there.|near an icy sea.;living quietly there.|The monk gives both geographic markers and treats the descendants' presence as likely.
120 67|||Rafael sums up the village clue and anchors the direction in relation to China.
120 72|Look near the base of the vast peninsula, at the foot of a tall peak on its eastern coast.|the vast peninsula,;its eastern coast.|Keep the base of the peninsula and the east-coast peak, and make it clear where to look.
120 75|An ordinary ship may struggle to reach a place that far away. Go unprepared, and it'll cost you your lives.|cost you your lives.|The monk warns about the distance and the danger of treating the expedition casually.
120 78|||Rafael gulps privately instead of interrupting the monk's warning.
120 83|Listen well. Never hand the Proof to anyone with evil intentions. Don't let greed get the better of you, either.|with evil intentions.;get the better of you,|The warning applies to both outsiders and Rafael's own conduct.
120 86|I will. Thank you for telling us.|Thank you for telling us.|Rafael accepts the responsibility and thanks the monk for the information.
"""


def main():
    assert not OUTPUT.exists()
    packet, prior, release, names, catalogue = map(base.load, (SOURCE, PRIOR, parent.RELEASE, NAMES, CATALOGUE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    earlier = {(row["block"], row["source_reference"]["offset"]): row for row in prior["records"]}
    speakers = {r["actor_ID"]: r["progressive_nameplate"] for r in catalogue["source_and_current_default_name_fields"]}
    assert all(speakers[r["actor_ID"]] == r["english"] for r in names["records"] if r["actor_ID"] != 135)
    assert speakers[135] == "Officiant"
    speakers.update({207: "Captain selected by the scene", 208: "Companion selected by the scene",
                     254: "System panel", None: "Player choice"})
    decisions = {}
    for line in DECISIONS.strip().splitlines():
        key, replacement, protected, explanation = line.split("|")
        key = tuple(map(int, key.split()))
        assert key not in decisions
        decisions[key] = replacement, protected.split(";") if protected else [], explanation
    rows, plans, failures = [], {}, []
    for group in packet["groups"]:
        n, path = group["block"], group["file_path"]
        for item in group["records"]:
            selector, number, word = [item[k] for k in ("selector", "source_record_index", "native_command_word")]
            old = earlier.pop((n, item["source_offset"]))
            assert item["Japanese"] == old["source_Japanese"] and selector == old.get("source_selector")
            assert all(old["review"].values())
            replacement, phrases, note = decisions.pop((n, number))
            current = logical(item["current_English"])
            english = replacement or current
            assert english.isascii() and logical(english) == english, (n, number)
            assert all(p.casefold() in english.casefold() for p in phrases), (n, number, phrases)
            assert TOKEN.findall(item["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english), (n, number)
            prefix = f"{selector:02x}" if word == 0x4000 else ""
            refs = {side: dict(file_path=path, block=n, offset=item[f"{side}_offset"],
                               command_offset=item[f"{side}_command_offset"],
                               archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                               exact_hex=prefix + item[f"{side}_body_hex"])
                    for side in ("source", "current")}
            assert refs["source"]["exact_hex"] == old["source_hex"]
            kind = "typed-choice-label" if selector is None else "system-FE" if selector == 254 else "progressive"
            assert kind == old["kind"]
            if word == 0x4100:
                assert item["slots"] == old["source_style_indices"]
            different = current != english
            row = dict(id=old["id"], file_path=path, route=0, block=n, source_record_index=number, kind=kind,
                       native_command_word=word, native_slots=item["slots"], source_selector=selector,
                       source_reference=refs["source"], current_reference=refs["current"],
                       source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                       Japanese=item["Japanese"], previous_English=current, english=english, speaker=speakers[selector],
                       context=CONTEXTS[n], source_meaning=old["source_meaning"], localization_note=note,
                       protected_phrases=phrases, decision="revision" if different or phrases else "retention",
                       finding="wording" if different else "wrap" if phrases else "retention",
                       review=dict.fromkeys(GATES, True) | {"formatting": False})
            if row["decision"] == "revision" and kind == "progressive":
                jp, en = (bytes.fromhex(item[f"{side}_body_hex"]) for side in ("source", "current"))
                try:
                    body, plan = plan_progressive(row, selector, en, jp)
                    if body.rstrip(b" ") == en.rstrip(b" "):
                        assert not different
                        row.update(decision="retention", finding="retention")
                    else:
                        plans[row["id"]] = plan
                except (ValueError, AssertionError) as error:
                    failures.append((n, number, english, phrases, str(error)))
            rows.append(row)
    assert len(rows) == 255 and not decisions and not earlier
    assert not failures, failures
    findings = dict(Counter(row["finding"] for row in rows))
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), status="Contextual review complete. Native display and release verification pending.",
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        earlier_contextual_reviews={str(PRIOR): base.digest(PRIOR)}, scoped_name_precedent={str(NAMES): base.digest(NAMES)},
        records=rows, plans=plans, findings=findings, new_editorial_credit=0))
    print(f"Reviewed {len(rows)} records across {len(BLOCKS[0])} encounters. {findings}.")


if __name__ == "__main__":
    main()

