"""Draft the missing-ship sequence, both dock follow-ups, and Jam’s return from clean Japanese."""
from scripts.seal_clean_independent_drafts_v1 import seal


MISSING = (
    "A sailor wakes Rafael with news that the ship is missing. The departure office worker saw a skinny young man "
    "aboard alone and thought he was inspecting it. Rafael excuses the misunderstanding and wonders how one person "
    "could get the ship under way. Claudio is alarmed and wants to look for the thief."
)
WAITING = "The departure office worker says the ship still appears to be away. Keep each native follow-up reference separate."
RETURN = (
    "The ship returns with Jam aboard. He treats taking a ship as picking up something someone dropped, brags about "
    "sailing alone and rattles off his own sayings. Rafael takes his ability seriously, and Jam pretends to turn down "
    "the invitation before revealing the joke. Preserve his repeated cheer, the spoken spelling of Jam, the English "
    "and French flourishes and the distinct full introduction."
)
CONTEXT = {173: MISSING, 174: WAITING, 175: WAITING, 176: RETURN}

DATA = {
    173: {
        5: ("The sailor urgently addresses the admiral and reports that the ship is gone.", "Admiral! We've got trouble! The ship... The ship is gone!"),
        8: ("Rafael mumbles sleepily and asks what is happening so early.", "Mmm... What is it? At this hour?"),
        12: ("Claudio thinks he heard that the ship is gone and finds it impossible.", "Did I hear you say the ship's gone? No way..."),
        23: ("Arcadius says it would be serious if true.", "Well, if it's true, we're in serious trouble."),
        29: ("The sailor insists it is true and asks them to come to the departure office immediately.", "It's true! Come to the departure office, quick!"),
        32: ("Rafael is shocked to see it really is gone.", "What?! No! It's gone! It really is gone!"),
        36: ("The sailor stammers as he asks what they should do.", "Wh-what do we do?"),
        48: ("Arcadius reacts mildly and confirms the ship is absent.", "Oh, dear. It really is gone."),
        54: ("Claudio demands an explanation.", "What happened?!"),
        58: ("The departure office worker calls urgently to the admiral.", "Hey! Admiral!"),
        62: ("The worker saw a thin young man doing something with the ship all by himself early that morning.", "It's bad! Early this morning I saw some skinny young fellow messing with the ship all by himself, and then..."),
        66: ("The worker blurts out that the young man took the ship out.", "He sailed right out of port!"),
        70: ("Claudio indignantly echoes the report, objecting to how casually it is delivered.", "Hold on! He sailed out of port, just like that?!"),
        81: ("Arcadius is taken aback that someone capable of that exists.", "My, my... Some people really are remarkable."),
        84: ("Claudio says now is no time to admire the man or stay so relaxed.", "Quit admiring him! This is no time to stand around talking!"),
        91: ("The worker did not expect him to sail off alone and assumed it was an inspection or something similar.", "I never thought he'd sail off. He was alone. I figured he was just checking the ship or something."),
        95: ("Rafael thinks that was a normal assumption and absolves the departure office worker.", "That's what anyone would've thought. You did nothing wrong."),
        99: ("Rafael wonders what sort of person could have set sail alone.", "Still, setting sail all by himself... What kind of person does that?"),
        103: ("Claudio tells Rafael to quit taking it easy and proposes asking around town so he can catch the ship thief.", "Quit daydreaming and let's ask around town. I'm gonna catch that ship thief!"),
    },
    174: {6: ("The departure office worker thinks the ship has yet to return.", "Looks like it still hasn't come back.")},
    175: {6: ("The separate departure office follow-up gives the same report.", "Looks like it still hasn't come back.")},
    176: {
        5: ("The worker calls twice to the admiral and says the ship has returned.", "Admiral! Admiral! That ship's back!"),
        8: ("Rafael is startled and asks what he said.", "What?! Say that again!"),
        13: ("The worker points out the unmistakable ship.", "There! That's the ship. No mistaking it!"),
        18: ("Jam whoops and delights in the vastness of the sea.", "Yahoo! The sea is great! Wide open! Huge!"),
        22: ("Jam says he has been having fun since morning and cheers for another fine day.", "Whew. I've been having fun since sunup. What a fine day! Yahoo!"),
        25: ("Rafael privately finds him even stranger than expected.", "...He's even stranger than I thought."),
        30: ("Claudio tells Jam off for taking someone else's ship without asking.", "Hey, you! You don't just take someone else's ship without asking!"),
        34: ("Jam acts baffled and says he found it lying around.", "Huh? What are you talking about? I found it lying around!"),
        37: ("Claudio says a ship cannot just be lying around somewhere.", "...Ships don't just lie around waiting to be picked up!"),
        40: ("Jam grandly claims he found it while walking through the harbor, lonely and abandoned. He insists it is true.", "I was walking through the harbor when I found it. There it was, all lonely and abandoned! True story. What can I say?"),
        44: ("Jam praises his own kindness, says he picked it up, spells his given name and cheers.", "So I, the kindhearted Jam, picked it up. That's Jam, J-A-M. Yahoo!"),
        47: ("Rafael clarifies Jam's reasoning and asks how he moved the ship by himself.", "You got aboard because you found it? But how'd you get it moving? You did it all by yourself, right?"),
        52: ("Jam vaguely describes doing this and that and says he more or less winged it.", "A little of this, a little of that... I just sort of winged it. Yahoo!"),
        55: ("Rafael is impressed.", "...That's amazing."),
        60: ("Claudio reminds Jam the ship is on water and asks what he would have done if it had sunk.", "Listen, pal. Ships sail on water, you know. What were you gonna do if it sank?"),
        64: ("Jam clicks his tongue and tells Claudio to listen to his words of wisdom.", "Tsk, tsk, tsk! Let me share some words of wisdom. Listen close!"),
        68: ("Jam declares that one can do what one sets out to do. He cheers and says it is fine by him.", "Where there's a will, there's a way! Yahoo! And if I say it's all right, it's all right!"),
        79: ("Fernando says a dangerous or crazy fellow has appeared.", "Oh, boy. This guy's trouble."),
        86: ("Rafael repeats the saying with uncertainty.", "Where there's a will, there's a way, huh..."),
        91: ("Jam takes himself as proof and coins a grand maxim about a life that is very large and very short.", "It all works out because I'm me! Here's another one. Life should be big and short!"),
        95: ("Jam scorns keeping his head down and living a long, narrow life. It would be too dull for him.", "Keep my head down and live a small, long life? Too dull for me. I couldn't stand it!"),
        98: ("Claudio asks FI whether they should turn Jam over to the guards.", "What a piece of work... FI, what do we do? Hand him over to the guards?"),
        102: ("Rafael rejects that idea and proposes taking Jam into the crew.", "No way, Clau. Let's ask him to join us!"),
        106: ("Claudio asks FI whether Jam's foolishness has rubbed off on him.", "Hold on, FI. Is his foolishness rubbing off on you?"),
        109: ("Rafael praises Jam for moving the ship alone and checks his name.", "But he can sail a ship all by himself! That's incredible. Jam... That was your name, right?"),
        114: ("Rafael invites Jam onto his ship.", "Want to sail with me?"),
        119: ("Jam wonders whether to go, theatrically asks for a moment, then says he needs two seconds.", "Hmm. Do I go or don't I? What to do... Just a moment! Give me two seconds to think!"),
        122: ("Jam suddenly announces that he has decided.", "All right!"),
        126: ("Rafael asks whether he made up his mind.", "Made up your mind?"),
        131: ("Jam says yes, pretends to decline, says goodbye and wishes them a good voyage.", "Yep. I decided I'm not coming! See you! Have a good voyage!"),
        135: ("Rafael is shocked and asks him to wait, stammering.", "What?! W-wait a second!"),
        140: ("Jam is delighted to get the reaction he expected, says Merci and reveals his joke.", "Ha! Just the reaction I was hoping for! Merci! I was kidding!"),
        143: ("Rafael is incredulous that it was a joke.", "You were kidding?!"),
        148: ("Jam asks to go with them, introduces himself with his full name and cheers.", "Yeah, take me with you! Let's do this properly. I'm Jam Jack Ludwyan! Yahoo!"),
    },
}


if __name__ == '__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105', 'B173_B176_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 55)
