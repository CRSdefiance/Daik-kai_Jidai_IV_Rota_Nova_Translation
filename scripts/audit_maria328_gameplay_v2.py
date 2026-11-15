"""Keep separate source/stored menu offsets in the unchanged actual-coverage audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/audit_maria328_gameplay_v1.py').read_text(encoding='utf-8'),{
    "assert [s['frame'] for s in menus['menu_samples'] if s['source_command_offset']==next(m['stored_command_offset'] for m in menus['menus'] if m['block']==87)]==[6000,6120]":
        "assert [(s['source_command_offset'],s['stored_command_offset'],s['frame']) for s in menus['menu_samples'] if s['source_command_offset']==816]==[(816,796,6000),(816,796,6120)]",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-coverage-guards-distinct-source-andstored-menu-offsets','exec'),globals())
