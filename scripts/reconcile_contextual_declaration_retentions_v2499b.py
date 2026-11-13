"""Correct a nonexistent case-sensitive authoring substitution before reconciliation."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_declaration_retentions_v2499.py')
source=OLD.read_text();line=" 'historical-only battle/return binding':'historical-only cancellation/battle-transition binding',\n";assert source.count(line)==1;source=source.replace(line,'');exec(compile(source,__file__,'exec'),globals())
