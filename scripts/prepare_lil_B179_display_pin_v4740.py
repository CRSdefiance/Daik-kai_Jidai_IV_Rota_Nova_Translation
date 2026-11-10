"""Finish pin derivation after the preserved tool-preparation label mismatch."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B179_display_tools_v4739b')
assert not ROOT.exists()
source=Path('scripts/pin_lil_B178_display_v4692.py');text=source.read_text(encoding='utf-8')
start=text.index('tool=derive(');end=text.index('fixture_path=',start)
tool=derive(source,'scripts/pin_lil_B179_display_v4740.py',{
    text[start:end]:'tool=None\n',
    'B178':'B179','display_tools_v4692':'display_tools_v4740','display_fixture_v4691':'display_fixture_v4739',
    'source_speeches=13,progressive=12':'source_speeches=14,progressive=13',
    'Pin both complete B178 content fixtures and correct an unexecuted audit summary label.':
        'Pin both complete B179 content fixtures while preserving every earlier ROM.',
    'Corrected13-panel audit summary before execution.':'All14-panel audit counts are source bound;no C200 probe.',
})
prepared=[Path('scripts')/name for name in ['research_lil_B179_display_fixture_v4739.py',
    'run_lil_B179_display_fixture_v4741.py','audit_lil_B179_actual_v4742.py']]
assert all(p.exists() for p in prepared)
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(pin_tool=tool,prepared_tools={str(p):sha(p.read_bytes()) for p in prepared},
    stopped_preparer='scripts/prepare_lil_B179_display_tools_v4739.py',
    stopped_preparer_sha256=sha(Path('scripts/prepare_lil_B179_display_tools_v4739.py').read_bytes()),
    preserved_failure='Final pin-tool label used transformed B179 text as a source replacement key. First three tools were prepared, no ROM or metadata had changed.',
    source_speeches=14,source_commands=16,fixture_commands=25,source_A000=1,prelude_A000=4,C200=0,
    single_end508=True,no_existing_producer_overwritten=True,full_goal_complete=False))
