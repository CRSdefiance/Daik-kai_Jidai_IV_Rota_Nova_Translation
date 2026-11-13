"""Clean-source gloss,English and individual editorial reasons: B101-B105."""
SPEECH = {
(101,5): ("The priest asks whether the party is seeking the Proof of Conquest.", "Do you seek the Proof of Conquest?", "Retain the solemn opening question: its direct address and established title convey the priest's tentative identification without new lore."),
(101,14): ("Lil reacts with a puzzled question.", "?", "Retain the source's wordless puzzled reaction; do not invent an explanation or a spoken reply."),
(101,18): ("The priest wonders if he was mistaken.", "Perhaps I was mistaken...", "Restore his uncertainty; the preceding puzzled reaction does not establish that he definitely made a mistake."),
(101,22): ("Lil stops him to ask what the Proof of Conquest means.", "Wait. What's the Proof of Conquest?", "Retain the natural interruption and question; the established title and Lil's curiosity already match the exchange."),
(101,25): ("The priest says the object is said to come into the hands of whoever rules the seas.", "...It's said to come into the hands of the one who rules the seas.", "Restore the source's hearsay rather than declaring an established prize or guaranteed reward."),
(101,29): ("Lil repeats the idea of ruling the seas and finds it exciting.", "Rule the seas? Sounds fun!", "Retain the lively, idiomatic reaction; the question and enthusiastic reply preserve her playful interest."),
(101,39): ("Lil eagerly asks for more details.", "Come on, tell us more!", "Retain the informal eager request, distinct from Camille's polite alternative."),
(101,45): ("Camille politely asks whether the priest could explain further.", "Could you tell us more, please?", "Retain the courteous complete question; its register distinguishes Camille from Lil without invented status."),
(101,54): ("Lil reacts with surprise and asks Father whether he knows something about the Proof.", "Huh? Father, do you know something about it?", "Restore the religious address to the source priest; Father expresses his role and does not invent kinship or make Camille a priest."),
(101,60): ("The priest warns that finding the Proof is difficult and he will not tell the halfhearted; he asks whether they have the resolve.", "Finding the Proof is no easy task. I will not speak of it to those who lack resolve. Are you prepared?", "Preserve the priest's explicit refusal and challenge, not just a vague demand for readiness."),
(101,64): ("Lil says to leave it to her; despite appearances, once she decides to do something she never gives up.", "You bet! I may not look it, but once I've made up my mind, I never quit!", "Restore the playful contrast with her appearance while keeping her determined, confident voice."),
(101,68): ("The priest accepts their resolve.", "Very well.", "Retain the measured acceptance after Lil's promise; its short form gives the exchange a natural turn."),
(101,72): ("He knows that the map to the Proof becomes useful only after its two Map Keys are combined.", "The Proof's map only works when its two Map Keys are joined.", "Retain the complete two-key condition; it does not imply that either key alone gives a usable map."),
(101,76): ("Each key has no meaning on its own.", "Each key means nothing on its own.", "Retain the clear follow-up reinforcing the preceding two-key requirement."),
(101,79): ("They may already have noticed: Map Keys may be hidden in ruins or held by unexpected people.", "You may have noticed already: Map Keys can be hidden in ruins or held by people you'd never suspect...", "Restore his acknowledgment of what they may know; preserve the alternatives and uncertainty rather than a guaranteed location."),
(101,82): ("Lil pauses silently.", "...", "Retain the deliberate pause before the priest offers the sword; no invented response is needed."),
(101,86): ("The priest offers them a sword.", "Take this sword.", "Retain the natural gift instruction; do not insert the Laocoon Sword UI name where the spoken source only says a sword."),
(101,93): ("They should overcome the trials set before them and help those in difficulty.", "Overcome the trials ahead. Help those in need.", "Retain the priest's concise moral instruction and its two distinct duties."),
(101,96): ("Do not be captive to greed; give to those without wealth, stop the source of strife, and bring peace widely.", "Do not let greed rule you. Give to the poor, put an end to the source of strife, and bring peace far and wide.", "Restore stopping the source of conflict as well as charity and broad peace; keep this as the priest's counsel, not a new gameplay condition."),
(101,100): ("The priest wishes God's protection upon the party.", "May God watch over you.", "Retain the natural religious blessing, preserving the source's faith and respectful tone."),
(102,7): ("Donna stops the travelers and asks whether they have visited Santiago Cathedral.", "Wait! Have you visited Santiago Cathedral?", "Retain the complete, friendly question and exact registered cathedral name."),
(102,11): ("Lil reacts with a puzzled question.", "?", "Retain the source's brief puzzled reaction between Donna's invitation and explanation."),
(102,15): ("People from across Europe have made pilgrimages there since old times; it is a famous place.", "People from all over Europe have made pilgrimages there for ages. It's quite famous.", "Preserve the pilgrims' origins and use there rather than inventing that Donna is already at the cathedral."),
(102,19): ("She suggests a visit while they are in Seville and offers directions.", "Why not visit while you're in Seville? I'll give you directions.", "Keep the invitation and offer of directions; do not imply that she personally escorts the party."),
(103,5): ("The priest identifies them as pilgrims and asks each to accept a commemorative cross.", "You're pilgrims, aren't you? Please, accept these crosses as a memento of your visit.", "Translate the still-Japanese passage in full, retaining the welcome and commemorative purpose without inserting the item name."),
(103,9): ("He leads a prayer in the name of the Father, the Son and the Holy Spirit, ending with Amen.", "Let us pray. In the name of the Father, and of the Son, and of the Holy Spirit... Amen.", "Use the recognizable Christian prayer formula respectfully; the surrounding religious context establishes Holy Spirit despite the Japanese orthography."),
(103,13): ("Lil notices that everyone else's cross seems newer than hers.", "Why is my cross older than theirs?", "Retain the natural puzzled comparison, which prepares the companion's color observation and her complaint."),
(103,38): ("Lil complains that it is unfair.", "No fair!", "Retain her youthful pout immediately after the companion confirms the difference."),
(103,42): ("She reconsiders that being so old may actually give it an understated stylish charm.", "...Still, maybe it's kind of classy because it's so old.", "Preserve the change of heart and uncertainty; the appeal comes from its age, not power, value or a new religious history."),
(104,29): ("The anonymous voice addresses whoever has visited the temple.", "Visitor to this temple...", "Restore the temple address; keep the ritual FE voice unlabeled and do not invent a deity."),
(104,33): ("Lil is startled that the object spoke.", "Whoa, it talks?!", "Retain the idiomatic surprised response, without naming the object or adding an explanation."),
(104,37): ("The voice lends its power and urges them to engage freely in debate.", "I shall lend you my power. Debate freely.", "Preserve lending rather than permanent bestowal, and retain debate rather than changing it into combat or a stat effect."),
(105,5): ("Lil marvels at how large the object is.", "Whoa, it's huge!", "Retain the lively astonishment before the unseen voice speaks."),
(105,10): ("The Sphinx commands them to answer its question.", "Answer me.", "Retain the terse imperious command; the speaker is identified in source choices but receives no invented visible label."),
(105,14): ("Lil cries out and asks who is speaking.", "Ah! Who's there?!", "Retain the startled complete response to the sudden voice."),
(105,20): ("What animal has four legs in the morning, two at noon and three in the evening?", "Tell me: What animal walks on four legs in the morning, two at noon, and three in the evening?", "Restore the full spoken riddle and the source morning/noon/evening sequence; do not replace these with narrower dawn/dusk wording."),
(105,76): ("The Sphinx asks which animal it is.", "Name the animal.", "Retain the firm follow-up after the player claims to know; the next three options provide the answer."),
(105,132): ("The old, overused riddle is boring; the Sphinx asks another question.", "That old riddle bores me... Here's one more.", "Retain the dismissive switch that prompts Lil's accusation of unfairness."),
(105,135): ("Lil objects that changing the question is unfair.", "No fair!", "Retain the immediate indignant reaction; its repetition elsewhere is separately source-owned."),
(105,139): ("The Sphinx pauses silently.", "...", "Retain the intentional wordless beat after Lil objects."),
(105,143): ("There are ten adults and babies altogether; with thirty-two hands and feet touching the floor, how many are babies?", "There are ten people in all, adults and babies. If 32 hands and feet touch the floor, how many are babies?", "Keep the total ten, both age groups and thirty-two floor-contact limbs; do not imply ten adults plus extra babies or thirty-two feet."),
(105,198): ("Lil hesitates while thinking.", "Um...", "Retain her hesitation before Camille's optional guidance and her calculation."),
(105,213): ("Camille tells FI to calm down and suggests starting with the number of feet on the floor.", "{MACRO:FI}, calm down. Let's start by counting the feet on the floor.", "Keep the source FI substitution and Camille's collaborative guidance rather than only ordering Lil to count."),
(105,220): ("Ten people's feet should total twenty; Lil seeks confirmation.", "Ten people have 20 feet, right?", "Retain the correct intermediate number and her uncertain confirmation question."),
(105,231): ("Camille suggests subtracting the twenty feet from thirty-two.", "Subtract those 20 feet from 32...", "Use natural spoken arithmetic while keeping the source units and unfinished reasoning."),
(105,238): ("Twelve hands remain on the floor; Lil realizes that this means six babies.", "That leaves 12 hands on the floor... I've got it! There are six babies!", "Restore her excited realization as well as the complete calculation, preserving all numbers."),
(105,250): ("Camille is impressed.", "Wow!", "Retain the warm, spontaneous praise after Lil solves the riddle."),
(105,259): ("The Sphinx praises the wise one and tells them to accept the gift.", "Wise one! Take this reward!", "Retain the solemn conditional praise and gift, without naming the Crescent Shotel in spoken text or claiming it was earned in current gameplay.")
}

VOICE = {
(103,208,20): ("The polite companion asks what is wrong, then confirms the admiral's cross alone has a wholly different color.", "What's wrong? Oh, you're right. Your cross is a completely different color from ours, Admiral...", "Restore both conversational turns and the address for voice0; do not leave only the color observation."),
(103,208,74): ("The formal companion asks what is wrong and confirms that only the admiral's cross has a different color.", "Is something wrong? Ah, you're right. Your cross is an entirely different color, Admiral...", "Keep the measured register shared by source styles1/7 and preserve their original alias."),
(103,208,130): ("The casual companion asks what is wrong and agrees the admiral's cross is a different color.", "What's the matter? Oh, you're right. Yours is a completely different color, Admiral...", "Restore question and realization in a natural casual form shared by source styles2/3; do not add gendered or relationship wording."),
(103,208,180): ("The colloquial companion asks what is wrong, realizes the difference and points out the admiral's cross color.", "What's wrong? Huh, you're right. Your cross is a totally different color, Admiral...", "Use a relaxed voice4 realization while keeping the entire exchange."),
(103,208,234): ("The older-sounding companion asks what is wrong and then agrees about the admiral's different cross.", "What's the matter? Well, I'll be. Your cross is a whole different color, Admiral...", "Localize the older turns of phrase naturally for voice5 without adding kinship or an accent stereotype."),
(103,208,298): ("The youthful companion asks what is wrong and enthusiastically realizes the cross color differs.", "What's wrong? Ohhh, you're right! Yours is a totally different color, Admiral...", "Retain the source's drawn-out realization and youthful energy for voice6 without invented baby talk."),
(104,10,20): ("The companion politely asks the admiral to look at the object.", "Admiral, take a look!", "Retain the natural request already suitable for shared source styles0/1 and preserve their alias."),
(104,10,48): ("The casual companion calls the admiral's attention to the object.", "Admiral, look!", "Retain the concise, excited request shared by source styles2/3; the object is clear from the scene."),
(104,10,68): ("The colloquial companion asks the admiral to look at this.", "Admiral, look at this!", "Retain the complete natural voice4 request and source address."),
(104,10,94): ("The older-sounding companion calls the admiral's attention here.", "Admiral, look here!", "Retain the natural older register; it calls attention to the displayed object without invented information."),
(104,10,120): ("The youthful companion eagerly calls the admiral's attention to the object.", "Admiral! Look!", "Retain the excited short calls for voice6; they preserve the drawn-out attention-seeking effect."),
(104,10,146): ("The formal companion politely asks the admiral to examine this.", "Admiral, please have a look at this.", "Replace grandiose behold with the source's respectful request for voice7.")
}

CHOICES = {
(105,186,0): ("The player says they know the riddle's answer.", "I know.", "Restore a natural first-person reply rather than the ambiguous fragment Know it; keep result index0."),
(105,186,1): ("The player admits not knowing.", "No clue", "Retain Lil's natural colloquial admission; the menu context supplies the omitted subject and preserves result index1."),
(105,186,2): ("The player denies that such an animal exists.", "There's no such animal.", "Keep the full denial and the source's generic animal, without changing the third result."),
(105,424,0): ("The player identifies themselves, humans, as the animal.", "Us (humans)", "Restore the source's self-identification and parenthetical explanation; retain index0."),
(105,424,1): ("The player identifies the addressed Sphinx as the animal.", "You (the Sphinx)", "Restore the explicit source Sphinx identification and index1 rather than leaving an unexplained You."),
(105,424,2): ("The player proposes a different animal.", "Other", "Retain the natural compact menu category; the prompt makes the referent clear and index2 remains unchanged."),
(105,842,0): ("The player answers four babies.", "4", "Retain the exact quantity and index0; the immediate question supplies babies, so no extra label is needed."),
(105,842,1): ("The player answers five babies.", "5", "Retain the exact quantity and index1; the immediate question supplies babies."),
(105,842,2): ("The player answers six babies.", "6", "Retain the correct quantity and index2; do not reorder the answers or imply current earned success.")
}

FAILURES = [(43,47,'denying knowledge'),(59,63,'denying that such an animal exists'),(99,103,'answering the Sphinx'),(115,119,'answering other'),(163,167,'answering four babies'),(179,183,'answering five babies')]
for banish,cry,reason in FAILURES:
    SPEECH[105,banish] = ("After "+reason+", the Sphinx calls the answerer foolish and orders them to leave.", "Begone, fool!", "Retain the imperious insult and dismissal in this separate failure branch for "+reason+"; repetition is source-owned.")
    SPEECH[105,cry] = ("Lil cries out in alarm after the banishment for "+reason+".", "Aah!", "Retain the startled cry tied to "+reason+"; CF is the native captain selector, not an invented victim or death.")
