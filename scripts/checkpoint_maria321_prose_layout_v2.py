"""Publish the final equivalent plan selection through the unchanged atomic guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/checkpoint_maria321_prose_layout_v1.py').read_text(encoding='utf-8'), {
    '`formatting_v1/page_phrase_preferences_v3.json` and `plan_v3/automatic_plans.json`':
        '`formatting_v1/page_phrase_preferences_v4.json` and `plan_v4/automatic_plans.json`',
    'Nine explicit comparisons retain better original phrase/page layouts':
        'Ten explicit comparisons retain better original phrase/page layouts',
    "In particular, the initial ship/crew's wrap has not been repaired by the unmatched ship/crew preference; review that ordinary boundary as a retention or remove the inert preference before a later final plan. Do not report it as an improvement.":
        "The inert ship/crew preference was removed after checking the actual possessive crew's token. Plan_v4 confirms every compiled body byte is identical to plan_v3; the ordinary genitive wrap is retained, not reported as a repair.",
    '**Next:** remove the inert ship/crew pair through a source-bound preference successor if needed, confirming unchanged compiled output; then prepare body-only native inputs':
        '**Next:** prepare body-only native inputs',
    "'formatting_v1/page_phrase_preferences_v4.json']], Path(__file__)]":
        "'formatting_v1/page_phrase_preferences_v4.json']], Path('scripts/checkpoint_maria321_prose_layout_v1.py'), Path(__file__)]",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-atomic-guards-final-equivalent-plan-selection', 'exec'),
        {'__file__': __file__, '__name__': '__main__'})
