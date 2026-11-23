"""Review Hodram's guild captures and return exchanges from B265 through B280."""

from scripts import review_hodram_B261_B264_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B265_B280_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    265: "Hodram delivers Gabriel to the Stockholm guild. Gabriel repeats his tavern excuse, the guildmaster rewards Hodram, and the guild leaves the stolen item in his care.",
    266: "A guildmaster commissions Hodram to apprehend Julian Vermeer and passes on a report about his work in the Mediterranean.",
    267: "The guildmaster taunts the captured Julian, pays Hodram, and gives him directions to the mosque in the Sahara.",
    268: "Hodram reviews the Mediterranean lead, then hears it again along with the guildmaster's urgent request to catch Julian.",
    269: "The port worker passes on that the guild in Sao Jorge was looking for the captain.",
    270: "The Hangzhou guildmaster makes a personal appeal for a woman whose father was killed by Plett Perrault.",
    271: "Plett tries to answer an accusation of murder with a claim of remorse. The guildmaster thanks Hodram for taking him alive and leaves his fate to the woman.",
    272: "Hodram reminds himself of the assignment, and the guildmaster presses him to bring Plett in.",
    273: "The guildmaster asks Hodram to capture Jean Ramusio and warns him about the fleet that ambushed the force sent after him.",
    274: "Jean denies smuggling, then tries to wriggle out of the guildmaster's advice. The guildmaster pays Hodram and shares a legend about a treasure in a mosque.",
    275: "Hodram recalls that Jean's fleet is in India. The guildmaster passes on a report that Jean is hiding there.",
    276: "The guildmaster asks for help with Jacob Portunto, whose resources now outmatch the guild's, and pays an advance.",
    277: "Jacob laments losing his cargo. The guildmaster points out that it belongs to others, then pays Hodram and offers a tip about nearby ruins.",
    278: "Hodram reminds himself to find Jacob's fleet, and the guildmaster asks if he has found Jacob yet.",
    279: "The guildmaster reluctantly asks Hodram for help with a pirate who terrifies the merchants. He gives the Mediterranean lead and an advance.",
    280: "The captured Hernan demands a grand entrance. Hodram dryly assesses him, and the relieved guildmaster pays for the capture and suggests a local landmark.",
}
DECISIONS = {
    265: """
5|I brought Gabriel back.|I brought Gabriel back.|Hodram announces that he has returned with the man the guildmaster requested.
9|Back at last, are you? Now hand over the money you pocketed behind our backs.|Back at last, are you?;you pocketed behind our backs.|The guildmaster greets Gabriel with sarcasm and demands the money he secretly took.
13|I-I'll pay you next time. I swear...|pay you next time.;I swear...|Gabriel stalls with the same next-time promise and stammers when the guildmaster confronts him.
17|I heard that excuse at the tavern. Well, I'll leave you to it.|that excuse at the tavern.;I'll leave you to it.|Hodram calls back to the tavern exchange and takes his leave of the guildmaster.
21|||The guildmaster stops Hodram, uses the surname substitution and insists he accept a payment before leaving.
26|||The result panel preserves the exact reward of 22,000 gold coins.
49|||The result panel preserves the slight increase in Stockholm market share without an invented amount.
60|Keep the stolen item for now. If we can't find the owner, do what you like with it.|the stolen item for now.;find the owner,;do what you like with it.|The guildmaster entrusts the item to Hodram. The captain may use it as he pleases if the owner cannot be found.
""",
    266: """
6|I've got someone I need you to bring in. I know I can count on you.|I need you to bring in.;I can count on you.|The guildmaster chooses Hodram because he trusts him to subdue the target.
9|His name is Julian Vermeer. He's Portuguese, but he betrayed his country and sided with Spain. I hear he's been running cargo in the Mediterranean.|Julian Vermeer.;sided with Spain.;running cargo;in the Mediterranean.|The guildmaster gives Julian's name, homeland and allegiance, then attributes his activity as a carrier to hearsay.
""",
    267: """
5|||The guildmaster recognizes Julian and mocks his bedraggled appearance. The two short exclamations fit his reaction.
8|D-damn it! Let go of me!|Let go of me!|Julian starts with a stammer and demands his release. Keep his anger and the rough delivery.
12|You did a fine job. We'll take it from here. Here, this is for you.|You did a fine job.;We'll take it from here.;this is for you.|The guildmaster thanks Hodram, takes responsibility for the aftermath, and hands over the reward.
16|||The result panel gives the stated 32,000 gold coins.
41|||The result panel uses the established Sao Jorge spelling and gives the slight share increase.
59|Say, if you want to see the mosque deep in the Sahara, take a map and set out through the gate at the edge of town.|deep in the Sahara,;set out through the gate;at the edge of town.|The guildmaster starts a new topic and gives all three route details in one natural set of directions.
""",
    268: """
12|Julian's fleet was in the Mediterranean. He was working as a courier, wasn't he?|in the Mediterranean.;as a courier, wasn't he?|Hodram recalls both the fleet's location and Julian's reported work as a carrier.
24|Catch that traitor Julian as soon as you can. I hear he's been running cargo in the Mediterranean.|Catch that traitor Julian;as soon as you can.;in the Mediterranean.|The guildmaster presses for an arrest and repeats the same report about Julian's carrying work.
""",
    269: """
6|||The port worker gives the location and says its guild was looking for the captain. The casual wording suits the messenger.
""",
    270: """
6|||The guildmaster asks whether Hodram has a heart. The friendly pressure sets up the appeal.
9|||The request preserves the man's English origin, his killing of the woman's father and her aim to avenge him. The short beats let the guildmaster ask for help without sounding formal.
13|||The guildmaster gives the approved full name and renews the appeal with a familiar question tag.
""",
    271: """
5|Plett, you bastard! How dare you show your face, you monster...|Plett, you bastard!;show your face,;you monster...|The guildmaster erupts when he sees Plett. The unfinished condemnation leaves Plett room to respond.
8|I-I'm telling you, I regret it...|I regret it...|Plett claims remorse and stammers through his defense, prompting the guildmaster to say that regret is insufficient.
12|||The guildmaster dismisses Plett's claimed remorse in one plain sentence. Sorry picks up Plett's defense and leaves no doubt what he has done.
15|||The guildmaster thanks Hodram and says the woman who came to the guild may decide what to do with Plett.
19|I never thought you'd bring him in alive. You've earned a handsome reward. Take it.|bring him in alive.;a handsome reward.|The guildmaster was surprised to see Plett alive and personally offers the larger reward.
23|||The panel reports the exact reward of 35,000 gold coins.
48|||The panel reports a slight increase in the player's Hangzhou share.
66|||The guildmaster recommends the Forbidden City at least once and acknowledges the distance from Hangzhou.
69|||The guildmaster asks the captain to keep his name out of any conversation with officials. The sudden hush suits him.
""",
    272: """
12|I'd better put a stop to Plett soon.|put a stop to Plett soon.|Hodram reminds himself the outlaw still needs to be defeated soon without specifying Plett's fate.
25|||The guildmaster bluntly demands Plett's capture and presses for speed.
""",
    273: """
5|There's a bounty I want you to take. Bring in a man named Jean Ramusio.|a bounty I want you to take.;Jean Ramusio.|The guildmaster asks Hodram to capture the wanted man and supplies the approved full name.
9|We were after him for smuggling, but he turned the tables on the force we sent after him in India.|after him for smuggling,;turned the tables;in India.|The guildmaster says the force hunting him met with defeat in India, where Jean turned the attack back on his pursuers.
13|||The guildmaster repeats the report comparing the fleet to a pirate's and hands over an advance. The warning sounds urgent.
23|||The notice gives the exact advance of 15,000 gold coins.
""",
    274: """
5|Well, if it isn't the smuggler! You finally caught him.|the smuggler!;You finally caught him.|The guildmaster recognizes Jean and is relieved that Hodram has caught him at last.
8|Everyone calls me a smuggler, but they've got it wrong. All of them! I'm the one being put out here, you know.|calls me a smuggler,;they've got it wrong.;All of them!;being put out here, you know.|Jean insists everyone misunderstands him and plays the victim. The repetition belongs to his performance.
11|You sure can talk. Ever stop to think about the trouble you've caused everyone else?|You sure can talk.;the trouble you've caused;everyone else?|The guildmaster derides Jean's glibness and tells him to consider those he inconvenienced.
15|||Jean's exasperated demand sets up the guildmaster's direct answer.
19|||The guildmaster tells Jean to earn an honest living and heads off the excuse that he already does. The plain speech suits his exasperation.
22|...I can't say that?|I can't say that?|Jean immediately checks whether the escape the guildmaster just ruled out is really closed. Keep the pause for his comic timing.
26|I'm sorry you had to deal with him. It's a small token, but please take it.|you had to deal with him.;please take it.|The guildmaster turns away from Jean, sincerely apologizes and offers the customary modest description of the reward.
30|||The reward notice gives the exact 75,000 gold coins.
55|||The separate notice records a slight rise in Basra market share.
73|||The guildmaster offers an inside tip, places the mosque far inland and says it holds remarkable treasure.
76|They say you'll need the blessing of the king enshrined there to claim the treasure. I'd say it's worth a try for you.|the king enshrined there;to claim the treasure.;worth a try for you.|The stated requirement is recognition from the king honored at the mosque. The guildmaster treats it as a story and encourages Hodram to try.
""",
    275: """
12|Jean's fleet is in India. I need to defeat him.|Jean's fleet is in India.;I need to defeat him.|Hodram remembers both the fleet and the objective. His reminder sounds current.
17|||The guildmaster passes on a report that Jean is hiding in India and treats his whereabouts as uncertain.
""",
    276: """
5|Mr. FA, I've got a favor to ask. I know I can count on you.|I've got a favor to ask.;I can count on you.|The guildmaster uses the established surname token and explains why he picked Hodram.
8|What is it?|What is it?|Hodram asks what the favor is. His directness leaves the guildmaster to explain.
12|||The guildmaster asks for the capture of a wanted Dutch smuggler. Keep Jacob Portunto's approved name.
16|||The guildmaster contrasts Jacob's days as a petty thug with his rumored windfall in Africa and his present pirate pretensions.
19|Here's an advance. We can't take him on ourselves, but I think you can. See what you can do.|Here's an advance.;take him on ourselves,;I think you can.;See what you can do.|The guildmaster offers advance payment, admits the guild is outmatched and expresses confidence in Hodram.
28|||The separate notice gives the exact 16,000-gold advance.
""",
    277: """
5|||The guildmaster recognizes the returning captain with a plain familiar greeting.
9|||Jacob's short complaint makes his lost cargo his first concern, setting up the rebuke.
13|||The guildmaster rejects Jacob's claim outright. His emphatic answer supplies the fact that it belonged to other people.
16|||The guildmaster thanks Hodram for capturing Jacob and offers a reward with customary modesty.
19|||The panel gives the exact reward of 72,000 gold coins.
44|||The panel records a slight increase in Calicut's market share.
62|I've got a tip for you. This one's worth hearing.|I've got a tip for you.;worth hearing.|The guildmaster shifts to his especially good tip and directs it to Hodram personally.
66|Try heading out through the city gate. I hear there's a building out that way with a fine treasure hidden inside.|through the city gate.;a building out that way;hidden inside.|The guildmaster recommends the gate as the starting point and treats the treasure in the building as hearsay.
77|||The guildmaster reminds Hodram to get a map before exploring. The brief instruction is easy to act on.
""",
    278: """
12|||Hodram reminds himself to find Jacob's fleet rather than giving a new destination or tactic.
25|||The guildmaster's informal question asks if there is any sign of Jacob yet.
""",
    279: """
5|Hmm... What am I going to do? I guess you're the only one I can ask...|What am I going to do?;the only one I can ask...|The guildmaster first frets, then decides Hodram is the only viable person to ask.
8|||The guildmaster asks Hodram to defeat the Spanish pirate and gives his approved full name.
11|||The guildmaster explains the threat to local merchants and how even mentioning Hernan frightens others away from the job.
15|Word is he's been prowling the Mediterranean. I'm counting on you. Here's your advance.|prowling the Mediterranean.;I'm counting on you.;Here's your advance.|The guildmaster repeats the reported location, expresses confidence and hands over advance payment.
24|||The notice preserves the exact 30,000-gold advance.
""",
    280: """
5|||Hernan pompously demands passage despite being a captive. The grand self-introduction makes the next response work.
8|He's tied up and still acts like a king. Unbelievable.|still acts like a king.;Unbelievable.|Hodram contrasts the man's restraints with his royal airs and voices his disbelief.
11|You finally caught him! I knew I was right to ask you. Well done. Please take this.|You finally caught him!;I was right to ask you.;Please take this.|The guildmaster's relief turns to praise and an offer of payment.
14|||The notice gives the stated 110,000 gold coins.
40|||The next notice records a slight rise in Athens market share.
58|||The guildmaster changes the subject and asks whether the captain has seen the local landmark.
61|||The question echoes the guildmaster's word to ask for clarification.
65|Go have a look. It's practically the symbol of the town.|Go have a look.;the symbol of the town.|The guildmaster urges a visit and explains what the landmark means to the town without inventing its identity.
""",
}

review = checked_text(previous.review, {"len(records) == 17": "len(records) == 80"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::guild-captures", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
