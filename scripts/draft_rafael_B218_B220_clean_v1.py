"""Draft the earring pitch, the Minotaur rumor and Cristina's sword lead."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {
    218: "A shady seller pitches ceramic earrings to Rafael, Claudio and Cristina. The seduction legend and the claims about information at the tavern are his sales talk. Cristina questions both their point and his attitude. Keep the two decisions and each distinct rejection.",
    219: "Emilio asks for the Minotaur's Axe because he wants to grow stronger. Rafael is amused that he wants something other than food. Emilio knows only a local rumor. Rafael says he might look for it, without promising it to him.",
    220: "An older man says Cristina reminds him of a formidable woman pirate. He means her bearing rather than her looks. His account of the sword lost in a Caribbean battle is hearsay, with no exact site or search method. The story ends with Cristina's private curiosity and a separate Charm notice.",
}
DATA = {
    218: {
        5: ("The seller says he has something good and asks if they want to buy it.", "I've got something good. Interested in buying?"),
        9: ("Cristina asks what he means by something good.", "What have you got?"),
        13: ("The seller presents the item.", "Right here."),
        17: ("Claudio recognizes earrings.", "Oh, earrings."),
        21: ("The seller confirms they are ceramic earrings.", "That's right. Ceramic earrings."),
        25: ("Rafael doubts they are particularly rare.", "They don't look all that rare to me."),
        29: ("The seller chuckles and insists they are no ordinary earrings.", "Heh heh. These aren't just any earrings."),
        33: ("Cristina asks what makes them different.", "What's so different about them?"),
        37: ("The seller says they belonged to a dancer reputed to be the world's greatest and cites a legend that dancing in them will charm any man.", "They belonged to a dancer people called the greatest in the world. Legend says you could charm any man if you danced in these."),
        40: ("Claudio has no use for them himself and asks Cristina.", "They wouldn't do me much good. How about you, Cristina?"),
        44: ("Cristina might consider it if they made her a better dancer, but no man is worth that much effort to attract.", "I'd think about it if they made me a better dancer. But there's no man I'd go to that much trouble to impress."),
        48: ("The seller says there are other uses. He claims giving them to a woman at the tavern would win her over at once.", "You don't have to wear them yourself. Give them to a woman at the tavern and she'll fall for you in no time. You'll be on good terms just like that."),
        51: ("Cristina repeats the idea of getting friendly and asks what purpose it would serve.", "Get friendly? And what would you do then?"),
        55: ("The seller claims someone on good terms with the women at the tavern can learn all kinds of things because they are well informed.", "Once you're on good terms, you can hear all sorts of things. The women at the tavern know what's going on."),
        70: ("The seller seeks agreement and asks whether they understand the point now.", "See? Now you get it."),
        73: ("Rafael decides to take the item.", "All right, I'll take them."),
        78: ("The seller asks for 9,000 gold and claims the price is already a sacrifice and cannot drop by even a coin.", "That'll be 9,000 gold. I'm practically giving them away. I won't take a coin less."),
        93: ("The seller praises their judgment and presents the ceramic earrings.", "You've got a good eye. Here are your ceramic earrings."),
        100: ("The seller decides he misjudged them, dismisses them and withdraws the sale.", "...Looks like I had you wrong. Get lost. I'm not selling."),
        103: ("Claudio objects to his tone and points out that the seller approached them first.", "What's with the attitude? You're the one who came up to us!"),
        106: ("The seller sneers that he has no business with cheapskates and orders them away.", "Hmph. I don't deal with cheapskates. Get lost already."),
        109: ("Claudio says they have no business with him either and tells FI to leave with him.", "Fine by me! Come on, FI, let's go!"),
        119: ("The seller refuses to sell to someone who still cannot understand after all that explanation and dismisses them.", "...If you still don't get it after all that, I'm not selling to you. Get lost."),
        122: ("Cristina is baffled by his point and calls his behavior unpleasant.", "Excuse me? What's he even trying to say? What an unpleasant man."),
    },
    219: {
        5: ("Emilio draws out the title Admiral and says there is a weapon he wants.", "Admiral... There's a weapon I want."),
        8: ("Rafael is surprised.", "Huh?"),
        13: ("Emilio explains that he wants a weapon so he can get stronger too.", "You know, I want to get stronger too. That's why I want a weapon."),
        16: ("Rafael says wanting something besides food is unusual for Emilio and asks what the weapon is called.", "You don't usually ask for anything but food. What's the weapon called?"),
        20: ("Emilio names the Minotaur's Axe.", "The Minotaur's Axe!"),
        24: ("Rafael thinks the name sounds powerful and asks where it is.", "Sounds pretty powerful. So where is it?"),
        28: ("Emilio does not know. He has heard the Minotaur was on this island long ago, and knows nothing else.", "I dunno. I heard the Minotaur was on this island a long time ago. That's all I know."),
        32: ("Rafael says there is little to go on, but may look for it if he feels like it.", "That's not much to go on... Well, maybe I'll look for it if I feel like it."),
        36: ("Emilio cheers.", "Yay!"),
        40: ("Rafael reiterates that he will only look if he feels like it.", "Only if I feel like it, okay?"),
        45: ("Emilio cheers anyway.", "Still. Yay!"),
        49: ("Rafael hesitates and clarifies that he did not promise to give it to Emilio.", "You know... I never promised I'd give it to you."),
        53: ("Emilio groans in disappointment.", "Aww..."),
    },
    220: {
        5: ("The older man calls out to a passerby and asks for a moment.", "Excuse me. Could I have a moment?"),
        9: ("Cristina asks if he means her.", "Me?"),
        13: ("The man confirms he does.", "Yes, you."),
        17: ("Cristina asks what he wants.", "What is it?"),
        21: ("Looking at Cristina reminds him of a formidable woman pirate from long ago. He stresses how strong she really was.", "Looking at you reminds me of a woman pirate I knew of long ago. She really was formidable."),
        25: ("Cristina asks if they look that much alike, perhaps in their features.", "Do I look that much like her? Is it the face?"),
        28: ("The man means her presence rather than her face and wonders if it is because she looks strong too.", "It's more the way you carry yourself. Maybe it's because you look strong too."),
        32: ("Cristina asks whether she really seems that way and resolves to take after the pirate and grow stronger.", "Do I really? Then I'd better follow her example and get stronger."),
        36: ("The man asks if she wants to grow stronger and suggests looking for the sword the pirate had.", "Oh, you want to get stronger, do you? Then how about looking for that pirate's treasured sword?"),
        40: ("Cristina repeats the idea of the pirate's treasured sword.", "The pirate's treasured sword?"),
        44: ("The man says it is the sword she is said to have used, but he does not know its value.", "Yes. It's the sword she was said to use. I don't know what it might be worth."),
        48: ("Cristina is intrigued and asks where it is.", "Hmm. That's interesting. So where's the sword?"),
        51: ("The man says it is in the Caribbean.", "In the Caribbean."),
        55: ("Cristina repeats the location thoughtfully.", "The Caribbean..."),
        59: ("He says the pirate took part in a major naval battle there and is said to have lost the sword during the fighting.", "There was a great sea battle in the Caribbean. She fought in it, and the story goes she lost the sword in the fighting."),
        62: ("Cristina waits for more.", "And?"),
        66: ("The man says that is all.", "That's all."),
        70: ("Cristina is taken aback by the lack of detail and asks how she is supposed to find it.", "That's all? Then how am I supposed to find it?"),
        73: ("The man says he cannot answer, but has a feeling she could find it.", "How would I know? I just have a feeling you could find it."),
        76: ("Cristina accepts that and says she will remember it.", "I see. Well, I'll keep it in mind."),
        79: ("The man says he is sure she could find it and wishes her luck.", "Yes. I'm sure you could find it. Good luck to you."),
        82: ("Cristina thanks him.", "Thank you."),
        86: ("Cristina privately thinks about the pirate's sword lost in the Caribbean and wants to see it.", "(A pirate's treasured sword, lost in the Caribbean... I'd like to see that.)"),
        90: ("The system announces one point of Charm gained by Cristina.", "Cristina's Charm went up by 1!"),
    },
}
CHOICES = {}

if __name__ == '__main__':
    from pathlib import Path
    from scripts.audit_story_glyph_consistency import load
    root=Path('work/analysis/Rafael_B201_B220_clean_20261106')
    offered={
        (836,0): ('Respond that the use makes sense.', 'I see'),
        (836,1): ('Ask why that would matter.', 'So what?'),
        (1006,0): ('Accept the stated price and buy the earrings.', "I'll take them!"),
        (1006,1): ('Object that the price is high.', 'Too expensive...'),
    }
    choices=[r for r in load(root/'clean_choice_objects.json')['records'] if r['block']==218]
    assert {(r['source_command_offset'],r['source_index']) for r in choices}==offered.keys()
    # Each menu needs its own captions even where the button index is the same.
    from scripts.seal_clean_independent_drafts_offset_v1 import seal_offsets
    seal_offsets(root,'B218_B220_clean_drafts_v1.json',DATA,CONTEXT,offered,__file__,65)
