"""Review Julio's complete on-deck exchange at its ordinary post-Trade entry."""

from types import FunctionType

from scripts import replay_rafael_deck_after_trade_20261119 as replay
from scripts import review_rafael_deck_lesson_20261119 as earlier

base,native,parent = earlier.base,earlier.native,replay.parent
ROOT = replay.ROOT/'source_review_v2'
SOURCE,OUTPUT = ROOT/'paired_source.json',ROOT/'contextual_review.json'
BLOCKS,CONTEXT,GATES,TOKEN,logical,intake = (getattr(earlier,k) for k in ('BLOCKS','CONTEXT','GATES','TOKEN','logical','intake'))
LESSON = {
    7: ('Julio checks that Rafael is following and introduces the work that he and the other navigators do.',
        'Keep the familiar question. Let Julio include himself in the lesson in the same sentence and lead naturally into assigning duties.',
        "Still with me? I'll show you what we do as navigators.", ('Still with me?', "I'll show you", 'what we do as navigators.')),
    11: (earlier.LESSON[11][0], 'Keep the simple statement of the admiral’s responsibility. The next turn shows how to do it.', None, ()),
    14: (earlier.LESSON[14][0], 'Retain the reason for dividing the work and the exact Deck View command that Julio uses to demonstrate it.', None, ()),
    17: earlier.LESSON[17],
    20: (earlier.LESSON[20][0],
        'Keep the Sail Handler title, the exact adjustment and the one-per-mast rule. Give the staffing rule a complete clause.',
        "Next is the Sail Handler. They adjust the sails' angle to the wind. Each mast needs one.",
        ('Sail Handler.', 'Each mast needs one.')),
    23: (earlier.LESSON[23][0],
        'Keep the instruction direct and put turning the ship quickly in one phrase. The next turn supplies the battle example.',
        'To turn the ship quickly, count on your Helmsman.', ('turn the ship quickly', 'count on your Helmsman.')),
    27: earlier.LESSON[27],
    30: (earlier.LESSON[30][0], 'Keep the optional First Mate and both benefits. The separate closing compliment is Julio’s, and the complete explanation still fits one page.', None, ()),
    33: (earlier.LESSON[33][0], 'Keep Auto Move as the exact command and let the two coordinates stay together. The short final sentence conveys Julio’s judgment of the job.', None, ()),
    37: (earlier.LESSON[37][0], 'Keep the two distinct reports from the Lookout, ship affiliation and town conditions, in Julio’s everyday language.', None, ()),
    40: (earlier.LESSON[40][0], 'The cautious “about all” stays, and the invitation to try other jobs leads to the separate system instruction.', None, ()),
    45: earlier.LESSON[45],
}


if __name__ == '__main__':
    FunctionType(earlier.main.__code__,vars(earlier)|globals())()
