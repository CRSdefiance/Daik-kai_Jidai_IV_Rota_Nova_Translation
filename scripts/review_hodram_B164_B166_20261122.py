"""Review the two port reports and Jam's return with the missing ship."""

from scripts import review_hodram_B161_B163_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B164_B166_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    164: "The port worker tells the crew the missing ship has apparently yet to return. This is a separate script from the identical alternative report.",
    165: "The alternate port report gives the same negative result while the crew is waiting.",
    166: "The port worker spots the missing ship. Jam claims he rescued an abandoned ship and boasts that he taught himself to sail it. Gerhard is furious, Charles is baffled, and Hodram sees promise in him. Jam turns his answer to the invitation into a joke and gives his full name.",
}
DECISIONS = {
    164: """
6|Looks like it isn't back yet.|isn't back yet.|The worker reports that the ship still appears to be missing. Retain the uncertainty before the positive sighting.
""",
    165: """
6|Looks like it isn't back yet.|isn't back yet.|The second report has the same source wording and function. Keep the alternative occurrence distinct while matching the worker's voice.
""",
    166: """
5|||The worker repeats the admiral's title in excitement and announces the ship's return. The direct reference to their ship answers the earlier reports.
8|||Hodram repeats the news in disbelief. The concise question gives the worker a chance to point out the ship.
12|||The worker points to the ship and asks for confirmation. The immediate gesture moves the encounter to Jam.
17|Yaaahoo! I love the sea! It's so wide! So huge!|I love the sea!;So huge!|Jam shouts a drawn-out version of his refrain and marvels at the sea's size. The repetition shows how little attention he is paying to the owners' alarm.
21|Whew! I've been having a ball all morning. What a beautiful day! Yahoo!|all morning.;What a beautiful day!|Jam says he has been enjoying himself since morning and celebrates the day. Preserve his breezy refrain and the time he has been out.
24|||Hodram laughs to himself at the kind of person the world can turn up. The dry amusement anticipates his reaction to Jam's story.
28|You there! Who gave you permission to board that ship?!|Who gave you permission;board that ship?!|Gerhard confronts Jam and demands to know who authorized him to board. Keep the direct address and contrast with Jam's casual answer.
31|Huh? What are you talking about? The ship was just lying there!|What are you talking about?;just lying there!|Jam answers as if Gerhard's question makes no sense and insists he found the ship lying there. The absurd claim is in Jam's voice.
34|||Gerhard dismisses the excuse outright. The short indignation leaves Charles the next turn.
46|A ship can't just be lying around in the sea! It's scientifically impossible!|lying around;scientifically impossible!|Charles treats Jam's excuse as a claim about the physical world. Retain the comic incongruity and his habit of appealing to science.
52|||Jam claims he found the ship walking through the port and describes it as abandoned and lonely. His quick insistence keeps the whole account as his own excuse.
56|||Jam congratulates himself on rescuing the ship, spells his given name, and shouts his usual refrain. The spelling stays consistent with his full name later.
59|||Hodram asks whether Jam decided to try sailing it, then how he managed to move it. His interest in the feat leaves the accusation to Gerhard.
63|||Jam gives a comically vague explanation and says he figured it out by feel. The refrain punctuates his boast.
66|||Hodram is already impressed. His understated praise comes before Charles lists what could have gone wrong.
78|||Charles says such a feat is normally impossible and names being lost at sea and running aground. The real risks stay explicit.
84|Tsk, tsk, tsk! Let me teach you a saying. Listen close!|teach you a saying.;Listen close!|Jam clicks his tongue three times and demands attention for a maxim. The colloquial imperative fits his self-appointed authority.
88|||Jam quotes an English equivalent of the Japanese maxim about achieving what you set out to do. His assertion that things are fine if he says so keeps the boast.
99|||Fernando calls the stranger a wild one. His informal aside is distinct from Gerhard's outrage.
106|||Hodram laughs under his breath. His growing amusement sets up Gerhard's loss of patience.
110|What a character! I've had enough of your nonsense!|I've had enough|Gerhard is exasperated and tells Jam to stop fooling around. It does not require a judgment about Jam's intelligence.
113|||Jam announces his own motto about a large, short life. Its intentionally odd wording is what Hodram notices next.
117|(That's not a real proverb...)|not a real proverb...)|Hodram privately observes that Jam has made up the motto. Keep the joke private while Jam keeps explaining it.
121|||Jam rejects the opposite idea of a small, long life, picturing it as keeping one's head down. The punch line stays in plain speech.
124|||Gerhard wants to hand Jam over to the guards and addresses Hodram with the original name substitution. His practical option keeps the decision open.
127|||Hodram says he likes Jam. That short, unexpected judgment sets up the crew's incredulity.
131|W-what are you saying?! Have you lost your mind?|W-what are you saying?!;Have you lost your mind?|Gerhard reacts with a stammer and questions whether Hodram is sane. His alarm is distinct from his earlier indignation at Jam.
135|||Hodram assures Gerhard he is serious and names both the solo sailing and the reckless philosophy as reasons Jam interests him. Preserve both before he makes the invitation.
139|||Gerhard cannot believe where this is going. The unfinished objection leaves Charles to name the possibility.
151|||Charles voices the possibility of recruiting Jam. The tentative question stays separate from Hodram's confirmation.
158|Exactly. Jam, was it? Want to come with us?|Jam, was it?;come with us?|Hodram confirms what the others suspected, checks the given name, and offers Jam a place. The invitation is in his own plain register.
162|Hmm. Should I go or stay? What to do... Just a moment! Give me two seconds to think!|What to do...;Just a moment!;two seconds to think!|Jam plays up his indecision, demands a moment, and specifies two seconds. The time is part of the joke he is preparing.
165|||Jam exclaims that he has made up his mind. The brief shout sets up Hodram's literal question.
169|Made up your mind?|Made up your mind?|Hodram asks whether Jam has decided. His quick practical question keeps the response to the absurd two-second deadline dry.
173|Yep. I'm staying! See ya! Have a good trip!|I'm staying!;Have a good trip!|Jam pretends to refuse and wishes them a good trip. His breezy farewell sets up the joke when Hodram barely reacts.
177|||Hodram says nothing. That exact pause is the reaction Jam complains about in his next turn.
181|||Jam says the joke got too little reaction, tells Hodram twice to stay calm, and reveals he was kidding. The quick reassurance rescues his prank.
185|||Hodram repeats the explanation in disbelief. The single word keeps his dry response before Jam accepts.
189|||Jam asks to come and formally introduces himself again, using the established full name and his usual shout. Preserve the name and the running refrain.
""",
}
review = checked_text(previous.review, {"len(records) == 60": "len(records) == 41"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::the-ship-returns", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

