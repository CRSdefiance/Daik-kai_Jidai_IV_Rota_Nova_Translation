"""Review Kublai Khan's prophecy, Janus's letter, and the Avalon leads."""

from scripts import pair_hodram_B201_B220_20261122 as paired
from scripts import review_hodram_B211_B216_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B217_B220_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    217: "An older man recognizes something Hodram is carrying. He tells the story handed down from a retainer of Kublai Khan and sees Hodram as the seafarer in its prophecy. Hodram scoffs, but the older man gives him the clue to the emperor's greatsword.",
    218: "A crew member announces Janus's letter using one of the native personality voices. Janus relates a rumor about Judas's sword and argues that its origin need not make it worthless. Hodram recognizes Janus's practical point and Manuel gives his own response.",
    219: "A hostile merchant tries to drive away a woman asking about a king. She introduces herself as Vivienne and urges Hodram to seek Excalibur in Avalon. Hodram does not recognize the place, and Gerhard suggests asking at the tavern.",
    220: "The Avalon lead continues at the tavern. The barkeep is tired of hearing about Vivienne and dismisses the story of King Arthur. He still passes along the rumor that Avalon is just west of town.",
}
DECISIONS = {
    217: """
5|||The older man catches Hodram's attention respectfully. The brief greeting fits his first approach.
9|||Hodram checks whether the stranger is addressing him. The hesitation preserves his surprise.
13|||The older man asks to see a particular object. The phrasing keeps the request courteous and leaves the item implicit.
16|||Hodram echoes the reference because he is unsure what the man means.
20|||The older man confirms which thing he wants to examine. Keep the brief response before his recognition.
24|Hmm... There's no mistake. Just as the story says.|There's no mistake.;Just as the story says.|The older man recognizes what he sees as matching an account handed down to him. Calling it a story leads into his telling of it.
27|||Hodram's wordless question shows that he has no explanation yet. The source punctuation preserves that beat.
31|||The older man puts Kublai Khan's rule of the mainland more than 300 years earlier. His praise opens the account of the emperor.
35|But the day came when even that great emperor had to leave this world...|that great emperor;leave this world...|The older man marks the approach of the emperor's death and lets the thought hang before quoting him.
38|The emperor told his retainer, "Two hundred years from now, a ruler of the oceans shall come to this land.|Two hundred years from now,;a ruler of the oceans;come to this land.|The opening of the prophecy fixes the exact span and the expected arrival. Keep the quote open through the next paragraph.
42|"The king of the seas shall command many foreigners and bring a gold seal from a land I could never rule. Give my sword to that hero."|king of the seas;bring a gold seal;from a land;Give my sword|The emperor identifies the ruler, the people under him and the gold seal. The last instruction gives the sword to that same person. The quote closes here.
45|That retainer was our ancestor. We've been waiting for the king of the seas ever since...|was our ancestor.;king of the seas;ever since...|The older man identifies his own clan as descendants of the retainer. The long wait leads directly to his recognition of Hodram.
48|And today, you've come at last. Ruler of the oceans, we've been waiting for you.|you've come at last.;Ruler of the oceans,;waiting for you.|The older man turns his ancestor's story into a direct greeting. The address and repeated wait preserve the moment of recognition.
52|Me? Come on, old man. I'm nobody that important.|Come on, old man.;nobody that important.|Hodram reacts with disbelief and downplays his own importance. His familiar address is directed to the older man.
56|||The older man insists he is certain and identifies Hodram as the Sea King. The certainty belongs to his belief about the prophecy.
59|||The older man tells Hodram where to search for the emperor's greatsword. His expectation of finding it remains prospective.
62|||The older man entrusts the sword to Hodram and takes his leave. The words follow the clue without producing a physical handover.
""",
    218: """
SC1_B218_STYLE_8_0|||This speaker gives the captain a simple update about the incoming letter. Janus remains the sender.
SC1_B218_STYLE_8_40|Admiral, correspondence has arrived from Janus.|correspondence has arrived;from Janus.|The formal voice uses the more ceremonious noun for the letter. Match the register of the same voice in Yukihisa's scene.
SC1_B218_STYLE_8_82|Admiral, there's a letter from Janus.|there's a letter;from Janus.|The plainspoken version announces the same sender and keeps the captain's form of address.
SC1_B218_STYLE_8_120|||This alternative puts the letter first and uses the personal address at the end. The existing wording fits its warm delivery.
SC1_B218_STYLE_8_150|Letter from Janus for you, Admiral.|Letter from Janus;for you, Admiral.|The rough voice delivers the news briskly. The sender and recipient remain clear.
SC1_B218_STYLE_8_188|Admiral, a letter's come from Janus.|a letter's come;from Janus.|This voice announces the arrival in an established familiar construction and names the writer.
SC1_B218_STYLE_8_224|||The eager call suits the speaker's enthusiasm. The source still assigns the identity dynamically.
34|||Janus opens his letter to the admiral and says he is writing from a road leading to Rome. The existing opening has a natural written register.
38|Walking this road, I keep hearing stories about the missionaries who endured persecution long ago and went on spreading their faith.|I keep hearing stories;who endured persecution;spreading their faith.|Janus cannot help hearing about the older missionaries. Keep the persecution they endured and their continuing work in the account.
41|||Janus says religion is of little interest to him but that one story caught his attention. The existing words explain why he continued listening.
44|It seems a sword once carried by Judas, one of Jesus's twelve disciples, may still lie in a place associated with him.|once carried by Judas,;Jesus's twelve disciples,;associated with him.|Janus reports a rumor about a sword that may remain in a place linked to Judas. The source identifies Judas as one of the twelve.
48|Judas betrayed Jesus. People find the sword unsettling just because it belonged to him, so no one wants to claim it.|Judas betrayed Jesus.;find the sword unsettling;wants to claim it.|Janus explains both the reputation and its effect on prospective owners. This is the account he heard.
51|Still, I hear it's a fine blade with a keen edge. The sword bears no guilt itself. I think it would be worth looking for.|a fine blade;with a keen edge.;bears no guilt itself.;worth looking for.|Janus praises the rumored quality and separates the sword's merits from its owner. His conclusion is a practical suggestion about searching.
62|Of course, I doubt Manuel would care for this story, devout as he is.|care for this story,;devout as he is.|Janus expects Manuel to dislike the story because of his faith. The expectation sets up Manuel's more nuanced response.
68|||Janus promises to write again if he learns anything else. Keep the approved signature and the letter's closing beat.
75|A traitor's sword... If it's a fine blade, its origins don't matter to him. Practical as ever, Janus.|A traitor's sword...;its origins don't matter;Practical as ever, Janus.|Hodram recognizes Janus's practical reasoning about the sword. His reaction retains both the loaded description and the distinction Janus makes.
87|...Well, I wouldn't rule it out entirely. Judas did repent in the end, after all. I'll leave the decision to you, Admiral.|wouldn't rule it out entirely.;repent in the end,;the decision to you, Admiral.|Manuel says his objection is less absolute than Janus expected. He gives his own account of Judas's repentance and leaves the decision to the admiral.
""",
    219: """
5|||The woman asks where the king is. Her trailing delivery suits the repeated question that gets the merchant's attention.
9|||The merchant blames her for interfering with business and angrily tells her to leave. The existing insult sounds like a merchant losing patience.
13|Where is the king...? Where is the hero who shall bear the sword...?|Where is the king...?;shall bear the sword...?|The woman asks again about the king and adds her search for the hero who is to bear the sword. The double question keeps the two people distinct.
16|...What's wrong? Who are you?|What's wrong?;Who are you?|Hodram asks what is happening and who she is. His pause suits the interruption of the disturbance.
19|||She gives her name as Vivienne and claims to have made King Arthur's sacred sword. Preserve the established name and the uncertainty created by her speech.
22|||Hodram echoes the name in surprise. The famous name leads to her account of the king and sword.
26|The king has gone to sleep... Yet the sacred sword still seeks a hero...|has gone to sleep...;still seeks a hero...|Vivienne says the king has gone to sleep and that the sword is still seeking a hero. Preserve her mysterious delivery and the sword's continuing search.
29|Seek the sacred sword Excalibur, hero! It is calling to you from Avalon, where the king sleeps!|the sacred sword Excalibur,;calling to you from Avalon,;where the king sleeps!|Vivienne names the sword and urges Hodram to find it in Avalon. Her certainty that it seeks him belongs to her claim.
32|||Hodram does not recognize Avalon. The direct response prompts Gerhard's suggestion.
36|Someone at the tavern might know where it is.|might know where it is.|Gerhard suggests the tavern as a place to ask. He offers a possible lead rather than a definite location.
""",
    220: """
5|Barkeep, have you heard of Avalon?|heard of Avalon?|Hodram follows Gerhard's suggestion and asks the barkeep about the place. Use the established role in his address.
8|Again? Don't tell me you believe that nonsense from the woman who calls herself a witch.|Don't tell me;woman who calls herself;a witch.|The barkeep is tired of the question and disbelieves the woman's account. The title witch is presented as her claim.
12|||The barkeep conveys the rumor about Avalon lying immediately west of town. The uncertainty stays in his reply.
16|King Arthur's a fairy tale. People keep asking me about Avalon, but I've never heard of anyone finding it.|King Arthur's a fairy tale.;asking me about Avalon,;anyone finding it.|The barkeep dismisses the story and comments on repeated inquiries. He only claims that he has never heard of a successful search.
""",
}

review = checked_text(previous.review, {"len(records) == 93": "len(records) == 48"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::prophecy-and-avalon", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
