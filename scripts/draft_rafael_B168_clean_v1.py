"""Draft the complete clean B168 recruitment and trading exchange before opening current English."""
from scripts.seal_clean_independent_drafts_v1 import seal

CONTEXT = {168: (
    "Angelo mistakes Rafael for a junior crew member, and Claudio answers with a gendered taunt. The two trade barbs "
    "until Rafael identifies himself and stops the confrontation. Angelo admits he provoked them, and Claudio pivots "
    "from anger to inviting him aboard as a navigator. The linked trading exchange distinguishes a well-developed "
    "Mediterranean with high barriers to entry from the potential of overseas trade. Preserve Angelo's estimates as "
    "his own, without turning his claim into guaranteed earnings."
)}

DATA = {168: {
    5: ("Angelo calls out to Rafael as a boy in a condescending way.", "Hey, you! Kid!"),
    9: ("Rafael asks whether the slight was directed at him.", "You mean me?"),
    14: ("Angelo assumes Rafael is a crew boy doing errands and says he was wondering whether the ship needed a navigator.", "Yeah, you. You're on this crew, right? A powder monkey, or some other errand boy? I was wondering if the ship needed a navigator."),
    18: ("Angelo wants to meet the captain, doubts an introduction from a low-ranking boy will do any good and laughs.", "I'd like to see the captain. Though I doubt an introduction from the likes of you would get me anywhere. Ha ha!"),
    22: ("Angelo offers a casual apology and dismisses his request.", "Pardon me. Forget I asked."),
    26: ("Claudio retorts with a gendered insult about Angelo and challenges whether he knows whose ship this is.", "Hey, princess! Just whose ship do you think this is?"),
    30: ("Angelo indignantly repeats the gendered taunt and points out that Claudio is wearing earrings.", "...Princess?! I'm no princess! You're the one wearing earrings!"),
    33: ("Claudio takes offense, says his earring is a warrior's mark and threatens a fight.", "What'd you say, you punk?! This is a warrior's mark! You wanna fight?!"),
    37: ("Angelo asks why Claudio is angry and scoffs at someone whose brains seem to be made of muscle.", "What's got you so mad? This is the trouble with muscleheads."),
    41: ("Claudio stretches out an enraged threat.", "Why, you little...!"),
    45: ("Rafael orders Claudio to stop, using his familiar nickname.", "Stop it, Clau!"),
    50: ("Rafael says he is no mere boy and introduces himself by given and family names as admiral of the ship.", "...I'm no kid. My name is FI FA. I'm the admiral of this ship."),
    55: ("Angelo exclaims in Italian and reacts to Rafael's rank in disbelief.", "Mamma mia! You're the admiral?!"),
    59: ("Angelo realizes his mistake and asks Rafael's forgiveness.", "...I see. That was rude of me. I'm sorry. Forgive me."),
    62: ("Surprised by the apology, Rafael begins apologizing for his own companion's insults.", "Huh...? Oh, no. I'm the one who should apologize. My friend said some terrible things..."),
    67: ("Claudio vehemently tells Rafael he has nothing to apologize for, using his given name.", "FI! You've got nothing to apologize for!"),
    70: ("Rafael starts to explain but is interrupted.", "But..."),
    75: ("Angelo sides with Claudio. He catches himself calling diligent people plain, says he cannot resist teasing them and apologizes.", "No, he's right about this. When I see someone dull... I mean, someone working hard, I can't help needling them. I'm sorry."),
    78: ("Claudio calls him odd and says he should not have said it in the first place if he was going to apologize.", "You sure are a strange one. If you're gonna apologize, why say it in the first place?"),
    82: ("Angelo says he truly was rude and prepares to leave.", "I really was out of line. Well, see you."),
    85: ("Claudio tells him to wait.", "Hey, wait!"),
    89: ("Angelo gives a questioning reaction.", "...?"),
    93: ("Claudio confirms that Angelo said he wanted to be a navigator.", "You said you wanted to be a navigator, right?"),
    96: ("Angelo admits he did, but hesitates.", "Well, yeah, but..."),
    100: ("Claudio chuckles at the idea and calls to Rafael for agreement.", "Heh heh. Well, then... What do you say, FI?"),
    103: ("Rafael says having more companions is fun and invites Angelo to sail with them.", "Sure. The more of us, the merrier. Want to come with us?"),
    107: ("Angelo stammers in surprise and asks if they are sure.", "H-hey! Are you sure about this?"),
    110: ("Claudio confirms, introduces himself by full name and offers a friendly greeting.", "That's the idea. I'm Claudio Manaus. Good to have you with us."),
    114: ("Angelo says the others are odd themselves and gives his full name.", "...You lot are pretty strange yourselves. I'm Angelo Puccini."),
    117: ("Rafael addresses Angelo and asks whether he is confident in his skills as a navigator.", "Well, Angelo, if you want to navigate, you're confident you can do it, right?"),
    122: ("Claudio says that anybody willing to pick a fight with him has nerve.", "Well, he's got guts if he's willing to pick a fight with me."),
    126: ("Angelo downplays the compliment with a vague agreement.", "Yeah, something like that."),
    130: ("Rafael warmly looks forward to working with Angelo.", "Glad to have you aboard, Angelo!"),
    134: ("Angelo warmly accepts and addresses Rafael by his rank.", "Same here, Admiral!"),
    154: ("Angelo tells the admiral he cannot expect big trading profits by sticking to small deals in the Mediterranean.", "By the way, Admiral, if you wanna make money trading, you can't just make little deals here in the Mediterranean."),
    158: ("Rafael asks why, taken aback.", "Huh? Why not?"),
    171: ("Julio is impressed that Angelo understands the matter.", "Oh! You know what you're talking about, I see!"),
    174: ("Rafael responds with puzzled silence.", "...?"),
    182: ("Angelo says developed trade routes look attractive, but the major powers have already developed the region, leaving little room for gain.", "The trade routes here look good at first. They're well established, but the big powers have already built up the place. There's not much left in it for us."),
    186: ("Rafael agrees after thinking it over, citing high contract fees and investment costs and little room to enter the market.", "Hmm. Now that you mention it, the contract fees and investments are awfully high. There's hardly any room for us to get in."),
    190: ("Angelo urges looking overseas, where Africa and the New World have room to grow and a small investment can bring a large return.", "That's why we have to look farther afield. Africa and the New World still have room to grow. A little investment can bring a big return."),
    193: ("Angelo says the unusual goods should make even round trips with Europe highly profitable.", "They sell goods you don't see every day. Just going back and forth to Europe ought to bring in a lot of money."),
    196: ("Rafael is impressed that Angelo also understands trade.", "Wow. You know a lot about trade, too."),
    200: ("Angelo brushes off the praise. He is repeating what he heard from sailors.", "Aw, quit it. I'm just passing on what other sailors told me."),
    211: ("Julio insists that Angelo is right.", "No, no. He's quite right."),
    214: ("Julio explains that more cargo holds do not help merchants move large volumes in Europe if they cannot secure market share.", "Even if you buy a ship and get more cargo holds, it's hard to gain market share in Europe. That means you can't trade large quantities at once."),
    220: ("Rafael realizes they should follow earlier Portuguese seafarers by looking outward, then decides to try Africa.", "I see. We should follow the example of the Portuguese who sailed before us and look beyond our own waters. All right, let's try Africa!"),
}}

if __name__ == '__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105','B168_clean_drafts_v1.json',DATA,CONTEXT,{},__file__,47)
