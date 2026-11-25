"""Use the frozen read-only FE observer for the declared reviewed-English fixture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/run_source_FE_geometry_probe.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    fixture=load(args.fixture);rom=Path(fixture['research_ROM']);":
        "    fixture=load(args.fixture);assert fixture['text_language']=='reviewed-English';rom=Path(fixture['research_ROM']);",
    'source_content_fixture_not_natural_story_activation=True,':
        "source_content_fixture_not_natural_story_activation=True,text_language='reviewed-English',",
})
exec(compile(source,__file__+'::same-readonly-observer-reviewed-English','exec'),globals())
