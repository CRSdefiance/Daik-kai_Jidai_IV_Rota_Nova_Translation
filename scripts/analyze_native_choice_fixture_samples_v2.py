"""Keep distinct clean-source andrelocated-storage menu offsets in the live pixel receipt."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/analyze_native_choice_fixture_samples_v1.py').read_text(encoding='utf-8'),{
    "        target=versions[-1]['object_hex'];declared=next(m for m in fixture['menus'] if m['command_hex']==target)":
        """        target=versions[-1]['object_hex'];declared=next(m for m in fixture['menus'] if m['command_hex']==target)
        manuscript_path=Path(proof['manuscript']);assert sha(manuscript_path.read_bytes())==proof['manuscript_sha256']
        source_offsets={r['source_command_offset'] for r in load(manuscript_path)['records']}
        assert len(source_offsets)==1;source_offset=next(iter(source_offsets))""",
    "source_command_offset=declared['stored_command_offset']":
        "source_command_offset=source_offset,stored_command_offset=declared['stored_command_offset']",
})
exec(compile(source,__file__+'::same-live-pixel-checks-with-both-exact-menu-offset-references','exec'),globals())
