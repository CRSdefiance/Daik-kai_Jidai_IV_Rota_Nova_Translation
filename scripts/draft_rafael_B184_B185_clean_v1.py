"""Draft both clean Silla Gold Crown inquiry scenes."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {
    184: "Rafael overhears Julian trying to charm Meihua. Meihua has heard about the crown and wants it. Julian treats her tentative willingness to consider a date as a promise and rushes off. She flatters Rafael’s party into looking as well. Her sources are secondhand and she gives no precise site.",
    185: "The party asks about the crown. The woman recalls a smooth talker who seems to have gone to the Tomb of King Muryeong. She cannot confirm his name. Her report about the crown is hearsay, and Claudio responds as if Julian may be ahead.",
}
DATA = {
    184: {
        7: ("Julian tells Meihua he lives for her radiant smile.", "Meihua, I live for that radiant smile of yours."),
        11: ("Meihua reacts with familiar, understated embarrassment.", "Oh, Julian..."),
        15: ("Rafael dryly observes that every country has people like Julian.", "...There are people like that in every country, huh?"),
        19: ("Julian expects his line to make her smile and worries she no longer likes him.", "H-huh? This is where you usually smile. You don't like me anymore?"),
        23: ("Meihua denies it and says his words usually cheer her up.", "...No, that's not it. You usually cheer me right up when you talk like that, but..."),
        27: ("She wants something badly and has been thinking about it day and night.", "The truth is, there's something I want more than anything. Lately I can't get it out of my head, day or night."),
        31: ("Julian says the look on her face does not suit her and asks what she wants so badly.", "Oh, Meihua, that look doesn't suit you at all. What is it you want so badly?"),
        35: ("She names the Silla Gold Crown, calls the name mysterious and reports it is precious.", "It's called the Silla Gold Crown. It sounds mysterious, doesn't it? I hear it's very valuable."),
        39: ("Julian worries it sounds expensive and asks where it is sold.", "Sounds expensive... I wonder if I can afford it. Where do they sell it?"),
        42: ("Meihua has heard that it isn’t sold in shops and may be in Seoul.", "That's the thing. Apparently you can't buy it in a shop. I heard it might be in Seoul, though."),
        45: ("Julian echoes the shop information and suddenly thinks of a place he leaves unnamed.", "They don't sell it in shops? Wait... Of course! It has to be there!"),
        48: ("Meihua asks whether he has an idea where to look.", "Oh? You have somewhere in mind?"),
        52: ("Julian tells her to leave it to him and vows to find the crown quickly and restore her smile.", "Leave it to me! I'll find that Silla Gold Crown as soon as I can and bring back your smile!"),
        56: ("Julian says her smile is his source of strength, then asks for a date if he gets the crown.", "Your smile is what keeps me going! Oh, if I get you the Silla Gold Crown, you'll go on a date with me, right?"),
        59: ("Meihua teases him for getting ahead of himself and agrees only to think about the date.", "You haven't even found it yet. Getting ahead of yourself, aren't you? All right, I'll think about it."),
        63: ("Julian cheers, calls her answer a promise and says he will leave for Seoul immediately.", "Yes! Don't you forget that promise! I'm off to Seoul right now!"),
        66: ("Meihua says she is counting on him, then realizes he has already left.", "I'm counting on you... Oh, he's gone already."),
        69: ("Rafael hesitantly gets her attention.", "Um..."),
        74: ("Meihua welcomes them and apologizes for not noticing them.", "Oh, welcome! I'm sorry I didn't see you there."),
        77: ("Rafael asks about the crown he overheard them discussing.", "About what you were just saying... What is the Silla Gold Crown?"),
        81: ("Meihua forgot what she was told about it and remembers only that it is beautiful.", "Well... Someone told me, but I've forgotten. All I remember is that it's supposed to be gorgeous."),
        85: ("Claudio tells FI that the conversation has made him curious.", "Huh... That's got me curious. How about you, FI?"),
        88: ("Rafael agrees, but they do not know what it is and Julian has already gone to look for it.", "A little. But we don't even know what it is, and that Julian fellow already went looking for it."),
        93: ("Meihua says she would accept the crown from Rafael too and asks if she’s not worth a present.", "Oh, I wouldn't mind getting it from you. Don't you think I'm worth a present?"),
        96: ("Claudio tells Rafael they can hardly back down after hearing that.", "You heard her. We can't back out now, can we?"),
        99: ("Rafael thinks Clau is easily led, then agrees to look and confirms Seoul.", "(Clau's so easy to talk into things.) All right, let's all look for it. Um... You said it was in Seoul?"),
        103: ("Meihua says that is what she heard but she does not know where in the city.", "That's what I heard. I couldn't tell you where in Seoul, though."),
        107: ("Claudio suggests going there, asking local people and looking around.", "Let's go there first. We can ask around once we get there."),
        111: ("Rafael says they may run into the man they just saw.", "We might run into that fellow along the way."),
    },
    185: {
        6: ("Rafael asks Clau how to begin looking into the Silla Gold Crown.", "Hey, Clau. Where do you think we should start looking for the Silla Gold Crown?"),
        11: ("Claudio thinks briefly and suggests asking someone.", "Hmm. Why don't we ask around?"),
        14: ("The woman greets the party.", "Oh, welcome!"),
        18: ("Claudio asks whether she knows of the crown.", "You ever hear of the Silla Gold Crown?"),
        21: ("She has heard of it and asks why they want to know.", "Yes, I've heard of it. Why do you ask?"),
        24: ("Rafael says they are looking for it and asks whether she has any information.", "We're looking for it. Do you know anything about it?"),
        28: ("She wonders if hunting for the crown has become fashionable because someone just asked the same question.", "...Is looking for the Silla Gold Crown the thing to do now? Someone just asked me the same thing."),
        32: ("Claudio asks whether the other visitor was a smooth talker.", "Was he... a bit of a smooth talker?"),
        35: ("She could not tell whether he was after information or flirting with her.", "Well, I couldn't tell whether he wanted information or wanted to charm me."),
        38: ("Rafael asks whether it was Julian and says they met him before in Hangzhou.", "Was his name Julian, by any chance? We met him in Hangzhou."),
        43: ("She does not remember the name, apologizes, and says he seems to have gone to the named tomb.", "Was that his name? I'm sorry, I don't remember. I think he went to the Tomb of King Muryeong, though."),
        46: ("Claudio echoes the tomb’s name in surprise.", "The Tomb of King Muryeong?"),
        50: ("She describes it as a nearby historic site and says she has heard the crown is there.", "It's a historic site near here. I've heard the Silla Gold Crown is there."),
        54: ("Claudio realizes someone is ahead and urges FI to hurry.", "Uh-oh. He beat us to it! Come on, FI, we'd better hurry!"),
    },
}
if __name__ == '__main__':
    seal('work/analysis/Rafael_B181_B200_clean_20261105', 'B184_B185_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 43)
