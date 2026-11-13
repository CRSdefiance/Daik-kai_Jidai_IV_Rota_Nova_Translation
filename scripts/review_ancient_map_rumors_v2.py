"""Refine five spoken passages after checking the native portrait lines."""

from types import FunctionType

from scripts import review_ancient_map_rumors_v1 as original


OUTPUT = original.OUTPUT.with_name('ancient_map_rumors_context_v2.json')
DECISIONS = original.DECISIONS | {
    3661: ("It's a crimson crystal. Hold it to the light and, they say, a star-shaped pattern appears inside.",
           'Keep the crystal’s color and the report about the pattern, with the action and result in spoken order.'),
    3662: ("They say there's a diamond inside this strange crystal. They call it a jewel that eats jewels.",
           'Lead naturally into the nickname and preserve the strange crystal and reported diamond.'),
    3664: ("I hear it's a statue of a Siren, once used as a figurehead. A witch that wrecks ships, right on the bow? Hard to believe.",
           'Keep the reported figurehead and the informant’s incredulity. The witch comparison is their reaction.'),
    3665: ("They say it's a twisted horn. Some say it's a dragon's. I hear it can be made into medicine for any illness.",
           'Keep the shape, possible origin and separate medicinal rumor in three complete thoughts.'),
    3666: ("They say this shield belonged to a great king and bears a goddess's image. Sailors call it their best charm.",
           'Keep the shield’s reported owner and image, and end with the sailors’ reputation for it.'),
}


if __name__ == '__main__':
    environment = vars(original) | dict(OUTPUT=OUTPUT, DECISIONS=DECISIONS)
    FunctionType(original.main.__code__, environment)()
