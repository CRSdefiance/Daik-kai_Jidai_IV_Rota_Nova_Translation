"""Reuse the original read-only modal observer andcapture requested cursor-state frames."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/run_source_FE_geometry_probe.py').read_text(encoding='utf-8'),{
    "    try:harness.main()":
        "    if fixture.get('capture_extra'):sys.argv.extend(['--capture-at',*map(str,fixture['capture_extra'])])\n    try:harness.main()",
})
exec(compile(source,__file__+'::same-ordinary-coldboot-readonly-observer-with-extra-QA-captures', 'exec'),globals())
