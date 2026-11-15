"""Draft Al's full recruitment exchange from clean B167 before opening current English."""
from scripts.seal_clean_independent_drafts_v1 import seal

CONTEXT = {167: (
    "Rafael hears a bodyguard argue with his employer over being treated as an errand boy. When the employer fires "
    "him, Rafael sees a potential ally, but Claudio recognizes that flattering him will get nowhere. The alternative "
    "Claudio and Julio exchanges preserve their separate voices. Claudio finally challenges the mercenary to put his "
    "strength to use at sea. Al sees through the provocation and joins anyway. Preserve his agency and qualify the "
    "provisional full-name spelling against the established name fields before final review."
)}

DATA = {167: {
    5: ("The bodyguard insists he was hired to protect his employer, not carry things or run errands.", "Let's get one thing straight. You hired me as a bodyguard. I'm not your porter or your errand boy."),
    9: ("Rafael reacts with wordless curiosity.", "...?"),
    14: ("The employer suspects he is making excuses to loaf again and demands obedience because he pays him.", "Hmph. Looking for another excuse to loaf around? I pay your wages. Do the work I give you."),
    17: ("The bodyguard tells him to hire someone softer if he wants obedience. He stakes his life on this work.", "If you want somebody who'll do whatever you say, hire someone softer. I put my life on the line for this job."),
    21: ("The employer mocks him for being fit only to fight and unable to do other work.", "Hmph. Fighting's your only talent, so you can't do anything else. Is that it?"),
    25: ("The employer says he will hire someone more tractable and tells the bodyguard to go wherever he likes.", "Fine. I'll hire someone who knows how to follow orders. You can go wherever you please!"),
    31: ("The bodyguard dismissively tells the employer to do as he pleases.", "Suit yourself!"),
    35: ("An associate grumbles that Al's skill has gone to his head.", "That Al... Just because he's good at what he does, he thinks he can act like that."),
    39: ("The employer fires Al for insolence and orders his associate to find another bodyguard at once.", "That insolent man's fired. Find me another bodyguard. Now!"),
    42: ("The associate hesitantly agrees, but doubts they can easily find another person as strong.", "Yes, sir... It's just that someone with that kind of strength isn't easy to come by."),
    46: ("The employer reminds him that finding one is his job and orders him to come along.", "Finding one is your job. Come on."),
    50: ("Rafael hears that the man is exceptionally strong and immediately wants him as a crewmate.", "They said he's incredibly strong. Wouldn't he be great on our crew?"),
    54: ("Claudio dryly teases Rafael for his familiar naive optimism.", "Still looking on the bright side, aren't you? You make everything sound so simple."),
    63: ("Claudio doubts a man like that will be easy to recruit.", "I don't think a guy like that will be easy to bring aboard..."),
    68: ("Julio expresses the same caution in the alternative branch.", "I doubt we'll have much luck bringing a man like that aboard..."),
    74: ("Rafael insists that they won't know without trying and urges them to go.", "We won't know until we try. Come on, let's go!"),
    79: ("Rafael spots Al and tentatively asks for a moment.", "There he is. Uh, could we talk for a minute?"),
    83: ("Al asks bluntly what they want.", "What do you want?"),
    87: ("Rafael wants to discuss a proposition because of Al's strength.", "I'm here because of your strength. I have a proposition for you."),
    91: ("Al privately wonders whether this is a job and says the stranger seems to know his worth.", "(A job?) Hmph. I don't know you, but you seem to know what I'm worth."),
    95: ("Claudio thinks to himself that the man is remarkably sure of himself.", "(Oh, boy. This one's sure of himself.)"),
    98: ("Rafael stammers that his build makes it obvious and asks Claudio to agree.", "Y-yes. Anyone can see that just by looking at you. Right, Clau?"),
    103: ("Claudio asks whether Al is a sailor.", "...Are you a sailor?"),
    107: ("Al says he is a mercenary and has always made a living by his own strength.", "Hardly. I'm a mercenary. I've always made my living with these two hands."),
    110: ("Rafael asks how Al makes a living when there is no fighting, as at present.", "I see... What do you do when there's no fighting, like now?"),
    114: ("Al says he works as a bodyguard and the dangerous times keep him employed.", "I work as a bodyguard. It's a dangerous world. There's work to be had."),
    117: ("Rafael asks what Al is doing now.", "What about now?"),
    122: ("Al says they saw him lose his job. He refuses to become a sailor and will talk only if they have a job offer.", "You saw. I just got fired. But I'm not taking up sailing. If you haven't got a job for me, we're done talking."),
    125: ("Claudio accepts the rebuff and excuses the interruption.", "...Fair enough. Sorry to bother you."),
    130: ("Rafael asks Claudio to wait, apologizes to Al and trails off on a later meeting.", "W-wait, Clau! Oh, sorry. Maybe another time..."),
    140: ("Claudio says the result was exactly what he expected.", "Just what I thought..."),
    144: ("Rafael protests that Claudio seems to understand everything while he understands none of it.", "Hey! What makes that so obvious to you? I don't get it at all!"),
    148: ("Claudio says a man like that gets cocky if approached too deferentially.", "A guy like that just gets cockier if you go asking too nicely."),
    153: ("In the alternate exchange Julio says it went as expected.", "Just as I thought..."),
    157: ("Claudio agrees and begins explaining how a man like that responds.", "Yeah. A guy like that..."),
    161: ("Rafael protests that both of them understand and he does not.", "Wait! You two might understand what just happened, but I don't!"),
    166: ("Julio addresses Rafael as admiral and explains that deference makes men like that push their advantage.", "Listen, Admiral. If you go hat in hand to a man like that, he'll just get cockier."),
    173: ("Rafael hesitates and asks what they should do instead.", "But... then what should we do?"),
    177: ("Claudio observes that Rafael really took a liking to the man.", "You really took a shine to him, huh?"),
    180: ("Rafael says the man's strength makes him a desirable ally and a worrying enemy.", "He looks so strong! I'd rather have somebody like that on our side. I sure wouldn't want him against us."),
    185: ("Claudio calls Rafael simple again but agrees to try to make a deal.", "You really do keep it simple... All right, I'll go see if I can talk him into it."),
    188: ("Al asks whether Claudio still has more to say.", "...What is it now?"),
    192: ("Claudio questions whether Al can put his vaunted strength to use in town when walking the streets takes none.", "If you stay here, when are you ever gonna use that strength you're so proud of? It doesn't take much muscle to walk around town."),
    195: ("Al reacts indignantly.", "What'd you say?"),
    199: ("Claudio says their ship would give Al plenty of chances to show what he can do, with strong enemies everywhere.", "Come aboard our ship and you'll get plenty of chances to show what you can do. There's no shortage of tough enemies out there."),
    203: ("Al remains silent.", "..."),
    207: ("Claudio baits Al by saying he needn't force himself if he doubts his ability to fight at sea. They don't want dead weight.", "Well, if you're not sure you can fight at sea, don't push yourself. We don't need dead weight on board."),
    210: ("Al sees through the obvious act, confirms they need him and agrees to sail.", "Hmph. Drop the act. You need my strength, don't you? All right. I'll come aboard."),
    214: ("Claudio declares it settled and asks his name.", "Good. That's settled. So, what's your name?"),
    217: ("He gives his short name and then his full name, with draft spelling to qualify.", "Al. Al Ferid Singh."),
}}

if __name__ == '__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105', 'B167_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 50)
