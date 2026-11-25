"""Reuse the frozen read-only observer for the declared mixed page/speaker/menu fixture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/run_source_FE_geometry_probe.py').read_text(encoding='utf-8'),{
    "    fixture=load(args.fixture);rom=Path(fixture['research_ROM']);":
        "    fixture=load(args.fixture);assert fixture['text_language']=='reviewed-English' and fixture['synthetic_cross_scene_QA_sequence_not_a_story_exchange'];rom=Path(fixture['research_ROM']);",
    'source_content_fixture_not_natural_story_activation=True,':
        "source_content_fixture_not_natural_story_activation=True,text_language='reviewed-English',purpose='page-spacing-speaker-transitions-long-menu',",
})
exec(compile(source,__file__+'::same-readonly-observer-focused-mixed-fixture','exec'),globals())
