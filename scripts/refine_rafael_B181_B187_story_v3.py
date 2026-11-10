"""Resolve the two overconstrained visual refinements and preserve exact delta checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

parent = Path(__file__).with_name('refine_rafael_B181_B187_story_v2.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'story_formatting_manuscript_v3.json': 'story_formatting_manuscript_v4.json',
    'story_visual_preferences_v3.json': 'story_visual_preferences_v4.json',
    'story_plans_v3/automatic_plans.json': 'story_plans_v4/automatic_plans.json',
    '''(181,14): (None, ("I've got a bad feeling about this...",), 'Keep Claudio’s hunch intact before his suggestion.'),''':
        '''(181,14): ("I've got a bad feeling... Let's get back to the ship early today.",
        ("I've got a bad feeling...",), 'Keep the hunch and decision to return to the ship early today.'),''',
    """(183,75): (None, ('keep up her training,',), 'Keep the instruction to continue training intact.'),""":
        '''(183,75): ("And if you can... Tell her to keep training even off the mountain and follow our teacher's instructions.",
        ('keep training',), 'Preserve his tentative request, training away from the mountain and their teacher’s instructions.'),''',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-visual-delta-proof', 'exec'), globals())
