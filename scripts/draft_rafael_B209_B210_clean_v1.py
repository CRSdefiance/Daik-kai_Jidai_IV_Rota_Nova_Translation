"""Draft Ian's book offer and the clean Namahage encounter."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {
    209: "A seller calls out to Ian and offers an Indian classic for 8,500. If he buys it, she wishes him a romance like the one in the book and he declines the idea. Refusing prompts her to find another buyer. In the branch where Ian cannot afford it, she gives it to him and vanishes, prompting his speculation. Preserve the ask to the admiral, the three choice meanings and the precise Charm notice.",
    210: "An unseen voice repeats its call for misbehaving children, then asks Yukihisa directly. He recognizes Namahage and denies wrongdoing. He first treats the encounter as a dream. Another speaker reacts to something apparently present afterward, and Yukihisa intends to give it to the admiral in the morning. Preserve the repeated caller, the uncertainty and the unnamed object.",
}
DATA = {
    209: {
        5: ("The seller calls out to the handsome man over there.", "Excuse me, handsome!"),
        9: ("Ian asks whether she means him.", "Do you mean me?"),
        14: ("She asks if he would buy a book for 8,500 gold.", "Would you buy this book for 8,500 gold?"),
        17: ("Ian asks what kind of book it is.", "What kind of book is it?"),
        21: ("She says it is an Indian classic about the love between a heavenly maiden and an immortal sage and asks if he is interested.", "An Indian classic. It's a love story about a heavenly maiden and an immortal sage. Interested?"),
        24: ("Ian asks the admiral what to do.", "What do you think, Admiral?"),
        45: ("Ian decides to accept the offer.", "I'll take it."),
        49: ("The seller wishes that he could fall in love with a heavenly maiden too.", "Maybe you'll fall in love with a heavenly maiden yourself."),
        53: ("Ian says he is afraid he has no interest.", "I'm afraid I'm not interested."),
        57: ("The seller reacts with teasing dismay and says it is a shame for a man that handsome.", "Oh, what a shame. And such a handsome man, too."),
        65: ("Ian politely declines the purchase.", "No, I think I'll pass."),
        69: ("The seller is disappointed and says she will find another buyer.", "Is that so? What a pity. I'll find someone else to buy it."),
        75: ("Ian says he would like to buy it but does not have that kind of money.", "I'd like to buy it, but I don't have that kind of money."),
        78: ("The seller acknowledges his explanation.", "I see."),
        82: ("Ian apologizes for disappointing her.", "I'm sorry to disappoint you."),
        86: ("She decides to give him the book.", "Then you can have it."),
        90: ("Ian reacts in surprise.", "What?!"),
        94: ("The seller chuckles and says she would like to fall in love with someone like him next time.", "Heh heh... Next time, I'd like to fall in love with a man like you."),
        98: ("Ian stammers that she has vanished.", "Sh-she's gone..."),
        102: ("Ian wonders if she was a heavenly maiden and chides himself for the foolish thought.", "Could she have been a heavenly maiden...? Hah. What a foolish thought."),
        110: ("The system announces that Ian's Charm increased by one.", "Ian's Charm went up by 1!"),
    },
    210: {
        10: ("An unseen caller repeatedly asks if any misbehaving children are around.", "Any naughty children here? Any naughty children?"),
        14: ("The same call repeats.", "Any naughty children here? Any naughty children?"),
        18: ("The caller asks if the person addressed is a naughty child.", "Are you a naughty child?"),
        22: ("Yukihisa demands to know who is there.", "Who's there?"),
        26: ("The caller repeats the question.", "Are you a naughty child?"),
        30: ("Yukihisa recognizes the caller as Namahage.", "...You're Namahage!"),
        34: ("The caller asks the same question again.", "Are you a naughty child?"),
        38: ("Yukihisa cannot recall having done anything wrong.", "I can't recall doing anything wrong."),
        42: ("The caller draws out a subdued acknowledgment.", "I see..."),
        49: ("Yukihisa is silent.", "..."),
        53: ("Yukihisa takes the experience for a dream.", "A dream, then."),
        65: ("The other speaker cries out and asks what the thing is.", "Whoa! What is this thing?!"),
        72: ("Yukihisa reacts with surprise.", "Hmm?!"),
        76: ("Yukihisa pauses silently.", "..."),
        80: ("Yukihisa observes that strange things do happen.", "Strange things do happen."),
        84: ("Yukihisa says he will give the object to the admiral in the morning.", "I'll give this to the admiral in the morning."),
        95: ("The other speaker still insists on knowing what it is.", "...But what is it?!"),
    },
}
CHOICES = {
    (209,0): ("Tell Ian to go ahead and buy the offered book.", "Buy"),
    (209,1): ("Decline the offered book.", "Don't Buy"),
    (209,2): ("Leave the decision to Ian.", "Your Call"),
}


if __name__ == '__main__':
    seal('work/analysis/Rafael_B201_B220_clean_20261106', 'B209_B210_clean_drafts_v1.json', DATA, CONTEXT, CHOICES, __file__, 41)
