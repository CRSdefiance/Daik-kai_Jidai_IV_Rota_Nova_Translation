"""Bind the imported punctuation-mask verifier to its checksum implementation."""
from dk4tool.patch.grand_race_menu_release import sha
from scripts.analyze_rafael_B181_B187_actual_v1 import prior


if __name__ == '__main__':
    prior.sha = sha
    exact_masks = prior.exact_masks
    exec(compile(prior.SOURCE, __file__ + '::same-ordered-check-retained-source-ellipses', 'exec'), globals())
