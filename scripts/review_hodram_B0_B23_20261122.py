"""Review Hodram's opening encounters, rescue, elegy, and Aziza's mutiny."""

from inspect import getsource
from types import SimpleNamespace

from scripts import pair_hodram_next_20261122 as intake
from scripts import review_hodram_opening_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base = intake.base
ROOT = intake.pairing.ROOT.with_name("hodram_B0_B23_followup_20261122")
paired = SimpleNamespace(PACKET=ROOT / "paired_source_registered_candidate.json", CARRY=ROOT / "prior_contextual_decisions.json")
OUTPUT = ROOT / "contextual_decisions_v4.json"
CONTEXTS = {
    0: "Gerhard identifies the Indian traditions in a book. Hodram tests what they might imply about Sera's homeland and then doubts his own hypothesis.",
    1: "Yukihisa identifies Muramasa and is drawn to its ominous light.",
    2: "Gerhard recognizes a recovered possession from the dull sheen he remembers.",
    3: "Aziza rallies Snake, Angel, Dandy, and the crew against Hodram's fleet. Hodram hears Gerhard's observation and orders battle preparations.",
    4: "Aziza challenges Hodram again. Keep the two approach branches and the crew's answer distinct.",
    5: "Hodram stops Julian's ship and accuses him of betraying his homeland. Julian's drunken contempt stays his own.",
    6: "Hodram confronts Plett about murder. Plett attacks his self-righteousness and Hodram decides to close in.",
    7: "Gerhard demands surrender. Ramusio asks for evidence and threatens the patrol when Hodram refuses to back down.",
    8: "Hodram confronts Portunto about profiting from smuggling. Portunto resents being lectured by him.",
    9: "Hodram acknowledges Hernan as a capable opponent. Hernan boasts that ships usually flee from him, then welcomes the challenge.",
    10: "Hodram delivers the royal order against Iscal, who recognizes the admiral and accepts the fight.",
    11: "Clive's drawn-out laughter and threats frame Gerhard's recognition and Hodram's assessment.",
    12: "Hayreddin boasts after the fight, tells Hodram to prove himself in the Caribbean, and warns him away from the southern Mediterranean.",
    15: "Hodram orders captives freed. The crew finds Sera on a grounded ship. She tries to defend herself before Hodram offers her the choice to leave and a weapon for protection.",
    16: "The crew wins the battle. Manuel mourns those lost and recites a three-panel poem before reflecting on what the sea takes in.",
    17: "Aziza's crew mutinies after another loss. Hodram and his people intervene, buy her release, learn what her father's sword meant to her, and offer her a place aboard.",
    18: "Aziza withdraws in two branches. The longer departure identifies her by name, and Hodram acknowledges it.",
    19: "Hodram withdraws despite Aziza's taunts. A separate outcome shows Gerhard urging withdrawal and Hodram acknowledging her skill.",
    20: "Hodram orders Julian taken to Sao Jorge. Julian curses and his last word is cut off.",
    21: "Hodram orders Plett bound and taken to Hangzhou. Plett cries out and stammers a claim of remorse.",
    22: "Hodram remarks on the Basra guild's difficulty handling Ramusio. Ramusio defends his conduct and Gerhard responds with disgust.",
    23: "Portunto mourns his cargo. Hodram identifies it as stolen and tells him to worry about his own fate in Calicut.",
}
DECISIONS = {
    0: """
6|||Gerhard tentatively identifies the book as a written account of old Indian traditions.
9|||Hodram considers an Indian kingdom as a possibility. The installed wrap already keeps both Sera's homeland and the complete question phrase intact.
12|||The distance from Ottoman territory is the reason he immediately doubts that possibility.
""",
    1: """
6|||Yukihisa repeats himself in wonder as he identifies Muramasa. The approved short name stays.
10|||The eerie light draws him in. The measured delivery fits his reaction to the blade.
""",
    2: """
6|Yes, that's it! It's got the same dull gleam it had when I gave it up.|the same dull gleam;when I gave it up.|Gerhard recognizes the same muted sheen from when he parted with the object.
10|||His astonishment that nobody else picked it up follows the recognition. Preserve the unfinished thought.
""",
    3: """
6|Look there! That's FO. They're the ones muscling in on our waters!|muscling in on our waters!|Aziza identifies the fleet through the original company substitution and accuses it of encroaching.
9|Yeah!|Yeah!|This is a collective cheer after Aziza identifies the fleet. Formal assent blunted the reaction.
13||battle stations!;Snake, take command!|The existing wording gives the battle order and tells Snake to take command. Put each complete order on its own row.
16|||Snake acknowledges the order briefly in the middle of the flurry of commands.
20|Angel! Take us off their starboard quarter!|their starboard quarter!|Aziza orders the ship to the enemy's right rear. Use the nautical term for that relative position.
23|Oh, yeah! You got it, boss!|You got it, boss!|Angel answers with exuberant assent. Aziza plainly directs him as captain.
26|||Aziza calls Dandy by his established nickname and checks whether the guns are ready.
29|||Dandy's clipped readiness report distinguishes him from Angel's exuberance.
33|Heh... Now this gets my blood up. Listen up, you lot!|gets my blood up.;Listen up, you lot!|Aziza relishes the coming fight and sharply calls for the crew's attention.
36|Time to settle who deserves to rule these waters. Me or FO!|rule these waters.|Aziza says the contest will decide whether she or the named fleet deserves to rule these waters.
39|Yeah!!!|Yeah!!!|The louder collective cheer answers Aziza's challenge before the scene cuts to Hodram.
43|||Hodram identifies the sailors as pirates with a single dry word.
51|She's still a pirate. Ready for battle.|She's still a pirate.;Ready for battle.|Hodram dismisses the significance of Gerhard's observation and orders preparations.
55|||Gerhard's restrained reply returns to carrying out the order.
""",
    4: """
43|Finally found you! This time we'll settle it!|This time we'll settle it!|Aziza has finally found her quarry and insists this encounter will decide matters.
46|Yeah!|Yeah!|The crew cheers in response to her challenge.
52|Back for more, are you, FO? This time I'll send you to the bottom!|Back for more, are you,;send you to the bottom!|Keep the accusation that they never learn, the address to the fleet, and the promise to sink them.
""",
    5: """
8|||The hiccup and contemptuous question carry Julian's drunken defiance.
11|You sold out your own country for gold. I won't let that go unpunished.|your own country for gold.;go unpunished.|Hodram condemns Julian for betraying his homeland for money.
""",
    6: """
5|Plett Perrault. You look like you've committed plenty of crimes. I can't leave a murderer at large...|a murderer at large...|Hodram recognizes Plett and says he cannot leave a murderer at large. His first remark is about what Plett looks like.
8|Who do you think you are? Don't talk down to me. You've never broken a law in your life, have you?|Who do you think you are?;Don't talk down to me.;in your life, have you?|Plett calls Hodram self-righteous and challenges him to deny having ever broken the law.
11|So crime really is all you're good at. No reason to hold back, then. Here we come!|all you're good at.;No reason to hold back,|Hodram concludes Plett is only good at wrongdoing and decides to advance without restraint.
""",
    7: """
5|Jean Ramusio! Cease your illegal trading and surrender at once!|illegal trading;surrender at once!|Gerhard gives a formal order to stop the illicit trading immediately and surrender.
8|||Ramusio feigns surprise and mocks the demand by asking for proof.
11|You're all the proof I need. You reek of dirty dealings. I can shake the truth out of you if I have to.|all the proof I need.;dirty dealings.|Hodram treats Ramusio himself as evidence and threatens to use force. Keep the forceful metaphor without giving details.
14|||Ramusio's mocking question and threat are natural after Hodram refuses to back down.
""",
    8: """
6|Jacob Portunto. Smuggling's treated you well. That ends today.|Smuggling's treated you well.;That ends today.|Hodram names the crime and says the benefit Portunto got from it ends now.
9|||Portunto is outraged that this particular opponent would presume to lecture him.
""",
    9: """
5|Hernan Berio. I'll take you on. A worthy opponent makes a nice change.|I'll take you on.;A worthy opponent|Hodram welcomes testing himself against a skilled opponent for a change.
9|Been a while since anyone came at me. Now they flee at full sail the second they see me. Being this good has its drawbacks.|at full sail;this good has its drawbacks.|Hernan boasts that ships flee at full speed on sight and jokes that his strength is a nuisance.
12|||Hernan has been bored too. The short invitation answers Hodram's challenge.
""",
    10: """
7|Iscal Yasar? I'm here on the king's orders to bring you down. Prepare yourself.|the king's orders;Prepare yourself.|Hodram makes clear that the king sent him against Iscal and tells him to be ready.
11|Admiral FA... Now there's a worthy opponent. Come on!|Admiral FA...;a worthy opponent.|Iscal recognizes the admiral through the original surname substitution and welcomes the matchup.
""",
    11: """
6|||Clive's stretched vowels and shrill laughter distinguish him from the other captains.
9|||Gerhard recognizes that the opponent they were waiting for has finally appeared.
13|||Hodram pauses and agrees that the man is dangerous. The dry line works against Clive's shouting.
17||I'll sink you!|Keep the shrill laugh and all three threats while the formatter keeps each repetition intact.
""",
    12: """
5|||Hayreddin laughs, asks whether the defeat taught a lesson, and says he is letting Hodram go this time.
8|||He makes a name in the Caribbean a prerequisite to challenging him again. The boast is short and direct.
12|Show your face again in the southern Mediterranean and I'll chase you to the ends of the earth and crush you!|the southern Mediterranean;to the ends of the earth|Hayreddin threatens to chase Hodram to the ends of the earth and crush him if he returns to the southern Mediterranean. Keep both geographic phrases together.
""",
    15: """
11|||Hodram gives an unqualified order to release all the prisoners.
17|||The brief curse responds to the reversal before Gerhard reports what the other ships are doing.
21|They're breaking off. Looks like they won't press the chase. Hm?|won't press the chase.|Gerhard reports a quick withdrawal without a sustained pursuit, then notices something else.
25|||Gerhard reports one grounded ship, without claiming it is abandoned.
29|||Hodram guesses the ship was abandoned and orders the crew to look inside.
35|||Gerhard trails off in getting Hodram's attention. The next turn supplies his concern.
39|||Hodram asks what's wrong with a single blunt question.
43|We found someone who seems out of place on this ship.|out of place on this ship.|Gerhard says the person seems out of place aboard, leaving who she is for the next scene.
46|||Hodram's questioning sound gives Gerhard room to show him.
50|||Gerhard directs Hodram to the person they found.
56|||Keep Hodram's brief, subjective comparison to a doll in its original speakerless panel.
60|||The speakerless punctuation marks the sudden action before Gerhard calls out.
64|Admiral! That woman...!|Admiral!|Gerhard calls to the admiral and breaks off in alarm at her attack.
67|Wait! Ngh... I think she took me for a pirate or something.|took me for a pirate|Hodram stops Gerhard, reacts to pain and suggests she mistook him for a pirate or a similar threat.
73|||Sera makes no reply. Keep the speakerless beat after Hodram explains her reaction.
77|I don't blame you. It's all right. You're free now.|I don't blame you.;You're free now.|Hodram acknowledges why she mistrusted him and directly tells her she is free.
80|||Sera stays silent after the assurance. Preserve the pause before Hodram guesses at her origins.
84|Your features... You look different from the other Africans here.|the other Africans here.|Keep this as Hodram's observation, without treating her appearance as proof of where she comes from.
87|From your clothes, I'd guess you're not Muslim. Maybe you come from a prominent family.|I'd guess you're not Muslim.;a prominent family.|Hodram guesses about her faith and family from her dress. Both conclusions are tentative.
91|||The silence follows Hodram's guesses and helps him realize they cannot understand one another.
95|||Hodram concludes they do not share a language, without naming hers.
107|What shall we do? We can't take her home if we don't know where they brought her from.|What shall we do?;where they brought her from.|Gerhard politely asks what to do and explains they cannot return her without her point of origin.
113|What do we do? We can't take her home without knowing where they took her from.|What do we do?;where they took her from.|Manuel voices the same practical obstacle in a more familiar register. The captors brought her from a place the crew does not know.
120|||Hodram turns from Sera to ask about the other captives.
130|||Gerhard says the captives seem to want them to let them go where they are.
135|||Charles gives the same report on the alternate crew path. The uncertain seem agrees with the source.
141|As far as they're concerned, we could be just as bad. All right. Anyone who wants to go is free to leave.|All right.;Anyone who wants to go;free to leave.|Hodram recognizes the captives cannot be expected to trust him and lets all who wish to leave go here.
151|||Gerhard acknowledges the release order on his path.
157|||Charles gives the same assent on his path.
164|You can go if you want, too. That knife won't keep you safe out there. Here, take this.|That knife won't keep you safe;out there.;Here, take this.|Hodram offers Sera the same freedom, judges the knife inadequate for defense, and offers an alternative weapon.
168|||The speakerless heading keeps Sera unidentified and records her startled reaction without spoken dialogue.
171|I-it's dangerous to give her a weapon! She might come at you again!|give her a weapon!;come at you again!|Gerhard stammers a warning that giving her the weapon may let her attack again.
175|||Hodram's calm reply leaves her the choice, even if she wants to use the weapon against him.
179|||Gerhard's alarm remains a single brief address to Hodram.
183|||The original caption marks Sera's silent reaction as the crew watches.
194|||Manuel's wordless alarm fits the moment when her action is unclear.
201|||The shout is Gerhard's last warning before her response is apparent.
205|||Keep Sera's pause in the original caption rather than giving her a line.
208|||Hodram realizes she may not want the weapon and asks her a direct question.
212|||The caption records a nod, without supplying words she does not speak.
215|||Hodram pauses and quietly accepts what her nod means.
226|(That scared me...)||(Manuel privately admits the action startled him.) The aside stays distinct from the spoken lines.
233|||Gerhard's quiet relief follows Manuel's reaction and closes the scene.
""",
    16: """
6|||Gerhard acknowledges the victory simply, before Hodram responds.
10|Of course. If we're aiming to be the strongest fleet, this is the least we should manage.|the strongest fleet,;the least we should manage.|For Hodram the victory is the minimum expected of a fleet aiming to be the strongest.
13|||Gerhard's dry observation answers Hodram's high expectations.
17|They were lost at sea... Or perhaps I should say they went home to Mother Sea.|lost at sea...;Mother Sea.|Manuel shifts from mourning the loss to picturing a return to the sea as a mother.
21|||Hodram speaks Manuel's name as the mood changes. Preserve his hesitation.
25|Let's honor the spirits of those we lost at sea.|honor the spirits;we lost at sea.|Manuel proposes comforting the dead. The reference to their spirits leads into the elegy.
28|||Hodram's brief puzzlement leaves the floor to Manuel.
32|"The sea is like a mother. The waves lap with a familiar rhythm, like the heartbeat of a mother far away.|The sea is like a mother.;a familiar rhythm,;a mother far away.|The first panel compares the recurring waves to the remembered heartbeat of a distant mother. Keep the poem's opening quotation.
35|The sea is like a mother. In some lands, they say the words for sea and mother can look and sound the same.|The sea is like a mother.;In some lands,;look and sound the same.|Repeat the opening of the second stanza and preserve the hearsay that sounds and written forms can coincide in other languages.
39|The sea is like a mother. Both hold us in a bond that lasts as long as we live."|The sea is like a mother.;as long as we live.|The final stanza repeats the refrain and places both in the enduring bond of a lifetime. Close the quotation here.
42|||Hodram genuinely admires the poem and is surprised by Manuel's talent.
45|||Gerhard adds a simple agreement rather than repeating Hodram's compliment at length.
49|||Manuel says the sea welcomes everything and wishes people could do the same. Keep his quiet reflection.
52|||Hodram leaves the thought unanswered and the scene ends on silence.
""",
    17: """
6|Damn, I lost again... But next time... Huh?!|I lost again...;But next time...|Aziza acknowledges another loss, starts to promise revenge and breaks off as she notices the mutiny.
9|||Angel repeats her phrase and makes it clear she will get no further chance. The existing wrap keeps a next time together.
12|||Snake's low laugh backs Angel before Aziza demands he repeat himself.
16|||Aziza reacts with disbelief and demands that Angel say it again.
20|||Angel taunts her by asking whether she heard him.
24|There's nobody left here who'll take orders from you!|take orders from you!|Angel spells out the mutiny. Nobody there will follow her orders.
27|||Aziza realizes her crew has betrayed her and curses them.
30|||Hodram notices noise across the way without knowing what it means yet.
34|||Gerhard identifies Aziza as the pirate they encountered and says her own people seem to have surrounded her.
37|||Hodram's short order brings the ship closer before they intervene.
41|We keep losing. Our pockets are empty. You're gonna answer for it.|Our pockets are empty.;You're gonna answer for it.|Angel blames Aziza for the repeated defeats and lack of money, then demands she answer for it.
45|||Aziza repeats Angel's demand in surprise and anger.
49|Why are we chasing FO all over, anyway?|all over, anyway?|Dandy asks why Aziza keeps having them chase the named fleet.
53|Heh. Got a reason you can't tell the rest of us, huh?!|the rest of us, huh?!|Snake insinuates that her reasons are something she cannot admit in front of the crew.
56|||Aziza's wordless reaction gives Snake room to expose her motive.
60|You just want the Bloodstained Shamshir back from FO. A keepsake from your old man!|Bloodstained Shamshir;your old man!|Snake identifies the named blade as what Aziza wants back and says it is a keepsake from her father.
64|||The unfinished denial preserves Aziza's sudden uncertainty after being confronted.
68|You've been slipping. Who's gonna follow a captain who can't make them any money? You've got this coming!|make them any money?;You've got this coming!|Angel says no one wants to follow a leader who brings them no money, then threatens her.
72|Admiral! If we do nothing, they'll kill her!|they'll kill her!|Gerhard warns Hodram that leaving Aziza alone will mean her death.
76|||Hodram succinctly decides that they cannot abandon her.
80|||Al Shin's short statement makes him the first to move.
84|W-wait! Don't do anything rash!|Don't do anything rash!|Gerhard stammers as he tries to stop Al Shin from rushing into the fight.
88|||Snake tells the newcomer to stay out of the mutiny. His blunt insult works in context.
91|...Don't get cocky, you two-bit thug.|you two-bit thug.|Al Shin dismisses Snake as a presumptuous underling before Angel escalates.
95|None of your business! While we're at it, let's get rid of Aziza and this guy!|None of your business!;While we're at it,;Aziza and this guy!|Angel rejects the intervention and orders the men to deal with both of them.
99|Al, I will lend you my blade.|lend you my blade.|Yukihisa offers Al formal assistance in the fight.
103|||Cristina volunteers and condemns men who rely on superior numbers.
106|Why don't we send them flying with a good, loud bang?|a good, loud bang?|Charles offers explosive help and enjoys the prospect. No weapon or result is asserted.
110|||Al Shin directly challenges the pirates. The short invitation fits his voice.
113|||Aziza is bewildered that people who were her enemies moments ago fight for her now.
117|D-damn! We're outmatched!|We're outmatched!|Angel stammers when he realizes the fight has turned against him.
121|||Hodram's dry retort shows he thinks the change in their odds should have been obvious.
125|||Aziza trails off as she recognizes Hodram. Keep both name substitutions in source order.
129|||Snake is surprised Hodram has also come to help Aziza.
133|What if I did?|What if I did?|Hodram answers Snake's question about him personally, without explaining his reasons yet.
137|Tch. This is all her fault. How'd we end up in this mess?|This is all her fault.;this mess?|Angel blames Aziza and bitterly questions how his men ended up losing control of the situation.
140|Had enough of complaining? Why don't you let her go?|Had enough of complaining?;Why don't you let her go?|Hodram tells the mutineers to stop complaining and suggests they release Aziza.
143|You just want Aziza gone, right?|just want Aziza gone, right?|Hodram checks that getting rid of Aziza is all they want. Keep the short tag together.
149|||Aziza stays silent after Dandy confirms they will no longer follow her.
153|Then we'll take Aziza with us.|take Aziza with us.|Hodram offers to take her away with them if they want her gone.
156|||Aziza's wordless surprise interrupts the bargaining.
164|||Al Shin reacts to Dandy's demand for payment with a short incredulous question.
168|Al, leave it. How much do you want?|How much do you want?|Hodram stops Al Shin from escalating and asks Dandy to name a price.
171|||Dandy names the exact sum of one million gold.
176|||Al Shin calls Aziza toward him with a subdued pause.
180|||Aziza makes no spoken response as she goes with them.
184|||Angel declares their business done and brusquely leaves.
190|Never thought my own crew would turn on me. I've really sunk low... Anyway, why'd you save me?|my own crew;why'd you save me?|Aziza is stunned by the betrayal and then returns to the question of why her enemies rescued her.
193|||Al Shin simply says he could not leave her there. He does not give a grand reason.
197|Anyone who'd leave you there would have to be heartless.|would have to be heartless.|Hodram says abandoning her in that situation would be inhumane.
200|I've been wondering... Why would someone with your skill turn to piracy?|with your skill;turn to piracy?|Yukihisa asks respectfully despite viewing piracy as a fall from what she could be.
204|You think too highly of me. I didn't fall into piracy. I'm a pirate's daughter. My father was one.|You think too highly of me.;a pirate's daughter.|Aziza answers Yukihisa by denying that she fell from anything and explicitly identifying her father as a pirate.
207|||Hodram gives a short interested prompt before Aziza tells the story of her upbringing.
211|Those pirates were my father's crew. I grew up copying them, learning swordplay and the pirate trade.|my father's crew.;the pirate trade.|Aziza explains that they used to serve her father and she learned his trade and swordsmanship by watching and imitating.
214|||Gerhard asks where her father is now, without assuming he is still alive.
218|||Aziza says he died in an accident and that the sword he treasured vanished with him. Keep the event and the uncertainty about the sword.
222|||Al Shin names the Bloodstained Shamshir, tying it to the conversation about her father.
225|||Aziza openly admits she wanted to be a great pirate like her father and imitated everything he did.
229|When I heard you had his sword, I had to get it back. I thought...|I had to get it back.;I thought...|Aziza explains why she went after the sword and trails off before saying what she thought it would prove.
232|||Hodram's puzzled silence gives her room to continue.
236|I thought it would prove I was a little more like him. Heh... But you know what?|a little more like him.;But you know what?|Aziza says the sword seemed like proof she was measuring up to her father, then reevaluates what she really wanted.
240||a great pirate.;remember my father by...|The wording already makes the keepsake more important than becoming a great pirate. Move the final phrase about her father onto one line.
243|No wonder they turned on me. I was chasing something that wouldn't make them any money. I can't blame them for being angry.|they turned on me.;being angry.|Aziza understands her crew's anger at spending time on something that would earn no money, without excusing how they treated her.
247|||Al Shin asks whether she still wants the life of a pirate.
251|I was chasing my father, not a life of piracy. I'm done with it.|chasing my father,;I'm done with it.|Aziza distinguishes missing her father from wanting to continue as a pirate, and says she intends to quit.
255|||Al Shin begins to address Hodram but leaves the request unspoken.
259|I know what you want to say, Al. Aziza, will you sail with us?|I know what you want to say, Al.;Aziza, will you sail with us?|Hodram understands Al Shin's unspoken request and directly asks Aziza to join his ship.
262|I'd be grateful. I'll work my heart out. I owe you my life, after all.|I'll work my heart out.;I owe you my life,|Aziza accepts gratefully and promises to work hard because they saved her life.
266|||Aziza invites them to use her given name. The plain phrasing fits her new place among them.
272|||Hodram anticipates that things will get even livelier. The wry understatement closes the encounter.
""",
    18: """
18|We're pulling out! We'll settle this next time!|We'll settle this next time!|Aziza calls off the current fight and promises to settle the matter next time.
21|||Hodram brushes off her threat with a dry two-word response.
27|||Aziza says the retreat is temporary, refuses to submit and tells him her full name.
31|||Hodram's terse acknowledgment plays off her forceful introduction.
""",
    19: """
16|||Hodram decides to withdraw for now. The short declaration suits the urgency.
20|Running away?! You're more of a coward than you look!|Running away?!;than you look!|Aziza taunts him for retreating and calls him more cowardly than he looks.
23|||Gerhard warns Hodram not to take the bait. The existing idiom works in the exchange.
27|||Hodram knows she is trying to provoke him and immediately repeats the order to withdraw.
33|||Aziza complains that they got away.
37|||Gerhard advises pulling out for now on the alternate branch.
41|That pirate's no amateur. She'd hold her own as a naval admiral...|hold her own;as a naval admiral...|Hodram acknowledges that her ability would stand up in a regular navy. He does not assert that she holds a rank.
45|||Aziza asks if he thought he could beat her and threatens him the next time they meet.
""",
    20: """
9|||Hodram tells Julian to behave and gives Sao Jorge as their destination. The terse wording suits a prisoner transfer.
12|||Julian curses and tells them not to touch him. The abrupt muffled end preserves the interruption.
""",
    21: """
9|||Hodram orders them to tie Plett securely and take him to Hangzhou.
12|Ow, ow, ow! I-I know what I did was wrong...|I-I know what I did was wrong...|Plett cries out at being bound and stammers a claim of remorse.
""",
    22: """
8|||Hodram's dry comment explains why the Basra guild has had such trouble with Ramusio.
11|||Ramusio defends himself by claiming the region would have fared even worse without him.
15|Trying to justify what you did? You're a disgrace. Have you no shame?|Trying to justify what you did?;Have you no shame?|Gerhard is disgusted by Ramusio's attempt to justify his wrongdoing.
""",
    23: """
9|||Portunto stammers and laments what he calls his precious cargo.
12|Never mind the stolen cargo. Worry about yourself. We're taking you to Calicut.|the stolen cargo.;taking you to Calicut.|Hodram corrects Portunto's claim to the cargo and reminds him that he will be taken to Calicut to face his own situation.
""",
}

source = checked_text(getsource(previous.main), {
    'len(records) == 118': 'len(records) == 195',
})
scope = vars(previous) | globals()
exec(compile(source, __file__ + "::opening-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
