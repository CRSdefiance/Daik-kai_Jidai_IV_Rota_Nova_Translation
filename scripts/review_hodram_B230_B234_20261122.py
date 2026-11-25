"""Review Yifa and Samwell's exchanges and Carlo's medical-text rumor."""

from scripts import pair_hodram_B221_B240_20261122 as paired
from scripts import review_hodram_B224_B229_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B230_B234_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    230: "Hodram finds Yifa training late. She explains why hesitation in a sword fight is dangerous and mentions a tough martial arts garment. Remembering what her teacher would say, she goes back to training.",
    231: "Samwell asks Hodram about a shield that supposedly uses hard armadillo hide. He thinks it would help in a fight. His clue is too broad for a deliberate search, but Hodram promises to keep it in mind.",
    232: "Samwell repeats much of his armadillo pitch, this time about a giant tortoise shield. Hodram recognizes the repetition before asking where it could be. They still have only a broad region to go on.",
    233: "Samwell describes a helmet supposedly forged in a phoenix's fire. Hodram anticipates his reasoning and expects another vague answer. He is surprised to hear that Samwell narrowed the search to Britain.",
    234: "Carlo tells Hodram that an old text by Herophilus supposedly gives advice for limiting a crew's fatigue. The pair are interested, but Carlo remembers only a broad region and an old sighting.",
}
DECISIONS = {
    230: """
5|||Yifa is already practicing. The two effort sounds let Hodram react to it.
9|You're still training? I wish the marines would take a lesson from you.|still training?;take a lesson from you.|Hodram notices the late hour and admires the example she sets for the marines.
13|||Yifa explains that facing an opponent armed with a sword calls for courage. The simple tag suits her voice.
16|But if you're afraid of the blade and hesitate as you step in, you can get hurt worse. That's why it takes resolve to face your fears.|afraid of the blade;as you step in,;face your fears.|Yifa warns against halfhearted commitment and links it to worse injury. The point is mental resolve.
19|Oh, I heard about a training outfit so tough it can chip a sword that strikes it. Have you heard of it?|a training outfit;chip a sword;Have you heard of it?|Yifa recalls a martial arts garment and describes what it is said to do. The question asks whether Hodram knows of it.
22|||Hodram is intrigued by the claim that striking the outfit might chip a sword.
25|If I had something like that, I could really go all out in a fight...|something like that,;go all out in a fight...|Yifa daydreams about what the clothing might let her do.
28|Oops. My teacher would scold me for relying on gear. 'Train yourself first!' he'd say.|relying on gear.;'Train yourself first!'|Yifa catches herself depending on equipment and imitates her teacher's training instruction.
32|||Yifa returns to practicing. The familiar effort sounds bring the exchange back to its opening.
""",
    231: """
5|||Samwell asks for a moment in a familiar tone. His opening is the cue he repeats with the other clues.
9|||Hodram's brief acknowledgment gives Samwell room to tell him what he heard.
13|I just heard about an animal called an armadillo. Ever heard of one? They say its hide is harder than iron.|an animal called an armadillo.;Ever heard of one?;harder than iron.|Samwell shares the reported property of an unfamiliar animal. Keep the younger man's conversational questions.
17|||Hodram asks Samwell to get to the point. The same prompt is repeated in the tortoise exchange.
21|||Samwell relates the story of a shield made long ago from the hide. Keep the approved item name Armadillo Hide.
24|||Hodram asks why the shield matters. The question is a setup for Samwell's enthusiasm.
28|Come on, keep up! It's a shield harder than iron! Don't you want it? Think how handy it'd be in a fight.|Come on, keep up!;harder than iron!;Don't you want it?;handy it'd be in a fight.|Samwell chides Hodram and repeats the rumored strength before making his pitch. Match its last two sentences to his next shield pitch.
31|||Hodram acknowledges the possible benefit and asks where they would find the shield.
34|Well... All I know is it's hidden somewhere around Africa.|All I know is;somewhere around Africa.|Samwell can name only the region. His hesitation follows the confidence of his pitch.
38|...That's not enough to go looking for it.|not enough;go looking for it.|Hodram explains why the broad region gives them no practical lead.
42|||Samwell agrees while still hoping they might find the shield. The trailing turn leaves room for reassurance.
46|Don't look so disappointed. I'll keep it in mind. With any luck, we'll find it.|look so disappointed.;I'll keep it in mind.;With any luck,|Hodram offers encouragement and promises only to remember the rumor. Keep the same reassurance in the next shield scene.
49|||Samwell accepts the reassurance in a short reply.
""",
    232: """
5|Got a minute, Admiral?|Got a minute, Admiral?|Repeat the original opening of the armadillo exchange so Hodram's recognition has a natural setup.
9|||Hodram gives the same brief acknowledgment as before.
13|I just heard a rumor about a giant tortoise. Ever heard of one? They say its shell is harder than iron.|a giant tortoise.;Ever heard of one?;harder than iron.|Match Samwell's earlier rhythm while preserving the changed animal and its shell.
16|||Hodram repeats his old question, prompting Samwell to explain the item.
20|||Samwell gives the story of how the shell became a shield. Keep the approved Giant Tortoise Shield name.
23|Hm? This sounds familiar... Didn't you say something like that about an armadillo?|This sounds familiar...;about an armadillo?|Hodram recognizes the pattern and points back to the earlier conversation.
27|||Samwell asks whether he said it and casually claims not to remember.
31|||Hodram drops the first objection and asks why the shield matters.
34|||The pitch repeats the last two sentences of Samwell's armadillo pitch. Its echo makes Hodram's next line work.
38|That's exactly what you said about the armadillo shield.|exactly what you said;the armadillo shield.|Hodram catches the repetition for a second time and calls it out directly.
41|Did I? Never mind, never mind.|Never mind, never mind.|Samwell waves off the repetition. The double dismissal is part of his comic evasiveness.
45|||Hodram pauses before asking the same practical question as in the first exchange.
48|||Samwell reports a broad area around the Indian Ocean. He cannot be more specific.
51|That's not enough to go looking for it.|not enough;go looking for it.|Hodram comes to the same conclusion as with the first clue.
55|||Samwell agrees reluctantly. His pause leaves the next turn open to Hodram's reassurance.
59|Don't look so disappointed. I'll keep it in mind. With any luck, we'll find it.|look so disappointed.;I'll keep it in mind.;With any luck,|Hodram repeats his reassurance about the armadillo shield. The promise remains qualified.
62|||Samwell accepts, as in the previous exchange.
""",
    233: """
5|Got a minute, Admiral?|Got a minute, Admiral?|Match Samwell's opening to the two earlier rumors so the different answer later can land.
9|||Hodram gives the same brief response he did to the other questions.
13|||Samwell asks whether phoenixes exist. His direct question gives Hodram something new to react to.
17|||Hodram says he would like to see one if they exist and asks why the subject came up.
21|||Samwell reports a helmet forged from iron heated in a phoenix's fire. His uncertainty about the exact name stays in the sentence.
24|And you want it because it'd come in handy in a fight?|come in handy in a fight?|Hodram anticipates the argument Samwell made for both shields. The repeated phrasing is the joke.
27|Wow, you caught on fast!|you caught on fast!|Samwell is impressed by Hodram's quick inference. His voice remains bright.
31|You've said that before.|said that before.|Hodram reminds him why the argument was so easy to guess.
34|||Samwell playfully compliments Hodram's memory. He still avoids conceding anything certain about the repetition.
38|||Hodram asks for the location and names Africa and India to echo the earlier vague search areas.
42|What are you talking about? It's in Britain.|What are you talking about?;It's in Britain.|Samwell pushes back and gives a more specific place. Keep Britain as his clue.
46|Oh. You narrowed it down quite a bit this time.|narrowed it down;quite a bit this time.|Hodram is momentarily taken aback that the clue is narrower.
49|||Samwell is proud of checking the rumor himself. The wider northern European lead remains the starting point.
53|I see. Nice work.|Nice work.|Hodram recognizes the work Samwell did before bringing him the lead.
57|||Samwell laughs and accepts the praise. His casual reply is part of the character beat.
61|||Hodram credits Samwell's effort and promises to keep the specific helmet in mind.
65|||Samwell hopes they can find it. The short line closes with enthusiasm.
""",
    234: """
5|||Carlo opens by asking whether Hodram has heard of Herophilus. The approved historical name remains complete.
9|No, I haven't. What about him?|What about him?|Hodram says the name is unfamiliar and asks why Carlo brings it up.
12|||Carlo identifies him as an early physician and credits him with the oldest medical text in the game's account.
16|||Hodram responds briefly so Carlo can explain the importance of the book.
20|They say the book tells you how to keep sailors from tiring so quickly...|the book tells you;sailors from tiring so quickly...|Carlo relates the advice as something he heard. The point is reducing crew fatigue.
24|Well, that would be quite a book. If it's true, I'd like to get hold of it.|quite a book.;get hold of it.|Hodram is intrigued but keeps the benefit conditional.
27|||Carlo agrees. His short reply leaves the question of how to search to Hodram.
31|||Hodram asks for a practical lead after expressing interest in the book.
35|Well... It was a long time ago, but I think I heard someone saw it deep in the Mediterranean.|a long time ago,;deep in the Mediterranean.|Carlo gives the broad region from an old, uncertain memory. The wording keeps each qualification.
39|Anything else?|Anything else?|Hodram asks whether there is another clue. The short phrasing is a natural follow-up.
43|||Carlo can provide nothing beyond that memory. The short answer prompts the next judgment.
47|||Hodram says the clue offers little direction. His reply stays calm.
50|||Carlo apologizes for having no better lead. His formality follows his earlier hesitant answer.
54|||Hodram reassures him that there is no need for an apology.
58|||Carlo acknowledges that reassurance with a pause.
62|||Hodram concludes they will have to search in the Mediterranean themselves if they want it.
""",
}

review = checked_text(previous.review, {"len(records) == 97": "len(records) == 72"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::training-shield-rumors-and-book", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
