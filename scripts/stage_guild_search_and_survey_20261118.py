"""Review the survey parties and four guild searches from the clean dialogue."""

from pathlib import Path
from types import FunctionType

from scripts import register_ruin_statue_and_ice_20261118 as parent
from scripts import stage_ruin_statue_and_ice_20261118 as workflow


base, native, precedent = workflow.base, workflow.native, workflow.precedent
ROOT = Path("work/guild_search_and_survey_20261118_v1")
ROM = ROOT / "Guild_Search_and_Survey_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
MANUSCRIPT = workflow.MANUSCRIPT.with_name("guild_search_and_survey_20261118_v1.json")
HISTORY = (
    ("rafael_B261_B280_final_review_v1",),
    ("hodram_B231_B250_final_review_v1", "hodram_B251_B280_final_review_v1"),
    ("lil_B243_B282_final_review_v1",),
    ("maria_B216_B252_final_review_v1",),
)
CONTEXT = {
    (0, 265): "The guild offers Rafael a job arresting Jean Ramusio before a deal around India grows into a bigger problem.",
    (0, 266): "Rafael interrupts Jean belittling a man. Jean mistakes the inquiry for admiration, then tries to talk his way out of an arrest.",
    (0, 267): "The Sofala guild rebukes Jean, compensates Rafael, and points him toward the local ruins and their legend.",
    (0, 268): "Rafael recalls the region and a local points him toward Ceylon.",
    (0, 269): "The Lisbon guild trusts Rafael with finding Jacob Portunto, an illicit trader active around East Africa.",
    (0, 270): "Jacob plays the generous boss until a subordinate lets his name slip. Rafael watches them flee and takes him to Lisbon.",
    (0, 271): "The guild tells Jacob his fate depends on him, then rewards Rafael.",
    (0, 272): "Rafael remembers East Africa and learns Jacob is reportedly based in Mozambique.",
    (1, 248): "The guild asks Hodram to sail west to Rio de Janeiro with a survey party. The tavern hires and extra funds are part of the request.",
    (1, 249): "Hodram recalls Rio's location and the guild follows up on the survey.",
    (1, 250): "The guild repays Hodram's expenses, gives him a reward and recommends the ruins near Sofala.",
    (1, 256): "The guild asks Hodram to find a Dutch nobleman who has neglected his estate while traveling.",
    (1, 257): "A local recognizes Yuris by his runtime name and relays the London guild's search.",
    (1, 258): "Yuris admires Rome before revealing himself to an impatient Hodram. Yuris remembers his estate and Hodram sets London as the first stop.",
    (1, 259): "Yuris is reminded of his duty and offered a rest. After the reward, a rude customer reveals the supply of ruin maps is gone.",
    (1, 260): "The square in Syracuse is a reported sighting, with no claim of certainty.",
    (2, 247): "The guild asks Lil to sail east to Leveque with a survey party. Lil reacts to the distance and hears the requirements for crew and funds.",
    (2, 248): "Lil remembers Leveque's location and the guild follows up on the survey.",
    (2, 249): "The Sofala guild pays for the completed survey and directs Lil to the nearby ruins.",
    (2, 255): "The guild asks Lil to find Jacks Bloom, last known to have headed for Sao Jorge. It will wait for her.",
    (2, 256): "The bartender and another patron set up the reveal that Jacks is present. Lil tells Jacks who wants him and he asks for a lift.",
    (2, 257): "Jacks reunites with the Hamburg guild. The guild rewards Lil and mentions a nearby church and its learned priest.",
    (2, 258): "Lil remembers Sao Jorge and the guild repeats the last reliable lead.",
    (3, 225): "The guild contact professes to be too intimidated to ask Maria for help while slipping her every detail. Maria sees through him.",
    (3, 226): "Plett gives himself away in the Ternate tavern. One of Maria's crew recognizes the man who framed him. Maria stops the beating and leaves the rest to the guild.",
    (3, 227): "Maria tells the guild contact where she found Plett. He apologizes for the imposition and offers her a reward.",
    (3, 228): "Maria and the contact recall the only lead, somewhere around Indonesia.",
    (3, 229): "The guild offers Maria the Jean Ramusio job before his planned deal around India becomes a bigger problem.",
    (3, 230): "Maria interrupts Jean to ask his name. He reads it as admiration, which makes his excuses look all the worse when she tells him why she is there.",
    (3, 231): "The Sofala guild calls out Jean's defiance, compensates Maria for bringing him in, and recommends the nearby ruins.",
    (3, 232): "Maria recalls the region and a local points her toward Ceylon.",
}
BLOCKS = {key: key for key in CONTEXT}
EDITS = {}


def revise(route, block, turn, text, note, *phrases):
    EDITS[route, block, turn] = (text, phrases, note)


revise(0, 265, 13, "Word is he's setting up a big deal around India. Catch him before things get out of hand.",
       "The deal is rumored. The guild wants it stopped before it escalates.", "a big deal", "out of hand.")
revise(0, 266, 37, "I'm here to arrest you. It looks like you've been making money from smuggling. You're coming with me.",
       "Rafael answers Jean's posturing with the apparent crime and an instruction to come along.", "from smuggling.", "You're coming with me.")
revise(0, 266, 56, "You were talking big a minute ago. Look at you now. Come on. We're going to the guild in Sofala.",
       "Rafael notices the change from bluster to pleading and takes Jean in.", "Look at you now.", "the guild in Sofala.")
revise(0, 267, 12, "Cornered, and now you act like you're innocent? Pathetic.",
       "The guildmaster identifies Jean's change to defiance after his denial.", "you're innocent?")
revise(0, 268, 26, "Jean's in Ceylon, from what I hear. Go catch him!",
       "Keep the reported location tentative and the request urgent.", "from what I hear.")
revise(0, 269, 14, "I need you to catch a smuggler named Jacob Portunto. He's a slippery one and a real nuisance.",
       "The guild supplies the name and takes a dim view of Jacob's cunning.", "Jacob Portunto.", "a real nuisance.")
revise(0, 270, 5, "Come on, boys. Live it up today!",
       "Jacob encourages his men to enjoy themselves before one lets his name slip.", "Live it up today!")
revise(0, 270, 8, "Thanks, boss!",
       "The first man's thanks to the boss refers to Jacob's immediately preceding offer.", "Thanks, boss!")
revise(0, 272, 13, "Jacob, the smuggler... He was supposed to be in East Africa.",
       "Rafael is recalling a lead. Keep the report tentative.", "East Africa.")

revise(1, 248, 5, "I need a hand.",
       "A direct offer leads into the details of the survey.")
revise(1, 248, 20, "The southern New World, across the Atlantic... A long way.",
       "Hodram thinks through the location and measures the distance aloud.", "southern New World,")
revise(1, 250, 55, "They say it was King Solomon's treasury. Have a look.",
       "The guildmaster recounts what the ruin supposedly once was, then recommends a visit.", "King Solomon's treasury.")
revise(1, 256, 5, "I've got a job for you. I need to find someone.",
       "The guildmaster invites Hodram to take the search before naming Yuris.")
revise(1, 258, 5, "This should be the town where that fellow Yuris was seen.",
       "Hodram recalls the reported sighting and still has to find Yuris.")
revise(1, 258, 12, "Excuse me. Do you know a man named Yuris?",
       "Hodram makes a direct inquiry to the man he has yet to identify.")
revise(1, 258, 31, "Can you afford to idle? Your people are upset. Their lord left and never came back.",
       "Hodram challenges the lord's neglect directly and reports his subjects' complaint.", "never came back.")
revise(1, 258, 37, "London first. We'll see from there.",
       "Hodram remains firm about the immediate next stop and defers the rest.")
revise(1, 259, 5, "Ah, Yuris. What have you been doing all this time? Your people are in a bind with you shirking your duties.",
       "The guildmaster asks what occupied Yuris and connects the neglect to the hardship back home.", "shirking your duties.")
revise(1, 259, 86, "Maps to some ruins. A strange bunch has been hanging around there lately. I hear the locals are fed up with them.",
       "Keep the guildmaster's report, the unfamiliar group and the effect on nearby residents.", "fed up with them.")

revise(2, 247, 9, "There's a village called Leveque far to the east, across the Indian Ocean. I'd like you to take a survey party there.",
       "The approved village and geographical lead remain intact. The guild wants a party sent to carry out a survey.", "the Indian Ocean.", "a survey party there.")
revise(2, 247, 12, "Survey party?",
       "Lil picks up the exact phrase she wants explained.")
revise(2, 247, 16, "Take them along as sailors. When you get to the tavern, hire a few more than usual.",
       "The guildmaster explains the assignment through the ordinary sailor hiring process.", "more than usual.")
revise(2, 247, 24, "That's why I'm asking you.",
       "The speaker personally appeals to Lil because of the distance.")
revise(2, 248, 18, "How's the Leveque survey? It's a long way east, across the Indian Ocean.",
       "The guild asks how the Leveque survey is going and repeats the route across the Indian Ocean.", "the Indian Ocean.")
revise(2, 249, 5, "Thanks! Here's your reward, plus enough to cover your expenses.",
       "The guild gives both compensation and expense reimbursement.", "cover your expenses.")
revise(2, 256, 27, "Do I know him...",
       "The other patron starts a knowing reply. Jacks himself delivers the punch line.")
revise(2, 256, 43, "Great! Hamburg's guild is looking for you!",
       "Lil's delighted surprise leads straight into why she came.", "looking for you!")
revise(2, 257, 67, "The local church's priest is a noted scholar.",
       "The nearby church and the priest's reputation for learning stay explicit.", "a noted scholar.")

revise(3, 225, 27, "...You certainly know how to ask a favor.",
       "Maria sees the contact's repeated protest as a way of getting her to volunteer.", "ask a favor.")
revise(3, 226, 20, "Oh? What's got you so flustered? Don't tell me you're Plett.",
       "Maria tests her suspicion after hearing Plett fall over.", "you're Plett.")
revise(3, 226, 34, "...You'd best give up.",
       "Maria starts with a cool warning, then backs it up with action.")
revise(3, 226, 74, "Aaah! You! I remember you, you bastard!",
       "The crewman's surprise turns into angry recognition.")
revise(3, 226, 87, "Heh heh... Admiral, may I?",
       "He formally asks Maria to let him handle it just before refusing to take no for an answer.", "Admiral, may I?")
revise(3, 226, 91, "I won't back down. Now brace yourself!",
       "The crewman refuses to be talked out of confronting Plett, then tells him to brace himself.", "Now brace yourself!")
revise(3, 227, 11, "I-I see. Sorry for the trouble. I'm almost embarrassed to offer so little, but please take it.",
       "The guild contact is apologetic, stammers, and humbly offers the reward.", "please take it.")
revise(3, 229, 5, "Want a little job?",
       "A casual offer invites Maria to hear the details.")
revise(3, 230, 34, "You've got the wrong idea. The Sofala guild sent me to bring you in for smuggling.",
       "Maria punctures Jean's assumption and states the charge and guild's role.", "The Sofala guild", "in for smuggling.")
revise(3, 230, 37, "Wha...?",
       "Jean's confidence collapses mid-exchange, rendered with ordinary speech punctuation.")
revise(3, 230, 41, "Well, that saved me.",
       "Jean's companion is relieved to be out from under the reprimand.")
revise(3, 230, 52, "You're embarrassing yourself. It's over. You're coming with me to the Sofala guild.",
       "Maria has no patience left for Jean's denial and orders him to come along.", "the Sofala guild.")
revise(3, 231, 11, "Now that you're cornered, you're acting like you did nothing wrong? Pathetic.",
       "The same guildmaster calls out Jean's sudden defiance after his denial.", "nothing wrong?")
revise(3, 231, 63, "They say it was King Solomon's treasury. Have a look.",
       "The ruins' former identity is a local legend and the guild encourages a visit.", "King Solomon's treasury.")
revise(3, 232, 11, "That's right, we were looking for that Jean fellow somewhere around India.",
       "Maria recalls the region and only part of Jean's name.", "somewhere around India.")

RETENTIONS = {
    (0, 267, 18): "The gold-coin notice gives the exact 20,000 payment. Preserve its original system presentation.",
    (0, 270, 39): "Rafael's praise is plainly sarcastic after Jacob's own men run away.",
    (0, 270, 52): "Jacob's panicked curse and realization that he is finished already land in one short retort.",
    (0, 271, 8): "The guildmaster leaves Jacob's treatment conditional on his conduct.",
    (0, 271, 15): "Keep the exact 18,000 gold-coin payment in the system notice.",
    (1, 248, 12): "The short echo is Hodram's request for an explanation of an unfamiliar assignment.",
    (1, 248, 24): "Hodram's objection about the distance supplies the reason referred to in this reply.",
    (1, 257, 6): "Keep the runtime name, the London guild and the recognition beat. The original caller is on Hodram's route.",
    (1, 258, 15): "The paired observations convey what holds Yuris's attention while Hodram tries to interrupt.",
    (1, 259, 79): "The guildmaster's retort follows the departing customer's insult and explains why the maps sold out.",
    (1, 259, 90): "Hodram follows up on the ruin's location with a quick question. The guildmaster answers it directly.",
    (2, 247, 20): "Lil's astonishment is proportionate to the voyage. The geographic inference and playful stress already work.",
    (2, 256, 23): "The brief surprised question keeps the comic pause just before Jacks reveals himself.",
    (2, 257, 12): "Jacks apologizes casually, consistent with the relaxed reunion and his earlier request for a lift.",
    (3, 225, 17): "Maria volunteers plainly, taking the hint without echoing the contact's coy delivery.",
    (3, 226, 12): "The sound effect keeps the clatter and fall that give Plett away.",
    (3, 226, 26): "Maria's dry compliment gives way to a clear order to accompany the group to Hangzhou.",
    (3, 226, 112): "Maria stops her crewman and leaves the matter to the Hangzhou guild.",
    (3, 227, 7): "Maria names the Ternate tavern and keeps the dry understatement about Plett giving up.",
    (3, 230, 22): "Jean confirms his identity in a short aside before his longer boasts, following Maria's use of his full name.",
}

scope = workflow.SCOPE | globals()
for function in (workflow.SCOPE["historical"], workflow.SCOPE["review_exchange"],
                 workflow.oral_collect, workflow.SCOPE["main"]):
    scope[function.__name__] = FunctionType(function.__code__, scope)
scope["validate_native"] = workflow.precedent.validate_native


if __name__ == "__main__":
    scope["main"]()
