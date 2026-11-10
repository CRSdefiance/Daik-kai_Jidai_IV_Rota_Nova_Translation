"""Resolve one oversized phrase and one visually introduced second page."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent = Path(__file__).with_name('refine_rafael_B188_B200_town_v1.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'town_formatting_manuscript_v2.json': 'town_formatting_manuscript_v3.json',
    'town_visual_preferences_v2.json': 'town_visual_preferences_v3.json',
    'town_plans_v2/automatic_plans.json': 'town_plans_v3/automatic_plans.json',
    "(189, 12): (None, ('set my heart on fire',), 'Keep the idiom intact as she remembers a passionate love.'),":
        """(189, 12): ("That's what I love about them! It's the red of passion. Ah, I had a love in my youth that set my heart on fire.",
        ("It's the red of passion.", 'set my heart on fire.'), 'Preserve her fondness for the color, its association with passion and the love that consumed her in her youth.'),""",
    '''(194, 14): (None, ("Just what you'd expect of the duke...",), 'Keep the full reaction about the duke together.'),''':
        '''(194, 14): ("That's the duke for you... I wonder when we'll see the princess wearing that jewel.",
        ("That's the duke for you...",), "Keep her reaction to the duke's extravagance and her wish to see the princess wearing the jewel."),''',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-source-bound-visual-delta', 'exec'), globals())
