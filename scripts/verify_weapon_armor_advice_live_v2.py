"""Verify both footer labels in the equippable item view."""

from inspect import getsource

from scripts import verify_weapon_armor_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(getsource(previous.verify_live), {
        "footer = find_mask(font, 'Advice', returned, (152, 365, 209, 384))":
            "footer = [find_mask(font, 'Advice', returned, (102, 365, 160, 384)),\n"
            "                  find_mask(font, 'Equip', returned, (160, 365, 211, 384))]",
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::equippable-item-footer', 'exec'), env)
    env['verify_live']()


if __name__ == '__main__':
    main()
