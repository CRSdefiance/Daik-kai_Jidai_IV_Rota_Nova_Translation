"""Use the frozen read-only modal observer with optional exact-frame captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/run_source_FE_geometry_probe.py').read_text(encoding='utf-8'),{
    "    fixture=load(args.fixture);rom=Path(fixture['research_ROM']);":
        "    fixture=load(args.fixture);assert fixture['text_language']=='reviewed-English';rom=Path(fixture['research_ROM']);",
    'source_content_fixture_not_natural_story_activation=True,':
        "source_content_fixture_not_natural_story_activation=True,text_language='reviewed-English',",
    "'--inputs-json',fixture['inputs'],'--capture-every','120','--dump-ram']":
        "'--inputs-json',fixture['inputs'],'--capture-every','120',*(['--capture-at',*map(str,fixture['capture_extra'])] if fixture.get('capture_extra') else []),'--dump-ram']",
})
exec(compile(source,__file__+'::same-readonly-observer-optional-exact-frame-capture','exec'),globals())
