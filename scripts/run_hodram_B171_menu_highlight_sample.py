"""Read-only dense video sampling of the initial short-menu highlight window."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/run_hodram_B171_B190_actual.py').read_text(encoding='utf-8'), {
    "    'source_content_fixture_not_natural_story_activation=True,':":
    """    "'--inputs-json',fixture['inputs'],'--capture-every','120','--dump-ram']":
        "'--inputs-json',fixture['inputs'],'--capture-every','120','--capture-window','4480','4720','--dump-ram']",
    'source_content_fixture_not_natural_story_activation=True,':""",
})
exec(compile(source, __file__ + '::same-observer-dense-readonly-capture-window', 'exec'), globals())
