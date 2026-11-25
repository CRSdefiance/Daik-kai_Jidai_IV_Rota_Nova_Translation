"""Publish the staged armor registration directly through the verified atomic publisher."""

import inspect
from types import FunctionType

from scripts import register_armor_item_cards_v1 as armor
from scripts import register_sea_event_review_v2 as transaction
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    env = vars(transaction) | vars(armor) | {'prior': armor.base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    notes = checked_text(inspect.getsource(armor.publish), {
        'f\'and {tick}--publish-prepared{tick}. Preserve':
            'f\'and {tick}python scripts/publish_armor_item_cards_v2.py{tick}. Preserve',
    })
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.armor_item_cards.pending.json',
    })
    exec(compile(notes + '\n\n' + code, __file__ + '::atomic-armor-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    main()
