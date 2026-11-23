"""Compile the reviewed Deck lines into the exact registered Shortage candidate."""

from types import FunctionType

from scripts import review_rafael_deck_after_trade_20261119 as review
from scripts import stage_story_tag_wraps_20261118 as template

base,native,stage,parent = template.base,template.native,template.stage,review.parent
ROOT = review.replay.ROOT/'staged_v2'
ROM,PROOF = ROOT/'Deck_After_Trade_STAGED.nds',ROOT/'stored_proof.json'
logical_end = template.logical_end


if __name__ == '__main__':
    main = template.env['main']
    scope = main.__globals__|globals()|dict(paired=review)
    scope['catalogue_membership'] = FunctionType(template.catalogue_membership.__code__,scope)
    FunctionType(main.__code__,scope)()
    proof = base.load(PROOF)
    assert proof['whole_parent_inverse'] and proof['changed_blocks'] == {'/data/SC0.DK4':[43]}
