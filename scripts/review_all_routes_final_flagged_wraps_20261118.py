"""Review Lil's and Maria's remaining identified phrase breaks."""

from collections import defaultdict
from inspect import getsource
from pathlib import Path

from scripts import register_all_routes_remaining_phrase_wraps_20261118 as parent
from scripts import review_rafael_early_phrase_wraps_20261118 as common
from scripts.source_locked_derivation_v5118 import checked_text

base, TOKEN, logical = common.base, common.TOKEN, common.logical
ROOT = Path("work/all_routes_final_flagged_wraps_20261118")
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v1.json"
REVISIONS_TEXT = """
2,189,13|Ceramics owner confirms it is as fine as he expected.|His confident praise leads naturally into the other collector's request to see it.|Yes. Superb, just as I expected.
2,197,49|The dealer wishes Ian the same romance as the tale.|Match the other purchase branch and keep the wish playful.|@3,170,48
2,199,95|Lil is delighted by an apparently old gift she believes is from Camille.|Her teasing delight gives him no time to finish explaining.|It looks old. A gift from you, Camille? That hardly ever happens!|A gift from you, Camille?|That hardly ever happens!
2,212,5|The speaker greets the group and asks whether they know the Romance of the Three Kingdoms.|Put the full work title in the question before the reply choices.|Hey there! Ever heard of Romance of the Three Kingdoms?|Hey there! Ever heard of|Romance of the Three Kingdoms?
2,213,72|The old man tells them to search south of the Shandong Peninsula for the imperial greatsword.|Match the wording used for this clue in Rafael's route.|@0,225,66|south of the Shandong Peninsula.
2,228,28|Samwell presses Lil to see the value of a shield harder than iron and asks if she wants it.|Keep the exasperation and his practical reason in complete thoughts.|Come on! A shield harder than iron. Don't you want one? It'd come in handy in a fight.|A shield harder than iron.|Don't you want one?|It'd come in handy in a fight.
2,235,44|The Spanish navy's chance appearance saves the convoy after it holds out and the pirates scatter.|Use Charles's matching report and keep the escape on a single page.|@3,208,43
2,235,47|The sound remains unidentified and a scientific natural explanation is uncertain.|Use the same measured wording as Charles's corresponding letter to Hodram.|@1,238,47
2,239,91|The ornament may be inexpensive but it was a birthday gift from her father because she loves roses.|Match the same personal account in Rafael's route within four rows.|@0,251,100
2,240,120|The barkeep says to return the ornament and vows to report the swindler if he sees him again.|Keep the conditions of the threat and fit the handover on one page.|@0,252,116
2,242,35|Only people the figurehead likes can take it.|Match the priest's explanation in Rafael's route.|@0,254,37
2,250,98|Cesare agrees aloud and privately admits mild disappointment.|His quick spoken assent keeps its own beat above the aside.|Of course. (Too bad, though...)|(Too bad, though...)
2,254,10|The woman acknowledges the worldwide search but says there are no especially famous ruins nearby.|Use the established reply for this shared source line.|@0,264,10
2,261,5|Lil tells the older guildmaster she found the adventurer Julian, but pauses on the complication.|Preserve the adventurer detail and stop where Lil is interrupted.|Found the adventurer Julian, but...
2,268,17|The guildmaster is unimpressed and glad a foreign guild did not get the thief, since someone might take advantage of his noble status.|Keep the sarcasm and the reason a foreign guild might want him.|Some prize. At least no foreign guild got him. People will use him just because he's a nobleman.|At least no foreign guild got him.|just because he's a nobleman.
2,268,74|It is said to be sealed in the town ruins and the guildmaster urges a firsthand check.|Keep the discovery a rumor and let the invitation stand on its own.|It's sealed in the town ruins, so they say. Go see for yourself.|It's sealed in the town ruins,|so they say.|Go see for yourself.
2,273,15|A former petty thug apparently struck it rich in Africa and now acts like a big pirate.|Keep the change in his fortunes and remove the padded spaces in the introduction.|He was a petty thug until recently. Then he got rich in Africa, I hear. Now he's playing big-shot pirate.|He was a petty thug until recently.|Then he got rich in Africa, I hear.|Now he's playing big-shot pirate.
2,287,83|The map is genuine. The speaker half-suspects Lil might belong to the group.|Keep the suspicion tentative so his laugh in the next turn works.|Yeah, that's it! Wait... Are you with that bunch, too?|Are you with that bunch, too?
2,288,122|Camille objects that the normal response is to say let's go.|The stammer and quoted example keep the joke about hesitation.|W-what are you saying? This is where you say, 'Let's go!'|W-what are you saying?|'Let's go!'
2,290,57|Lil understands the platinum reference and decides to take some aboard.|Keep her brisk conclusion and the shipboard destination.|Oh, that! Let's take some platinum aboard.|Let's take some platinum aboard.
2,296,23|Lil needs to get the wristband to the Istanbul guild right away.|Keep the full artifact name on one line in the delivery reminder.|The Heavenly Wristband has to go to the guild in Istanbul right away.|The Heavenly Wristband|the guild in Istanbul|right away.
2,296,39|The guildmaster checks if the wristband has been found.|Use the entire artifact name in the one-line question.|Found the Heavenly Wristband yet?|the Heavenly Wristband
2,299,152|Camille confirms the animal went deeper into the forest.|Keep the direction of retreat in one continuous response.|Yeah. It went deeper into the woods.|deeper into the woods.
2,304,11|Local merchants do not trade spices, so the guild must source them in other towns.|Preserve what the player already knows and why the guild needs outside supply.|You know we don't sell spices here. We'll have to buy them out of town.|You know we don't sell spices here.|We'll have to buy them out of town.
2,306,159|The crewmate reluctantly agrees, then spots a ferry and alerts Lil.|Let his first reaction finish before the sudden discovery.|Yeah, sure... Huh? Admiral, look! There's a ferry over there!|Admiral, look!|There's a ferry over there!
2,310,52|Lil returns with the tea and sugar.|Her jaunty report names the goods from the earlier instructions in one line.|I'm back with the tea and sugar!|tea and sugar!
2,313,13|The host is supposed to conceal the gate's location from foreigners.|Match the same hesitant disclosure in Hodram's route.|@1,310,13
2,313,16|Outside pressure has made the seclusion policy nearly meaningless, so the host agrees to tell Lil in confidence.|Use the same political explanation and private offer as in the parallel exchange.|@1,310,16
2,319,11|The speaker apologizes for the form of address but warns that a young woman is in danger here even if she leads a company.|Keep the patronizing voice, warning and rank already established in Lil's reply.|Ha! Sorry, sorry. In charge or not, a young woman shouldn't wander around here. It's dangerous. Watch yourself.|In charge or not,|a young woman|It's dangerous.|Watch yourself.
2,323,104|Lil proposes trying to proceed into the limited visibility.|Her casual encouragement follows the immediate route choice.|Come on. Let's see how far we get.
2,327,8|The guildmaster wants New World tomatoes to become fashionable in Mediterranean Genoa.|Keep the commission direct and the city and region explicit.|I want New World tomatoes to catch on in Genoa, over in the Mediterranean.|New World tomatoes|catch on in Genoa,|over in the Mediterranean.
2,327,22|Publicizing a town's enthusiasm is the quickest way to make people try a good food they distrust.|Keep the proposed rumor and why he wants to spread it.|Want folks to try tomatoes? Get them talking about a whole town that loves 'em. That's the fastest way.|Want folks to try tomatoes?|a whole town that loves 'em.|That's the fastest way.
2,335,82|Charles found out that he needs the Alchemy Book to obtain the material.|Use the corresponding unfinished thought from the other route.|@0,342,78
2,335,86|Charles is certain the book points to a precious metal and begins thinking aloud about how to use it.|Use the matched line before Lil cuts him off.|@0,342,82
2,335,89|Lil cuts Charles off because she anticipates a long explanation.|Keep the stammer and land the aside after a complete interruption.|O-okay, spare us the details. This could take a while...|O-okay, spare us the details.|This could take a while...
3,212,116|Maria proposes Havana because they appear to have no other lead.|Keep the reasoning cautious after Xien says the swindler is not necessarily the thief.|Let's try Havana. It's the only lead we've got.|Let's try Havana.|It's the only lead we've got.
3,213,45|The swindler takes the challenge as an attempt to make trouble for his business.|Keep the angry overreaction and complete his question.|Wh-what?! You trying to make trouble for me? For my business?|You trying to make trouble|For my business?
3,213,107|The barkeep returns the ornament and threatens to report the crook if he sees him again.|Match the one-page handover from the same exchange on Rafael's route.|@0,252,116
3,215,35|The figurehead itself chooses who can carry it off.|Match the previous explanation by the same priest.|@0,254,37
3,221,125|The sailor points out a statue that looks like a figurehead.|Keep the exact parallel wording before the noise interrupts.|@0,261,137
3,224,9|The woman acknowledges a worldwide ruins search and says none here are particularly famous.|Match the same disappointed reply used in the other routes.|@0,264,10
3,225,24|The only clue about Plett is that he is hiding somewhere around Indonesia.|Keep the uncertainty that makes the favor seem difficult.|He's in hiding near Indonesia. That's the only lead I've got.|He's in hiding near Indonesia.|That's the only lead I've got.
3,226,23|Plett stammers and admits his identity once he is discovered.|His admission and full name stand apart from the opening hesitation.|N-no use hiding it. I'm Plett Perrault, all right.|N-no use hiding it.|I'm Plett Perrault, all right.
3,231,63|The ruins are said to be Solomon's former treasury and the guildmaster invites a visit.|Use the earlier wording for the same legend and invitation.|@1,250,55
3,233,13|The guildmaster wants Maria to find the Spanish spy Peralonso Aguirre, reportedly active near Southeast Asia.|Keep the name and geographic lead complete.|Find a Spanish spy for me. His name's Peralonso Aguirre. Word is he's in Southeast Asia.|Find a Spanish spy for me.|His name's Peralonso Aguirre.|Word is he's in Southeast Asia.
3,234,21|Maria ignores the attempt to get her to pour a drink and asks the barkeep for a man by name.|Keep her cool redirection and the complete name she is about to hear echoed.|...Barkeep, I'm looking for a man named Peralonso Aguirre.|Peralonso Aguirre.
3,238,15|The guildmaster is relieved no foreign guild took the thief because others might exploit a nobleman.|Match his wording in Lil's reward exchange.|#2,268,17
3,243,4|The guildmaster asks an able fighter to deal with a wanted man.|His opening challenge invites the player into the specific commission.|Handy in a fight? Can you deal with a wanted man for us?|Handy in a fight?|a wanted man for us?
3,252,277|Samwell warns the admiral that it could be a man-eating bear and that an ill-judged attack would endanger them.|Restore the animal named in Japanese and keep the warning on one page.|Admiral, this is bad! It could be a man-eating bear! If we go after it, we'll be the ones in danger!|Admiral, this is bad!|It could be a man-eating bear!|If we go after it,|we'll be the ones in danger!
3,261,59|The guildmaster offers an interesting story in thanks.|Give the favor a conversational transition to the rumor.|Let me tell you a story. My way of saying thanks.|Let me tell you a story.|My way of saying thanks.
3,262,65|The same guildmaster thanks the player with the same rumor.|Use the exact same introduction before the parallel rumor.|#3,261,59
3,265,5|A dockworker says the guild in Istanbul has been looking for the player.|Keep the name of the city and the purpose of the notification in one line.|Istanbul's guild wants to see you.
3,267,89|Xien says they did not finish the creature off but its wounds will keep it away for a while.|Keep both the outcome and his reason for believing they are safe.|We didn't finish it off. With wounds like that, it won't be back for a while...|We didn't finish it off.|With wounds like that,|it won't be back for a while...
3,271,4|The speaker asks the group if anyone knows both shipbuilding and gunnery.|Keep the dual specialty in the question that prompts the crew to speak up.|Any shipbuilders who know gunnery?
3,273,14|The guildmaster thanks Maria on behalf of the shipwright.|Keep the relationship and his gratitude ahead of the gift.|On the shipwright's behalf, thanks.
3,275,65|The man helped foreigners sell weapons and armor without the local lords knowing.|Keep what he sold and who was kept in the dark in his blunt admission.|I helped foreigners sell arms and armor behind the local lords' backs. That was the racket.|I helped foreigners sell|arms and armor|behind the local lords' backs.|That was the racket.
3,275,128|His boss was tight-lipped and kept telling him to stay away from the distinguished party.|Preserve the self-deprecation and repeated order without invisible padding in the first row.|Dunno. The boss was tight-lipped. He kept telling a lout like me to keep away from such fine guests.|Dunno. The boss was tight-lipped.|He kept telling a lout like me|to keep away from such fine guests.
3,275,138|He suggests the informant in the Macao tavern might know more.|Give Maria one coherent lead in a sentence she can act on.|The informant in the Macao tavern might know something.|the Macao tavern|might know something.
3,277,58|Maria calms him down and says the supposed missionaries are probably impostors.|Let her give the conclusion with its uncertainty intact.|Calm down. Hear me out. I think they're fake missionaries.|Calm down. Hear me out.|I think they're fake missionaries.
3,277,81|Maria explains that a deal at government scale would earn a fortune and starts to consider what they will buy.|Keep the conditional and the trailing inference that the next line completes.|It's a deal on a national scale. They'll make a fortune if it works. And with that money...|It's a deal on a national scale.|They'll make a fortune if it works.|And with that money...
3,277,139|The suspects went toward the governor's office and Maria wants to hurry after them.|Keep the destination intact and give her urgency a complete thought.|They went to the governor's office. We'd better hurry!|They went to the governor's office.|We'd better hurry!
3,279,25|The woman is surprised at Maria's ordeal, then notices the time.|The second reaction turns smoothly to the temple visit.|What an ordeal! Oh! Is it that late already?|What an ordeal!|Is it that late already?
3,290,5|The new security is tight enough that the bandits should give up.|Keep this as the guildmaster's expectation after seeing the delivery.|Good. With security this tight, the bandits should give up.|With security this tight,|the bandits should give up.
3,292,178|Maria is startled by the bats after successive obstacles and expresses exasperation.|Keep the surprise and exasperation in a brief reaction.|Bats now? What next...?
3,293,78|The guide announces arrival and says they will continue on foot.|Match the identical guide instruction in the other routes.|@0,334,81
3,295,22|The guildmaster has sent both patrols and fleets to pursue the enemy, but it has never been seen and vanishes without trace.|Use plain terms for both responses and keep the mystery central.|We've sent patrols and fleets to hunt it down. No one's spotted it yet. It comes and goes without a trace.|to hunt it down.|No one's spotted it yet.|It comes and goes without a trace.
3,296,123|The guide asks Maria to find the Ancient City Map and let him know so he can join the search.|Keep the artifact name and his request to accompany them.|First, get the Ancient City Map. When you find it, let me know. I'll join the search.|First, get the Ancient City Map.|When you find it, let me know.|I'll join the search.
3,302,75|Charles knows the book is required to obtain the material.|Keep his same unfinished thought in the parallel encounter.|@0,342,78
3,302,79|Charles is certain it's a clue to a precious metal and begins muttering about using the book.|Use the matched earlier turn and leave room for Maria's interruption.|@0,342,82
3,208,46|Charles does not know what made the sound or whether science could explain it as a natural event.|Use the established wording from the equivalent letter and eliminate the break seen after is.|@1,238,47
"""
RETENTIONS_TEXT = """
2,189,9|The collector asks whether the other man's purchase was the ceramics.|The recognition identifies what the reply praises.
2,189,16|He wants to see the fine ceramics.|The courteous request makes the invitation to visit natural.
2,197,45|Ian decides to buy it.|His plain acceptance sets up the seller's teasing wish.
2,197,53|Ian says he is uninterested.|His dry rejection keeps the joke understated.
2,199,91|Camille starts to explain that it is not what Lil thinks.|The stammer allows Lil to interrupt without understanding.
2,199,103|Lil thanks Camille.|Her uncomplicated gratitude completes the misunderstanding.
2,213,69|The elder is sure she is the ruler of the seas.|The confident claim leads to the geographic clue.
2,213,75|He entrusts the greatsword to her and leaves.|The farewell makes clear why the clue is all he gives them.
2,228,24|Lil asks Samwell for his point.|Her impatience gives him a reason to explain the shield's usefulness.
2,228,31|Lil understands and asks where to look.|Her change of mind gives him the next question.
2,235,41|A strange roar rallies the ship crews and they fight fiercely.|The lion image preserves Charles's description before the rescue.
2,235,50|Charles suggests investigating and signs his letter.|The suggestion remains optional and the signature is clearly his.
2,239,87|Lil asks about the woman's treasure.|The simple echo prompts her account.
2,239,94|The woman loved the ornament because it looks like an actual frozen rose.|The image gives the gift its personal significance.
2,240,115|The barkeep thanks the crew and identifies the object they came for.|His question gives the context for the return instruction.
2,242,31|Julio prompts the priest to finish.|The brief echo carries the hesitation naturally.
2,242,39|Most people who tried went home injured and empty-handed.|The consequence makes the priest's warning concrete.
2,250,102|Lil suggests heading back.|The quick decision follows Cesare's spoken assent.
2,250,109|Cesare agrees and privately reflects on the statue.|His second aside keeps the private reaction distinct from his ordinary reply.
2,254,6|The woman greets Lil by name.|The native given-name token and informal greeting still work.
2,261,8|The guildmaster asks where Julian is.|The short follow-up lets Lil finish the explanation.
2,261,12|Julian is in Copenhagen and will not come back to Seville.|Keep both locations and attribute the reluctance to Julian.
2,268,13|Lil is tired of the nobleman's protest.|The short aside leaves the guildmaster to comment on the capture.
2,268,20|The guildmaster presents the reward.|The direct handoff follows his relief.
2,268,66|He introduces a rumor about a demon statue.|The quick question changes subject before he identifies the ruins.
2,273,11|The guildmaster wants Lil to catch a wanted Dutch smuggler.|The characterization and exact name identify the target.
2,273,18|He offers an advance because they cannot take the man on themselves.|Both the advance and their reason for asking Lil remain clear.
2,287,78|Lil shows him a map and asks whether it is the one he means.|The direct question sets up recognition.
2,287,86|The speaker laughs off his suspicion.|His laughter closes the teasing response.
2,288,128|Lil hesitantly agrees.|The stammer keeps the cave fear apparent.
2,288,140|Camille asks if Lil is afraid of caves.|His question explains the awkward replies and keeps the live given name.
2,290,54|Charles reminds Lil of the Alchemy Book.|The established book name sets up her recognition.
2,290,61|He thinks platinum is mined in southern Africa.|Both the region and the uncertainty remain.
2,296,18|Lil wonders where the wristband is and remarks on the size of the New World.|The title and broad search area remain explicit.
2,299,166|Lil exclaims that they are running.|Her emphatic choice fits the alternate retreat.
2,304,8|Indian Ocean traders are preparing an exhibition with spices to sell.|Both purposes are clear before the supply problem.
2,304,15|Preparations leave the guild short of spices to sell.|The detail explains why they cannot solve the problem themselves.
2,306,162|Lil sees the convenience of the ferry and orders an orderly crossing.|Her attitude shifts from crossing by foot to using the boat.
2,310,56|The customer thanks Lil then starts the next instruction.|The trailing phrase sets up her impatient answer.
2,313,6|The host welcomes Lil by name.|The live given-name token preserves the familiar welcome.
2,313,9|She confirms Lil wants to know the location of the city gate.|The question makes the referent in the confidential reply clear.
2,319,8|Lil objects to being called little lady because she leads the company.|The live company token and sharp reply keep her authority clear.
2,319,14|Lil asks why the area is dangerous.|Her short question lets him explain the actual risk.
2,327,12|Lil asks why tomatoes should be popularized in Genoa specifically.|Her confusion explains why the guildmaster gives more than a commission.
2,327,19|The guildmaster says people avoid tomatoes because the red reminds them of blood.|The explanation stays part of his effort to sell the idea.
2,327,25|Genoa seems the best bet because tomatoes are already liked in Italy.|The reported liking and his inference give his choice a reason.
2,327,28|Lil agrees to try.|Her short conclusion follows the whole pitch.
2,335,94|Lil declares that she has found it at last.|The brief excitement fits the completed discovery branch.
3,212,109|The woman reports an indirect lead about a Havana swindler passing glass off as jade or crystal.|The chain of hearsay, city and materials explain Xien's skepticism.
3,212,112|Xien says being a swindler does not prove he stole the rose.|His caution motivates Maria's choice to follow the only lead anyway.
3,212,123|The woman thanks them.|Her quick reaction lets the decision stand.
3,213,42|Maria asks whether the ornament is real amethyst.|The pointed question motivates the swindler's outburst.
3,213,49|Maria calls Xien.|The brief address directs her next step without explaining it aloud.
3,213,102|The barkeep thanks them and asks if this is the object they wanted.|His question prepares the return instruction.
3,215,31|Julio echoes the priest's hesitation.|The brief prompt works before the explanation.
3,215,39|Most attempts to take the statue ended with injury and no figurehead.|The result gives weight to the rule.
3,221,121|Maria asks where the crewmate spotted the statue.|The brief question leaves the discovery with the crewmate.
3,221,132|The crewmate stammers in alarm.|His reaction keeps the cracking sound unexpected.
3,224,5|The woman greets Maria by name.|Her direct greeting keeps the live substitution.
3,225,17|Maria agrees to capture Plett Perrault.|Her plain agreement keeps the assignment clear.
3,225,27|Maria recognizes that he is good at asking favors.|The dry remark lands after the modest claim about his lead.
3,226,20|Maria sees his alarm and guesses he is Plett.|Her teasing question gives him a reason to confess.
3,226,26|Maria notes his honesty and tells him he is coming to Hangzhou.|The measured order motivates his refusal.
3,231,60|The guildmaster asks whether they know the nearby ruins.|The opening question identifies the place in his legend.
3,233,9|Maria asks what kind of work he has in mind.|Her pause preserves her reception of his flattery.
3,233,16|She suspects the assignment might be easier for a woman.|Her assessment leads to his invitation to meet the target.
3,234,18|Peralonso asks Maria to pour him a drink.|The command shows why Maria bypasses him.
3,234,25|He recognizes his own name and announces himself.|The repetition makes the apparent coincidence comic.
3,238,12|Maria calls the man's complaint petty.|Her dry response fits his fixation on being called a thief.
3,238,18|The guildmaster hands over the reward.|The handoff follows his relief about the capture.
3,243,8|Cardocci is trading illegally under their agreement and causing trouble.|His name and the exact complaint identify the work.
3,243,11|The guildmaster says the guards cannot take on the fleet and gives an advance.|The reasoning makes the advance and preparation relevant.
3,261,63|The ruins of an ancient kingdom supposedly stand intact inland.|Their location and the report's uncertainty motivate Maria's disbelief.
3,261,67|Maria doubts the claim about the ancient kingdom.|Her skepticism leaves the rumor open.
3,262,69|The speaker repeats the report that the intact ruins stand in the inland jungle.|The parallel rumor maintains the same setting.
3,262,73|Maria finds it hard to believe.|Her reaction works for this alternate commission.
3,267,85|Maria lets out a relieved breath.|The release of tension sets up Xien's assessment.
3,267,100|Maria wants to retreat to avoid a pointless fight.|Her wording makes the reason for the alternate action clear.
3,271,15|One crewmate offers to help if able.|The offer naturally follows the request for expertise.
3,271,29|A different crewmate wonders whether this is his chance to help.|His warmer reaction preserves the alternate response.
3,273,10|The speaker says the help should make the couriers' job easier.|The anticipated benefit precedes the reward.
3,273,19|Maria asks what the offered object is.|Her curiosity leaves its explanation to the giver.
3,275,68|Maria identifies him as their contact in Japan.|Her inference follows the confession.
3,275,71|He says he supplied firearms and other goods to the wokou.|The example and group name establish what his role entailed.
3,275,124|Maria asks when and where the missionaries will arrive.|Both questions motivate his admission that he does not know.
3,275,131|He wonders whether the boss thought preaching would sway him.|The joking guess fits his self-deprecation.
3,275,141|Maria confirms the Macao tavern and says she will inquire.|Her answer converts the rumor to a next action.
3,277,54|The companion says he is lost and asks what Maria has understood.|His impatience prompts her to slow him down.
3,277,74|Maria suspects the group intends to sell weapons and contraband to the Ming government.|Her specific inference gives the scale of the operation.
3,277,85|She thinks they could buy weapons capable of destroying any fleet sent after them.|The threat completes her previous sentence and remains conditional.
3,277,135|Maria says they must handle it themselves if the army will not listen.|The decision leads directly to the pursuit.
3,279,28|Maria asks if the woman was about to go out.|The question follows the sudden concern about time.
3,279,32|She says she planned to pray at the temple.|The specific destination closes the change of subject.
3,290,9|The guildmaster apologizes for the repeated trips and pays the price plus a reward.|Both parts of the payout explain the next notice.
3,292,174|Maria proposes lighting a light source.|The action sets up her surprised discovery of the bats.
3,293,65|The guide asks the party not to tell the sailors where the ruins are.|Both exclusive permission and secrecy explain the route.
3,293,81|The guide recognizes the place when they find it.|The exclamation fits the end of the search.
3,295,19|No one who had seen the enemy lived to report what it was.|The uncertainty motivates the guildmaster's account of the searches.
3,295,26|Maria thinks they must be skilled.|Her inference follows the guild's repeated failure to find them.
3,296,114|The guide pays an advance that need not be repaid if the ruins remain unfound.|The condition and advance are clear.
3,296,126|The guide will wait at the city gate.|The exact meeting point follows his offer to join the search.
3,302,72|Charles came after hearing that a material useful to his experiments was found in the New World.|He still speaks of a reported discovery rather than a proven fact.
3,302,82|Maria asks Charles to continue later.|Her calm deferral stays distinct from Lil's stammered interruption.
3,208,43|The Spanish navy arrived by chance and the convoy narrowly escaped.|The approved wording matches both other reviewed routes and keeps the escape on one page.
3,208,49|Charles recommends investigating and signs the letter.|His scientific uncertainty can lead naturally into the measured recommendation.
"""
PRIOR_LEDGERS = tuple(Path(f"releases/all_routes_editorial_20261118_{label}_candidate/verification/registered_review.json")
    for label in ("dialogue_followup", "continuing_phrase_wraps", "next_review_wraps", "ongoing_phrase_wraps"))
BLOCKS = ((), (), (), ())


def key(s):
    route, block, index = map(int, s.split(","))
    return route, block, index


def build_decisions(packet):
    current = {(g["route"], g["block"], r["source_record_index"]): r for g in packet["groups"] for r in g["records"]}
    prior = {}
    for file in PRIOR_LEDGERS:
        sha256 = base.digest(file)
        for r in base.load(file)["records"]:
            prior[r["route"], r["block"], r["source_reference"]["record_index"]] = (r, file, sha256)

    entries, revisions, matches, contexts = defaultdict(list), {}, {}, defaultdict(list)
    for line in REVISIONS_TEXT.strip().splitlines():
        identity, meaning, note, english, *phrases = line.split("|")
        route, block, index = record = key(identity)
        row = current[record]
        if english.startswith("@"):
            earlier, ledger, sha256 = prior[key(english[1:])]
            assert row["source_body_hex"] == earlier["source_hex"][2:] and earlier["review"]["formatting"]
            english, phrases = earlier["english"], phrases or earlier["protected_phrases"]
            matches[record] = dict(ledger=str(ledger), ledger_sha256=sha256,
                id=earlier["id"], reference=earlier["registered_reference"])
        elif english.startswith("#"):
            other = key(english[1:])
            previous = current[other]
            assert row["source_body_hex"] == previous["source_body_hex"]
            english, phrases = revisions[other]
            matches[record] = dict(file_path=previous["file_path"], block=other[1], source_record_index=other[2],
                source_offset=previous["source_offset"], exact_source_body_hex=previous["source_body_hex"])
        assert record not in revisions
        revisions[record] = english, phrases
        entries[route, block].append((index, meaning, note))
        contexts[route, block].append(meaning)
    for line in RETENTIONS_TEXT.strip().splitlines():
        identity, meaning, note = line.split("|")
        route, block, index = record = key(identity)
        assert record not in revisions and current[record]["selector"] < 207
        entries[route, block].append((index, meaning, note))
        contexts[route, block].append(meaning)
    assert entries.keys() == {(g["route"], g["block"]) for g in packet["groups"]}
    assert all(len(values) == len({index for index, _, _ in values}) for values in entries.values())
    notes = {group: "\n".join("|".join((str(index), meaning, note)) for index, meaning, note in sorted(values))
             for group, values in entries.items()}
    return revisions, matches, notes, {group: " ".join(values) for group, values in contexts.items()}


def main():
    global BLOCKS
    packet, selected = map(base.load, (SOURCE, ROOT / "selected_wrap_leads.json"))
    assert selected["paired_source_sha256"] == base.digest(SOURCE)
    assert selected["queue_sha256"] == base.digest(QUEUE)
    assert selected["candidate_sha256"] == packet["candidate_sha256"]
    assert len(selected["records"]) == 64
    BLOCKS = tuple(tuple(g["block"] for g in packet["groups"] if g["route"] == route) for route in range(4))
    revisions, matches, notes, contexts = build_decisions(packet)
    assert len(revisions) == 70
    assert {(int(r["file_path"][-5]), r["block"], r["source_record_index"]) for r in selected["records"]} <= revisions.keys()
    source = checked_text(getsource(common.main), {
        "len(resolved) == 8": "len(resolved) == 64",
        "NOTES[block]": "NOTES[route, block]",
        "CONTEXT[block]": "CONTEXT[route, block]",
        "key = (block, idx)": "key = (route, block, idx)",
        "            if lead := open_wraps.get": '''            if key in MATCHES:
                row["matching_dialogue"] = MATCHES[key]
            if lead := open_wraps.get''',
    })
    scope = vars(common) | globals() | dict(REVISIONS=revisions, MATCHES=matches, NOTES=notes, CONTEXT=contexts)
    exec(compile(source, __file__ + "::contextual-review-ledger", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
