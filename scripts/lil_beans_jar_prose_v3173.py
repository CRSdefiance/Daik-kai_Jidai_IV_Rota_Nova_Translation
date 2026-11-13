"""Clean-source gloss,English and editorial reasons:B109-B110."""
SPEECH = {
(109,7): ("The voice addresses the Colosseum visitor and commands an answer to its question.", "Visitor to the Colosseum, answer my question!", "Restore a natural complete ritual address with the article, keeping the FE voice anonymous."),
(109,10): ("Lil asks what is happening.", "Huh? What's going on?", "Retain her natural confused reaction before the riddle begins."),
(109,13): ("The voice introduces its question.", "Here is my question.", "Replace the clipped label Question with spoken English; the source's leading blank lines are vertical staging, not an English pause requiring manual breaks."),
(109,17): ("The strange bean doubles each second:two after one second,four after two,eight after three.", "A magic bean doubles each second: two after one, four after two, eight after three.", "Retain the complete doubling rule and 1/2/3-to-2/4/8 sequence; the opening establishes seconds for all examples without correcting the fictional premise."),
(109,21): ("One bean fills a bag after sixty seconds; starting with two asks how many seconds it takes to fill.", "A bag fills in 60 seconds if I put one bean inside. How many seconds would it take if I started with two?", "Make the initial two-bean condition and seconds explicit without changing the capacity or doubling rule."),
(109,24): ("The voice orders them to choose among the following answers.", "Choose your answer!", "Retain the natural instruction immediately before the three-option menu; do not copy source-leading staging breaks."),
(109,225): ("Without Camille's solution,Lil tentatively guesses fifty-nine seconds.", "...Fifty-nine seconds, maybe...", "Restore spoken units instead of sec and keep her uncertainty; do not make her confidently calculate the right answer."),
(109,256): ("Lil awkwardly agrees when the companion asks whether she worked it out.", "Uh, yeah...", "Retain the evasive, hesitant agreement after her uncertain guess."),
(109,262): ("Camille suddenly realizes the solution.", "Oh, of course!", "Retain the spontaneous realization in the distinct Camille-present branch."),
(109,266): ("Lil is excited that Camille figured it out and praises him.", "You figured it out?! Nice work, Camille!", "Retain the complete effective runtime replacement with the approved Camille name, not the shorter Kamil storage key; the praise adds no relationship."),
(109,269): ("Camille gives the answer,fifty-nine seconds.", "The answer's 59 seconds!", "Use a natural spoken sentence rather than the clipped Answer label, preserving the correct number and unit."),
(109,273): ("Lil stammers that she too was just thinking that very thing.", "I-I was just thinking that myself!", "Restore her flustered claim of simultaneous realization, not an earlier confident guess."),
(109,279): ("The voice praises the one with wisdom and courage and grants a gift.", "Well done! You possess wisdom and courage. Accept this gift!", "Restore both qualities and remove the invented hero label; keep the gift conditional and the Golden Dividers name out of spoken source that only says this."),
(109,292): ("Lil is relieved and calls it lucky.", "Phew, that was lucky!", "Express her relief as natural spoken English while preserving the lucky-guess branch."),
(109,298): ("Lil tells Camille he is reliable.", "I can count on you, Camille!", "Retain the effective registered runtime wording and approved name; its warmth matches her source praise without new romance or kinship."),
(109,302): ("Camille confidently accepts the praise.", "You bet!", "Retain the natural confident reply closing the successful Camille-present exchange."),
(110,33): ("A stone tablet shaped like a jar is embedded here.", "A jar-shaped stone tablet is embedded here.", "Restore stone and embedded while avoiding an invented wall,floor or new artifact name."),
(110,36): ("The inscription addresses the traveler and says to pour from the sacred jar using the left hand.", "Traveler, pour from the sacred jar with your left hand.", "Preserve the traveler address and the left-hand clue; do not identify the jar-shaped mechanism as the Starlight Globe reward."),
(110,39): ("Lil puzzles over the instruction to pour from the jar with the left hand.", "Pour from the jar... with my left hand?", "Restore the jar/pouring context and hesitation under the original CF captain selector."),
(110,60): ("Lil reacts with sudden alarm in the push branch.", "!!", "Retain the wordless reaction in its original branch; do not invent a voiced explanation or a casualty."),
(110,66): ("She reasons that pouring with the left hand should tip the jar to the right.", "If I pour with my left hand, the jar should tilt to the right...", "Preserve the inferred rightward tilt and should; do not swap the successful right-turn and failed left-turn answers."),
(110,70): ("Lil reacts to the mechanism in the right-turn branch.", "!!", "Retain the brief source reaction without naming or explaining the mechanism's effect."),
(110,82): ("Lil reacts with sudden alarm in the other failed mechanism branch.", "!!", "Retain this separately stored reaction before the danger sequence; do not merge source branches."),
(110,89): ("Lil screams and urgently tells everyone to run.", "Aah! R-run!", "Keep the panic and stammer in a natural escape cry without claiming the party has already escaped."),
(110,93): ("The retainer cries out in pain or alarm.", "Aaah!", "Retain the cry without inventing death,identity or a particular injury."),
(110,100): ("The system reports injuries among the sailors.", "Sailors were injured!", "Keep the unmarked group injury notice without inventing one fixed casualty count or deaths; this is conditional script text,not earned current damage.")
}

# Both wrong-answer branches are complete parallel exchanges with distinct answers.
for prompt,answer,praise,boast,reject,question,hunch,number in [
    (76,82,93,96,103,115,118,'one second'),
    (165,171,182,185,192,204,207,'thirty seconds')
]:
    SPEECH[109,prompt] = ("Camille says the problem is difficult and asks FI for her thoughts before the "+number+" answer.", "This is a tough one. What do you think, {MACRO:FI}?", "Restore a complete natural question and preserve the source FI substitution in this separate "+number+" branch.")
    SPEECH[109,answer] = ("Lil laughs confidently,tells them to leave it to her,and announces the wrong answer "+number+".", "Hee hee! Leave it to me! The answer is "+number+"!", "Restore her playful laugh and confidence while preserving the deliberately wrong "+number+" answer; do not correct the joke into fifty-nine seconds.")
    SPEECH[109,praise] = ("Camille is impressed by Lil's confidence and believes she is sure of this answer.", "Wow, you're sure of yourself!", "Retain the natural impressed response before her boast in the "+number+" branch; it conveys confidence without inventing skepticism.")
    SPEECH[109,boast] = ("Lil boasts that she has both intelligence and beauty.", "I've got brains and beauty!", "Restore her complete self-congratulatory sentence before the "+number+" answer is rejected.")
    SPEECH[109,reject] = ("The voice calls her foolish after the wrong "+number+" answer.", "You fool!", "Retain the source insult in this separate failed-answer branch; no added punishment or death is asserted.")
    SPEECH[109,question] = ("Camille asks what made her so confident after the "+number+" failure.", "So... what made you so sure?", "Retain the natural follow-up that sets up the admission of a hunch in this branch.")
    SPEECH[109,hunch] = ("Lil admits the "+number+" answer was only a hunch.", "Just a hunch.", "Retain the short deflating admission after Camille's question; do not turn it into an actual calculation.")

VOICE = {
(109,442,20): ("The polite companion asks the admiral what she thinks and admits not understanding.", "What do you think, Admiral? I'm completely lost...", "Restore the question and complete admission for voice0 before the one-second guess."),
(109,442,56): ("The formal companion finds the problem difficult and does not know the answer.", "This is... difficult. I don't know the answer.", "Restore voice1's measured hesitation and a complete sentence before the one-second guess."),
(109,442,84): ("The casual companion is stumped and has no idea.", "I'm stumped... I have no idea.", "Keep the casual admission of defeat for voice2 rather than two generic labels."),
(109,442,114): ("The feminine-style companion gives up,not understanding at all.", "It's no use... I have no idea at all.", "Restore a natural frustrated thought for voice3 without inventing a named speaker."),
(109,442,144): ("The rough companion wonders what the riddle means.", "Hmm... What's all that supposed to mean?", "Restore the thinking sound and colloquial voice4 question."),
(109,442,168): ("The older-sounding companion wonders what it all means.", "Hmm... Now, what does that mean?", "Give voice5 a natural reflective cadence without invented kinship or accent."),
(109,442,194): ("The youthful companion is utterly bewildered.", "????", "Retain all four source question marks as the intended wordless comic reaction; do not invent understanding."),
(109,442,204): ("The formal older-style companion finds the question difficult.", "Hmm. This is a difficult one.", "Restore a complete measured thought for voice7 instead of a generic clipped phrase."),
(109,1016,20): ("The polite companion asks the admiral what she thinks and admits not understanding.", "What do you think, Admiral? I'm completely lost...", "Restore the full voice0 exchange in the separate thirty-second branch; the same source wording warrants the same English."),
(109,1016,56): ("The formal companion finds it difficult and does not know.", "This is... difficult. I don't know the answer.", "Restore the measured voice1 thought in the distinct thirty-second branch."),
(109,1016,86): ("The casual companion gives up and has no idea.", "...I give up. I haven't a clue.", "Keep the explicit surrender and initial pause for voice2,distinct from the earlier stumped reaction."),
(109,1016,112): ("The feminine-style companion finds it hopeless and has no idea.", "...It's no use. I have no idea at all.", "Keep the source pause and frustration for voice3 in the separate wrong-answer branch."),
(109,1016,140): ("The rough companion wonders what the riddle means.", "Hmm... What's all that supposed to mean?", "Retain the complete voice4 intent and reuse the faithful wording for identical source in this distinct branch."),
(109,1016,164): ("The older-sounding companion wonders what it means.", "Hmm... Now, what does that mean?", "Preserve voice5's reflective cadence in this separate branch without inventing a relationship."),
(109,1016,190): ("The youthful companion is utterly bewildered.", "????", "Retain the source's four question marks separately in the thirty-second branch; the reaction does not imply a spoken solution."),
(109,1016,200): ("The formal older-style companion calls it a difficult problem.", "Hmm. This is quite a difficult question.", "Preserve voice7's measured formality and the source's hard-question wording."),
(109,1610,20): ("The polite companion asks whether the admiral calculated the answer.", "Did you do the math, Admiral?", "Restore the calculation question,important to Lil's ensuing awkward agreement,for voice0."),
(109,1610,46): ("The formal companion politely asks whether the admiral calculated the answer.", "Have you calculated the answer, Admiral?", "Keep voice1's respectful,measured question and the distinction between calculation and guessing."),
(109,1610,74): ("The casual companion excitedly asks whether she solved it.", "You solved it?!", "Retain the natural excited question for voice2; the source address is clear from the exchange."),
(109,1610,96): ("The feminine-style companion asks whether she figured it out.", "You solved it?", "Retain the natural understated question for voice3,distinct from the excited voice2 punctuation."),
(109,1610,116): ("The rough companion is surprised that she calculated it.", "You did the math?!", "Restore the source calculation nuance and rough surprise for voice4."),
(109,1610,140): ("The older-sounding companion is surprised and asks whether she solved it.", "Oh! You worked it out?", "Restore the source noticing exclamation and reflective voice5 question."),
(109,1610,162): ("The youthful companion is impressed that she solved it.", "Wow, you solved it!", "Retain the source's enthusiastic praise for voice6 without inventing how she reached the answer."),
(109,1610,192): ("The formal older-style companion confirms that she found the answer.", "Ah, you have the answer, then?", "Restore voice7's polite confirming register rather than making every style identical."),
(110,16,20): ("The polite companion informs the admiral of a dead end.", "Admiral, it's a dead end.", "Restore a complete natural report for voice0 without adding a route or destination."),
(110,16,44): ("The formal companion reports a dead end to the admiral.", "Admiral, it's a dead end.", "Restore the complete measured voice1 report; equivalent source does not require gratuitous synonyms."),
(110,16,66): ("The casual companion notices a dead end.", "Huh, a dead end.", "Retain the natural casual noticing fragment for voice2; it already carries the whole source intent."),
(110,16,90): ("The feminine-style companion tells the admiral they have reached a dead end.", "Admiral, we've reached a dead end.", "Restore a complete voice3 observation without inventing uncertainty about the visible obstacle."),
(110,16,112): ("The rough companion notices the dead end and reacts.", "Whoa, it's a dead end.", "Use a natural voice4 noticing sound without implying they made a navigational mistake."),
(110,16,136): ("The older-sounding companion tells the admiral they are at a dead end.", "Well, Admiral, we've come to a dead end.", "Preserve voice5's reflective older register without kinship terms."),
(110,16,162): ("The youthful companion calls the admiral's attention to the dead end.", "Admiral! It's a dead end!", "Restore a complete excited observation for voice6 rather than a clipped label."),
(110,16,190): ("The formal older-style companion mildly reacts to the dead end.", "Oh my, a dead end.", "Retain the natural mild exclamation already suitable for voice7.")
}

CHOICES = {
(109,384,0): ("The player answers one second.", "1 second", "Spell out the unit for natural player-facing text while preserving the first wrong answer and index0."),
(109,384,1): ("The player answers thirty seconds.", "30 seconds", "Restore the complete unit and preserve the second wrong answer at index1."),
(109,384,2): ("The player answers fifty-nine seconds.", "59 seconds", "Restore the full unit and preserve the correct answer at index2; do not move it ahead of the wrong choices."),
(110,336,0): ("The player pushes the mechanism.", "Push", "Retain the clear action and original result index0."),
(110,336,1): ("The player turns the mechanism right.", "Turn right", "Restore the turning action rather than an unexplained direction; keep correct index1 despite the clue's left-hand wording."),
(110,336,2): ("The player turns the mechanism left.", "Turn left", "Restore the turning action and preserve failed index2,without changing the riddle's logic.")
}
