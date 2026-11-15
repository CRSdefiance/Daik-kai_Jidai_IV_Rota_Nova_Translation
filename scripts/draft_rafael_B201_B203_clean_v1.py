"""Draft the next three complete clean-Japanese commodity scenes."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {
    201: "Two polite collectors discuss a newly acquired piece of china and complain about fashionable collecting. Two opportunists overhear. Their private talk reveals that one of them has already sold worthless china to the pair at an astonishing price. They decide to approach them again. Keep the collectors' manners, the shift in register and the prospective Hamburg notice.",
    202: "Two men gossip about the master of the house and his unexplained illness. The first repeats a rumor that a commercially available remedy cured him at once and now has a cure-all reputation. The second is initially skeptical, then agrees to go look for it. All the claims about the remedy belong to the speakers, separate from the Havana notice.",
    203: "The shopkeeper likes the color but is hesitant about buying more dye. The other speaker pushes him to act before other shops buy it all, argues that the color will be profitable and wears down his objections. The repeated uncertainty and repeated assurance form a comic refrain.",
}
DATA = {
    201: {
        6: ("The collector finally acquired the item the other already knows about.", "I finally got my hands on it the other day."),
        9: ("The other collector asks if it was the china.", "Oh, the china?"),
        13: ("The first confirms it and says the piece was as fine as he expected.", "Yes. It was every bit as fine as I'd hoped."),
        16: ("The second is impressed and would like to see it.", "Splendid. I should very much like to see it."),
        19: ("The first warmly invites him to visit his home.", "Of course! Please, do come by my home for a look."),
        22: ("The second says good pieces have become hard to acquire amid the recent collecting fashion.", "With everyone collecting china these days, it's getting harder to find a good piece."),
        26: ("The first says people who cannot judge its value are buying it up just because it is in fashion.", "So I hear. People who don't know what any of it is worth are buying it up just because it's fashionable."),
        30: ("The second is annoyed by the situation.", "What a nuisance."),
        34: ("The first agrees emphatically.", "Quite so."),
        38: ("A nearby speaker tells his companion to look at the men over there.", "Hey, take a look at those men over there."),
        42: ("The companion confirms the pair and asks what about them.", "Those two? What about 'em?"),
        46: ("The first says they recently bought worthless china from him for an incredible price.", "The other day they paid me a ridiculous price for some china that wasn't worth a thing."),
        49: ("The companion calls them good customers and suggests approaching them because he is short on money.", "Well, well. Good customers, huh? I'm a little short on cash. Why don't we go have a word with them?"),
        53: ("The first likes the suggestion.", "I like the sound of that."),
        57: ("The companion decides to go.", "That settles it. Come on."),
        61: ("The first calls out to get a collector's attention with ingratiating deference.", "Good sir!"),
        65: ("The notice predicts china may become fashionable in Hamburg.", "China may catch on in Hamburg."),
    },
    202: {
        24: ("One man opens by asking whether the other has heard.", "Hey, did you hear?"),
        28: ("The other asks what he means.", "Hear what?"),
        32: ("The first identifies the master of this house as the subject.", "About the master of the house."),
        36: ("The other asks if he means the illness with no known cause.", "You mean that illness nobody could explain?"),
        40: ("The first confirms it.", "That's the one."),
        44: ("The second says everyone knows about that.", "Everybody knows about that."),
        48: ("The first asks whether he knows what happened afterward.", "Do you know what happened after that?"),
        52: ("The second echoes the question.", "After that?"),
        56: ("The first reports an ordinary medicine from a shop cured the illness at once.", "They say a remedy you can buy in a shop cleared it right up."),
        59: ("The other incredulously asks if a store-bought remedy cured the unexplained illness.", "Nobody knew what was wrong with him, and something from a shop cured it?"),
        63: ("The first affirms and calls the story extraordinary.", "That's right. Some story, huh?"),
        67: ("The second agrees hesitantly and asks whether it is true.", "Yeah... But is it true?"),
        71: ("The first says it apparently is true and the medicine has a reputation for curing all ailments.", "Apparently. And now people are saying it cures everything."),
        74: ("The second is impressed and says he wants some if it is that good.", "Wow! If it's that good, I want some too."),
        77: ("The first suggests going to buy it.", "Want to go buy some?"),
        81: ("The other agrees and urges him to go.", "Sure. Let's go!"),
        85: ("The notice predicts medicine may become fashionable in Havana.", "Medicine may catch on in Havana."),
    },
    203: {
        53: ("The shopkeeper says that particular dye is the only way to achieve this color.", "That dye really is the only way to get this color."),
        56: ("The other agrees and warns that rival shops will buy it all if they wait.", "Exactly. If we don't buy some now, the other shops will buy it all up."),
        60: ("The shopkeeper hesitates.", "Well, but..."),
        64: ("The other rebukes his lack of urgency and says waiting until it is sold out will be too late.", "Why take your time? Once it's sold out, it'll be too late."),
        68: ("The shopkeeper doubts that it will sell out even if they do not rush.", "I doubt it'll sell out just because we don't rush out and buy it now."),
        72: ("The other disagrees, citing its popularity and expecting a quick sellout.", "It absolutely will! It's so popular it'll be gone in no time."),
        76: ("The shopkeeper is still doubtful.", "You think so?"),
        80: ("The other answers emphatically.", "I do!"),
        84: ("The shopkeeper gives in and leaves it to the other speaker.", "All right, I'll leave it to you."),
        88: ("The other tells the shopkeeper not to sulk and promises profit if they can secure that color.", "Come on, don't sulk. If we can get our hands on that color, we'll make a profit for sure."),
        92: ("The shopkeeper repeats his doubt.", "You think so?"),
        96: ("The other repeats the assurance with more insistence.", "I'm telling you, we will!"),
        100: ("The notice predicts dyes may become fashionable in Calicut.", "Dyes may catch on in Calicut."),
    },
}


if __name__ == '__main__':
    seal('work/analysis/Rafael_B201_B220_clean_20261106', 'B201_B203_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 47)
